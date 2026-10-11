/* Cool Comfort demo: operable price instrument, BA slider, live clock, sticky bar, reveals, mailto form */
(function(){
"use strict";
var $=function(s,c){return (c||document).querySelector(s)};
var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- live Tampa-time presence chip ---------- */
var chip=$('#liveChip');
function tick(){
  if(!chip)return;
  try{
    var now=new Date();
    var parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit',hour12:true}).formatToParts(now);
    var hr=parseInt(parts.filter(function(p){return p.type==='hour'})[0].value,10);
    var ap=parts.filter(function(p){return p.type==='dayPeriod'})[0].value;
    var h24=hr%12+(ap==='PM'?12:0); if(ap==='AM'&&hr===12)h24=0;
    var t=parts.filter(function(p){return p.type==='hour'})[0].value+':'+parts.filter(function(p){return p.type==='minute'})[0].value+' '+ap+' ET';
    if(h24>=7&&h24<22){chip.innerHTML='<span class="open">OPEN NOW</span> &middot; '+t;}
    else{chip.textContent='OPENS 7 AM ET';}
  }catch(e){chip.textContent='7 AM\u201310 PM DAILY';}
}
tick();setInterval(tick,30000);

/* ---------- THE NUMBER FIRST: replacement-cost instrument ---------- */
var sqft=$('#sqft'),out=$('#sqftOut'),range=$('#calcRange'),note=$('#calcNote');
var curType='split';
var NOTES={split:'split system \u00B7 15 SEER2',heat:'heat pump \u00B7 16 SEER2 \u00B7 cools + heats',pack:'package unit \u00B7 15 SEER2 \u00B7 all-in-one cabinet',mini:'ductless mini-split \u00B7 one zone'};
function r100(n){return Math.round(n/100)*100}
function fmt(n){return n.toLocaleString('en-US')}
function calc(){
  var s=parseInt(sqft.value,10);
  out.textContent=s.toLocaleString('en-US')+' sq ft';
  var lo,hi;
  if(curType==='mini'){lo=3800;hi=5500;}
  else{
    lo=r100(3900+s*1.10);hi=r100(5200+s*1.50);
    if(curType==='heat'){lo+=1000;hi+=1200;}
    if(curType==='pack'){lo-=400;hi-=400;}
  }
  range.innerHTML='<span class="cur">$</span>'+fmt(lo)+'\u2013'+fmt(hi);
  var approx=curType==='mini'?'covers one room, most homes need 2+':'~'+fmt(s)+' sq ft';
  note.textContent=approx+' \u00B7 '+NOTES[curType]+(curType==='mini'?'':' \u00B7 installed, permitted, hauled away');
}
if(sqft){
  sqft.addEventListener('input',calc);
  $$('.chip').forEach(function(c){
    c.addEventListener('click',function(){
      $$('.chip').forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false')});
      c.classList.add('on');c.setAttribute('aria-pressed','true');
      curType=c.getAttribute('data-type');calc();
    });
  });
  calc();
}

/* ---------- before/after slider (Nielsen rules: grip, labels, 50%, keyboard) ---------- */
var view=$('.ba-view'),grip=$('#baGrip'),after=$('.ba-after');
function setPos(p){
  p=Math.max(2,Math.min(98,p));
  if(after)after.style.width=p+'%';
  if(grip){grip.style.left=p+'%';grip.setAttribute('aria-valuenow',Math.round(p));}
  var img=$('.ba-after img');
  if(img&&view)img.style.width=view.clientWidth+'px';
}
if(view&&grip){
  setPos(50);
  var drag=false;
  function fromEvent(e){
    var r=view.getBoundingClientRect();
    var x=(e.touches&&e.touches[0]?e.touches[0].clientX:e.clientX)-r.left;
    setPos(x/r.width*100);
  }
  grip.addEventListener('pointerdown',function(e){drag=true;grip.setPointerCapture(e.pointerId);e.preventDefault()});
  grip.addEventListener('pointermove',function(e){if(drag)fromEvent(e)});
  grip.addEventListener('pointerup',function(){drag=false});
  grip.addEventListener('pointercancel',function(){drag=false});
  view.addEventListener('click',function(e){if(e.target!==grip&&!grip.contains(e.target))fromEvent(e)});
  grip.addEventListener('keydown',function(e){
    var cur=parseFloat(grip.getAttribute('aria-valuenow'))||50;
    if(e.key==='ArrowLeft'){setPos(cur-5);e.preventDefault()}
    if(e.key==='ArrowRight'){setPos(cur+5);e.preventDefault()}
  });
  window.addEventListener('resize',function(){setPos(parseFloat(grip.getAttribute('aria-valuenow'))||50)});
}

/* ---------- mobile menu ---------- */
var burger=$('#burger'),mnav=$('#mnav');
if(burger&&mnav){
  burger.addEventListener('click',function(){
    var open=mnav.hasAttribute('hidden');
    if(open){mnav.removeAttribute('hidden');burger.setAttribute('aria-expanded','true');burger.setAttribute('aria-label','Close menu')}
    else{mnav.setAttribute('hidden','');burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label','Open menu')}
  });
  $$('#mnav a').forEach(function(a){a.addEventListener('click',function(){mnav.setAttribute('hidden','');burger.setAttribute('aria-expanded','false')})});
}

/* ---------- sticky bottom bar: after hero, hides at final CTA ---------- */
var mbar=$('#mbar'),hero=$('.hero'),final=$('.final');
if(mbar&&hero){
  var pastHero=false,atFinal=false;
  function upd(){
    if(pastHero&&!atFinal)mbar.classList.add('show');else mbar.classList.remove('show');
    if(atFinal)mbar.classList.add('final-in');else mbar.classList.remove('final-in');
  }
  if('IntersectionObserver'in window){
    new IntersectionObserver(function(es){pastHero=!es[0].isIntersecting&&es[0].boundingClientRect.top<0;upd()}).observe(hero);
    if(final)new IntersectionObserver(function(es){atFinal=es[0].isIntersecting;upd()},{threshold:.15}).observe(final);
  }else{
    window.addEventListener('scroll',function(){pastHero=window.scrollY>hero.offsetHeight*.6;upd()},{passive:true});
  }
}

/* ---------- reveals: blur-to-sharp, one-shot, no-interaction fallback ---------- */
var targets=$$('h1, h2, .eyebrow, .calc, .panic-in, figure, .cell, .tier, .stat, details, .ba-proof');
targets.forEach(function(el){el.classList.add('rv')});
function revealAll(){targets.forEach(function(el){el.classList.add('in')})}
if(reduced){revealAll();}
else if('IntersectionObserver'in window){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}});
  },{threshold:.12});
  targets.forEach(function(el){io.observe(el)});
  setTimeout(revealAll,3000); /* no-interaction fallback: everything readable by 3s */
}else{revealAll()}

/* ---------- estimate form: mailto handoff, nothing stored ---------- */
var form=$('#qform');
if(form){
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var n=$('#qname').value.trim(),p=$('#qphone').value.trim(),s=$('#qsymptom').value;
    var body='Name: '+n+'\nPhone: '+p+'\nWhat is going on: '+s+'\n\nSent from the Cool Comfort demo website.';
    window.location.href='mailto:contact@coolcomfortflorida.com?subject='+encodeURIComponent('Written quote request (demo site)')+'&body='+encodeURIComponent(body);
  });
}
})();
