"""Real Chrome + CDP attach (Cloudflare passes because the browser is not automation-launched)."""
import json
import os
import subprocess
import time
from pathlib import Path

import requests

ROOT = Path("/root/polyester-bot")
PROFILE = ROOT / "profile2"
CHROME = "/usr/bin/google-chrome"
PORT = int(os.getenv("CDP_PORT", "9333"))
CDP = f"http://127.0.0.1:{PORT}"
BASE = "https://testnet.polyester.com"
INJECT = (ROOT / "wallet_provider.js").read_text()


def log(*a):
    print(*a, flush=True)


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


def close_chrome():
    kill_existing()
