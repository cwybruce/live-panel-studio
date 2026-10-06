# Config schema

One JSON object. All coordinates are canvas pixels (default 1200x1500, y grows downward). Colour names refer to `theme.colors`. Generic terminal text is monospace: Latin glyphs are 0.6 em wide and CJK glyphs two cells. Authored editorial scenes also use the bundled LP Serif and LP Sans fonts; terminal presentation applies monospace text to the supported scene components.

## Top level

| key | meaning |
| --- | --- |
| `meta` | `{title, lang}` page title and language |
| `canvas` | `{preset:"4:5"|"3:4"|"1:1", width, height, duration, fps, preroll}` (explicit width/height win over the preset); `preroll` (s) is added to packet phases so delivery counters start above zero |
| `theme` | `{preset:"terminal-dark"|"light-pastel", font, fontSize, lineHeight, boxMode:"segmented"|"solid", radius, borderWidth, wireWidth, packetSize, glow, colors:{name:"#rrggbb"}}`. A preset supplies every field; your values override it, `colors` are merged name by name. Colour names used by the engine: `bg bar line dim fg wh` (+ `line2` log frame, `dots` bar track); add any others |
| `clock` | `{start:"HH:MM:SS", rate}`: log time at t=0 and how many log-seconds pass per second |
| `titlebar` | `{text, height?, size?}` terminal title bar with three dots |
| `credit` | text element for the source/credit line: `{text, y, size?, c?}` (default 12 px, centred, dim) |
| `machines` | named state machines, see below |
| `elements` | drawn in order (later = on top) |
| `presentation` | optional `{style:"diagram"|"terminal", sceneId?, title?, command?, events:[{t,actor,text}]}` for the eight authored editorial scenes; omitted means Diagram, see below |
| `effects` | optional `{neon:{enabled, intensity, period, heroPeriod, tail}}`; flowing light on authored editorial function-block borders, see below |

## Presentation styles

Presentation and palette are independent. The eight authored editorial scenes
support `diagram` (the original composition, default) and `terminal` (a complete
macOS-style terminal window). Each supports all four `theme.variant` values. The
terminal style is a visual presentation and does not require macOS; its title bar,
ASCII block borders, command prompt and log rows are rendered into the same
self-contained HTML and exported video. The underlying scene geometry and named
block-crop coordinates are preserved.

```json
"presentation": {
  "style": "terminal",
  "sceneId": "rag-explainer",
  "title": "~/motion-diagram-studio/rag-explainer — zsh",
  "command": "python scripts/render.py --config examples/capability-demos/rag-explainer/config-console-terminal.json",
  "events": [
    {"t": 0, "actor": "studio", "text": "演示启动 · 预设模拟"},
    {"t": 3, "actor": "rag", "text": "演示关键点：重排证据"}
  ]
}
```

`events` are authored simulated messages, not an operating-system terminal or a
live process log. `t` is seconds on the scene timeline; only finite event times
from 0 up to (but excluding) `canvas.duration` are displayed. Rows are sorted by
`t` and the two latest visible messages are shown. Command typing, spinners,
logs and cursor blinking are pure functions of `seek(t)`, following replay,
scrubbing and frame-by-frame export. The generator derives events from the demo's
preauthored checkpoints and adds an explicit simulation label.

The manifest records files in
`styleVariants[style].themeVariants[theme]` (`config`, `page`, `video`, `poster`,
`videoReady`). Its legacy `themeVariants` remains the Diagram mapping. Terminal
files use the independent names `config-console-{dark|light|terminal|pastel}.json`,
`live-console-*.html`, `demo-console-*.mp4` and `poster-console-*.png`.

Use `?style=terminal&theme=terminal-classic#rag-explainer` in the gallery URL, or
`?style=terminal&theme=terminal-classic` on the homepage. The homepage stores
independent browser preferences, with URL values taking precedence. The gallery
keeps both choices in its URL. First visits default to Diagram. Existing theme
IDs and original filenames remain valid.

```bash
# Terminal presentation, all four palettes (32 complete videos)
python scripts/make_capability_demos.py --render --styles terminal --themes all --jobs 2
# Both presentations, all four palettes (64 complete videos)
python scripts/make_capability_demos.py --render --styles both --themes all --jobs 2
# A single full terminal export
python scripts/export_demo.py --scene rag-explainer --style terminal --theme terminal-classic --avatar spider --view full --out rag-console.mp4
```

