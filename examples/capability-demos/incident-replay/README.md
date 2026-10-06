# 故障与恢复回放

依赖节点、余量曲线、阈值圆环与恢复检查，明确区分服务恢复和业务验收。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- gauge
- any_low
- cycle
- 指标条
- 异常路径
- 模拟日志
- 余量曲线
- 阈值圆环
- 恢复检查
- LP 字体
- 竖屏图形叙事

## 观察与修改

- 指标阈值可以驱动节点和连线样式
- 回放同一时刻能复现同一画面
- 真实运维需要额外的事件数据接口

关键时刻：2s 健康：0.94 / 0.91；6s 拥塞：0.36 / 0.24；10s 恢复：0.88 / 0.83

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑主题默认角色）、`demo-light.mp4`（暖纸主题默认角色）、`poster.png`。

每个示例提供 `config-dark.json` / `config-light.json` 与对应 HTML。播放器主题同时切换场景与界面。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/incident-replay/config.json --out examples/capability-demos/incident-replay/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene incident-replay --theme light-pastel --view full --out examples/capability-demos/incident-replay/custom-light.mp4
```
