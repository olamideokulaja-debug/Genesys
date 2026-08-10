/* Pricing calculator — indicative monthly/annual cost by active-user count,
   derived entirely from pricing.config.js (single source of truth). The 15%
   annual discount is stated in that file's note (from the client proposal). */
(function(){
  var P = window.GENESYS_PRICING; if(!P) return;
  var root = document.getElementById("priceCalc"); if(!root) return;
  var NG = "\u20A6";

  function num(s){ var m=(s||"").replace(/,/g,"").match(/\d+/g); return m?m.map(Number):[]; }
  function fmt(n){ return NG + Math.round(n).toLocaleString("en-NG"); }

  var lite = P.tiers.find(function(t){return t.id==="lite";});
  var std  = P.tiers.find(function(t){return t.id==="standard";});
  var ent  = P.tiers.find(function(t){return t.id==="enterprise";});
  var liteRange = num(lite.recurring.display);                    // [80000,200000]
  var bands = (std.bands||[]).map(function(b){ return { cap: num(b.seats)[0], price: num(b.price)[0], name:b.band }; });
  var entBase = num(ent.recurring.display)[0];                    // 1500000

  function pick(seats){
    if(seats<=4) return { tier:lite, monthly:liteRange, label:"Up to 4 accounts" };
    for(var i=0;i<bands.length;i++){ if(seats<=bands[i].cap) return { tier:std, monthly:[bands[i].price], label:std.name+" \u00b7 "+bands[i].name+" (\u2264"+bands[i].cap+")" }; }
    return { tier:ent, monthly:[entBase], label:"Unlimited seats" };
  }

  root.innerHTML =
    '<div class="calc-head"><span class="eyebrow">Estimate</span>'+
    '<h2>What would it cost my facility?</h2>'+
    '<p class="muted">Move the slider to your number of active staff accounts. Figures are indicative &mdash; a firm quote follows scoping.</p></div>'+
    '<div class="calc-grid">'+
      '<div class="calc-controls">'+
        '<label class="calc-seatlab">Active users: <b id="calcSeatN">25</b></label>'+
        '<input id="calcSeat" class="calc-slider" type="range" min="1" max="150" value="25" step="1" aria-label="Active users">'+
        '<div class="calc-scale"><span>1</span><span>25</span><span>60</span><span>120</span><span>150+</span></div>'+
        '<div class="calc-toggle" role="group" aria-label="Billing period">'+
          '<button id="calcMonthly" class="on" aria-pressed="true">Monthly</button>'+
          '<button id="calcAnnual" aria-pressed="false">Annual <span class="calc-save">&minus;15%</span></button>'+
        '</div>'+
      '</div>'+
      '<div class="calc-out">'+
        '<div class="calc-tier" id="calcTier"></div>'+
        '<div class="calc-figure"><span class="calc-amt" id="calcAmt"></span><span class="calc-per" id="calcPer"></span></div>'+
        '<div class="calc-setup" id="calcSetup"></div>'+
        '<a class="btn btn-primary" href="contact.html">Get a firm quote <span class="arrow">&rarr;</span></a>'+
      '</div>'+
    '</div>';

  var seat=document.getElementById("calcSeat"), seatN=document.getElementById("calcSeatN");
  var amt=document.getElementById("calcAmt"), per=document.getElementById("calcPer");
  var tierEl=document.getElementById("calcTier"), setupEl=document.getElementById("calcSetup");
  var bM=document.getElementById("calcMonthly"), bA=document.getElementById("calcAnnual");
  var annual=false;

  function money(range){
    if(annual){ range = range.map(function(v){ return v*12*0.85; }); }
    return range.length>1 ? fmt(range[0])+" \u2013 "+fmt(range[1]) : fmt(range[0]);
  }
  function paint(){
    var s=parseInt(seat.value,10); seatN.textContent=s;
    var r=pick(s);
    tierEl.textContent=r.label;
    amt.textContent=money(r.monthly);
    per.textContent = annual ? "per year" : "per month";
    setupEl.innerHTML="One-time setup: <b>"+r.tier.setup.display+"</b>";
  }
  function setMode(a){ annual=a; bA.classList.toggle("on",a); bM.classList.toggle("on",!a);
    bA.setAttribute("aria-pressed",a?"true":"false"); bM.setAttribute("aria-pressed",a?"false":"true"); paint(); }
  seat.addEventListener("input", paint);
  bM.addEventListener("click", function(){ setMode(false); });
  bA.addEventListener("click", function(){ setMode(true); });
  paint();
})();
