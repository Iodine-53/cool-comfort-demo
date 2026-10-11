"""Screenshots for cool-comfort demo. Run: cd ~/workspace/tampa-leads/demos/cool-comfort && python3 shoot.py"""
import subprocess, time, os, base64
from playwright.sync_api import sync_playwright

DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8942
OUT_CRIT = os.path.expanduser('~/workspace/goals/tampa-demo-first-cold-pitch/hidden_files/critique-2026-10-10')
os.makedirs(OUT_CRIT, exist_ok=True)

srv = subprocess.Popen(['python3','-m','http.server',str(PORT)], cwd=DIR,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
base = f'http://127.0.0.1:{PORT}/index.html'

def capture(pg, w, h, path):
    cdp = pg.context.new_cdp_session(pg)
    pg.set_viewport_size({'width': w, 'height': h})
    pg.goto(base, wait_until='networkidle')
    # scroll through so lazy images load
    pg.evaluate("""(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,90))}})()""")
    pg.wait_for_timeout(1500)
    # force reveals on, un-stick chrome for clean full-page capture
    pg.evaluate("""document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));
                   document.querySelectorAll('.hd,.mbar,.mnav,.doors').forEach(e=>e.style.position='static');
                   window.scrollTo(0,0);""")
    pg.wait_for_timeout(600)
    # verify lazy images loaded
    n = pg.evaluate('[...document.querySelectorAll("img")].filter(i=>i.complete&&i.naturalWidth>0).length')
    print('images loaded:', n, 'of', pg.evaluate('document.querySelectorAll("img").length'))
    shot = cdp.send('Page.captureScreenshot', {'format':'png','captureBeyondViewport':True,'fromSurface':True})
    with open(path, 'wb') as f:
        f.write(base64.b64decode(shot['data']))
    print('saved', path)

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.path.expanduser('~/workspace/.tools/chrome-linux64/chrome'),
                           args=['--no-sandbox','--force-device-scale-factor=1'])
    pg = br.new_page()
    pg.set_viewport_size({'width':1440,'height':900}); pg.goto(base, wait_until='networkidle'); pg.wait_for_timeout(2500)
    dh = pg.evaluate('document.body.scrollHeight')
    pg.set_viewport_size({'width':390,'height':844}); pg.wait_for_timeout(1200)
    mh = pg.evaluate('document.body.scrollHeight')
    print('desktop h', dh, 'mobile h', mh)
    capture(pg, 1440, dh, os.path.join(OUT_CRIT, 'cool-comfort-desktop.png'))
    capture(pg, 390, mh, os.path.join(OUT_CRIT, 'cool-comfort-mobile.png'))
    br.close()
srv.terminate()
print('done')
