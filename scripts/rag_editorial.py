"""Original editorial RAG composition, based on the reference's visual grammar."""


def scene():
    cfg = {
        'meta': {'title': 'RAG · 一个问题如何找到它的依据', 'lang': 'zh-CN'},
        'canvas': {'width': 984, 'height': 1280, 'duration': 12, 'fps': 30},
        'theme': {'preset': 'terminal-dark', 'colors': {'bg': '#12110f'}},
        'machines': {'rag': {'type': 'cycle', 'period': 3,
                            'values': ['明确问题', '检索候选', '筛选证据', '带引用回答']}},
        'elements': [
            {'type': 'ragEditorial', 'x': 0, 'y': 0, 'w': 984, 'h': 1280},
            {'type': 'drone', 'avatar': 'spider', 'avatarScale': .48, 'timelineMachine': 'rag',
             'avatarColors': {'leg': '#d68865', 'joint': '#88c4a2', 'shell': '#9d9acc', 'core': '#e776af'},
             'x': 0, 'y': 0, 'w': 984, 'h': 1280, 'period': 12, 'focusPeriod': 3,
             'path': [[145, 478], [376, 478], [607, 478], [838, 478]],
             'targets': [{'x': x-60, 'y': 283, 'w': 120, 'h': 113} for x in [145, 376, 607, 838]],
             'words': []},
        ],
    }
    return {'id': 'rag-explainer', 'title': 'RAG 证据讲解', 'category': 'AI 技术教学',
            'summary': '全幅流程、候选文档、评分筛选、引用与拒答；蜘蛛沿时间线引导当前步骤。',
            'capabilities': ['图形叙事', '路径光点', '文档阵列', '评分条', '引用流向', '蜘蛛导览', '确定性回放'],
            'learn': ['先检索候选，再筛选和核对依据；不能只看相关性分数。',
                      '引用应当定位到原文；缺少依据时明确说明。',
                      '细边界、局部光效和分区微图，支持暖黑、暖纸、经典终端与经典粉彩四套配色。'],
            'checkpoints': [{'time': 1.5, 'label': '明确问题'}, {'time': 4.5, 'label': '检索片段'},
                            {'time': 7.5, 'label': '重排证据'}, {'time': 10.5, 'label': '依据生成'}],
            'themeSwitch': False, 'visualStyle': 'editorial', 'beforePage': 'live-before.html',
            'config': cfg}
