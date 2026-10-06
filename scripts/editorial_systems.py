"""Portrait editorial versions of three existing simulated system scenes."""

from demo_scenes import agent_team, incident_replay, product_request


FONT = '"LP Sans", "Microsoft YaHei", sans-serif'
PALETTE = {'bg': '#12110f', 'fg': '#eee9df', 'dim': '#9f9587',
           'line': '#3c352c', 'cy': '#64bed0', 'bl': '#64bed0',
           'pu': '#e776af', 'gr': '#88c4a2', 'ye': '#dfb96d',
           'rd': '#d77768', 'wh': '#eee9df', 'panel': '#191713',
           'hl': '#29241c', 'bar': '#191713', 'dots': '#52483c',
           'line2': '#3c352c'}


def _portrait(factory, component, title, summary, path, targets, labels):
    out = factory()
    cfg = out['config']
    cfg['meta']['title'] = title
    cfg['canvas'] = {'width': 984, 'height': 1280, 'duration': 12, 'fps': 30}
    cfg['theme'] = {'preset': 'terminal-dark', 'font': FONT,
                    'fontSize': 13, 'lineHeight': 19,
                    'colors': dict(PALETTE)}
    cfg['elements'] = [
        {'type': component, 'x': 0, 'y': 0, 'w': 984, 'h': 1280},
        {'type': 'drone', 'avatar': 'spider', 'avatarScale': .48,
         'avatarColors': {'leg': '#d68865', 'joint': '#88c4a2',
                          'shell': '#9d9acc', 'core': '#e776af'},
         'x': 0, 'y': 0, 'w': 984, 'h': 1280,
         'period': 12, 'focusPeriod': 12 / len(targets),
         'path': path, 'targets': targets, 'words': []},
    ]
    out.update(summary=summary, visualStyle='editorial',
               beforePage='live-before.html', themeSwitch=False)
    out['capabilities'] += labels
    return out


def scenes():
    agents = _portrait(
        agent_team, 'agentEditorial', '协作 · 一次任务，四种角色',
        '四角色交接、任务树、时间泳道与验收包，展示建议、状态与事件的同步回放。',
        [[145, 487], [376, 487], [607, 487], [838, 487]],
        [{'x': x - 57, 'y': 282, 'w': 114, 'h': 114} for x in [145, 376, 607, 838]],
        ['任务树', '时间泳道', '交接包', 'LP 字体', '竖屏图形叙事'])
    request = _portrait(
        product_request, 'requestEditorial', '请求 · 走捷径，或回到源头',
        '缓存键值阵列、双路合流与独立模拟计数，共同解释命中、未命中和返回。',
        [[165, 508], [838, 508], [342, 508]],
        [{'x': 541, 'y': 254, 'w': 91, 'h': 90},
         {'x': 791, 'y': 313, 'w': 96, 'h': 91},
         {'x': 541, 'y': 378, 'w': 91, 'h': 88}],
        ['缓存键值阵列', '两路合流', '模拟计数轨迹', 'LP 字体', '竖屏图形叙事'])
    incident = _portrait(
        incident_replay, 'incidentEditorial', '回放 · 让异常沿依赖显形',
        '依赖节点、余量曲线、阈值圆环与恢复检查，明确区分服务恢复和业务验收。',
        [[176, 487], [492, 487], [808, 487]],
        [{'x': x - 58, 'y': 281, 'w': 116, 'h': 116} for x in [176, 492, 808]],
        ['余量曲线', '阈值圆环', '恢复检查', 'LP 字体', '竖屏图形叙事'])
    return [agents, request, incident]
