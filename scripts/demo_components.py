"""Original examples for the SVG component library and selectable avatars.

All numbers describe authored animation data. No external API or telemetry is used.
"""
from html import escape

from demo_common import actor, base, box, path, text


def _svg_text(x, y, value, size=12, color='#e8eff8', weight='normal'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}">{escape(value)}</text>')


def _tile(x, y, width, height, title, note):
    markup = (f'<rect x="1" y="1" width="{width-2}" height="{height-2}" '
              'rx="12" fill="#192331" stroke="#415269"/>')
    markup += _svg_text(15, 26, title, 16, '#8ab4ff', 'bold')
    markup += _svg_text(15, height-15, note, 11, '#9aacc2')
    return {'type': 'vector', 'x': x, 'y': y, 'w': width, 'h': height,
            'markup': '<g font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif">'
                      + markup + '</g>'}


def component_lab(preset='terminal-dark'):
    cfg = base('六种矢量组件，一张画布', '发光角色、汇聚节点、比例环、流带、虚实对比与任务看板。', preset)
    e = cfg['elements']
    for x, title, note in [(24, '01 · 发光角色', '浮动、渐变与脉冲光环'),
                           (336, '02 · 比例环', '六个分区 · 第一分区轻微呼吸'),
                           (648, '03 · 虚实对比', '虚线候选 → 四个高亮对象')]:
        e.append(_tile(x, 151, 288, 207, title, note))
    for x, title, note in [(24, '04 · 节点汇聚', '25 个候选节点 · 顺序收敛'),
                           (336, '05 · 分支流带', '五条动画路径 · 带宽为示意'),
                           (648, '06 · 任务看板', '停留、移动与完成状态')]:
        e.append(_tile(x, 374, 288, 212, title, note))
    e.extend([
        {'type': 'orb', 'x': 79, 'y': 184, 'w': 180, 'h': 147,
         'cy': 51, 'r': 33, 'color': '#52b9db', 'light': '#b8efff',
         'dark': '#183958', 'eyeColor': '#e7faff', 'label': '知识向导',
         'subtitle': '把注意力引向关键节点', 'detail': '原创演示角色'},
        {'type': 'donut', 'x': 340, 'y': 187, 'w': 460, 'h': 228, 'scale': .60,
         'labels': {'total': '100%', 'period': '示例分布',
                    'items': ['检索', '重排', '生成', '校验', '缓存', '其他'],
                    'values': ['30%', '20%', '20%', '10%', '10%', '10%'],
                    'notes': ['占比来自预设配置', '高亮分区可用于讲解', '动画摆动不代表实时变化']},
         'data': {'parts': [.3, .2, .2, .1, .1, .1], 'pulseAmount': .025}},
        {'type': 'ghostSeats', 'x': 656, 'y': 189, 'w': 480, 'h': 218, 'scale': .55,
         'labels': {'topValue': '25', 'topCaption': '候选知识片段', 'middleValue': '8',
                    'middleLines': ['初步检索命中', '进入后续筛选'], 'bottomValues': ['4', '3'],
                    'bottomLines': ['四个重点对象', '逐渐显现', '其中三个高亮', '一个待人工复核']},
         'data': {'revealPeriod': 12, 'revealStart': 3, 'revealDuration': 3}},
        {'type': 'seats', 'x': 28, 'y': 432, 'w': 833, 'h': 148, 'scale': .334,
         'period': 12,
         'labels': {'title': '候选节点逐个汇入协调中心', 'leader': '协调器',
                    'teams': ['检索', '分析', '验证', '输出'], 'hub': ['汇聚', '中心'],
                    'count': '已选', 'captions': ['已选节点', '处理片段', '任务单位', '总候选']},
         'data': {'metrics': [{'perSeat': 1, 'suffix': ' 项'},
                              {'perSeat': 4, 'suffix': ' 段'},
                              {'perSeat': 2, 'suffix': ' 单位'},
                              {'value': 25, 'suffix': ' 项'}]}},
        {'type': 'ribbons', 'x': 337, 'y': 401, 'w': 568, 'h': 280, 'scale': .495,
         'labels': {'source': '一份查询请求', 'branches': ['检索路径', '重排路径', '生成路径', '校验路径', '输出路径'],
                    'values': ['A', 'B', 'C', 'D', 'E'],
                    'footer': '路径粒子用于讲解流向，宽度为视觉示意'}},
        {'type': 'kanban', 'x': 654, 'y': 399, 'w': 439, 'h': 227, 'scale': .62,
         'period': 12, 'tickets': ['工单01', '工单02', '工单03', '工单04', '工单05', '工单06'],
         'labels': {'columns': ['待处理', '进行中', '待复核', '已完成'],
                    'countCaption': '演示进度单位', 'footer': '计数预设独立于卡片位置，并非真实工单统计'},
         'data': {'countStart': 0, 'countMax': 24, 'countRate': 24, 'countPeriod': 12}},
    ])
    e.extend([text(44, 512, '节点与计数同步演示', 13, 'dim'),
              text(44, 536, '原始几何可统一缩放', 13, 'dim')])
    return cfg


