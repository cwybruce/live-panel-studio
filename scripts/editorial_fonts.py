"""Embed bundled, renamed OFL font subsets in portable HTML pages."""
import base64
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent / 'assets/fonts'


def font_style():
    rules = []
    for family, file, weight in [('LP Sans', 'lp-sans.woff', '100 900'),
                                  ('LP Serif', 'lp-serif.woff', '100 900'),
                                  ('LP Mono', 'lp-mono.woff', '400')]:
        blob = base64.b64encode((FONTS / file).read_bytes()).decode('ascii')
        rules.append(f'@font-face{{font-family:"{family}";src:url(data:font/woff;base64,{blob}) format("woff");font-weight:{weight};font-style:normal;font-display:block}}')
    license_notes = '\n'.join((FONTS / name).read_text(encoding='utf-8') for name in
                             ['noto-sans-OFL.txt', 'noto-serif-OFL.txt', 'plex-mono-OFL.txt'])
    return '<!-- Embedded font subsets: Noto Sans SC / Noto Serif SC / IBM Plex Mono.\n' + license_notes + '\n-->\n<style id="editorial-fonts">' + '\n'.join(rules) + '</style>'