`--styles diagram` and `--style diagram` are the defaults. The existing
`--themes both` selects the original Warm Ink / Warm Paper palette pair;
`--styles both` selects two presentations. A named block export retains its
original content crop and glow margin, without the outer terminal window shell;
`--view full` includes the complete terminal presentation. Retained reference and
pre-rendered block videos keep their original styles.

## Flowing neon borders

All eight editorial demos offer four palette variants: `terminal-dark` (warm
black), `light-pastel` (warm paper), `terminal-classic` (the upstream cool terminal
colors), and `pastel-classic` (the upstream white and colorful pastel scheme).
For editorial configs, `theme.variant` selects the semantic palette; `theme.preset`
remains `terminal-dark` or `light-pastel` for the base renderer. The generator
writes explicit `theme.colors` for every variant. `theme.colors` overrides are
still applied by name. This adds color choices without changing layout or fonts.
The palette applies to panels, text, graph surfaces, gradients,
actors and reusable component colors. The gallery theme selector also changes
the surrounding controls without resetting playback time, pause or actor choice.
The manifest's `styleVariants` maps presentation styles to these palette variants;
the legacy `themeVariants` contains the original Diagram files. Existing
warm-theme filenames and CLI IDs remain valid.

Use the local `scripts/preview_server.py` to export the current scheme. The
gallery's `exportViews` manifest lists named, whitelisted block crops; `full`
exports the entire Demo. Blocks retain a 12px glow margin, even dimensions and
the entire 12-second timeline. Style, theme and actor are applied to a copied config;
the source files are retained. `scripts/export_demo.py` provides the same export
as a CLI, e.g. `--scene rag-explainer --theme light-pastel --avatar drone
--view rag-rerank --out rerank.mp4`.

The eight editorial demos opt into `effects.neon`. Each function block keeps its
original thin border and adds a moving bright tip, tapered tail and local bloom.
The active block is brighter. Light themes reduce the bloom; text is never blurred.

```json
"effects": {
  "neon": {"enabled": true, "intensity": 0.8, "period": 6, "heroPeriod": 12, "tail": 144}
}
```

`intensity` is clamped to 0–1 (0 hides the light), periods are in seconds, and
`tail` is in canvas pixels (the hero tail is 1.35 times longer). Set `enabled`
to `false` to omit the effect. Omitting `effects.neon` preserves older scenes.
For a seamless exported loop, choose periods that divide the canvas duration.
All light positions are pure functions of `seek(t)` and follow pause, replay,
scrubbing and export. There is no independent CSS animation or random clock.

New authored SVG blocks can opt in by marking their outer `rect` with
`data-neon-border="unique-label"` and `data-neon-color="#rrggbb"`; add
`data-neon-role="hero"` for the slower hero period. These are authoring attributes,
not new JSON elements. The fixed semantic color remains even while the existing
state controller changes the base border stroke.

## Elements

- `text` `{x, y, w?, align, runs | t | text, size?, lh?, c?, b?, ls?, font?, inside?}`; `y` is the vertical centre of the line. `inside:true` = intentionally drawn on top of a box (icons).
- `box` `{x, y, w, h, color (border), fill?, radius?, border? (px), dash?, container?, pad:[top,left,right?], align, sides:"solid"?, lines:[...], when?, then?:{fill,color,border,glow}}`. Lines flow at `lineHeight`. `container:true` marks a box that holds other boxes (skipped by the overlap check). `when/then` restyle the whole box while a condition holds (`glow` = colour name).
- `path` `{points:[[x,y],...], color, width?, r? (corner radius), dash?, arrow?:false, head?, opacity?, when?, then?:{color,width,opacity}, flow?:{period, offsets, color, tail, when}}` SVG polyline with arrow head; `flow` adds packets along it.
- `line` `{from:[x,y], to:[x,y], dash?, color?, width?}` axis-aligned wire.
- `glyph` `{x, y, ch, c, size}` e.g. an arrow head.
- `rule` `{x, y, w}` double rule.
- `flow` `{path:[[x,y],...], period, offsets:[...], color, gap?:[y0,y1], tail?, when?}` packets looping along a polyline. Delivery count of all flows is `{packets}`.
- `tarrow` `{machine, i, from:[x,y], to:[x,y]}` dashed arrow for trigger `i` of a `triggers` machine; coloured and carrying a packet while that trigger is lit.
- `log` `{x, y, w, rows, padTop, padBottom, padLeft, title, titleX, titleW, cols:[{key:"time|who|m|g", x}]}`.

### Lines inside a box

