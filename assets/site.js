(function(){
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  /* ---------- theme ---------- */
  var root=document.documentElement;
  try{ var saved=localStorage.getItem('gx-theme'); if(saved) root.setAttribute('data-theme',saved); }catch(e){}
  var tb=$('#themeBtn');
  if(tb) tb.addEventListener('click',function(){
    var next = root.getAttribute('data-theme')==='dark' ? 'light':'dark';
    root.setAttribute('data-theme',next);
    try{ localStorage.setItem('gx-theme',next); }catch(e){}
  });

  /* ---------- sticky nav shadow ---------- */
  var nav=$('header.nav');
  if(nav) window.addEventListener('scroll',function(){
    nav.classList.toggle('stuck', window.scrollY>8);
  },{passive:true});

  /* ---------- mega menu ---------- */
  var megaTab=$('.tab.has-mega'), mega=$('#mega'), megaT;
  function openMega(v){ if(mega) mega.classList.toggle('open',v); }
  if(megaTab&&mega){
    var row=$('.tabrow');
    row.addEventListener('mouseenter',function(e){ if(e.target.closest('.has-mega')){clearTimeout(megaT);openMega(true);} },true);
    row.addEventListener('mouseleave',function(){ megaT=setTimeout(function(){openMega(false);},180); });
    mega.addEventListener('mouseenter',function(){clearTimeout(megaT);});
    mega.addEventListener('mouseleave',function(){ megaT=setTimeout(function(){openMega(false);},180); });
    megaTab.addEventListener('focus',function(){openMega(true);});
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') openMega(false); });
  }

  /* ---------- scroll reveal ---------- */
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  $$('.reveal').forEach(function(el){io.observe(el);});

  /* ---------- animated counters ---------- */
  function animateNum(el){
    var target=parseFloat(el.getAttribute('data-to')||'0');
    var dec=parseInt(el.getAttribute('data-dec')||'0',10);
    var sep=el.getAttribute('data-sep')!=='0';
    function fmt(v){var t=v.toFixed(dec);return sep?t.replace(/\B(?=(\d{3})+(?!\d))/g,','):t;}
    var dur=RM?0:1500, t0=null;
    function step(ts){
      if(!t0) t0=ts;
      var p=Math.min((ts-t0)/dur,1);
      var eased=1-Math.pow(1-p,3);
      el.textContent=fmt(target*eased);
      if(p<1) requestAnimationFrame(step);
    }
    if(RM){ el.textContent=fmt(target); return; }
    requestAnimationFrame(step);
  }
  var cio=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('in');
        $$('[data-to]',e.target).forEach(animateNum);
        cio.unobserve(e.target);
      }
    });
  },{threshold:.4});
  $$('.stat, .uicard').forEach(function(el){cio.observe(el);});

  /* ---------- hero UI card bars ---------- */
  var hio=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        $$('.uc-bar i',e.target).forEach(function(b){
          setTimeout(function(){ b.style.width=b.getAttribute('data-w')||'60%'; },220);
        });
        hio.unobserve(e.target);
      }
    });
  },{threshold:.3});
  $$('.uicard').forEach(function(el){hio.observe(el);});

  /* ---------- expanding ledger + accordions ---------- */
  function toggleCollapse(btn, row, body){
    var open=row.classList.contains('open');
    if(open){ body.style.maxHeight='0px'; row.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }
    else{ body.style.maxHeight=body.scrollHeight+40+'px'; row.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
  }
  $$('.lhead').forEach(function(btn){
    var row=btn.closest('.lrow'), body=$('.lbody',row);
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',function(){ toggleCollapse(btn,row,body); });
  });
  $$('.acc-btn').forEach(function(btn){
    var item=btn.closest('.acc-item'), body=$('.acc-body',item);
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',function(){ toggleCollapse(btn,item,body); });
  });

  /* ---------- product tour tabs ---------- */
  $$('.tour').forEach(function(tour){
    var btns=$$('.tour-nav button',tour), panels=$$('.tour-panel',tour);
    btns.forEach(function(b,i){
      b.addEventListener('click',function(){
        btns.forEach(function(x){x.setAttribute('aria-selected','false');});
        panels.forEach(function(p){p.classList.remove('active');});
        b.setAttribute('aria-selected','true');
        panels[i].classList.add('active');
      });
    });
  });

  /* ---------- before / after slider ---------- */
  $$('.ba').forEach(function(ba){
    var input=$('.ba-input',ba), pane=$('.ba-pane',ba);
    function set(v){ pane.style.setProperty('--pos', v+'%'); $('.ba-handle',ba).style.left=v+'%'; }
    if(input){
      set(input.value);
      input.addEventListener('input',function(){ set(input.value); });
    }
  });

  /* ---------- testimonial carousel ---------- */
  $$('.carou').forEach(function(c){
    var slides=$$('.slide',c), dots=$$('.dot',c), i=0, timer=null, playing=true;
    var pause=$('.carou-pause',c);
    function show(n){
      i=(n+slides.length)%slides.length;
      slides.forEach(function(s,k){s.classList.toggle('active',k===i);});
      dots.forEach(function(d,k){d.setAttribute('aria-selected',k===i?'true':'false');});
    }
    function start(){ if(RM||slides.length<2) return; stop(); timer=setInterval(function(){show(i+1);},5200); playing=true; if(pause)pause.textContent='Pause'; }
    function stop(){ if(timer)clearInterval(timer); timer=null; }
    dots.forEach(function(d,k){ d.addEventListener('click',function(){ show(k); start(); }); });
    if(pause) pause.addEventListener('click',function(){
      if(playing){ stop(); playing=false; pause.textContent='Play'; } else { start(); }
    });
    c.addEventListener('mouseenter',stop);
    c.addEventListener('mouseleave',function(){ if(playing) start(); });
    show(0); start();
  });

  /* ---------- cursor-aware route cards ---------- */
  if(!RM) $$('.route').forEach(function(el){
    el.addEventListener('mousemove',function(e){
      var r=el.getBoundingClientRect();
      el.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
      el.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
    });
  });

  /* ---------- solution chooser ---------- */
  var recData={
    emr:{pk:'Recommended \u00b7 1 to 20 beds',h:'Genesys EMR',p:'A clean clinical record at the centre of a small practice, with mid-level automation across the areas you run. Simple enough to operate without an IT department.'},
    clinical:{pk:'Recommended \u00b7 20 to 100 beds',h:'Clinical Specialized Packages',p:'Targeted automation that brings the functions you already part-run up to one standard, without replacing everything at once.'},
    hmis:{pk:'Recommended \u00b7 100 to 500 beds',h:'Genesys HMIS',p:'The ERP-class system: records, finance, pharmacy, laboratory, claims and wards automated across every department on one spine.'},
    standalone:{pk:'Recommended \u00b7 Not a hospital',h:'Stand-alone Packages',p:'Built for labs, pharmacies and imaging centres in the healthcare ecosystem that do not fit routine hospital or clinic classification.'}
  };
  var rec=$('#rec');
  if(rec){
    var sbtns=$$('.scale button');
    sbtns.forEach(function(b){
      b.addEventListener('click',function(){
        sbtns.forEach(function(x){x.setAttribute('aria-pressed','false');});
        b.setAttribute('aria-pressed','true');
        var d=recData[b.getAttribute('data-rec')];
        rec.classList.remove('empty');
        rec.innerHTML='<span class="pk">'+d.pk+'</span><h4>'+d.h+'</h4><p>'+d.p+'</p>'+
          '<a href="contact.html">Request a demo of '+d.h+' \u2192</a>';
      });
    });
  }

  /* ---------- form submit state ---------- */
  var fb=$('#formBtn');
  if(fb) fb.addEventListener('click',function(){
    var ok=$('#formOk'); if(ok) ok.classList.add('show');
  });

  /* ---------- tabs: centre active on overflow ---------- */
  var tabs=$('.tabs'), cur=$('.tab[aria-current="page"]');
  if(tabs&&cur&&tabs.scrollWidth>tabs.clientWidth+4){
    tabs.scrollLeft=cur.offsetLeft-(tabs.clientWidth-cur.offsetWidth)/2;
  }
})();
