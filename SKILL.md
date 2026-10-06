---
name: motion-diagram-studio
description: Use when the user wants animated architecture, agent, RAG or business-flow diagrams from JSON, with interactive HTML playback or whole-diagram and block MP4 exports.
---

# Motion Diagram Studio · 动态图解工作室

Turn a system description into a continuously animated diagram, an interactive web page and an MP4 video. A complete diagram stays readable while packets, states, logs, counters, neon borders and guide avatars show how the flow works.

This is an independently maintained extension of [live-panel-skill](https://github.com/ythx-101/live-panel-skill) by **[@YuLin807](https://x.com/YuLin807)**, maintained here by **[@sycbruce](https://x.com/sycbruce)**. It adds eight Chinese demos, four palettes, SVG components, spider / robot avatars, interactive playback and local export of whole demos or named blocks. It is not the upstream official project. All bundled demo events and metrics are **scripted simulations**, not live agents or business telemetry.

> **Design credit.** The upstream terminal look and motion grammar were inspired by **[@thedelost](https://x.com/thedelost)**'s [Codex agent-tree clip](https://x.com/thedelost/status/2105398038026195279), shared through **[@slashui](https://x.com/slashui)**'s [quote-post](https://x.com/slashui/status/2105850132365443528). `examples/codex-agents/` recreates that design; `examples/agent-architecture/` animates 小红书 **@林纾**'s infographic. Their visual designs, layout and wording retain their original rights; keep credits when publishing recreations. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## When to use

- Animate architecture, agent handoffs, RAG evidence, request paths, knowledge cards, ticket workflows or incident recovery.
- Provide a live page with pause, replay, timeline scrubbing, speed and key-moment controls; switch palettes and supported avatars.
- Render a complete diagram or a named demo block as an MP4 for teaching or project demonstrations.
- For real telemetry, first define and implement a data integration. The bundled examples and preview service do not provide one.

## Input

A JSON config defines canvas dimensions, colors, text, boxes, wires, packet paths, state machines, components, avatars and source credits. Read [references/config-schema.md](references/config-schema.md) for the fields; the HTML template normally needs no edits.

Start with `examples/capability-demos/rag-explainer/config.json`, or choose another scene from [the demo guide](examples/capability-demos/README.md): `agent-team`, `product-request`, `knowledge-card`, `business-workflow`, `incident-replay`, `component-lab` or `avatar-themes`.

Upstream configs remain supported: `examples/codex-agents/`, `examples/airbnb/` and `examples/agent-architecture/`. Canvas presets remain `4:5` (1200×1500), `3:4` (1080×1440) and `1:1` (1080×1080); the added demos use 984×1280 compositions. Positions are absolute canvas pixels, so a different aspect ratio needs its own layout. Internal `livepanel` module names retain compatibility and do not change the installed skill name.

## Four palettes and compatible config fields

| Palette / CLI theme ID | Appearance |
| --- | --- |
| `terminal-dark` | Warm Ink / 暖黑 |
| `light-pastel` | Warm Paper / 暖纸 |
| `terminal-classic` | Classic Terminal / 经典终端 |
| `pastel-classic` | Classic Pastel / 经典粉彩 |

Editorial configs use `theme.variant` for these four palettes. The compatible base-renderer field `theme.preset` remains `terminal-dark` or `light-pastel`; explicit `theme.colors` supplies the selected palette. Use the generated matching config rather than replacing `theme.preset` with a classic variant ID. Theme and avatar are independent: `spider` is the spider and `drone` is the robot. Avatars appear in scenes with actor definitions.

## Fixed procedure

1. **Collect content and where each number comes from.** List boxes, who talks to whom, which things are "on call" triggers, what the log would say. Write the source (link or "simulated") next to every number. If a number has no real source, it is simulated: say so on screen (a footer line, or "(illustrative)" next to the counter). Never invent a figure and present it as real.
2. **Write the config.** Copy an example. Place boxes on a pixel grid (x, y, w, h in canvas px); text lines flow inside boxes at one fixed line height. Put the credit/source line in `credit`. Read `references/motion-grammar.md` before choosing machines and periods. If editing generated JSON directly, render that config; rerunning the demo generator replaces generated configs.
3. **Render.** `python scripts/render.py --config my.json --out my.mp4 --html-out page.html` (needs a system Chrome / Chromium / Edge and FFmpeg; `--chrome` / `--ffmpeg` accept explicit paths). The saved self-contained HTML includes the bundled font subsets and runs offline.
4. **Check by frames, not by trust.** `python scripts/check_frames.py --config my.json --out-dir frames --repeat` samples ~120 time points, measures text overflow and overlaps from the DOM, exports PNGs and tests replay determinism. Open the PNGs and look: the checker catches geometry, not taste. Fix the config and repeat until it exits 0.

For installation and platform status, follow [README.md](README.md) or [README.en.md](README.en.md). Windows has been tested; upstream Linux/macOS paths remain, while the added end-to-end export flow still needs platform validation.

## Interactive preview and block export

From the repository root, generate the demo pages if needed and start the local service:

```bash
python scripts/make_capability_demos.py
python scripts/preview_server.py --port 8779
```

Open `http://127.0.0.1:8779/index.html`. Select a scene, one of four palettes, a supported avatar and an export scope. Playback offers pause, replay, timeline scrubbing, 0.5/1/2× speed and key moments. The component lab also offers six close-up views.

Pre-rendered MP4s are distributed through versioned Releases. To restore local demo videos, run `python scripts/media_assets.py download --set demos`; use `--set all` for retained examples, recreations and block exports too. Interactive HTML and rendering new videos do not require those pre-rendered files. See [media distribution](docs/media-distribution.md).

The eight demos have **39 named export blocks**. “导出当前方案” exports the full scene or selected block on its complete 12-second timeline, at 30 fps, as H.264 MP4. Blocks are actual canvas crops retaining text, internal animation and a glow margin. The service binds only to `127.0.0.1` and writes new files to `examples/capability-demos/exports/`, preserving source configs and videos.

The same export is available from the CLI:

```bash
# Entire RAG demo, Warm Paper, robot
python scripts/export_demo.py --scene rag-explainer --theme light-pastel --avatar drone --view full --out rag-light.mp4

# Reranking evidence block, Classic Pastel, robot
python scripts/export_demo.py --scene rag-explainer --theme pastel-classic --avatar drone --view rag-rerank --out rag-rerank.mp4
```

Valid scenes, palette variants and block IDs are listed in [manifest.json](examples/capability-demos/manifest.json). Static hosting supports interactive playback and existing video downloads; rendering a new MP4 requires the local Python service or CLI. For demo-wide verification, run `python scripts/verify_capability_demos.py` and `python scripts/verify_demo_exports.py`; browser / video checks need the installed browser, FFmpeg and `ffprobe`.

## Motion rules in one screen

(Full text and rationale: `references/motion-grammar.md`.)

- **Layout stays fixed.** A readable complete diagram is present at frame 0; state and guide avatars move within it.
- **Three tempos at once**: fast (packets with trails on every wire, spinners, fast counters), medium (log scrolls with newest line bright and older grey; bars re-roll and flip colour and label past a threshold), slow (side-rail triggers light up one at a time in order, their arrow changes colour and carries a packet, advice is typed out, totals accumulate).
- **One truth everywhere.** The number in the log is the number on the bar; the trigger lit in the rail is the one the log mentions; counters in the status bar equal counters in boxes. In this engine that holds by construction: log lines are generated from the same state machines as the boxes.
- **No real data? Say "illustrative".** Fixed facts stay fixed; only the animation's own counters move, and they are labelled.
- **Neon follows the timeline.** Configure `effects.neon` for sweeping borders, tails and local bloom. Light palettes reduce bloom; text stays sharp.

## Determinism (why it renders the same every time)

The page exposes `window.seek(t)`. Every visual is a pure function of `t` (and a fixed integer seed for the few "random" picks): no wall clock, no `Math.random`, no CSS animation. The renderer calls `seek(i/fps)` and screenshots; `check_frames.py --repeat` seeks away and back and compares bytes. Opened in a normal browser (no `?manual`), the same function is driven by `requestAnimationFrame` and loops.

## Files

- `assets/template.html` - the generic page. `scripts/render.py` - MP4. `scripts/check_frames.py` - checks + PNGs. `scripts/livepanel.py` - shared browser and renderer helpers.
- `scripts/make_capability_demos.py`, `scripts/preview_server.py`, `scripts/export_demo.py` - demo generation, local preview and named exports.
- `references/motion-grammar.md`, `references/config-schema.md`.
- `examples/capability-demos/` - eight scenes, four palettes, standalone HTML, JSON configs and export metadata.
- `examples/codex-agents/`, `examples/airbnb/`, `examples/agent-architecture/` - compatible upstream examples; preserve their individual source credits.

## Light theme notes

For infographics keep the original colours and structure; motion is gentler: small packets drift along every arrow, state-bound arrows turn the accent colour and carry two packets, active boxes get a glow, lists (steps, tools) light one row at a time from one shared `cycle` machine so that everything on screen refers to the same step. Use `container:true` on boxes that hold other boxes so the checker does not call nested boxes overlapping, and `inside:true` on icon text placed on a box.

## Credit rule

Always put the original author and link of any picture you re-animate or recreate in the video footer (`credit`) and in the post. State when a figure is simulated.

[LICENSE](LICENSE) contains the MIT code license and original upstream copyright. Bundled fonts remain under SIL OFL 1.1, and third-party reference designs retain their own rights; the engine's MIT license does not relicense them. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for sources and exclusions.
