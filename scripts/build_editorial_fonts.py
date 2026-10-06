"""Subset OFL fonts for the editorial demos; rendering needs only bundled WOFFs.

Rebuilding requires fonttools. Noto source paths may be supplied on any platform.
No network requests are made by this script.
"""
import argparse
import hashlib
import json
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/fonts'


def corpus():
    paths = list((ROOT / 'assets').glob('*.js')) + list((ROOT / 'assets').glob('*.html'))
    paths += list((ROOT / 'scripts').glob('*editorial*.py'))
    paths += [ROOT / 'scripts/demo_export_views.py']
    paths += list((ROOT / 'examples/capability-demos').glob('*/config.json'))
    chars = set(range(32, 127))
    for path in paths:
        chars.update(ord(c) for c in path.read_text(encoding='utf-8') if ord(c) >= 32)
    return chars


def build(source, filename, family, wanted, license_file, source_url):
    font = TTFont(source)
    original_names = {str(n): font['name'].getDebugName(n) for n in (0, 1, 5, 13, 14)}
    available = set(font.getBestCmap())
    options = subset.Options()
    options.name_IDs = ['*']
    options.name_languages = ['*']
    options.name_legacy = True
    sub = subset.Subsetter(options=options)
    sub.populate(unicodes=wanted & available)
    sub.subset(font)
    # Subsets are derivative fonts; retain copyright/license but rename families.
    for record in font['name'].names:
        if record.nameID in (1, 4, 16, 21):
            record.string = family.encode(record.getEncoding())
        elif record.nameID in (3, 6):
            record.string = family.replace(' ', '').encode(record.getEncoding())
    font.flavor = 'woff'
    destination = OUT / filename
    font.save(destination)
    return {'file': filename, 'family': family, 'original': original_names,
            'sourceUrl': source_url, 'license': license_file,
            'sourceSha256': hashlib.sha256(Path(source).read_bytes()).hexdigest(),
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
            'bytes': destination.stat().st_size,
            'unicodeCount': len(font.getBestCmap()),
            'missingChinese': [chr(c) for c in sorted(wanted - available) if 0x4e00 <= c <= 0x9fff]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sans', type=Path, default=Path('C:/Windows/Fonts/NotoSansSC-VF.ttf'))
    ap.add_argument('--serif', type=Path, default=Path('C:/Windows/Fonts/NotoSerifSC-VF.ttf'))
    ap.add_argument('--mono', type=Path, default=OUT / 'plex-mono-source.ttf')
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    chars = corpus()
    records = [build(args.sans, 'lp-sans.woff', 'LP Sans', chars, 'noto-sans-OFL.txt',
                     'https://github.com/notofonts/noto-cjk'),
               build(args.serif, 'lp-serif.woff', 'LP Serif', chars, 'noto-serif-OFL.txt',
                     'https://github.com/notofonts/noto-cjk'),
               build(args.mono, 'lp-mono.woff', 'LP Mono', set(range(32, 127)), 'plex-mono-OFL.txt',
                     'https://github.com/google/fonts/tree/main/ofl/ibmplexmono')]
    (OUT / 'manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('\n'.join(f"{r['family']}: {r['bytes']} bytes, {r['unicodeCount']} glyphs" for r in records))


if __name__ == '__main__':
    main()
