# Motion Diagram Studio · 动态图解工作室

**中文** · [English](README.en.md)

把架构与流程，做成会动的图解。支持交互网页与 MP4 视频导出。

基于 [live-panel-skill](https://github.com/ythx-101/live-panel-skill)，将 JSON 配置变成动态示意图、交互网页与 MP4 视频，提供八个原创中文 Demo、四套配色、动态角色与功能块独立导出。

由 @sycbruce 独立扩展和维护，非上游官方项目。本项目原名 Live Panel Studio。

维护与交流：**[@sycbruce · X](https://x.com/sycbruce)** · [提交问题](https://github.com/cwybruce/motion-diagram-studio/issues)

**[在线体验与视频库](https://cwybruce.github.io/motion-diagram-studio/)** · [交互体验馆](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html) · [功能块导出案例](https://cwybruce.github.io/motion-diagram-studio/#exports)

网页可直接播放 8 个 Demo 的四套配色成片、初期复刻与蜘蛛更新视频，并浏览 39 个功能块成片及 3 个浅色机器人导出案例。支持播放、拖动进度和 MP4 下载；生成新方案请运行下方本地服务。

## 动态 Demo

下方动画直接取自已经导出的 MP4，节选前 **6 秒**并自动循环。**点击动画观看完整成片**；完整视频保留原画质与帧率。更多场景、角色和功能块见 [在线视频库](https://cwybruce.github.io/motion-diagram-studio/)。

| RAG 证据讲解 · 暖黑 | RAG 证据讲解 · 暖纸 |
| --- | --- |
| [![RAG 证据讲解：暖黑动态预览](assets/readme/rag-explainer-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo.mp4) | [![RAG 证据讲解：暖纸动态预览](assets/readme/rag-explainer-light.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-light.mp4) |
| [▶ 完整 MP4 · 12 秒](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo.mp4) | [▶ 完整 MP4 · 12 秒](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-light.mp4) |

| RAG 证据讲解 · 经典终端 | RAG 证据讲解 · 经典粉彩 |
| --- | --- |
| [![RAG 证据讲解：经典终端动态预览](assets/readme/rag-explainer-terminal.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-terminal.mp4) | [![RAG 证据讲解：经典粉彩动态预览](assets/readme/rag-explainer-pastel.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-pastel.mp4) |
| [▶ 完整 MP4 · 12 秒](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-terminal.mp4) | [▶ 完整 MP4 · 12 秒](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-pastel.mp4) |

## 能做什么

- **8 个原创中文 Demo**：RAG 证据讲解、多 Agent 交接、请求与缓存、知识卡、工单流转、故障恢复、矢量组件、角色导航。
- **四套配色方案**：暖黑、暖纸、经典终端、经典粉彩，均使用 984 × 1280 竖屏排版与内嵌中文字体；每个功能块有流动的霓虹边缘、拖尾与局部泛光。
- **交互播放**：暂停、重播、时间轴拖动、关键时刻跳转、0.5 / 1 / 2 倍速；含角色的场景支持蜘蛛与机器人切换。
- **独立 MP4 导出**：每个 Demo 可整段导出，也可单独导出内部功能块，共 **39 个命名区域**。导出按当前主题、角色与范围生成新文件。
- **确定性回放**：动画由 `window.seek(t)` 驱动，浏览器预览和逐帧渲染使用同一时间线。
- **可修改的 JSON 和 SVG**：配置文本、数据、配色与时间线，扩展组件或重新设计场景。

Demo 中的事件、指标、日志和数据均为**预设模拟**，没有连接真实 Agent、数据库或业务服务。默认成片为 **12 秒、30 fps、H.264 MP4，附带静音 AAC 音轨**。

## 四套配色

暖黑与暖纸延续本项目现有风格；经典终端与经典粉彩分别沿用上游 Codex Agent 图和 AI Agent 架构图的配色方向，并应用到八个原创场景。

| 配色 | 主题 ID | 风格与在线体验 |
| --- | --- | --- |
| 暖黑 | `terminal-dark` | 暖黑底、金橙色强调；[打开 RAG](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html?theme=terminal-dark#rag-explainer) |
| 暖纸 | `light-pastel` | 米白纸底、柔和暖色；[打开 RAG](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html?theme=light-pastel#rag-explainer) |
| 经典终端 | `terminal-classic` | 冷灰黑底、青 / 蓝 / 绿 / 紫强调；[打开 RAG](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html?theme=terminal-classic#rag-explainer) |
| 经典粉彩 | `pastel-classic` | 白底、蓝 / 黄 / 橙 / 紫 / 红色分区；[打开 RAG](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html?theme=pastel-classic#rag-explainer) |

主题与角色可以分别选择，整段和功能块导出都使用当前选择的配色。新增配色不改变现有主题 ID 或旧成片文件名。

## 快速开始

当前实测环境为 **Windows、Python 3.11、系统 Chrome 与 FFmpeg**，渲染器也支持检测已安装的 Edge。推荐 Python 3.11 或更新版本。原上游保留 Linux / macOS 渲染路径；本项目新增的完整导出流程尚未在这些平台实测。

先安装：

1. [Python](https://www.python.org/downloads/) 3.11+。
2. [Chrome](https://www.google.com/chrome/) 或 [Edge](https://www.microsoft.com/edge)。使用系统浏览器，无需下载 Playwright Chromium。
3. [FFmpeg](https://ffmpeg.org/download.html)，将包含 `ffmpeg` 与 `ffprobe` 的目录加入 `PATH`。

在终端运行：

```powershell
git clone https://github.com/cwybruce/motion-diagram-studio.git
cd motion-diagram-studio
python -m pip install -r requirements-windows.txt
python scripts/make_capability_demos.py
python scripts/preview_server.py --port 8779
```

打开 **[http://127.0.0.1:8779/index.html](http://127.0.0.1:8779/index.html)**，选择 Demo、主题、角色和导出范围，再点击“导出当前方案”。服务只监听本机，生成的文件保存在 `examples/capability-demos/exports/`。

已生成的独立 HTML 可离线打开，也可部署到静态网站。**从 HTML 文件或静态托管网站浏览时，交互动画可用；生成新的 MP4 需要运行上面的本地 Python 预览服务。** 预生成的视频可直接下载。

## 示例与导出

| Demo | 场景 | 完整视频 |
| --- | --- | --- |
| [RAG 证据讲解](examples/capability-demos/rag-explainer/README.md) | 检索、评分、重排、引用与回答流向 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/rag-explainer/demo-pastel.mp4) |
| [多 Agent 任务交接](examples/capability-demos/agent-team/README.md) | 任务树、时间泳道、交接包与状态切换 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo-pastel.mp4) |
| [请求与缓存分支](examples/capability-demos/product-request/README.md) | 请求路径、缓存命中、回源与合流 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo-pastel.mp4) |
| [短视频知识卡](examples/capability-demos/knowledge-card/README.md) | 章节轮播、出处核对与回顾图谱 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo-pastel.mp4) |
| [业务工单流转](examples/capability-demos/business-workflow/README.md) | 四站看板、问题分流、复核与重试 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo-pastel.mp4) |
| [故障与恢复回放](examples/capability-demos/incident-replay/README.md) | 余量曲线、阈值、异常路径与恢复检查 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo-pastel.mp4) |
| [矢量组件实验室](examples/capability-demos/component-lab/README.md) | 光球、座位、圆环、流带、看板与人物组件 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo-pastel.mp4) |
| [角色导航与主题](examples/capability-demos/avatar-themes/README.md) | 蜘蛛 / 机器人、路径移动、目标框与关键词提示 | [暖黑](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo.mp4) · [暖纸](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo-light.mp4) · [经典终端](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo-terminal.mp4) · [经典粉彩](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo-pastel.mp4) |

<details>
<summary>展开其余 7 个 Demo 的动态预览</summary>

### 多 Agent 任务交接

[![多 Agent 任务交接动态预览](assets/readme/agent-team-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/agent-team/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#agent-team)

### 请求与缓存分支

[![请求与缓存分支动态预览](assets/readme/product-request-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/product-request/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#product-request)

### 短视频知识卡

[![短视频知识卡动态预览](assets/readme/knowledge-card-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/knowledge-card/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#knowledge-card)

### 业务工单流转

[![业务工单流转动态预览](assets/readme/business-workflow-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/business-workflow/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#business-workflow)

### 故障与恢复回放

[![故障与恢复回放动态预览](assets/readme/incident-replay-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/incident-replay/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#incident-replay)

### 矢量组件实验室

[![矢量组件实验室动态预览](assets/readme/component-lab-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/component-lab/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#component-lab)

### 角色导航与主题

[![角色导航与主题动态预览](assets/readme/avatar-themes-dark.gif)](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo.mp4)

[▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/avatar-themes/demo.mp4) · [交互体验](https://cwybruce.github.io/motion-diagram-studio/examples/capability-demos/index.html#avatar-themes)

</details>

<details>
<summary>参考画面复刻：初期完整成片与蜘蛛更新</summary>

这些动画来自本项目重新实现和渲染的成片。参考设计、布局与措辞的权利归原作者，业务数字仅用于视觉演示；来源与范围见 [第三方说明](THIRD_PARTY_NOTICES.md)。

| 初期完整成片 · 71 秒 | 蜘蛛更新 · 12 秒 |
| --- | --- |
| [![初期复刻动态预览](assets/readme/first-recreation.gif)](https://cwybruce.github.io/motion-diagram-studio/media/recreations/first-recreation.mp4) | [![蜘蛛更新动态预览](assets/readme/spider-recreation.gif)](https://cwybruce.github.io/motion-diagram-studio/media/recreations/spider-recreation.mp4) |
| [▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/media/recreations/first-recreation.mp4) | [▶ 完整 MP4](https://cwybruce.github.io/motion-diagram-studio/media/recreations/spider-recreation.mp4) |

</details>

### 功能块独立成片

RAG 重排证据区域，暖纸主题、机器人配置。点击预览观看完整的 **478 × 324、12 秒 MP4**。

[![RAG 重排证据：暖纸机器人分区动态预览](assets/readme/rag-rerank-light-drone.gif)](https://cwybruce.github.io/motion-diagram-studio/media/exports/robot/rag-rerank-light-drone.mp4)

[▶ 完整分区 MP4](https://cwybruce.github.io/motion-diagram-studio/media/exports/robot/rag-rerank-light-drone.mp4) · [浏览全部 39 个功能块与导出案例](https://cwybruce.github.io/motion-diagram-studio/#exports)

每个目录包含四套配色的配置 JSON、独立 HTML、MP4、PNG 预览图和说明。暖黑提供 `config-dark.json` / `live-dark.html`，以及默认入口 `config.json` / `live.html`，成片和预览图为 `demo.mp4` / `poster.png`；暖纸使用 `-light` 后缀，经典终端使用 `-terminal` 后缀，经典粉彩使用 `-pastel` 后缀。完整体验说明见 [能力体验馆](examples/capability-demos/README.md)。

重新生成全部四套配色视频：

```powershell
python scripts/make_capability_demos.py --render --themes all --jobs 2
```

只生成原来的暖黑与暖纸两套时，仍可使用 `--themes both`。

命令行也可独立导出一个 Demo 或其中一个功能块：

```powershell
# 整段：RAG、浅色主题、机器人
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view full --out examples/capability-demos/exports/rag-light.mp4

# 功能块：只导出 RAG 的重排区域
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view rag-rerank --out examples/capability-demos/exports/rag-rerank-light.mp4

# 经典终端配色：多 Agent 整段
python scripts/export_demo.py --scene agent-team --theme terminal-classic --avatar spider --view full --out examples/capability-demos/exports/agent-terminal.mp4

# 经典粉彩配色：RAG 重排功能块
python scripts/export_demo.py --scene rag-explainer --theme pastel-classic --avatar drone --view rag-rerank --out examples/capability-demos/exports/rag-rerank-pastel.mp4
```

功能块按实际画布裁剪，保留内部动画、文字和边缘泛光；可用的场景及区域 ID 记录在 [`manifest.json`](examples/capability-demos/manifest.json) 中。原有配置与成片不会被当前方案导出覆盖。

## 做自己的场景

复制一份示例配置，修改文本、数据、颜色与布局，再导出：

```powershell
python scripts/render.py --config my-config.json --out my-video.mp4 --html-out my-page.html
python scripts/check_frames.py --config my-config.json --out-dir my-frames --repeat
```

- [`references/config-schema.md`](references/config-schema.md)：元素、状态机、主题、角色与 `effects.neon` 参数。
- [`references/motion-grammar.md`](references/motion-grammar.md)：路径光点、状态变化和时间线动法。
- `scripts/rag_editorial.py`、`editorial_systems.py`、`editorial_stories.py`、`editorial_components.py`：八个 Demo 的配置与叙事数据。
- `assets/*editorial*.js`、`components.js`、`neon-flow.js`：SVG 绘制、组件、角色与流光。
- [`SKILL.md`](SKILL.md)：供编码 Agent 使用的原上游工作流。

如果直接编辑生成后的 JSON，用 `render.py` 导出；再次运行 `make_capability_demos.py` 会按生成器内容重建配置。坐标以画布像素计，改比例需要重新排版；`render.py --width / --height` 只缩放输出。

中文字体子集已内嵌，现有场景无需联网或安装字体。新增汉字后如需保持跨设备一致的排版，应重新构建子集，方法与原始字体来源见 [`assets/fonts/README.md`](assets/fonts/README.md)。

## 验证

```powershell
python -m unittest discover -s tests -v
python scripts/verify_capability_demos.py
python scripts/verify_demo_exports.py
```

浏览器和导出检查需要系统浏览器、FFmpeg 与 `ffprobe`；完整检查会渲染 / 解码视频，在体验馆目录生成 `verification.json` 和 `export-verification.json`。这些本机报告不随源码发布；请以自己环境里的运行结果为准。

## 来源、许可与致谢

本项目基于 [ythx-101/live-panel-skill](https://github.com/ythx-101/live-panel-skill)，扩展起点为 [`8a70aa2`](https://github.com/ythx-101/live-panel-skill/commit/8a70aa2c4e3fac68b40e2472407e32e2637a7a36)。保留上游代码的 **MIT License** 和版权声明；在此基础上新增能力体验馆、原创中文场景、SVG 组件、角色、四套配色和本地功能块导出。

上游的灵感及保留示例各有来源：

- [@thedelost](https://x.com/thedelost) 的 [Codex Agent 架构动态图](https://x.com/thedelost/status/2105398038026195279)，由 [@slashui](https://x.com/slashui/status/2105850132365443528) 引用传播；`examples/codex-agents/` 是其画面复刻，设计归原作者。
- `examples/agent-architecture/` 重现小红书 **@林纾** 的《AI Agent 的完整架构》静态信息图，设计、措辞和配色归原作者。
- `examples/airbnb/` 使用 [Latent.Space 访谈](https://www.latent.space/p/airbnb) 中 Airbnb 管理者自述的数据；跳动的计数用于演示。
- Noto Serif SC、Noto Sans SC 与 IBM Plex Mono 字体采用 **SIL OFL 1.1**，随仓库保留许可与更名子集说明。

MIT 许可覆盖代码，不将上述第三方视觉设计、文字、数据或字体重新授权为 MIT。来源及许可边界详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 与 [`LICENSE`](LICENSE)。用户提供的参考原视频和参考帧不公开；视频库中的“复刻演示”为本项目生成的成片，保留参考设计的原作者权利，并与八个原创场景分列。

## 静态网站与视频库维护

仓库根目录的 `index.html`、`assets/showcase.css` 和 `assets/showcase.js` 构成静态首页。八个 Demo 读取 `examples/capability-demos/manifest.json`，复刻与导出案例读取 [`media/catalog.json`](media/catalog.json)。视频均为仓库内真实 MP4，不依赖外部播放器；默认不预加载整段视频，播放一个视频时会暂停其他视频。

本站使用 GitHub Pages 的 `main` 分支根目录发布，并以 `.nojekyll` 保留静态文件。设置步骤见 [GitHub 官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。更新首页、案例清单或媒体后推送到 `main` 即可重新部署。

README 使用从实际成片生成的 GIF 节选展示动画，并链接到完整 MP4。GIF 与视频源文件随仓库保存，便于维护。更新成片后运行 `python scripts/make_readme_previews.py`，即可重新生成 `assets/readme/` 中的预览；需要 FFmpeg。

`media/exports/` 中 39 个浅色蜘蛛功能块由对应完整成片裁剪，另有 3 个通过渲染器按浅色机器人配置逐帧生成的全段 / 主流程 / 重排区域案例。两种生成方式在视频库明确标注。网站播放和下载已有成片，交互体验馆可调主题、角色与时间线；静态 Pages 不运行 Python 渲染器，生成新 MP4 需本地服务。

欢迎提交 Issue、改进场景或贡献组件。项目交流与联系方式：**[X / @sycbruce](https://x.com/sycbruce)**。
