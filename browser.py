"""Shared Playwright browser factory + Cloudflare challenge handling."""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from w3wallet import WalletBridge

ROOT = Path("/root/polyester-bot")
PROFILE = ROOT / "profile"
CHROME = "/usr/bin/google-chrome" if Path("/usr/bin/google-chrome").exists() else \
    "/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"

STEALTH_JS = r"""
(() => {
  const def = (o, p, get) => { try { Object.defineProperty(o, p, {get, configurable: true}); } catch(e){} };
  def(navigator, 'webdriver', () => undefined);
  def(navigator, 'languages', () => ['en-US', 'en']);
  def(navigator, 'hardwareConcurrency', () => 8);
  def(navigator, 'deviceMemory', () => 8);
  def(navigator, 'maxTouchPoints', () => 0);
  def(navigator, 'plugins', () => ([
    {name:'PDF Viewer', filename:'internal-pdf-viewer', description:'Portable Document Format'},
    {name:'Chrome PDF Viewer', filename:'internal-pdf-viewer', description:'Portable Document Format'},
    {name:'Chromium PDF Viewer', filename:'internal-pdf-viewer', description:'Portable Document Format'},
    {name:'Microsoft Edge PDF Viewer', filename:'internal-pdf-viewer', description:'Portable Document Format'},
    {name:'WebKit built-in PDF', filename:'internal-pdf-viewer', description:'Portable Document Format'},
  ]));
  def(navigator, 'mimeTypes', () => ([{type:'application/pdf'}, {type:'text/pdf'}]));
  if (!window.chrome) window.chrome = {};
  window.chrome.runtime = window.chrome.runtime || {};
  window.chrome.app = window.chrome.app || {isInstalled: false, InstallState: {DISABLED:'disabled', INSTALLED:'installed', NOT_INSTALLED:'not_installed'}, RunningState: {CANNOT_RUN:'cannot_run', READY_TO_RUN:'ready_to_run', RUNNING:'running'}};
  window.chrome.csi = window.chrome.csi || function(){ return {}; };
  window.chrome.loadTimes = window.chrome.loadTimes || function(){ return {}; };
  window.chrome.heapProfiler = window.chrome.heapProfiler || {};
  window.chrome.profiler = window.chrome.profiler || {};
  const gp = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function (p) {
    if (p === 37445) return 'Google Inc. (Intel)';
    if (p === 37446) return 'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)';
    return gp.apply(this, arguments);
  };
  const gp2 = WebGL2RenderingContext.prototype.getParameter;
  WebGL2RenderingContext.prototype.getParameter = function (p) {
    if (p === 37445) return 'Google Inc. (Intel)';
    if (p === 37446) return 'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)';
    return gp2.apply(this, arguments);
  };
  try {
    const q = window.navigator.permissions.query.bind(window.navigator.permissions);
    window.navigator.permissions.query = (p) => (
      p && p.name === 'notifications'
        ? Promise.resolve({state: Notification.permission, onchange: null})
        : q(p));
  } catch(e){}
})();
"""
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")
BASE = "https://testnet.polyester.com"

CF_TEXT = ("just a moment", "performing security verification",
           "verifying you are human", "security verification", "attention required")


def is_challenge(page) -> bool:
    try:
        tl = page.title().lower()
        if any(k in tl for k in ("just a moment", "attention required")):
            return True
        txt = page.inner_text("body")[:300].lower()
        return any(k in txt for k in CF_TEXT)
    except Exception:
        return False


def click_turnstile(page) -> bool:
    """Click the interactive Turnstile checkbox. The widget iframe lives in a shadow root,
    so locate it through page.frames and frame_element()."""
    frames = []
    for f in page.frames:
        try:
            if "challenges.cloudflare.com" in (f.url or ""):
                frames.append(f)
        except Exception:
            pass
    for f in frames:
        box = None
        try:
            el = f.frame_element()
            box = el.bounding_box()
        except Exception:
            box = None
        if not box:
            continue
        for fx in (0.18, 0.30, 0.5):
            x = box["x"] + box["width"] * fx
            y = box["y"] + box["height"] / 2
            try:
                page.mouse.move(x, y, steps=10)
                page.wait_for_timeout(300)
                page.mouse.click(x, y)
                return True
            except Exception:
                pass
    # fallback: plain iframe selectors
    for sel in ("iframe[src*='challenges.cloudflare.com']", "iframe[title*='Cloudflare']",
                "#cf-chl-widget-iframe"):
        try:
            el = page.query_selector(sel)
            box = el.bounding_box() if el else None
        except Exception:
            box = None
        if box and box.get("width", 0) > 10:
            try:
                page.mouse.click(box["x"] + 30, box["y"] + box["height"] / 2)
                return True
            except Exception:
                pass
    return False


def pass_cf(page, timeout=120, label="") -> bool:
    """Wait out / solve the Cloudflare challenge. Clicks the checkbox and reloads on stall."""
    t0 = time.time()
    last_click = 0
    clicks = 0
    while time.time() - t0 < timeout:
        if not is_challenge(page):
            print(f"  [cf{label}] passed in {time.time()-t0:.1f}s", flush=True)
            return True
        if clicks < 8 and time.time() - last_click > 5:
            if click_turnstile(page):
                clicks += 1
                last_click = time.time()
                print(f"  [cf{label}] clicked checkbox #{clicks}", flush=True)
        # stall -> reload (but not too eagerly)
        if time.time() - last_click > 50 and time.time() - t0 > 50:
            try:
                page.reload(wait_until="domcontentloaded", timeout=45000)
            except Exception:
                pass
            last_click = time.time()
            clicks = 0
            print(f"  [cf{label}] reload", flush=True)
        time.sleep(1.5)
    print(f"  [cf{label}] TIMEOUT", flush=True)
    return False


def goto(page, url, timeout=90000, tries=4):
    for i in range(tries):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        except Exception as e:
            print("  goto err:", str(e)[:120], flush=True)
        if pass_cf(page, 110, f"{i}" if i else ""):
            return True
        print(f"  goto retry {i+1}", flush=True)
    return False


def make_browser(playwright, headless=False, profile=True):
    args = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled", "--window-size=1440,900",
            "--lang=en-US", "--no-first-run", "--no-default-browser-check",
            "--disable-features=IsolateOrigins,site-per-process"]
    if profile:
        ctx = playwright.chromium.launch_persistent_context(
            str(PROFILE), headless=headless, executable_path=CHROME, args=args,
            viewport={"width": 1440, "height": 900}, user_agent=UA, locale="en-US",
            timezone_id="Asia/Jakarta")
    else:
        b = playwright.chromium.launch(headless=headless, executable_path=CHROME, args=args)
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, user_agent=UA,
                            locale="en-US", timezone_id="Asia/Jakarta")
    ctx.add_init_script(STEALTH_JS)
    pages = ctx.pages
    return ctx, (pages[0] if pages else ctx.new_page())


def attach_wallet(page, wallet: WalletBridge):
    wallet.bind(page)
    page.add_init_script(
        f"window.__WALLET_ADDRESS={json.dumps(wallet.address)};"
        f"window.__WALLET_CHAIN_HEX={json.dumps(wallet.chain_hex)};")
    page.add_init_script((ROOT / "wallet_provider.js").read_text())
