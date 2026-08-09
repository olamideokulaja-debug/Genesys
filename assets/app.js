/* ===========================================================================
   GENESYS — application controller
   Tabs (ARIA + deep-link), counters, parallax, journey transport, form,
   capability detection and the flat-fallback boundary. No framework.
   =========================================================================== */
const TABS = ["overview","journey","modules","pricing","rollout","trust"];
const $  = (s, c=document) => c.querySelector(s);
const $$ = (s, c=document) => Array.from(c.querySelectorAll(s));
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isMobile = window.matchMedia("(max-width: 767px)").matches;

/* ---- easing (implemented directly; equals the specified GSAP curves) ---- */
const expoOut  = p => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p));
const power2Out= p => 1 - Math.pow(1 - p, 2);
const countEase= p => 1 - Math.pow(1 - p, 1.7);   // spec: 1-(1-p)**1.7

function tween(ms, onUpdate, ease = power2Out, onDone){
  if (reduceMotion) { onUpdate(1); onDone && onDone(); return; }
  const t0 = performance.now();
  (function frame(now){
    const p = Math.min(1, (now - t0) / ms);
    onUpdate(ease(p));
    if (p < 1) requestAnimationFrame(frame); else onDone && onDone();
  })(t0);
}

/* ============================ TAB ROUTER ============================ */
let current = "overview";
let scene = null;   // set if WebGL scene loads

function activate(name, {push = true, focus = false} = {}){
  if (!TABS.includes(name)) name = "overview";
  current = name;
  TABS.forEach(t => {
    const tab   = $(`#tab-${t}`);
    const panel = $(`#panel-${t}`);
    const on = t === name;
    tab.setAttribute("aria-selected", on ? "true" : "false");
    tab.tabIndex = on ? 0 : -1;
    panel.setAttribute("data-active", on ? "true" : "false");
    if (on) { panel.hidden = false; panel.scrollTop = 0; }
    else if (!isMobile) { /* keep in DOM for crawlability; hide via CSS+aria */ panel.hidden = false; }
  });
  if (focus) $(`#tab-${name}`).focus();
  if (push){
    const hash = "#" + name;
    if (location.hash !== hash) history.pushState({tab:name}, "", hash);
  }
  document.title = titleFor(name);
  if (scene) scene.flyTo(name);          // camera flight (expo.out inside scene)
  runCounters(name);
  if (name === "journey") Journey.autoplayOnce();
}

function titleFor(name){
  const map = {
    overview:"Genesys Health — the hospital as one connected system",
    journey:"The Journey — Genesys Health",
    modules:"Modules — Genesys Health",
    pricing:"Pricing — Genesys Health",
    rollout:"Rollout — Genesys Health",
    trust:"Trust & data protection — Genesys Health"
  };
  return map[name] || map.overview;
}

/* tab click + roving-tabindex arrow keys (ARIA tabs pattern) */
$$(".tab").forEach((tab, i) => {
  tab.addEventListener("click", () => activate(tab.id.replace("tab-",""), {focus:true}));
  tab.addEventListener("keydown", e => {
    let j = null;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") j = (i+1) % TABS.length;
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") j = (i-1+TABS.length) % TABS.length;
    else if (e.key === "Home") j = 0;
    else if (e.key === "End")  j = TABS.length-1;
    if (j !== null){ e.preventDefault(); activate(TABS[j], {focus:true}); }
  });
});

/* buttons that jump between tabs */
$$("[data-goto]").forEach(b => b.addEventListener("click", () => activate(b.dataset.goto, {focus:true})));

/* deep-link: restore on load + browser back/forward */
window.addEventListener("popstate", e => activate((location.hash||"#overview").slice(1), {push:false}));

/* ============================ COUNTERS ============================ */
const counted = new Set();
function runCounters(panelName){
  $$(`#panel-${panelName} [data-count]`).forEach(el => {
    if (counted.has(el)) return;
    counted.add(el);
    const target = parseFloat(el.dataset.count);
    const plain  = el.dataset.plain === "1";   // year: no thousands separator
    const suffix = el.dataset.suffix || "";
    tween(1700, p => {
      const v = Math.round(target * countEase(p));
      el.textContent = (plain ? String(v) : v.toLocaleString("en-NG")) + suffix;
    }, x=>x /* countEase already applied above */);
  });
}

