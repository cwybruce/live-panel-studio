# 请求与缓存分支

缓存键值阵列、双路合流与独立模拟计数，共同解释命中、未命中和返回。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- 浅色主题
- cycle
- counter
- 条件分支
- 路径光点
- 架构布局
- 缓存键值阵列
- 两路合流
- 模拟计数轨迹
- LP 字体
- 竖屏图形叙事

## 观察与修改

- 缓存命中可以省去数据库读取
- 不同分支汇合到统一响应
- 计数器可展示明确标注的模拟指标

关键时刻：2s 命中缓存；6s 读取数据库；10s 返回客户端

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。

每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/product-request/config.json --out examples/capability-demos/product-request/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene product-request --theme light-pastel --view full --out examples/capability-demos/product-request/custom-light.mp4
```
