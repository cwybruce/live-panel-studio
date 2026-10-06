# 短视频知识卡

展开书页，把输入、过程、输出与回顾做成有图形关系的四章讲解。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- 展开书页
- 章节轮播
- 信息流向
- 出处核对
- 回顾图谱
- 蜘蛛导览
- MP4 导出

## 观察与修改

- 先说明问题和已有材料，再展示处理关系，最后核对输出。
- 四章讲解每 3 秒推进一次；计数器展示模拟播放次数。
- 动画、光点、引用与强调状态都可以暂停、跳转和确定性回放。

关键时刻：0.8s 明确输入；3.8s 展示过程；6.8s 检查输出；9.8s 回顾要点

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑）、`demo-light.mp4`（暖纸）、`demo-terminal.mp4`（经典终端）、`demo-pastel.mp4`（经典粉彩）；四套成片均使用默认角色。

预制 MP4 由 Releases 分发。需要本地观看成片时，从仓库根目录运行 `python scripts/media_assets.py download --set demos`；交互 HTML 和生成新视频不依赖这些预制成片。

每个示例提供 `config-dark.json` / `config-light.json` / `config-terminal.json` / `config-pastel.json` 与对应 HTML。播放器主题同时切换场景与界面，导出跟随当前主题。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/knowledge-card/config.json --out examples/capability-demos/knowledge-card/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene knowledge-card --theme light-pastel --view full --out examples/capability-demos/knowledge-card/custom-light.mp4
```
