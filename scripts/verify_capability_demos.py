"""Check every gallery scene in real Chrome, replay pixels, controls and MP4s."""
import argparse
import functools
import json
import subprocess
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import livepanel as lp
from check_frames import pixel_diff, TOL_PIXELS

OUT = lp.ROOT / 'examples/capability-demos'
EXPECTED_THEMES = {'terminal-dark', 'light-pastel', 'terminal-classic', 'pastel-classic'}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def editorial_layout(br):
    """Measure authored SVG text after font loading and every transform."""
    return br.eval('''(()=>{
      const stage=document.getElementById('stage'),sr=stage.getBoundingClientRect(),
            scale=sr.width/parseFloat(stage.style.width),texts=[],problems=[];
      for(const n of stage.querySelectorAll('[data-component-text],[data-terminal-text]')){
        if(n.closest('[data-component="drone"]'))continue;
        const b=n.getBoundingClientRect();if(!b.width||!b.height)continue;
        const t={l:b.left,r:b.right,t:b.top,b:b.bottom,s:n.textContent,n};texts.push(t);
        if(b.left<sr.left-.5*scale||b.top<sr.top-.5*scale||b.right>sr.right+.5*scale||b.bottom>sr.bottom+.5*scale)
          problems.push('outside scene: '+t.s);
        const panel=n.closest('[data-panel]'),border=panel&&panel.querySelector('[data-panel-border]');
        if(border){const r=border.getBoundingClientRect();
          if(b.left<r.left-.5*scale||b.top<r.top-.5*scale||b.right>r.right+.5*scale||b.bottom>r.bottom+.5*scale)
            problems.push('outside editorial panel: '+t.s);
        }
      }
      for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){
        const a=texts[i],b=texts[j];
        if(Math.min(a.r,b.r)-Math.max(a.l,b.l)>1.5*scale&&Math.min(a.b,b.b)-Math.max(a.t,b.t)>1.5*scale)
          problems.push('editorial text overlap: '+a.s+' / '+b.s);
      }
      return problems;
    })()''')


