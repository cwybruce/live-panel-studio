# Live Panel 能力体验馆

8 个原创中文 Demo，展示当前引擎能做的流程动画、状态切换、数据组件、角色、主题与导出。
所有演示使用模拟数据与预设时间线，没有连接真实 Agent、数据库、工单或日志服务。
全部 8 个场景均有暖黑、暖纸、经典终端、经典粉彩四套竖屏配色：984×1280、细线、局部光感、各自的图形叙事。
经典终端与经典粉彩源于上游 skill 原有两套配色；布局、文案和动画沿用当前示例。
每个功能块的边缘有错开相位的霓虹扫光、渐隐拖尾与局部泛光，当前块更亮；浅色主题降低泛光。
标题使用 Noto Serif SC，正文 Noto Sans SC，英文与数字 IBM Plex Mono。
网页嵌入更名的 OFL 字体子集（LP Serif / Sans / Mono），无需安装字体或联网。
本地存在旧版网页时显示“旧版对照”；公开版本不要求这些历史对照文件。

运行 `启动预览.ps1`，或从仓库根目录执行 `python scripts/preview_server.py --port 8779`，
然后打开 http://127.0.0.1:8779/index.html 。预览服务同时提供本地 MP4 导出。

| 编号 | Demo | 能力 |
| --- | --- | --- |
| 1 | [RAG 证据讲解](rag-explainer/live.html) | 图形叙事, 路径光点, 文档阵列, 评分条, 引用流向, 蜘蛛导览, 确定性回放 |
| 2 | [多 Agent 任务交接](agent-team/live.html) | triggers, lane, cycle, 日志, 打字文本, 蜘蛛导览, 任务树, 时间泳道, 交接包, LP 字体, 竖屏图形叙事 |
| 3 | [请求与缓存分支](product-request/live.html) | 浅色主题, cycle, counter, 条件分支, 路径光点, 架构布局, 缓存键值阵列, 两路合流, 模拟计数轨迹, LP 字体, 竖屏图形叙事 |
| 4 | [短视频知识卡](knowledge-card/live.html) | 展开书页, 章节轮播, 信息流向, 出处核对, 回顾图谱, 蜘蛛导览, MP4 导出 |
| 5 | [业务工单流转](business-workflow/live.html) | 旅行工单, 四站看板, 问题分流, 完成比例, 复核状态, 重试支路, 模拟计数器 |
| 6 | [故障与恢复回放](incident-replay/live.html) | gauge, any_low, cycle, 指标条, 异常路径, 模拟日志, 余量曲线, 阈值圆环, 恢复检查, LP 字体, 竖屏图形叙事 |
| 7 | [矢量组件实验室](component-lab/live.html) | orb, seats, donut, ribbons, ghostSeats, kanban, 统一缩放 |
| 8 | [角色导航与主题](avatar-themes/live.html) | spider / drone, 路径移动, 目标框, 虚线指向, 关键词闪烁, 配色 / 大小 / 步频, 深浅主题, 确定性回放 |

播放器支持暂停、重播、拖动时间轴、0.5/1/2 倍速与关键时刻跳转。
含角色的场景可切换蜘蛛/机器人；全部示例可切换四种配色。
组件实验室的“组件视图”下拉框可放大查看六个组件。

每个目录都含 JSON 配置、独立 HTML、12 秒 MP4、预览图和说明。
每个 Demo 可独立导出整段 MP4，也可选择内部功能块单独导出（共 39 块）。
“导出当前方案”按当前主题、角色和范围生成 12 秒、30fps H.264 MP4。
功能块视频裁剪真实画布，保留文字、内部动画和边缘泛光，不将总览的缩放视图误当作裁剪。
导出文件另存于 `exports/`，原始配置和成片保留。无需连接外部服务。

从仓库根目录生成或重新导出：

```powershell
python scripts/make_capability_demos.py
python scripts/make_capability_demos.py --render --jobs 2
python scripts/make_capability_demos.py --render --themes light --jobs 2
python scripts/make_capability_demos.py --render --themes all --jobs 2
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view rag-rerank --out examples/capability-demos/rag-explainer/rerank-light.mp4
python scripts/verify_capability_demos.py
```

修改 `scripts/rag_editorial.py`、`editorial_systems.py`、`editorial_stories.py`、`editorial_components.py` 的数据与时间线，
或 `assets/*editorial*.js` 的图形布局后可以重新生成。
如果直接修改生成的 JSON，不要运行生成器覆盖它；使用 `scripts/render.py` 单独导出。
页面动画都由 `window.seek(t)` 驱动；`verification.json` 记录实际浏览器与视频检查结果。
`effects.neon` 可调整光效强度、扫光周期、主场景周期和拖尾长度，也可关闭；详见配置文档。

保留上游 MIT LICENSE 与 README 致谢。本组示例的可见文案、场景和数字采用原创配置与模拟数据，未打包参考视频。
独立 HTML 嵌入完整兼容组件库，其中保留旧示例的默认字符串；原有复刻示例的授权说明仍见仓库 README。
引擎和 SVG 动法基于原仓库及本地扩展。字体保留各自 OFL 许可，详见 `assets/fonts/README.md`。
