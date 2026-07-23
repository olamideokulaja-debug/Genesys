#!/usr/bin/env python3
"""Build the Genesys site: 7 pages, shared nav/footer, interactive components."""
import pathlib
OUT = pathlib.Path(__file__).parent
TABS = [("index.html","Home"),("solutions.html","Solutions"),("who-we-serve.html","Who we serve"),
        ("proof.html","Proof"),("about.html","About"),("insights.html","Insights"),("contact.html","Contact")]
LOGO = '<img src="assets/genesys-logo.png" srcset="assets/genesys-logo.png 1x, assets/genesys-logo@2x.png 2x" alt="Genesys" height="30">'
SUN = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2'
       'M5 5l1.5 1.5M17.5 17.5 19 19M19 5l-1.5 1.5M6.5 17.5 5 19"/></svg>')

MEGA = """
    <div class="mega" id="mega">
      <div class="mega-grid">
        <a class="mega-item" href="solutions.html"><span class="mi-k">Large practices</span><h4>Genesys HMIS</h4><p>ERP-class automation across every department on one spine.</p></a>
        <a class="mega-item" href="solutions.html"><span class="mi-k">Small to mid</span><h4>Genesys EMR</h4><p>A clean clinical record at the centre of the consultation.</p></a>
        <a class="mega-item" href="solutions.html"><span class="mi-k">Small to mid</span><h4>Clinical Packages</h4><p>Targeted modules for practices already running some IT.</p></a>
        <a class="mega-item" href="solutions.html"><span class="mi-k">Non-hospital</span><h4>Stand-alone</h4><p>For laboratories, pharmacies and imaging centres.</p></a>
      </div>
      <div class="mega-foot"><span>Not sure which fits? The chooser takes 10 seconds.</span>
        <a class="btn btn-primary" href="index.html#chooser">Find my system <span class="arrow">&rarr;</span></a></div>
    </div>"""

def head(t,d):
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>"""

def nav(cur):
    tabs=""
    for h,l in TABS:
        cls="tab has-mega" if h=="solutions.html" else "tab"
        aria=' aria-current="page"' if h==cur else ''
        tabs+=f'<a class="{cls}" href="{h}"{aria}>{l}</a>'
    return f"""
<header class="nav">
  <div class="wrap nav-top">
    <a class="brand" href="index.html" aria-label="Genesys Health home">{LOGO}</a>
    <div class="nav-actions">
      <span class="lang" title="French coming soon"><b>EN</b> / FR</span>
      <button class="iconbtn" id="themeBtn" aria-label="Switch colour theme">{SUN}</button>
      <a class="btn btn-primary" href="contact.html">Request a demo</a>
    </div>
  </div>
  <div class="tabrow"><div class="wrap"><nav class="tabs" aria-label="Main">{tabs}</nav></div>{MEGA}</div>
</header>"""

def cta(h="See Genesys running on your own facility's workflow."):
    return f"""
<section class="tight">
  <div class="wrap"><div class="cta reveal"><h2>{h}</h2>
    <div style="display:flex;gap:11px;flex-wrap:wrap">
      <a class="btn btn-white" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
      <a class="btn btn-ghost" href="contact.html">Chat on WhatsApp</a></div>
  </div></div>
</section>"""

MARQUEE_ITEMS = ["NDPR aligned","HL7 / FHIR ready","ICD-10 coded","Offline-first architecture",
                 "NHIA &amp; HMO claims","Multi-site reporting","Role-based access","Data export on request"]
def marquee():
    items="".join(f'<span class="mq-item">{i}</span>' for i in MARQUEE_ITEMS)
    return f'<div class="marquee"><div class="mq-track">{items}{items}</div></div>'

FOOT = f"""
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div><div class="brand" style="margin-bottom:12px">{LOGO}</div>
        <p class="addr">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos<br><br>+234 903 600 1000<br>info@genesys-health.com</p></div>
      <div class="fcol"><h4>Solutions</h4><a href="solutions.html">Genesys HMIS</a><a href="solutions.html">Genesys EMR</a><a href="solutions.html">Clinical Packages</a><a href="solutions.html">Stand-alone Packages</a></div>
      <div class="fcol"><h4>Company</h4><a href="about.html">About</a><a href="about.html">The team</a><a href="proof.html">Proof</a><a href="insights.html">Insights</a></div>
      <div class="fcol"><h4>Stay in the loop</h4><p class="addr" style="margin-bottom:4px">News on Genesys and African health tech.</p>
        <div class="news"><input type="email" placeholder="Your email address" aria-label="Email address"><button type="button">&rarr;</button></div></div>
    </div>
    <div class="foot-base"><span>&copy; 2026 Genesys Health Information Systems Limited.</span><span>Privacy &middot; Terms &middot; Sitemap</span></div>
  </div>
</footer>
<div class="mobar">
  <a class="btn btn-primary" href="contact.html">Request a demo</a>
  <a class="btn btn-ghost" href="contact.html">WhatsApp</a>
