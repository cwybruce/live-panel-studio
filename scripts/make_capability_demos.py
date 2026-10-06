"""Build the original capability gallery; optionally render every 12-second MP4."""
import argparse
import copy
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import livepanel as lp
from editorial_systems import scenes as system_scenes
from editorial_stories import stories
from editorial_components import scenes as component_scenes
from rag_editorial import scene as editorial_rag
from editorial_fonts import font_style
from demo_export_views import export_views
from media_assets import published_paths

OUT = lp.ROOT / 'examples/capability-demos'
EDITORIAL_PALETTES = {'terminal-dark': {'bg': '#191713',
                   'panel': '#25221b',
                   'surface': '#211e18',
                   'line': '#958871',
                   'fg': '#fff5e6',
                   'dim': '#d0c1aa',
                   'amber': '#f3cf88',
                   'cyan': '#8de1ee',
                   'pink': '#ff9bcc',
                   'mint': '#a7e6bd',
                   'red': '#ff9a88',
                   'blue': '#aacff7',
                   'ye': '#f3cf88',
                   'cy': '#8de1ee',
                   'pu': '#ff9bcc',
                   'gr': '#a7e6bd',
                   'rd': '#ff9a88',
                   'wh': '#fff5e6',
                   'bl': '#aacff7',
                   'pi': '#ff9bcc',
                   'pk': '#ff9a88',
                   'gn': '#a7e6bd',
                   'ort': '#f3cf88',
                   'blt': '#aacff7',
                   'put': '#ff9bcc',
                   'mc': '#ff9bcc',
                   'tl': '#8de1ee',
                   'gy': '#958871',
                   'or': '#f3cf88',
                   'yl': '#f3cf88',
                   'bar': '#25221b',
                   'line2': '#958871',
                   'dots': '#958871',
                   'hl': '#362c29',
                   'gnf': '#2e3026',
                   'blf': '#2e2e2a',
                   'ylf': '#332e23',
                   'orf': '#332e23',
                   'rdf': '#342a23',
                   'puf': '#342a27',
                   'mcf': '#342a27',
                   'tlf': '#2c2f2a',
                   'gyf': '#312d25',
                   'lit': '#332e23'},
 'light-pastel': {'bg': '#faf7f0',
                  'panel': '#fffdf8',
                  'surface': '#f2ecdf',
                  'line': '#978a76',
                  'fg': '#24211c',
                  'dim': '#62584a',
                  'amber': '#885412',
                  'cyan': '#216674',
                  'pink': '#943768',
                  'mint': '#326743',
                  'red': '#a1382b',
                  'blue': '#2f568d',
                  'ye': '#885412',
                  'cy': '#216674',
                  'pu': '#943768',
                  'gr': '#326743',
                  'rd': '#a1382b',
                  'wh': '#24211c',
                  'bl': '#2f568d',
                  'pi': '#943768',
                  'pk': '#a1382b',
                  'gn': '#326743',
                  'ort': '#885412',
                  'blt': '#2f568d',
                  'put': '#943768',
                  'mc': '#943768',
                  'tl': '#216674',
                  'gy': '#978a76',
                  'or': '#885412',
                  'yl': '#885412',
                  'bar': '#fffdf8',
                  'line2': '#978a76',
                  'dots': '#978a76',
                  'hl': '#f6edec',
                  'gnf': '#f1f3eb',
                  'blf': '#f0f1f1',
                  'ylf': '#f7f1e8',
                  'orf': '#f7f1e8',
                  'rdf': '#f8efea',
                  'puf': '#f8efee',
                  'mcf': '#f8efee',
                  'tlf': '#eff2ef',
                  'gyf': '#f4f1ec',
                  'lit': '#f7f1e8'},
 'terminal-classic': {'bg': '#191f27',
                      'panel': '#222a35',
                      'surface': '#1e2630',
                      'line': '#8395ad',
                      'fg': '#f6f8ff',
                      'dim': '#c0cbd9',
                      'amber': '#f2ca80',
                      'cyan': '#80dfef',
                      'pink': '#c7acff',
                      'mint': '#89e7b4',
                      'red': '#ff786f',
                      'blue': '#9bbeff',
                      'ye': '#f2ca80',
                      'cy': '#80dfef',
                      'pu': '#c7acff',
                      'gr': '#89e7b4',
                      'rd': '#ff786f',
                      'wh': '#f6f8ff',
                      'bl': '#9bbeff',
                      'pi': '#c7acff',
                      'pk': '#ff786f',
                      'gn': '#89e7b4',
                      'ort': '#f2ca80',
                      'blt': '#9bbeff',
                      'put': '#c7acff',
                      'mc': '#c7acff',
                      'tl': '#80dfef',
                      'gy': '#8395ad',
                      'or': '#f2ca80',
                      'yl': '#f2ca80',
                      'bar': '#222a35',
                      'line2': '#8395ad',
                      'dots': '#8395ad',
                      'hl': '#2f3445',
                      'gnf': '#29373e',
                      'blf': '#2a3443',
                      'ylf': '#31353a',
                      'orf': '#31353a',
                      'rdf': '#312f39',
                      'puf': '#2e3343',
                      'mcf': '#2e3343',
                      'tlf': '#293742',
                      'gyf': '#2d3540',
                      'lit': '#31353a'},
 'pastel-classic': {'bg': '#ffffff',
                    'panel': '#ffffff',
                    'surface': '#f1f4f8',
                    'line': '#8996a8',
                    'fg': '#18212f',
                    'dim': '#526174',
                    'amber': '#9f4800',
                    'cyan': '#146f70',
                    'pink': '#723d9d',
                    'mint': '#326b25',
                    'red': '#b72b36',
                    'blue': '#275bac',
                    'ye': '#9f4800',
                    'cy': '#146f70',
                    'pu': '#723d9d',
                    'gr': '#326b25',
                    'rd': '#b72b36',
                    'wh': '#18212f',
                    'bl': '#275bac',
                    'pi': '#723d9d',
                    'pk': '#b72b36',
                    'gn': '#326b25',
                    'ort': '#9f4800',
                    'blt': '#275bac',
                    'put': '#723d9d',
                    'mc': '#723d9d',
                    'tl': '#146f70',
                    'gy': '#8996a8',
                    'or': '#9f4800',
                    'yl': '#9f4800',
                    'bar': '#ffffff',
                    'line2': '#8996a8',
                    'dots': '#8996a8',
                    'hl': '#f4eff7',
                    'gnf': '#f1f5f0',
                    'blf': '#f0f4f9',
                    'ylf': '#f8f2ed',
                    'orf': '#f8f2ed',
                    'rdf': '#faf0f1',
                    'puf': '#f5f1f8',
                    'mcf': '#f5f1f8',
                    'tlf': '#eff5f5',
                    'gyf': '#f3f4f5',
                    'lit': '#f8f2ed'}}

