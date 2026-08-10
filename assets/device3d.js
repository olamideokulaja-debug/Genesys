/* ===========================================================================
   GENESYS — 3D laptop. A stylised laptop that displays the real product
   screenshots on its screen and cycles through them, with gentle idle motion
   and pointer parallax. Sized to its container, paused when off-screen.
   =========================================================================== */
import * as THREE from "./vendor/three.module.js";

export function createLaptop({ canvas, shots=[], reduceMotion=false, onError }){
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, powerPreference:"high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 2, 0.1, 100);
  camera.position.set(0, 1.1, 7.4); camera.lookAt(0, 0.15, 0);

  canvas.addEventListener("webglcontextlost", e=>{ e.preventDefault(); running=false; onError && onError(); }, false);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x223355, 0.9));
  const key = new THREE.DirectionalLight(0xffffff, 1.5); key.position.set(3,6,6); scene.add(key);
  const rim = new THREE.DirectionalLight(0x8fbaff, 0.7); rim.position.set(-5,2,-3); scene.add(rim);

  const laptop = new THREE.Group(); scene.add(laptop);

  // screen aspect from the shots (~2.11); keep the panel matched to avoid distortion
  const SW = 4.0, SH = SW/2.11;
  const bodyMat = new THREE.MeshStandardMaterial({ color:0x2b3446, metalness:0.55, roughness:0.42 });
  const edgeMat = new THREE.MeshStandardMaterial({ color:0x1b2230, metalness:0.6, roughness:0.5 });

  // hinge group holds the lid so it can tilt back
  const lid = new THREE.Group(); laptop.add(lid);
  const bezel = new THREE.Mesh(new THREE.BoxGeometry(SW+0.28, SH+0.28, 0.12), bodyMat);
  lid.add(bezel);

  // screens: two stacked planes for cross-fade between shots
  const loader = new THREE.TextureLoader();
  function tex(url){ const t=loader.load(url, ()=>{}, undefined, ()=>{}); if("colorSpace" in t) t.colorSpace=THREE.SRGBColorSpace; return t; }
  const texes = (shots.length?shots:["assets/shots/login.jpg"]).map(tex);
  const scrGeo = new THREE.PlaneGeometry(SW, SH);
  const scrA = new THREE.Mesh(scrGeo, new THREE.MeshBasicMaterial({ map:texes[0], transparent:true, opacity:1 }));
  const scrB = new THREE.Mesh(scrGeo, new THREE.MeshBasicMaterial({ map:texes[1%texes.length], transparent:true, opacity:0 }));
  scrA.position.z = scrB.position.z = 0.065; lid.add(scrA); lid.add(scrB);

  // base / keyboard deck
  const base = new THREE.Group(); laptop.add(base);
  const deck = new THREE.Mesh(new THREE.BoxGeometry(SW+0.5, 0.16, SH+0.7), bodyMat);
  base.add(deck);
  const pad = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.02, 0.9),
    new THREE.MeshStandardMaterial({ color:0x1a2030, metalness:0.5, roughness:0.5 }));
  pad.position.set(0, 0.09, 0.55); base.add(pad);

  // arrange: deck flat, lid hinged up at the back edge
  const hingeZ = -(SH+0.7)/2;
  base.position.y = -SH/2 - 0.05;
  lid.position.set(0, -SH/2 - 0.05, hingeZ);
  lid.geometryPivot = true;
  // move lid content so its bottom sits on the hinge, then tilt back
  [bezel, scrA, scrB].forEach(m=> m.position.y += SH/2 + 0.14);
  lid.rotation.x = -0.28;                 // slight recline
  laptop.rotation.x = 0.12;

  /* screen cycling with cross-fade */
  let idx=0, cycT=0, fading=false, fadeT=0;
  function startFade(){ if(texes.length<2) return; const next=(idx+1)%texes.length;
    scrB.material.map=texes[next]; scrB.material.needsUpdate=true; fading=true; fadeT=0; }
  /* pointer parallax */
  let px=0,py=0,cx=0,cy=0;
  function setPointer(nx,ny){ px=nx; py=ny; }

  let running=true, hidden=false, t=0, last=0, raf=null;
  function resize(){ const r=canvas.getBoundingClientRect(); let w=Math.round(r.width),h=Math.round(r.height);
    if(w<2||h<2){ const pr=canvas.parentElement.getBoundingClientRect(); w=Math.round(pr.width); h=Math.round(pr.height); }
    if(w<2||h<2) return; renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix(); }
  window.addEventListener("resize", resize);
  if(window.ResizeObserver){ try{ new ResizeObserver(resize).observe(canvas); }catch(e){} }
  [0,80,300,800].forEach(ms=>setTimeout(()=>requestAnimationFrame(resize),ms));

  function frame(now){
    if(!running){ raf=null; return; }
    const dt=Math.min(0.05,(now-last)/1000||0.016); last=now; t+=dt;
    if(!reduceMotion){
      cycT+=dt; if(!fading && cycT>3.4){ cycT=0; startFade(); }
      if(fading){ fadeT+=dt; const k=Math.min(1,fadeT/0.6); scrB.material.opacity=k; scrA.material.opacity=1-k;
        if(k>=1){ fading=false; idx=(idx+1)%texes.length; scrA.material.map=texes[idx]; scrA.material.needsUpdate=true;
          scrA.material.opacity=1; scrB.material.opacity=0; } }
    }
    cx+=(px-cx)*0.05; cy+=(py-cy)*0.05;
    laptop.rotation.y = (reduceMotion?0:Math.sin(t*0.4)*0.12) + cx*0.4;
    laptop.rotation.x = 0.12 - cy*0.18;
    renderer.render(scene,camera); raf=requestAnimationFrame(frame);
  }
  function start(){ if(!raf && running){ last=performance.now(); raf=requestAnimationFrame(frame); } }
  function pause(){ running=false; if(raf){cancelAnimationFrame(raf); raf=null;} }
  document.addEventListener("visibilitychange", ()=>{ hidden=document.hidden; if(hidden) pause(); else { running=true; start(); } });

  resize(); start();
  return { setPointer, setVisible(v){ if(v){ running=true; start(); } else pause(); }, stop:pause,
    setTheme(){}, setProgress(){} };
}