</div>
<script src="assets/site.js"></script>
</body>
</html>"""

def page(f,t,d,body):
    (OUT/f).write_text(head(t,d)+nav(f)+body+FOOT); return f

# ---------------------------------------------------------------- HOME
BLEEDS=[("Fragmented record management","The history exists; nobody can find it in time.","record loss",
         "A single patient record, searchable across every department and site.","78%"),
        ("No reliable data for decisions","The facility is flown blind.","blind spend",
         "Live dashboards on occupancy, revenue and throughput, refreshed as care happens.","84%"),
        ("Financial misappropriation","Revenue leaks between the point of service and the ledger.","revenue leak",
         "Every service posts to billing automatically, with an audit trail on each entry.","91%"),
        ("Time management","Clinician hours consumed by clerical work.","lost hours",
         "Click-and-drag note capture, so consultations end with the record already written.","64%"),
        ("Unmanaged cost centres","Nobody knows which department loses money.","hidden cost",
         "Departmental P&amp;L reporting that shows which unit earns and which drains.","73%"),
        ("Procurement management","Stockouts standing beside expiries.","dead stock",
         "Stock, expiry and reorder tracked against real dispensing volumes.","69%"),
        ("HMO management","Claims delayed, denied, or never filed.","unpaid claims",
         "e-Claim workflow that files clean, complete claims from the encounter itself.","88%"),
        ("Quality of care management","Outcomes unmeasured, therefore unimproved.","flat outcomes",
         "Outcome and quality indicators tracked per clinician, unit and period.","57%")]
ledger="".join(f"""
      <div class="lrow">
        <button class="lhead"><span><span class="lname">{n}</span><span class="lcsq">{c}</span></span>
          <span class="ltag">{t}</span><span class="lplus" aria-hidden="true"></span></button>
        <div class="lbody"><div class="lbody-in">
          <p class="lfix"><b>How Genesys closes it.</b> {fix}</p>
          <span class="lmeter">reduction<span class="track" style="--w:{w}"><i></i></span>{w}</span>
        </div></div>
      </div>""" for n,c,t,fix,w in BLEEDS)

ROUTES=[("Path 01","I run a hospital","50 to 500 beds. You need to see where the money goes and know the business outlives you.","See the hospital path"),
        ("Path 02","I run a small practice","A clinic, lab or pharmacy. Affordable, and runs without an IT department.","See the practice path"),
        ("Path 03","I run a public health system","A ministry or agency. Scale across facilities and data you can govern.","Book a consultation"),
        ("Path 04","I am a payer","An HMO or insurer. Claims that arrive clean and on time.","Book a consultation")]
routes="".join(f'<a class="route reveal d{i}" href="who-we-serve.html"><div><span class="rk">{k}</span>'
               f'<h3>{h}</h3><p>{p}</p></div><span class="go">{g} &rarr;</span></a>'
               for i,(k,h,p,g) in enumerate(ROUTES,1))

QUOTES=[("Our transition was eased by the assistance of the Genesys team. The software is quick and efficient, yet complete.","[Name needed]","Role and facility to be confirmed"),
        ("We can finally see which department earns and which one drains. That conversation used to be guesswork.","[Name needed]","Hospital administrator, facility to be confirmed"),
        ("Claims that used to sit for weeks now leave the same day the patient does.","[Name needed]","Billing lead, facility to be confirmed")]
slides="".join(f'<div class="slide{" active" if i==0 else ""}"><p class="q">&ldquo;{q}&rdquo;</p>'
               f'<div class="attr"><b>{n}</b>{r}</div></div>' for i,(q,n,r) in enumerate(QUOTES))
dots="".join(f'<button class="dot" aria-selected="{"true" if i==0 else "false"}" aria-label="Quote {i+1}"></button>'
             for i in range(len(QUOTES)))

home=f"""
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Health information systems &middot; Lekki, Lagos</span>
    <h1>Run the whole hospital <em>from one record.</em></h1>
    <p class="sub">Genesys builds the hospital management and electronic medical records systems that African health facilities run on, from a single clinic to a multi-site group. Engineered for real power and real bandwidth.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
      <a class="btn btn-ghost" href="#chooser">Find the system that fits my practice</a>
    </div>
    <div class="hero-stage">
      <div class="hero-photo"><img src="assets/img/hero.jpg" alt="Genesys specialists reviewing connected hospital, laboratory, pharmacy and records data across a map of Africa"></div>
      <div class="uicard">
        <div class="uc-top"><span class="uc-title">Facility overview</span>
          <span class="uc-live"><span class="uc-dot"></span>Live</span></div>
        <div class="uc-rows">
          <div class="uc-row"><span class="uc-label">Bed occupancy</span><span class="uc-val"><span data-to="86">0</span>%</span>
            <span class="uc-bar"><i data-w="86%"></i></span></div>
          <div class="uc-row"><span class="uc-label">Claims filed today</span><span class="uc-val" data-to="147">0</span>
            <span class="uc-bar"><i data-w="72%"></i></span></div>
          <div class="uc-row"><span class="uc-label">Revenue captured</span><span class="uc-val">&#8358;<span data-to="4.8" data-dec="1">0</span>m</span>
            <span class="uc-bar"><i data-w="91%"></i></span></div>
        </div>
        <div class="uc-foot">Illustrative interface &middot; not live client data</div>
      </div>
    </div>
    <div class="hero-trust">
      <span class="jv">Backed by Vatebra and Realms</span>
      <span class="chip">Offline-first</span><span class="chip">NDPR-aligned</span>
      <span class="chip">HL7 / FHIR</span><span class="chip">ICD-10 ready</span>
    </div>
  </div>
</section>

{marquee()}

