"""Original Chinese teaching scenes for the current, time-driven engine.

These examples describe scripted simulations. They neither connect to a live
Agent runtime nor collect application metrics.
"""

from demo_common import actor, base, box, path, text


def _line(t, c="fg", **extra):
    return dict(t=t, c=c, **extra)


def _var(name, c=None):
    run = {"v": name}
    if c:
        run["c"] = c
    return {"runs": [run]}


def _eq(name, value):
    return {"var": name, "eq": value}


def _branch(points, color, period, when):
    """Leave the inactive route dim; only its active route carries packets."""
    e = path(points, "line", period, when,
             {"color": color, "width": 3, "opacity": 1})
    e["opacity"] = .35
    e["flow"]["color"] = color
    return e


def _log(y=504, rows=3):
    return {"type": "log", "x": 36, "y": y, "w": 888,
            "rows": rows, "padTop": 10, "padBottom": 12, "padLeft": 18,
            "title": "模拟事件记录", "titleX": 24, "titleW": 180,
            "cols": [{"key": "time", "x": 0}, {"key": "who", "x": 110},
                     {"key": "m", "x": 225}]}


def _scene(scene_id, title, category, summary, capabilities, learn, checkpoints, cfg):
    return {"id": scene_id, "title": title, "category": category,
            "summary": summary, "capabilities": capabilities, "learn": learn,
            "checkpoints": [{"time": t, "label": label} for t, label in checkpoints],
            "config": cfg}


def rag_explainer():
    cfg = base("RAG：让回答跟着证据走", "四步循环：明确问题 → 检索片段 → 重排证据 → 生成回答")
    cfg["theme"]["lineHeight"] = 24
    cfg["machines"] = {
        "rag": {"type": "cycle", "period": 3, "values": [
            {"t": "① 明确问题", "detail": "先确定用户要解决的问题，避免把不相关文档送入后续步骤。"},
            {"t": "② 检索知识", "detail": "从知识库取出候选片段；检索结果只是候选依据。"},
            {"t": "③ 重排证据", "detail": "保留最相关的两条证据，剔除弱关联片段。"},
            {"t": "④ 生成回答", "detail": "依据已选片段生成回答；没有依据的问题需要明确说明。"},
        ]},
    }
    e = cfg["elements"]
    e += [text(36, 153, "当前步骤：{rag}", 16, "cy", b=True)]
    nodes = [
        (36, "用户提问", ["如何重置密码？", "明确问题范围"], "cy"),
        (266, "检索知识", ["候选片段：3 条", "找到相关文档"], "bl"),
        (496, "重排证据", ["保留片段：2 条", "剔除弱关联内容"], "pu"),
        (726, "生成回答", ["先引用，再解释", "缺少依据时说明"], "gr"),
    ]
    for i, (x, title, lines, color) in enumerate(nodes):
        e.append(box(x, 191, 198, 120, title, [_line(s, "dim") for s in lines], color,
                     _eq("rag.i", i), {"glow": color, "border": 3, "fill": "hl"}))
    for i in range(3):
        e.append(_branch([[234 + i * 230, 250], [266 + i * 230, 250]],
                         "cy", 1.2, _eq("rag.i", i)))
    e += [text(36, 349, "{rag.detail}", 15, "fg"),
          box(36, 390, 428, 119, "可核对的回答", [
              _line("进入登录页，点击“忘记密码”。"),
              _line("按邮件中的链接重置密码。"),
              _line("依据：账户帮助 / 第 2 节", "gr"),
          ], "gr"),
          box(496, 390, 428, 119, "缺少证据时", [
              _line("问题：管理员口令是什么？"),
              _line("文档没有给出这项信息。"),
              _line("回答：无法据此确认。", "ye"),
          ], "ye"),
          text(36, 548, "观察：亮框指示当前步骤，移动光点表示片段或问题正在传递。", 15, "dim"),
          text(36, 578, "本例展示流程机制；文字、片段数量和回答均为预先编写。", 14, "dim")]
    return _scene("rag-explainer", "RAG 证据讲解", "AI 技术教学",
                  "用高亮节点和流动光点解释问题如何经过检索、重排与生成。",
                  ["cycle", "box", "path", "flow", "条件高亮", "确定性回放"],
                  ["检索结果需要再筛选", "回答应能对照证据", "预设演示与真实检索需要区分"],
                  [(1.5, "明确问题"), (4.5, "检索片段"), (7.5, "重排证据"), (10.5, "依据生成")], cfg)


