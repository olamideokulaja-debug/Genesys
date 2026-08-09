/* Renders the Pricing page from the single source of truth (pricing.config.js)
   in the site's light style. Change figures in pricing.config.js only. */
(function(){
  var P = window.GENESYS_PRICING; if(!P) return;
  var root = document.getElementById("priceRoot"); if(!root) return;

  var tiers = P.tiers.map(function(t){
    var bands = t.bands ? '<div class="pr-bands">' + t.bands.map(function(b){
      return '<div class="pr-band"><span>'+b.band+' &middot; '+b.seats+'</span><b>'+b.price+'</b></div>';
    }).join("") + '</div>' : "";
    var amort = t.setup.amortised ? '<div class="pr-amort">'+t.setup.amortised+'</div>' : "";
    return '<div class="pr-tier reveal">'
      + '<div class="pr-head"><h3>'+t.name+'</h3><p class="pr-who">'+t.forWho+'</p></div>'
      + '<div class="pr-line"><span class="pr-k">Setup, one-time</span><span class="pr-v">'+t.setup.display+'</span>'+amort+'<p class="pr-sub">'+t.setup.includes+'</p></div>'
      + '<div class="pr-line"><span class="pr-k">Subscription</span><span class="pr-v">'+t.recurring.display+' <span class="pr-u">'+t.recurring.unit+'</span></span>'+bands+'<p class="pr-sub">'+t.recurring.detail+'</p></div>'
      + '<div class="pr-line"><span class="pr-k">Seats &amp; support</span><p class="pr-sub">'+t.seatModel+'. '+t.supentry+'.</p></div>'
      + '<a class="btn btn-ghost" href="contact.html">Request a quote</a>'
      + '</div>';
  }).join("");

  var addons = P.addons.map(function(a){
    return '<tr><td>'+a.name+'</td><td class="pr-basis">'+a.basis+'</td><td class="pr-rate">'+a.rate+'</td></tr>';
  }).join("");

  var terms = P.terms.map(function(x){ return '<li>'+x+'</li>'; }).join("");

  root.innerHTML =
    '<div class="pr-grid">'+tiers+'</div>'
    + '<h2 class="pr-h2">Add-ons and overages</h2>'
    + '<div class="pr-tablewrap"><table class="pr-table"><thead><tr><th>Component</th><th>Basis</th><th>Indicative rate</th></tr></thead><tbody>'+addons+'</tbody></table></div>'
    + '<h2 class="pr-h2">Terms</h2><ul class="pr-terms">'+terms+'</ul>'
    + '<p class="pr-note">'+P.note+' '+P.billingModel+'</p>';
})();