<section class="tight">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><div class="num"><span data-to="8">0</span></div><div class="lab">operational bleeds closed by one system</div></div>
      <div class="stat reveal d1"><div class="num"><span data-to="4">0</span></div><div class="lab">systems sized from clinic to multi-site group</div></div>
      <div class="stat reveal d2"><div class="num"><span data-to="99.5" data-dec="1">0</span><sup>%</sup></div><div class="lab">target uptime, including through power cuts</div></div>
      <div class="stat reveal d3"><div class="num"><span data-to="2017" data-sep="0">0</span></div><div class="lab">building health systems in Lagos since</div></div>
    </div>
    <p class="stat-note">Figures shown are illustrative targets, not audited client results. Verified numbers replace these once published.</p>
  </div>
</section>

<section class="band">
  <div class="wrap split wide-left">
    <div class="reveal">
      <span class="eyebrow">The real diagnosis</span>
      <h2 style="font-size:clamp(26px,3.6vw,42px);margin:10px 0 14px">African healthcare rarely fails for want of skill. It fails for want of <em style="font-style:italic;color:var(--blue)">information.</em></h2>
      <p style="margin-bottom:14px">Records sit in paper, spreadsheets and disconnected systems. Managers cannot see what is happening in their own facility until it has already cost them. It is why so many African health businesses do not survive past the first generation.</p>
      <p class="muted">Open any line to see how Genesys closes it.</p>
    </div>
    <div class="ledger reveal">{ledger}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Paper to platform</span>
      <h2>Drag the divider. That is the whole pitch.</h2>
      <p>The left is how most facilities still hold a patient history. The right is the same history in Genesys.</p></div>
    <div class="ba reveal">
      <div class="ba-pane">
        <div class="ba-side ba-after">
          <span class="ba-tag">Genesys record</span>
          <div class="mock" style="flex:1">
            <div class="mock-bar"><i></i><i></i><i></i><span>genesys / patient / A-40218</span></div>
            <div class="mock-body">
              <div class="mock-row"><span><b>Adaeze Nwosu &middot; 34F</b><em>MRN A-40218 &middot; last seen 12 Jun</em></span><span class="mock-pill ok">Complete</span></div>
              <div class="mock-row"><span><b>Antenatal review</b><em>Dr Bello &middot; BP 118/76 &middot; notes signed</em></span><span class="mock-pill">Encounter</span></div>
              <div class="mock-row"><span><b>Full blood count</b><em>Lab &middot; resulted in 42 min</em></span><span class="mock-pill ok">Resulted</span></div>
              <div class="mock-row"><span><b>Claim 88213</b><em>HMO &middot; filed automatically</em></span><span class="mock-pill ok">Paid</span></div>
            </div>
          </div>
        </div>
        <div class="ba-side ba-before">
          <span class="ba-tag">Paper records</span>
          <div class="paper">
            NWOSU, A. &mdash; folder 4 of ?<br>
            seen&hellip; 12/06 (or 12/08?)<br>
            BP &mdash; illegible<br>
            FBC &mdash; sent, result not filed<br>
            HMO claim &mdash; pending, form missing<br>
            prev. visit folder &mdash; archive room
            <span class="smudge"></span>
          </div>
        </div>
        <div class="ba-handle"><span class="ba-grip">&#8596;</span></div>
        <input class="ba-input" type="range" min="0" max="100" value="50" aria-label="Compare paper records with the Genesys record">
      </div>
      <div class="ba-cap"><span>Drag to compare</span><span>Illustrative interface</span></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Start where you sit</span>
      <h2>Four ways in. One system underneath.</h2>
      <p>The bleeds look different depending on where you stand. Pick your seat.</p></div>
    <div class="grid-4">{routes}</div>
  </div>
</section>

<section class="tight" id="chooser">
  <div class="wrap"><div class="chooser reveal">
    <span class="eyebrow">Solution chooser</span>
    <h3>How big is the practice you run?</h3>
    <p class="q">Tell us the scale and we will point you to the Genesys system built for it.</p>
    <div class="scale" role="group" aria-label="Choose your scale">
      <button data-rec="emr" aria-pressed="false">1 to 20 beds</button>
      <button data-rec="clinical" aria-pressed="false">20 to 100 beds</button>
      <button data-rec="hmis" aria-pressed="false">100 to 500 beds</button>
      <button data-rec="standalone" aria-pressed="false">Not a hospital</button>
    </div>
    <div class="rec empty" id="rec" aria-live="polite">Pick a scale to see your recommended system.</div>
  </div></div>
</section>

<section class="band">
  <div class="wrap split wide-right">
    <div class="reveal">
      <span class="eyebrow">Why Genesys</span>
      <h2 style="font-size:clamp(25px,3.4vw,38px);margin:10px 0 18px">Software that survives the conditions it runs in.</h2>
      <div class="grid-2" style="gap:18px">
        <div class="pillar"><h3>Offline-first</h3><p>Built for intermittent power and low bandwidth. The clinic keeps working through a power cut, then syncs.</p></div>
        <div class="pillar"><h3>Simple by design</h3><p>Records generated by clicking and dragging, so a facility runs without an IT department.</p></div>
        <div class="pillar"><h3>Affordable</h3><p>A staged path from paper to full digital operations, priced to the scale of the practice.</p></div>
        <div class="pillar"><h3>Its own team, deep roots</h3><p>Genesys runs its own operation, drawing on software delivery at Vatebra and healthcare experience at Realms.</p></div>
      </div>
    </div>
    <div class="figure reveal"><img src="assets/img/band_why.jpg" alt="A clinician working with a live health data dashboard"></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">In their words</span><h2>What facilities tell us.</h2></div>
    <div class="carou reveal">{slides}
      <div class="carou-ctl">{dots}<button class="carou-pause">Pause</button></div>
    </div>
    <p class="stat-note">Quotes are held with placeholder attribution until each facility confirms name and role for publication.</p>
  </div>
