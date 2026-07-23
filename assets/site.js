(function(){
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  /* ---------- theme ---------- */
  var root=document.documentElement;
  window.gxPrefsAllowed=function(){
    try{ var c=JSON.parse(localStorage.getItem('gx-consent')||'null'); return !!(c&&c.preferences); }
    catch(e){ return false; }
  };
  try{ if(window.gxPrefsAllowed()){ var saved=localStorage.getItem('gx-theme'); if(saved) root.setAttribute('data-theme',saved); } }catch(e){}
  var tb=$('#themeBtn');
  if(tb) tb.addEventListener('click',function(){
    var next = root.getAttribute('data-theme')==='dark' ? 'light':'dark';
    root.setAttribute('data-theme',next);
    if(window.gxPrefsAllowed()){ try{ localStorage.setItem('gx-theme',next); }catch(e){} }
  });

  /* ---------- sticky nav shadow ---------- */
  var nav=$('header.nav');
  if(nav) window.addEventListener('scroll',function(){
    nav.classList.toggle('stuck', window.scrollY>8);
  },{passive:true});

  /* ---------- dropdown menus (multi-tab) ---------- */
  var dropT=null, openEl=null;
  function closeAll(){ $$('.mega').forEach(function(m){m.classList.remove('open');}); openEl=null; }
  function openFor(tab){
    var id=tab.getAttribute('data-drop'); if(!id) { closeAll(); return; }
    var m=document.getElementById(id); if(!m) { closeAll(); return; }
    if(openEl && openEl!==m) openEl.classList.remove('open');
    m.classList.add('open'); openEl=m;
  }
  $$('.tab').forEach(function(tab){
    tab.addEventListener('mouseenter',function(){ clearTimeout(dropT); openFor(tab); });
    tab.addEventListener('focus',function(){ clearTimeout(dropT); openFor(tab); });
    tab.addEventListener('mouseleave',function(){ dropT=setTimeout(closeAll,200); });
  });
  $$('.mega').forEach(function(m){
    m.addEventListener('mouseenter',function(){ clearTimeout(dropT); });
    m.addEventListener('mouseleave',function(){ dropT=setTimeout(closeAll,200); });
  });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeAll(); });

  /* ---------- module picker (clinical packages) ---------- */
  var picker=$('#modPicker'), out=$('#modOut');
  if(picker&&out){
    var mods=$$('.mod',picker);
    mods.forEach(function(m){
      m.addEventListener('click',function(){
        m.setAttribute('aria-pressed', m.getAttribute('aria-pressed')==='true'?'false':'true');
        var sel=mods.filter(function(x){return x.getAttribute('aria-pressed')==='true';})
                    .map(function(x){return x.getAttribute('data-mod');});
        if(!sel.length){ out.innerHTML='Nothing selected yet. Choose the departments where records, scheduling or reporting are still manual.'; return; }
        var list=sel.length===1?sel[0]:sel.slice(0,-1).join(', ')+' and '+sel[sel.length-1];
        out.innerHTML='<b>'+sel.length+' selected.</b> A Clinical Specialized Package covering '+list+
          ', scoped to your existing systems and priced to that scope alone. '+
          '<a href="contact.html" style="color:var(--blue);font-weight:600">Send this scope to us &rarr;</a>';
      });
    });
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

/* =================== CHAT · LANGUAGE · LIGHTBOX · SUPABASE =================== */
(function(){
  var CFG = window.GENESYS_CONFIG || {};
  var $  = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  /* ---- Supabase REST helper (no SDK needed) ---- */
  function sbConfigured(){
    return !!(CFG.SUPABASE_URL && CFG.SUPABASE_ANON_KEY &&
              /^https:\/\/[a-z0-9-]+\.supabase\.co/i.test(CFG.SUPABASE_URL.trim()));
  }
  function sbInsert(table, row){
    if(!sbConfigured()){
      console.warn('[Genesys] Supabase not configured. Add SUPABASE_URL and SUPABASE_ANON_KEY in assets/config.js, then redeploy.');
      return Promise.resolve({ok:false, reason:'not-configured'});
    }
    return fetch(CFG.SUPABASE_URL.replace(/\/$/,'')+'/rest/v1/'+table, {
      method:'POST',
      headers:{'Content-Type':'application/json','apikey':CFG.SUPABASE_ANON_KEY,
               'Authorization':'Bearer '+CFG.SUPABASE_ANON_KEY,'Prefer':'return=minimal'},
      body: JSON.stringify(row)
    }).then(function(r){
      if(r.ok) return {ok:true, status:r.status};
      return r.text().then(function(t){
        console.error('[Genesys] Supabase rejected the insert into "'+table+'". HTTP '+r.status+' — '+t);
        return {ok:false, status:r.status, reason:t};
      });
    }).catch(function(e){
      console.error('[Genesys] Could not reach Supabase:', e);
      return {ok:false, reason:String(e)};
    });
  }
  window.gxInsert = sbInsert;

  /* Diagnostic: type gxCheck() in the browser console on the live site */
  window.gxCheck = function(){
    var u=(CFG.SUPABASE_URL||'').trim(), k=(CFG.SUPABASE_ANON_KEY||'').trim();
    console.log('%c Genesys connection check ','background:#0B4FC4;color:#fff;padding:2px 6px;border-radius:3px');
    console.log('URL set:      ', u ? u : 'NO — assets/config.js SUPABASE_URL is empty');
    console.log('Anon key set: ', k ? (k.slice(0,12)+'… ('+k.length+' chars)') : 'NO — assets/config.js SUPABASE_ANON_KEY is empty');
    if(!sbConfigured()){
      console.warn('VERDICT: not configured. Fill both values in assets/config.js, commit, and let Vercel redeploy.');
      return;
    }
    ['leads','chat_messages','subscribers'].forEach(function(t){
      fetch(u.replace(/\/$/,'')+'/rest/v1/'+t+'?select=id&limit=1',
        {headers:{'apikey':k,'Authorization':'Bearer '+k}})
      .then(function(r){
        if(r.status===200) console.log('table '+t+': reachable (read allowed)');
        else if(r.status===401||r.status===403) console.log('table '+t+': exists, public reads blocked by RLS (expected)');
        else if(r.status===404) console.error('table '+t+': NOT FOUND — run supabase/schema.sql in the SQL editor');
        else console.warn('table '+t+': HTTP '+r.status);
      }).catch(function(e){ console.error('table '+t+': network error', e); });
    });
    fetch(u.replace(/\/$/,'')+'/rest/v1/leads',{method:'POST',
      headers:{'Content-Type':'application/json','apikey':k,'Authorization':'Bearer '+k,'Prefer':'return=minimal'},
      body:JSON.stringify({full_name:'Connection test',email:'test@genesys-health.com',
        message:'Automated check from gxCheck(). Safe to delete.',source_page:'gxCheck'})})
    .then(function(r){
      if(r.ok) console.log('%cWRITE TEST PASSED — a row named "Connection test" is now in your leads table.','color:#0B8C5A;font-weight:bold');
      else r.text().then(function(t){ console.error('WRITE TEST FAILED — HTTP '+r.status+': '+t); });
    }).catch(function(e){ console.error('WRITE TEST FAILED — network:', e); });
  };

  /* ---- LIGHTBOX for product screenshots ---- */
  var lb = document.createElement('div');
  lb.className='lightbox';
  lb.innerHTML='<button class="lb-close" aria-label="Close">&times;</button>'+
    '<img alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">'+
    '<div class="lb-cap"></div>';
  document.body.appendChild(lb);
  var lbImg=$('img',lb), lbCap=$('.lb-cap',lb);
  function closeLb(){ lb.classList.remove('open'); }
  $('.lb-close',lb).addEventListener('click',closeLb);
  lb.addEventListener('click',function(e){ if(e.target===lb) closeLb(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeLb(); });
  $$('.zoomable').forEach(function(el){
    el.addEventListener('click',function(){
      var img=el.tagName==='IMG'?el:$('img',el);
      if(!img) return;
      lbImg.src=img.src; lbImg.alt=img.alt||'';
      lbCap.textContent=img.getAttribute('data-cap')||img.alt||'';
      lb.classList.add('open');
    });
  });

  /* ---- CHAT WIDGET ---- */
  var wa = CFG.WHATSAPP || '2349036001000';
  var mail = CFG.EMAIL || 'info@genesys-health.com';
  var fab=document.createElement('button');
  fab.className='chat-fab'; fab.setAttribute('aria-label','Chat with Genesys');
  fab.innerHTML='<span class="badge"></span><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.9-.9L3 21l1.9-5A8.4 8.4 0 0 1 12 3.1a8.4 8.4 0 0 1 9 8.4z"/></svg>';
  var panel=document.createElement('div');
  panel.className='chat-panel'; panel.setAttribute('role','dialog'); panel.setAttribute('aria-label','Chat with Genesys');
  panel.innerHTML =
    '<div class="chat-head"><span class="ch-av">G</span><span><b>Genesys</b>'+
      '<span><i></i>Usually replies within one business day</span></span>'+
      '<button class="ch-x" aria-label="Close chat">&times;</button></div>'+
    '<div class="chat-body" id="chatBody">'+
      '<div class="bubble bot">Hello. Tell us about the facility you run and we will point you to the right system. What would you like to do?</div>'+
    '</div>'+
    '<div class="quicks" id="chatQuicks">'+
      '<button class="quick" data-q="demo">Request a demo</button>'+
      '<button class="quick" data-q="which">Which system fits us?</button>'+
      '<button class="quick" data-q="price">Pricing</button>'+
      '<button class="quick" data-q="wa">WhatsApp us</button>'+
    '</div>'+
    '<div class="chat-foot"><input id="chatIn" type="text" placeholder="Type a message…" aria-label="Your message">'+
      '<button id="chatSend" aria-label="Send">&rarr;</button></div>'+
    '<div class="chat-note">Automated assistant. Not for medical advice or patient information.</div>';
  document.body.appendChild(fab); document.body.appendChild(panel);

  var body=$('#chatBody',panel), input=$('#chatIn',panel);
  var session='gx-'+Math.random().toString(36).slice(2,10);
  function add(text, who){
    var b=document.createElement('div');
    b.className='bubble '+(who==='me'?'me':'bot');
    b.innerHTML=text; body.appendChild(b); body.scrollTop=body.scrollHeight;
  }
  function botReply(text){ setTimeout(function(){ add(text,'bot'); }, 420); }
  var REPLIES={
    demo:'Good. Use the <a href="contact.html" style="color:var(--blue);font-weight:600">demo request form</a> and tell us your facility type and bed count. We reply within one business day, and the demo runs on workflows that match your facility rather than a generic script.',
    which:'It comes down to scale. 1 to 20 beds is usually <a href="solutions-emr.html" style="color:var(--blue);font-weight:600">Genesys EMR</a>; 100 to 500 beds is <a href="solutions-hmis.html" style="color:var(--blue);font-weight:600">Genesys HMIS</a>; a lab, pharmacy or imaging centre wants <a href="solutions-standalone.html" style="color:var(--blue);font-weight:600">Stand-alone Packages</a>. How many beds do you run?',
    price:'Pricing is set to the scale of the practice, and we scope before quoting rather than publishing a number that would not hold. Tell us your facility type and size and we will come back with a real figure.',
    wa:'Opening WhatsApp now. If it does not open, message us on +234 903 600 1000.'
  };
  function handle(q, label){
    add(label,'me');
    if(q==='wa'){ botReply(REPLIES.wa); window.open('https://wa.me/'+wa,'_blank','noopener'); return; }
    botReply(REPLIES[q] || 'Thank you. A member of the team will follow up. If it is urgent, message us on WhatsApp at +234 903 600 1000 or email <a href="mailto:'+mail+'" style="color:var(--blue);font-weight:600">'+mail+'</a>.');
  }
  $$('.quick',panel).forEach(function(b){
    b.addEventListener('click',function(){ handle(b.getAttribute('data-q'), b.textContent); });
  });
  function send(){
    var v=input.value.trim(); if(!v) return;
    add(v,'me'); input.value='';
    sbInsert('chat_messages',{session_id:session,sender:'visitor',body:v,source_page:location.pathname});
    botReply('Thank you. A member of the team will pick this up and reply within one business day. If it is urgent, <a href="https://wa.me/'+wa+'" target="_blank" rel="noopener" style="color:var(--blue);font-weight:600">message us on WhatsApp</a>.');
  }
  $('#chatSend',panel).addEventListener('click',send);
  input.addEventListener('keydown',function(e){ if(e.key==='Enter') send(); });
  function toggle(open){ panel.classList.toggle('open', open); if(open) setTimeout(function(){input.focus();},250); }
  fab.addEventListener('click',function(){ toggle(!panel.classList.contains('open')); });
  $('.ch-x',panel).addEventListener('click',function(){ toggle(false); });

  /* ---- FORM: validate → Supabase if configured → always give a real way to send ---- */
  var fb=$('#formBtn');
  if(fb){
    var val=function(id){var e=document.getElementById(id);return e?e.value.trim():'';};
    var fieldEl=function(id){return document.getElementById(id);};
    function flag(id,bad){
      var e=fieldEl(id); if(!e) return;
      e.style.borderColor = bad ? '#C4341F' : '';
      e.style.boxShadow   = bad ? '0 0 0 3px rgba(196,52,31,.12)' : '';
    }
    fb.addEventListener('click',function(){
      var name=val('name'), email=val('email'), phone=val('phone');
      var okName=!!name, okMail=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
      var tick=document.getElementById('consentTick');
      var okConsent = tick ? tick.checked : true;
      var cbox=document.getElementById('consentBox');
      if(cbox) cbox.classList.toggle('bad', !okConsent);
      flag('name',!okName); flag('email',!okMail);
      var ok=$('#formOk');
      if(okName&&okMail&&!okConsent){
        if(ok){ ok.className='form-ok show';
          ok.innerHTML='<span>!</span><span>Please tick the consent box so we may lawfully use your details to reply.</span>';
          ok.style.background='rgba(196,52,31,.08)'; ok.style.color='#C4341F'; }
        tick.focus(); return;
      }
      if(!okName||!okMail){
        if(ok){ ok.className='form-ok show';
          ok.innerHTML='<span>!</span><span>Please add '+(!okName?'your name':'')+
            (!okName&&!okMail?' and ':'')+(!okMail?'a valid email address':'')+' so we can reply.</span>';
          ok.style.background='rgba(196,52,31,.08)'; ok.style.color='#C4341F'; }
        (fieldEl(!okName?'name':'email')||{focus:function(){}}).focus();
        return;
      }
      var row={full_name:name,email:email,phone:phone,facility_name:val('facility'),
        facility_type:val('ftype'),beds_sites:val('beds'),product:val('product'),message:val('msg'),
        source_page:location.pathname,
        locale:(function(){try{return (window.gxPrefsAllowed&&window.gxPrefsAllowed())?(localStorage.getItem('gx-lang')||'en'):'en';}catch(e){return 'en';}})(),
        consent_given:true, consent_at:new Date().toISOString(),
        marketing_opt_in:!!(document.getElementById('marketingTick')||{}).checked};

      var lines=['Demo request via genesys-health.com','',
        'Name: '+row.full_name,'Email: '+row.email,'Phone: '+(row.phone||'-'),
        'Facility: '+(row.facility_name||'-'),'Type: '+row.facility_type,
        'Beds / sites: '+row.beds_sites,'Product of interest: '+row.product,'',
        'Message:', (row.message||'-')].join('\n');
      var subject='Demo request — '+(row.facility_name||row.full_name);
      var mailto='mailto:'+mail+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(lines);
      var waLink='https://wa.me/'+wa+'?text='+encodeURIComponent(lines);

      sbInsert('leads',row).then(function(res){
        if(!ok) return;
        ok.style.background=''; ok.style.color='';
        ok.className='form-ok show';
        if(res.ok){
          ok.innerHTML='<span>&#10003;</span><span>Thank you, '+row.full_name.split(' ')[0]+
            '. Your request has reached us and we reply within one business day.</span>';
        } else {
          ok.innerHTML='<span>&#10003;</span><span style="display:block">'+
            '<b style="display:block;margin-bottom:6px">Almost there, '+row.full_name.split(' ')[0]+'.</b>'+
            'Choose how to send it and your details go straight to our enquiries team.'+
            '<span style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">'+
              '<a class="btn btn-primary" style="font-size:14px;padding:.6em 1em" href="'+mailto+'">Send by email</a>'+
              '<a class="btn btn-ghost" style="font-size:14px;padding:.6em 1em" href="'+waLink+'" target="_blank" rel="noopener">Send on WhatsApp</a>'+
              '<button class="btn btn-ghost" id="copyLead" style="font-size:14px;padding:.6em 1em">Copy details</button>'+
            '</span></span>';
          var cp=document.getElementById('copyLead');
          if(cp) cp.addEventListener('click',function(){
            (navigator.clipboard?navigator.clipboard.writeText(lines):Promise.reject())
              .then(function(){cp.textContent='Copied';}).catch(function(){cp.textContent='Select and copy above';});
          });
        }
      });
    });
  }
  /* ---- newsletter ---- */
  $$('.news button').forEach(function(b){
    b.addEventListener('click',function(){
      var inp=b.parentNode.querySelector('input'); if(!inp||!inp.value.trim()) return;
      sbInsert('subscribers',{email:inp.value.trim()});
      inp.value=''; b.textContent='✓';
      var note=b.parentNode.parentNode.querySelector('.sub-note');
      if(!note){ note=document.createElement('p'); note.className='sub-note';
        note.style.cssText='font-size:12px;color:var(--text-muted);margin-top:7px;line-height:1.5';
        b.parentNode.parentNode.appendChild(note); }
      note.innerHTML='Thank you. You consented to occasional updates and can withdraw any time via '+
        '<a href="data-request.html" style="color:var(--blue)">your data rights</a>.';
      setTimeout(function(){b.innerHTML='&rarr;';},2200);
    });
  });

  /* ---- DATA SUBJECT REQUEST FORM (NDPA rights) ---- */
  var dsrBtn=$('#dsrBtn');
  if(dsrBtn) dsrBtn.addEventListener('click',function(){
    var g=function(id){var e=document.getElementById(id);return e?e.value.trim():'';};
    var name=g('dsrName'), email=g('dsrEmail');
    var tick=document.getElementById('dsrTick'), box=document.getElementById('dsrConsentBox');
    var okMail=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
    var out=document.getElementById('dsrOk');
    if(box) box.classList.toggle('bad', !(tick&&tick.checked));
    if(!name||!okMail||!(tick&&tick.checked)){
      if(out){ out.className='form-ok show';
        out.style.background='rgba(196,52,31,.08)'; out.style.color='#C4341F';
        out.innerHTML='<span>!</span><span>Please give your name, a valid email address, and tick the confirmation box.</span>'; }
      return;
    }
    var row={request_type:g('dsrType'),full_name:name,email:email,phone:g('dsrPhone'),
             details:g('dsrDetails'),source_page:location.pathname};
    var lines=['Data rights request via genesys-health.com','','Request: '+row.request_type,
      'Name: '+row.full_name,'Email: '+row.email,'Phone: '+(row.phone||'-'),'','Details:',(row.details||'-')].join('\n');
    sbInsert('dsr_requests',row).then(function(res){
      if(!out) return;
      out.style.background=''; out.style.color=''; out.className='form-ok show';
      if(res.ok){
        out.innerHTML='<span>&#10003;</span><span>Request received. We will respond within 30 days, and may first ask you to verify your identity.</span>';
      } else {
        out.innerHTML='<span>&#10003;</span><span style="display:block">'+
          '<b style="display:block;margin-bottom:6px">One more step.</b>Send it to our data protection contact:'+
          '<span style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">'+
          '<a class="btn btn-primary" style="font-size:14px;padding:.6em 1em" href="mailto:'+mail+
          '?subject='+encodeURIComponent('Data rights request \u2014 '+row.request_type)+
          '&body='+encodeURIComponent(lines)+'">Send by email</a></span></span>';
      }
    });
  });

  /* ---- LANGUAGE TOGGLE (EN / FR) ---- */
  var FR={
    "Home":"Accueil","How it works":"Comment ça marche","Solutions":"Solutions","Who we serve":"Qui nous servons",
    "Proof":"Références","About":"À propos","Insights":"Analyses","Contact":"Contact",
    "Request a demo":"Demander une démo","Chat on WhatsApp":"Discuter sur WhatsApp",
    "Book a consultation":"Réserver une consultation","Read more":"En savoir plus",
    "All solutions":"Toutes les solutions","Everyone we serve":"Tous nos clients",
    "Case studies":"Études de cas","Security &amp; compliance":"Sécurité et conformité",
    "Implementation":"Mise en œuvre","Our story":"Notre histoire","The team":"L'équipe",
    "Vision &amp; values":"Vision et valeurs","Stories by Genesys":"Récits de Genesys",
    "Industry news":"Actualité du secteur","Hospitals":"Hôpitaux",
    "Clinics &amp; practices":"Cliniques et cabinets","Public health systems":"Systèmes de santé publique",
    "Payers &amp; HMOs":"Assureurs et HMO","Stay in the loop":"Restez informé",
    "Company":"Entreprise","Your email address":"Votre adresse e-mail"
  };
  var lang = (function(){ try{return (window.gxPrefsAllowed&&window.gxPrefsAllowed()) ? (localStorage.getItem('gx-lang')||'en') : 'en';}catch(e){return 'en';} })();
  var banner=document.createElement('div');
  banner.className='fr-banner';
  banner.innerHTML='<div class="wrap"><b>Version française en cours.</b> La navigation est traduite; le contenu détaillé est en cours de traduction professionnelle. <a href="contact.html" style="color:var(--blue);font-weight:600">Contactez-nous en français</a>.</div>';
  var hdr=document.querySelector('header.nav');
  if(hdr && hdr.parentNode) hdr.parentNode.insertBefore(banner, hdr.nextSibling);

  function applyLang(l){
    var fr = (l==='fr');
    banner.classList.toggle('show', fr);
    document.documentElement.setAttribute('lang', fr?'fr':'en');
    $$('[data-i18n]').forEach(function(el){
      var k=el.getAttribute('data-i18n');
      if(fr && FR[k]) el.textContent=FR[k];
      else el.textContent=k.replace(/&amp;/g,'&');
    });
    $$('.langbtn').forEach(function(b){
      b.innerHTML = fr ? 'EN / <b>FR</b>' : '<b>EN</b> / FR';
      b.setAttribute('aria-label', fr?'Switch to English':'Passer en français');
    });
    if(window.gxPrefsAllowed&&window.gxPrefsAllowed()){ try{ localStorage.setItem('gx-lang', l); }catch(e){} }
  }
  $$('.langbtn').forEach(function(b){
    b.addEventListener('click',function(){ lang = (lang==='fr'?'en':'fr'); applyLang(lang); });
  });
  applyLang(lang);
})();

/* =================== PRODUCT WALKTHROUGH PLAYER =================== */
(function(){
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pl = document.querySelector('.player');
  if(!pl) return;
  var $  = function(s,c){return (c||pl).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||pl).querySelectorAll(s));};

  var slides = $$('.pl-slide');
  var segs   = $$('.pl-seg');
  var chaps  = $$('.pl-chapters button');
  var kick=$('.pl-kicker'), title=$('.pl-title'), desc=$('.pl-desc'), count=$('.pl-count');
  var btnPlay=$('.pl-btn.play'), btnPrev=$('.pl-btn.prev'), btnNext=$('.pl-btn.next');
  var DUR = 6500, i = 0, raf = null, t0 = null, playing = !RM, hovered = false;

  function setChapter(idx){
    var ch = slides[idx].getAttribute('data-chapter');
    chaps.forEach(function(c){ c.setAttribute('aria-selected', c.getAttribute('data-chapter')===ch ? 'true':'false'); });
  }
  function render(idx){
    slides.forEach(function(s,k){ s.classList.toggle('on', k===idx); });
    segs.forEach(function(s,k){
      s.classList.toggle('done', k<idx);
      s.classList.toggle('now', k===idx);
      if(k>idx){ s.classList.remove('done','now'); s.style.setProperty('--p','0%'); }
      if(k===idx) s.style.setProperty('--p','0%');
    });
    var s = slides[idx];
    kick.textContent  = s.getAttribute('data-kicker');
    title.textContent = s.getAttribute('data-title');
    desc.textContent  = s.getAttribute('data-desc');
    count.textContent = 'Screen ' + (idx+1) + ' of ' + slides.length;
    setChapter(idx);
  }
  function tick(ts){
    if(!t0) t0 = ts;
    var p = Math.min((ts - t0)/DUR, 1);
    if(segs[i]) segs[i].style.setProperty('--p', (p*100)+'%');
    if(p >= 1){ go(i+1); return; }
    raf = requestAnimationFrame(tick);
  }
  function stop(){ if(raf) cancelAnimationFrame(raf); raf=null; t0=null; }
  function start(){
    stop();
    if(!playing || RM) return;
    raf = requestAnimationFrame(tick);
  }
  function go(n, manual){
    i = (n + slides.length) % slides.length;
    render(i);
    if(manual){ /* keep current play state */ }
    start();
  }
  function setPlaying(v){
    playing = v;
    btnPlay.innerHTML = v ? '&#10073;&#10073;' : '&#9658;';
    btnPlay.setAttribute('aria-label', v ? 'Pause walkthrough' : 'Play walkthrough');
    if(v) start(); else stop();
  }

  btnPrev.addEventListener('click', function(){ go(i-1, true); });
  btnNext.addEventListener('click', function(){ go(i+1, true); });
  btnPlay.addEventListener('click', function(){ setPlaying(!playing); });
  segs.forEach(function(s,k){ s.addEventListener('click', function(){ go(k, true); }); });
  chaps.forEach(function(c){
    c.addEventListener('click', function(){
      var ch=c.getAttribute('data-chapter');
      for(var k=0;k<slides.length;k++){
        if(slides[k].getAttribute('data-chapter')===ch){ go(k, true); break; }
      }
    });
  });
  $('.pl-zoom').addEventListener('click', function(){
    var img = slides[i].querySelector('img'); if(img) img.click();
  });

  // pause while hovering the stage, resume after
  var stage=$('.pl-stage');
  stage.addEventListener('mouseenter', function(){ hovered=true; stop(); });
  stage.addEventListener('mouseleave', function(){ hovered=false; if(playing) start(); });

  // pause when the tab is hidden or the player is off-screen
  document.addEventListener('visibilitychange', function(){
    if(document.hidden) stop(); else if(playing && !hovered) start();
  });
  var vio = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){ if(playing && !hovered) start(); }
      else stop();
    });
  },{threshold:.25});
  vio.observe(pl);

  // keyboard
  pl.setAttribute('tabindex','0');
  pl.addEventListener('keydown', function(e){
    if(e.key==='ArrowRight'){ e.preventDefault(); go(i+1,true); }
    if(e.key==='ArrowLeft'){ e.preventDefault(); go(i-1,true); }
    if(e.key===' '){ e.preventDefault(); setPlaying(!playing); }
  });

  // touch swipe
  var x0=null;
  stage.addEventListener('touchstart', function(e){ x0=e.touches[0].clientX; stop(); }, {passive:true});
  stage.addEventListener('touchend', function(e){
    if(x0===null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if(Math.abs(dx) > 45) go(i + (dx<0?1:-1), true); else if(playing) start();
    x0=null;
  }, {passive:true});

  render(0);
  setPlaying(!RM);
})();