/* ============================ PRICING (from single config) ============================ */
(function renderPricing(){
  const P = window.GENESYS_PRICING;
  if (!P) return;
  const money = s => `<span class="mono">${s}</span>`;
  const grid = $("#priceGrid");
  grid.innerHTML = P.tiers.map(t => {
    const bands = t.bands ? `<div class="bands">${t.bands.map(b =>
      `<div class="band"><span class="bseats">${b.band} &middot; ${b.seats}</span><span class="bprice">${b.price}</span></div>`).join("")}</div>` : "";
    const amort = t.setup.amortised ? `<div class="sub muted">${t.setup.amortised}</div>` : "";
    return `<div class="tier">
      <div><h3>${t.name}</h3><div class="who">${t.forWho}</div></div>
      <div class="lineitem"><div class="k">Setup (one-time)</div>
        <div class="v">${t.setup.display}</div>${amort}
        <div class="sub">${t.setup.includes}</div></div>
      <div class="lineitem"><div class="k">Subscription</div>
        <div class="v">${t.recurring.display}<span class="u">${t.recurring.unit}</span></div>
        ${bands}<div class="sub">${t.recurring.detail}</div></div>
      <div class="lineitem"><div class="k">Seats &amp; support</div>
        <div class="sub">${t.seatModel}.<br>${t.supentry}.</div></div>
      <button class="btn btn-ghost" data-goto="trust">Request a quote</button>
    </div>`;
  }).join("");
  $("#addonTable tbody").innerHTML = P.addons.map(a =>
    `<tr><td>${a.name}</td><td class="muted">${a.basis}</td><td class="rate">${a.rate}</td></tr>`).join("");
  $("#priceNote").textContent = P.note + " " + P.billingModel;
  // re-bind goto on freshly-rendered buttons
  $$("#panel-pricing [data-goto]").forEach(b => b.addEventListener("click", () => activate(b.dataset.goto, {focus:true})));
})();

/* ============================ JOURNEY TRANSPORT ============================ */
const Journey = (function(){
  const stops = ["Registration","Consultation","Laboratory","Pharmacy","Billing","Discharge"];
  const track = $("#jTrack"), fill = $("#jFill"), icon = $("#jIcon"), playBtn = $("#jPlay");
  const chipEls = $$(".tp-stop");
  let playing = false, prog = 0, raf = null, played = false;
  const DUR = 9000; // ms for the full journey

  function setIcon(p){ icon.innerHTML = p
    ? '<rect x="4" y="3" width="3" height="10"/><rect x="9" y="3" width="3" height="10"/>'
    : '<path d="M4 3l9 5-9 5z"/>'; }

  function render(){
    fill.style.width = (prog*100).toFixed(1) + "%";
    track.setAttribute("aria-valuenow", Math.round(prog*100));
    const lit = Math.floor(prog * stops.length + 0.0001);
    chipEls.forEach((c,i)=>c.classList.toggle("lit", i <= Math.min(lit, stops.length-1) && prog>0));
    if (scene) scene.journeyProgress(prog);
    track.setAttribute("aria-valuetext", prog<=0 ? "not started" :
       prog>=1 ? "complete, facility fully lit" : "at " + stops[Math.min(lit,stops.length-1)]);
  }
  function loop(t0, from){
    raf = requestAnimationFrame(now => {
      prog = Math.min(1, from + (now - t0)/DUR);
      render();
      if (prog < 1 && playing) loop(t0, from);
      else { playing = false; setIcon(false); }
    });
  }
  function play(){ if (prog>=1) prog=0; playing=true; setIcon(true); loop(performance.now(), prog); }
  function pause(){ playing=false; setIcon(false); if(raf) cancelAnimationFrame(raf); }
  playBtn.addEventListener("click", ()=> playing ? pause() : play());

  function scrub(clientX){
    const r = track.getBoundingClientRect();
    prog = Math.max(0, Math.min(1, (clientX - r.left)/r.width));
    render();
  }
  track.addEventListener("pointerdown", e=>{ pause(); scrub(e.clientX);
    track.setPointerCapture(e.pointerId);
    const mv = ev=>scrub(ev.clientX);
    const up = ()=>{track.removeEventListener("pointermove",mv);track.removeEventListener("pointerup",up);};
    track.addEventListener("pointermove",mv); track.addEventListener("pointerup",up);
  });
  track.addEventListener("keydown", e=>{
    const step = 1/ (stops.length);
    if (e.key==="ArrowRight"){ prog=Math.min(1,prog+step); render(); e.preventDefault(); }
    else if (e.key==="ArrowLeft"){ prog=Math.max(0,prog-step); render(); e.preventDefault(); }
    else if (e.key===" "||e.key==="Enter"){ playing?pause():play(); e.preventDefault(); }
  });

  return {
    autoplayOnce(){ if(played||reduceMotion) { render(); return; } played=true; setTimeout(play, 500); },
    reset(){ pause(); prog=0; render(); }
  };
})();