</section>
{cta()}"""

# ------------------------------------------------------------ SOLUTIONS
TOUR=[("Records","Genesys HMIS","One patient record, every department",
       ["Single record across wards, laboratory and pharmacy","Offline capture that syncs when the line returns","Role-based access with a full audit trail"],
       [("Adaeze Nwosu &middot; 34F","MRN A-40218 &middot; antenatal","Active","ok"),
        ("Chinedu Okafor &middot; 51M","MRN A-40219 &middot; cardiology","Admitted",""),
        ("Fatima Bello &middot; 8F","MRN A-40220 &middot; paediatrics","Discharged","ok")],None),
      ("Billing","Revenue capture","Every service reaches the ledger",
       ["Services post to billing at the point of care","Departmental P&amp;L, not one lump figure","Reconciliation that shows where a naira went"],
       [("Consultation &middot; Dr Bello","Posted 09:14","&#8358;15,000","ok"),
        ("Full blood count","Posted 09:51","&#8358;8,500","ok"),
        ("Ward &middot; 2 nights","Posted 11:02","&#8358;60,000","")],[38,55,47,72,64,88]),
      ("Claims","HMO &amp; NHIA","Claims that arrive clean",
       ["e-Claim built from the encounter itself","Validation before submission, not after denial","Ageing view on every outstanding claim"],
       [("Claim 88213 &middot; HMO","Filed automatically","Paid","ok"),
        ("Claim 88214 &middot; NHIA","Awaiting response &middot; 3 days","Pending",""),
        ("Claim 88215 &middot; HMO","Validation passed","Filed","ok")],None),
      ("Pharmacy","Stock &amp; dispensing","No stockouts beside expiries",
       ["Dispensing writes back to the patient record","Expiry and reorder alerts on real volumes","Batch tracking from delivery to patient"],
       [("Amoxicillin 500mg","Batch AX-2291 &middot; exp 03/27","In stock","ok"),
        ("Artemether inj.","Batch RT-1180 &middot; exp 11/26","Reorder",""),
        ("Paracetamol IV","Batch PC-3320 &middot; exp 08/27","In stock","ok")],[62,48,70,55,80,66])]
def mock(rows,chart):
    r="".join(f'<div class="mock-row"><span><b>{a}</b><em>{b}</em></span>'
              f'<span class="mock-pill {k}">{c}</span></div>' for a,b,c,k in rows)
    ch=""
    if chart:
        bars="".join(f'<i style="--h:{h}%"></i>' for h in chart)
        ch=f'<div class="mock-chart">{bars}</div>'
    return f'<div class="mock"><div class="mock-bar"><i></i><i></i><i></i><span>genesys / console</span></div><div class="mock-body">{r}{ch}</div></div>'
tour_nav="".join(f'<button aria-selected="{"true" if i==0 else "false"}">{t[0]}</button>' for i,t in enumerate(TOUR))
tour_panels="".join(f"""
      <div class="tour-panel{' active' if i==0 else ''}">
        <div class="tour-grid">
          <div class="tour-copy"><span class="eyebrow">{k}</span><h3>{ttl}</h3>
            <div class="tour-list">{"".join(f'<div><span class="tick">&#10003;</span><span>{b}</span></div>' for b in bullets)}</div>
          </div>
          {mock(rows,chart)}
        </div>
      </div>""" for i,(k,ttl,head_,bullets,rows,chart) in
      [(i,(t[0],t[1],t[2],t[3],t[4],t[5])) for i,t in enumerate(TOUR)])

SOLS=[("sol_hmis","Genesys HMIS","Large practices","An ERP-class system automating processes across every functional area and department. Records, finance, pharmacy, laboratory, claims and wards run on one spine.","Whole-facility automation","[deployment time: fact needed]","Clinician and administrator reviewing a hospital-wide dashboard"),
      ("sol_emr","Genesys EMR","Small to mid-scale","Mid-level process automation across clinical functional areas. Best suited to practices already running disparate IT that need a clean clinical record at the centre.","Clinical workflow","[proof point: fact needed]","Doctor sharing a tablet record with a patient"),
      ("sol_clinical","Clinical Specialized Packages","Small to mid-scale","Targeted automation for practices that already run IT in some areas and need specific clinical functions brought up to the same standard.","Targeted modules","[module list: fact needed]","Multidisciplinary clinical team reviewing diagnostic imaging"),
      ("sol_lab","Stand-alone Packages","Non-hospital","For independent players in the healthcare ecosystem, such as diagnostic laboratories, pharmacies and imaging centres.","Labs &middot; pharmacies &middot; imaging","[proof point: fact needed]","Laboratory scientists reviewing results on a diagnostic dashboard")]
sol_cards="".join(f"""
      <article class="card reveal d{i}"><div class="ph"><img src="assets/img/{img}.jpg" alt="{alt}"></div>
        <div class="body"><span class="fit">{fit}</span><h3>{n}</h3><p class="desc">{d}</p>
          <div class="meta"><span>{m}</span><span class="needs">{nd}</span></div>
          <a class="go" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a></div>
      </article>""" for i,(img,n,fit,d,m,nd,alt) in enumerate(SOLS,1))

FAQ=[("How long does deployment take?","Timelines depend on the size of the facility and the state of existing records. We scope it before quoting rather than promising a number we cannot hold. [Exact ranges: fact needed]"),
     ("Does it work when the power or network drops?","Yes. Genesys is offline-first: the facility keeps recording locally and synchronises once connectivity returns."),
     ("Can we move our existing records across?","Migration from paper and legacy systems is part of implementation, not an extra project you handle alone."),
     ("Who owns the data?","You do. Full ownership, with export available on request at any time.")]
faq="".join(f'<div class="acc-item"><button class="acc-btn">{q}<span class="lplus" aria-hidden="true"></span></button>'
            f'<div class="acc-body"><p>{a}</p></div></div>' for q,a in FAQ)

solutions=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">Solutions</span>
    <h1>Sized to the practice, <em>from paper to full digital operations.</em></h1>
    <p>One taxonomy, four fits. Each closes the same operational bleeds at the scale you actually run.</p></div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Product tour</span><h2>Look inside the system.</h2>
      <p>Four areas of the platform. Switch between them.</p></div>
    <div class="tour reveal"><div class="tour-nav" role="tablist">{tour_nav}</div>{tour_panels}</div>
    <p class="stat-note">Interfaces shown are illustrative mockups of Genesys workflows, not screenshots of live client data.</p>
  </div>
</section>

<section class="band">
  <div class="wrap"><div class="sec-head reveal"><h2>The four systems.</h2></div>
    <div class="grid-2">{sol_cards}</div></div>
</section>

<section class="tight">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Also covered</span>
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 12px">Pharmacy, dispensing and stock</h2>
      <p>Stock movement, expiry and dispensing tracked against the same patient record, so procurement stops guessing.</p></div>
    <div class="figure reveal"><img src="assets/img/sol_pharmacy.jpg" alt="A pharmacist scanning medication stock into the system" style="aspect-ratio:2/1"></div>
  </div>
  <div class="wrap split" style="margin-top:clamp(20px,3vw,36px)">
    <div class="figure reveal" style="order:-1"><img src="assets/img/sol_telemed.jpg" alt="A patient on a video consultation with a doctor" style="aspect-ratio:2/1"></div>
    <div class="reveal"><span class="eyebrow">Also covered</span>
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 12px">Telemedicine and remote consultation</h2>
      <p>Remote consultations that write back to the same record, so a visit from a phone is not a visit lost to paper.</p>
      <p class="needs" style="margin-top:8px">[module detail: fact needed]</p></div>
  </div>
</section>

<section class="band tight">
  <div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Questions</span><h2>What buyers ask first.</h2></div>
    <div class="acc reveal">{faq}</div></div>
</section>
{cta("Not sure which system fits? We will tell you straight.")}"""

