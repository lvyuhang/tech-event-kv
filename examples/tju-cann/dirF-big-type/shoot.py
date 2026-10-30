import base64,sys,subprocess,time
from playwright.sync_api import sync_playwright
srv=subprocess.Popen([sys.executable,'-m','http.server','8766'],cwd='/home/claude/tju-cann/hero3d',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
W,H=int(sys.argv[1]),int(sys.argv[2])
try:
 with sync_playwright() as p:
  b=p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
  pg=b.new_page(viewport={'width':W,'height':H}); pg.on('pageerror',lambda e:print('ERR',e)); pg.on('console',lambda m:print('c',m.text) if m.type=='error' else None)
  pg.goto(f'http://localhost:8766/scene.html?w={W}&h={H}'); pg.wait_for_function('window.DONE===true',timeout=600000)
  u=pg.evaluate("document.querySelector('canvas').toDataURL('image/png')"); open('hero.png','wb').write(base64.b64decode(u.split(',')[1])); print('ok')
finally: srv.kill()