THEME_VARIANTS = {
    'terminal-dark': {'label': '暖黑 / Warm Ink', 'preset': 'terminal-dark',
                      'config': 'config-dark.json', 'page': 'live-dark.html',
                      'video': 'demo.mp4', 'poster': 'poster.png'},
    'light-pastel': {'label': '暖纸 / Warm Paper', 'preset': 'light-pastel',
                     'config': 'config-light.json', 'page': 'live-light.html',
                     'video': 'demo-light.mp4', 'poster': 'poster-light.png'},
    'terminal-classic': {'label': '经典终端 / Classic Terminal', 'preset': 'terminal-dark',
                         'config': 'config-terminal.json', 'page': 'live-terminal.html',
                         'video': 'demo-terminal.mp4', 'poster': 'poster-terminal.png'},
    'pastel-classic': {'label': '经典粉彩 / Classic Pastel', 'preset': 'light-pastel',
                       'config': 'config-pastel.json', 'page': 'live-pastel.html',
                       'video': 'demo-pastel.mp4', 'poster': 'poster-pastel.png'},
}

STYLE_VARIANTS = {
    'diagram': {'label': '原版图解 / Diagram', 'themeVariants': THEME_VARIANTS},
    'terminal': {'label': 'macOS 终端 / macOS Terminal', 'themeVariants': {
        theme: {**files,
                'config': 'config-console-' + suffix + '.json',
                'page': 'live-console-' + suffix + '.html',
                'video': 'demo-console-' + suffix + '.mp4',
                'poster': 'poster-console-' + suffix + '.png'}
        for theme, suffix in (('terminal-dark', 'dark'), ('light-pastel', 'light'),
                              ('terminal-classic', 'terminal'), ('pastel-classic', 'pastel'))
        for files in (THEME_VARIANTS[theme],)
    }},
}


