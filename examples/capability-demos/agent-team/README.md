# 多 Agent 任务交接

四角色交接、任务树、时间泳道与验收包，展示建议、状态与事件的同步回放。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- triggers
- lane
- cycle
- 日志
- 打字文本
- 蜘蛛导览
- 任务树
- 时间泳道
- 交接包
- LP 字体
- 竖屏图形叙事

## 观察与修改

- 任务交接需要携带验收依据
- 状态、建议和日志可以保持同步
- 本例尚未接入真实 Agent

关键时刻：1.5s 规划与建议；4.5s 检索交接；7.5s 实现交接；11.3s 审核与交付

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。

每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/agent-team/config.json --out examples/capability-demos/agent-team/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene agent-team --theme light-pastel --view full --out examples/capability-demos/agent-team/custom-light.mp4
```