def avatar_themes(preset='terminal-dark'):
    cfg = base('角色导航与视觉主题', '蜘蛛沿路径游走，指向当前目标；角色、配色、大小与步频可配置。', preset)
    e = cfg['elements']
    stages = [
        (40, '检索依据', '找到与问题相关的片段', '先看证据，再组织回答', 'cy'),
        (350, '检查依据', '核对来源与上下文', '标记不充分的部分', 'ye'),
        (660, '解释结果', '突出结论和关键步骤', '让读者理解发生了什么', 'gr'),
    ]
    for x, title, first, second, color in stages:
        e.append(box(x, 213, 260, 175, title,
                     [{'t': first, 'size': 14}, {'t': second, 'size': 14}], c=color))
    e.extend([path([[300, 300], [350, 300]], 'cy', 2),
              path([[610, 300], [660, 300]], 'gr', 2),
              text(40, 537, '框与虚线：当前讲解目标', 15, 'cy'),
              text(40, 563, '关键词轻闪：引导注意力；移动和步态始终由时间线决定。', 14, 'dim')])
    guide = actor([[170, 459], [480, 459], [790, 459]],
                  targets=[{'x': x, 'y': 213, 'w': 260, 'h': 175} for x in (40, 350, 660)],
                  scale=.56)
    guide.update(focusPeriod=4, gaitSpeed=9,
                 avatarColors={'leg': '#f89573', 'joint': '#88e6cf',
                               'shell': '#ac94ed', 'core': '#ffd38c'},
                 words=[{'x': 74, 'y': 357, 'w': 82, 't': '找到依据'},
                        {'x': 384, 'y': 357, 'w': 82, 't': '检查依据'},
                        {'x': 694, 'y': 357, 'w': 82, 't': '解释结果'}])
    e.append(guide)
    return cfg


def scenes():
    return [
        {'id': 'component-lab', 'title': '矢量组件实验室', 'category': '组件与角色',
         'summary': '六种现有矢量组件的原创中文示例，使用预设数据。',
         'capabilities': ['orb', 'seats', 'donut', 'ribbons', 'ghostSeats', 'kanban', '统一缩放'],
         'learn': ['六种组件如何组合', '如何更换中文标签与示例数值', '流带宽度与计数的证据边界'],
         'checkpoints': [{'time': 0, 'label': '候选与初始比例'}, {'time': 4, 'label': '虚线对象开始显现'},
                         {'time': 7, 'label': '四个重点对象与任务推进'}, {'time': 10, 'label': '汇聚与看板后段'}],
         'themeSwitch': False, 'config': component_lab()},
        {'id': 'avatar-themes', 'title': '角色导航与主题', 'category': '组件与角色',
         'summary': '展示蜘蛛游走、目标高亮、关键词，以及角色和视觉主题切换。',
         'capabilities': ['spider / drone', '路径移动', '目标框', '虚线指向', '关键词闪烁', '配色 / 大小 / 步频', '深浅主题'],
         'learn': ['角色如何引导注意力', '同一时间线切换角色', '主题变化与角色样式分别配置'],
         'checkpoints': [{'time': 0, 'label': '指向检索依据'}, {'time': 4, 'label': '指向检查依据'},
                         {'time': 8, 'label': '指向解释结果'}],
         'themeSwitch': True, 'config': avatar_themes()},
    ]
