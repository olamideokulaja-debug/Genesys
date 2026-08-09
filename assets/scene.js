/* ===========================================================================
   GENESYS — WebGL scene (vanilla Three.js, one persistent canvas)
   Six camera anchors inside one environment. GPU points field (one draw call).
   The Journey: one abstract record threads through six departments, each
   igniting and staying lit. DPR capped at 2, 30fps on blur, paused when hidden.
   =========================================================================== */
import * as THREE from "./vendor/three.module.js";

export function createScene({ canvas, onError }){
  const DESKTOP_PARTICLES = 12000;
  const expoOut = p => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p));

  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, powerPreference:"high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));   // DPR cap 2
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 200);
  const camTarget = new THREE.Vector3(0,0,0);

  // context-loss → hand back to the flat fallback
  canvas.addEventListener("webglcontextlost", e => { e.preventDefault(); stop(); onError && onError(); }, false);

  /* ---------------- department nodes (shared across tabs) ---------------- */
  const DEPTS = [
    { name:"Registration", pos:new THREE.Vector3(-6, 1.6, 0) },
    { name:"Consultation", pos:new THREE.Vector3(-3.2,-0.6, 1.8) },
    { name:"Laboratory",   pos:new THREE.Vector3(-0.4, 1.2,-1.6) },
    { name:"Pharmacy",     pos:new THREE.Vector3( 2.4,-0.9, 1.4) },
    { name:"Billing",      pos:new THREE.Vector3( 4.6, 1.4,-0.8) },
    { name:"Discharge",    pos:new THREE.Vector3( 7.0,-0.2, 0.4) }
  ];
  const COL_DIM  = new THREE.Color(0x2b4a7a);
  const COL_LIT  = new THREE.Color(0x39e0ff);

  const nodeGroup = new THREE.Group();
  scene.add(nodeGroup);
  const nodeMeshes = DEPTS.map(d => {
    const geo = new THREE.IcosahedronGeometry(0.7, 1);
    const mat = new THREE.MeshBasicMaterial({ color:COL_DIM.clone(), wireframe:true, transparent:true, opacity:1 });
    const m = new THREE.Mesh(geo, mat); m.position.copy(d.pos);
    const halo = new THREE.Mesh(new THREE.SphereGeometry(0.8,20,20),
      new THREE.MeshBasicMaterial({ color:COL_LIT.clone(), transparent:true, opacity:0, blending:THREE.AdditiveBlending, depthWrite:false }));
    m.add(halo); m.userData.halo = halo; m.userData.lit = 0;
    nodeGroup.add(m); return m;
  });

  /* ambient wireframe volume — the facility shell around the nodes */
  const shell = new THREE.Group();
  for (let i=0;i<10;i++){
    const s = 0.8 + Math.random()*1.6;
    const box = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.BoxGeometry(s,s*0.7,s)),
      new THREE.LineBasicMaterial({ color:0x1c3358, transparent:true, opacity:0.5 }));
    box.position.set((Math.random()-.5)*16, (Math.random()-.5)*6, (Math.random()-.5)*10);
    box.rotation.set(Math.random(),Math.random(),Math.random());
    shell.add(box);
  }
  scene.add(shell);

  /* ---------------- the journey thread ---------------- */
  const curve = new THREE.CatmullRomCurve3(DEPTS.map(d=>d.pos), false, "catmullrom", 0.4);
  const CURVE_SEG = 240;
  const pts = curve.getPoints(CURVE_SEG);
  const threadGeo = new THREE.BufferGeometry().setFromPoints(pts);
  const threadMat = new THREE.LineBasicMaterial({ color:COL_LIT.clone(), transparent:true, opacity:0.9 });
  const thread = new THREE.Line(threadGeo, threadMat);
  threadGeo.setDrawRange(0, 0);   // revealed by journey progress
  scene.add(thread);

  const spark = new THREE.Mesh(new THREE.SphereGeometry(0.16,16,16),
    new THREE.MeshBasicMaterial({ color:0xffffff, transparent:true, opacity:0, blending:THREE.AdditiveBlending, depthWrite:false }));
  scene.add(spark);

  /* ---------------- GPU particle field (one draw call) ---------------- */
  const N = DESKTOP_PARTICLES;
  const pos = new Float32Array(N*3), seed = new Float32Array(N);
  for (let i=0;i<N;i++){
    // centred on the scene origin, wide enough to fill a pulled-back view
    pos[i*3]   = (Math.random()-.5)*46;
    pos[i*3+1] = (Math.random()-.5)*30;
    pos[i*3+2] = (Math.random()-.5)*34 - 4;
    seed[i]    = Math.random()*6.283;
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute("position", new THREE.BufferAttribute(pos,3));
  pGeo.setAttribute("seed", new THREE.BufferAttribute(seed,1));
  const pMat = new THREE.ShaderMaterial({
    uniforms:{ uTime:{value:0}, uSpeed:{value:1}, uOpacity:{value:0.5}, uColor:{value:new THREE.Color(0x39e0ff)} },
    transparent:true, depthWrite:false, blending:THREE.AdditiveBlending,
    vertexShader:`
      attribute float seed; uniform float uTime, uSpeed; varying float vA;
      void main(){
        vec3 p = position;
        float t = uTime*uSpeed;
        p.x += sin(t*0.3 + seed)*0.6;
        p.y += cos(t*0.24 + seed*1.7)*0.5;
        p.z += sin(t*0.19 + seed*2.3)*0.6;
        vA = 0.4 + 0.6*abs(sin(t*0.5 + seed));
        vec4 mv = modelViewMatrix * vec4(p,1.0);
        gl_PointSize = (18.0 / -mv.z);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader:`
      precision mediump float; uniform float uOpacity; uniform vec3 uColor; varying float vA;
      void main(){
        vec2 d = gl_PointCoord - 0.5;
        float m = smoothstep(0.5, 0.0, length(d));
        gl_FragColor = vec4(uColor, m*vA*uOpacity);
      }`
  });
  const points = new THREE.Points(pGeo, pMat);
  scene.add(points);

  /* ---------------- camera anchors ---------------- */
  const ANCHORS = {
    overview:{ pos:new THREE.Vector3(0.5, 5.5, 20),  target:new THREE.Vector3(0.5,0,0) },
    journey: { pos:new THREE.Vector3(-1, 3.2, 12),   target:new THREE.Vector3(0.5,0,0) },
    modules: { pos:new THREE.Vector3(0, 1.5, 13.5),  target:new THREE.Vector3(0.5,0,0) },
    pricing: { pos:new THREE.Vector3(0, 0.5, 24),    target:new THREE.Vector3(0,0,-2) },   // recede
    rollout: { pos:new THREE.Vector3(0.5, 2.0, 15),  target:new THREE.Vector3(0.5,0,0) },
    trust:   { pos:new THREE.Vector3(0.5, 1.0, 18),  target:new THREE.Vector3(0.5,0,0) }
  };
  const TAB_ENERGY = { overview:1, journey:1, modules:0.7, pricing:0.12, rollout:0.5, trust:0.14 };
  camera.position.copy(ANCHORS.overview.pos); camTarget.copy(ANCHORS.overview.target);

  let flyRAF=null;
  function flyTo(name, instant=false){
    const a = ANCHORS[name] || ANCHORS.overview;
    targetEnergy = TAB_ENERGY[name] ?? 0.6;
    allowDrag = (name === "modules");
    if (instant){ camera.position.copy(a.pos); camTarget.copy(a.target); return; }
    if (flyRAF) cancelAnimationFrame(flyRAF);
    const p0 = camera.position.clone(), t0 = camTarget.clone();
    const start = performance.now(), DUR = 1000;   // 0.9–1.2s window
    (function step(now){
      const p = Math.min(1, (now-start)/DUR), e = expoOut(p);
      camera.position.lerpVectors(p0, a.pos, e);
      camTarget.lerpVectors(t0, a.target, e);
      if (p<1) flyRAF = requestAnimationFrame(step);
    })(start);
  }

  /* ---------------- journey progress (driven from app.js transport) ---- */
  let journeyP = 0;
  function journeyProgress(p){
    journeyP = p;
    threadGeo.setDrawRange(0, Math.floor(p * (CURVE_SEG+1)));
    const at = curve.getPoint(Math.min(0.999, Math.max(0.001,p)));
    spark.position.copy(at);
    spark.material.opacity = p>0 && p<1 ? 1 : 0;
    // ignite nodes as the record passes; they stay lit
    DEPTS.forEach((d,i)=>{
      const nodeT = i/(DEPTS.length-1);
      if (p >= nodeT - 0.02) nodeMeshes[i].userData.lit = 1;
      if (p === 0) nodeMeshes[i].userData.lit = 0;
    });
  }

  /* ---------------- modules drag-to-rotate ---------------- */
  let allowDrag=false, dragging=false, lastX=0, lastY=0, spin=0.0, spinY=0;
  canvas.addEventListener("pointerdown", e=>{ if(!allowDrag) return; dragging=true; lastX=e.clientX; lastY=e.clientY; });
  window.addEventListener("pointerup", ()=> dragging=false);
  window.addEventListener("pointermove", e=>{
    if(!dragging) return;
    spin  += (e.clientX-lastX)*0.005;
    spinY += (e.clientY-lastY)*0.003;
    spinY = Math.max(-0.6, Math.min(0.6, spinY));
    lastX=e.clientX; lastY=e.clientY;
  });

  /* ---------------- render loop with throttle + pause ---------------- */
  let energy=1, targetEnergy=1, running=true, focused=true, t=0, lastFrame=0;
  function resize(){
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w,h,true);           // true → also sets canvas CSS size
    camera.aspect = w/h; camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);
  requestAnimationFrame(resize);          // after first layout
  resize();

  window.addEventListener("blur", ()=>focused=false);
  window.addEventListener("focus", ()=>focused=true);
  document.addEventListener("visibilitychange", ()=>{ running = !document.hidden; if(running) loop(performance.now()); });

  function loop(now){
    if (!running) return;
    const minDelta = focused ? 0 : 1000/30;   // throttle to 30fps when blurred
    if (now - lastFrame < minDelta){ requestAnimationFrame(loop); return; }
    const dt = Math.min(0.05, (now-lastFrame)/1000 || 0.016); lastFrame = now;
    t += dt;

    energy += (targetEnergy - energy) * 0.05;
    pMat.uniforms.uTime.value = t;
    pMat.uniforms.uSpeed.value = 0.4 + energy*1.2;
    pMat.uniforms.uOpacity.value = 0.10 + energy*0.5;

    // gentle idle rotation on overview; drag rotation on modules
    shell.rotation.y += dt*0.03*energy;
    nodeGroup.rotation.y += dt*0.05*energy*(allowDrag?0:1) + (allowDrag?0:0);
    if (allowDrag){ nodeGroup.rotation.y += spin*0.15; nodeGroup.rotation.x = spinY; spin*=0.9; }

    // node ignition lerp
    nodeMeshes.forEach(m=>{
      const target = m.userData.lit;
      const cur = m.material.color;
      cur.lerp(m.userData.lit ? COL_LIT : COL_DIM, 0.08);
      m.userData.halo.material.opacity += ((target?0.7:0.12) - m.userData.halo.material.opacity)*0.08;
      const s = 1 + (target?0.14:0)*Math.sin(t*3);
      m.scale.setScalar(s);
    });
    threadMat.opacity = 0.35 + journeyP*0.6;

    camera.lookAt(camTarget);
    renderer.render(scene, camera);
    requestAnimationFrame(loop);
  }
  function stop(){ running=false; }
  requestAnimationFrame(loop);

  return { flyTo, journeyProgress, stop };
}
