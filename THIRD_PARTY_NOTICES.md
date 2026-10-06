# Third-party notices / 第三方来源与许可

本文件区分代码、示例视觉素材和字体的来源。仓库的 MIT 许可不替代第三方内容各自的许可或权利归属。

## 上游代码

- 项目：[ythx-101/live-panel-skill](https://github.com/ythx-101/live-panel-skill)。
- 本项目扩展起点：[`8a70aa2c4e3fac68b40e2472407e32e2637a7a36`](https://github.com/ythx-101/live-panel-skill/commit/8a70aa2c4e3fac68b40e2472407e32e2637a7a36)。
- 许可：MIT，原声明 `Copyright (c) 2026 live-panel contributors` 保留在 [`LICENSE`](LICENSE) 中。
- Live Panel Studio 在上游基础上扩展了八个中文能力示例、SVG 组件、角色与主题、霓虹流光、预览体验和本地 MP4 导出。

## 上游保留示例与参考设计

### `examples/codex-agents/`

该示例复刻了 **[@thedelost](https://x.com/thedelost)** 发布的 [Codex Agent 架构动态图](https://x.com/thedelost/status/2105398038026195279)。作品经 **[@slashui](https://x.com/slashui)** 的 [引用帖](https://x.com/slashui/status/2105850132365443528) 传播。

上游从视频画面重新实现了布局、内容和动法，并非原作者的代码。示例的视觉设计、布局和措辞归原作者，不属于本仓库 MIT 代码许可的授权范围。

### `examples/agent-architecture/`

该示例将小红书 **@林纾** 的《AI Agent 的完整架构》静态信息图做成动画。原图的布局、措辞与配色归原作者，画面页脚保留出处。该视觉设计不属于本仓库 MIT 代码许可的授权范围。

### `examples/airbnb/`

数字来源于 Airbnb 管理者在 [Latent.Space 访谈](https://www.latent.space/p/airbnb) 中的自述。动画计数为示意，不表示实时指标或经本项目独立核验的数据。

### 本地参考视频与商业信息图

开发过程中使用了用户提供的参考视频，并产生本地 `examples/business-infographic/` 复刻。原视频、参考帧和该复刻样例不作为本项目的新增公开内容打包。其参考设计、布局与措辞不因引擎代码采用 MIT 而获得 MIT 授权；原作者权利保留。

### `examples/capability-demos/`

八个能力示例的可见文案、场景叙事和模拟数字使用本项目新增配置。引擎与部分组件动法在上游和本地扩展基础上实现。独立 HTML 为自包含播放嵌入完整组件库，库中保留兼容旧示例的默认字符串；上述第三方示例的来源说明同样适用于这些字符串。

## 字体

| 发布名称 | 原始字体 | 来源 | 许可 |
| --- | --- | --- | --- |
| LP Serif | Noto Serif SC | [Noto CJK](https://github.com/notofonts/noto-cjk) | SIL OFL 1.1 |
| LP Sans | Noto Sans SC | [Noto CJK](https://github.com/notofonts/noto-cjk) | SIL OFL 1.1 |
| LP Mono | IBM Plex Mono Regular | [Google Fonts / IBM Plex Mono](https://github.com/google/fonts/tree/main/ofl/ibmplexmono) | SIL OFL 1.1 |

字体子集为修改后的版本，已更名为 LP Serif、LP Sans 和 LP Mono；字体版权与许可元数据保留在二进制中。OFL 原文保留在 `assets/fonts/`，并嵌入生成网页的注释。字体不采用本仓库的 MIT 代码许可。

来源、版本、哈希与字形覆盖记录见 [`assets/fonts/manifest.json`](assets/fonts/manifest.json)，构建方式见 [`assets/fonts/README.md`](assets/fonts/README.md)。捆绑的 IBM Plex Mono 原始字体文件同样适用其 OFL 许可。

## 运行依赖

Windows 渲染依赖通过 `requirements-windows.txt` 安装，可选字体构建依赖通过 `requirements-fonts.txt` 安装；它们的代码未复制进本仓库，适用各自软件包附带的许可。

Chrome / Edge 与 FFmpeg 由用户另外安装，没有作为本仓库二进制分发；它们适用各自的条款与许可。
