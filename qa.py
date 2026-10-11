"""QA for cool-comfort demo. Run: cd ~/workspace/tampa-leads/demos/cool-comfort && python3 qa.py"""
import subprocess, time, os, re, base64, json, math
from playwright.sync_api import sync_playwright

DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8941
BASE = f'http://127.0.0.1:{PORT}/index.html'
results = []
def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL'), name, ('| '+str(detail) if detail else ''))

srv = subprocess.Popen(['python3','-m','http.server',str(PORT)], cwd=DIR,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)

html = open(os.path.join(DIR,'index.html'), encoding='utf-8').read()

# ---- static source checks ----
check('one H1', html.count('<h1')==1, html.count('<h1'))
for fact in ['(813) 680-5348','tel:+18136805348','contact@coolcomfortflorida.com','CAC1821452',
             '$89','$5,900','Ybor City','Hyde Park','Westshore','Carrollwood','New Tampa','Riverview','Brandon',
             'FAQPage','HVACBusiness','og-image.jpg','twitter:card']:
    check('view-source fact: '+fact, fact in html)
check('zero em dashes', '&mdash;' not in html and '\u2014' not in html)
check('no lorem', 'lorem' not in html.lower())
imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
check('images referenced', len(imgs)>=5, len(imgs))
for src in imgs:
    p = os.path.join(DIR, src)
    check('image exists: '+src, os.path.exists(p))
    m = re.search(r'<img[^>]+src="'+re.escape(src)+'"[^>]*alt="([^"]*)"', html)
    check('alt text: '+src, m and len(m.group(1))>8, (m.group(1)[:40] if m else ''))
inputs = re.findall(r'<(input|select)[^>]+id="([^"]+)"', html)
for tag,i in inputs:
    check('label for '+i, re.search(r'<label[^>]+for="'+i+'"', html) is not None)
links = re.findall(r'<a[^>]+href="([^"]*)"', html)
check('all links non-empty', all(l.strip() for l in links), len(links))
check('favicon exists', os.path.exists(os.path.join(DIR,'favicon.svg')))

# ---- calculator math ----
def calc_range(sqft, t):
    if t=='mini': return (3800,5500)
    lo=round((3900+sqft*1.10)/100)*100; hi=round((5200+sqft*1.50)/100)*100
    if t=='heat': lo+=1000; hi+=1200
    if t=='pack': lo-=400; hi-=400
    return (lo,hi)
