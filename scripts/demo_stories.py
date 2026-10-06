"""Original knowledge-card and business-workflow example configurations."""
from demo_common import base, text, box, path, actor


def stories():
    cfg = base('把一个知识点，做成动态讲解卡', '短视频内容示例：看输入、理解处理、核对输出；12 秒循环。')
    cfg['machines'] = {
        'chapter': {'type': 'cycle', 'period': 3, 'values': [
            {'t': '01 / 明确输入', 'note': '先说明问题与已有材料。'},
            {'t': '02 / 展示过程', 'note': '让信息沿连线经过处理节点。'},
            {'t': '03 / 检查输出', 'note': '结果应当有依据，并且可以核对。'},
            {'t': '04 / 回顾要点', 'note': '看清输入、过程、输出，再迁移到自己的场景。'}]},
        'views': {'type': 'counter', 'start': 120, 'rate': 8, 'suffix': ' 次演示播放'},
    }
    cfg['elements'] += [
        text(36, 165, '{chapter}', 20, 'cy', b=True),
        {'type': 'rule', 'x': 36, 'y': 193, 'w': 888},
        path([[290, 316], [354, 316]], 'cy', 1.6),
        path([[606, 316], [670, 316]], 'pu', 1.6),
    ]
    specs = [(36, '输入', '一个问题', '一组可核对的材料', 'cy'),
             (354, '过程', '解释关键步骤', '展示信息如何流动', 'bl'),
             (672, '输出', '有依据的结果', '知道怎样检查它', 'gr')]
    for i, (x, title, a, b, color) in enumerate(specs):
        cfg['elements'].append(box(x, 243, 252, 146, title,
            [{'t': a, 'size': 17}, {'t': b, 'size': 15, 'c': 'dim'}], color,
            {'var': 'chapter.i', 'in': [i, 3]}))
    cfg['elements'] += [
        {'type': 'glyph', 'x': 320, 'y': 281, 'ch': '→', 'c': 'cy', 'size': 22},
        box(36, 434, 888, 103, '当前讲解', [{'t': '{chapter.note}', 'size': 17}], 'pu'),
        text(36, 569, '{views}', 13, 'dim'),
        text(570, 569, '可导出 MP4，也可以保留可交互网页', 13, 'dim'),
        actor([[152, 211], [480, 211], [795, 211], [480, 406]],
              [{'x': 36, 'y': 243, 'w': 252, 'h': 146},
               {'x': 354, 'y': 243, 'w': 252, 'h': 146},
               {'x': 672, 'y': 243, 'w': 252, 'h': 146}], .33),
    ]
    knowledge = {'id': 'knowledge-card', 'title': '短视频知识卡', 'category': '内容创作',
                 'summary': '把输入、过程、输出做成 12 秒动态讲解。',
                 'capabilities': ['文字与节点', '章节轮播', '连线光点', '角色引导', 'MP4 导出'],
                 'learn': ['用 cycle 定义 4 个章节；节点通过 when / then 点亮。',
                           '演示播放次数使用预设计数器，未接入内容平台数据。'],
                 'checkpoints': [{'time': .8, 'label': '明确输入'}, {'time': 3.8, 'label': '展示过程'},
                                 {'time': 6.8, 'label': '检查输出'}, {'time': 9.8, 'label': '回顾要点'}],
                 'config': cfg}

    cfg = base('客服工单：从受理到完成', '业务培训示例：工单卡片沿四列移动；数字是模拟演示，不是运营统计。')
    cfg['machines'] = {
        'policy': {'type': 'cycle', 'period': 4, 'values': [
            {'t': '受理：先确认用户问题', 'detail': '补齐订单编号，确认工单属于哪一类。'},
            {'t': '处理：给出可执行方案', 'detail': '核对资料，处理问题，并记录处理依据。'},
            {'t': '复核：确认问题已解决', 'detail': '复核处理结果，再将工单归档。'}]},
        'received': {'type': 'counter', 'start': 24, 'rate': 2},
        'review': {'type': 'lane', 'period': 6, 'run': 4, 'off': 0,
                   'busy': '复核处理中', 'done': ['复核通过'], 'busyColor': 'ye'},
    }
    cfg['elements'] += [
        box(36, 158, 426, 80, '当前培训提示', [{'t': '{policy}', 'size': 15}], 'cy'),
        box(482, 158, 210, 80, '收到工单', [{'t': '{received} 单（模拟）', 'size': 15}], 'bl'),
        box(712, 158, 212, 80, '复核状态', [{'runs': [{'v': 'review'}], 'size': 15}], 'ye'),
        {'type': 'kanban', 'x': 36, 'y': 266, 'w': 888, 'h': 238, 'period': 12,
         'tickets': ['工单01 退款', '工单02 登录', '工单03 配送', '工单04 发票', '工单05 地址', '工单06 订阅'],
         'labels': {'columns': ['待受理', '处理中', '待复核', '已完成'],
                    'countCaption': '已完成工单 · 模拟计数', 'footer': '卡片停留、转交、归档，用于解释处理流程'},
         'data': {'countStart': 6, 'countMax': 30, 'countRate': 24, 'countPeriod': 12}},
        box(36, 517, 888, 72, '处理原则', [{'t': '{policy.detail}', 'size': 14}], 'gr'),
    ]
    workflow = {'id': 'business-workflow', 'title': '业务工单流转', 'category': '业务培训',
                'summary': '工单在受理、处理、复核、完成之间移动。',
                'capabilities': ['看板卡片动画', '模拟计数器', '状态条', '轮播培训提示'],
                'learn': ['kanban 展示卡片在四列之间停留、移动和完成。',
                          'lane 模拟复核忙碌与完成；提示和卡片各自循环。'],
                'themeSwitch': False,
                'checkpoints': [{'time': 1, 'label': '受理提示'}, {'time': 5, 'label': '处理提示'},
                                {'time': 9, 'label': '复核提示'}], 'config': cfg}
    return [knowledge, workflow]
