/* ===========================================================================
   GENESYS — command palette. Cmd/Ctrl+K (or the nav search button) opens a
   searchable list of every destination; type to filter, arrow keys to move,
   Enter to go. Pure DOM, no dependencies.
   =========================================================================== */
(function(){
  var DESTS = [
    ["Home","index.html","Start"],
    ["How it works","how-it-works.html","Product walkthrough"],
    ["Pricing","pricing.html","Setup and subscription"],
    ["Request a demo","contact.html","Contact"],
    ["Find your system","find-your-system.html","Chooser"],
    ["Why Genesys","the-problem.html","The problem we solve"],
    ["Paper vs Genesys","paper-vs-genesys.html","Comparison"],
    ["Why us","why-genesys.html","Our difference"],
    ["Solutions","solutions.html","All four systems"],
    ["Genesys HMIS","solutions-hmis.html","Large practices"],
    ["Genesys EMR","solutions-emr.html","Small to mid-scale"],
    ["Clinical Specialized Packages","solutions-clinical.html","Specialist modules"],
    ["Stand-alone Packages","solutions-standalone.html","Single modules"],
    ["Who we serve","who-we-serve.html","By facility type"],
    ["Hospitals","serve-hospitals.html","Who we serve"],
    ["Clinics","serve-clinics.html","Who we serve"],
    ["Payers & HMOs","serve-payers.html","Who we serve"],
    ["Public health","serve-public.html","Who we serve"],
    ["Proof","proof.html","Clients and evidence"],
    ["Implementation","implementation.html","Rollout"],
    ["Security & compliance","security.html","NDPA, data protection"],
    ["Insights","insights.html","Articles and news"],
    ["About","about.html","The company"],
    ["Leadership","leadership.html","The team"],
    ["Values","values.html","What we stand for"],
    ["Privacy Notice","privacy.html","NDPA"],
    ["Cookie Notice","cookies.html","Consent"],
    ["Data request","data-request.html","Your data rights"]
  ];

  var overlay, input, list, items = [], active = 0, built = false;

  function build(){
    overlay = document.createElement("div"); overlay.className = "cmdk"; overlay.setAttribute("role","dialog");
    overlay.setAttribute("aria-modal","true"); overlay.setAttribute("aria-label","Search the site");
    overlay.innerHTML =
      '<div class="cmdk-box">'+
      '<div class="cmdk-top"><span class="cmdk-ico" aria-hidden="true">&#9906;</span>'+
      '<input class="cmdk-input" type="text" placeholder="Search pages\u2026" aria-label="Search pages" autocomplete="off">'+
      '<kbd class="cmdk-esc">esc</kbd></div>'+
      '<ul class="cmdk-list" role="listbox"></ul></div>';
    document.body.appendChild(overlay);
    input = overlay.querySelector(".cmdk-input");
    list = overlay.querySelector(".cmdk-list");
    overlay.addEventListener("click", function(e){ if(e.target===overlay) close(); });
    input.addEventListener("input", render);
    input.addEventListener("keydown", onKey);
    built = true;
  }

  function score(q, label){
    label = label.toLowerCase(); q = q.toLowerCase();
    if(!q) return 1;
    if(label.indexOf(q)>=0) return 2;
    var i=0,j=0; while(i<q.length && j<label.length){ if(q[i]===label[j]) i++; j++; }
    return i===q.length ? 0.5 : 0;
  }

  function render(){
    var q = input.value.trim();
    var ranked = DESTS.map(function(d){ return {d:d, s:score(q,d[0]+" "+d[2])}; })
                      .filter(function(r){ return r.s>0; })
                      .sort(function(a,b){ return b.s-a.s; });
    list.innerHTML=""; items=[]; active=0;
    ranked.forEach(function(r,idx){
      var li=document.createElement("li"); li.className="cmdk-item"+(idx===0?" on":"");
      li.setAttribute("role","option");
      li.innerHTML='<span class="cmdk-label">'+r.d[0]+'</span><span class="cmdk-hint">'+r.d[2]+'</span>';
      li.addEventListener("click", function(){ go(r.d[1]); });
      li.addEventListener("mousemove", function(){ setActive(idx); });
      list.appendChild(li); items.push({el:li, url:r.d[1]});
    });
    if(!items.length){ list.innerHTML='<li class="cmdk-empty">No matches</li>'; }
  }
  function setActive(i){
    if(!items.length) return;
    active=(i+items.length)%items.length;
    items.forEach(function(it,idx){ it.el.classList.toggle("on", idx===active); });
    items[active].el.scrollIntoView({block:"nearest"});
  }
  function onKey(e){
    if(e.key==="ArrowDown"){ e.preventDefault(); setActive(active+1); }
    else if(e.key==="ArrowUp"){ e.preventDefault(); setActive(active-1); }
    else if(e.key==="Enter"){ e.preventDefault(); if(items[active]) go(items[active].url); }
    else if(e.key==="Escape"){ e.preventDefault(); close(); }
  }
  function go(url){ close(); window.location.href = url; }
  function open(){ if(!built) build(); overlay.classList.add("show"); input.value=""; render();
    setTimeout(function(){ input.focus(); }, 20); document.documentElement.style.overflow="hidden"; }
  function close(){ if(overlay){ overlay.classList.remove("show"); } document.documentElement.style.overflow=""; }

  document.addEventListener("keydown", function(e){
    if((e.metaKey||e.ctrlKey) && (e.key==="k"||e.key==="K")){ e.preventDefault();
      if(overlay && overlay.classList.contains("show")) close(); else open(); }
    else if(e.key==="/" && !/input|textarea|select/i.test((e.target.tagName||""))){ e.preventDefault(); open(); }
  });
  document.addEventListener("click", function(e){
    var t=e.target.closest && e.target.closest("[data-cmdk-open]");
    if(t){ e.preventDefault(); open(); }
  });
  window.gxOpenPalette = open;
})();
