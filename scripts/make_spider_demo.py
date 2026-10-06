"""Create a close-up motion study of the selectable mechanical spider avatar."""
import json
import math
from pathlib import Path
import livepanel as lp


def main():
    out = lp.ROOT / 'examples/spider-avatar'
    out.mkdir(parents=True, exist_ok=True)
    plate = '''<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="#424953" opacity=".35"/></pattern></defs>
    <rect width="880" height="620" fill="#11151c"/>
    <rect x="24" y="24" width="832" height="572" rx="14" fill="url(#grid)" stroke="#333c4e"/>
    <g font-family="Consolas,Microsoft YaHei,monospace">
    <text x="52" y="59" fill="#8cb7ff" font-size="11" letter-spacing="3">SPIDER AVATAR / MOTION STUDY 01</text>
    <text x="52" y="105" fill="#e6eaff" font-size="30" font-weight="bold">机械蜘蛛 · 八足步态</text>
    <text x="52" y="132" fill="#8e99ac" font-size="13">红色分节腿  /  绿色发光关节  /  蓝紫机械甲壳  /  粉色能量核心</text>
    <path d="M58 166H822" stroke="#30394b"/>
    <g fill="none" stroke="#40516c" stroke-width="1" stroke-dasharray="3 5">
    <path d="M81 229H202L321 269"/><path d="M688 247H636L493 321"/>
    <path d="M93 427H217L309 406"/><path d="M701 430H661L566 385"/>
    </g>
    <text x="66" y="214" fill="#ff7c75" font-size="13">4 对、8 条分节腿</text>
    <text x="688" y="232" fill="#9cbfff" font-size="13">双段机械躯干</text>
    <text x="66" y="454" fill="#7aeeb0" font-size="13">膝部与脚端发光</text>
    <text x="665" y="458" fill="#ffa7d5" font-size="13">交替抬脚、回摆</text>
    <path d="M58 520H822" stroke="#30394b"/>
    <text x="52" y="552" fill="#8997ad" font-size="12">avatar: spider     |     avatarScale: 2.4     |     deterministic seek(t)</text>
    <text x="52" y="577" fill="#647186" font-size="11">原创矢量角色组件 · 可切换回机器人 · 颜色、大小与步频可配置</text>
    </g>'''
    cfg = {
        'meta': {'title': '机械蜘蛛 · 八足步态近景', 'lang': 'zh-CN'},
        'canvas': {'width': 880, 'height': 620, 'duration': 8, 'fps': 60},
        'theme': {'preset': 'terminal-dark', 'colors': {'bg': '#11151c'}},
        'machines': {},
        'elements': [
            {'type': 'vector', 'x': 0, 'y': 0, 'w': 880, 'h': 620, 'markup': plate},
            {'type': 'drone', 'avatar': 'spider', 'avatarScale': 2.4, 'avatarHeading': 0,
             'x': 0, 'y': 0, 'w': 880, 'h': 620, 'period': 8, 'gaitSpeed': math.tau,
             'path': [[440,345],[450,345],[440,355],[430,345]], 'targets': [], 'words': []}
        ]
    }
    path = out / 'config.json'
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
    lp.build_page(path, out / 'live.html')
    # The existing local viewer serves only the business example directory.
    # Copy the self-contained close-up so it can share that preview entry.
    local_viewer = lp.ROOT / 'examples/business-infographic'
    if local_viewer.is_dir():
        (local_viewer / 'spider-closeup.html').write_bytes((out / 'live.html').read_bytes())
    print(path)


if __name__ == '__main__':
    main()
