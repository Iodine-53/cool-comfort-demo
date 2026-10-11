"""og-image.jpg 1200x630 cropped from the hero. Run: cd ~/workspace/tampa-leads/demos/cool-comfort && python3 og.py"""
import subprocess, time, os, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8943
srv = subprocess.Popen(['python3','-m','http.server',str(PORT)], cwd=DIR,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.path.expanduser('~/workspace/.tools/chrome-linux64/chrome'),
                           args=['--no-sandbox','--force-device-scale-factor=1'])
    pg = br.new_page(viewport={'width':1440,'height':900})
    pg.goto(f'http://127.0.0.1:{PORT}/index.html', wait_until='networkidle')
    pg.wait_for_timeout(2800)
    pg.evaluate("""document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));
                   document.querySelectorAll('.hd,.mbar').forEach(e=>e.style.position='static');
                   window.scrollTo(0,0);""")
    pg.wait_for_timeout(500)
    shot = pg.screenshot()  # top 1440x900: doors + header + hero
    br.close()
srv.terminate()
im = Image.open(io.BytesIO(shot))
im = im.resize((1200, 750), Image.LANCZOS)      # keep aspect
top = (750 - 630) // 2
im = im.crop((0, top, 1200, top + 630))
im.save(os.path.join(DIR, 'og-image.jpg'), quality=88)
print('og-image.jpg', im.size)