def presentation_config(config, style, demo, theme):
    """Add optional terminal furniture while preserving authored crop geometry."""
    if style not in STYLE_VARIANTS:
        raise ValueError('Unknown presentation style: ' + str(style))
    version = copy.deepcopy(config)
    if style == 'diagram':
        return version
    files = STYLE_VARIANTS[style]['themeVariants'][theme]
    events = [{'t': 0, 'actor': 'studio', 'text': '演示启动 · 预设模拟'}]
    events += [{'t': float(checkpoint['time']), 'actor': demo['id'].split('-')[0],
                'text': '演示关键点：' + checkpoint['label']}
               for checkpoint in demo['checkpoints']
               if 0 <= float(checkpoint['time']) < lp.canvas(version)[2]]
    version['presentation'] = {
        'style': 'terminal', 'sceneId': demo['id'],
        'title': '~/motion-diagram-studio/' + demo['id'] + ' — zsh',
        'command': 'python scripts/render.py --config examples/capability-demos/' +
                   demo['id'] + '/' + files['config'],
        'events': sorted(events, key=lambda event: event['t']),
    }
    return version


def theme_config(config, variant):
    """Apply a whitelisted palette without changing the source scene or timing."""
    metadata = THEME_VARIANTS[variant]
    version = copy.deepcopy(config)
    theme = version.setdefault('theme', {})
    theme.update(preset=metadata['preset'], variant=variant)
    theme.setdefault('colors', {}).update(EDITORIAL_PALETTES[variant])
    return version


def render_themes(selection):
    """The legacy `both` option continues to render only the two warm themes."""
    return {'dark': ['terminal-dark'], 'light': ['light-pastel'],
            'both': ['terminal-dark', 'light-pastel'],
            'terminal': ['terminal-classic'], 'pastel': ['pastel-classic'],
            'all': list(THEME_VARIANTS)}[selection]


