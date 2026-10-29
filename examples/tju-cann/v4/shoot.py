import base64, sys, subprocess, time
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable,'-m','http.server','8765'],cwd='/home/claude/tju-cann/v4',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1)
W,H = (int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (2560,1440)
try:
  with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for ps in ['main','fg']:
      pg = b.new_page(viewport={'width':W,'height':H})
      pg.on('console', lambda m: print('console:', m.text) if m.type in ('error','warning') else None)
      pg.on('pageerror', lambda e: print('pageerror:', e))
      pg.goto(f'http://localhost:8765/scene.html?pass={ps}&w={W}&h={H}')
      pg.wait_for_function('window.DONE===true', timeout=600000)
      url = pg.evaluate("document.querySelector('canvas').toDataURL('image/png')")
      open(f'r_{ps}.png','wb').write(base64.b64decode(url.split(',')[1])); print('ok', ps)
    b.close()
finally: srv.kill()
