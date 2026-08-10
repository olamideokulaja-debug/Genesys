/* ===========================================================================
   GENESYS — homepage dynamics. A rotating hero word, mouse-follow tilt on
   cards, and a typing interoperability terminal. All motion respects
   prefers-reduced-motion, the Lite toggle, and touch devices.
   =========================================================================== */
(function(){
  var root = document.documentElement;
  function still(){ return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || root.getAttribute("data-motion")==="off" || root.hasAttribute("data-lite"); }
  var coarse = window.matchMedia("(pointer: coarse)").matches;

  /* ---- rotating hero word ---- */
  var rot = document.querySelector(".rotword");
  if (rot){
    var words = (rot.getAttribute("data-words")||"").split(",").filter(Boolean);
    if (words.length>1 && !still()){
      var i=0;
      setInterval(function(){
        i=(i+1)%words.length;
        rot.style.opacity="0"; rot.style.transform="translateY(-6px)";
        setTimeout(function(){ rot.textContent=words[i]; rot.style.opacity="1"; rot.style.transform="none"; }, 240);
      }, 2200);
    }
  }

  /* ---- mouse-follow tilt on cards ---- */
  if (!still() && !coarse){
    var tilts = document.querySelectorAll(".route, .card, .tilt");
    tilts.forEach(function(el){
      el.style.transformStyle="preserve-3d";
      el.addEventListener("pointermove", function(e){
        var r=el.getBoundingClientRect();
        var px=(e.clientX-r.left)/r.width-0.5, py=(e.clientY-r.top)/r.height-0.5;
        el.style.transform="perspective(700px) rotateX("+(-py*5).toFixed(2)+"deg) rotateY("+(px*6).toFixed(2)+"deg) translateY(-3px)";
      });
      el.addEventListener("pointerleave", function(){ el.style.transform=""; });
    });
  }

  /* ---- typing interoperability terminal ---- */
  var term = document.getElementById("ioTerm");
  if (term){
    var lines = [
      {t:"$ ", c:"curl https://api.genesys-health.com/fhir/Patient/1042", cls:"cmd"},
      {t:"", c:"HTTP/2 200  \u00b7  FHIR R4  \u00b7  142 ms", cls:"ok"},
      {t:"", c:"{", cls:"j"},
      {t:"", c:"  \"resourceType\": \"Patient\",", cls:"j"},
      {t:"", c:"  \"identifier\": [{ \"system\": \"NHIA\", \"value\": \"\u2022\u2022\u2022\u2022\" }],", cls:"j"},
      {t:"", c:"  \"active\": true,", cls:"j"},
      {t:"", c:"  \"managingOrganization\": \"Genesys HMIS\"", cls:"j"},
      {t:"", c:"}", cls:"j"},
      {t:"", c:"# HL7 v2 \u00b7 ICD-10 \u00b7 offline-first sync \u2713", cls:"cm"}
    ];
    var host = term.querySelector(".term-body");
    function render(full){
      host.innerHTML = lines.map(function(l){ return '<div class="tl '+l.cls+'"><span class="tp">'+l.t+'</span>'+l.c+'</div>'; }).join("");
    }
    if (still()){ render(true); }
    else {
      host.innerHTML="";
      var li=0;
      function typeLine(){
        if (li>=lines.length){ setTimeout(function(){ host.innerHTML=""; li=0; typeLine(); }, 4200); return; }
        var l=lines[li], div=document.createElement("div"); div.className="tl "+l.cls;
        var tp=document.createElement("span"); tp.className="tp"; tp.textContent=l.t; div.appendChild(tp);
        var span=document.createElement("span"); div.appendChild(span); host.appendChild(div);
        var full=l.c, k=0;
        (function ch(){
          span.textContent=full.slice(0,k++);
          if (k<=full.length){ setTimeout(ch, l.cls==="cmd"?26:8); }
          else { li++; setTimeout(typeLine, l.cls==="cmd"?360:90); }
        })();
      }
      // start when scrolled into view
      if ("IntersectionObserver" in window){
        var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); typeLine(); } }); }, {threshold:0.3});
        io.observe(term);
      } else typeLine();
    }
  }
})();
