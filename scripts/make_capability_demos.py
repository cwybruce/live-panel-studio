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
EDITORIAL_PALETTES = {
    'terminal-dark': {'bg': '#12110f', 'panel': '#191713', 'line': '#3c352c',
                      'fg': '#eee9df', 'dim': '#9f9587', 'amber': '#dfb96d',
                      'cyan': '#64bed0', 'pink': '#e776af', 'mint': '#88c4a2',
                      'red': '#d77768', 'ye': '#dfb96d', 'cy': '#64bed0',
                      'pu': '#e776af', 'gr': '#88c4a2', 'rd': '#d77768',
                      'surface': '#171511', 'wh': '#eee9df', 'bar': '#191713',
                      'hl': '#29241c', 'dots': '#52483c', 'line2': '#3c352c',
                      'bl': '#64bed0', 'pi': '#e776af'},
    'light-pastel': {'bg': '#f1eee5', 'panel': '#e9e4d9', 'line': '#b2a797',
                     'fg': '#302d27', 'dim': '#746b5e', 'amber': '#9b6f28',
                     'cyan': '#317e89', 'pink': '#aa587e', 'mint': '#507e5f',
                     'red': '#ad554c', 'ye': '#9b6f28', 'cy': '#317e89',
                     'pu': '#aa587e', 'gr': '#507e5f', 'rd': '#ad554c',
                     'surface': '#faf6ed', 'wh': '#302d27', 'bar': '#e9e4d9',
                     'hl': '#e3d9c5', 'dots': '#b2a797', 'line2': '#b2a797',
                     'bl': '#317e89', 'pi': '#aa587e'},
    # The upstream terminal and pastel presets, adapted to the semantic roles
    # used by the authored SVG scenes. Keep the warm presets and files stable.
    'terminal-classic': {'bg': '#14171c', 'panel': '#1b2028', 'surface': '#191d24',
                         'line': '#4a5367', 'line2': '#3a4154', 'fg': '#e4e8f0',
                         'dim': '#8d97ac', 'amber': '#e3c07a', 'cyan': '#86e1e6',
                         'blue': '#8fb4f6', 'pink': '#b9a2f2', 'mint': '#7fdba8',
                         'red': '#f46d70', 'bar': '#262a32', 'hl': '#302d45',
                         'dots': '#566078', 'wh': '#ffffff', 'ye': '#e3c07a',
                         'cy': '#86e1e6', 'bl': '#8fb4f6', 'pu': '#b9a2f2',
                         'pi': '#b9a2f2', 'gr': '#7fdba8', 'rd': '#f46d70'},
    'pastel-classic': {'bg': '#fcfcfb', 'panel': '#ffffff', 'surface': '#f5f5f4',
                       'line': '#c9ccd1', 'line2': '#c9ccd1', 'fg': '#23272e',
                       'dim': '#69727e', 'amber': '#d9731a', 'cyan': '#25877e',
                       'blue': '#3a6fc8', 'pink': '#7d4fb0', 'mint': '#4f8e34',
                       'red': '#d24a4a', 'bar': '#f1f1ef', 'hl': '#fff1b8',
                       'dots': '#b9bdc4', 'wh': '#ffffff', 'ye': '#d9731a',
                       'cy': '#25877e', 'bl': '#5f93e0', 'pu': '#b389d9',
                       'pi': '#7d4fb0', 'gr': '#6fb34f', 'rd': '#e47b7b',
                       'gn': '#6fb34f', 'gnf': '#e7f4de', 'blf': '#e4eefc',
                       'blt': '#3a6fc8', 'yl': '#e3b93d', 'ylf': '#fff5d6',
                       'or': '#e79a4c', 'orf': '#fdeedc', 'ort': '#d9731a',
                       'rdf': '#fde7e7', 'rdt': '#d24a4a', 'puf': '#f2eafa',
                       'put': '#7d4fb0', 'mc': '#9a92d9', 'mcf': '#eeebfa',
                       'tl': '#5fbdb2', 'tlf': '#e0f4f1', 'gy': '#b9bdc4',
                       'gyf': '#f5f5f4', 'pk': '#f0575f', 'lit': '#fff1b8'},
}

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
        for variant, files in THEME_VARIANTS.items():
            variants.append((files['config'], files['page'], theme_config(config, variant)))
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
                                       for theme, files in THEME_VARIANTS.items()})
        manifest.append(metadata)
        readme = [f"# {demo['title']}", '', demo['summary'], '',
                  '原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。', '',
                  '## 能力', '', *['- ' + s for s in demo['capabilities']], '',
                  '## 观察与修改', '', *['- ' + s for s in demo['learn']], '',
                  '关键时刻：' + '；'.join(f"{c['time']}s {c['label']}" for c in demo['checkpoints']), '',
                  '文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。', '',
                  '预制 MP4 由 Releases 分发。需要本地观看成片时，从仓库根目录运行 `python scripts/media_assets.py download --set demos`；交互 HTML 和生成新视频不依赖这些预制成片。', '',
                  '每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。', '',
                  '每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。', '',
                  '从仓库根目录重新导出：', '', '```powershell',
                  f"python scripts/render.py --config examples/capability-demos/{demo['id']}/config.json --out examples/capability-demos/{demo['id']}/demo.mp4", '```', '',
                  '修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。',
                  '“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。', '',
                  '单独导出此 Demo 的浅色版：', '', '```powershell',
                  f"python scripts/export_demo.py --scene {demo['id']} --theme light-pastel --view full --out examples/capability-demos/{demo['id']}/custom-light.mp4", '```', '']
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
    demo, theme = job
    dest = OUT / demo['id']
    files = THEME_VARIANTS[theme]
    subprocess.run([sys.executable, str(lp.ROOT / 'scripts/render.py'), '--config',
                    str(dest / files['config']), '--out',
                    str(dest / files['video'])], check=True)
    return demo['id'] + ':' + theme


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--jobs', type=int, default=1, choices=[1, 2])
    ap.add_argument('--themes', choices=['dark', 'light', 'both', 'terminal', 'pastel', 'all'], default='both',
                    help='themes to render; both = the two warm themes; generation always includes all four')
    args = ap.parse_args()
    demos = generate()
    if args.render:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            themes = render_themes(args.themes)
            for name in pool.map(render, [(demo, theme) for demo in demos for theme in themes]):
                print('rendered', name, flush=True)
        generate()
    print(f'Built {len(demos)} demos: {OUT / "index.html"}')


if __name__ == '__main__':
    main()