A line is a string, or an object:
`{runs | t, c, b, align, indent, size, h, items, when, then, trigger}`
- `runs`: list of strings or run objects `{t | v | sw | cursor, c, b, size, when, then}`. `t` is text (may contain `{var}`), `v` a variable name, `sw` a colour swatch, `cursor` a blinking block. A run `v` that returns a coloured value uses its colour unless `c` is set.
- `items`: flex row `[{w?, grow?, ml?, align?, runs | bar}]`. `bar` is `{w, h, gauge: id}` (bound to a gauge machine) or `{w, h, segments:[{from,to,c}], mark?}` (fractions 0-1).
- `when` / `then`: condition `{var, eq|ne|in:[...]}` (a list of conditions = AND) and override `{c, b, bg}`. On a line the override applies to the whole row (e.g. highlight background); on a run it changes colour/weight.
- `trigger: [machineId, index]`: shortcut for a side-rail row bound to a triggers machine (`◇`/`◆` label, highlight).

## Machines (all pure functions of t)

| type | fields | variables |
| --- | --- | --- |
| `counter` | `start, rate, format:"comma"?, prefix?, suffix?` | `id` |
| `cycle` | `values:[string \| {t,m,g,...}], period, t0, order?, log?:{who,c}` | `id`, `id.i` (index), `id.<field>` |
| `gauge` | `values:[numbers], period, t0, seed, threshold, decimals?, high:{label,dest}, low:{label,dest}, log?:{who,c,msgs:[...],tail:"p={value} {label}"}` | `id`, `id.num`, `id.low` ("1"), `id.label`, `id.dest` |
| `any_low` | `of:[gaugeIds]` | `id` = "low" / "high" |
| `lane` | `period, run, off, busy, done:[...], phase?, spin?, log?:{who,c,msgs:[[text,tag]]}` | `id` (spinner + text, coloured), `id.state` |
| `triggers` | `period, on, t0, items:[{name, adv:[l1,l2], to?}], color, callsStart?, tokens?:{start,step,unit}, cps?, onText, offText, log?:{who,c,start:{m,g},end:{m,g}}` | `id.active` (index or -1), `id.label<i>`, `id.adv0`, `id.adv1` (typed), `id.calls`, `id.tokens`, `id.status`, `id.<item field>` |

Built-in variables: `{packets}` (deliveries so far), `{clock}`. Log templates may use item/gauge fields, e.g. `{name}`, `{value}`, `{label}`, `{dest}`.

## Added vector components

These components are loaded from `assets/components.js` and embedded into the
generated HTML, so the page has no external JS dependency. Existing configs
still use the same elements, machines and `seek(t)` interface.

Every component accepts `{type, x, y, w, h, scale?:1}`. Coordinates refer to its
local SVG; `scale` scales the rendered component uniformly about the top left.

| type | additional fields | motion |
| --- | --- | --- |
| `vector` | `markup`: trusted, authored SVG children | static panel, text and decoration |
| `orb` | `kind:"pixel"` or round, `r`, `cy`, `color`, `light`, `dark`, `eyeColor`, `phase`, `label`, `subtitle`, `detail` | glowing body floats, outer rings pulse |
| `seats` | `period` (12.5 seconds), `phase` (seconds), optional `labels` and `data.metrics` | 25 nodes disappear into a hub; four metric labels follow the selected count |
| `kanban` | `period` (9 seconds), `tickets:[strings]`, optional `labels` and `data` | tickets dwell in four columns, move between them, turn green, illustrative progress count advances |
| `donut` | optional `labels`, `data.parts`, `data.pulseAmount` | six sectors, expanding first slice and orbiting sparks |
| `ribbons` | optional `labels` | five fixed-width illustrative paths with continuous particles |
| `ghostSeats` | optional `labels` and `data` | dashed candidate nodes, three green people and one amber person fade in |
| `drone` | `period`, `path:[[x,y],...]`, `focusPeriod`, `targets:[{x,y,w,h}]`, `words:[{x,y,w,t}]` | smooth looping robot path, fan of wires and lights, target outline and dotted pointer, word highlights |

`drone` also accepts `avatar:"spider"|"drone"` (default `drone`),
`avatarScale` (default 1), `avatarColors:{leg,joint,shell,core}`,
`gaitSpeed` (default 7.2 radians/second), and optional `avatarHeading` (degrees).
The spider has eight independently articulated legs with alternating gait groups.
Its heading follows the path smoothly unless fixed, and its center is kept inside
the canvas to avoid cutting off legs. `window.setAvatar(kind)` switches all
traveling actors while retaining their paths and timeline position.

