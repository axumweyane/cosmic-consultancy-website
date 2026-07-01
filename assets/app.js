/* ============================================================
   CCS shared app script
   ============================================================ */
(function(){
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.matchMedia('(max-width: 768px)').matches;

  /* ---------- i18n ---------- */
  const LANGS = {en:{label:'English',native:'English'}, es:{label:'Español',native:'Español'}, ti:{label:'Tigrinya',native:'ትግርኛ'}};
  function getLang(){ return localStorage.getItem('ccs_lang') || 'en'; }
  function applyLang(lang){
    const dict = (window.CCS_I18N && window.CCS_I18N[lang]) || {};
    document.querySelectorAll('[data-i18n]').forEach(el=>{
      const key = el.getAttribute('data-i18n');
      if(dict[key] != null) el.textContent = dict[key];
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
      const key = el.getAttribute('data-i18n-ph');
      if(dict[key] != null) el.setAttribute('placeholder', dict[key]);
    });
    document.documentElement.lang = lang;
    document.documentElement.dir = 'ltr'; // Tigrinya (Ge'ez script) is left-to-right
    localStorage.setItem('ccs_lang', lang);
    const cur = document.getElementById('lang-current');
    if(cur) cur.textContent = lang.toUpperCase();
    document.querySelectorAll('.lang-menu button').forEach(b=>{
      b.classList.toggle('sel', b.dataset.lang === lang);
    });
  }
  window.CCS_applyLang = applyLang;

  document.addEventListener('DOMContentLoaded', ()=>{
    applyLang(getLang());

    const langBtn = document.getElementById('lang-btn');
    const langMenu = document.getElementById('lang-menu');
    if(langBtn && langMenu){
      langBtn.addEventListener('click', e=>{ e.stopPropagation(); langMenu.classList.toggle('open'); });
      document.addEventListener('click', ()=> langMenu.classList.remove('open'));
      langMenu.querySelectorAll('button').forEach(b=>{
        b.addEventListener('click', ()=>{ applyLang(b.dataset.lang); langMenu.classList.remove('open'); });
      });
    }

    /* mobile menu */
    const toggle = document.getElementById('mtoggle');
    const links = document.getElementById('nav-links');
    if(toggle && links){
      toggle.addEventListener('click', ()=>{ toggle.classList.toggle('open'); links.classList.toggle('open'); });
      links.querySelectorAll('a').forEach(a=> a.addEventListener('click', ()=>{ toggle.classList.remove('open'); links.classList.remove('open'); }));
    }
  });

  /* ---------- nav scroll ---------- */
  const nav = document.getElementById('nav');
  if(nav) window.addEventListener('scroll', ()=> nav.classList.toggle('scrolled', window.scrollY > 40), {passive:true});

  /* ---------- THREE.JS hero (home only) ---------- */
  function initHero(){
    const canvas = document.getElementById('hero-canvas');
    if(!canvas || !window.THREE) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.z = 6;
    const renderer = new THREE.WebGLRenderer({canvas, alpha:true, antialias:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    const BLUE = 0x5BAEDC, BLUE_LT = 0xA8D8F0;
    const detail = isMobile ? 1 : 2;
    const geo = new THREE.IcosahedronGeometry(2.1, detail);
    const sphere = new THREE.LineSegments(new THREE.WireframeGeometry(geo), new THREE.LineBasicMaterial({color:BLUE, transparent:true, opacity:0.55}));
    scene.add(sphere);
    const lineMat = sphere.material;
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({color:BLUE_LT, size:0.06, transparent:true, opacity:0.9}));
    scene.add(pts);
    function ring(r, tilt){
      const m = new THREE.Mesh(new THREE.RingGeometry(r-0.008, r+0.008, 128), new THREE.MeshBasicMaterial({color:BLUE, side:THREE.DoubleSide, transparent:true, opacity:0.35}));
      m.rotation.x = tilt; return m;
    }
    const ringGroup = new THREE.Group();
    ringGroup.add(ring(3.0, Math.PI/2.4)); ringGroup.add(ring(3.5, Math.PI/1.8));
    ringGroup.rotation.z = 0.3; scene.add(ringGroup);
    const starCount = isMobile ? 700 : 1400;
    const starGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(starCount*3);
    for(let i=0;i<starCount;i++){
      const r=8+Math.random()*14, theta=Math.random()*Math.PI*2, phi=Math.acos(2*Math.random()-1);
      positions[i*3]=r*Math.sin(phi)*Math.cos(theta); positions[i*3+1]=r*Math.sin(phi)*Math.sin(theta); positions[i*3+2]=r*Math.cos(phi);
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(positions,3));
    const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({color:BLUE_LT, size:0.05, transparent:true, opacity:0.7}));
    scene.add(stars);
    let mx=0,my=0,tx=0,ty=0;
    if(!isMobile) window.addEventListener('mousemove', e=>{ mx=(e.clientX/window.innerWidth-0.5); my=(e.clientY/window.innerHeight-0.5); }, {passive:true});
    const clock = new THREE.Clock(); let visible=true;
    document.addEventListener('visibilitychange', ()=>{ visible=!document.hidden; });
    function animate(){
      requestAnimationFrame(animate);
      if(!visible) return;
      const t = clock.getElapsedTime();
      if(!reduceMotion){
        sphere.rotation.y=t*0.12; sphere.rotation.x=t*0.05; pts.rotation.copy(sphere.rotation);
        ringGroup.rotation.y=t*0.18; stars.rotation.y=t*0.015; lineMat.opacity=0.55+Math.sin(t*1.2)*0.12;
      }
      tx+=(mx-tx)*0.04; ty+=(my-ty)*0.04; camera.position.x=tx*1.2; camera.position.y=-ty*1.2; camera.lookAt(0,0,0);
      renderer.render(scene, camera);
    }
    animate();
    if(!reduceMotion && window.ScrollTrigger){
      gsap.to(sphere.scale, {x:0.6,y:0.6,z:0.6, scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1}});
      gsap.to(camera.position, {z:9, scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1}});
    }
    window.addEventListener('resize', ()=>{ camera.aspect=window.innerWidth/window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); }, {passive:true});
  }

  /* ---------- GSAP reveals + counters ---------- */
  function initMotion(){
    if(!window.gsap || !window.ScrollTrigger) return;
    gsap.registerPlugin(ScrollTrigger);
    if(!reduceMotion && document.querySelector('.hero h1')){
      gsap.from('.eyebrow',{y:24,opacity:0,duration:.8,delay:.2,ease:'power3.out'});
      gsap.from('.hero h1',{y:36,opacity:0,duration:1,delay:.35,ease:'power3.out'});
      gsap.from('.hero p.lead',{y:24,opacity:0,duration:.8,delay:.6,ease:'power3.out'});
      gsap.from('.hero .creds',{y:20,opacity:0,duration:.8,delay:.75,ease:'power3.out'});
      gsap.from('.hero-cta',{y:24,opacity:0,duration:.8,delay:.9,ease:'power3.out'});
    }
    gsap.utils.toArray('.reveal').forEach(el=> gsap.to(el,{opacity:1,y:0,duration:.9,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 90%'}}));
    ScrollTrigger.batch('.card',{start:'top 92%',onEnter:b=>gsap.to(b,{opacity:1,y:0,stagger:0.08,duration:.7,ease:'power3.out'})});
    ScrollTrigger.batch('.step,.ind,.case-item,.cap,.member',{start:'top 92%',onEnter:b=>gsap.to(b,{opacity:1,y:0,stagger:0.08,duration:.7,ease:'power3.out'})});

    function runCounter(el){
      if(!el.dataset.target) return;
      const target=+el.dataset.target, suffix=el.dataset.suffix||'';
      const valEl=el.querySelector('.val'), sufEl=el.querySelector('.suf');
      if(!valEl) return; if(sufEl) sufEl.textContent=suffix;
      if(reduceMotion){ valEl.textContent=target; return; }
      const obj={n:0}; gsap.to(obj,{n:target,duration:1.8,ease:'power2.out',onUpdate:()=>valEl.textContent=Math.round(obj.n)});
    }
    const stats = document.querySelector('.stats');
    if(stats) ScrollTrigger.create({trigger:stats,start:'top 85%',once:true,onEnter:()=>stats.querySelectorAll('.stat .num').forEach(runCounter)});
  }

  /* ---------- card tilt ---------- */
  function initTilt(){
    if(isMobile || reduceMotion) return;
    document.querySelectorAll('[data-tilt]').forEach(card=>{
      const max=10;
      card.addEventListener('mousemove', e=>{
        const r=card.getBoundingClientRect(); const px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
        card.style.transform=`perspective(900px) rotateX(${(py-0.5)*-2*max}deg) rotateY(${(px-0.5)*2*max}deg) translateY(-6px)`;
        card.style.setProperty('--mx',px*100+'%'); card.style.setProperty('--my',py*100+'%');
      });
      card.addEventListener('mouseleave', ()=>{ card.style.transform='perspective(900px) rotateX(0) rotateY(0) translateY(0)'; });
    });
  }

  /* ---------- contact form ---------- */
  function initForm(){
    const form = document.getElementById('contact-form');
    if(!form) return;
    const btn=document.getElementById('submit-btn'), spinner=document.getElementById('spinner');
    const label=btn.querySelector('.btn-label'), successPanel=document.getElementById('form-success');
    const consentWrap=document.getElementById('consent-wrap'), consentErr=document.getElementById('consent-err');
    const emailRe=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const fieldOf=i=>i.closest('.field');
    const setInvalid=(i,bad)=>{ const f=fieldOf(i); if(f) f.classList.toggle('invalid',bad); };
    function validate(){
      let ok=true;
      const nameBad=!form.name.value.trim(); setInvalid(form.name,nameBad); if(nameBad)ok=false;
      const emailBad=!emailRe.test(form.email.value.trim()); setInvalid(form.email,emailBad); if(emailBad)ok=false;
      const serviceBad=!form.service.value; setInvalid(form.service,serviceBad); if(serviceBad)ok=false;
      const msgBad=form.message.value.trim().length<10; setInvalid(form.message,msgBad); if(msgBad)ok=false;
      const consentBad=!form.consent.checked; consentWrap.classList.toggle('invalid',consentBad);
      if(consentErr) consentErr.style.display=consentBad?'block':'none'; if(consentBad)ok=false;
      return ok;
    }
    ['name','email','service','message'].forEach(n=>{
      const ev = (n==='service')?'change':'input';
      form[n].addEventListener(ev, ()=>{ if(fieldOf(form[n]).classList.contains('invalid')){
        if(n==='email') setInvalid(form[n],!emailRe.test(form[n].value.trim()));
        else if(n==='message') setInvalid(form[n],form[n].value.trim().length<10);
        else setInvalid(form[n],!form[n].value.trim());
      }});
    });
    form.consent.addEventListener('change', ()=>{ if(form.consent.checked){ consentWrap.classList.remove('invalid'); if(consentErr)consentErr.style.display='none'; }});
    form.addEventListener('submit', async e=>{
      e.preventDefault();
      if(!validate()){ const fb=form.querySelector('.field.invalid input,.field.invalid select,.field.invalid textarea,.consent.invalid input'); if(fb)fb.focus(); return; }
      const key=form.access_key.value;
      if(!key || key.indexOf('YOUR_WEB3FORMS')===0){
        /* No Web3Forms key set — fall back to the visitor's email client */
        const d=Object.fromEntries(new FormData(form).entries());
        const nl='%0D%0A';
        const body='Name: '+(d.name||'')+nl+'Email: '+(d.email||'')+nl+'Company: '+(d.company||'')+nl+'Service: '+(d.service||'')+nl+'Budget: '+(d.budget||'')+nl+nl+encodeURIComponent(d.message||'');
        const subj=encodeURIComponent('Consultation request — '+(d.name||'website'));
        window.location.href='mailto:info@cosmicconsultancyservices.com?subject='+subj+'&body='+body;
        form.style.display='none'; successPanel.classList.add('show'); successPanel.scrollIntoView({behavior:'smooth',block:'center'});
        return;
      }
      btn.disabled=true; label.textContent='Sending…'; spinner.style.display='inline-block';
      try{
        const data=Object.fromEntries(new FormData(form).entries());
        const res=await fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
        const json=await res.json();
        if(json.success){ form.style.display='none'; successPanel.classList.add('show'); successPanel.scrollIntoView({behavior:'smooth',block:'center'}); }
        else throw new Error(json.message||'failed');
      }catch(err){ btn.disabled=false; label.textContent='Send message'; spinner.style.display='none';
        alert('Something went wrong. Please email us directly at info@cosmicconsultancyservices.com — or try again shortly.'); }
    });
  }

  /* init after libs load */
  window.addEventListener('load', ()=>{ initHero(); initMotion(); initTilt(); initForm(); });
})();