# ---------------------------------------------------------- WHO WE SERVE
SERVE=[("srv_hospitals","Hospitals","50 to 500 beds","You need to see where the money goes, keep clinicians out of clerical work, and know the business survives its founder.","Genesys HMIS"),
       ("srv_clinics","Clinics and practices","1 to 100 beds","You need something affordable that runs without an IT department, and a clean clinical record at the centre of every consultation.","Genesys EMR or Clinical Packages"),
       ("srv_public","Public health systems","Ministries and agencies","You need to scale across many facilities, govern the data, and report reliably.","Genesys HMIS, multi-facility"),
       ("srv_payers","Payers and HMOs","Insurers and schemes","You need claims that arrive clean and on time, with an audit trail that holds up.","Claims and e-Claim workflow")]
serve_cards="".join(f"""
      <article class="card reveal d{i}"><div class="ph"><img src="assets/img/{img}.jpg" alt="{n}"></div>
        <div class="body"><span class="fit">{s}</span><h3>{n}</h3><p class="desc">{d}</p>
          <div class="meta"><span>Recommended: {r}</span></div>
          <a class="go" href="contact.html">Talk to us <span class="arrow">&rarr;</span></a></div>
      </article>""" for i,(img,n,s,d,r) in enumerate(SERVE,1))

serve=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">Who we serve</span>
    <h1>Four seats at the table, <em>one system underneath.</em></h1>
    <p>The same operational bleeds look different depending on where you sit. Find the version of the problem that sounds like yours.</p></div>
</section>
<section class="tight"><div class="wrap"><div class="grid-2">{serve_cards}</div></div></section>
{marquee()}
<section class="tight">
  <div class="wrap"><div class="sec-head reveal"><h2>Whichever seat you take, the same spine.</h2>
    <p>The four systems differ in scope, not in standard. Every one is offline-first, auditable and yours to export.</p></div>
    <div class="grid-4">
      <div class="stat reveal"><div class="num"><span data-to="1">0</span></div><div class="lab">patient record across every department</div></div>
      <div class="stat reveal d1"><div class="num"><span data-to="24">0</span><sup>/7</sup></div><div class="lab">operation, including through outages</div></div>
      <div class="stat reveal d2"><div class="num"><span data-to="100">0</span><sup>%</sup></div><div class="lab">data ownership retained by you</div></div>
      <div class="stat reveal d3"><div class="num"><span data-to="4">0</span></div><div class="lab">systems to match your scale</div></div>
    </div>
    <p class="stat-note">Illustrative summary of product commitments, not audited performance figures.</p>
  </div>
