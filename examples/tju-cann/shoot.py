import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
here = Path(__file__).parent
out = Path(sys.argv[1] if len(sys.argv) > 1 else here / "out/kv_16x9.png"); out.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.on("pageerror", lambda e: print("err:", e))
    pg.goto((here / "kv.html").as_uri()); pg.wait_for_selector("body[data-ready='1']", state="attached")
    pg.wait_for_timeout(300)
    for bx in pg.evaluate("window.KV_BOXES"):
        name, l, t, r, bt = bx
        if l < 0 or t < 0 or r > 1920 or bt > 1080:
            print("  出画:", bx)
    pg.screenshot(path=str(out)); b.close()
print(out)
