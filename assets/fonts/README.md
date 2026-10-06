# Editorial demo fonts

The portable editorial HTML pages embed three renamed WOFF subsets:

| Family | Original font | Use | License |
| --- | --- | --- | --- |
| LP Serif | Noto Serif SC | Chinese titles and section headings | SIL OFL 1.1 |
| LP Sans | Noto Sans SC | Chinese body and labels | SIL OFL 1.1 |
| LP Mono | IBM Plex Mono Regular | Latin metadata and tabular numbers | SIL OFL 1.1 |

The subset families have new names because subsetting modifies the fonts.
Each binary retains original copyright and license metadata. The original
license texts are included here and embedded in the generated HTML comments.
These fonts remain under OFL rather than the repository's code MIT license.

Sources: [Noto CJK](https://github.com/notofonts/noto-cjk),
[IBM Plex Mono on Google Fonts](https://github.com/google/fonts/tree/main/ofl/ibmplexmono).
`manifest.json` records original metadata, source and subset SHA-256 hashes,
glyph coverage and file sizes. Noto source font versions are recorded in it.

Rendering and playback need no font installation, CDN or network access.
Only rebuilding the subsets requires `fonttools` and the original Noto source
files. The bundled IBM source font is also covered by `plex-mono-OFL.txt`.

```powershell
python -m pip install -r requirements-fonts.txt
python scripts/build_editorial_fonts.py --sans PATH_TO_NotoSansSC-VF.ttf --serif PATH_TO_NotoSerifSC-VF.ttf
python scripts/make_capability_demos.py --render --jobs 2
```

On this Windows workstation the script defaults to the installed Noto source
files in `C:/Windows/Fonts`. New text outside the subset falls back to installed
fonts; rebuild after adding Chinese text for consistent portable typography.
The live gallery and every editorial scene embed their own complete subsets.
