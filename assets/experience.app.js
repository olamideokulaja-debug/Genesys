/* ===========================================================================
   GENESYS — embedded experience controller (scoped to #gx / .gx)
   Tabs, counters, parallax, journey transport, form, capability gate.
   Loaded as a module; dynamically imports the scene only on the WebGL path.
   =========================================================================== */
const TABS = ["overview","journey","modules","pricing","rollout","trust"];
const ROOT = document.getElementById("gx");
if (ROOT){
  const $  = (s, c=ROOT) => c.querySelector(s);
  const $$ = (s, c=ROOT) => Array.from(c.querySelectorAll(s));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isMobile = window.matchMedia("(max-width: 767px)").matches;

  const power2Out = p => 1 - Math.pow(1 - p, 2);
  const countEase = p => 1 - Math.pow(1 - p, 1.7);
  function tween(ms, onUpdate, onDone){
    if (reduceMotion){ onUpdate(1); onDone && onDone(); return; }
    const t0 = performance.now();
    (function frame(now){
      const p = Math.min(1, (now - t0) / ms);
      onUpdate(p);
      if (p < 1) requestAnimationFrame(frame); else onDone && onDone();
    })(t0);
  }

  let current = "overview";
  let scene = null;

  function tabOwnsHash(){ return TABS.includes((location.hash||"").replace("#","")); }

  function activate(name, {push=true, focus=false}={}){
    if (!TABS.includes(name)) name = "overview";
    current = name;
    TABS.forEach(t => {
      const tab = $(`#gx-tab-${t}`), panel = $(`#gx-panel-${t}`);
      const on = t === name;
      tab.setAttribute("aria-selected", on ? "true":"false");
      tab.tabIndex = on ? 0 : -1;
      panel.setAttribute("data-active", on ? "true":"false");
      if (on) panel.scrollTop = 0;
    });
    if (focus) $(`#gx-tab-${name}`).focus();
    if (push){
      const hash = "#" + name;
      if (location.hash !== hash) history.pushState({gx:name}, "", hash);
    }
    if (scene) scene.flyTo(name);
    runCounters(name);
    if (name === "journey") Journey.autoplayOnce();
  }

  $$(".gx-tab").forEach((tab,i)=>{
    tab.addEventListener("click", ()=> activate(tab.id.replace("gx-tab-",""), {focus:true}));
    tab.addEventListener("keydown", e=>{
      let j=null;
      if (e.key==="ArrowRight"||e.key==="ArrowDown") j=(i+1)%TABS.length;
      else if (e.key==="ArrowLeft"||e.key==="ArrowUp") j=(i-1+TABS.length)%TABS.length;
      else if (e.key==="Home") j=0; else if (e.key==="End") j=TABS.length-1;
      if (j!==null){ e.preventDefault(); activate(TABS[j], {focus:true}); }
    });
  });
  $$("[data-gx-goto]").forEach(b=> b.addEventListener("click", ()=> activate(b.dataset.gxGoto, {focus:true})));
  window.addEventListener("popstate", ()=>{ if (tabOwnsHash()) activate(location.hash.slice(1), {push:false}); });

  /* counters */
  const counted = new Set();
  function runCounters(name){
    $$(`#gx-panel-${name} [data-count]`).forEach(el=>{
      if (counted.has(el)) return; counted.add(el);
      const target = parseFloat(el.dataset.count);
      const plain = el.dataset.plain === "1";
      const suffix = el.dataset.suffix || "";
      tween(1700, p=>{
        const v = Math.round(target * countEase(p));
        el.textContent = (plain ? String(v) : v.toLocaleString("en-NG")) + suffix;
      });
    });
  }

  /* pricing from single config */
  (function renderPricing(){
    const P = window.GENESYS_PRICING; if (!P) return;
    const grid = $("#gxPriceGrid"); if (!grid) return;
    grid.innerHTML = P.tiers.map(t=>{
      const bands = t.bands ? `<div class="gx-bands">${t.bands.map(b=>
        `<div class="gx-band"><span class="bseats">${b.band} &middot; ${b.seats}</span><span class="bprice">${b.price}</span></div>`).join("")}</div>` : "";
      const amort = t.setup.amortised ? `<div class="sub gx-muted">${t.setup.amortised}</div>` : "";
      return `<div class="gx-tier">
        <div><h3>${t.name}</h3><div class="who">${t.forWho}</div></div>
        <div class="lineitem"><div class="k">Setup (one-time)</div><div class="v">${t.setup.display}</div>${amort}<div class="sub">${t.setup.includes}</div></div>
        <div class="lineitem"><div class="k">Subscription</div><div class="v">${t.recurring.display}<span class="u">${t.recurring.unit}</span></div>${bands}<div class="sub">${t.recurring.detail}</div></div>
        <div class="lineitem"><div class="k">Seats &amp; support</div><div class="sub">${t.seatModel}.<br>${t.supentry}.</div></div>
        <a class="gx-btn gx-btn-ghost" href="contact.html">Request a quote</a>
      </div>`;
    }).join("");
    $("#gxAddonTable tbody").innerHTML = P.addons.map(a=>
      `<tr><td>${a.name}</td><td class="gx-muted">${a.basis}</td><td class="rate">${a.rate}</td></tr>`).join("");
    $("#gxPriceNote").textContent = P.note + " " + P.billingModel;
  })();

  /* journey transport */
  const Journey = (function(){
    const stops = ["Registration","Consultation","Laboratory","Pharmacy","Billing","Discharge"];
    const track=$("#gxTrack"), fill=$("#gxFill"), icon=$("#gxIcon"), playBtn=$("#gxPlay");
    const chipEls=$$(".gx-tp-stop");
    let playing=false, prog=0, raf=null, played=false; const DUR=9000;
    function setIcon(p){ icon.innerHTML = p
      ? '<rect x="4" y="3" width="3" height="10"/><rect x="9" y="3" width="3" height="10"/>'
      : '<path d="M4 3l9 5-9 5z"/>'; }
    function render(){
      fill.style.width = (prog*100).toFixed(1)+"%";
      track.setAttribute("aria-valuenow", Math.round(prog*100));
      const lit = Math.floor(prog*stops.length + 0.0001);
      chipEls.forEach((c,i)=>c.classList.toggle("lit", i<=Math.min(lit,stops.length-1) && prog>0));
      if (scene) scene.journeyProgress(prog);
      track.setAttribute("aria-valuetext", prog<=0?"not started":prog>=1?"complete, facility fully lit":"at "+stops[Math.min(lit,stops.length-1)]);
    }
    function loop(t0, from){
      raf=requestAnimationFrame(now=>{
        prog=Math.min(1, from+(now-t0)/DUR); render();
        if (prog<1 && playing) loop(t0, from); else { playing=false; setIcon(false); }
      });
    }
    function play(){ if(prog>=1) prog=0; playing=true; setIcon(true); loop(performance.now(), prog); }
    function pause(){ playing=false; setIcon(false); if(raf) cancelAnimationFrame(raf); }
    playBtn.addEventListener("click", ()=> playing?pause():play());
    function scrub(x){ const r=track.getBoundingClientRect(); prog=Math.max(0,Math.min(1,(x-r.left)/r.width)); render(); }
    track.addEventListener("pointerdown", e=>{ pause(); scrub(e.clientX); track.setPointerCapture(e.pointerId);
      const mv=ev=>scrub(ev.clientX); const up=()=>{track.removeEventListener("pointermove",mv);track.removeEventListener("pointerup",up);};
      track.addEventListener("pointermove",mv); track.addEventListener("pointerup",up); });
    track.addEventListener("keydown", e=>{ const step=1/stops.length;
      if(e.key==="ArrowRight"){prog=Math.min(1,prog+step);render();e.preventDefault();}
      else if(e.key==="ArrowLeft"){prog=Math.max(0,prog-step);render();e.preventDefault();}
      else if(e.key===" "||e.key==="Enter"){playing?pause():play();e.preventDefault();} });
    return { autoplayOnce(){ if(played||reduceMotion){render();return;} played=true; setTimeout(play,500); } };
  })();

  /* pointer parallax */
  if (!reduceMotion && !isMobile){
    const layers=$$(".gx-par"); let tx=0,ty=0,cx=0,cy=0;
    ROOT.addEventListener("pointermove", e=>{ const r=ROOT.getBoundingClientRect();
      tx=((e.clientX-r.left)/r.width-.5); ty=((e.clientY-r.top)/r.height-.5); });
    (function damp(){ cx+=(tx-cx)*.06; cy+=(ty-cy)*.06;
      layers.forEach(l=>{ const d=parseFloat(l.dataset.depth||"1");
        l.style.transform=`translate3d(${(-cx*d*10).toFixed(2)}px,${(-cy*d*10).toFixed(2)}px,0)`; });
      requestAnimationFrame(damp); })();
  }

  /* enquiry form (email / WhatsApp fallback; consistent with the site) */
  const send=$("#gxSend");
  if (send) send.addEventListener("click", ()=>{
    const g=id=>($("#"+id).value||"").trim();
    const name=g("gxName"), email=g("gxEmail");
    const okMail=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
    const ok=$("#gxOk");
    if(!name||!okMail){ ok.className="gx-form-ok show err";
      ok.textContent="Please add your name and a valid work email so we can reply.";
      $("#"+(!name?"gxName":"gxEmail")).focus(); return; }
    const lines=["Genesys enquiry via the site","","Name: "+name,"Email: "+email,"Facility: "+g("gxFacility"),"Tier of interest: "+g("gxTier"),"","Message:",g("gxMsg")||"-"].join("\n");
    const mailto="mailto:cordor@genesys-health.com?subject="+encodeURIComponent("Genesys enquiry — "+(g("gxFacility")||name))+"&body="+encodeURIComponent(lines);
    ok.className="gx-form-ok show";
    ok.innerHTML=`Thank you, ${name.split(" ")[0]}. Choose how to send it: `+
      `<a href="${mailto}" style="color:var(--gx-ok);font-weight:600;margin-left:6px">open email</a> &middot; `+
      `<a href="https://wa.me/2347047999337?text=${encodeURIComponent(lines)}" target="_blank" rel="noopener" style="color:var(--gx-ok);font-weight:600">WhatsApp</a>`;
  });

  /* capability gate */
  function webglOK(){ try{ const c=document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl2")||c.getContext("webgl"))); }catch(e){ return false; } }
  function weakDevice(){ const m=navigator.deviceMemory, c=navigator.hardwareConcurrency; return (m&&m<=2)||(c&&c<=2); }
  function goFlat(reason){ ROOT.classList.add("is-flat"); ROOT.dataset.flatReason=reason; }
  if (isMobile) ROOT.classList.add("is-mobile");

  async function boot(){
    if (tabOwnsHash()) activate(location.hash.slice(1), {push:false});
    else activate("overview", {push:false});
    runCounters(current);
    if (isMobile || reduceMotion || !webglOK() || weakDevice()){
      goFlat(isMobile?"mobile":reduceMotion?"reduced-motion":!webglOK()?"no-webgl":"weak-device");
      return;
    }
    try{
      const mod = await import("./experience.scene.js");
      scene = mod.createScene({ canvas:$("#gxfield"), onError:()=>{ scene=null; goFlat("context-lost"); } });
      scene.flyTo(current, true);
    }catch(err){ console.warn("[genesys] scene failed, flat mode:", err); goFlat("scene-error"); }
  }
  boot();
}
