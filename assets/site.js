(function(){
  var recData={
    emr:{pk:'Recommended \u00b7 1 to 20 beds',h:'Genesys EMR',p:'A clean clinical record at the centre of a small practice, with mid-level automation across the areas you run. Simple enough to operate without an IT department.'},
    clinical:{pk:'Recommended \u00b7 20 to 100 beds',h:'Clinical Specialized Packages',p:'Targeted automation that brings the functions you already part-run up to one standard, without replacing everything at once.'},
    hmis:{pk:'Recommended \u00b7 100 to 500 beds',h:'Genesys HMIS',p:'The ERP-class system: records, finance, pharmacy, laboratory, claims and wards automated across every department on one spine.'},
    standalone:{pk:'Recommended \u00b7 Not a hospital',h:'Stand-alone Packages',p:'Built for labs, pharmacies and imaging centres in the healthcare ecosystem that do not fit routine hospital or clinic classification.'}
  };
  var rec=document.getElementById('rec');
  if(rec){
    var btns=document.querySelectorAll('.scale button');
    btns.forEach(function(b){
      b.addEventListener('click',function(){
        btns.forEach(function(x){x.setAttribute('aria-pressed','false')});
        b.setAttribute('aria-pressed','true');
        var d=recData[b.getAttribute('data-rec')];
        rec.classList.remove('empty');
        rec.innerHTML='<span class="pk">'+d.pk+'</span><h4>'+d.h+'</h4><p>'+d.p+'</p>'+
          '<a href="contact.html">Request a demo of '+d.h+' \u2192</a>';
      });
    });
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
  },{threshold:.1});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  // keep the active tab in view on mobile
  var tabs=document.querySelector('.tabs');
  var cur=document.querySelector('.tab[aria-current="page"]');
  if(tabs&&cur&&tabs.scrollWidth>tabs.clientWidth+4){
    tabs.scrollLeft=cur.offsetLeft-(tabs.clientWidth-cur.offsetWidth)/2;
  }
})();