Business-specific labels and illustrative arithmetic remain the defaults for
compatibility with `scripts/make_business_example.py`. New configs can replace
them without changing JavaScript using the optional fields below. Omitting those
fields preserves the previous demo. Do not run a generator after manually editing
its `config.json` unless you intend to regenerate that file.

### Optional component labels and illustrative data

`labels` values are strings; arrays must contain every entry noted below.
Coordinates and component geometry remain fixed. The authored labels must fit the
local SVG dimensions; use the frame checker after replacing them. These fields
do not connect to a service, model, or live measurement.

| component | `labels` fields | `data` fields |
| --- | --- | --- |
| `seats` | `title`, `leader`, `teams:[4 strings]`, `hub:[2 strings]`, `count`, `captions:[4 strings]` | `metrics:[4 objects]`, each `{value?:number, perSeat?:number, prefix?:string, suffix?:string, decimals?:integer}`. `value` is fixed; otherwise the selected node count is multiplied by `perSeat` (default 1). The 25-node geometry stays fixed. |
| `donut` | `total`, `period`, `items:[6 strings]`, `values:[6 strings]`, `notes:[3 strings]` | `parts:[6 fractions]` (default `[.41,.19,.15,.09,.08,.08]`, nonnegative, sum 1); `pulseAmount` (default `.035`) is added to sector 1 and subtracted from sector 6. Keep each sector larger than its 2 px visual gap and `pulseAmount` smaller than sector 6. Legend values are authored captions, independent of the decorative pulse. |
| `kanban` | `columns:[4 strings]`, `countCaption`, `footer` | `countStart` (61), `countMax` (312, must be positive), `countRate` (360), `countPeriod` (35 seconds, must be positive). Progress is `min(countMax, countStart + floor(phase(t,countPeriod) * countRate))`. Keep `0 <= countStart <= countMax` and `countRate >= 0`. This preauthored counter is independent of the six moving cards. |
| `ribbons` | `source`, `branches:[5 strings]`, `values:[5 strings]`, `footer` | none; widths illustrate flow and do not derive quantitatively from captions |
| `ghostSeats` | `topValue`, `topCaption`, `middleValue`, `middleLines:[2 strings]`, `bottomValues:[2 strings]`, `bottomLines:[4 strings]` | `revealPeriod` (35 seconds), `revealStart` (8 seconds), `revealDuration` (4 seconds). Period and duration must be positive; reveal time uses the repeating local period. Geometry stays 25 dashed nodes, three green figures and one amber figure. |

`scripts/editorial_components.py` supplies the current portrait Chinese examples
of these fields and avatar navigation. The component showcase and avatar
navigation support all four editorial palette variants.

For cycle-driven guides, optional `drone.timelineMachine` names a `cycle`
machine. Its `period`, `t0` and `order` then drive route traversal and the focus
target together. Path points and targets correspond to that machine's value
indices. Without this field the original independent timing is preserved.

All animated state is a pure function of `t`. The vector text validator includes
SVG group transforms and uniform component scaling. Drone overlays are excluded
from text bounds checking because they intentionally highlight other elements.

## Original editorial scenes

`ragEditorial` is an authored scene component with `{x,y,w:984,h:1280}`.
It draws the original RAG composition in `assets/rag-editorial.js`: one main
journey and four detailed panels for retrieval, ranking, citations and abstention.
The default four 3-second stages and traveling particles remain pure functions of `t`.
Text, scores and document examples are authored data, not connected measurements.
`scripts/rag_editorial.py` configures the scene and the separate selectable spider.
`livepanel.build_page` embeds this optional asset alongside the standard components.
The older RAG page remains available as `examples/capability-demos/rag-explainer/live-before.html`.

The collection also registers `agentEditorial`, `requestEditorial`,
`incidentEditorial`, `knowledgeEditorial`, `workflowEditorial`, `labEditorial`
and `avatarEditorial` through `assets/editorial-*.js`. These are original,
authored 984×1280 compositions. Machines provide live state inside the simulated
timeline; labels, document fragments and geometry remain authored scene data.
Edit the Python scene builders for machine settings and the JS for composition.
Every example retains its original web page, configuration, poster and video.

`meta.visualStyle: "editorial"` asks `build_page` to embed the bundled LP font
subsets. Fonts and their original OFL notices remain self-contained in the HTML;
see `assets/fonts/README.md`. The gallery uses the same embedded typography.

## Replay hook (unchanged)

`window.seek(t)` draws the frame at second `t`. `window.__ready` becomes true when the config is loaded and fonts are ready; `window.__check()` returns a list of layout problems (used by `check_frames.py`). `?manual` in the URL disables the live loop.