def platform_fonts(br, style='diagram'):
    """CDP proves that the embedded font files rendered the visible glyphs."""
    br.cmd('DOM.enable')
    br.cmd('CSS.enable')
    root = br.cmd('DOM.getDocument', {'depth': 1})['root']['nodeId']
    result = {}
    for family in (['LP Mono'] if style == 'terminal' else ['LP Sans', 'LP Serif', 'LP Mono']):
        selector = f'#stage text[font-family*="{family}"]'
        if style == 'terminal':
            selector = f'#stage [data-terminal-shell] text[font-family*="{family}"]'
        if family == 'LP Sans':
            selector += ':not([font-family*="LP Serif"]):not([font-family*="LP Mono"])'
        node = br.cmd('DOM.querySelector', {'nodeId': root,
                      'selector': selector})['nodeId']
        assert node, f'No authored text for {family}'
        faces = br.cmd('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
        assert any(f['isCustomFont'] and f['familyName'] == family for f in faces), faces
        result[family] = faces
    selector = '#stage text[data-component-text],#stage text[data-terminal-text]'
    nodes = br.cmd('DOM.querySelectorAll', {'nodeId': root, 'selector': selector})['nodeIds']
    texts = br.eval('Array.from(document.querySelectorAll(' + json.dumps(selector) + ')).map(n=>n.textContent)')
    visible = br.eval('Array.from(document.querySelectorAll(' + json.dumps(selector) + ')).map(n=>!!n.getBoundingClientRect().width)')
    checked = 0
    for node, text, rendered in zip(nodes, texts, visible):
        if not rendered:
            continue
        if not any('\u4e00' <= c <= '\u9fff' for c in text):
            continue
        faces = br.cmd('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
        assert faces and all(f['isCustomFont'] for f in faces if f['glyphCount']), (text, faces)
        checked += 1
    result['chineseTextRunsWithoutSystemFallback'] = checked
    return result


def wait_gallery(br, action):
    return br.eval('''(async()=>{ ACTION;
      const end=performance.now()+10000;
      while(!window.galleryState().ready){
        if(window.__galleryError)throw new Error(window.__galleryError);
        if(performance.now()>end)throw new Error('gallery timeout');
        await new Promise(r=>setTimeout(r,30));
      }
      return window.galleryState();
    })()'''.replace('ACTION', action))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--skip-video', action='store_true', help='for a preliminary layout pass before rendering')
    args = ap.parse_args()
    manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
    for demo in manifest:
        assert set(demo['themeVariants']) == EXPECTED_THEMES, demo['id']
        assert set(demo['styleVariants']) == {'diagram', 'terminal'}, demo['id']
        for style in demo['styleVariants'].values():
            assert set(style['themeVariants']) == EXPECTED_THEMES, demo['id']
    chrome = lp.find_exe(None, lp.CHROME_NAMES, 'Chrome')
    result = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'browser': chrome,
              'simulatedData': True, 'scenes': [], 'gallery': {}, 'videos': []}
    element_types, machine_types = set(), set()
    errors = []
    with lp.Chrome(chrome, 960, 640) as br:
        for demo in manifest:
            dest = OUT / demo['id']
            variants = [('diagram', 'default', {'config': 'config.json', 'page': 'live.html', 'poster': 'poster.png'})]
            if demo.get('themeSwitch', True):
                variants += [(style, theme, files) for style, spec in demo['styleVariants'].items()
                             for theme, files in spec['themeVariants'].items()]
            default_record = None
            for style, theme, files in variants:
                config_path = dest / files['config']
                cfg = lp.load_config(config_path)
                assert cfg.get('presentation', {}).get('style', 'diagram') == style
                if theme != 'default':
                    assert cfg['theme']['variant'] == theme, (demo['id'], theme)
                w, h, _, _ = lp.canvas(cfg)
                br.cmd('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h,
                       'deviceScaleFactor': 1, 'mobile': False})
                element_types.update(e['type'] for e in cfg['elements'])
                if any(e.get('flow') for e in cfg['elements']):
                    element_types.add('flow')
                machine_types.update(m['type'] for m in cfg.get('machines', {}).values())
                suffix = config_path.stem.replace('config', '')
                br.open((dest / files['page']).as_uri() + '?manual')
                problems = set()
                for i in range(61):
                    br.seek(12 * i / 61)
                    problems.update(br.eval('window.__check()'))
                    if demo.get('visualStyle') == 'editorial':
                        problems.update(editorial_layout(br))
                problems.update([br.eval('window.__error')] if br.eval('window.__error||""') else [])
                t = demo['checkpoints'][len(demo['checkpoints']) // 2]['time']
                br.seek(t)
                first = br.shot()
                br.seek((t + 5.33) % 12)
                other = br.shot()
                br.seek(t)
                same = br.shot()
                count, delta = pixel_diff(br, first, same)
                movement, _ = pixel_diff(br, first, other)
                record = {'id': demo['id'], 'variant': config_path.stem, 'theme': theme, 'style': style, 'samples': 61,
                          'layoutProblems': sorted(problems), 'replayDifferentPixels': count,
                          'maxReplayChannelDelta': delta, 'animationDifferentPixels': movement}
                if demo.get('visualStyle') == 'editorial':
                    assert (w, h) == (984, 1280)
                    record['embeddedFonts'] = platform_fonts(br, style)
                if style == 'terminal':
                    terminal = br.eval('''(()=>({shell:document.querySelectorAll('[data-terminal-shell]').length,
                      borders:document.querySelectorAll('[data-terminal-border]').length,
                      text:document.querySelector('[data-terminal-shell]')?.textContent||''}))()''')
                    assert terminal['shell'] == 1 and terminal['borders'] > 0, terminal
                    record['terminal'] = terminal
                if cfg.get('effects', {}).get('neon', {}).get('enabled'):
                    sources = br.eval('Array.from(document.querySelectorAll("[data-neon-border]")).map(n=>n.getAttribute("data-neon-border"))')
                    layers = br.eval('Array.from(document.querySelectorAll("[data-neon-layer]")).map(n=>n.getAttribute("data-neon-layer"))')
                    assert sources and len(set(sources)) == len(sources)
                    assert sorted(sources) == sorted(layers)
                    heads = 'Array.from(document.querySelectorAll("[data-neon-head]")).map(n=>[Number(n.getAttribute("cx")),Number(n.getAttribute("cy"))])'
                    br.seek(0)
                    start = br.eval(heads)
                    br.seek(3)
                    assert br.eval(heads) != start
                    br.seek(12)
                    end = br.eval(heads)
                    assert len(start) == len(end) == len(sources)
                    assert all(abs(a-b) < 0.001 for p, q in zip(start, end) for a, b in zip(p, q))
                    record['neon'] = {'blocks': len(sources), 'labels': sources,
                                      'moves': True, 'twelveSecondPositionLoop': True}
                    br.seek(t)
                result['scenes'].append(record)
                (dest / files['poster']).write_bytes(first)
                if theme == 'default':
                    default_record = record
                if problems or count > TOL_PIXELS or movement <= TOL_PIXELS:
                    errors.append(record)
                print(f"{demo['id']}{suffix}: layout={len(problems)} replay={count} motion={movement}", flush=True)
            # Check specific educational claims, using the default scene.
            br.open((dest / 'live.html').as_uri() + '?manual')
            snapshots = []
            for checkpoint in demo['checkpoints']:
                br.seek(checkpoint['time'])
                snapshots.append({'time': checkpoint['time'], 'text': br.eval('document.getElementById("stage").textContent')})
            default_record['checkpointText'] = snapshots
            if demo['id'] == 'product-request':
                assert '缓存命中' in snapshots[0]['text'] and '缓存未命中' in snapshots[1]['text']
            if demo['id'] == 'incident-replay':
                assert '0.36' in snapshots[1]['text'] and '0.24' in snapshots[1]['text']
            if demo['id'] == 'agent-team':
                br.seek(10.8)
                assert '本轮已交付' in br.eval('document.getElementById("stage").innerText')
            if demo['id'] == 'rag-explainer' and demo.get('visualStyle') == 'editorial':
                assert '当前 · 明确问题' in snapshots[0]['text']
                assert '当前 · 筛选证据' in snapshots[2]['text']
                br.seek(10.5)
                assert br.eval('document.querySelector("[data-step=\\"3\\"]").getAttribute("opacity")') == '1'

    handler = functools.partial(QuietHandler, directory=str(OUT))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with lp.Chrome(chrome, 1440, 1120) as br:
            br.open(f'http://127.0.0.1:{server.server_port}/index.html')
            assert br.eval('document.querySelectorAll(".demo-card").length') == 8
            theme_options = br.eval('Array.from(document.getElementById("theme").options).map(n=>n.value)')
            assert set(theme_options) == EXPECTED_THEMES
            checked_theme_scenes = []
            for demo in manifest:
                wait_gallery(br, 'window.selectDemo(' + json.dumps(demo['id']) + ')')
                br.eval('window.jumpDemo(6.5)')
                for theme, files in demo['themeVariants'].items():
                    state = wait_gallery(br, 'document.getElementById("theme").value=' + json.dumps(theme) + ';document.getElementById("theme").dispatchEvent(new Event("change"))')
                    assert state['time'] == 6.5 and not state['playing']
                    assert state['theme'] == theme
                    assert br.eval('document.getElementById("scene").contentWindow.__error||""') == ''
                    assert br.eval('document.documentElement.dataset.theme') == theme
                    assert br.eval('document.getElementById("videoLink").getAttribute("href")') == demo['id'] + '/' + files['video']
                    assert br.eval('document.getElementById("watchVideoLink").getAttribute("href")') == demo['id'] + '/' + files['video']
                    assert br.eval('document.getElementById("htmlLink").getAttribute("href")') == demo['id'] + '/' + files['page']
                    assert br.eval('document.getElementById("configLink").getAttribute("href")') == demo['id'] + '/' + files['config']
                    expected_bg = lp.load_config(OUT / demo['id'] / files['config'])['theme']['colors']['bg']
                    assert br.eval('document.getElementById("scene").contentDocument.documentElement.style.getPropertyValue("--c-bg")') == expected_bg
                    assert br.eval('getComputedStyle(document.getElementById("videoLink")).display') == ('flex' if files['videoReady'] else 'none')
                    checked_theme_scenes.append({'id': demo['id'], 'theme': theme})
                assert br.eval('document.getElementById("exportView").options.length') == 1 + len(demo['exportViews'])
                assert br.eval('document.querySelectorAll("#checkpoints button").length') == len(demo['checkpoints'])
                expected_theme = 'none' if demo.get('themeSwitch', True) is False else 'flex'
                assert br.eval('getComputedStyle(document.getElementById("themeLabel")).display') == expected_theme
                has_actor = br.eval('document.getElementById("scene").contentDocument.querySelectorAll("[data-avatar=spider]").length>0')
                assert br.eval('getComputedStyle(document.getElementById("avatarLabel")).display') == ('flex' if has_actor else 'none')
                assert br.eval('document.querySelector(".workspace").dataset.shape') == ('portrait' if demo['width'] < demo['height'] else 'landscape')
                assert br.eval('getComputedStyle(document.getElementById("beforeLink")).display') == ('flex' if demo.get('beforePage') else 'none')
            wait_gallery(br, 'window.selectDemo("component-lab")')
            assert br.eval('document.getElementById("view").options.length') == 7
            br.eval('window.jumpDemo(7);document.getElementById("view").value="2";document.getElementById("view").dispatchEvent(new Event("change"))')
            zoom = next(d for d in manifest if d['id'] == 'component-lab')['focusViews'][1].get('zoom', 2.8)
            assert f'scale({zoom})' in br.eval('document.getElementById("scene").style.transform')
            assert br.eval('window.galleryState().time') == 7
            (OUT / 'component-closeup.png').write_bytes(br.shot())
            wait_gallery(br, 'window.selectDemo("avatar-themes")')
            br.eval('window.jumpDemo(4.5); document.getElementById("avatar").value="drone";document.getElementById("avatar").dispatchEvent(new Event("change"))')
            assert br.eval('Array.from(document.getElementById("scene").contentDocument.querySelectorAll("[data-avatar=spider]")).every(n=>n.style.display==="none")')
            state = wait_gallery(br, 'document.getElementById("theme").value="light-pastel";document.getElementById("theme").dispatchEvent(new Event("change"))')
            assert state['time'] == 4.5 and not state['playing']
            expected_light_bg = lp.load_config(OUT / 'avatar-themes' / 'config-light.json')['theme']['colors']['bg']
            assert br.eval('document.getElementById("scene").contentDocument.documentElement.style.getPropertyValue("--c-bg")') == expected_light_bg
            assert br.eval('document.documentElement.dataset.theme') == 'light-pastel'
            assert br.eval('document.getElementById("videoLink").getAttribute("href")') == 'avatar-themes/demo-light.mp4'
            (OUT / 'gallery-light-preview.png').write_bytes(br.shot())
            assert br.eval('Array.from(document.getElementById("scene").contentDocument.querySelectorAll("[data-avatar=spider]")).every(n=>n.style.display==="none")')
            avatar_demo = next(d for d in manifest if d['id'] == 'avatar-themes')
            for theme in avatar_demo['themeVariants']:
                state = wait_gallery(br, 'document.getElementById("theme").value=' + json.dumps(theme) + ';document.getElementById("theme").dispatchEvent(new Event("change"))')
                assert state['time'] == 4.5 and not state['playing'] and state['avatar'] == 'drone'
                assert br.eval('Array.from(document.getElementById("scene").contentDocument.querySelectorAll("[data-avatar=spider]")).every(n=>n.style.display==="none")')
            br.eval('document.getElementById("replay").click()')
            assert br.eval('window.galleryState().playing')
            br.eval('document.getElementById("play").click()')
            assert not br.eval('window.galleryState().playing')
            wait_gallery(br, 'document.getElementById("theme").value="terminal-dark";window.selectDemo("rag-explainer")')
            br.eval('window.jumpDemo(7.5)')
            br.eval('document.body.dispatchEvent(new KeyboardEvent("keydown",{code:"ArrowRight",bubbles:true}))')
            assert br.eval('window.galleryState().time') == 8.5
            br.eval('window.jumpDemo(7.5)')
            if manifest[0].get('beforePage'):
                assert br.eval('document.getElementById("beforeLink").getAttribute("href")') == 'rag-explainer/live-before.html'
                assert br.eval('document.getElementById("scene").contentWindow.__check()') == []
            (OUT / 'gallery-preview.png').write_bytes(br.shot())
            result['gallery'] = {'demoCount': 8, 'allScenesLoad': True, 'seekAndPause': True,
                                 'themePreservesTimeAndAvatar': True, 'replayAndPlayButtons': True,
                                 'unusedControlsHidden': True, 'sixComponentCloseups': True,
                                 'keyboardSeek': True, 'mixedCanvasRatios': True,
                                 'beforeComparisonLink': bool(manifest[0].get('beforePage'))}
            result['gallery']['themeCount'] = len(theme_options)
            result['gallery']['checkedThemeScenes'] = checked_theme_scenes
            result['gallery']['exportBlockCount'] = sum(len(d['exportViews']) for d in manifest)
    finally:
        server.shutdown()
        server.server_close()

    if not args.skip_video:
        ffprobe = lp.find_exe(None, ['ffprobe'], 'ffprobe')
        ffmpeg = lp.find_exe(None, ['ffmpeg'], 'ffmpeg')
        for demo, style, theme, files in [(d, style, theme, files) for d in manifest
                                        for style, spec in d['styleVariants'].items()
                                        for theme, files in spec['themeVariants'].items()]:
            file = OUT / demo['id'] / files['video']
            assert files['videoReady'] and file.is_file(), (demo['id'], theme)
            data = json.loads(subprocess.check_output([ffprobe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(file)]))
            video = next(s for s in data['streams'] if s['codec_type'] == 'video')
            cfg = lp.load_config(OUT / demo['id'] / files['config'])
            w, h, duration, fps = lp.canvas(cfg)
            assert (video['codec_name'], video['width'], video['height'], video['r_frame_rate'], int(video['nb_frames'])) == ('h264', w, h, f'{fps}/1', round(fps*duration))
            assert abs(float(data['format']['duration']) - 12) < .1
            assert any(s['codec_type'] == 'audio' for s in data['streams'])
            subprocess.run([ffmpeg, '-v', 'error', '-i', str(file), '-f', 'null', '-'], check=True, stdout=subprocess.DEVNULL)
            result['videos'].append({'id': demo['id'], 'theme': theme, 'style': style, 'codec': 'h264', 'width': w, 'height': h,
                                     'fps': fps, 'frames': round(fps*duration), 'duration': float(data['format']['duration']),
                                     'bytes': file.stat().st_size, 'fullDecode': 'passed'})
            print('video checked', demo['id'], style, theme, flush=True)
    result['coverage'] = {'elementTypes': sorted(element_types), 'machineTypes': sorted(machine_types)}
    result['passed'] = not errors
    (OUT / ('verification-layout.json' if args.skip_video else 'verification.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if errors:
        raise SystemExit('Scene layout, animation or replay check failed; see verification JSON.')
    print(f"PASS: {len(result['scenes'])} scene variants, gallery controls, {len(result['videos'])} MP4s")


if __name__ == '__main__':
    main()
