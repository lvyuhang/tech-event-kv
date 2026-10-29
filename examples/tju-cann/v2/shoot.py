import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
here = Path(__file__).parent
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
qs = sys.argv[2] if len(sys.argv) > 2 else ""
W, H = 1920, 1080
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for mode in (0, 1):
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.on("console", lambda m: print("console:", m.text)); pg.on("pageerror", lambda e: print("err:", e))
        t = time.time()
        pg.goto((here / "scene.html").as_uri() + f"?w={W}&h={H}&mode={mode}&tex=6144&{qs}")
        pg.wait_for_selector("body[data-done='1']", state="attached", timeout=900000)
        pg.locator("#gl").screenshot(path=str(out / ("color.png" if mode == 0 else "depth.png")))
        if mode == 0 and "tex" in sys.argv:
            data = pg.evaluate("TEX.toDataURL('image/jpeg', 0.85)")
            import base64; (out / "tex.jpg").write_bytes(base64.b64decode(data.split(",")[1]))
        print(mode, f"{time.time()-t:.1f}s"); pg.close()
    b.close()
