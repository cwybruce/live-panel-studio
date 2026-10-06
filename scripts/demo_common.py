"""Small authoring helpers for the original, simulated capability examples."""

WIDTH, HEIGHT = 960, 640
FONT = '"Microsoft YaHei","Noto Sans CJK SC",Consolas,sans-serif'
PALETTES = {
    'terminal-dark': {'bg': '#111822', 'bar': '#192331', 'panel': '#192331',
                      'line': '#415269', 'line2': '#415269', 'dim': '#9aacc2',
                      'fg': '#e8eff8', 'wh': '#ffffff', 'cy': '#67d8dd',
                      'bl': '#8ab4ff', 'gr': '#8ce2b2', 'pu': '#c4a3ff',
                      'ye': '#ffcf86', 'rd': '#ff8f96', 'hl': '#26384b',
                      'dots': '#3c5068', 'none': 'transparent'},
    'light-pastel': {'bg': '#f4f7fb', 'bar': '#e8edf5', 'panel': '#ffffff',
                     'line': '#8596ae', 'line2': '#c1cbd9', 'dim': '#53657c',
                     'fg': '#243349', 'wh': '#ffffff', 'cy': '#147d86',
                     'bl': '#366ab3', 'gr': '#218653', 'pu': '#7955b4',
                     'ye': '#926314', 'rd': '#c74956', 'hl': '#e7edf7',
                     'dots': '#ccd7e5', 'none': 'transparent'},
}


def text(x, y, t, size=16, c='fg', w=None, align='left', b=False):
    e = {'type': 'text', 'x': x, 'y': y, 't': t, 'size': size,
         'c': c, 'align': align, 'font': FONT, 'b': b}
    if w is not None:
        e['w'] = w
    return e


def box(x, y, w, h, title, lines=None, c='cy', when=None, then=None):
    e = {'type': 'box', 'x': x, 'y': y, 'w': w, 'h': h, 'color': c,
         'fill': 'panel', 'radius': 12, 'sides': 'solid', 'pad': [15, 18, 18],
         'align': 'left', 'lines': [{'t': title, 'b': True, 'c': c, 'size': 18}] + (lines or [])}
    if when:
        e.update(when=when, then=then or {'glow': c, 'border': 2})
    return e


def path(points, c='cy', period=2, when=None, then=None):
    e = {'type': 'path', 'points': points, 'color': c, 'width': 2, 'r': 10,
         'flow': {'period': period, 'offsets': [0, period / 2], 'tail': 12}}
    if when:
        e['when'] = when
        e['then'] = then or {'color': c, 'width': 3}
        e['flow']['when'] = when
    return e


def actor(path, targets=None, scale=.45):
    return {'type': 'drone', 'avatar': 'spider', 'x': 0, 'y': 0,
            'w': WIDTH, 'h': HEIGHT, 'period': 12, 'focusPeriod': 3,
            'avatarScale': scale, 'path': path, 'targets': targets or [], 'words': []}


def footnote():
    return text(36, 613, '原创能力示例 · 预设时间线与模拟数据 · 可 seek 回放 / 网页播放 / MP4 导出', 12, 'dim')


def base(title, subtitle, preset='terminal-dark', duration=12):
    return {'meta': {'title': title, 'lang': 'zh-CN'},
            'canvas': {'width': WIDTH, 'height': HEIGHT, 'duration': duration, 'fps': 30},
            'theme': {'preset': preset, 'font': FONT, 'fontSize': 15, 'lineHeight': 26,
                      'boxMode': 'solid', 'radius': 12, 'glow': True,
                      'colors': dict(PALETTES[preset])},
            'clock': {'start': '00:00:00', 'rate': 1}, 'machines': {},
            'elements': [text(36, 40, 'MOTION DIAGRAM STUDIO / CAPABILITY DEMO', 12, 'cy'),
                         text(36, 80, title, 30, 'fg', b=True),
                         text(36, 117, subtitle, 14, 'dim'), footnote()]}
