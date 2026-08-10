/* ===========================================================================
   GENESYS — reusable 3D engine (neon on blue). One engine, three modes:
     journey       one record threads through six departments, lighting each
     constellation the department nodes, drag to rotate
     facility      the connected volume, slow idle rotation
   Additive neon on a blue field. One draw call for particles. DPR capped at 2,
   paused when off-screen or hidden. Used by the hero and by page bands.
   =========================================================================== */
import * as THREE from "./vendor/three.module.js";

export function createScene({ canvas, mode="journey", reduceMotion=false, colors={}, onError }){
  const C = {
    accent: colors.accent || "#39e0ff",
    dim:    colors.dim    || "#2b4a7a",
    particle: colors.particle || "#39e0ff",
    particleOpacity: (colors.particleOpacity!=null?colors.particleOpacity:0.5),
    shell:  colors.shell  || "#1c3358"
  };
  const cx0 = s => new THREE.Color().setStyle((s||"#39e0ff").trim());
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, powerPreference:"high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(mode==="constellation"?50:46, 2.4, 0.1, 200);
  camera.position.set(0.4, mode==="constellation"?1.2:1.6, mode==="constellation"?13.5:15.5);
  const camTarget = new THREE.Vector3(0.4, 0.1, 0);

  canvas.addEventListener("webglcontextlost", e => { e.preventDefault(); running=false; onError && onError(); }, false);

  const COL_DIM = cx0(C.dim);
  const COL_LIT = cx0(C.accent);

  const DEPTS = [
    new THREE.Vector3(-8.2, 0.9, 0.2), new THREE.Vector3(-4.9,-0.7, 1.6),
    new THREE.Vector3(-1.6, 0.8,-1.2), new THREE.Vector3( 1.7,-0.6, 1.3),
    new THREE.Vector3( 5.0, 0.9,-0.7), new THREE.Vector3( 8.3,-0.2, 0.3)
  ];
  const group = new THREE.Group(); scene.add(group);
  const nodes = DEPTS.map(p=>{
    const mat = new THREE.MeshBasicMaterial({ color:COL_DIM.clone(), wireframe:true, transparent:true, opacity:.95 });
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.72,1), mat); m.position.copy(p);
    const halo = new THREE.Mesh(new THREE.SphereGeometry(0.82,18,18),
      new THREE.MeshBasicMaterial({ color:COL_LIT.clone(), transparent:true, opacity:0, blending:THREE.AdditiveBlending, depthWrite:false }));
    m.add(halo); m.userData.halo=halo; m.userData.lit = mode==="constellation"?1:0;
    group.add(m); return m;
  });
  const shellMats=[];
  for (let i=0;i<9;i++){
    const s=0.8+Math.random()*1.5;
    const sm=new THREE.LineBasicMaterial({ color:cx0(C.shell), transparent:true, opacity:.55 });
    shellMats.push(sm);
    const box=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(s,s*.7,s)), sm);
    box.position.set((Math.random()-.5)*20,(Math.random()-.5)*6,(Math.random()-.5)*10-2);
    box.rotation.set(Math.random(),Math.random(),Math.random());
    group.add(box);
  }

  const curve=new THREE.CatmullRomCurve3(DEPTS,false,"catmullrom",0.4);
  const SEG=240, pts=curve.getPoints(SEG);
  const threadGeo=new THREE.BufferGeometry().setFromPoints(pts);
  const threadMat=new THREE.LineBasicMaterial({ color:COL_LIT.clone(), transparent:true, opacity:.85 });
  const thread=new THREE.Line(threadGeo,threadMat);
  threadGeo.setDrawRange(0, mode==="journey"?0:(SEG+1));
  if (mode==="constellation") threadMat.opacity=0.22;
  group.add(thread);
  const spark=new THREE.Mesh(new THREE.SphereGeometry(0.17,16,16),
    new THREE.MeshBasicMaterial({ color:0xffffff, transparent:true, opacity:0, blending:THREE.AdditiveBlending, depthWrite:false }));
  group.add(spark);

  const N=5200; const pos=new Float32Array(N*3), seed=new Float32Array(N);
  for (let i=0;i<N;i++){ pos[i*3]=(Math.random()-.5)*42; pos[i*3+1]=(Math.random()-.5)*22; pos[i*3+2]=(Math.random()-.5)*26-4; seed[i]=Math.random()*6.283; }
  const pGeo=new THREE.BufferGeometry();
  pGeo.setAttribute("position",new THREE.BufferAttribute(pos,3));
  pGeo.setAttribute("seed",new THREE.BufferAttribute(seed,1));
  const pMat=new THREE.ShaderMaterial({
    uniforms:{ uTime:{value:0}, uOpacity:{value:C.particleOpacity}, uColor:{value:cx0(C.particle)} },
    transparent:true, depthWrite:false, blending:THREE.AdditiveBlending,
    vertexShader:`attribute float seed; uniform float uTime; varying float vA;
      void main(){ vec3 p=position; float t=uTime;
        p.x+=sin(t*0.3+seed)*0.6; p.y+=cos(t*0.24+seed*1.7)*0.5; p.z+=sin(t*0.19+seed*2.3)*0.6;
        vA=0.4+0.6*abs(sin(t*0.5+seed));
        vec4 mv=modelViewMatrix*vec4(p,1.0); gl_PointSize=(16.0/-mv.z); gl_Position=projectionMatrix*mv; }`,
    fragmentShader:`precision mediump float; uniform float uOpacity; uniform vec3 uColor; varying float vA;
      void main(){ vec2 d=gl_PointCoord-0.5; float m=smoothstep(0.5,0.0,length(d)); gl_FragColor=vec4(uColor,m*vA*uOpacity); }`
  });
  const points=new THREE.Points(pGeo,pMat); scene.add(points);

  /* journey */
  let jp = mode==="journey"?0:1, phase="run", phaseT=0;
  function setJourney(p){
    jp=p; threadGeo.setDrawRange(0, Math.floor(p*(SEG+1)));
    const at=curve.getPoint(Math.min(0.999,Math.max(0.001,p))); spark.position.copy(at);
    spark.material.opacity=(p>0&&p<1)?1:0;
    DEPTS.forEach((d,i)=>{ if(p>=i/(DEPTS.length-1)-0.02) nodes[i].userData.lit=1; });
    threadMat.opacity=0.25+p*0.6;
  }

  /* constellation drag */
  let dragging=false,lastX=0,lastY=0,spin=0,spinY=0;
  if (mode==="constellation"){
    canvas.style.touchAction="none";
    canvas.addEventListener("pointerdown", e=>{ dragging=true; lastX=e.clientX; lastY=e.clientY; });
    window.addEventListener("pointerup", ()=>dragging=false);
    window.addEventListener("pointermove", e=>{ if(!dragging)return;
      spin+=(e.clientX-lastX)*0.005; spinY+=(e.clientY-lastY)*0.003; spinY=Math.max(-0.6,Math.min(0.6,spinY));
      lastX=e.clientX; lastY=e.clientY; });
  }

  /* pointer parallax */
  let px=0,py=0,cx=0,cy=0;
  function setPointer(nx,ny){ px=nx; py=ny; }

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

    if(mode==="journey"){
      if(!reduceMotion){ phaseT+=dt;
        if(phase==="run"){ setJourney(Math.min(1,jp+dt/11)); if(jp>=1){phase="hold";phaseT=0;} }
        else if(phase==="hold"){ if(phaseT>2.5){phase="fade";phaseT=0;} }
        else if(phase==="fade"){ if(phaseT>1.6){ nodes.forEach(n=>n.userData.lit=0); jp=0; setJourney(0); phase="run"; } }
      } else setJourney(1);
    }

    cx+=(px-cx)*0.05; cy+=(py-cy)*0.05;
    if(mode==="constellation"){
      group.rotation.y += spin*0.02 + (reduceMotion?0:dt*0.05); group.rotation.x = spinY; spin*=0.92;
      group.rotation.y += cx*0.15;
    } else {
      group.rotation.y = (reduceMotion?0:t*0.04) + cx*0.22;
      group.rotation.x = -cy*0.15;
    }

    nodes.forEach(m=>{
      m.material.color.lerp(m.userData.lit?COL_LIT:COL_DIM, 0.07);
      const ho=m.userData.halo.material; ho.opacity += ((m.userData.lit?0.5:0)-ho.opacity)*0.07;
      m.scale.setScalar(1 + (m.userData.lit?0.12:0)*Math.sin(t*3));
    });

    camera.lookAt(camTarget); renderer.render(scene,camera); raf=requestAnimationFrame(frame);
  }
  function start(){ if(!raf && running){ last=performance.now(); raf=requestAnimationFrame(frame); } }
  function pause(){ running=false; if(raf){cancelAnimationFrame(raf); raf=null;} }
  function resume(){ if(!hidden){ running=true; start(); } }
  document.addEventListener("visibilitychange", ()=>{ hidden=document.hidden; if(hidden) pause(); else resume(); });

  function setTheme(nc){
    if(nc.accent){ COL_LIT.setStyle(nc.accent.trim()); threadMat.color.copy(COL_LIT);
      nodes.forEach(m=>m.userData.halo.material.color.copy(COL_LIT)); }
    if(nc.dim) COL_DIM.setStyle(nc.dim.trim());
    if(nc.particle) pMat.uniforms.uColor.value.setStyle(nc.particle.trim());
    if(nc.particleOpacity!=null) pMat.uniforms.uOpacity.value=parseFloat(nc.particleOpacity);
    if(nc.shell) shellMats.forEach(sm=>sm.color.setStyle(nc.shell.trim()));
  }

  resize(); running=true; start();
  return { setPointer, pause, resume, stop:pause, setTheme,
    setVisible(v){ if(v){ running=true; start(); } else pause(); } };
}