def agent_team():
    cfg = base("多 Agent：一次任务，四次交接", "十二秒模拟循环：角色分工、打字建议和事件记录，共用一条时间线")
    cfg["theme"]["lineHeight"] = 24
    cfg["clock"]["start"] = "09:00:00"
    cfg["machines"] = {
        "handoff": {"type": "triggers", "period": 3, "on": 2.8, "t0": 0,
                    "color": "pu", "cps": 28, "callsStart": 1,
                    "onText": "正在交接", "offText": "准备下一步",
                    "items": [
                        {"name": "规划", "adv": ["拆成三个可验收的小任务。", "交给检索角色补齐所需资料。"]},
                        {"name": "检索", "adv": ["找到接口约束和数据样例。", "把证据连同来源交给实现角色。"]},
                        {"name": "实现", "adv": ["按约束完成最小实现。", "把补丁和复现方法交给审核角色。"]},
                        {"name": "审核", "adv": ["核对行为、边界和证据。", "记录可验收结果，再交付用户。"]},
                    ],
                    "log": {"who": "协作", "c": "pu", "start": {"m": "开始：{name}"},
                            "end": {"m": "完成：{name}，准备交接"}}},
        "task": {"type": "lane", "period": 12, "run": 10.8, "off": 0,
                 "busy": "任务协作中", "done": ["本轮已交付"],
                 "busyColor": "cy", "doneColor": "gr"},
    }
    # Separate cycles make waiting, working and delivered states explicit.
    states = [
        ["正在规划", "计划已交接", "计划已交接", "计划已交接"],
        ["等待计划", "正在检索", "证据已交接", "证据已交接"],
        ["等待证据", "等待证据", "正在实现", "补丁已交接"],
        ["等待补丁", "等待补丁", "等待补丁", "核对并交付"],
    ]
    for i, values in enumerate(states):
        cfg["machines"]["role" + str(i)] = {"type": "cycle", "period": 3, "values": values}
    e = cfg["elements"]
    e += [text(36, 151, "本轮状态：", 15, "dim"),
          {"type": "text", "x": 124, "y": 151, "size": 15, "runs": [{"v": "task"}]}]
    roles = [
        (36, "规划角色", "明确验收条件", "cy"),
        (266, "检索角色", "补齐接口证据", "bl"),
        (496, "实现角色", "编写最小补丁", "pu"),
        (726, "审核角色", "核对边界行为", "gr"),
    ]
    for i, (x, title, desc, color) in enumerate(roles):
        e.append(box(x, 181, 198, 119, title, [_line(desc, "dim"), _var("role" + str(i), color)],
                     color, _eq("handoff.cur", i), {"glow": color, "border": 3}))
    for i in range(3):
        e.append(_branch([[234 + i * 230, 241], [266 + i * 230, 241]], "cy", 1,
                         _eq("handoff.active", i)))
    e += [actor([[135, 347], [365, 347], [595, 347], [825, 347]],
                targets=[{"x": x - 4, "y": 177, "w": 206, "h": 127} for x, _, _, _ in roles],
                scale=.36),
          box(36, 392, 888, 91, "当前交接说明", [
              _var("handoff.adv0", "fg"), _var("handoff.adv1", "dim")], "pu"),
          _log(508, 3)]
    return _scene("agent-team", "多 Agent 任务交接", "协作过程展示",
                  "四种角色依次工作，蜘蛛引导视线，交接建议和日志随时间更新。",
                  ["triggers", "lane", "cycle", "日志", "打字文本", "蜘蛛导览"],
                  ["任务交接需要携带验收依据", "状态、建议和日志可以保持同步", "本例尚未接入真实 Agent"],
                  [(1.5, "规划与建议"), (4.5, "检索交接"), (7.5, "实现交接"), (11.3, "审核与交付")], cfg)