def collection():
    source = [editorial_rag()] + system_scenes() + stories() + component_scenes()
    order = ['rag-explainer', 'agent-team', 'product-request', 'knowledge-card',
             'business-workflow', 'incident-replay', 'component-lab', 'avatar-themes']
    return sorted(source, key=lambda d: order.index(d['id']))


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    demos = collection()
    released_videos = published_paths()
    manifest = []
    for demo in demos:
        dest = OUT / demo['id']
        dest.mkdir(exist_ok=True)
        def video_ready(filename):
            path = dest / filename
            return path.is_file() or path.relative_to(lp.ROOT).as_posix() in released_videos

        config = demo['config']
        demo['themeSwitch'] = True
        demo['exportViews'] = export_views(demo['id'])
        config['meta']['visualStyle'] = 'editorial'
        config['effects'] = {'neon': {'enabled': True, 'intensity': 0.8,
                                     'period': 6, 'heroPeriod': 12, 'tail': 144}}
        config['theme']['font'] = '"LP Sans",sans-serif'
        config = theme_config(config, 'terminal-dark')
        variants = [('config.json', 'live.html', config)]
        for style, style_files in STYLE_VARIANTS.items():
            for variant, files in style_files['themeVariants'].items():
                version = presentation_config(theme_config(config, variant), style, demo, variant)
                variants.append((files['config'], files['page'], version))
        for config_name, page_name, version in variants:
            path = dest / config_name
            path.write_text(json.dumps(version, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            lp.build_page(path, dest / page_name)
        metadata = {k: v for k, v in demo.items() if k != 'config'}
        before_page = metadata.get('beforePage')
        if before_page and not (dest / before_page).is_file():
            metadata.pop('beforePage')
        metadata.update(width=lp.canvas(config)[0], height=lp.canvas(config)[1],
                        duration=lp.canvas(config)[2], sceneTitle=config['meta']['title'],
                        videoReady=video_ready('demo.mp4'),
                        lightVideoReady=video_ready('demo-light.mp4'),
                        videos={theme: files['video'] for theme, files in THEME_VARIANTS.items()},
                        themeVariants={theme: {**{k: v for k, v in files.items() if k != 'preset'},
                                               'videoReady': video_ready(files['video'])}
                                       for theme, files in THEME_VARIANTS.items()},
                        styleVariants={style: {
                            'label': style_files['label'],
                            'themeVariants': {theme: {
                                **{k: v for k, v in files.items() if k != 'preset'},
                                'videoReady': video_ready(files['video'])}
                                for theme, files in style_files['themeVariants'].items()}}
                            for style, style_files in STYLE_VARIANTS.items()})
        manifest.append(metadata)
        readme = [f"# {demo['title']}", '', demo['summary'], '',
                  '原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。', '',
                  '## 能力', '', *['- ' + s for s in demo['capabilities']], '',
                  '## 观察与修改', '', *['- ' + s for s in demo['learn']], '',
                  '关键时刻：' + '；'.join(f"{c['time']}s {c['label']}" for c in demo['checkpoints']), '',
                  '文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。', '',
                  '预制 MP4 由 Releases 分发。需要本地观看成片时，从仓库根目录运行 `python scripts/media_assets.py download --set demos`；交互 HTML 和生成新视频不依赖这些预制成片。', '',
                  '每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。', '',
                  '展示样式与配色分别选择：原版图解保留原有排版；macOS 终端加入窗口外壳、等宽文字、字符边框、模拟日志与命令光标。终端配置、网页、视频与海报使用 `config-console-*` / `live-console-*` / `demo-console-*` / `poster-console-*` 文件名。', '',
                  '每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。', '',
                  '从仓库根目录重新导出：', '', '```powershell',
                  f"python scripts/render.py --config examples/capability-demos/{demo['id']}/config.json --out examples/capability-demos/{demo['id']}/demo.mp4", '```', '',
                  '修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。',
                  '“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。', '',
                  '单独导出此 Demo 的浅色版：', '', '```powershell',
                  f"python scripts/export_demo.py --scene {demo['id']} --theme light-pastel --view full --out examples/capability-demos/{demo['id']}/custom-light.mp4", '```', '']
        readme += ['导出此 Demo 的经典终端配色与 macOS 终端样式：', '', '```powershell',
                   f"python scripts/export_demo.py --scene {demo['id']} --theme terminal-classic --style terminal --view full --out examples/capability-demos/{demo['id']}/custom-console.mp4", '```', '']
        (dest / 'README.md').write_text('\n'.join(readme), encoding='utf-8')
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    template = (lp.ROOT / 'assets/demo-gallery.html').read_text(encoding='utf-8')
    blob = json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')
    template = template.replace('</head>', font_style() + '</head>')
    (OUT / 'index.html').write_text(template.replace('/*DEMO_MANIFEST*/', blob), encoding='utf-8')
    rows = '\n'.join(f"| {i+1} | [{d['title']}]({d['id']}/live.html) | {', '.join(d['capabilities'])} |" for i, d in enumerate(manifest))
    (OUT / 'README.md').write_text('''# Motion Diagram Studio 能力体验馆

8 个原创中文 Demo，展示当前引擎能做的流程动画、状态切换、数据组件、角色、主题与导出。
预制成片由 Releases 分发，本地运行 `python scripts/media_assets.py download --set demos` 恢复到原路径。
所有演示使用模拟数据与预设时间线，没有连接真实 Agent、数据库、工单或日志服务。
全部 8 个场景均有暖黑、暖纸、经典终端、经典粉彩四套竖屏配色：984×1280、细线、局部光感、各自的图形叙事。
经典终端与经典粉彩源于上游 skill 原有两套配色；布局、文案和动画沿用当前示例。
每个功能块的边缘有错开相位的霓虹扫光、渐隐拖尾与局部泛光，当前块更亮；浅色主题降低泛光。
标题使用 Noto Serif SC，正文 Noto Sans SC，英文与数字 IBM Plex Mono。
网页嵌入更名的 OFL 字体子集（LP Serif / Sans / Mono），无需安装字体或联网。
本地存在旧版网页时显示“旧版对照”；公开版本不要求这些历史对照文件。

运行 `启动预览.ps1`，或从仓库根目录执行 `python scripts/preview_server.py --port 8779`，
然后打开 http://127.0.0.1:8779/index.html 。预览服务同时提供本地 MP4 导出。

| 编号 | Demo | 能力 |
| --- | --- | --- |
''' + rows + '''

播放器支持暂停、重播、拖动时间轴、0.5/1/2 倍速与关键时刻跳转。
含角色的场景可切换蜘蛛/机器人；全部示例可切换四种配色。
展示样式另行切换“原版图解 / macOS 终端”，与四套配色互不绑定；终端的标题栏、日志和光标也进入整段 MP4。功能块保持原裁剪范围。
组件实验室的“组件视图”下拉框可放大查看六个组件。

每个目录都含 JSON 配置、独立 HTML、12 秒 MP4、预览图和说明。
每个 Demo 可独立导出整段 MP4，也可选择内部功能块单独导出（共 39 块）。
“导出当前方案”按当前主题、角色和范围生成 12 秒、30fps H.264 MP4。
功能块视频裁剪真实画布，保留文字、内部动画和边缘泛光，不将总览的缩放视图误当作裁剪。
导出文件另存于 `exports/`，原始配置和成片保留。无需连接外部服务。

从仓库根目录生成或重新导出：

```powershell
python scripts/make_capability_demos.py
python scripts/make_capability_demos.py --render --jobs 2
python scripts/make_capability_demos.py --render --themes light --jobs 2
python scripts/make_capability_demos.py --render --themes all --jobs 2
python scripts/make_capability_demos.py --render --styles terminal --themes all --jobs 2
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view rag-rerank --out examples/capability-demos/rag-explainer/rerank-light.mp4
python scripts/verify_capability_demos.py
```

修改 `scripts/rag_editorial.py`、`editorial_systems.py`、`editorial_stories.py`、`editorial_components.py` 的数据与时间线，
或 `assets/*editorial*.js` 的图形布局后可以重新生成。
如果直接修改生成的 JSON，不要运行生成器覆盖它；使用 `scripts/render.py` 单独导出。
页面动画都由 `window.seek(t)` 驱动；`verification.json` 记录实际浏览器与视频检查结果。
`effects.neon` 可调整光效强度、扫光周期、主场景周期和拖尾长度，也可关闭；详见配置文档。

保留上游 MIT LICENSE 与 README 致谢。本组示例的可见文案、场景和数字采用原创配置与模拟数据，未打包参考视频。
独立 HTML 嵌入完整兼容组件库，其中保留旧示例的默认字符串；原有复刻示例的授权说明仍见仓库 README。
引擎和 SVG 动法基于原仓库及本地扩展。字体保留各自 OFL 许可，详见 `assets/fonts/README.md`。
''', encoding='utf-8')
    return demos


def render(job):
    demo, theme, style = job
    dest = OUT / demo['id']
    files = STYLE_VARIANTS[style]['themeVariants'][theme]
    subprocess.run([sys.executable, str(lp.ROOT / 'scripts/render.py'), '--config',
                    str(dest / files['config']), '--out',
                    str(dest / files['video'])], check=True)
    return demo['id'] + ':' + theme + ':' + style


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--jobs', type=int, default=1, choices=[1, 2])
    ap.add_argument('--themes', choices=['dark', 'light', 'both', 'terminal', 'pastel', 'all'], default='both',
                    help='themes to render; both = the two warm themes; generation always includes all four')
    ap.add_argument('--styles', choices=['diagram', 'terminal', 'both'], default='diagram',
                    help='presentation to render; default preserves the original diagram videos')
    args = ap.parse_args()
    demos = generate()
    if args.render:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            themes = render_themes(args.themes)
            styles = list(STYLE_VARIANTS) if args.styles == 'both' else [args.styles]
            for name in pool.map(render, [(demo, theme, style) for demo in demos for style in styles for theme in themes]):
                print('rendered', name, flush=True)
        generate()
    print(f'Built {len(demos)} demos: {OUT / "index.html"}')


if __name__ == '__main__':
    main()
