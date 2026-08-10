/* ===========================================================================
   GENESYS — 3D init. Boots the shared engine for the hero (crossfading with the
   photo) and for [data-scene3d] page bands. Theme-aware (recolours live),
   Lite-aware (no 3D), and reduced-motion-aware. Capability-gated with static
   fallbacks; the engine is only fetched on pages that have 3D.
   =========================================================================== */
const root = document.documentElement;
const isMobile = window.matchMedia("(max-width: 767px)").matches;
function reduceMotion(){ return window.matchMedia("(prefers-reduced-motion: reduce)").matches || root.getAttribute("data-motion")==="off"; }
function lite(){ return root.hasAttribute("data-lite"); }
function webglOK(){ try{ const c=document.createElement("canvas");
  return !!(window.WebGLRenderingContext && (c.getContext("webgl2")||c.getContext("webgl"))); }catch(e){ return false; } }
function weakDevice(){ const m=navigator.deviceMemory,c=navigator.hardwareConcurrency; return (m&&m<=2)||(c&&c<=2); }
function capable(){ return !(isMobile || lite() || reduceMotion() || !webglOK() || weakDevice()); }

function themeColors(){
  const cs=getComputedStyle(root); const g=n=>cs.getPropertyValue(n).trim();
  return { accent:g("--s3d-accent")||"#39e0ff", dim:g("--s3d-dim")||"#2b4a7a",
           particle:g("--s3d-particle")||"#39e0ff",
           particleOpacity:parseFloat(g("--s3d-particle-opacity"))||0.5,
           shell:g("--s3d-shell")||"#1c3358" };
}
function onView(el, cb){
  if(!("IntersectionObserver" in window)){ cb(true); return; }
  new IntersectionObserver(es=>es.forEach(e=>cb(e.isIntersecting)), {threshold:0.05}).observe(el);
}
function parallax(el, scene){
  if (reduceMotion()) return;
  const r=()=>el.getBoundingClientRect();
  window.addEventListener("pointermove", e=>{ const b=r(); if(!b.width) return;
    scene.setPointer((e.clientX-b.left)/b.width-0.5, (e.clientY-b.top)/b.height-0.5); }, {passive:true});
}

window.gxScenes = window.gxScenes || [];
document.addEventListener("gx-theme-change", ()=>{ const c=themeColors(); window.gxScenes.forEach(s=> s.setTheme && s.setTheme(c)); });

let booted = false;
async function boot(){
  if (booted) return;
  const hasHero = !!document.getElementById("heroField");
  const bands = document.querySelectorAll("canvas[data-scene3d]");
  const devices = document.querySelectorAll("canvas[data-device3d]");
  const clusters = document.querySelectorAll("canvas[data-cluster3d]");
  if (!hasHero && !bands.length && !devices.length && !clusters.length) return;
  if (!capable()) return;
  booted = true;

  let engine; try { engine = await import("./scene3d.js"); } catch(e){ booted=false; return; }
  const colors = themeColors();

  const frame = document.getElementById("heroFrame");
  const heroCanvas = document.getElementById("heroField");
  if (frame && heroCanvas){
    let timer = null;
    const hero = engine.createScene({ canvas:heroCanvas, mode:"journey", reduceMotion:reduceMotion(), colors,
      onError:()=>{ frame.classList.remove("hero-live"); if(timer) clearInterval(timer); } });
    window.gxScenes.push(hero); parallax(frame, hero);
    let showing3D=false, onScreen=true;
    function show3D(v){ showing3D=v; frame.classList.toggle("hero-live", v); hero.setVisible(v && onScreen); }
    show3D(false);
    setTimeout(()=>{ show3D(true); timer=setInterval(()=>show3D(!showing3D), 7000); }, 5000);
    onView(frame, vis=>{ onScreen=vis; hero.setVisible(showing3D && vis); });
  }

  const scrubScenes=[];
  bands.forEach(cv=>{
    const band = cv.closest(".scene3d-band") || cv.parentElement;
    const mode = cv.dataset.scene3d || "facility";
    const doScrub = (mode === "journey");
    const scene = engine.createScene({ canvas:cv, mode, reduceMotion:reduceMotion(), colors, scrub:doScrub,
      onError:()=> band.classList.remove("s3d-live") });
    window.gxScenes.push(scene); band.classList.add("s3d-live");
    parallax(band, scene);
    onView(band, vis=> scene.setVisible(vis));
    if (doScrub) scrubScenes.push({scene, band});
  });
  if (scrubScenes.length){
    let ticking=false;
    function upd(){ ticking=false; const vh=window.innerHeight;
      scrubScenes.forEach(o=>{ const r=o.band.getBoundingClientRect();
        const p=Math.max(0,Math.min(1,(vh - r.top)/(vh + r.height))); o.scene.setProgress(p); }); }
    function onScroll(){ if(!ticking){ ticking=true; requestAnimationFrame(upd); } }
    window.addEventListener("scroll", onScroll, {passive:true});
    window.addEventListener("resize", onScroll);
    upd();
  }

  /* 3D laptop showing real screens */
  devices.forEach(async cv=>{
    const stage = cv.closest("[data-device-stage]") || cv.parentElement;
    try{
      const mod = await import("./device3d.js");
      const shots=(cv.dataset.shots||"").split(",").filter(Boolean).map(s=>"assets/shots/"+s+".jpg");
      const dev = mod.createLaptop({ canvas:cv, shots, reduceMotion:reduceMotion(), onError:()=>stage.classList.remove("live") });
      window.gxScenes.push(dev); stage.classList.add("live"); parallax(stage, dev); onView(stage, vis=>dev.setVisible(vis));
    }catch(e){}
  });

  /* stylised facility cluster */
  clusters.forEach(async cv=>{
    const band = cv.closest(".scene3d-band") || cv.parentElement;
    const layer = band.querySelector(".gx-pins");
    try{
      const mod = await import("./cluster3d.js");
      const labels=(cv.dataset.labels||"").split("|").filter(Boolean);
      const cl = mod.createCluster({ canvas:cv, labels, labelLayer:layer, colors, reduceMotion:reduceMotion(), onError:()=>band.classList.remove("s3d-live") });
      window.gxScenes.push(cl); band.classList.add("s3d-live"); parallax(band, cl); onView(band, vis=>cl.setVisible(vis));
    }catch(e){}
  });
}
window.gxBootScenes = function(){ if(!booted) boot(); else window.gxScenes.forEach(s=>s.setVisible(true)); };
boot();
