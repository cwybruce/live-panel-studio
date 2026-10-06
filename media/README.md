# 视频库

首页从 [`catalog.json`](catalog.json) 读取视频的标题、路径、尺寸、时长、主题、角色和生成方式。所有路径相对网站根目录，可部署于 GitHub Pages 的项目子路径。视频已将 MP4 索引移至文件开头，以支持在线播放；海报取自各自视频，不是参考原视频帧。

- `recreations/`：本项目按用户提供的参考画面重新实现的 71 秒完整信息面板与 12 秒蜘蛛更新演示。原作者身份尚未确认，原始参考视频及其参考帧未公开。参考设计、布局和措辞的权利归原作者，详见 [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md)。
- `exports/<scene>/`：八个原创能力 Demo 的 39 个浅色功能块。由相应完整 MP4 成片按 `manifest.json` 中的 `exportViews.crop` 裁剪，不是 39 次独立浏览器渲染。
- `exports/robot/`：RAG 浅色机器人整段、主流程和重排区域，按该配置经浏览器逐帧渲染生成，展示主题、角色和范围选择共同生效。

八个 Demo 的完整深浅成片位于 [`examples/capability-demos/`](../examples/capability-demos/README.md)。全部内容为预设模拟，没有连接真实业务系统。

生成自己的整段 / 功能块视频：

```powershell
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view full --out out/rag-full.mp4
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view rag-rerank --out out/rag-rerank.mp4
```

添加已生成的视频时，用清晰的文件名、真实视频海报和媒体参数更新 `catalog.json`；`method` 使用 `renderer`（按配置渲染）或 `crop`（从对应完整成片裁剪）。请只收录有意公开的媒体，不加入本地作业日志、参考原文件或含绝对路径的验证报告。
