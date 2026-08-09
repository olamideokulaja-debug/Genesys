/* ===========================================================================
   GENESYS — homepage hero scene (light treatment, white background)
   One connected facility rendered in brand blue on white: department nodes,
   a record thread that cycles through them lighting each in turn, and a soft
   particle field. Normal blending (additive washes out on white). One draw
   call for the field. Sized to the hero frame, paused when off-screen/hidden.
   =========================================================================== */
import * as THREE from "./vendor/three.module.js";

export function createHero({ canvas, onError, reduceMotion=false }){
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, powerPreference:"high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);   // transparent → CSS light gradient shows through

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(46, 2.4, 0.1, 200);
  camera.position.set(0.4, 1.6, 15.5);
  const camTarget = new THREE.Vector3(0.4, 0.1, 0);

  canvas.addEventListener("webglcontextlost", e => { e.preventDefault(); running=false; onError && onError(); }, false);

  const COL_DIM = new THREE.Color(0xA9C4EC);   // light blue-grey
  const COL_LIT = new THREE.Color(0x0B4FC4);   // brand blue
  const COL_HALO= new THREE.Color(0x2E82FF);

  // departments along a gentle horizontal arc (wide hero framing)
  const DEPTS = [
    new THREE.Vector3(-8.2, 0.9, 0.2),
    new THREE.Vector3(-4.9,-0.7, 1.6),
    new THREE.Vector3(-1.6, 0.8,-1.2),
    new THREE.Vector3( 1.7,-0.6, 1.3),
    new THREE.Vector3( 5.0, 0.9,-0.7),
    new THREE.Vector3( 8.3,-0.2, 0.3)
  ];

  const group = new THREE.Group(); scene.add(group);
  const nodes = DEPTS.map(p=>{
    const mat = new THREE.MeshBasicMaterial({ color:COL_DIM.clone(), wireframe:true, transparent:true, opacity:.95 });
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.72,1), mat); m.position.copy(p);
    const halo = new THREE.Mesh(new THREE.SphereGeometry(0.95,20,20),
      new THREE.MeshBasicMaterial({ color:COL_HALO.clone(), transparent:true, opacity:0, depthWrite:false }));
    m.add(halo); m.userData.halo=halo; m.userData.lit=0;
    group.add(m); return m;
  });

  // light structural shell for depth
  for (let i=0;i<8;i++){
    const s=0.8+Math.random()*1.5;
    const box=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(s,s*.7,s)),
      new THREE.LineBasicMaterial({ color:0xCBDDF5, transparent:true, opacity:.6 }));
    box.position.set((Math.random()-.5)*20,(Math.random()-.5)*6,(Math.random()-.5)*10-2);
    box.rotation.set(Math.random(),Math.random(),Math.random());
    group.add(box);
  }

  // record thread
  const curve=new THREE.CatmullRomCurve3(DEPTS,false,"catmullrom",0.4);
  const SEG=240, pts=curve.getPoints(SEG);
  const threadGeo=new THREE.BufferGeometry().setFromPoints(pts);
  const threadMat=new THREE.LineBasicMaterial({ color:COL_LIT.clone(), transparent:true, opacity:.85 });
  const thread=new THREE.Line(threadGeo,threadMat); threadGeo.setDrawRange(0,0); group.add(thread);
  const spark=new THREE.Mesh(new THREE.SphereGeometry(0.17,16,16),
    new THREE.MeshBasicMaterial({ color:0x0B4FC4, transparent:true, opacity:0 }));
  group.add(spark);

  // particle field — normal blending, soft blue on white, one draw call
  const N=5200; const pos=new Float32Array(N*3), seed=new Float32Array(N);
  for (let i=0;i<N;i++){
    pos[i*3]=(Math.random()-.5)*40; pos[i*3+1]=(Math.random()-.5)*22; pos[i*3+2]=(Math.random()-.5)*26-4;
    seed[i]=Math.random()*6.283;
  }
  const pGeo=new THREE.BufferGeometry();
  pGeo.setAttribute("position",new THREE.BufferAttribute(pos,3));
  pGeo.setAttribute("seed",new THREE.BufferAttribute(seed,1));
  const pMat=new THREE.ShaderMaterial({
    uniforms:{ uTime:{value:0}, uOpacity:{value:.42}, uColor:{value:new THREE.Color(0x2E82FF)} },
    transparent:true, depthWrite:false, blending:THREE.NormalBlending,
    vertexShader:`attribute float seed; uniform float uTime; varying float vA;
      void main(){ vec3 p=position; float t=uTime;
        p.x+=sin(t*0.28+seed)*0.6; p.y+=cos(t*0.22+seed*1.7)*0.5; p.z+=sin(t*0.18+seed*2.3)*0.6;
        vA=0.5+0.5*abs(sin(t*0.4+seed));
        vec4 mv=modelViewMatrix*vec4(p,1.0);
        gl_PointSize=(15.0/-mv.z); gl_Position=projectionMatrix*mv; }`,
    fragmentShader:`precision mediump float; uniform float uOpacity; uniform vec3 uColor; varying float vA;
      void main(){ vec2 d=gl_PointCoord-0.5; float m=smoothstep(0.5,0.0,length(d));
        gl_FragColor=vec4(uColor, m*vA*uOpacity); }`
  });
  const points=new THREE.Points(pGeo,pMat); scene.add(points);

  /* ---- journey auto-cycle ---- */
  let jp=0, phase="run", phaseT=0;   // run → hold → fade → run
  function setJourney(p){
    jp=p; threadGeo.setDrawRange(0, Math.floor(p*(SEG+1)));
    const at=curve.getPoint(Math.min(0.999,Math.max(0.001,p)));
    spark.position.copy(at); spark.material.opacity = (p>0&&p<1)?1:0;
    DEPTS.forEach((d,i)=>{ const nt=i/(DEPTS.length-1); if(p>=nt-0.02) nodes[i].userData.lit=1; });
    threadMat.opacity=0.2+p*0.65;
  }

  /* ---- pointer parallax (set from controller) ---- */
  let px=0,py=0,cx=0,cy=0;
  function setPointer(nx,ny){ px=nx; py=ny; }

  /* ---- loop ---- */
  let running=true, hidden=false, t=0, last=0, raf=null;
  function resize(){
    const r=canvas.getBoundingClientRect(); let w=Math.round(r.width),h=Math.round(r.height);
    if(w<2||h<2){ const pr=canvas.parentElement.getBoundingClientRect(); w=Math.round(pr.width); h=Math.round(pr.height); }
    if(w<2||h<2) return;
    renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);
  if(window.ResizeObserver){ try{ new ResizeObserver(resize).observe(canvas); }catch(e){} }
  [0,80,300,800].forEach(ms=>setTimeout(()=>requestAnimationFrame(resize),ms));

  function frame(now){
    if(!running){ raf=null; return; }
    const dt=Math.min(0.05,(now-last)/1000||0.016); last=now; t+=dt;
    pMat.uniforms.uTime.value=t;

    // journey state machine
    if(!reduceMotion){
      phaseT+=dt;
      if(phase==="run"){ setJourney(Math.min(1, jp+dt/11)); if(jp>=1){phase="hold";phaseT=0;} }
      else if(phase==="hold"){ if(phaseT>2.5){phase="fade";phaseT=0;} }
      else if(phase==="fade"){ if(phaseT>1.6){ nodes.forEach(n=>n.userData.lit=0); jp=0; setJourney(0); phase="run"; } }
    } else { setJourney(1); nodes.forEach(n=>n.userData.lit=1); }

    // parallax + idle
    cx+=(px-cx)*0.05; cy+=(py-cy)*0.05;
    const idle = reduceMotion?0:t*0.04;
    group.rotation.y = idle + cx*0.25;
    group.rotation.x = -cy*0.16;

    nodes.forEach(m=>{
      m.material.color.lerp(m.userData.lit?COL_LIT:COL_DIM, 0.07);
      const ho=m.userData.halo.material; ho.opacity += ((m.userData.lit?0.16:0)-ho.opacity)*0.07;
      m.scale.setScalar(1 + (m.userData.lit?0.12:0)*Math.sin(t*3));
    });

    camera.lookAt(camTarget);
    renderer.render(scene,camera);
    raf=requestAnimationFrame(frame);
  }
  function start(){ if(!raf && running){ last=performance.now(); raf=requestAnimationFrame(frame); } }
  function pause(){ running=false; if(raf){cancelAnimationFrame(raf); raf=null;} }
  function resume(){ if(!hidden){ running=true; start(); } }
  document.addEventListener("visibilitychange", ()=>{ hidden=document.hidden; if(hidden) pause(); else resume(); });

  resize(); running=true; start();
  return { setPointer, pause, resume, stop:pause,
    setVisible(v){ if(v){ running=true; start(); } else pause(); } };
}
