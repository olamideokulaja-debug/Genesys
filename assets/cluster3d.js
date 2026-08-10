/* ===========================================================================
   GENESYS — stylised facility cluster. Glowing pins in a loose 3D cluster,
   one per live facility, with HTML labels that track each pin. Drag to rotate,
   gentle drift, theme-aware. Not a literal map — a stylised constellation of
   where Genesys is already running.
   =========================================================================== */
import * as THREE from "./vendor/three.module.js";

export function createCluster({ canvas, labels=[], labelLayer, colors={}, reduceMotion=false, onError }){
  const accent = (colors.accent||"#39e0ff").trim();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, powerPreference:"high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  renderer.setClearColor(0x000000,0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(46, 2, 0.1, 100);
  camera.position.set(0,0.6,11); const target=new THREE.Vector3(0,0,0);
  canvas.addEventListener("webglcontextlost", e=>{ e.preventDefault(); running=false; onError&&onError(); }, false);

  const cCol = new THREE.Color().setStyle(accent);
  const glowTex=(function(){ const c=document.createElement("canvas"); c.width=c.height=128;
    const g=c.getContext("2d"); const gr=g.createRadialGradient(64,64,0,64,64,64);
    gr.addColorStop(0,"rgba(255,255,255,1)"); gr.addColorStop(.25,"rgba(255,255,255,.55)"); gr.addColorStop(1,"rgba(255,255,255,0)");
    g.fillStyle=gr; g.fillRect(0,0,128,128); return new THREE.CanvasTexture(c); })();

  const group=new THREE.Group(); group.rotation.x=-0.18; group.position.set(3.6,-0.2,0); scene.add(group);
  const n=Math.max(1,labels.length);
  const R=4.0, pins=[];
  for(let i=0;i<n;i++){
    const a=i*2.399963, rad=Math.sqrt((i+0.6)/n)*R;
    const pos=new THREE.Vector3(Math.cos(a)*rad, (Math.random()-.5)*2.6, Math.sin(a)*rad);
    const core=new THREE.Mesh(new THREE.IcosahedronGeometry(0.28,1),
      new THREE.MeshBasicMaterial({ color:cCol.clone(), wireframe:true, transparent:true, opacity:.95 }));
    core.position.copy(pos);
    const glow=new THREE.Sprite(new THREE.SpriteMaterial({ map:glowTex, color:cCol.clone(),
      transparent:true, opacity:.85, blending:THREE.AdditiveBlending, depthWrite:false, depthTest:false }));
    glow.scale.setScalar(1.9); core.add(glow);
    group.add(core); pins.push({core, pos, label:null});
  }
  // faint connective lines pin -> centroid
  const centroid=new THREE.Vector3(0,0,0);
  const lgeo=new THREE.BufferGeometry(); const lp=[];
  pins.forEach(p=>{ lp.push(p.pos.x,p.pos.y,p.pos.z, centroid.x,centroid.y,centroid.z); });
  lgeo.setAttribute("position", new THREE.Float32BufferAttribute(lp,3));
  const lines=new THREE.LineSegments(lgeo, new THREE.LineBasicMaterial({ color:cCol.clone(), transparent:true, opacity:.22 }));
  group.add(lines);

  // labels
  if(labelLayer){
    labelLayer.innerHTML="";
    pins.forEach((p,i)=>{ const el=document.createElement("span"); el.className="gx-pin"; el.textContent=labels[i]||("Site "+(i+1));
      labelLayer.appendChild(el); p.label=el; });
  }

  let dragging=false,lastX=0,lastY=0,spin=0,spinY=0,px=0,py=0,cx=0,cy=0;
  canvas.style.touchAction="none";
  canvas.addEventListener("pointerdown", e=>{ dragging=true; lastX=e.clientX; lastY=e.clientY; });
  window.addEventListener("pointerup", ()=>dragging=false);
  window.addEventListener("pointermove", e=>{ if(dragging){ spin+=(e.clientX-lastX)*0.005; spinY+=(e.clientY-lastY)*0.003; spinY=Math.max(-0.5,Math.min(0.5,spinY)); lastX=e.clientX; lastY=e.clientY; } });
  function setPointer(nx,ny){ px=nx; py=ny; }

  let running=true, t=0, last=0, raf=null, W=2, H=2;
  function resize(){ const r=canvas.getBoundingClientRect(); let w=Math.round(r.width),h=Math.round(r.height);
    if(w<2||h<2){ const pr=canvas.parentElement.getBoundingClientRect(); w=Math.round(pr.width); h=Math.round(pr.height); }
    if(w<2||h<2) return; W=w; H=h; renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix(); }
  window.addEventListener("resize", resize);
  if(window.ResizeObserver){ try{ new ResizeObserver(resize).observe(canvas); }catch(e){} }
  [0,80,300,800].forEach(ms=>setTimeout(()=>requestAnimationFrame(resize),ms));

  const v=new THREE.Vector3();
  function frame(now){
    if(!running){ raf=null; return; }
    const dt=Math.min(0.05,(now-last)/1000||0.016); last=now; t+=dt;
    cx+=(px-cx)*0.05; cy+=(py-cy)*0.05;
    group.rotation.y += spin*0.02 + (reduceMotion?0:dt*0.06); spin*=0.92;
    group.rotation.x = -0.18 + spinY + (reduceMotion?0:Math.sin(t*0.3)*0.03) - cy*0.12;
    group.rotation.y += cx*0.12;
    camera.lookAt(target); renderer.render(scene,camera);
    // position labels
    if(labelLayer){
      pins.forEach(p=>{ if(!p.label) return;
        v.copy(p.pos); p.core.parent.localToWorld(v); v.project(camera);
        const x=(v.x*0.5+0.5)*W, y=(-v.y*0.5+0.5)*H;
        const infront = v.z < 1;
        p.label.style.transform = "translate(-50%,-140%) translate("+x.toFixed(1)+"px,"+y.toFixed(1)+"px)";
        p.label.style.opacity = infront ? "1" : "0";
      });
    }
    raf=requestAnimationFrame(frame);
  }
  function start(){ if(!raf&&running){ last=performance.now(); raf=requestAnimationFrame(frame); } }
  function pause(){ running=false; if(raf){cancelAnimationFrame(raf); raf=null;} }
  document.addEventListener("visibilitychange", ()=>{ if(document.hidden) pause(); else { running=true; start(); } });

  resize(); start();
  return { setPointer, setVisible(v){ if(v){ running=true; start(); } else pause(); }, stop:pause,
    setProgress(){}, setTheme(nc){ if(nc.accent){ cCol.setStyle(nc.accent.trim());
      pins.forEach(p=>{ p.core.material.color.copy(cCol); p.core.children[0].material.color.copy(cCol); });
      lines.material.color.copy(cCol); } } };
}
