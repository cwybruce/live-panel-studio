# 矢量组件实验室

六种真实可复用 SVG 组件，用四套深浅配色展示各自的动画与用途。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- orb
- seats
- donut
- ribbons
- ghostSeats
- kanban
- 统一缩放

## 观察与修改

- 组件保留真实几何和动画，可通过 JSON 组合与复用。
- 标签、示例数值和显现时间都可以配置。
- 流带宽度是示意；看板计数独立于卡片位置，不是实时统计。

关键时刻：1.5s 角色与初始比例；4.5s 候选对象显现；7.5s 节点汇聚与任务推进；10.5s 后段计数与流带

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。

预制 MP4 由 Releases 分发。需要本地观看成片时，从仓库根目录运行 `python scripts/media_assets.py download --set demos`；交互 HTML 和生成新视频不依赖这些预制成片。

每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。

展示样式与配色分别选择：原版图解保留原有排版；macOS 终端加入窗口外壳、等宽文字、字符边框、模拟日志与命令光标。终端配置、网页、视频与海报使用 `config-console-*` / `live-console-*` / `demo-console-*` / `poster-console-*` 文件名。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/component-lab/config.json --out examples/capability-demos/component-lab/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene component-lab --theme light-pastel --view full --out examples/capability-demos/component-lab/custom-light.mp4
```

导出此 Demo 的经典终端配色与 macOS 终端样式：

```powershell
python scripts/export_demo.py --scene component-lab --theme terminal-classic --style terminal --view full --out examples/capability-demos/component-lab/custom-console.mp4
```