</section>
{cta("Tell us where you sit. We will show you the fit.")}"""

# --------------------------------------------------------------- PROOF
proof=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">Proof</span><h1>The record is <em>the argument.</em></h1>
    <p>Named clients, certifications and quantified case studies belong here. We publish only what we can stand behind, and mark clearly what is still to be confirmed.</p></div>
</section>
<section class="tight">
  <div class="wrap"><div class="carou reveal">{slides}
    <div class="carou-ctl">{dots}<button class="carou-pause">Pause</button></div></div>
    <p class="stat-note">Quotes are held with placeholder attribution until each facility confirms name and role for publication.</p>
  </div>
</section>
<section class="band tight">
  <div class="wrap split wide-left">
    <div class="reveal"><span class="eyebrow">What we can show</span>
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 14px">Evidence, not adjectives.</h2>
      <div class="mkrow"><span class="dot2"></span><span>Named client logos <span class="needs">[permission needed]</span></span></div>
      <div class="mkrow"><span class="dot2"></span><span>Certifications: NDPR &middot; ISO &middot; HL7 <span class="needs">[numbers needed]</span></span></div>
      <div class="mkrow"><span class="dot2"></span><span>Anonymised case studies, quantified</span></div>
      <div class="mkrow"><span class="dot2"></span><span>Established 2017, Lagos</span></div>
      <div class="mkrow"><span class="dot2"></span><span>Deployed across hospitals, laboratories and pharmacies</span></div>
    </div>
    <div class="figure reveal"><img src="assets/img/band_proof.jpg" alt="Genesys specialists monitoring connected health facility data" style="aspect-ratio:4/3"></div>
  </div>
</section>
<section class="tight">
  <div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Case studies</span>
    <h2>Three slots, ready for real numbers.</h2>
    <p>Each case follows the same shape: the facility, the situation before, what was deployed, and what changed.</p></div>
    <div class="grid-3">
      <a class="ins reveal" href="contact.html"><span class="k">Case study &middot; pending</span><h3>Multi-site hospital group</h3>
        <div class="skeleton" style="width:92%"></div><div class="skeleton" style="width:76%"></div><div class="skeleton" style="width:84%"></div>
        <p style="margin-top:6px">Facility profile, before state, deployment and measured change to be supplied.</p></a>
      <a class="ins reveal d1" href="contact.html"><span class="k">Case study &middot; pending</span><h3>Diagnostic laboratory</h3>
        <div class="skeleton" style="width:88%"></div><div class="skeleton" style="width:70%"></div><div class="skeleton" style="width:80%"></div>
        <p style="margin-top:6px">Facility profile, before state, deployment and measured change to be supplied.</p></a>
      <a class="ins reveal d2" href="contact.html"><span class="k">Case study &middot; pending</span><h3>Private clinic, single site</h3>
        <div class="skeleton" style="width:90%"></div><div class="skeleton" style="width:74%"></div><div class="skeleton" style="width:82%"></div>
        <p style="margin-top:6px">Facility profile, before state, deployment and measured change to be supplied.</p></a>
    </div>
  </div>
</section>
{cta("Want the detail behind a deployment? Ask us.")}"""

# --------------------------------------------------------------- ABOUT
VALUES=[("Integrity","In everything we do, internally and externally."),
        ("Diligence","We work hard and smart at improving healthcare sustainability in Africa."),
        ("Empathy","We build relationships, with our team and our clients, with empathy."),
        ("Accountability","Our word is our bond. We take responsibility and communicate clearly."),
        ("Loyalty","We are about relationships, and we go the extra mile.")]
values="".join(f'<div class="value"><b>{n}</b><span>{d}</span></div>' for n,d in VALUES)
MEMBERS=[("mike","Mike Aigbe","Deputy Managing Director, Vatebra Limited","Leads business direction, product development, marketing and relationship management at Vatebra, and coordinates its work across Abuja, Ghana, Kenya, Sierra Leone and The Gambia. He holds a B.Sc in Computer Science from the University of Benin, an M.Sc in Computer Science from the University of Lagos, an MBA from the University of Nigeria, Nsukka, and an M.Sc in Corporate Governance from Leeds Metropolitan University.",""),
         ("olamide","Olamide Okulaja","Chief Executive Officer, Realms Healthcare","A healthcare strategist with a background in health systems and healthcare financing, he brings the operating side of the business to the board, pairing clinical and management insight with deep software experience.","Fuller biography to follow"),
         ("jennifer","Jennifer Kaja","Managing Director, Realms Healthcare","She helps lead the healthcare consulting arm of the business and its work with health facilities across the Genesys client base.","Fuller biography to follow")]
members="".join(f"""
      <article class="card member reveal d{i}">
        <div class="portrait" style="border:none;border-bottom:1px solid var(--border);border-radius:0">
          <img src="assets/team/{img}.jpg" alt="{n}, board member"></div>
        <div class="body"><span class="mtag">Board member</span><h3>{n}</h3><span class="aff">{r}</span>
          <p class="bio">{b}</p>{f'<span class="todo">{t}</span>' if t else ''}</div>
      </article>""" for i,(img,n,r,b,t) in enumerate(MEMBERS,1))