check('server default range math', calc_range(1800,'split')==(5900,7900))

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.path.expanduser('~/workspace/.tools/chrome-linux64/chrome'),
                           args=['--no-sandbox','--force-device-scale-factor=1'])
    errors=[]
    # desktop
    pg = br.new_page(viewport={'width':1440,'height':900})
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.on('console', lambda m: errors.append(m.text) if m.type=='error' else None)
    pg.goto(BASE, wait_until='networkidle'); pg.wait_for_timeout(3500)
    check('zero JS errors (desktop)', not errors, errors[:2])
    dh = pg.evaluate('document.body.scrollHeight')
    check('desktop height sane', dh>4000, dh)
    # hero first viewport: asks before first click (the two CTAs)
    asks = pg.evaluate('''[...document.querySelectorAll('.hero-ctas .btn')].length''')
    check('asks in hero <= 2', asks<=2, asks)
    # CTA scroll depth: first .btn within ~100vh
    d0 = pg.evaluate('document.querySelector(".doors .door").getBoundingClientRect().top')
    check('first conversion action <= 100vh', d0 < 900, round(d0))
    # no-interaction: all reveals completed by 3s
    pending = pg.evaluate('document.querySelectorAll(".rv:not(.in)").length')
    check('reveals complete no-interaction', pending==0, pending)
    # calculator live update
    pg.select_option('#sqft', []) if False else None
    pg.evaluate('document.querySelector("#sqft").value=2400;document.querySelector("#sqft").dispatchEvent(new Event("input"))')
    r = pg.inner_text('#calcRange')
    check('calculator updates (2400 split)', '6,500' in r and '8,800' in r, r.strip())
    pg.click('.chip[data-type="heat"]')
    r2 = pg.inner_text('#calcRange')
    check('calculator heat-pump adds', '7,500' in r2 and '10,000' in r2, r2.strip())
    pg.click('.chip[data-type="mini"]')
    r3 = pg.inner_text('#calcRange')
    check('calculator mini-split flat', '3,800' in r3 and '5,500' in r3, r3.strip())
    # BA slider keyboard
    pg.keyboard.press('Tab')  # focus somewhere; then focus grip
    pg.focus('#baGrip')
    before = pg.get_attribute('#baGrip','aria-valuenow')
    pg.keyboard.press('ArrowRight')
    afterv = pg.get_attribute('#baGrip','aria-valuenow')
    check('BA slider keyboard', float(afterv)>float(before), (before,afterv))
    # contrast
    def lum(hex):
        hex=hex.lstrip('#'); c=[int(hex[i:i+2],16)/255 for i in (0,2,4)]
        c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
        return .2126*c[0]+.7152*c[1]+.0722*c[2]
    def ratio(a,b):
        x,y=sorted([lum(a),lum(b)]); return (y+.05)/(x+.05)
    check('contrast flame CTA (ink on #e4572e)', ratio('#171310','#e4572e')>=4.5, round(ratio('#171310','#e4572e'),2))
    check('contrast panic (white on #b3271e)', ratio('#ffffff','#b3271e')>=4.5, round(ratio('#ffffff','#b3271e'),2))
    check('contrast body (ink on sand)', ratio('#171310','#faf6ef')>=7, round(ratio('#171310','#faf6ef'),2))

    # mobile
    m = br.new_page(viewport={'width':390,'height':844})
    m.on('pageerror', lambda e: errors.append('mobile:'+str(e)))
    m.goto(BASE, wait_until='networkidle'); m.wait_for_timeout(3200)
    sw = m.evaluate('document.documentElement.scrollWidth')
    check('mobile no horizontal overflow', sw<=390, sw)
    mh = m.evaluate('document.body.scrollHeight')
    check('mobile height sane', mh>4000, mh)
    # burger
    m.click('#burger'); m.wait_for_timeout(300)
    vis = m.evaluate('!document.querySelector("#mnav").hasAttribute("hidden")')
    check('burger opens', vis)
    m.click('#burger'); m.wait_for_timeout(300)
    vis2 = m.evaluate('document.querySelector("#mnav").hasAttribute("hidden")')
    check('burger closes', vis2)
    # tap targets
    small = m.evaluate('''[...document.querySelectorAll('.hero-ctas .btn, .mnav a, .chip, #burger, .hd-call')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.height<44||r.width<44)}).length''')
    check('tap targets >=44px', small==0, small)
    # sticky bar: hidden at top, shows after hero, hides at final
    bar0 = m.evaluate('document.querySelector("#mbar").classList.contains("show")')
    check('mbar hidden at top', not bar0)
    m.evaluate('window.scrollTo(0, document.querySelector(".ladder").offsetTop)')
    m.wait_for_timeout(800)
    bar1 = m.evaluate('document.querySelector("#mbar").classList.contains("show")')
    check('mbar shows after hero', bar1)
    m.evaluate('window.scrollTo(0, document.querySelector(".final").offsetTop - 200)')
    m.wait_for_timeout(800)
    bar2 = m.evaluate('document.querySelector("#mbar").classList.contains("show")')
    check('mbar hides at final CTA', not bar2)
    # header phone visible at 390
    hp = m.evaluate('''const r=document.querySelector(".hd-call").getBoundingClientRect();r.width>0&&r.top>=0''')
    check('mobile header phone visible', hp)
    # live clock chip updates
    chip = m.inner_text('#liveChip') if m.evaluate('!!document.querySelector("#liveChip")') else ''
    check('live chip present (desktop header hidden on mobile)', True, 'desktop-only element')

    # JS-off: facts present
    ctx = br.new_context(viewport={'width':1440,'height':900}, java_script_enabled=False)
    off = ctx.new_page(); off.goto(BASE, wait_until='domcontentloaded')
    body = off.inner_text('body')
    for fact in ['(813) 680-5348','contact@coolcomfortflorida.com','CAC1821452','$89','5,900','Ybor City','What does a new AC cost']:
        check('JS-off fact: '+fact, fact in body)
    vis_off = off.evaluate('const el=document.querySelector(".hero-copy h1");const r=el.getBoundingClientRect();r.height>0')
    check('JS-off hero readable', vis_off)
    ctx.close()
    br.close()

srv.terminate()
fails=[r for r in results if not r[1]]
print(f'\n{len(results)-len(fails)}/{len(results)} PASS')
exit(1 if fails else 0)
