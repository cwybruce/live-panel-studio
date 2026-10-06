"""Shared helpers: build the page from template + config, and drive Chrome over the DevTools pipe (standard library only)."""
import base64, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = ROOT / "assets" / "template.html"
CHROME_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "microsoft-edge"]


def find_exe(explicit, names, what):
    if explicit:
        p = shutil.which(explicit) or (explicit if os.path.exists(explicit) else None)
        if p:
            return p
        sys.exit(f"{what} not found: {explicit}")
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    if what == 'Chrome' and os.name == 'nt':
        for prefix in (os.environ.get('PROGRAMFILES'), os.environ.get('PROGRAMFILES(X86)'), os.environ.get('LOCALAPPDATA')):
            if not prefix:
                continue
            for suffix in ('Google/Chrome/Application/chrome.exe', 'Microsoft/Edge/Application/msedge.exe'):
                p = Path(prefix) / suffix
                if p.is_file():
                    return str(p)
    sys.exit(f"{what} not found on PATH (tried {', '.join(names)}); pass it explicitly")


CANVAS_PRESETS = {"4:5": (1200, 1500), "3:4": (1080, 1440), "1:1": (1080, 1080)}


def canvas(cfg):
    """(width, height, duration, fps) from a config, honouring canvas.preset."""
    cv = cfg.get("canvas", {})
    pw, ph = CANVAS_PRESETS.get(cv.get("preset"), (1200, 1500))
    return cv.get("width", pw), cv.get("height", ph), cv.get("duration", 30), cv.get("fps", 30)


def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_page(config_path, out_path, template=None):
    """Write a self-contained HTML file: template with the JSON config embedded. Returns the config dict."""
    cfg = load_config(config_path)
    tpl = Path(template or DEFAULT_TEMPLATE).read_text(encoding="utf-8")
    if '<!--LIVE_EXTENSIONS-->' in tpl:
        ext = (Path(template or DEFAULT_TEMPLATE).parent / 'components.js').read_text(encoding='utf-8')
        for filename in ['editorial-theme.js', 'rag-editorial.js', 'editorial-systems.js',
                         'editorial-stories.js', 'editorial-components.js', 'neon-flow.js', 'terminal-shell.js']:
            editorial = Path(template or DEFAULT_TEMPLATE).parent / filename
            if editorial.is_file():
                ext += '\n' + editorial.read_text(encoding='utf-8')
        tpl = tpl.replace('<!--LIVE_EXTENSIONS-->', ext)
    if cfg.get('meta', {}).get('visualStyle') == 'editorial':
        from editorial_fonts import font_style
        tpl = tpl.replace('</head>', font_style() + '</head>')
    blob = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    tag = f'<script id="live-config" type="application/json">{blob}</script>'
    if "<!--LIVE_CONFIG-->" not in tpl:
        sys.exit("template has no <!--LIVE_CONFIG--> placeholder")
    Path(out_path).write_text(tpl.replace("<!--LIVE_CONFIG-->", tag), encoding="utf-8")
    return cfg


class Chrome:
    """Headless Chrome driven through --remote-debugging-pipe (no websocket, no third-party packages)."""

    def __init__(self, chrome, width, height, no_sandbox=None):
        self._pw = None
        if os.name == 'nt':
            try:
                from playwright.sync_api import sync_playwright
            except ImportError as e:
                raise RuntimeError('Windows rendering requires: python -m pip install playwright (uses your installed Chrome/Edge).') from e
            self._pw = sync_playwright().start()
            try:
                self._browser = self._pw.chromium.launch(executable_path=chrome, headless=True,
                    args=['--force-device-scale-factor=1', '--font-render-hinting=none', '--allow-file-access-from-files'])
                self._page = self._browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
                self._cdp = self._page.context.new_cdp_session(self._page)
            except Exception:
                self._pw.stop()
                raise
            return
        self.tmp = tempfile.mkdtemp(prefix="livepanel-")
        r1, w1 = os.pipe()   # we write -> chrome fd 3
        r2, w2 = os.pipe()   # chrome fd 4 -> we read
        args = [chrome, "--headless=new", "--remote-debugging-pipe", f"--user-data-dir={self.tmp}", "--no-first-run",
                "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--font-render-hinting=none",
                "--allow-file-access-from-files", "--disable-background-timer-throttling", "--mute-audio", "about:blank"]
        if no_sandbox or (no_sandbox is None and hasattr(os, "geteuid") and os.geteuid() == 0):
            args.insert(1, "--no-sandbox")
        env = dict(os.environ, LP_R=str(r1), LP_W=str(w2))
        self.proc = subprocess.Popen(["sh", "-c", 'exec "$@" 3<&"$LP_R" 4>&"$LP_W"', "sh"] + args, pass_fds=(r1, w2), env=env,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.close(r1); os.close(w2)
        self.wf = os.fdopen(w1, "wb", buffering=0); self.rf = os.fdopen(r2, "rb", buffering=0)
        self.buf = b""; self.n = 0
        tid = self.call("Target.createTarget", {"url": "about:blank"})["targetId"]
        self.sid = self.call("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        self.cmd("Page.enable")
        self.cmd("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False})

    def call(self, method, params=None, session=None):
        self.n += 1
        msg = {"id": self.n, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self.wf.write(json.dumps(msg).encode() + b"\0")
        while True:
            while b"\0" not in self.buf:
                chunk = os.read(self.rf.fileno(), 1 << 20)
                if not chunk:
                    raise RuntimeError("Chrome closed the pipe")
                self.buf += chunk
            raw, self.buf = self.buf.split(b"\0", 1)
            m = json.loads(raw)
            if m.get("id") == self.n:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})

    def cmd(self, method, params=None):
        if self._pw:
            return self._cdp.send(method, params or {})
        return self.call(method, params, self.sid)

    def eval(self, expr):
        if self._pw:
            return self._page.evaluate(expr)
        r = self.cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in r:
            raise RuntimeError(f"js error: {r['exceptionDetails']}")
        return r["result"].get("value")

    def open(self, url, timeout=20):
        if self._pw:
            self._page.goto(url, wait_until='load', timeout=timeout * 1000)
            self._page.wait_for_function('window.__ready === true || Boolean(window.__error)', timeout=timeout * 1000)
            err = self.eval("window.__error||''")
            if err:
                raise RuntimeError('page error: ' + err)
            return
        self.cmd("Page.navigate", {"url": url})
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                if self.eval("window.__ready===true"):
                    err = self.eval("window.__error||''")
                    if err:
                        raise RuntimeError("page error: " + err)
                    return
                err = self.eval("window.__error||''")
                if err:
                    raise RuntimeError("page error: " + err)
            except RuntimeError as e:
                if "page error" in str(e):
                    raise
            time.sleep(0.1)
        raise RuntimeError("page did not become ready (check the config JSON)")

    def seek(self, t):
        self.eval(f"window.seek({t!r})")

    def shot(self):
        return base64.b64decode(self.cmd("Page.captureScreenshot", {"format": "png", "optimizeForSpeed": True})["data"])

    def close(self):
        if self._pw:
            try:
                self._browser.close()
            finally:
                self._pw.stop()
            return
        try:
            self.proc.terminate(); self.proc.wait(5)
        except Exception:
            self.proc.kill()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
