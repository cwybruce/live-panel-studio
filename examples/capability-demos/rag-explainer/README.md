# RAG 证据讲解

全幅流程、候选文档、评分筛选、引用与拒答；蜘蛛沿时间线引导当前步骤。

原创中文示例。所有事件、数字与状态来自预设时间线，未接入外部系统。

## 能力

- 图形叙事
- 路径光点
- 文档阵列
- 评分条
- 引用流向
- 蜘蛛导览
- 确定性回放

## 观察与修改

- 先检索候选，再筛选和核对依据；不能只看相关性分数。
- 引用应当定位到原文；缺少依据时明确说明。
- 细边界、局部光效和分区微图，支持暖黑与暖纸两种阅读环境。

关键时刻：1.5s 明确问题；4.5s 检索片段；7.5s 重排证据；10.5s 依据生成

文件：`config.json`（默认配置）、`live.html`（独立动画）、`demo.mp4`（暖黑主题默认角色）、`demo-light.mp4`（暖纸主题默认角色）、`poster.png`。

每个示例提供 `config-dark.json` / `config-light.json` 与对应 HTML。播放器主题同时切换场景与界面。

每个功能块带沿边缘流动的霓虹扫光与渐隐拖尾；在 `effects.neon` 中调整强度、周期与拖尾长度，或将 `enabled` 设为 `false` 关闭。

从仓库根目录重新导出：

```powershell
python scripts/render.py --config examples/capability-demos/rag-explainer/config.json --out examples/capability-demos/rag-explainer/demo.mp4
```

修改 JSON 中的角色：`avatar: "spider"` 或 `"drone"`；大小、配色和步频请参考配置文档。
“导出当前方案”按当前主题、角色与导出范围新建视频，不改变原始配置。范围可选整段或内部功能块；功能块保留完整 12 秒过程和边缘泛光。

单独导出此 Demo 的浅色版：

```powershell
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --view full --out examples/capability-demos/rag-explainer/custom-light.mp4
```