about=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">About</span><h1>A health-tech company <em>with its own team.</em></h1>
    <p>Genesys Health Information Systems Limited was established in Lagos in 2017 to close the information gap that costs African health facilities money, time and trust.</p></div>
</section>
<section class="tight">
  <div class="wrap split wide-left">
    <div class="reveal"><h2 style="font-size:clamp(24px,3.2vw,34px);margin-bottom:14px">Why we exist</h2>
      <p style="margin-bottom:12px">The Nigerian healthcare industry is short of data of any sort, credible or otherwise, and studies place it among the sectors most resistant to information technology. Having worked in the sector, we identified the pain points early, and they persist today.</p>
      <p style="margin-bottom:12px">The consequence is blunt. Inefficiencies in management are why so many health businesses do not survive past the first generation.</p>
      <p class="muted">The answer is the same one that transformed engineering, banking, finance and audit: put the information in one place, and let the facility see itself clearly.</p></div>
    <div class="figure reveal"><img src="assets/img/band_about.jpg" alt="A hospital management team meeting beside a ward" style="aspect-ratio:4/3"></div>
  </div>
</section>
<section class="band">
  <div class="wrap grid-2" style="gap:clamp(22px,3.5vw,44px)">
    <div class="reveal"><span class="eyebrow">Vision</span>
      <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 10px">To be the leading provider of simple, affordable health technology to public and private health systems in Africa.</h2>
      <span class="eyebrow" style="display:block;margin-top:20px">Mission</span>
      <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 0">To digitise and optimise healthcare service delivery through unparalleled client-centric service and technology solutions.</h2></div>
    <div class="reveal d1"><span class="eyebrow">Values &middot; IDEAL</span>
      <div style="display:grid;gap:14px;margin-top:14px">{values}</div></div>
  </div>
</section>
<section class="tight">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">The team</span><h2>The people building Genesys.</h2>
      <p>Our board brings together enterprise software leadership and healthcare operating experience, and sets the direction the company builds against.</p></div>
    <div class="split wide-right reveal" style="margin-bottom:22px;align-items:start">
      <div class="portrait chair"><span class="role-tag">Chairman</span>
        <img src="assets/team/kunle.jpg" alt="Kunle Akinniran, Chairman of the Genesys board"></div>
      <div><span class="eyebrow">Chairman of the board</span>
        <h2 style="font-size:clamp(27px,3.6vw,40px);margin:10px 0 4px">Kunle Akinniran</h2>
        <p style="color:var(--blue);font-weight:600;font-size:14.5px;margin-bottom:14px">Managing Director and CEO, Vatebra Limited</p>
        <p style="font-size:15.5px">A technology leader with over 20 years of experience, Kunle joined the Vatebra board in 2006. He was previously Group Head of IT at the defunct Fountain Trust Bank, where in 2001 he led the implementation of the Bankmaster and Branchpower banking systems, and he was part of the team that pioneered a scratch-card based online solution that carried Vatebra's work across Ghana, Sierra Leone and The Gambia. He holds a B.Sc in Computer Sciences from the University of Lagos and an MBA in International Business Management, and is a member of the Nigerian Computer Society, the Computer Professionals Registration Council of Nigeria and the Institute of Directors. He is a multiple-time winner of Tech Company CEO of the Year at the Nigeria Technology Awards.</p></div>
    </div>
    <div class="grid-3">{members}</div>
  </div>
</section>
{cta("Talk to the team behind Genesys.")}"""

# ------------------------------------------------------------- INSIGHTS
INS=[("Insight","Closing the revenue leak between service and ledger"),
     ("Insight","What offline-first really means in a Nigerian clinic"),
     ("Insight","Preparing a facility for its first digital records system")]
NEWS=[("Industry news","Population health management market outlook"),
      ("Industry news","Electronic health record market size projections"),
      ("Industry news","Vaccination and public health programmes across Africa")]
ins="".join(f'<a class="ins reveal d{i}" href="#"><span class="k">{k} &middot; pending</span><h3>{t}</h3>'
            f'<div class="skeleton" style="width:90%"></div><div class="skeleton" style="width:72%"></div>'
            f'<p style="margin-top:6px">Article to be written and managed from the admin panel.</p></a>'
            for i,(k,t) in enumerate(INS))
news="".join(f'<a class="ins reveal d{i}" href="#"><span class="k">{k} &middot; source needed</span><h3>{t}</h3>'
             f'<p>A 40-word summary and an outbound link to the original publisher.</p></a>'
             for i,(k,t) in enumerate(NEWS))
insights=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">Insights</span><h1>From the sector <em>we work in.</em></h1>
    <p>Our own writing on health information systems in Africa, kept separate from curated industry news.</p></div>
</section>
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><h2 style="font-size:clamp(23px,3vw,31px)">Written by Genesys</h2></div>
  <div class="grid-3">{ins}</div></div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><h2 style="font-size:clamp(23px,3vw,31px)">Industry news</h2>
    <p>Summaries only, each linking out to the original publisher.</p></div>
  <div class="grid-3">{news}</div></div></section>
{cta()}"""

