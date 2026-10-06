"""Editorial portrait examples for the existing SVG library and avatar guide."""


COLORS = {'bg': '#12110f', 'panel': '#191713', 'surface': '#171511',
          'line': '#3c352c', 'fg': '#eee9df', 'dim': '#9f9587',
          'ye': '#dfb96d', 'cy': '#64bed0', 'pi': '#e776af',
          'gr': '#88c4a2', 'rd': '#d77768'}


def _base(title):
    return {'meta': {'title': title, 'lang': 'zh-CN'},
            'canvas': {'width': 984, 'height': 1280, 'duration': 12, 'fps': 30},
            'theme': {'preset': 'terminal-dark', 'font': 'LP Sans', 'colors': dict(COLORS)},
            'machines': {}, 'elements': []}


def component_lab():
    cfg = _base('矢量组件实验室 · 六种组件的视觉讲解')
    cfg['elements'] = [
        {'type': 'labEditorial', 'x': 0, 'y': 0, 'w': 984, 'h': 1280},
        {'type': 'orb', 'x': 84, 'y': 226, 'w': 200, 'h': 198,
         'cy': 77, 'r': 52, 'color': '#64bed0', 'light': '#e0efe4',
         'dark': '#203b3b', 'eyeColor': '#faf6ed', 'label': '知识向导',
         'subtitle': '浮动 · 渐变 · 光环', 'detail': 'ORIGINAL VECTOR / 01'},
        {'type': 'seats', 'x': 73, 'y': 530, 'w': 833, 'h': 166, 'period': 12,
         'labels': {'title': '候选节点逐个汇入协调中心', 'leader': '协调器',
                    'teams': ['检索', '分析', '验证', '输出'], 'hub': ['汇聚', '中心'],
                    'count': '已选', 'captions': ['已选节点', '处理片段', '任务单位', '总候选']},
         'data': {'metrics': [{'perSeat': 1, 'suffix': ' 项'}, {'perSeat': 4, 'suffix': ' 段'},
                              {'perSeat': 2, 'suffix': ' 单位'}, {'value': 25, 'suffix': ' 项'}]}},
        {'type': 'donut', 'x': 41, 'y': 746, 'w': 460, 'h': 228, 'scale': .86,
         'labels': {'total': '100%', 'period': '示例分布',
                    'items': ['检索', '重排', '生成', '校验', '缓存', '其他'],
                    'values': ['30%', '20%', '20%', '10%', '10%', '10%'],
                    'notes': ['占比来自预设配置', '高亮分区用于讲解', '呼吸变化为视觉示意']},
         'data': {'parts': [.3, .2, .2, .1, .1, .1], 'pulseAmount': .025}},
        {'type': 'ghostSeats', 'x': 524, 'y': 759, 'w': 480, 'h': 218, 'scale': .80,
         'labels': {'topValue': '25', 'topCaption': '候选知识片段', 'middleValue': '8',
                    'middleLines': ['初步检索命中', '进入后续筛选'], 'bottomValues': ['4', '3'],
                    'bottomLines': ['四个重点对象', '逐渐显现', '其中三个高亮', '一个待人工复核']},
         'data': {'revealPeriod': 12, 'revealStart': 3, 'revealDuration': 3}},
        {'type': 'ribbons', 'x': 43, 'y': 985, 'w': 568, 'h': 280, 'scale': .73,
         'labels': {'source': '输入请求',
                    'branches': ['检索路径', '重排路径', '生成路径', '校验路径', '输出路径'],
                    'values': ['A', 'B', 'C', 'D', 'E'], 'footer': '流带宽度为视觉示意，数值来自作者配置'}},
        {'type': 'kanban', 'x': 519, 'y': 989, 'w': 439, 'h': 227, 'scale': .90,
         'period': 12, 'tickets': ['工单01', '工单02', '工单03', '工单04', '工单05', '工单06'],
         'labels': {'columns': ['待处理', '进行中', '待复核', '已完成'],
                    'countCaption': '演示进度单位', 'footer': '预设计数独立于卡片位置，未接入真实工单'},
         'data': {'countStart': 0, 'countMax': 24, 'countRate': 24, 'countPeriod': 12}},
    ]
    return {'id': 'component-lab', 'title': '矢量组件实验室', 'category': '组件与角色',
            'summary': '六种真实可复用 SVG 组件，用四套深浅配色展示各自的动画与用途。',
            'capabilities': ['orb', 'seats', 'donut', 'ribbons', 'ghostSeats', 'kanban', '统一缩放'],
            'learn': ['组件保留真实几何和动画，可通过 JSON 组合与复用。',
                      '标签、示例数值和显现时间都可以配置。',
                      '流带宽度是示意；看板计数独立于卡片位置，不是实时统计。'],
            'checkpoints': [{'time': 1.5, 'label': '角色与初始比例'}, {'time': 4.5, 'label': '候选对象显现'},
                            {'time': 7.5, 'label': '节点汇聚与任务推进'}, {'time': 10.5, 'label': '后段计数与流带'}],
            'focusViews': [{'label': '发光角色', 'x': 190, 'y': 323, 'zoom': 2.5},
                           {'label': '节点汇聚', 'x': 492, 'y': 584, 'zoom': 1.8},
                           {'label': '比例环', 'x': 255, 'y': 839, 'zoom': 2.1},
                           {'label': '虚实对比', 'x': 729, 'y': 839, 'zoom': 2.1},
                           {'label': '分支流带', 'x': 255, 'y': 1090, 'zoom': 2.1},
                           {'label': '任务看板', 'x': 729, 'y': 1090, 'zoom': 2.1}],
            'themeSwitch': False, 'visualStyle': 'editorial', 'beforePage': 'live-before.html',
            'config': cfg}


