"""Real Chrome + CDP attach, plus Cloudflare challenge handling.

Cloudflare passes because the browser is launched normally (not by Playwright)
and Playwright attaches over CDP.
"""
import os
import subprocess
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
PROFILE = ROOT / "profile2"
CHROME = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
PORT = int(os.getenv("CDP_PORT", "9333"))
CDP = f"http://127.0.0.1:{PORT}"
BASE = os.getenv("POLY_BASE", "https://testnet.polyester.com")
INJECT = (ROOT / "wallet_provider.js").read_text()

CF_TEXT = ("just a moment", "performing security verification",
           "verifying you are human", "security verification", "attention required")


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- Cloudflare

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
    """Click the interactive Turnstile checkbox. The widget iframe lives in a shadow
    root, so locate it through page.frames and frame_element()."""
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
    """Wait out / solve the Cloudflare challenge: click the checkbox, reload on stall."""
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


# ------------------------------------------------------------- Chrome / CDP

def kill_existing():
    subprocess.run(["pkill", "-f", f"user-data-dir={PROFILE}"], capture_output=True)
    time.sleep(1.5)


def is_running():
    try:
        r = requests.get(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def launch(url=BASE, headless_display=":99"):
    args = [CHROME, "--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
            f"--user-data-dir={PROFILE}", f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*", "--window-size=1440,900", "--no-first-run",
            "--no-default-browser-check", "--lang=en-US", url]
    env = dict(os.environ, DISPLAY=headless_display)
    subprocess.Popen(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        time.sleep(2)
        if is_running():
            return True
    return False


def page_target():
    try:
        for t in requests.get(f"http://127.0.0.1:{PORT}/json", timeout=5).json():
            if t.get("type") == "page" and "polyester" in (t.get("url") or ""):
                return t
    except Exception:
        pass
    return None


def wait_page(timeout=120):
    t0 = time.time()
    while time.time() - t0 < timeout:
        t = page_target()
        if t:
            title = t.get("title") or ""
            url = t.get("url") or ""
            if "Just a moment" not in title and "polyester" in url.lower():
                return t
        time.sleep(3)
    return None


def ensure_chrome(url=BASE):
    if not is_running():
        log("launching chrome...")
        kill_existing()
        launch(url)
    t = wait_page()
    if t:
        log("chrome ready:", t.get("title"), "|", t.get("url"))
    return t
