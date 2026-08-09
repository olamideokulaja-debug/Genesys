# -*- coding: utf-8 -*-
"""Body markup + script tags for the embedded holographic experience page.
Imported by build.py. Everything is scoped under #gx / .gx so it cannot collide
with the surrounding site. Tabs deep-link within the stage; CTAs route out to
the real pages of the site."""

EXP_SCRIPTS = (
  '<script src="assets/pricing.config.js?v=__XPRICEV__"></script>\n'
  '<script type="module" src="assets/experience.app.js?v=__XAPPV__"></script>'
)

EXP_BODY = r"""
<main id="main">
<section id="gx" class="gx" aria-label="Interactive walkthrough of Genesys">
  <div class="gx-stagewrap">
    <canvas class="gx-field" id="gxfield" aria-hidden="true"></canvas>
    <svg class="gx-flatsvg" id="gxFlat" aria-hidden="true" viewBox="0 0 1440 760" preserveAspectRatio="xMidYMid slice">
      <defs>
        <radialGradient id="gxfg" cx="50%" cy="6%" r="120%">
          <stop offset="0%" stop-color="#0a1630"/><stop offset="55%" stop-color="#050912"/><stop offset="100%" stop-color="#03060e"/>
        </radialGradient>
        <linearGradient id="gxedge" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#39E0FF" stop-opacity="0"/><stop offset="100%" stop-color="#39E0FF" stop-opacity=".5"/>
        </linearGradient>
      </defs>
      <rect width="1440" height="760" fill="url(#gxfg)"/>
      <g fill="none" stroke="#1c3358" stroke-width="1.2">
        <path d="M320 430 L540 340 L740 450 L920 360 L1100 470 L1290 400" stroke="url(#gxedge)" stroke-width="1.6"/>
        <circle cx="320" cy="430" r="24" stroke="#39E0FF"/><circle cx="320" cy="430" r="5" fill="#39E0FF" stroke="none"/>
        <circle cx="540" cy="340" r="24"/><circle cx="740" cy="450" r="24"/>
        <circle cx="920" cy="360" r="24"/><circle cx="1100" cy="470" r="24"/><circle cx="1290" cy="400" r="24"/>
        <g opacity=".5">
          <rect x="420" y="220" width="66" height="48" transform="rotate(12 453 244)"/>
          <rect x="880" y="540" width="76" height="56" transform="rotate(-9 918 568)"/>
          <rect x="1160" y="270" width="60" height="44" transform="rotate(18 1190 292)"/>
        </g>
      </g>
    </svg>

    <div class="gx-bar">
      <span class="gx-kick">Interactive &middot; the whole facility, one record</span>
      <div class="gx-tabs" role="tablist" aria-label="Walkthrough sections">
        <button class="gx-tab" role="tab" id="gx-tab-overview"  aria-controls="gx-panel-overview"  aria-selected="true"><span class="i">01</span>Overview</button>
        <button class="gx-tab" role="tab" id="gx-tab-journey"   aria-controls="gx-panel-journey"   aria-selected="false" tabindex="-1"><span class="i">02</span>Journey</button>
        <button class="gx-tab" role="tab" id="gx-tab-modules"   aria-controls="gx-panel-modules"   aria-selected="false" tabindex="-1"><span class="i">03</span>Modules</button>
        <button class="gx-tab" role="tab" id="gx-tab-pricing"   aria-controls="gx-panel-pricing"   aria-selected="false" tabindex="-1"><span class="i">04</span>Pricing</button>
        <button class="gx-tab" role="tab" id="gx-tab-rollout"   aria-controls="gx-panel-rollout"   aria-selected="false" tabindex="-1"><span class="i">05</span>Rollout</button>
        <button class="gx-tab" role="tab" id="gx-tab-trust"     aria-controls="gx-panel-trust"     aria-selected="false" tabindex="-1"><span class="i">06</span>Trust</button>
      </div>
    </div>

    <div class="gx-stage">
      <!-- OVERVIEW -->
      <section class="gx-panel" id="gx-panel-overview" role="tabpanel" aria-labelledby="gx-tab-overview" data-active="true" tabindex="0">
        <div class="gx-in gx-stagger">
          <span class="gx-eyebrow">The hospital as one connected system</span>
          <h2 class="gx-hxl gx-par" data-depth="3">Run the whole facility<br>from one record.</h2>
          <p class="gx-lede gx-par" data-depth="2">Front desk, wards, laboratory, pharmacy, billing and claims sit on one patient record, so the facility reports as one organisation rather than a set of disconnected departments. Move through the sections to see how.</p>
          <div class="gx-row" style="margin-top:20px">
            <button class="gx-btn gx-btn-primary" data-gx-goto="journey">See a record move through it &rarr;</button>
            <a class="gx-btn gx-btn-ghost" href="how-it-works.html">Watch real screens</a>
          </div>
          <div class="gx-grid gx-g4 gx-par" data-depth="1" style="margin-top:28px">
            <div class="gx-card gx-stat"><div class="gx-scan"></div><div class="n" data-count="8">0</div><div class="l">facilities live across Lagos today</div></div>
            <div class="gx-card gx-stat"><div class="n" data-count="12">0</div><div class="l">functional areas on one spine</div></div>
            <div class="gx-card gx-stat"><div class="n" data-count="2017" data-plain="1">0</div><div class="l">building health systems in Lagos since</div></div>
            <div class="gx-card gx-stat"><div class="n" data-count="1">0</div><div class="l">patient record, every department</div></div>
          </div>
          <p class="gx-illus" style="margin-top:16px">Illustrative &mdash; figures describe the deployment footprint, not audited performance.</p>
        </div>
      </section>

      <!-- JOURNEY -->
      <section class="gx-panel" id="gx-panel-journey" role="tabpanel" aria-labelledby="gx-tab-journey" data-active="false" tabindex="0">
        <div class="gx-in gx-stagger">
          <span class="gx-eyebrow">The journey of one record</span>
          <h2 class="gx-hlg">Watch a single record light up the whole facility.</h2>
          <p class="gx-lede">One record moves from registration to discharge. Each department it touches stays lit, so by the end the entire facility is illuminated by one patient having passed through it. That is interoperability, shown rather than claimed.</p>
          <div class="gx-card" style="margin-top:18px">
            <div class="gx-scan"></div>
            <div class="gx-row" style="justify-content:space-between;align-items:flex-start">
              <div><div class="mono" style="color:var(--gx-neon);font-size:12px;letter-spacing:.08em">RECORD IN MOTION</div>
                <div class="gx-muted" style="font-size:13px;margin-top:4px">An abstract record. No name, no number, no clinical detail.</div></div>
              <span class="gx-illus">Illustrative</span>
            </div>
            <div class="gx-transport" role="group" aria-label="Journey playback">
              <button class="gx-tp-btn" id="gxPlay" aria-label="Play or pause the journey">
                <svg id="gxIcon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 3l9 5-9 5z"/></svg>
              </button>
              <div class="gx-tp-track" id="gxTrack" role="slider" aria-label="Journey progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" tabindex="0">
                <div class="gx-tp-fill" id="gxFill"></div>
              </div>
            </div>
            <div class="gx-tp-stops" aria-hidden="true">
              <span class="gx-tp-stop">Registration</span><span class="gx-tp-stop">Consultation</span><span class="gx-tp-stop">Laboratory</span>
              <span class="gx-tp-stop">Pharmacy</span><span class="gx-tp-stop">Billing</span><span class="gx-tp-stop">Discharge</span>
            </div>
          </div>
          <div class="gx-grid gx-g3" style="margin-top:14px">
            <div class="gx-card"><h4 class="mono" style="color:var(--gx-neon);font-size:12px;letter-spacing:.06em">FINDABLE</h4><p class="gx-body" style="margin-top:6px">The same history reachable at 2am with one clerk on duty, not filed in an archive room.</p></div>
            <div class="gx-card"><h4 class="mono" style="color:var(--gx-neon);font-size:12px;letter-spacing:.06em">COMPLETE</h4><p class="gx-body" style="margin-top:6px">Results, prescriptions and claims attach to the record instead of waiting to be filed.</p></div>
            <div class="gx-card"><h4 class="mono" style="color:var(--gx-neon);font-size:12px;letter-spacing:.06em">BILLED</h4><p class="gx-body" style="margin-top:6px">Care delivered becomes money owed at the point of care, not reconstructed at month end.</p></div>
          </div>
        </div>
      </section>

      <!-- MODULES -->
      <section class="gx-panel" id="gx-panel-modules" role="tabpanel" aria-labelledby="gx-tab-modules" data-active="false" tabindex="0">
        <div class="gx-in gx-stagger">
          <span class="gx-eyebrow">Twelve functional areas, one spine</span>
          <h2 class="gx-hlg">Every department, on the same record.</h2>
          <p class="gx-lede">Genesys HMIS is ERP-class: twelve functional areas that share one patient record. Depth of modules scales by tier, shown under Pricing. For the full picture of each, visit the solutions pages.</p>
          <div class="gx-grid gx-g3" style="margin-top:18px">
            <div class="gx-mod gx-card"><div class="gx-scan"></div><h4>Patient &amp; front desk</h4><ul><li>Registration</li><li>Appointment scheduling</li><li>Patient triaging</li><li>Queue management</li></ul></div>
            <div class="gx-mod gx-card"><h4>Nurse workbench</h4><ul><li>Nursing services</li><li>Immunisation</li><li>Antenatal &amp; delivery suite</li><li>Inpatient suite</li></ul></div>
            <div class="gx-mod gx-card"><h4>Doctor workbench</h4><ul><li>GP &amp; specialty templates</li><li>Obstetrics &amp; gynaecology</li><li>Newborn examination</li><li>CPOE order entry</li></ul></div>
            <div class="gx-mod gx-card"><h4>Laboratory</h4><ul><li>Sample collection &amp; results</li><li>Advanced lab workflow <span class="mono gx-muted">Std+</span></li><li>Retail laboratory <span class="mono gx-muted">Std+</span></li></ul></div>
            <div class="gx-mod gx-card"><h4>Pharmacy</h4><ul><li>Medication vetting &amp; dispensing</li><li>Retail pharmacy <span class="mono gx-muted">Std+</span></li></ul></div>
            <div class="gx-mod gx-card"><h4>Radiology</h4><ul><li>Image upload &amp; result entry</li><li>Retail radiology <span class="mono gx-muted">Std+</span></li></ul></div>
            <div class="gx-mod gx-card"><h4>Theatre &amp; critical care</h4><ul><li>Theatre booking &amp; surgery <span class="mono gx-muted">Std+</span></li><li class="no">Accident &amp; emergency <span class="mono gx-muted">Ent</span></li><li class="no">ICU <span class="mono gx-muted">Ent</span></li></ul></div>
            <div class="gx-mod gx-card"><h4>Billing &amp; finance</h4><ul><li>Automated billing &amp; receipts</li><li>Corporate &amp; insurance profiles</li><li>HMO &amp; NHIA claims</li></ul></div>
            <div class="gx-mod gx-card"><h4>Inventory &amp; management</h4><ul><li>Inventory management</li><li>Audit trail</li><li>Report builder <span class="mono gx-muted">Std+</span></li><li class="no">Procurement &amp; manager dashboard <span class="mono gx-muted">Ent</span></li></ul></div>
            <div class="gx-mod gx-card" style="display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
              <h4>See each in depth</h4><p class="gx-body" style="margin:0 0 12px">Full module detail lives on the solutions pages.</p>
              <a class="gx-btn gx-btn-ghost" href="solutions-hmis.html">Genesys HMIS &rarr;</a></div>
          </div>
          <p class="gx-muted" style="margin-top:12px;font-size:13px"><span class="mono">Std+</span> included from Standard. <span class="mono">Ent</span> Enterprise only. Full matrix under Pricing.</p>
        </div>
      </section>

      <!-- PRICING -->
      <section class="gx-panel" id="gx-panel-pricing" role="tabpanel" aria-labelledby="gx-tab-pricing" data-active="false" tabindex="0">
        <div class="gx-in">
          <span class="gx-eyebrow plain">Commercial model</span>
          <h2 class="gx-hlg">Setup and subscription, as separate lines.</h2>
          <p class="gx-lede">A facility budgets capital and operating spend from different envelopes, so setup fee and recurring subscription are shown separately, never collapsed. Recurring cost is banded by active users rather than charged per individual seat.</p>
          <div class="gx-price-grid" id="gxPriceGrid" style="margin-top:18px"></div>
          <h3 class="gx-hlg" style="font-size:22px;margin:26px 0 6px">Add-ons and overages</h3>
          <table class="gx-ptable" id="gxAddonTable"><thead><tr><th>Component</th><th>Basis</th><th>Indicative rate</th></tr></thead><tbody></tbody></table>
          <p class="gx-pnote" id="gxPriceNote"></p>
          <div class="gx-row" style="margin-top:16px">
            <a class="gx-btn gx-btn-primary" href="contact.html">Request a quote &rarr;</a>
            <a class="gx-btn gx-btn-ghost" href="mailto:cordor@genesys-health.com?subject=Genesys%20pricing%20enquiry">cordor@genesys-health.com</a>
          </div>
        </div>
      </section>

      <!-- ROLLOUT -->
      <section class="gx-panel" id="gx-panel-rollout" role="tabpanel" aria-labelledby="gx-tab-rollout" data-active="false" tabindex="0">
        <div class="gx-in gx-stagger">
          <span class="gx-eyebrow">Implementation roadmap</span>
          <h2 class="gx-hlg">Brought live in sequence, never all at once.</h2>
          <p class="gx-lede">Large deployments roll out in five stages, grouped into three phases, so departments come online in an order that keeps the facility operating throughout. Durations are indicative and confirmed at scoping.</p>
          <div class="gx-grid gx-g3" style="margin-top:18px">
            <div class="gx-phase gx-card"><div class="gx-scan"></div><span class="ph">Phase 1 &mdash; Foundation</span><h4>Scope &amp; core records</h4><div class="dur">7 to 12 weeks</div>
              <div class="stages"><div class="stg"><b>Stage 1.</b> Scoping and data audit: map departments, records and systems. <span class="gx-muted mono">4&ndash;6 wks</span></div>
              <div class="stg"><b>Stage 2.</b> Core records and registration go live first. <span class="gx-muted mono">3&ndash;6 wks</span></div></div></div>
            <div class="gx-phase gx-card"><span class="ph">Phase 2 &mdash; Clinical</span><h4>Departmental modules</h4><div class="dur">4 to 8 weeks</div>
              <div class="stages"><div class="stg"><b>Stage 3.</b> Wards, laboratory, pharmacy and theatre brought on in sequence. <span class="gx-muted mono">4&ndash;8 wks</span></div></div></div>
            <div class="gx-phase gx-card"><span class="ph">Phase 3 &mdash; Operational</span><h4>Finance, claims &amp; handover</h4><div class="dur">10 to 18 weeks</div>
              <div class="stages"><div class="stg"><b>Stage 4.</b> Finance, HMO/NHIA claims and management reporting close the loop. <span class="gx-muted mono">8&ndash;16 wks</span></div>
              <div class="stg"><b>Stage 5.</b> Handover, training, documentation and a named support line. <span class="gx-muted mono">2 wks</span></div></div></div>
          </div>
          <div class="gx-row" style="margin-top:16px"><a class="gx-btn gx-btn-ghost" href="implementation.html">Full implementation detail &rarr;</a></div>
          <p class="gx-muted" style="margin-top:10px;font-size:13px">Five stages as set out in the pricing proposal, grouped here into three phases. Timeline confirmed in writing at scoping, before work begins.</p>
        </div>
      </section>

      <!-- TRUST -->
      <section class="gx-panel" id="gx-panel-trust" role="tabpanel" aria-labelledby="gx-tab-trust" data-active="false" tabindex="0">
        <div class="gx-in">
          <span class="gx-eyebrow plain">Data protection &amp; support</span>
          <h2 class="gx-hlg">What a facility is trusting us with.</h2>
          <div class="gx-grid gx-g2" style="margin-top:16px;align-items:start">
            <div>
              <div class="gx-trust-list">
                <div class="gx-trust-item"><b>Nigeria Data Protection Act 2023.</b><p>Data handling is aligned to the NDPA 2023 and the oversight of the Nigeria Data Protection Commission. In a deployment, the facility is the data controller and Genesys is the data processor under a written agreement.</p></div>
                <div class="gx-trust-item"><b>The facility owns its data.</b><p>The facility retains ownership of all patient data at all times. Export is available on request and guaranteed for a defined window after termination.</p></div>
                <div class="gx-trust-item"><b>Offline-first by design.</b><p>Built for real power and bandwidth. The facility keeps working through interruptions, capturing data locally and syncing when connectivity returns.</p></div>
                <div class="gx-trust-item"><b>Interoperable and coded.</b><p>HL7 v2 and FHIR resources for orders, results and identifiers; ICD-10 diagnosis coding; NHIA and HMO claim formats.</p></div>
                <div class="gx-trust-item"><b>Hosting and residency.</b><p><span class="mono gx-muted">[Hosting location and data residency arrangement: to be confirmed with Genesys before publication.]</span></p></div>
              </div>
              <p class="gx-muted" style="margin-top:14px;font-size:12.5px">We make no claim of certification, accreditation or approval that is not evidenced. Support: Lite 24-hour, Standard 8-hour, Enterprise 4-hour with a dedicated account manager, Custom 24/7 with an SLA-backed uptime target. See <a href="security.html">Security &amp; compliance</a>.</p>
            </div>
            <div class="gx-card">
              <h3 style="font-size:20px;margin-bottom:4px;color:#fff">Request a quote or a demo</h3>
              <p class="gx-muted" style="font-size:13.5px;margin-bottom:16px">We reply within one business day.</p>
              <div class="gx-field-row"><label for="gxName">Full name</label><input id="gxName" type="text" autocomplete="name"></div>
              <div class="gx-field-row"><label for="gxEmail">Work email</label><input id="gxEmail" type="email" autocomplete="email"></div>
              <div class="gx-field-row"><label for="gxFacility">Facility</label><input id="gxFacility" type="text"></div>
              <div class="gx-field-row"><label for="gxTier">Tier of interest</label>
                <select id="gxTier"><option>Not sure yet</option><option>GeneSys Lite</option><option>GeneSys Standard</option><option>GeneSys Enterprise</option><option>GeneSys Custom</option></select></div>
              <div class="gx-field-row"><label for="gxMsg">Anything else</label><textarea id="gxMsg" placeholder="Rough staff count, current systems, timelines."></textarea></div>
              <button class="gx-btn gx-btn-primary" id="gxSend" style="width:100%;justify-content:center">Send enquiry &rarr;</button>
              <div class="gx-form-ok" id="gxOk"></div>
            </div>
          </div>
        </div>
      </section>
    </div><!-- /gx-stage -->
  </div><!-- /gx-stagewrap -->

  <!-- belt: route back into the real site -->
  <div class="gx-belt">
    <div class="gx-belt-in">
      <span class="gx-eyebrow">Go deeper</span>
      <h2>This is the short version. The full site has the detail.</h2>
      <p>The walkthrough above is a summary. Every claim, screen and number is covered in depth across the site.</p>
      <div class="gx-links">
        <a class="gx-link" href="how-it-works.html"><span class="lk">Screens</span><h4>How it works</h4><p>Real screens from a live Genesys deployment, chapter by chapter.</p></a>
        <a class="gx-link" href="solutions.html"><span class="lk">Products</span><h4>Solutions</h4><p>HMIS, EMR, clinical packages and stand-alone systems compared.</p></a>
        <a class="gx-link" href="proof.html"><span class="lk">Evidence</span><h4>Proof</h4><p>Case studies and the facilities already running Genesys.</p></a>
        <a class="gx-link" href="implementation.html"><span class="lk">Delivery</span><h4>Implementation</h4><p>What happens after you sign, stage by stage.</p></a>
        <a class="gx-link" href="security.html"><span class="lk">Compliance</span><h4>Security</h4><p>How health data is held, protected and governed.</p></a>
        <a class="gx-link" href="contact.html"><span class="lk">Talk to us</span><h4>Contact</h4><p>Request a quote or a demo. We reply within a business day.</p></a>
      </div>
    </div>
  </div>
</section>
</main>
"""
