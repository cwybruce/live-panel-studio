# 平台支持与验证路线图 / Platform support and verification

截至 2026-10-06，源码保留 Windows、Linux 和 macOS 的渲染实现。本项目已完成的实际验收来自 **Windows、Python 3.11、系统 Chrome 和 FFmpeg**。Linux / macOS 的新增主题、完整导出和功能块导出仍需要在各平台实际运行验证。

As of 2026-10-06, the source retains rendering implementations for Windows, Linux and macOS. Completed acceptance runs used **Windows, Python 3.11, system Chrome and FFmpeg**. The new palettes, complete exports and block exports still need actual Linux and macOS acceptance runs.

| 平台 / Platform | 当前实现 / Current implementation | 验收边界 / Acceptance boundary |
| --- | --- | --- |
| Windows | `os.name == 'nt'` 使用 Playwright 控制已安装的 Chrome / Edge。 / Playwright drives an installed Chrome / Edge. | Chrome 已实测；Edge 自动查找路径存在，未据此声称 Edge 已完成验收。 / Chrome was tested; Edge discovery exists but does not establish Edge acceptance. |
| Linux | 保留上游的 `os.pipe`、`pass_fds`、`sh` 和 Chrome `--remote-debugging-pipe` 路径。 / Retains upstream pipes, file descriptors, shell and Chrome DevTools-pipe path. | 本项目新增流程尚未实际验收。 / The added workflow has not been accepted on Linux. |
| macOS | 使用同一非 Windows DevTools-pipe 路径；Chrome 可执行文件需放入 `PATH`，或对 `render.py` 显式传入 `--chrome`。 / Uses the same non-Windows pipe path; expose Chrome on `PATH` or pass `render.py --chrome`. | 本项目新增流程尚未实际验收。 / The added workflow has not been accepted on macOS. |

Windows 新增分支在初始化后返回；非 Windows 不会导入 Playwright。相关源码见 [`livepanel.py`](../scripts/livepanel.py)。这证明非 Windows 实现被保留，不能代替各平台的运行验收。

The Windows branch returns after initialization; non-Windows execution does not import Playwright. See [`livepanel.py`](../scripts/livepanel.py). Source retention establishes an available implementation path, while platform acceptance requires execution.

[`render.py`](../scripts/render.py) 使用 `Path.as_uri()` 处理本地网页路径，将 MP4 写入相邻 `.pending.mp4` 后通过 `os.replace()` 完成写入。[`export_demo.py`](../scripts/export_demo.py) 在输出目录内建立临时目录，完成视频尺寸、帧率、帧数、时长和完整解码检查后再替换输出；超时取消分别使用 Windows `taskkill` 或 POSIX 进程组信号。这些文件与进程操作包含两类平台的实现，但仍需验证真实运行和取消行为。

[`render.py`](../scripts/render.py) uses `Path.as_uri()` for local pages and writes a sibling `.pending.mp4` before `os.replace()`. [`export_demo.py`](../scripts/export_demo.py) uses a temporary directory inside the output directory and verifies dimensions, frame rate, frame count, duration and full decoding before replacement. Cancellation uses Windows `taskkill` or POSIX process-group signals. Both platform paths are implemented; real execution and cancellation still require platform testing.

## 当前测试证据 / Current test evidence

核查快照为提交 `cba94b8`：[`tests/`](../tests/) 下有 **7 个测试模块、34 个测试方法**；维护者的本地改名回归日志记录 `Ran 34 tests`、`OK`。导出请求测试包含 39 个功能块 × 4 主题 × 2 角色，共 312 种请求组合；其中 HTTP 队列测试使用模拟导出，不能等同于 312 段视频实际渲染。实际媒体检查覆盖 32 段完整 Demo；本地报告的浏览器路径是 Windows `Chrome.exe`。本地日志和验收 JSON 未作为跨平台 CI 结果发布。

At commit `cba94b8`, [`tests/`](../tests/) contains **7 test modules and 34 test methods**. The maintainer's local rebranding regression log records `Ran 34 tests` and `OK`. Request validation covers 39 blocks × 4 palettes × 2 avatars: 312 combinations. HTTP queue tests mock the exporter, so this does not represent 312 real rendered videos. Real media checks cover 32 complete demo videos; the local report identifies Windows `Chrome.exe`. Local logs and acceptance JSON are not published cross-platform CI results.

该快照的 Git 历史包含 7 次提交（含上游初始提交），并非单提交仓库。仓库当时没有 `.github/workflows` 测试矩阵；GitHub Pages 能访问只能证明静态资源发布，不能证明 Linux / macOS 的 Python 渲染与导出通过。