/* =================== NDPA 2023 CONSENT MANAGEMENT ===================
   Nigeria Data Protection Act 2023 + NDPC General Application and
   Implementation Directive (GAID) 2025, Article 19.
   - opt-in for everything except strictly necessary
   - no pre-ticked boxes
   - withdrawal as easy as giving consent
   - each decision logged with a timestamp                                */
(function(){
  var KEY='gx-consent';
  var $  = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  function read(){ try{ return JSON.parse(localStorage.getItem(KEY)||'null'); }catch(e){ return null; } }
  function write(o){ try{ localStorage.setItem(KEY, JSON.stringify(o)); }catch(e){} }

  var banner=document.createElement('div');
  banner.className='cbanner'; banner.setAttribute('role','region');
  banner.setAttribute('aria-label','Data and storage consent');
  banner.innerHTML=
    '<div class="wrap cb-in"><div class="cb-txt">'+
      '<h4>Your privacy choices</h4>'+
      '<p>We use storage that is strictly necessary for this site to work. Anything beyond that &mdash; '+
      'remembering your theme and language, or measuring how the site is used &mdash; happens only if you agree. '+
      'You can change or withdraw your choice at any time. Read our '+
      '<a href="privacy.html">Privacy Notice</a> and <a href="cookies.html">Cookie Notice</a>.</p>'+
    '</div><div class="cb-acts">'+
      '<button class="btn btn-ghost" id="cbManage">Manage choices</button>'+
      '<button class="btn btn-ghost" id="cbReject">Essential only</button>'+
      '<button class="btn btn-primary" id="cbAccept">Accept all</button>'+
    '</div></div>';

  var modal=document.createElement('div');
  modal.className='cmodal'; modal.setAttribute('role','dialog'); modal.setAttribute('aria-modal','true');
  modal.setAttribute('aria-label','Manage privacy choices');
  modal.innerHTML=
    '<div class="cm-box"><div class="cm-head"><h3>Manage your privacy choices</h3>'+
      '<button id="cmX" aria-label="Close">&times;</button></div>'+
    '<div class="cm-body">'+
      '<div class="copt"><div><b>Strictly necessary</b><p>Required for the site to load, stay secure and '+
        'remember the privacy choice you make here. It cannot be switched off, and it is permitted without '+
        'consent under Article 19 of the NDPC GAID.</p></div><span class="locked">Always on</span></div>'+
      '<div class="copt"><div><b>Preferences</b><p>Remembers your colour theme and language between visits. '+
        'Stored in your browser only. Nothing is shared with anyone.</p></div>'+
        '<label class="sw"><input type="checkbox" id="cPrefs" aria-label="Allow preference storage"><span></span></label></div>'+
      '<div class="copt"><div><b>Analytics</b><p>Would let us count visits and see which pages are useful. '+
        '<b>We do not currently run any analytics.</b> This switch stays off unless we add it and tell you.</p></div>'+
        '<label class="sw"><input type="checkbox" id="cStats" aria-label="Allow analytics"><span></span></label></div>'+
      '<p style="font-size:13.5px;color:var(--text-muted)">Information you type into the demo form, the chat or the '+
      'newsletter box is separate from this. That is handled under the consent you give at the point you send it, '+
      'and is explained in our <a href="privacy.html" style="color:var(--blue);font-weight:600">Privacy Notice</a>.</p>'+
    '</div>'+
    '<div class="cm-foot"><button class="btn btn-ghost" id="cmReject">Essential only</button>'+
      '<button class="btn btn-primary" id="cmSave">Save my choices</button></div></div>';

  document.addEventListener('DOMContentLoaded', function(){
    document.body.appendChild(banner); document.body.appendChild(modal);

    function log(c){
      if(window.gxInsert) window.gxInsert('consent_log',{
        preferences:!!c.preferences, analytics:!!c.analytics,
        given_at:c.at, source_page:location.pathname, policy_version:c.version });
    }
    function apply(c, doLog){
      c.at = new Date().toISOString(); c.version='2026-07';
      write(c); banner.classList.remove('show'); modal.classList.remove('show');
      if(doLog) log(c);
      if(!c.preferences){ try{ localStorage.removeItem('gx-theme'); localStorage.removeItem('gx-lang'); }catch(e){} }
      document.dispatchEvent(new CustomEvent('gx-consent', {detail:c}));
    }
    function openModal(){
      var c=read()||{};
      $('#cPrefs',modal).checked=!!c.preferences;   // never pre-ticked unless already chosen
      $('#cStats',modal).checked=!!c.analytics;
      modal.classList.add('show');
      setTimeout(function(){ $('#cPrefs',modal).focus(); },80);
    }
    window.gxPrivacyChoices = openModal;

    $('#cbAccept',banner).addEventListener('click',function(){ apply({preferences:true, analytics:true}, true); });
    $('#cbReject',banner).addEventListener('click',function(){ apply({preferences:false,analytics:false}, true); });
    $('#cbManage',banner).addEventListener('click', openModal);
    $('#cmX',modal).addEventListener('click',function(){ modal.classList.remove('show'); });
    $('#cmReject',modal).addEventListener('click',function(){ apply({preferences:false,analytics:false}, true); });
    $('#cmSave',modal).addEventListener('click',function(){
      apply({preferences:$('#cPrefs',modal).checked, analytics:$('#cStats',modal).checked}, true);
    });
    modal.addEventListener('click',function(e){ if(e.target===modal) modal.classList.remove('show'); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') modal.classList.remove('show'); });

    // any link or button marked data-privacy-choices reopens the panel (withdrawal path)
    $$('[data-privacy-choices]').forEach(function(el){
      el.addEventListener('click',function(e){ e.preventDefault(); openModal(); });
    });

    if(!read()) setTimeout(function(){ banner.classList.add('show'); }, 700);
  });
})();
