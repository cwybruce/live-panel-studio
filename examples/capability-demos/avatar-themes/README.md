# 角色导航与主题

八足蜘蛛游走、热区脉冲、目标聚焦与时间线；支持角色切换和深浅主题。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- spider / drone
- 路径移动
- 目标框
- 虚线指向
- 关键词闪烁
- 配色 / 大小 / 步频
- 深浅主题
- 确定性回放

## 观察与修改

- 角色与聚焦框一起引导读者关注当前步骤。
- 切换角色不会改变时间线；角色样式和主题分别配置。
- 浅色页读取主题颜色，不依赖固定的深色 SVG 背景。

关键时刻：1.5s 聚焦检索依据；5.5s 聚焦核对上下文；9.5s 聚焦解释结果

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。

预制 MP4 由 Releases 分发。需要本地观看成片时，从仓库根目录运行 `python scripts/media_assets.py download --set demos`；交互 HTML 和生成新视频不依赖这些预制成片。

每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/avatar-themes/config.json --out examples/capability-demos/avatar-themes/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene avatar-themes --theme light-pastel --view full --out examples/capability-demos/avatar-themes/custom-light.mp4
```