/* ============================ POINTER PARALLAX ============================ */
if (!reduceMotion && !isMobile){
  const layers = $$(".par");
  let tx=0, ty=0, cx=0, cy=0;
  window.addEventListener("pointermove", e=>{
    tx = (e.clientX/window.innerWidth - .5);
    ty = (e.clientY/window.innerHeight - .5);
  });
  (function damp(){
    cx += (tx-cx)*.06; cy += (ty-cy)*.06;
    layers.forEach(l=>{
      const d = parseFloat(l.dataset.depth||"1");
      l.style.transform = `translate3d(${(-cx*d*10).toFixed(2)}px,${(-cy*d*10).toFixed(2)}px,0)`;
    });
    requestAnimationFrame(damp);
  })();
}

/* ============================ ENQUIRY FORM ============================ */
$("#fSend").addEventListener("click", ()=>{
  const g = id => ($("#"+id).value||"").trim();
  const name=g("fName"), email=g("fEmail");
  const okMail=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
  const ok = $("#fOk");
  if (!name || !okMail){
    ok.className="form-ok show err";
    ok.textContent = "Please add your name and a valid work email so we can reply.";
    $("#"+(!name?"fName":"fEmail")).focus();
    return;
  }
  const lines = [
    "Genesys enquiry via the site","",
    "Name: "+name, "Email: "+email, "Facility: "+g("fFacility"),
    "Tier of interest: "+g("fTier"), "", "Message:", g("fMsg")||"-"
  ].join("\n");
  const mailto = "mailto:cordor@genesys-health.com?subject="+
    encodeURIComponent("Genesys enquiry — "+(g("fFacility")||name))+
    "&body="+encodeURIComponent(lines);
  ok.className="form-ok show";
  ok.innerHTML = `Thank you, ${name.split(" ")[0]}. Choose how to send it: `+
    `<a href="${mailto}" style="color:var(--ok);font-weight:600;margin-left:6px">open email</a>`+
    ` &middot; <a href="https://wa.me/2347047999337?text=${encodeURIComponent(lines)}" target="_blank" rel="noopener" style="color:var(--ok);font-weight:600">WhatsApp</a>`;
});

/* ============================ CAPABILITY GATE ============================ */
function webglOK(){
  try{
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext &&
      (c.getContext("webgl2") || c.getContext("webgl")));
  }catch(e){ return false; }
}
function weakDevice(){
  const mem = navigator.deviceMemory;      // GB, may be undefined
  const cpu = navigator.hardwareConcurrency;
  return (mem && mem <= 2) || (cpu && cpu <= 2);
}

function goFlat(reason){
  document.body.classList.add("is-flat");
  document.documentElement.dataset.flatReason = reason;
}

/* mobile: canvas disabled entirely, page scrolls normally */
if (isMobile) document.body.classList.add("is-mobile");

async function boot(){
  // restore deep-linked tab first, before any 3D
  activate((location.hash||"#overview").slice(1), {push:false});
  runCounters(current);

  if (isMobile || reduceMotion || !webglOK() || weakDevice()){
    goFlat(isMobile ? "mobile" : reduceMotion ? "reduced-motion" : !webglOK() ? "no-webgl" : "weak-device");
    return; // flat mode: no Three.js loaded at all
  }
  // WebGL path — dynamic import so the flat path never pays for it
  try{
    const mod = await import("./scene.js");
    scene = mod.createScene({
      canvas: $("#field"),
      onError: () => { scene = null; goFlat("context-lost"); }
    });
    scene.flyTo(current, true);
  }catch(err){
    console.warn("[genesys] 3D scene failed, using flat mode:", err);
    goFlat("scene-error");
  }
}
boot();
