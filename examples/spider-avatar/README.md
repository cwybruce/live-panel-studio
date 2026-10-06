# 机械蜘蛛近景

先看 `live.html` 或 `spider-closeup.mp4`。四对八条分节腿、红色腿段、绿色关节和脚端、蓝紫双段甲壳与粉色核心；两组四足交替抬脚与回摆。

近景图：`screenshots/frame_1_t01.00.png` 等。

在仓库根目录运行：

```powershell
python scripts/make_spider_demo.py
python scripts/render.py --config examples/spider-avatar/config.json --out examples/spider-avatar/spider-closeup.mp4 --html-out examples/spider-avatar/live.html
python scripts/check_frames.py --config examples/spider-avatar/config.json --out-dir examples/spider-avatar/screenshots --samples 60 --png 4 --repeat
```

组件仍使用 `type: "drone"` 来复用游走轨迹、指向线和高亮，新增 `avatar: "spider"` 选择造型；`avatar: "drone"` 继续使用之前的机器人。
`avatarScale` 控制角色缩放，`avatarColors` 可覆盖 `leg`、`joint`、`shell`、`core`，`gaitSpeed` 为步态角频率（弧度/秒）。
`avatarHeading` 可以固定角色朝向（度），省略时朝向随轨迹平滑变化。近景例固定为 0 度，以便看清八条腿。
所有动画仍由 `seek(t)` 确定计算，不依赖随机数或累计状态。