That snapshot has seven Git commits, including the upstream initial commit. It has no `.github/workflows` test matrix. GitHub Pages availability establishes static publication; it does not establish Linux / macOS Python rendering or export acceptance.

## Linux / macOS 可执行验收 / Reproducible Linux / macOS acceptance

先在目标机器安装 Python 3.11+、Chrome / Chromium、FFmpeg（含 `ffprobe` 和 `libx264`）；进入仓库根目录。以下 Bash 命令是待运行的验收步骤，本页未声称已经在这些平台执行。非 Windows 渲染与测试不需要安装 `requirements-windows.txt`。

Install Python 3.11+, Chrome / Chromium and FFmpeg with `ffprobe` and `libx264`, then enter the repository root. The Bash commands below are acceptance procedures to execute on the target machine, not completed Linux / macOS runs. The non-Windows renderer and tests do not require `requirements-windows.txt`.

```bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
mkdir -p out
python3 --version
ffmpeg -version
ffprobe -version
```

Linux 选择已安装浏览器；macOS 则使用应用内的实际可执行文件。任选对应的一段： / Choose the corresponding browser setup for the target OS:

```bash
# Linux
MDS_CHROME="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser)"
test -n "$MDS_CHROME"
```

```bash
# macOS: adjust this path if Chrome is installed elsewhere.
MDS_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
test -x "$MDS_CHROME"
mkdir -p out/platform-bin
ln -sf "$MDS_CHROME" out/platform-bin/google-chrome
export PATH="$PWD/out/platform-bin:$PATH"
```

记录版本，运行全部测试，随后实际逐帧生成一段完整视频和一段功能块视频；输出保存在忽略目录 `out/`。 / Record versions, run the full suite, then render a complete video and a block video frame by frame. Outputs go to the ignored `out/` directory.

```bash
git rev-parse HEAD
"$MDS_CHROME" --version
python3 -m unittest discover -s tests -v 2>&1 | tee out/platform-tests.log

python3 scripts/render.py \
  --config examples/capability-demos/rag-explainer/config-terminal.json \
  --out out/platform-terminal.mp4 --chrome "$MDS_CHROME"

python3 scripts/export_demo.py \
  --scene rag-explainer --theme pastel-classic --avatar drone \
  --view rag-rerank --out out/platform-pastel-rerank.mp4

python3 - <<'PY'
import json, platform, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from export_demo import validate_request, verify_video
checks = []
for theme, avatar, view, file in [
    ('terminal-classic', 'spider', 'full', 'out/platform-terminal.mp4'),
    ('pastel-classic', 'drone', 'rag-rerank', 'out/platform-pastel-rerank.mp4'),
]:
    spec = validate_request(dict(scene='rag-explainer', theme=theme,
                                 avatar=avatar, view=view))
    checks.append(dict(theme=theme, avatar=avatar, view=view, file=file,
                       **verify_video(Path(file), spec.width, spec.height)))
report = dict(platform=platform.platform(), python=sys.version, videos=checks)
Path('out/platform-media.json').write_text(json.dumps(report, indent=2) + '\n',
                                         encoding='utf-8')
print(json.dumps(report, indent=2))
PY
```

验收应包含：测试无失败、12 秒 / 30fps / 360 帧的视频完整解码、功能块尺寸正确，以及浏览器中主题 / 角色切换、暂停与拖动时间轴、本地导出成功。使用 `python3 scripts/preview_server.py --port 8779` 后访问 `http://127.0.0.1:8779/index.html`；停止服务用 Ctrl+C。另行测试取消 / 超时处理，确认目标视频不出现半成品，再保留系统、Python、浏览器与 FFmpeg 版本、提交 SHA、日志和媒体检查结果。

Acceptance should include a passing suite, fully decoded 12-second / 30fps / 360-frame videos, correct block dimensions, and browser checks for palette / avatar changes, pause / seeking and local export. Run `python3 scripts/preview_server.py --port 8779` and open `http://127.0.0.1:8779/index.html`; stop with Ctrl+C. Separately check cancellation / timeout behavior and absence of partial final videos. Preserve OS, Python, browser and FFmpeg versions, commit SHA, logs and media reports.

## 下一步 / Next steps

1. 先完成一台 Linux 与一台 macOS 的上述人工验收，记录失败和版本差异。 / Complete these manual checks on one Linux and one macOS machine, recording failures and version differences.
2. 再建立 Windows / Linux / macOS CI 矩阵，运行实际浏览器测试、完整视频与功能块导出，并保存结果作为构建产物。 / Then add a Windows / Linux / macOS CI matrix with actual browser tests, full and block exports, and retained artifacts.
3. 只有对应平台留下可复现的成功记录后，才将文档状态改为“实测通过”。 / Mark each platform as tested only after a reproducible successful run is recorded.
