/* ===========================================================================
   GENESYS — homepage hero controller
   Boots the light 3D scene into the hero frame on capable devices; otherwise
   leaves the static hero photo in place. Drives pointer parallax and pauses
   the scene when the hero scrolls out of view.
   =========================================================================== */
const frame  = document.getElementById("heroFrame");
const canvas = document.getElementById("heroField");
if (frame && canvas){
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isMobile = window.matchMedia("(max-width: 767px)").matches;

  function webglOK(){ try{ const c=document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl2")||c.getContext("webgl"))); }catch(e){ return false; } }
  function weakDevice(){ const m=navigator.deviceMemory,c=navigator.hardwareConcurrency; return (m&&m<=2)||(c&&c<=2); }

  // On low-capability or reduced-motion paths keep the photo; nothing else to do.
  if (isMobile || reduceMotion || !webglOK() || weakDevice()){
    // photo stays; hero remains fully functional and on-brand
  } else {
    import("./home-hero.scene.js").then(mod=>{
      const hero = mod.createHero({ canvas, reduceMotion,
        onError: ()=> frame.classList.remove("hero-live") });
      frame.classList.add("hero-live");   // reveals canvas, fades the photo out

      if (!reduceMotion){
        const r = ()=>frame.getBoundingClientRect();
        window.addEventListener("pointermove", e=>{
          const b=r(); if(!b.width) return;
          hero.setPointer((e.clientX-b.left)/b.width-0.5, (e.clientY-b.top)/b.height-0.5);
        }, {passive:true});
      }
      // pause when the hero is not on screen
      if ("IntersectionObserver" in window){
        new IntersectionObserver(es=>{
          es.forEach(en=> hero.setVisible(en.isIntersecting));
        }, {threshold:0.05}).observe(frame);
      }
    }).catch(()=>{ /* photo stays */ });
  }
}