# -------------------------------------------------------------- CONTACT
CFAQ=[("How quickly will you reply?","Within one business day. If it is urgent, WhatsApp reaches us fastest."),
      ("Can we see the system before committing?","Yes. A demo runs on workflows that match your facility type, not a generic script."),
      ("Do you work outside Lagos?","We work with facilities across Nigeria and beyond. Tell us where you are and we will confirm coverage.")]
cfaq="".join(f'<div class="acc-item"><button class="acc-btn">{q}<span class="lplus" aria-hidden="true"></span></button>'
             f'<div class="acc-body"><p>{a}</p></div></div>' for q,a in CFAQ)
contact=f"""
<section class="phead">
  <div class="wrap"><span class="eyebrow">Contact</span><h1>See Genesys on <em>your own workflow.</em></h1>
    <p>Tell us about the facility you run and we will show you the system built for it. We respond within one business day.</p></div>
</section>
<section class="tight">
  <div class="wrap split wide-left">
    <div class="form reveal">
      <div class="row2">
        <div class="field"><label for="name">Full name</label><input id="name" type="text" autocomplete="name"></div>
        <div class="field"><label for="email">Email address</label><input id="email" type="email" autocomplete="email"></div></div>
      <div class="row2">
        <div class="field"><label for="phone">Phone number</label><input id="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="facility">Facility name</label><input id="facility" type="text"></div></div>
      <div class="row2">
        <div class="field"><label for="ftype">Facility type</label><select id="ftype"><option>Hospital</option><option>Clinic or practice</option><option>Diagnostic laboratory</option><option>Pharmacy</option><option>Public health system</option><option>HMO or payer</option></select></div>
        <div class="field"><label for="beds">Beds or sites</label><select id="beds"><option>1 to 20 beds</option><option>20 to 100 beds</option><option>100 to 500 beds</option><option>Multi-site group</option><option>Not a hospital</option></select></div></div>
      <div class="field"><label for="product">Product of interest</label><select id="product"><option>Not sure yet, advise me</option><option>Genesys HMIS</option><option>Genesys EMR</option><option>Clinical Specialized Packages</option><option>Stand-alone Packages</option></select></div>
      <div class="field"><label for="msg">Message</label><textarea id="msg" placeholder="Tell us what you are trying to fix."></textarea></div>
      <button class="btn btn-primary" type="button" id="formBtn">Request a demo <span class="arrow">&rarr;</span></button>
      <div class="form-ok" id="formOk"><span>&#10003;</span><span>Thank you. This form is not yet connected, so nothing was sent.</span></div>
      <p class="needs" style="margin-top:10px">[Form is visual. Wiring to Supabase and email is a later stage.]</p>
    </div>
    <div class="reveal d1">
      <div class="figure"><img src="assets/img/band_contact.jpg" alt="A Genesys specialist guiding a practice manager at a clinic reception desk" style="aspect-ratio:2/1"></div>
      <div style="margin-top:20px"><span class="eyebrow">Come and see us</span>
        <p class="addr" style="margin-top:10px;font-size:15px">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos</p>
        <p class="addr" style="margin-top:12px;font-size:15px"><b style="color:var(--text)">+234 903 600 1000</b><br>info@genesys-health.com</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
          <a class="btn btn-ghost" href="#">Chat on WhatsApp</a><a class="btn btn-ghost" href="#">Book a consultation</a></div></div>
      <div class="acc" style="margin-top:24px">{cfaq}</div>
    </div>
  </div>
</section>
<section class="band tight">
  <div class="wrap"><div class="sec-head reveal"><h2 style="font-size:clamp(23px,3vw,31px)">What happens after you sign.</h2></div>
    <div class="grid-4">
      <div class="step reveal" style="border-top:2px solid var(--blue)"><span class="n">01</span><div><b>Migration</b><p>Paper and legacy records brought across, not abandoned.</p></div></div>
      <div class="step reveal d1" style="border-top:2px solid var(--blue)"><span class="n">02</span><div><b>Training</b><p>Staff trained on the workflows they will actually use.</p></div></div>
      <div class="step reveal d2" style="border-top:2px solid var(--blue)"><span class="n">03</span><div><b>Support</b><p>A response commitment and a named line. <span class="needs">[SLA: fact needed]</span></p></div></div>
      <div class="step reveal d3" style="border-top:2px solid var(--blue)"><span class="n">04</span><div><b>Your data stays yours</b><p>Full ownership and export, on request, at any time.</p></div></div>
    </div>
  </div>
</section>"""

if __name__=="__main__":
    page("index.html","Genesys Health — hospital and records systems for African health facilities","Genesys builds the hospital management and electronic medical records systems that African health facilities run on.",home)
    page("solutions.html","Solutions — Genesys Health","Genesys HMIS, EMR, Clinical Specialized Packages and Stand-alone Packages.",solutions)
    page("who-we-serve.html","Who we serve — Genesys Health","Hospitals, clinics and practices, public health systems, and payers.",serve)
    page("proof.html","Proof — Genesys Health","Case studies, certifications and client evidence for Genesys Health.",proof)
    page("about.html","About — Genesys Health","Why Genesys exists, our vision, mission, values and team.",about)
    page("insights.html","Insights — Genesys Health","Writing from Genesys on health information systems in Africa.",insights)
    page("contact.html","Contact — Genesys Health","Request a demo of Genesys, or book a consultation. Lekki Phase 1, Lagos.",contact)
    print("built",len(TABS),"pages")