def avatar_themes():
    cfg = _base('角色导航与主题 · 同一时间线上的游走讲解')
    cfg['machines'] = {'guide': {'type': 'cycle', 'period': 4,
                                'values': ['检索依据', '核对上下文', '解释结果']}}
    cfg['elements'] = [
        {'type': 'avatarEditorial', 'x': 0, 'y': 0, 'w': 984, 'h': 1280},
        {'type': 'drone', 'avatar': 'spider', 'avatarScale': 1.05, 'gaitSpeed': 8.4, 'timelineMachine': 'guide',
         'avatarColors': {'leg': '#d68865', 'joint': '#88c4a2', 'shell': '#9d9acc', 'core': '#dfb96d'},
         'x': 0, 'y': 0, 'w': 984, 'h': 1280, 'period': 12, 'focusPeriod': 4,
         'path': [[178, 352], [492, 352], [807, 352]],
         'targets': [{'x': x-80, 'y': 270, 'w': 160, 'h': 164} for x in (178, 492, 807)],
         'words': [{'x': 139, 'y': 456, 'w': 83, 't': '找到依据'},
                   {'x': 453, 'y': 456, 'w': 83, 't': '检查语境'},
                   {'x': 768, 'y': 456, 'w': 83, 't': '解释结果'}]},
    ]
    return {'id': 'avatar-themes', 'title': '角色导航与主题', 'category': '组件与角色',
            'summary': '八足蜘蛛游走、热区脉冲、目标聚焦与时间线；支持角色切换和深浅主题。',
            'capabilities': ['spider / drone', '路径移动', '目标框', '虚线指向', '关键词闪烁',
                             '配色 / 大小 / 步频', '深浅主题', '确定性回放'],
            'learn': ['角色与聚焦框一起引导读者关注当前步骤。',
                      '切换角色不会改变时间线；角色样式和主题分别配置。',
                      '浅色页读取主题颜色，不依赖固定的深色 SVG 背景。'],
            'checkpoints': [{'time': 1.5, 'label': '聚焦检索依据'}, {'time': 5.5, 'label': '聚焦核对上下文'},
                            {'time': 9.5, 'label': '聚焦解释结果'}],
            'focusViews': [{'label': '游走角色', 'x': 492, 'y': 355, 'zoom': 2},
                           {'label': '外观细节', 'x': 255, 'y': 714, 'zoom': 2},
                           {'label': '导览状态', 'x': 729, 'y': 714, 'zoom': 2},
                           {'label': '回放时间线', 'x': 492, 'y': 1040, 'zoom': 1.8}],
            'themeSwitch': True, 'visualStyle': 'editorial', 'beforePage': 'live-before.html',
            'config': cfg}


def scenes():
    return [component_lab(), avatar_themes()]
