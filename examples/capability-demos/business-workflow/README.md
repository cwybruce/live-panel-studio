# 业务工单流转

六张工单在四站看板流转，配合分配拓扑、完成环、复核轨迹与补充资料的重试支路。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- 旅行工单
- 四站看板
- 问题分流
- 完成比例
- 复核状态
- 重试支路
- 模拟计数器

## 观察与修改

- 工单依次经历受理、处理、复核、完成；转交应当附带处理依据。
- 6 秒复核周期包含 4 秒处理与 2 秒完成状态。
- 5–9 秒演示资料缺失与返回补充，随后重新进入复核。

关键时刻：1s 受理与分流；5s 处理与复核；7s 补齐资料；10s 重新复核

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑主题默认角色）、`demo-light.mp4`（暖纸主题默认角色）、`poster.png`。

每个示例提供 `config-dark.json` / `config-light.json` 与对应 HTML。播放器主题同时切换场景与界面。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/business-workflow/config.json --out examples/capability-demos/business-workflow/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene business-workflow --theme light-pastel --view full --out examples/capability-demos/business-workflow/custom-light.mp4
```
