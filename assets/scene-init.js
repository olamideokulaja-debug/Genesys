/* ===========================================================================
   GENESYS — 3D init. Boots the shared engine for the hero (which crossfades
   between the render and the photo) and for any page bands marked
   [data-scene3d]. Everything is capability-gated; on weak/mobile/no-webgl/
   reduced-motion paths the static fallbacks stay and no 3D is loaded.
   =========================================================================== */
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isMobile = window.matchMedia("(max-width: 767px)").matches;
function webglOK(){ try{ const c=document.createElement("canvas");
  return !!(window.WebGLRenderingContext && (c.getContext("webgl2")||c.getContext("webgl"))); }catch(e){ return false; } }
function weakDevice(){ const m=navigator.deviceMemory,c=navigator.hardwareConcurrency; return (m&&m<=2)||(c&&c<=2); }
const CAPABLE = !(isMobile || reduceMotion || !webglOK() || weakDevice());

function onView(el, cb){
  if(!("IntersectionObserver" in window)){ cb(true); return; }
  new IntersectionObserver(es=>es.forEach(e=>cb(e.isIntersecting)), {threshold:0.05}).observe(el);
}
function parallax(el, scene){
  if (reduceMotion) return;
  const r=()=>el.getBoundingClientRect();
  window.addEventListener("pointermove", e=>{ const b=r(); if(!b.width) return;
    scene.setPointer((e.clientX-b.left)/b.width-0.5, (e.clientY-b.top)/b.height-0.5); }, {passive:true});
}

async function boot(){
  if (!CAPABLE) return;   // fallbacks stay everywhere
  const hasHero = !!document.getElementById("heroField");
  const bands = document.querySelectorAll("canvas[data-scene3d]");
  if (!hasHero && bands.length === 0) return;   // no 3D on this page → never fetch the engine
  let engine;
  try { engine = await import("./scene3d.js"); }
  catch(e){ return; }

  /* ---- hero: crossfade between the 3D render and the photo ---- */
  const frame = document.getElementById("heroFrame");
  const heroCanvas = document.getElementById("heroField");
  if (frame && heroCanvas){
    let timer = null;
    const hero = engine.createScene({ canvas:heroCanvas, mode:"journey", reduceMotion,
      onError:()=>{ frame.classList.remove("hero-live"); if(timer) clearInterval(timer); } });
    parallax(frame, hero);

    let showing3D = false, onScreen = true;
    function show3D(v){
      showing3D = v;
      frame.classList.toggle("hero-live", v);
      hero.setVisible(v && onScreen);   // don't render during the photo phase
    }
    // start on the photo, then alternate evenly every 7s
    show3D(false);
    setTimeout(()=>{ show3D(true); timer = setInterval(()=>show3D(!showing3D), 7000); }, 5000);
    onView(frame, vis=>{ onScreen=vis; hero.setVisible(showing3D && vis); });
  }

  /* ---- page bands: any [data-scene3d] canvas ---- */
  bands.forEach(cv=>{
    const band = cv.closest(".scene3d-band") || cv.parentElement;
    const scene = engine.createScene({ canvas:cv, mode:cv.dataset.scene3d||"facility", reduceMotion,
      onError:()=> band.classList.remove("s3d-live") });
    band.classList.add("s3d-live");
    parallax(band, scene);
    onView(band, vis=> scene.setVisible(vis));
  });
}
boot();
