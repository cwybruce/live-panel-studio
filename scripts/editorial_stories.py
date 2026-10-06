"""Portrait story scenes in the original warm-black editorial visual system."""


def _base(title,kind,machines,path,targets):
    return {
        'meta': {'title': title, 'lang': 'zh-CN'},
        'canvas': {'width': 984, 'height': 1280, 'duration': 12, 'fps': 30},
        'theme': {'preset': 'terminal-dark', 'colors': {'bg': '#12110f'}},
        'machines': machines,
        'elements': [
            {'type': kind, 'x': 0, 'y': 0, 'w': 984, 'h': 1280},
            {'type': 'drone', 'avatar': 'spider', 'avatarScale': .48,
             'avatarColors': {'leg': '#d68865', 'joint': '#88c4a2',
                              'shell': '#9d9acc', 'core': '#e776af'},
             'x': 0, 'y': 0, 'w': 984, 'h': 1280,
             'period': 12, 'focusPeriod': 3, 'path': path,
             'targets': targets, 'words': []},
        ],
    }


def stories():
    knowledge = {
        'id': 'knowledge-card', 'title': '短视频知识卡', 'category': '内容创作',
        'summary': '展开书页，把输入、过程、输出与回顾做成有图形关系的四章讲解。',
        'capabilities': ['展开书页', '章节轮播', '信息流向', '出处核对',
                         '回顾图谱', '蜘蛛导览', 'MP4 导出'],
        'learn': ['先说明问题和已有材料，再展示处理关系，最后核对输出。',
                  '四章讲解每 3 秒推进一次；计数器展示模拟播放次数。',
                  '动画、光点、引用与强调状态都可以暂停、跳转和确定性回放。'],
        'checkpoints': [{'time': .8, 'label': '明确输入'},
                        {'time': 3.8, 'label': '展示过程'},
                        {'time': 6.8, 'label': '检查输出'},
                        {'time': 9.8, 'label': '回顾要点'}],
        'width': 984, 'height': 1280, 'themeSwitch': False,
        'visualStyle': 'editorial', 'beforePage': 'live-before.html',
    }
    knowledge['config'] = _base(
        '知识卡 · 把一个知识点翻成看得懂的页', 'knowledgeEditorial',
        {'chapter': {'type': 'cycle', 'period': 3, 'values': [
            {'t': '01 / 明确输入', 'note': '先说明问题与已有材料。'},
            {'t': '02 / 展示过程', 'note': '让信息沿连线经过处理节点。'},
            {'t': '03 / 检查输出', 'note': '结果应当有依据，并且可以核对。'},
            {'t': '04 / 回顾要点', 'note': '看清输入、过程、输出，再迁移到自己的场景。'}]},
         'views': {'type': 'counter', 'start': 120, 'rate': 8, 'suffix': ' 次演示播放'}},
        [[309, 481], [414, 481], [569, 481], [675, 481]],
        [{'x': 531+i*78, 'y': 387, 'w': 43, 'h': 43} for i in range(3)]
        + [{'x': 238, 'y': 285, 'w': 508, 'h': 204}],
    )

    knowledge['config']['elements'][1]['timelineMachine'] = 'chapter'

    workflow = {
        'id': 'business-workflow', 'title': '业务工单流转', 'category': '业务培训',
        'summary': '六张工单在四站看板流转，配合分配拓扑、完成环、复核轨迹与补充资料的重试支路。',
        'capabilities': ['旅行工单', '四站看板', '问题分流', '完成比例',
                         '复核状态', '重试支路', '模拟计数器'],
        'learn': ['工单依次经历受理、处理、复核、完成；转交应当附带处理依据。',
                  '6 秒复核周期包含 4 秒处理与 2 秒完成状态。',
                  '5–9 秒演示资料缺失与返回补充，随后重新进入复核。'],
        'checkpoints': [{'time': 1, 'label': '受理与分流'},
                        {'time': 5, 'label': '处理与复核'},
                        {'time': 7, 'label': '补齐资料'},
                        {'time': 10, 'label': '重新复核'}],
        'width': 984, 'height': 1280, 'themeSwitch': False,
        'visualStyle': 'editorial', 'beforePage': 'live-before.html',
    }
    workflow['config'] = _base(
        '工单 · 一张工单走过四个处理站', 'workflowEditorial',
        {'policy': {'type': 'cycle', 'period': 4, 'values': [
            {'t': '受理：先确认用户问题', 'detail': '补齐订单编号，确认工单属于哪一类。'},
            {'t': '处理：给出可执行方案', 'detail': '核对资料，处理问题，并记录处理依据。'},
            {'t': '复核：确认问题已解决', 'detail': '复核处理结果，再将工单归档。'}]},
         'received': {'type': 'counter', 'start': 24, 'rate': 2},
         'review': {'type': 'lane', 'period': 6, 'run': 4, 'off': 0,
                    'busy': '复核处理中', 'done': ['复核通过'], 'busyColor': 'ye'}},
        [[143, 558], [373, 558], [603, 558], [833, 558]],
        [{'x': x, 'y': 280, 'w': 195, 'h': 265} for x in [49, 279, 509, 739]],
    )
    return [knowledge, workflow]
