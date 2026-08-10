/* ===========================================================================
   GENESYS — theme picker. Four themes plus Lite and reduced-motion, persisted
   under functional consent. Colour themes apply live (CSS variables + a 3D
   recolour event). Lite / motion changes persist and reload so the 3D layer is
   rebuilt in the right state (or apply live for the session if consent is off).
   =========================================================================== */
(function(){
  var root = document.documentElement;
  var prefs = function(){ return !!(window.gxPrefsAllowed && window.gxPrefsAllowed()); };
  function save(k,v){ if(prefs()){ try{ localStorage.setItem(k,v); }catch(e){} } }

  var btn = document.getElementById("themeMenuBtn");
  var pop = document.getElementById("themePop");
  if(!btn || !pop) return;

  function curTheme(){ return root.getAttribute("data-theme") || "light"; }
  function syncUI(){
    var t = curTheme();
    Array.prototype.forEach.call(pop.querySelectorAll("[data-theme-set]"), function(b){
      b.setAttribute("aria-pressed", b.getAttribute("data-theme-set")===t ? "true":"false");
    });
    var lt=document.getElementById("liteToggle"), mt=document.getElementById("motionToggle");
    if(lt) lt.checked = root.hasAttribute("data-lite");
    if(mt) mt.checked = root.getAttribute("data-motion")==="off";
  }

  // open / close
  function open(v){ pop.classList.toggle("open", v); btn.setAttribute("aria-expanded", v?"true":"false"); }
  btn.addEventListener("click", function(e){ e.stopPropagation(); open(!pop.classList.contains("open")); });
  document.addEventListener("click", function(e){ if(!pop.contains(e.target) && e.target!==btn) open(false); });
  document.addEventListener("keydown", function(e){ if(e.key==="Escape") open(false); });

  // theme swatches — live
  Array.prototype.forEach.call(pop.querySelectorAll("[data-theme-set]"), function(b){
    b.addEventListener("click", function(){
      var t = b.getAttribute("data-theme-set");
      root.setAttribute("data-theme", t);
      save("gx-theme", t);
      syncUI();
      document.dispatchEvent(new CustomEvent("gx-theme-change", {detail:{theme:t}}));
    });
  });

  // Lite mode
  var lt=document.getElementById("liteToggle");
  if(lt) lt.addEventListener("change", function(){
    if(prefs()){ save("gx-lite", lt.checked?"1":"0"); location.reload(); return; }
    // no consent → apply live for the session
    if(lt.checked){ root.setAttribute("data-lite",""); (window.gxScenes||[]).forEach(function(s){ s.setVisible(false); }); }
    else { root.removeAttribute("data-lite"); if(window.gxBootScenes) window.gxBootScenes(); }
  });

  // Reduce motion
  var mt=document.getElementById("motionToggle");
  if(mt) mt.addEventListener("change", function(){
    root.setAttribute("data-motion", mt.checked?"off":"on");
    if(prefs()){ save("gx-motion", mt.checked?"off":"on"); location.reload(); return; }
  });

  syncUI();
})();