def product_request():
    cfg = base("一次请求：命中缓存，还是读取数据库？", "用互斥分支展示系统行为，再沿返回链路把结果送回用户", preset="light-pastel")
    cfg["theme"]["lineHeight"] = 24
    cfg["machines"] = {
        "route": {"type": "cycle", "period": 4, "values": [
            {"t": "缓存命中", "detail": "已有结果可复用：从缓存直接进入响应整理。"},
            {"t": "缓存未命中", "detail": "缓存没有结果：读取数据库，再进入响应整理。"},
            {"t": "返回用户", "detail": "统一结果格式，把响应沿返回链路送回用户。"},
        ]},
        "requests": {"type": "counter", "start": 0, "rate": 18, "format": "comma"},
    }
    e = cfg["elements"]
    e += [text(36, 153, "当前演示：{route}", 16, "cy", b=True),
          box(36, 187, 200, 101, "客户端", [_line("查询商品库存", "dim"), _line("发起 / 接收请求")], "cy"),
          box(326, 187, 220, 101, "API 服务", [_line("校验参数", "dim"), _line("选择查询分支")], "bl"),
          box(704, 187, 220, 101, "缓存", [_line("已存储的查询结果", "dim"),
              _line("状态：{route}", "cy")], "cy", _eq("route.i", 0), {"glow": "gr", "color": "gr"}),
          box(704, 356, 220, 101, "数据库", [_line("读取原始库存记录", "dim"), _line("仅未命中时进入")], "pu",
              _eq("route.i", 1), {"glow": "pu", "border": 3}),
          box(326, 356, 220, 101, "响应整理", [_line("统一输出格式", "dim"), _line("返回库存结果")], "gr",
              _eq("route.i", 2), {"glow": "gr", "border": 3})]
    initial = {"var": "route.i", "in": [0, 1]}
    e += [_branch([[236, 236], [326, 236]], "cy", 1.4, initial),
          _branch([[546, 236], [704, 236]], "bl", 1.4, initial),
          _branch([[814, 288], [814, 356]], "pu", 1.4, _eq("route.i", 1)),
          _branch([[704, 406], [546, 406]], "pu", 1.4, _eq("route.i", 1)),
          _branch([[704, 260], [624, 260], [624, 322], [436, 322], [436, 356]],
                  "gr", 2, _eq("route.i", 0)),
          _branch([[326, 406], [136, 406], [136, 288]], "gr", 2, _eq("route.i", 2)),
          text(551, 306, "命中：直接返回", 12, "gr"),
          text(831, 322, "未命中", 12, "pu"),
          box(36, 497, 888, 90, "{route}", [
              _line("{route.detail}"),
              _line("模拟请求计数：{requests}  ·  计数器独立演示，非线上流量。", "dim")], "cy")]
    return _scene("product-request", "请求与缓存分支", "产品与架构演示",
                  "浅色系统图展示命中与未命中的两条路径，以及结果返回过程。",
                  ["浅色主题", "cycle", "counter", "条件分支", "路径光点", "架构布局"],
                  ["缓存命中可以省去数据库读取", "不同分支汇合到统一响应", "计数器可展示明确标注的模拟指标"],
                  [(2, "命中缓存"), (6, "读取数据库"), (10, "返回客户端")], cfg)


def incident_replay():
    cfg = base("故障回放：从拥塞到恢复", "十二秒模拟循环：重放健康、异常和恢复，观察余量与依赖路径")
    cfg["theme"]["lineHeight"] = 24
    cfg["clock"]["start"] = "09:00:00"
    cfg["machines"] = {
        "phase": {"type": "cycle", "period": 4, "values": [
            {"t": "服务稳定", "reason": "工作池与存储余量充足，依赖链保持正常。", "m": "健康检查通过"},
            {"t": "出现拥塞", "reason": "两个余量指标低于阈值，需要定位共享瓶颈。", "m": "余量不足，标记异常依赖"},
            {"t": "恢复服务", "reason": "模拟排队压力解除；余量回升，再核对任务结果。", "m": "余量回升，开始恢复验证"},
        ], "log": {"who": "回放", "c": "cy"}},
        # Hash seed 3 deterministically selects indexes 0, 1, 2 at t=0, 4, 8.
        "pool": {"type": "gauge", "values": [.94, .36, .88], "period": 4,
                 "seed": 3, "threshold": .7, "decimals": 2,
                 "high": {"label": "余量正常"}, "low": {"label": "余量不足"},
                 "highColor": "gr", "lowColor": "rd"},
        "storage": {"type": "gauge", "values": [.91, .24, .83], "period": 4,
                    "seed": 3, "threshold": .7, "decimals": 2,
                    "high": {"label": "余量正常"}, "low": {"label": "余量不足"},
                    "highColor": "gr", "lowColor": "rd"},
        "health": {"type": "any_low", "of": ["pool", "storage"]},
    }
    e = cfg["elements"]
    e += [text(36, 153, "当前阶段：{phase}", 16, "cy", b=True),
          box(36, 192, 220, 131, "入口服务", [_line("请求持续进入", "dim"),
              _line("检查下游可用性"), _line("不把失败当成功")], "cy"),
          box(370, 192, 220, 131, "工作池", [_line("消耗执行资源", "dim"),
              _var("pool.label"), _line("可用余量：{pool}")], "gr",
              _eq("health", "low"), {"color": "rd", "glow": "rd", "border": 3}),
          box(704, 192, 220, 131, "存储服务", [_line("读取 / 写入结果", "dim"),
              _var("storage.label"), _line("可用余量：{storage}")], "gr",
              _eq("storage.low", "1"), {"color": "rd", "glow": "rd", "border": 3})]
    for points in [[[256, 257], [370, 257]], [[590, 257], [704, 257]]]:
        for state, color in [("high", "gr"), ("low", "rd")]:
            p = path(points, "line", 1.3, _eq("health", state),
                     {"color": color, "width": 3, "opacity": 1})
            p["opacity"] = 0
            p["flow"]["color"] = color
            e.append(p)
    for x, machine, title in [(36, "pool", "工作池余量"), (340, "storage", "存储余量")]:
        e.append(box(x, 375, 280, 132, title, [
            {"items": [{"bar": {"w": 236, "h": 16, "gauge": machine,
                                 "high": "gr", "low": "rd"}}]},
            _line("数值：{" + machine + "} / 1.00", "fg"),
            _line("告警阈值：0.70", "dim"),
        ], "cy"))
    e += [box(644, 375, 280, 132, "如何判断", [
              _line("任一指标低于阈值", "dim"),
              _line("→ 标记异常依赖", "rd"),
              _line("恢复后仍需核对结果", "dim"),
          ], "ye"),
          text(36, 344, "{phase.reason}", 15, "fg"), _log(541, 2)]
    return _scene("incident-replay", "故障与恢复回放", "运维机制演示",
                  "预设故障在第 4 秒发生，第 8 秒恢复；指标条、告警与日志同步变化。",
                  ["gauge", "any_low", "cycle", "指标条", "异常路径", "模拟日志"],
                  ["指标阈值可以驱动节点和连线样式", "回放同一时刻能复现同一画面", "真实运维需要额外的事件数据接口"],
                  [(2, "健康：0.94 / 0.91"), (6, "拥塞：0.36 / 0.24"), (10, "恢复：0.88 / 0.83")], cfg)


def scenes():
    """Return the four authored scenes without file IO or rendering."""
    return [rag_explainer(), agent_team(), product_request(), incident_replay()]
