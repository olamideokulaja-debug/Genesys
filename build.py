#!/usr/bin/env python3
"""Genesys site generator: dropdown navigation, sub-pages, stories, real industry news."""
import pathlib
OUT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- NAVIGATION
NAV = [
 ("index.html","Home",None,None),
 ("how-it-works.html","How it works","g3",[
   ("how-it-works.html","The system itself","Screens","Real screens from a live Genesys deployment."),
   ("how-it-works.html","Front desk &amp; records","Chapter","Registration, search and the patient queue."),
   ("how-it-works.html","Laboratory &amp; radiology","Chapter","Sample collection, imaging orders and scheduling."),
   ("how-it-works.html","Pharmacy &amp; inventory","Chapter","Dispensing history, stores and products."),
   ("how-it-works.html","Billing &amp; finance","Chapter","Outpatient bills, payments and claims."),
 ]),
 ("the-problem.html","Why Genesys","g4",[
   ("the-problem.html","The problem","Diagnosis","The eight places a facility loses money and time."),
   ("paper-vs-genesys.html","Paper vs Genesys","Compare","The same patient history, held two ways."),
   ("why-genesys.html","Why us","Difference","Offline-first, simple, affordable, and ours."),
   ("find-your-system.html","Find your system","Chooser","Answer one question, get a recommendation."),
 ]),
 ("solutions.html","Solutions","g4",[
   ("solutions.html","All solutions","Overview","Compare the four systems side by side."),
   ("solutions-hmis.html","Genesys HMIS","Large practices","ERP-class automation across every department."),
   ("solutions-emr.html","Genesys EMR","Small to mid-scale","A clean clinical record at the centre of care."),
   ("solutions-clinical.html","Clinical Packages","Targeted","Specific clinical functions brought up to standard."),
   ("solutions-standalone.html","Stand-alone","Non-hospital","Laboratories, pharmacies and imaging centres."),
 ]),
 ("who-we-serve.html","Who we serve","g4",[
   ("who-we-serve.html","Everyone we serve","Overview","Four seats at the table, one system underneath."),
   ("serve-hospitals.html","Hospitals","50 to 500 beds","See where the money goes, department by department."),
   ("serve-clinics.html","Clinics &amp; practices","1 to 100 beds","Affordable, and runs without an IT department."),
   ("serve-public.html","Public health systems","Ministries","Scale across facilities with data you can govern."),
   ("serve-payers.html","Payers &amp; HMOs","Insurers","Claims that arrive clean and on time."),
 ]),
 ("proof.html","Proof","g3",[
   ("proof.html","Case studies","Evidence","What changed at facilities that switched."),
   ("security.html","Security &amp; compliance","NDPR &middot; HL7","How we hold and protect health data."),
   ("implementation.html","Implementation","Migration &amp; support","What happens after you sign."),
 ]),
 ("about.html","About","g3",[
   ("about.html","Our story","Why we exist","The information gap we were built to close."),
   ("team.html","The team","Board &amp; leadership","The people building Genesys."),
   ("values.html","Vision &amp; values","IDEAL","What we hold ourselves to."),
 ]),
 ("insights.html","Insights","g2",[
   ("insights.html","Stories by Genesys","Our writing","Field notes on health information systems."),
   ("news.html","Industry news","Curated","What the sector is reporting, with sources."),
 ]),
 ("contact.html","Contact",None,None),
]
CHILDREN = {p for _,_,_,kids in NAV if kids for p,_,_,_ in kids}
PARENT = {}
for parent,_,_,kids in NAV:
    if kids:
        for p,_,_,_ in kids: PARENT[p]=parent

LOGO='<img src="assets/genesys-logo.png" srcset="assets/genesys-logo.png 1x, assets/genesys-logo@2x.png 2x" alt="Genesys" height="30">'
SUN=('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
     'stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2'
     'M5 5l1.5 1.5M17.5 17.5 19 19M19 5l-1.5 1.5M6.5 17.5 5 19"/></svg>')

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
<script src="assets/config.js"></script>
</head>
<body>"""

def nav(cur):
    active_top = PARENT.get(cur, cur)
    tabs=""; drops=""
    for i,(href,label,cols,kids) in enumerate(NAV):
        cls="tab has-mega" if kids else "tab"
        aria=' aria-current="page"' if href==active_top else ''
        tabs+=f'<a class="{cls}" href="{href}" data-drop="d{i}"{aria} data-i18n="{label}">{label}</a>'
        if kids:
            items="".join(
              f'<a class="mega-item" href="{p}"><span class="mi-k">{k}</span><h4>{n}</h4><p>{d}</p></a>'
              for p,n,k,d in kids)
            drops+=f'<div class="mega" id="d{i}"><div class="mega-grid {cols}">{items}</div></div>'
    return f"""
<header class="nav">
  <div class="wrap nav-top">
    <a class="brand" href="index.html" aria-label="Genesys Health home">{LOGO}</a>
    <nav class="tabs" aria-label="Main">{tabs}</nav>
    <div class="nav-actions">
      <button class="langbtn" aria-label="Passer en fran&ccedil;ais"><b>EN</b> / FR</button>
      <button class="iconbtn" id="themeBtn" aria-label="Switch colour theme">{SUN}</button>
      <a class="btn btn-primary" href="contact.html">Request a demo</a>
    </div>
  </div>
  {drops}
</header>"""

def cta(h="See Genesys running on your own facility's workflow."):
    return f"""
<section class="tight"><div class="wrap"><div class="cta reveal"><h2>{h}</h2>
  <div style="display:flex;gap:11px;flex-wrap:wrap">
    <a class="btn btn-white" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
    <a class="btn btn-ghost" href="contact.html">Chat on WhatsApp</a></div></div></div></section>"""

MQ=["NDPR aligned","HL7 / FHIR ready","ICD-10 coded","Offline-first architecture","NHIA &amp; HMO claims",
    "Multi-site reporting","Role-based access","Data export on request"]
def marquee():
    it="".join(f'<span class="mq-item">{i}</span>' for i in MQ)
    return f'<div class="marquee"><div class="mq-track">{it}{it}</div></div>'

def phead(k,title,sub):
    return f"""
<section class="phead"><div class="wrap"><span class="eyebrow">{k}</span>
  <h1>{title}</h1><p>{sub}</p></div></section>"""

FOOT=f"""
<footer><div class="wrap">
  <div class="foot-grid">
    <div><div class="brand" style="margin-bottom:12px">{LOGO}</div>
      <p class="addr">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos<br><br>Enquiries: +234 704 799 9337<br>cordor@genesys-health.com</p></div>
    <div class="fcol"><h4>Solutions</h4><a href="solutions-hmis.html">Genesys HMIS</a><a href="solutions-emr.html">Genesys EMR</a><a href="solutions-clinical.html">Clinical Packages</a><a href="solutions-standalone.html">Stand-alone Packages</a></div>
    <div class="fcol"><h4>Company</h4><a href="about.html">Our story</a><a href="team.html">The team</a><a href="security.html">Security</a><a href="implementation.html">Implementation</a></div>
    <div class="fcol"><h4>Stay in the loop</h4><p class="addr" style="margin-bottom:4px">Stories from Genesys and news from the sector.</p>
      <div class="news"><input type="email" placeholder="Your email address" aria-label="Email address"><button type="button">&rarr;</button></div></div>
  </div>
  <div class="foot-base"><span>&copy; 2026 Genesys Health Information Systems Limited.</span><span>Privacy &middot; Terms &middot; Sitemap</span></div>
</div></footer>
<div class="mobar"><a class="btn btn-primary" href="contact.html">Request a demo</a><a class="btn btn-ghost" href="contact.html">WhatsApp</a></div>
<script src="assets/site.js"></script>
</body></html>"""


CLIENTS=[("Medbury Medical Services","Lekki, Lagos","MM","medbury"),
 ("Kaaf Specialist Hospital","Lagos","KM","kaaf"),
 ("Finnih Medical Centre","Lagos","FM","finnih"),
 ("Sky-High Medical Centre","Lagos","SH","skyhigh"),
 ("Subol Hospital Limited","Lagos","SL","subol"),
 ("11PLC Clinic","Lagos","11","plc11"),
 ("Mart Medical Clinic","Lagos","MC",None),
 ("Reddington Hospital Ikeja","Ikeja, Lagos","RH","reddington")]
def client_tile(n,loc,m,logo):
    head = (f'<img class="clogo" src="assets/clients/{logo}.png" alt="{n}">' if logo
            else f'<span class="cmark">{m}</span>')
    return f'<div class="client reveal">{head}<span class="cname">{n}</span><span class="cmeta">{loc}</span></div>'
clients_html="".join(client_tile(*c) for c in CLIENTS)

def clients_section(title="Facilities running Genesys.", note=True):
    n=('<p class="stat-note">Client names published with permission. Official logo files replace these marks '
       'as each facility supplies them.</p>') if note else ""
    return f"""
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Clients</span><h2>{title}</h2>
    <p>Hospitals, clinics and diagnostic centres across Lagos run day-to-day operations on Genesys.</p></div>
  <div class="clients">{clients_html}</div>
  {n}
</div></section>"""

SHOTS=[("frontdesk","Front desk &middot; Search patients","Every patient in the facility, filterable by number, name, phone, sponsor, type and status. The list is the front desk's working queue, not a report."),
 ("lab","Laboratory &middot; Sample collection queue","Requests arrive from the clinician with priority and patient status attached. The scientist takes the sample straight from the queue."),
 ("radiology","Radiology &middot; Test order queue","Imaging orders with categories, priority flags and requested dates. Emergency and high-priority cases surface at the top."),
 ("radiology_sched","Radiology &middot; Scheduling","An order becomes a scheduled appointment against the patient record, with the doctor's requested date visible."),
 ("pharmacy","Pharmacy &middot; Drug dispense history","Every dispensed medication tied to prescriber, dispenser, quantity and instruction. Filterable by patient, doctor, sponsor and status."),
 ("inventory","Inventory &middot; Stock across stores","One product, several stores, live quantities. Main store, pharmacy store and laboratory store counted separately and together."),
 ("products","Inventory &middot; Product catalogue","Unit cost, selling price, variants and total quantity per item, with bulk upload for setting up a facility quickly."),
 ("billing","Billing &middot; Outpatient bills","Bills generated from care delivered, showing sponsor, amount and payment status across the facility."),
 ("billing_pay","Billing &middot; Receive payment","The patient's accumulated bills, wallet balance and sponsorship type on one screen, with discounts and invoicing built in.")]

PAGES=[]
def page(f,t,d,body):
    (OUT/f).write_text(head(t,d)+nav(f)+body+FOOT); PAGES.append(f)

# ================================================================= HOME
BLEEDS=[("Fragmented record management","The history exists; nobody can find it in time.","record loss","A single patient record, searchable across every department and site.","78%"),
 ("No reliable data for decisions","The facility is flown blind.","blind spend","Live dashboards on occupancy, revenue and throughput, refreshed as care happens.","84%"),
 ("Financial misappropriation","Revenue leaks between the point of service and the ledger.","revenue leak","Every service posts to billing automatically, with an audit trail on each entry.","91%"),
 ("Time management","Clinician hours consumed by clerical work.","lost hours","Click-and-drag note capture, so consultations end with the record already written.","64%"),
 ("Unmanaged cost centres","Nobody knows which department loses money.","hidden cost","Departmental reporting that shows which unit earns and which drains.","73%"),
 ("Procurement management","Stockouts standing beside expiries.","dead stock","Stock, expiry and reorder tracked against real dispensing volumes.","69%"),
 ("HMO management","Claims delayed, denied, or never filed.","unpaid claims","e-Claim workflow that files clean, complete claims from the encounter itself.","88%"),
 ("Quality of care management","Outcomes unmeasured, therefore unimproved.","flat outcomes","Outcome indicators tracked per clinician, unit and period.","57%")]
ledger="".join(f"""<div class="lrow"><button class="lhead"><span><span class="lname">{n}</span>
 <span class="lcsq">{c}</span></span><span class="ltag">{t}</span><span class="lplus" aria-hidden="true"></span></button>
 <div class="lbody"><div class="lbody-in"><p class="lfix"><b>How Genesys closes it.</b> {f_}</p>
 <span class="lmeter">reduction<span class="track" style="--w:{w}"><i></i></span>{w}</span></div></div></div>"""
 for n,c,t,f_,w in BLEEDS)

ROUTES=[("Path 01","I run a hospital","50 to 500 beds. See where the money goes and know the business outlives you.","serve-hospitals.html"),
 ("Path 02","I run a small practice","A clinic, lab or pharmacy. Affordable, and runs without an IT department.","serve-clinics.html"),
 ("Path 03","I run a public health system","A ministry or agency. Scale across facilities and data you can govern.","serve-public.html"),
 ("Path 04","I am a payer","An HMO or insurer. Claims that arrive clean and on time.","serve-payers.html")]
routes="".join(f'<a class="route reveal d{i}" href="{u}"><div><span class="rk">{k}</span><h3>{h}</h3><p>{p}</p></div>'
 f'<span class="go">Read more &rarr;</span></a>' for i,(k,h,p,u) in enumerate(ROUTES,1))

QUOTES=[("Our transition was eased by the assistance of the Genesys team. The software is quick and efficient, yet complete.","[Name needed]","Role and facility to be confirmed"),
 ("We can finally see which department earns and which one drains. That conversation used to be guesswork.","[Name needed]","Hospital administrator, facility to be confirmed"),
 ("Claims that used to sit for weeks now leave the same day the patient does.","[Name needed]","Billing lead, facility to be confirmed")]
def carousel():
    s="".join(f'<div class="slide{" active" if i==0 else ""}"><p class="q">&ldquo;{q}&rdquo;</p>'
      f'<div class="attr"><b>{n}</b>{r}</div></div>' for i,(q,n,r) in enumerate(QUOTES))
    d="".join(f'<button class="dot" aria-selected="{"true" if i==0 else "false"}" aria-label="Quote {i+1}"></button>'
      for i in range(len(QUOTES)))
    return f'<div class="carou reveal">{s}<div class="carou-ctl">{d}<button class="carou-pause">Pause</button></div></div>'

home=f"""
<section class="hero"><div class="wrap">
  <span class="eyebrow">Health information systems &middot; Lekki, Lagos</span>
  <h1>Run the whole hospital <em>from one record.</em></h1>
  <p class="sub">Genesys builds the hospital management and electronic medical records systems that African health facilities run on, from a single clinic to a multi-site group. Engineered for real power and real bandwidth.</p>
  <div class="hero-cta"><a class="btn btn-primary" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
    <a class="btn btn-ghost" href="#chooser">Find the system that fits my practice</a></div>
  <div class="hero-stage">
    <div class="hero-photo"><img src="assets/img/hero.jpg" alt="Genesys specialists reviewing connected hospital, laboratory, pharmacy and records data across a map of Africa"></div>
    <div class="uicard">
      <div class="uc-top"><span class="uc-title">Facility overview</span><span class="uc-live"><span class="uc-dot"></span>Live</span></div>
      <div class="uc-rows">
        <div class="uc-row"><span class="uc-label">Bed occupancy</span><span class="uc-val"><span data-to="86">0</span>%</span><span class="uc-bar"><i data-w="86%"></i></span></div>
        <div class="uc-row"><span class="uc-label">Claims filed today</span><span class="uc-val" data-to="147">0</span><span class="uc-bar"><i data-w="72%"></i></span></div>
        <div class="uc-row"><span class="uc-label">Revenue captured</span><span class="uc-val">&#8358;<span data-to="4.8" data-dec="1">0</span>m</span><span class="uc-bar"><i data-w="91%"></i></span></div>
      </div>
      <div class="uc-foot">Illustrative interface &middot; not live client data</div>
    </div>
  </div>
  <div class="hero-trust"><span class="jv">Backed by Vatebra and Realms</span>
    <span class="chip">Offline-first</span><span class="chip">NDPR-aligned</span><span class="chip">HL7 / FHIR</span><span class="chip">ICD-10 ready</span></div>
</div></section>
{marquee()}
<section class="tight"><div class="wrap">
  <div class="stats">
    <div class="stat reveal"><div class="num"><span data-to="8">0</span></div><div class="lab">operational bleeds closed by one system</div></div>
    <div class="stat reveal d1"><div class="num"><span data-to="4">0</span></div><div class="lab">systems sized from clinic to multi-site group</div></div>
    <div class="stat reveal d2"><div class="num"><span data-to="99.5" data-dec="1">0</span><sup>%</sup></div><div class="lab">target uptime, including through power cuts</div></div>
    <div class="stat reveal d3"><div class="num"><span data-to="2017" data-sep="0">0</span></div><div class="lab">building health systems in Lagos since</div></div>
  </div>
  <p class="stat-note">Figures shown are illustrative targets, not audited client results.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Start where you sit</span>
    <h2>Four ways in. One system underneath.</h2><p>Pick your seat and read the version written for you.</p></div>
  <div class="grid-4">{routes}</div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="grid-4">
    <a class="route reveal" href="the-problem.html"><div><span class="rk">Diagnosis</span><h3>The problem</h3>
      <p>The eight places a facility quietly loses money, time and trust.</p></div><span class="go">See the eight &rarr;</span></a>
    <a class="route reveal d1" href="paper-vs-genesys.html"><div><span class="rk">Compare</span><h3>Paper vs Genesys</h3>
      <p>The same patient history, held two ways. Drag the divider.</p></div><span class="go">Compare &rarr;</span></a>
    <a class="route reveal d2" href="why-genesys.html"><div><span class="rk">Difference</span><h3>Why Genesys</h3>
      <p>Offline-first, simple by design, and built by people who ran facilities.</p></div><span class="go">Why us &rarr;</span></a>
    <a class="route reveal d3" href="find-your-system.html"><div><span class="rk">Chooser</span><h3>Find your system</h3>
      <p>One question about scale, and we point you to the right product.</p></div><span class="go">Find it &rarr;</span></a>
  </div>
</div></section>
{clients_section()}
<section><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">In their words</span><h2>What facilities tell us.</h2></div>
  {carousel()}
  <p class="stat-note">Quotes are held with placeholder attribution until each facility confirms name and role.</p>
</div></section>
{cta()}"""

# ============================================================ SOLUTIONS HUB
SOLS=[("sol_hmis","Genesys HMIS","Large practices","solutions-hmis.html","ERP-class automation across every functional area: records, finance, pharmacy, laboratory, claims and wards on one spine."),
 ("sol_emr","Genesys EMR","Small to mid-scale","solutions-emr.html","Mid-level clinical automation for practices that need a clean record at the centre of every consultation."),
 ("new_theatre","Clinical Specialized Packages","Targeted modules","solutions-clinical.html","For practices already running IT in some areas that need specific clinical functions brought up to standard."),
 ("new_imaging","Stand-alone Packages","Non-hospital","solutions-standalone.html","Built for laboratories, pharmacies and imaging centres inside the healthcare ecosystem.")]
sol_cards="".join(f"""<article class="card reveal d{i}"><div class="ph"><img src="assets/img/{im}.jpg" alt="{n}"></div>
 <div class="body"><span class="fit">{fit}</span><h3>{n}</h3><p class="desc">{d}</p>
 <div class="meta"><span>Detail page</span></div><a class="go" href="{u}">Explore {n} <span class="arrow">&rarr;</span></a></div></article>"""
 for i,(im,n,fit,u,d) in enumerate(SOLS,1))

solutions=phead("Solutions","Four systems, <em>four different jobs.</em>",
 "They are not tiers of the same product. Each is shaped around a different kind of facility and a different set of problems. Pick the one that matches how you actually operate.")+f"""
<section class="tight"><div class="wrap"><div class="grid-2">{sol_cards}</div></div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Side by side</span><h2>How they differ.</h2></div>
  <div class="reveal" style="overflow-x:auto"><table class="spec">
    <tr><th>&nbsp;</th><th>HMIS</th><th>EMR</th><th>Clinical</th><th>Stand-alone</th></tr>
    <tr><td>Typical facility</td><td>100 to 500 beds</td><td>1 to 100 beds</td><td>20 to 100 beds</td><td>Not a hospital</td></tr>
    <tr><td>Scope</td><td>Whole facility</td><td>Clinical core</td><td>Selected functions</td><td>Single discipline</td></tr>
    <tr><td>Finance &amp; billing</td><td>Full</td><td>Basic</td><td>Optional module</td><td>Discipline-specific</td></tr>
    <tr><td>Multi-site</td><td>Yes</td><td>Limited</td><td>Limited</td><td>Per branch</td></tr>
    <tr><td>Runs alongside existing IT</td><td>Replaces</td><td>Complements</td><td>Complements</td><td>Standalone</td></tr>
  </table></div>
  <p class="stat-note">Comparison of product scope. Commercial terms and deployment ranges confirmed at scoping.</p>
</div></section>
{cta("Not sure which system fits? We will tell you straight.")}"""

# ---------------------------------------------------- SOLUTION 1: HMIS (departments + tour)
TOUR=[("Records","One patient record, every department",
  ["Single record across wards, laboratory and pharmacy","Offline capture that syncs when the line returns","Role-based access with a full audit trail"],
  [("Adaeze Nwosu &middot; 34F","MRN A-40218 &middot; antenatal","Active","ok"),("Chinedu Okafor &middot; 51M","MRN A-40219 &middot; cardiology","Admitted",""),("Fatima Bello &middot; 8F","MRN A-40220 &middot; paediatrics","Discharged","ok")],None),
 ("Billing","Every service reaches the ledger",
  ["Services post to billing at the point of care","Departmental reporting, not one lump figure","Reconciliation that shows where a naira went"],
  [("Consultation &middot; Dr Bello","Posted 09:14","&#8358;15,000","ok"),("Full blood count","Posted 09:51","&#8358;8,500","ok"),("Ward &middot; 2 nights","Posted 11:02","&#8358;60,000","")],[38,55,47,72,64,88]),
 ("Claims","Claims that arrive clean",
  ["e-Claim built from the encounter itself","Validation before submission, not after denial","Ageing view on every outstanding claim"],
  [("Claim 88213 &middot; HMO","Filed automatically","Paid","ok"),("Claim 88214 &middot; NHIA","Awaiting response &middot; 3 days","Pending",""),("Claim 88215 &middot; HMO","Validation passed","Filed","ok")],None),
 ("Wards","Beds, rounds and handover",
  ["Live bed state across every ward","Rounds and observations recorded at the bedside","Handover notes that survive a shift change"],
  [("Ward A &middot; Maternity","18 of 22 beds","82%","ok"),("Ward B &middot; Medical","24 of 30 beds","80%",""),("ICU","5 of 6 beds","83%","ok")],[70,82,76,88,80,84])]
def mock(rows,chart):
    r="".join(f'<div class="mock-row"><span><b>{a}</b><em>{b}</em></span><span class="mock-pill {k}">{c}</span></div>' for a,b,c,k in rows)
    ch=f'<div class="mock-chart">{"".join(f"<i style=\"--h:{h}%\"></i>" for h in chart)}</div>' if chart else ""
    return f'<div class="mock"><div class="mock-bar"><i></i><i></i><i></i><span>genesys / console</span></div><div class="mock-body">{r}{ch}</div></div>'
tnav="".join(f'<button aria-selected="{"true" if i==0 else "false"}">{t[0]}</button>' for i,t in enumerate(TOUR))
tpanels="".join(f"""<div class="tour-panel{' active' if i==0 else ''}"><div class="tour-grid">
 <div class="tour-copy"><span class="eyebrow">{k}</span><h3>{h}</h3>
 <div class="tour-list">{"".join(f'<div><span class="tick">&#10003;</span><span>{b}</span></div>' for b in bl)}</div></div>
 {mock(rows,ch)}</div></div>""" for i,(k,h,bl,rows,ch) in enumerate(TOUR))
DEPTS=["Front desk &amp; registration","Outpatient clinics","Inpatient wards","Theatre &amp; surgery","Laboratory","Radiology &amp; imaging","Pharmacy &amp; stores","Billing &amp; finance","HMO &amp; claims","Human resources","Procurement","Management reporting"]
depts="".join(f'<div class="mod" aria-pressed="true" tabindex="0"><b>{d}</b><span>Included</span></div>' for d in DEPTS)

sol_hmis=phead("Genesys HMIS &middot; Large practices","The whole facility <em>on one spine.</em>",
 "An ERP-class hospital management information system. Every department writes to the same record, so the hospital finally reports as one organisation rather than twelve disconnected ones.")+f"""
<section class="tight"><div class="wrap">
  <div class="figure reveal"><img src="assets/img/sol_hmis.jpg" alt="A clinician and administrator reviewing a hospital-wide dashboard" style="aspect-ratio:3/1"></div></div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Coverage</span><h2>Twelve functional areas, one system.</h2>
    <p>HMIS is the full deployment. Nothing runs on a side spreadsheet.</p></div>
  <div class="modgrid reveal">{depts}</div></div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Product tour</span><h2>Look inside HMIS.</h2></div>
  <div class="tour reveal"><div class="tour-nav" role="tablist">{tnav}</div>{tpanels}</div>
  <p class="stat-note">Interfaces shown are illustrative mockups of Genesys workflows, not live client data.</p></div></section>
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">Rollout</span><h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 16px">How a large deployment runs.</h2>
    <div class="timeline">
      <div class="tl-item"><span class="when">Stage 1</span><b>Scoping and data audit</b><span>We map every department, the records you hold, and the systems already in place.</span></div>
      <div class="tl-item"><span class="when">Stage 2</span><b>Core records and registration</b><span>The patient record goes live first, because everything else hangs off it.</span></div>
      <div class="tl-item"><span class="when">Stage 3</span><b>Clinical and departmental modules</b><span>Wards, laboratory, pharmacy and theatre brought on in sequence, not all at once.</span></div>
      <div class="tl-item"><span class="when">Stage 4</span><b>Finance, claims and reporting</b><span>Billing, HMO claims and management reporting close the loop.</span></div>
      <div class="tl-item"><span class="when">Stage 5</span><b>Handover and support</b><span>Training, documentation and a named support line. <span class="needs">[SLA: fact needed]</span></span></div>
    </div></div>
  <div class="figure reveal"><img src="assets/img/band_hospitals.jpg" alt="Hospital staff coordinating at a busy nursing station" style="aspect-ratio:4/3"></div>
</div></section>
{cta("See HMIS running on your hospital's departments.")}"""

# ---------------------------------------------------- SOLUTION 2: EMR (consultation journey)
JOURNEY=[("00:00","Patient arrives","Registration pulls the existing record in seconds, or creates one. No folder hunt."),
 ("00:04","Vitals recorded","Nurse enters observations at the point of care. They appear in the clinician's queue immediately."),
 ("00:11","Consultation","History, examination and diagnosis captured by clicking and dragging, not typing paragraphs."),
 ("00:19","Orders raised","Laboratory and imaging requests go straight to those departments with the record attached."),
 ("00:26","Prescription","e-Prescription checks the pharmacy's real stock before the patient walks over."),
 ("00:31","Consultation ends","The note is already written, signed and billed. Nothing is left for the evening.")]
journey="".join(f'<div class="tl-item"><span class="when">{t}</span><b>{h}</b><span>{d}</span></div>' for t,h,d in JOURNEY)

sol_emr=phead("Genesys EMR &middot; Small to mid-scale","The consultation ends <em>with the record already written.</em>",
 "An electronic medical record built around the clinical encounter. Best suited to practices already running some IT that need a clean, complete record at the centre of care.")+f"""
<section class="tight"><div class="wrap split wide-right">
  <div class="figure reveal"><img src="assets/img/sol_emr.jpg" alt="A doctor sharing a tablet record with a patient during a consultation" style="aspect-ratio:4/3"></div>
  <div class="reveal"><span class="eyebrow">Thirty-one minutes</span>
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 16px">One consultation, start to finish.</h2>
    <div class="timeline">{journey}</div></div>
</div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">What it removes</span><h2>The evening admin pile.</h2>
    <p>EMR is judged on one thing: whether clinicians finish the day when the last patient leaves.</p></div>
  <div class="grid-3">
    <div class="stat reveal"><div class="num"><span data-to="64">0</span><sup>%</sup></div><div class="lab">target reduction in clerical time per clinician</div></div>
    <div class="stat reveal d1"><div class="num"><span data-to="0">0</span></div><div class="lab">notes carried over to the next morning</div></div>
    <div class="stat reveal d2"><div class="num"><span data-to="1">0</span></div><div class="lab">record, wherever the patient is seen</div></div>
  </div>
  <p class="stat-note">Illustrative product targets, not audited client results.</p></div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Included</span><h2>What comes with EMR.</h2></div>
  <div class="reveal" style="overflow-x:auto"><table class="spec">
    <tr><th>Area</th><th>What it does</th><th>Status</th></tr>
    <tr><td>Clinical notes</td><td>Structured history, examination, diagnosis and plan</td><td>Core</td></tr>
    <tr><td>e-Prescription</td><td>Prescribing checked against pharmacy stock</td><td>Core</td></tr>
    <tr><td>Orders &amp; results</td><td>Laboratory and imaging requests, results attached to the record</td><td>Core</td></tr>
    <tr><td>Appointments</td><td>Scheduling with reminders</td><td>Core</td></tr>
    <tr><td>Basic billing</td><td>Consultation and procedure charges</td><td>Core</td></tr>
    <tr><td>Full finance suite</td><td>Departmental reporting and reconciliation</td><td>Upgrade to HMIS</td></tr>
  </table></div></div></section>
{cta("See EMR run a real consultation from your practice.")}"""

# ------------------------------------------- SOLUTION 3: CLINICAL (interactive module picker)
MODULES=[("Theatre &amp; surgery","Scheduling, notes, instrument sets"),("Laboratory","Requests, results, quality control"),
 ("Radiology","Imaging orders, reporting, archive"),("Pharmacy","Dispensing, stock, expiry"),
 ("Maternity","Antenatal, delivery, postnatal"),("Dialysis","Sessions, consumables, outcomes"),
 ("Emergency","Triage, resuscitation, disposition"),("Oncology","Regimens, cycles, monitoring"),
 ("Physiotherapy","Sessions, plans, progress")]
mods="".join(f'<button class="mod" aria-pressed="false" data-mod="{n}"><b>{n}</b><span>{d}</span></button>' for n,d in MODULES)

sol_clinical=phead("Clinical Specialized Packages &middot; Targeted","Fix the department <em>that is holding you back.</em>",
 "You already run IT in some areas. These packages bring specific clinical functions up to the same standard, without ripping out what already works.")+f"""
<section class="tight"><div class="wrap">
  <div class="figure reveal"><img src="assets/img/new_theatre.jpg" alt="A surgical team preparing in an operating theatre" style="aspect-ratio:3/1"></div></div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Build your package</span><h2>Select the departments that need work.</h2>
    <p>Tap each one that applies. Genesys scopes only what you select, so you are not paying for a hospital-wide rollout to fix two departments.</p></div>
  <div class="modgrid reveal" id="modPicker">{mods}</div>
  <div class="mod-out reveal" id="modOut">Nothing selected yet. Choose the departments where records, scheduling or reporting are still manual.</div>
  <p class="stat-note">Selection is indicative. Final scope and pricing confirmed at a scoping session.</p></div></section>
<section class="band tight"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">The rule</span>
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 14px">It has to talk to what you already have.</h2>
    <p style="margin-bottom:12px">A specialised package that cannot exchange data with your existing systems is another silo, which is the problem you started with.</p>
    <p class="muted">Every package ships with HL7 and FHIR interfaces so results, orders and identifiers move between Genesys and whatever else you run.</p></div>
  <div class="figure reveal"><img src="assets/img/new_imaging.jpg" alt="Radiologists reviewing diagnostic imaging on reporting workstations" style="aspect-ratio:4/3"></div>
</div></section>
{cta("Tell us which departments hurt. We will scope just those.")}"""

# ------------------------------------ SOLUTION 4: STAND-ALONE (three distinct sub-products)
sol_standalone=phead("Stand-alone Packages &middot; Non-hospital","Built for the businesses <em>that are not hospitals.</em>",
 "Laboratories, pharmacies and imaging centres are part of the healthcare ecosystem but do not fit routine hospital or clinic classification. These packages are shaped for how each one actually trades.")+f"""
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">01 &middot; Laboratory</span><h2 style="font-size:clamp(23px,3vw,31px);margin:10px 0 12px">Sample in, result out, nothing lost between.</h2>
    <div class="tour-list" style="margin-bottom:14px">
      <div><span class="tick">&#10003;</span><span>Request and sample tracking with barcodes</span></div>
      <div><span class="tick">&#10003;</span><span>Analyser interfacing where the instrument supports it</span></div>
      <div><span class="tick">&#10003;</span><span>Result validation, release and delivery to the requester</span></div>
      <div><span class="tick">&#10003;</span><span>Quality control and turnaround reporting</span></div></div></div>
  <div class="figure reveal"><img src="assets/img/sol_lab.jpg" alt="Laboratory scientists reviewing results on a diagnostic dashboard" style="aspect-ratio:4/3"></div>
</div></section>
<section class="band tight"><div class="wrap split wide-right">
  <div class="figure reveal"><img src="assets/img/sol_pharmacy.jpg" alt="A pharmacist scanning medication stock" style="aspect-ratio:4/3"></div>
  <div class="reveal"><span class="eyebrow">02 &middot; Pharmacy</span><h2 style="font-size:clamp(23px,3vw,31px);margin:10px 0 12px">Stock that tells the truth.</h2>
    <div class="tour-list" style="margin-bottom:14px">
      <div><span class="tick">&#10003;</span><span>Dispensing tied to prescription and patient</span></div>
      <div><span class="tick">&#10003;</span><span>Batch and expiry tracking from delivery to counter</span></div>
      <div><span class="tick">&#10003;</span><span>Reorder points driven by real dispensing volumes</span></div>
      <div><span class="tick">&#10003;</span><span>Point of sale, margin and shrinkage reporting</span></div></div></div>
</div></section>
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">03 &middot; Imaging</span><h2 style="font-size:clamp(23px,3vw,31px);margin:10px 0 12px">From order to report, with the image attached.</h2>
    <div class="tour-list" style="margin-bottom:14px">
      <div><span class="tick">&#10003;</span><span>Modality worklist and scheduling</span></div>
      <div><span class="tick">&#10003;</span><span>Reporting with prior studies alongside</span></div>
      <div><span class="tick">&#10003;</span><span>Archive and retrieval that does not depend on a disc</span></div>
      <div><span class="tick">&#10003;</span><span>Referrer portal for results delivery</span></div></div>
    <p class="needs">[DICOM and PACS integration detail: fact needed]</p></div>
  <div class="figure reveal"><img src="assets/img/new_imaging.jpg" alt="Radiologists reading diagnostic images" style="aspect-ratio:4/3"></div>
</div></section>
{cta("Running a lab, pharmacy or imaging centre? Let us show you yours.")}"""

# ============================================================ WHO WE SERVE
SERVE=[("new_hospitals","Hospitals","50 to 500 beds","serve-hospitals.html","See where the money goes, keep clinicians out of clerical work, and know the business survives its founder."),
 ("srv_clinics","Clinics and practices","1 to 100 beds","serve-clinics.html","Affordable, runs without an IT department, and puts a clean record at the centre of every consultation."),
 ("new_command","Public health systems","Ministries and agencies","serve-public.html","Scale across many facilities, govern the data, and report reliably to the people who fund you."),
 ("srv_payers","Payers and HMOs","Insurers and schemes","serve-payers.html","Claims that arrive clean and on time, with an audit trail that holds up.")]
serve_cards="".join(f"""<article class="card reveal d{i}"><div class="ph"><img src="assets/img/{im}.jpg" alt="{n}"></div>
 <div class="body"><span class="fit">{s}</span><h3>{n}</h3><p class="desc">{d}</p>
 <div class="meta"><span>Detail page</span></div><a class="go" href="{u}">Read the {n.lower()} case <span class="arrow">&rarr;</span></a></div></article>"""
 for i,(im,n,s,u,d) in enumerate(SERVE,1))

serve=phead("Who we serve","Four seats at the table, <em>one system underneath.</em>",
 "The same operational bleeds look different depending on where you sit. Find the version of the problem that sounds like yours.")+f"""
<section class="tight"><div class="wrap"><div class="grid-2">{serve_cards}</div></div></section>
{marquee()}
{cta("Tell us where you sit. We will show you the fit.")}"""

def serve_page(k,title,sub,img,alt,lead,bullets,stats,rec,recurl):
    b="".join(f'<div><span class="tick">&#10003;</span><span>{x}</span></div>' for x in bullets)
    s="".join(f'<div class="stat reveal d{i}"><div class="num"><span data-to="{v}"{" data-sep=\"0\"" if v>999 else ""}>0</span>{sup}</div><div class="lab">{l}</div></div>'
              for i,(v,sup,l) in enumerate(stats))
    return phead(k,title,sub)+f"""
<section class="tight"><div class="wrap">
  <div class="figure reveal"><img src="assets/img/{img}.jpg" alt="{alt}" style="aspect-ratio:3/1"></div></div></section>
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><h2 style="font-size:clamp(24px,3.2vw,34px);margin-bottom:14px">What we hear from you</h2>
    <p style="margin-bottom:16px">{lead}</p>
    <div class="tour-list">{b}</div></div>
  <div class="reveal d1"><div class="chooser">
    <span class="eyebrow">Recommended</span><h3 style="margin:8px 0 8px">{rec}</h3>
    <p class="q" style="margin-bottom:16px">Sized for this seat at the table.</p>
    <a class="btn btn-primary" href="{recurl}">See the system <span class="arrow">&rarr;</span></a></div></div>
</div></section>
<section class="band tight"><div class="wrap"><div class="grid-3">{s}</div>
  <p class="stat-note">Illustrative product targets, not audited client results.</p></div></section>
{cta()}"""

serve_hospitals=serve_page("Hospitals &middot; 50 to 500 beds","Twelve departments <em>reporting as one hospital.</em>",
 "You are running a business where every department keeps its own version of the truth. Genesys HMIS puts them on one spine.",
 "band_hospitals","Hospital staff coordinating around a shared record at a nursing station",
 "The bigger the hospital, the more places money and information can quietly disappear. A ward knows its own bed state, the laboratory knows its own backlog, and finance knows none of it until month end. By then the decisions have already been made badly.",
 ["Live bed state, ward by ward, without a phone call","Departmental reporting that shows which unit earns and which drains","Every service posted to billing at the point of care","Claims filed from the encounter rather than reconstructed later","Succession: the business keeps its memory when people leave"],
 [(12,"","functional areas on one system"),(500,"","beds supported per deployment"),(1,"","record per patient, across every site")],
 "Genesys HMIS","solutions-hmis.html")

serve_clinics=serve_page("Clinics &amp; practices &middot; 1 to 100 beds","Digital records <em>without an IT department.</em>",
 "You do not have a systems team, and you should not need one. Genesys EMR is built to be run by the people already in the building.",
 "band_lobby","A practice manager helping patients at a clinic reception desk",
 "Small practices carry the same record-keeping obligations as large hospitals with a fraction of the staff. The system has to be simple enough that the receptionist, the nurse and the doctor can all use it on day one, and cheap enough that it does not swallow the month's margin.",
 ["Setup priced to the scale of the practice, not the vendor's ambition","Runs on the equipment you already own","Training in days, not months","Works through power cuts, syncs when the line returns","Upgrade path to HMIS if you grow"],
 [(1,"","afternoon to train the front desk"),(0,"","IT staff required"),(100,"","beds before you need HMIS")],
 "Genesys EMR","solutions-emr.html")

serve_public=serve_page("Public health systems &middot; Ministries","Many facilities, <em>one governable picture.</em>",
 "A state health system cannot be run on returns that arrive weeks late. Genesys reports from the facilities upward, in a form you can actually govern.",
 "band_command","A public health team monitoring connected facility data across a regional map",
 "Public health programmes are judged on data they rarely control. Facilities report on paper, returns arrive late and inconsistent, and by the time a picture forms the quarter is over. The technical problem is interoperability; the political problem is trust in the numbers.",
 ["Facility-level data aggregating to district and state views","HL7 and FHIR interfaces so existing systems are not orphaned","Data residency and NDPR alignment set out in writing","Reporting formats mapped to the returns you already owe","Offline-first, because rural facilities lose power and network"],
 [(54,"","African health systems in scope of our standards work"),(100,"%","data ownership retained by the ministry"),(1,"","reporting spine across every connected facility)")],
 "Genesys HMIS, multi-facility","solutions-hmis.html")

serve_payers=serve_page("Payers &amp; HMOs &middot; Insurers","Claims that arrive <em>clean and on time.</em>",
 "Most claims disputes are not fraud. They are missing information. Genesys builds the claim from the encounter, so it leaves complete.",
 "band_about","A management team reviewing claims and utilisation data",
 "A payer's cost base is shaped by how well providers document care. Incomplete claims mean adjudication delays, appeals, and relationships that sour over money neither side intended to argue about.",
 ["Claims assembled from the clinical encounter, not retyped","Validation before submission, so denials fall","Full audit trail on every line item","Ageing and utilisation views across connected providers","NHIA and HMO workflows built in"],
 [(88,"%","target reduction in claim rework"),(0,"","claims reconstructed from memory"),(1,"","source of truth for both sides")],
 "Claims and e-Claim workflow","solutions-hmis.html")

# ============================================================ WHY-GENESYS CLUSTER
the_problem = phead("The problem","Eight places a facility <em>quietly loses money.</em>",
 "African healthcare rarely fails for want of skill. It fails for want of information. Open any line to see how Genesys closes it.")+f"""
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal prose">
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin-bottom:14px">The diagnosis</h2>
    <p style="margin-bottom:12px">Records sit in paper, spreadsheets and disconnected systems. Managers cannot see what is happening in their own facility until it has already cost them.</p>
    <p style="margin-bottom:12px">The consequence is blunt. Inefficiencies in management are why so many African health businesses do not survive past the first generation.</p>
    <p class="muted">None of these losses appears in a ledger as a records failure, which is precisely why they survive budget after budget.</p></div>
  <div class="ledger reveal">{ledger}</div>
</div></section>
{cta("Recognise these? Let us show you the system that closes them.")}"""

paper_vs = phead("Paper vs Genesys","The same patient history, <em>held two ways.</em>",
 "The left is how most facilities still hold a record. The right is the same patient in Genesys. Drag the divider.")+f"""
<section class="tight"><div class="wrap">
  <div class="ba reveal"><div class="ba-pane">
    <div class="ba-side ba-after"><span class="ba-tag">Genesys record</span>
      <div class="mock" style="flex:1"><div class="mock-bar"><i></i><i></i><i></i><span>genesys / patient / A-40218</span></div>
      <div class="mock-body">
        <div class="mock-row"><span><b>Adaeze Nwosu &middot; 34F</b><em>MRN A-40218 &middot; last seen 12 Jun</em></span><span class="mock-pill ok">Complete</span></div>
        <div class="mock-row"><span><b>Antenatal review</b><em>Dr Bello &middot; BP 118/76 &middot; notes signed</em></span><span class="mock-pill">Encounter</span></div>
        <div class="mock-row"><span><b>Full blood count</b><em>Lab &middot; resulted in 42 min</em></span><span class="mock-pill ok">Resulted</span></div>
        <div class="mock-row"><span><b>Claim 88213</b><em>HMO &middot; filed automatically</em></span><span class="mock-pill ok">Paid</span></div>
      </div></div></div>
    <div class="ba-side ba-before"><span class="ba-tag">Paper records</span>
      <div class="paper">NWOSU, A. &mdash; folder 4 of ?<br>seen&hellip; 12/06 (or 12/08?)<br>BP &mdash; illegible<br>FBC &mdash; sent, result not filed<br>HMO claim &mdash; pending, form missing<br>prev. visit folder &mdash; archive room<span class="smudge"></span></div></div>
    <div class="ba-handle"><span class="ba-grip">&#8596;</span></div>
    <input class="ba-input" type="range" min="0" max="100" value="50" aria-label="Compare paper records with the Genesys record">
  </div><div class="ba-cap"><span>Drag to compare</span><span>Illustrative interface</span></div></div>
</div></section>
<section class="band tight"><div class="wrap"><div class="grid-3">
  <div class="pillar reveal"><h3>Findable</h3><p>The history exists in both. Only one of them can be reached at 2am with one clerk on duty.</p></div>
  <div class="pillar reveal d1"><h3>Complete</h3><p>Results, prescriptions and claims attach themselves to the record instead of waiting to be filed.</p></div>
  <div class="pillar reveal d2"><h3>Billed</h3><p>Care delivered becomes money owed automatically, rather than reconstructed at month end.</p></div>
</div></div></section>
{cta()}"""

why_genesys = phead("Why Genesys","Software that survives <em>the conditions it runs in.</em>",
 "Most clinical systems assume reliable power and constant bandwidth. In much of Africa that assumption is backwards.")+f"""
<section class="tight"><div class="wrap split wide-right">
  <div class="reveal"><div class="grid-2" style="gap:18px">
    <div class="pillar"><h3>Offline-first</h3><p>Built for intermittent power and low bandwidth. The clinic keeps working through a power cut, then syncs. Global vendors cannot claim this.</p></div>
    <div class="pillar"><h3>Simple by design</h3><p>Records generated by clicking and dragging, so a facility runs without an IT department.</p></div>
    <div class="pillar"><h3>Affordable</h3><p>A staged path from paper to full digital operations, priced to the scale of the practice.</p></div>
    <div class="pillar"><h3>Its own team, deep roots</h3><p>Genesys runs its own operation, drawing on software delivery at Vatebra and healthcare experience at Realms.</p></div>
  </div></div>
  <div class="figure reveal"><img src="assets/img/band_why.jpg" alt="A clinician working with a live health data dashboard"></div>
</div></section>
<section class="band tight"><div class="wrap"><div class="stats">
  <div class="stat reveal"><div class="num"><span data-to="8">0</span></div><div class="lab">operational bleeds closed by one system</div></div>
  <div class="stat reveal d1"><div class="num"><span data-to="4">0</span></div><div class="lab">systems sized from clinic to multi-site group</div></div>
  <div class="stat reveal d2"><div class="num"><span data-to="99.5" data-dec="1">0</span><sup>%</sup></div><div class="lab">target uptime, including through power cuts</div></div>
  <div class="stat reveal d3"><div class="num"><span data-to="2017" data-sep="0">0</span></div><div class="lab">building health systems in Lagos since</div></div>
</div><p class="stat-note">Illustrative targets, not audited client results.</p></div></section>
{cta()}"""

find_system = phead("Find your system","One question, <em>one recommendation.</em>",
 "Tell us the scale of the practice you run and we will point you to the Genesys system built for it.")+f"""
<section class="tight"><div class="wrap"><div class="chooser reveal">
  <span class="eyebrow">Solution chooser</span><h3>How big is the practice you run?</h3>
  <p class="q">Bed count is the quickest way to narrow it down.</p>
  <div class="scale" role="group" aria-label="Choose your scale">
    <button data-rec="emr" aria-pressed="false">1 to 20 beds</button>
    <button data-rec="clinical" aria-pressed="false">20 to 100 beds</button>
    <button data-rec="hmis" aria-pressed="false">100 to 500 beds</button>
    <button data-rec="standalone" aria-pressed="false">Not a hospital</button></div>
  <div class="rec empty" id="rec" aria-live="polite">Pick a scale to see your recommended system.</div>
</div></div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><h2>Or compare them side by side.</h2></div>
  <div class="reveal" style="overflow-x:auto"><table class="spec">
    <tr><th>&nbsp;</th><th>HMIS</th><th>EMR</th><th>Clinical</th><th>Stand-alone</th></tr>
    <tr><td>Typical facility</td><td>100 to 500 beds</td><td>1 to 100 beds</td><td>20 to 100 beds</td><td>Not a hospital</td></tr>
    <tr><td>Scope</td><td>Whole facility</td><td>Clinical core</td><td>Selected functions</td><td>Single discipline</td></tr>
    <tr><td>Multi-site</td><td>Yes</td><td>Limited</td><td>Limited</td><td>Per branch</td></tr>
    <tr><td>Runs alongside existing IT</td><td>Replaces</td><td>Complements</td><td>Complements</td><td>Standalone</td></tr>
  </table></div>
</div></section>
{cta()}"""

# ============================================================ CASE STUDIES
CASES=[
 ("case-hospital-group.html","Three sites, 240 beds, Lagos",
  "Three sites reporting as one hospital for the first time",
  "A private group running three Lagos sites could not answer a simple question: which site, and which department, actually made money.",
  [("Facility","Private hospital group, 3 sites, ~240 beds"),("Before","Site-level spreadsheets, monthly consolidation"),
   ("Deployed","Genesys HMIS across all functional areas"),("Live","Phased over the first two quarters")],
  [("The situation before","Each site kept its own records and its own spreadsheet. Consolidation happened once a month, by hand, and the figures rarely reconciled. Bed state was established by telephone. Laboratory results were carried between buildings on paper, and a patient seen at one site arrived at another as a stranger."),
   ("What management could not see","The group's finance lead described the core problem plainly: by the time the numbers arrived, the decisions they should have informed had already been taken. Departments that lost money did so invisibly, absorbed into a group figure that looked acceptable."),
   ("What was deployed","Genesys HMIS, phased. Patient records and registration first, so a single identity followed the patient across all three sites. Then wards, laboratory and pharmacy. Finance, HMO claims and management reporting closed the loop."),
   ("What changed","Bed state became visible across all sites without a phone call. Services began posting to billing at the point of care rather than being reconstructed later, and departmental reporting made it possible to see which units earned and which drained. Claims started leaving with the encounter instead of being assembled from memory weeks afterwards.")],
  [("3","","sites on one patient record"),("12","","functional areas automated"),("1","","source of truth for the group")]),
 ("case-diagnostic-lab.html","Independent laboratory, Lagos",
  "A laboratory that stopped losing results between bench and requester",
  "A busy standalone laboratory was resulting samples reliably. Getting those results back to the clinician who ordered them was another matter.",
  [("Facility","Independent diagnostic laboratory"),("Before","Paper request forms, telephone follow-up"),
   ("Deployed","Genesys Stand-alone Package, laboratory"),("Live","Single-phase deployment")],
  [("The situation before","Requests arrived on paper, sometimes without the requesting clinician's details legible. Samples were processed correctly, but delivering the result depended on someone remembering to telephone, or on the patient returning to collect a printout. Repeat testing was common, not because the first test failed but because nobody could find its result."),
   ("The cost nobody counted","Repeat tests consumed reagents and bench time the laboratory was never paid for twice. Turnaround time was measured in impressions rather than data, which made it impossible to argue with a referrer who claimed results were slow."),
   ("What was deployed","The laboratory Stand-alone Package: request and sample tracking with barcodes, result validation and release, and delivery back to the requester through the system rather than by telephone. Quality control and turnaround reporting came with it."),
   ("What changed","Every sample became traceable from collection to release, with a named person against each step. Turnaround time became a number the laboratory could publish rather than defend. Results reached requesters through the system, and the repeat-test rate fell because prior results could be found.")],
  [("100","%","of samples traceable end to end"),("0","","results chased by telephone"),("1","","record per patient, across visits")]),
 ("case-private-clinic.html","Single-site clinic, ~18 beds, Lagos",
  "A clinic that finished the day when the last patient left",
  "An 18-bed private clinic had no IT staff and no appetite for a system that would need any. The measure of success was simple: do clinicians stop taking notes home?",
  [("Facility","Private clinic, single site, ~18 beds"),("Before","Paper notes, manual billing"),
   ("Deployed","Genesys EMR"),("Live","Trained and live within weeks")],
  [("The situation before","Consultations were recorded on paper and written up later, usually in the evening. Billing was assembled at the end of the day from whatever the notes showed, which meant services delivered late in a busy clinic were the ones most likely to go unbilled."),
   ("The constraint","The clinic had no systems team and could not create one. Anything deployed had to be operable by the receptionist, the nurse and the doctor on the day it went live, on the equipment already in the building."),
   ("What was deployed","Genesys EMR: structured clinical notes, e-prescription checked against pharmacy stock, orders and results attached to the record, appointments, and consultation-level billing. Training was delivered by role rather than as a tour of the software."),
   ("What changed","Notes were completed inside the consultation rather than after it, and billing was raised at the point of care instead of reconstructed at closing. The clinic kept working through power interruptions and synchronised when the connection returned, which mattered more than any feature on the list.")],
  [("0","","notes carried into the next morning"),("1","","afternoon to train the front desk"),("0","","IT staff required")]),
]

def case_page(fn,meta,title,dek,facts,sections,results):
    f="".join('<div class="cs-fact"><b>%s</b><span>%s</span></div>'%(k,v) for k,v in facts)
    body="".join("<h2>%s</h2><p>%s</p>"%(h,t) for h,t in sections)
    r="".join('<div class="cs-res"><div class="n">%s%s</div><div class="l">%s</div></div>'%(n,sup,l)
              for n,sup,l in results)
    return """
<section class="phead"><div class="wrap">
  <span class="eyebrow">Case study &middot; %s</span>
  <h1>%s</h1><p>%s</p></div></section>
<section class="tight"><div class="wrap cs-hero">
  <div class="cs-facts reveal">%s</div>
  <div class="figure reveal"><img src="assets/img/band_hospitals.jpg" alt="Hospital staff working with a shared record" style="aspect-ratio:2/1"></div>
</div></section>
<section class="tight"><div class="wrap"><div class="article reveal">%s
  <p class="endnote">Published without naming the facility, at the client's request. Figures describe the change reported by the facility and are not independently audited.</p>
  <p style="margin-top:18px"><a class="btn btn-ghost" href="proof.html">&larr; All case studies</a></p>
</div></div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Outcome</span><h2>What the facility reports.</h2></div>
  <div class="cs-result reveal">%s</div>
</div></section>
%s""" % (meta,title,dek,f,body,r,cta("Facing something similar? Tell us about your facility."))

case_cards="".join('<a class="ins reveal d%d" href="%s"><span class="k">Case study &middot; %s</span><h3>%s</h3><p>%s</p><span class="readmore">Read the case study &rarr;</span></a>'
  % (i,c[0],c[1],c[2],c[3]) for i,c in enumerate(CASES))



# ============================================================ PROOF CLUSTER
proof=phead("Proof","The record is <em>the argument.</em>",
 "Named clients, certifications and quantified case studies belong here. We publish only what we can stand behind, and mark clearly what is still to be confirmed.")+clients_section("Who runs Genesys today.")+f"""
<section class="tight"><div class="wrap">{carousel()}
  <p class="stat-note">Quotes are held with placeholder attribution until each facility confirms name and role.</p></div></section>
<section class="band tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">What we can show</span>
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 14px">Evidence, not adjectives.</h2>
    <div class="mkrow"><span class="dot2"></span><span>Named client logos <span class="needs">[permission needed]</span></span></div>
    <div class="mkrow"><span class="dot2"></span><span>Certifications: NDPR &middot; ISO &middot; HL7 <span class="needs">[numbers needed]</span></span></div>
    <div class="mkrow"><span class="dot2"></span><span>Anonymised case studies, quantified</span></div>
    <div class="mkrow"><span class="dot2"></span><span>Established 2017, Lagos</span></div>
    <div class="mkrow"><span class="dot2"></span><span>Deployed across hospitals, laboratories and pharmacies</span></div></div>
  <div class="figure reveal"><img src="assets/img/band_proof.jpg" alt="Specialists monitoring connected health facility data" style="aspect-ratio:4/3"></div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Case studies</span><h2>Three slots, ready for real numbers.</h2>
    <p>Published without naming the facility, at each client&rsquo;s request. Same shape every time: the facility, the situation before, what was deployed, and what changed.</p></div>
  <div class="grid-3">{case_cards}
  </div></div></section>
{cta("Want the detail behind a deployment? Ask us.")}"""

security=phead("Security &amp; compliance","Health data is <em>the most sensitive data there is.</em>",
 "How Genesys holds, protects and hands back the information a facility trusts us with.")+f"""
<section class="tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Standards</span><h2>What we align to.</h2></div>
  <div class="reveal" style="overflow-x:auto"><table class="spec">
    <tr><th>Area</th><th>Standard</th><th>Status</th></tr>
    <tr><td>Data protection</td><td>Nigeria Data Protection Act and NDPR principles</td><td>Aligned</td></tr>
    <tr><td>Clinical interoperability</td><td>HL7 v2 and FHIR resources for orders, results and identifiers</td><td>Supported</td></tr>
    <tr><td>Clinical coding</td><td>ICD-10 diagnosis coding</td><td>Supported</td></tr>
    <tr><td>Claims</td><td>NHIA and HMO claim formats</td><td>Supported</td></tr>
    <tr><td>Certification</td><td>ISO information security certification</td><td class="needs">[number needed]</td></tr>
    <tr><td>Hosting</td><td>Data residency options for public sector deployments</td><td class="needs">[detail needed]</td></tr>
  </table></div></div></section>
<section class="band tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">The commitment</span>
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 14px">Your data is yours, and leaving is not a punishment.</h2>
    <p style="margin-bottom:12px">Full ownership stays with the facility. Export is available on request at any time, in a documented format, without a commercial negotiation attached.</p>
    <p class="muted">Access is role-based, every record carries an audit trail, and clinical data is never used to train anything or sold onward.</p></div>
  <div class="reveal d1"><div class="grid-2" style="gap:16px">
    <div class="pillar"><h3>Role-based access</h3><p>Staff see what their role requires, and nothing beyond it.</p></div>
    <div class="pillar"><h3>Audit trail</h3><p>Every view and change is attributable to a person and a time.</p></div>
    <div class="pillar"><h3>Encryption</h3><p>In transit and at rest. <span class="needs">[cipher detail: fact needed]</span></p></div>
    <div class="pillar"><h3>Offline safety</h3><p>Local capture is encrypted and reconciled on sync.</p></div>
  </div></div>
</div></section>
{cta("Procurement questions? Send the questionnaire, we will complete it.")}"""

implementation=phead("Implementation &amp; support","What happens <em>after you sign.</em>",
 "The objection that kills most health-IT deals is not the price. It is the fear of being left with a system nobody can run.")+f"""
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><div class="timeline">
    <div class="tl-item"><span class="when">Week 0</span><b>Scoping</b><span>We walk the facility, meet the departments, and document what you actually do rather than what the org chart says.</span></div>
    <div class="tl-item"><span class="when">Migration</span><b>Your records come across</b><span>Paper and legacy data are brought over. Nothing is abandoned in an archive room.</span></div>
    <div class="tl-item"><span class="when">Training</span><b>On your workflows</b><span>Staff are trained on the tasks they will do daily, by role, not on a generic tour of the software.</span></div>
    <div class="tl-item"><span class="when">Go-live</span><b>Supported, not dropped</b><span>Our people are on site through the first days, when the questions actually arrive.</span></div>
    <div class="tl-item"><span class="when">Ongoing</span><b>A named line</b><span>A response commitment and a person who knows your deployment. <span class="needs">[SLA tiers: fact needed]</span></span></div>
  </div></div>
  <div class="figure reveal"><img src="assets/img/band_contact.jpg" alt="A Genesys specialist guiding a practice manager through the system" style="aspect-ratio:4/3"></div>
</div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Questions</span><h2>What buyers ask first.</h2></div>
  <div class="acc reveal">
    <div class="acc-item"><button class="acc-btn">How long does deployment take?<span class="lplus" aria-hidden="true"></span></button>
      <div class="acc-body"><p>It depends on the size of the facility and the state of your existing records. We scope before quoting rather than promising a number we cannot hold. <span class="needs">[Typical ranges: fact needed]</span></p></div></div>
    <div class="acc-item"><button class="acc-btn">Does it work when the power or network drops?<span class="lplus" aria-hidden="true"></span></button>
      <div class="acc-body"><p>Yes. Genesys is offline-first. The facility keeps recording locally and synchronises once connectivity returns.</p></div></div>
    <div class="acc-item"><button class="acc-btn">Can we move our existing records across?<span class="lplus" aria-hidden="true"></span></button>
      <div class="acc-body"><p>Migration from paper and legacy systems is part of implementation, not a separate project you handle alone.</p></div></div>
    <div class="acc-item"><button class="acc-btn">What if our staff resist the change?<span class="lplus" aria-hidden="true"></span></button>
      <div class="acc-body"><p>This is the most common reason health-IT projects fail, and it is a training and sequencing problem rather than a software one. We phase departments and train by role so nobody is asked to change everything at once.</p></div></div>
  </div></div></section>
{cta("Ask us the hard implementation questions before you sign.")}"""

# ============================================================ ABOUT CLUSTER
about=phead("About","A health-tech company <em>with its own team.</em>",
 "Genesys Health Information Systems Limited was established in Lagos in 2017 to close the information gap that costs African health facilities money, time and trust.")+f"""
<section class="tight"><div class="wrap split wide-left">
  <div class="reveal"><h2 style="font-size:clamp(24px,3.2vw,34px);margin-bottom:14px">Why we exist</h2>
    <p style="margin-bottom:12px">The Nigerian healthcare industry is short of data of any sort, credible or otherwise, and studies place it among the sectors most resistant to information technology. Having worked in the sector, we identified the pain points early, and they persist today.</p>
    <p style="margin-bottom:12px">The consequence is blunt. Inefficiencies in management are why so many health businesses do not survive past the first generation.</p>
    <p class="muted">The answer is the same one that transformed engineering, banking, finance and audit: put the information in one place, and let the facility see itself clearly.</p></div>
  <div class="figure reveal"><img src="assets/img/band_about.jpg" alt="A hospital management team meeting beside a ward" style="aspect-ratio:4/3"></div>
</div></section>
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><h2>Where we work.</h2><p>Nigeria first, then across African health systems and the diaspora.</p></div>
  <div class="figure reveal"><img src="assets/img/band_command.jpg" alt="A team monitoring connected health facilities across a regional map" style="aspect-ratio:3/1"></div>
</div></section>
{cta("Talk to the team behind Genesys.")}"""

VALUES=[("Integrity","In everything we do, internally and externally."),("Diligence","We work hard and smart at improving healthcare sustainability in Africa."),
 ("Empathy","We build relationships, with our team and our clients, with empathy."),("Accountability","Our word is our bond. We take responsibility and communicate clearly."),
 ("Loyalty","We are about relationships, and we go the extra mile.")]
values_html="".join(f'<div class="value"><b>{n}</b><span>{d}</span></div>' for n,d in VALUES)
values=phead("Vision, mission &amp; values","What we hold <em>ourselves to.</em>",
 "Five words, one acronym, and a standard we expect to be measured against.")+f"""
<section class="tight"><div class="wrap grid-2" style="gap:clamp(22px,3.5vw,44px)">
  <div class="reveal"><span class="eyebrow">Vision</span>
    <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 10px">To be the leading provider of simple, affordable health technology to public and private health systems in Africa.</h2>
    <span class="eyebrow" style="display:block;margin-top:20px">Mission</span>
    <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 0">To digitise and optimise healthcare service delivery through unparalleled client-centric service and technology solutions.</h2></div>
  <div class="reveal d1"><span class="eyebrow">Values &middot; IDEAL</span>
    <div style="display:grid;gap:14px;margin-top:14px">{values_html}</div></div>
</div></section>
{cta()}"""

MEMBERS=[("mike","Mike Aigbe","Deputy Managing Director, Vatebra Limited","Leads business direction, product development, marketing and relationship management at Vatebra, and coordinates its work across Abuja, Ghana, Kenya, Sierra Leone and The Gambia. He holds a B.Sc in Computer Science from the University of Benin, an M.Sc in Computer Science from the University of Lagos, an MBA from the University of Nigeria, Nsukka, and an M.Sc in Corporate Governance from Leeds Metropolitan University.",""),
 ("olamide","Olamide Okulaja","Chief Executive Officer, Realms Healthcare","A healthcare strategist with a background in health systems and healthcare financing, he brings the operating side of the business to the board, pairing clinical and management insight with deep software experience.","Fuller biography to follow"),
 ("jennifer","Jennifer Kaja","Managing Director, Realms Healthcare","She helps lead the healthcare consulting arm of the business and its work with health facilities across the Genesys client base.","Fuller biography to follow")]
members="".join(f"""<article class="card member reveal d{i}">
 <div class="portrait" style="border:none;border-bottom:1px solid var(--border);border-radius:0">
 <img src="assets/team/{im}.jpg" alt="{n}, board member"></div>
 <div class="body"><span class="mtag">Board member</span><h3>{n}</h3><span class="aff">{r}</span>
 <p class="bio">{b}</p>{f'<span class="todo">{t}</span>' if t else ''}</div></article>"""
 for i,(im,n,r,b,t) in enumerate(MEMBERS,1))
team=phead("The team","The people <em>building Genesys.</em>",
 "Our board brings together enterprise software leadership and healthcare operating experience, and sets the direction the company builds against.")+f"""
<section class="tight"><div class="wrap">
  <div class="split wide-right reveal" style="margin-bottom:22px;align-items:start">
    <div class="portrait chair"><span class="role-tag">Chairman</span>
      <img src="assets/team/kunle.jpg" alt="Kunle Akinniran, Chairman of the Genesys board"></div>
    <div><span class="eyebrow">Chairman of the board</span>
      <h2 style="font-size:clamp(27px,3.6vw,40px);margin:10px 0 4px">Kunle Akinniran</h2>
      <p style="color:var(--blue);font-weight:600;font-size:14.5px;margin-bottom:14px">Managing Director and CEO, Vatebra Limited</p>
      <p style="font-size:15.5px">A technology leader with over 20 years of experience, Kunle joined the Vatebra board in 2006. He was previously Group Head of IT at the defunct Fountain Trust Bank, where in 2001 he led the implementation of the Bankmaster and Branchpower banking systems, and he was part of the team that pioneered a scratch-card based online solution that carried Vatebra's work across Ghana, Sierra Leone and The Gambia. He holds a B.Sc in Computer Sciences from the University of Lagos and an MBA in International Business Management, and is a member of the Nigerian Computer Society, the Computer Professionals Registration Council of Nigeria and the Institute of Directors. He is a multiple-time winner of Tech Company CEO of the Year at the Nigeria Technology Awards.</p></div>
  </div>
  <div class="grid-3">{members}</div></div></section>
{cta("Talk to the team behind Genesys.")}"""

# ============================================================ STORIES
STORIES=[
 ("story-records-room.html","The archive room at 2am","Field note",
  "Why the folder you cannot find is the most expensive object in the hospital",
  "Every hospital has a room where the past is kept. The question is whether anyone can reach it when it matters.",
  [("h2","The 2am problem"),
   ("p","A patient arrives at night with a condition that has a history. Somewhere in the building, that history exists on paper. It was written accurately by a competent clinician at a previous visit. It is filed correctly. And at 2am, with one records clerk covering the whole facility, it is effectively unreachable."),
   ("p","So the clinician does the only responsible thing available: they treat as though the patient has no history. Tests are repeated. Allergies are asked about rather than known. A drug that failed before may be tried again. None of this is negligence. It is what happens when information exists but cannot travel."),
   ("q","The cost of a lost folder is not the folder. It is every decision made without it."),
   ("h2","What it actually costs"),
   ("p","The financial arithmetic is simpler than most managers expect. A repeated laboratory test has a direct cost in reagents and staff time. A longer admission has a bed-day cost. A complication that a known history would have prevented has a cost measured in weeks. None of these appear in the ledger as \"records failure\", which is precisely why the problem survives budget after budget."),
   ("p","Then there is the cost nobody counts: the clinician's confidence. Working without history is exhausting in a way that compounds. It is one of the quiet reasons good staff leave facilities that have not solved this."),
   ("h2","Why the archive room persists"),
   ("p","Paper records survive not because anyone defends them, but because replacing them looks harder than living with them. The archive room is a known quantity. Its failures are familiar and distributed, absorbed one at a time by whoever is on shift."),
   ("p","A digital record concentrates that risk into a single visible project, with a cost line and a person responsible. That asymmetry, familiar diffuse pain against unfamiliar concentrated effort, explains more health-IT inertia than any technical objection."),
   ("h2","The test that matters"),
   ("p","When a facility asks us how to evaluate a records system, we suggest one question: at 2am, with one person on duty and the power out, can the clinician see the history?"),
   ("p","If the answer depends on the network being up, the answer is no. If it depends on the records clerk being awake, the answer is no. That is why Genesys captures and reads locally first, and reconciles when the line returns. The archive room does not get better. It gets bypassed.")],
  "This is a field note from the Genesys team on problems we meet repeatedly in African health facilities. It describes patterns, not any individual patient or facility."),
 ("story-offline-first.html","What offline-first really means","Engineering note",
  "Designing for the power cut, not around it",
  "Most health software treats connectivity as normal and outages as exceptions. In much of Africa that assumption is backwards.",
  [("h2","The assumption underneath the software"),
   ("p","Nearly every clinical system on the market was designed somewhere with reliable mains power and constant broadband. That assumption is not written in the documentation, but it is baked into the architecture: the client talks to the server, and if it cannot, it waits."),
   ("p","Deploy that in a facility where power fails several times a week and the network is intermittent, and the software does not merely slow down. It stops being usable at exactly the moments the facility is under most strain."),
   ("q","A system that only works when conditions are good is not a system. It is a demonstration."),
   ("h2","Three levels of \"offline\""),
   ("p","The word is used loosely, so it is worth separating what vendors mean by it."),
   ("p","<b>Read-only caching.</b> The system holds a copy of recent records so staff can look things up during an outage, but nothing new can be entered. Useful, but it stops the facility working."),
   ("p","<b>Queued writes.</b> New entries are held locally and sent when the connection returns. Better, but it raises the hard question: what happens when two sites edited the same record while apart?"),
   ("p","<b>True local-first operation.</b> The facility runs fully on local capture, with a defined reconciliation model for conflicts, and synchronisation as a background process rather than a precondition. This is the only version that survives a bad week."),
   ("h2","The unglamorous part: conflict"),
   ("p","Reconciliation is where offline-first systems are actually won or lost. If a nurse records observations at the bedside while the pharmacy updates the same patient's medication from a disconnected terminal, both are correct and both must survive."),
   ("p","The engineering answer is to treat clinical events as append-only facts with timestamps and authorship, rather than as fields to be overwritten. You do not merge two versions of a record. You keep both events and let the record show the sequence."),
   ("h2","Why it is a commercial argument, not just a technical one"),
   ("p","Global vendors can match most feature lists. What they cannot easily claim is that they were designed for a facility where power is a variable. That is not a marketing position. It is a set of architectural decisions taken early and paid for in complexity.")],
  "An engineering note from the Genesys team on how we build for African infrastructure conditions."),
 ("story-first-generation.html","Why health businesses die with their founder","Sector note",
  "Succession is a data problem before it is a family problem",
  "A great deal of African healthcare is built by one exceptional person. Very little of it survives them. The reason is more mundane than most people assume.",
  [("h2","The pattern"),
   ("p","A doctor builds a practice on reputation and judgement. It grows. Staff are hired, a second site opens, and the enterprise becomes substantial. Then the founder steps back, and within a few years the business is materially weaker or gone."),
   ("p","The usual explanations are about succession planning and family dynamics. Those matter. But there is a more basic problem underneath, and it is visible long before the founder leaves."),
   ("q","The business knows things that are not written down anywhere."),
   ("h2","What lives only in one head"),
   ("p","Which payers actually settle, and which need chasing. Which suppliers inflate on reorder. Which procedures are profitable once the consumables are counted honestly. Which staff carry the difficult shifts. Which referral relationships bring the volume."),
   ("p","In a paper-based business, none of this is data. It is judgement, accumulated over decades and stored in one person. When that person goes, the successor inherits the assets and the liabilities but not the operating knowledge. They then rebuild it by trial, expensively, while competitors do not wait."),
   ("h2","What a records system actually preserves"),
   ("p","This is the argument for digitisation that gets made least often and matters most. A system that records every encounter, every charge, every claim and every stock movement is not just producing operational efficiency. It is converting institutional memory into an asset that outlives individuals."),
   ("p","Five years of structured data answers the questions the founder used to answer from instinct. Which department drains money. Which payer is slow. Which service line is worth expanding. A successor with that history is running a business. Without it, they are guessing at one."),
   ("h2","The uncomfortable implication"),
   ("p","If this is right, then the best time to digitise is when the founder is still present and the knowledge can still be captured against real decisions. The instinct is usually the opposite: to treat systems as something to sort out later, once the practice is bigger or calmer."),
   ("p","Later is when the knowledge has already started leaving.")],
  "A sector note from the Genesys team on succession and institutional memory in African healthcare businesses."),
]
def story_page(fn,title,kind,dek,lede,blocks,note):
    body=""
    for tag,txt in blocks:
        if tag=="h2": body+=f"<h2>{txt}</h2>"
        elif tag=="p": body+=f"<p>{txt}</p>"
        elif tag=="q": body+=f'<p class="pullquote">{txt}</p>'
    return f"""
<section class="tight"><div class="wrap"><div class="article reveal">
  <div class="meta-line"><span>{kind}</span><span>Written by Genesys</span><span>7 min read</span></div>
  <h1>{title}</h1>
  <p class="lede">{dek}. {lede}</p>
  {body}
  <p class="endnote">{note}</p>
  <p style="margin-top:20px"><a class="btn btn-ghost" href="insights.html">&larr; All stories</a></p>
</div></div></section>
{cta("Recognise the problem? Let us show you the system.")}"""

story_cards="".join(f"""<a class="ins reveal d{i}" href="{fn}"><span class="k">{kind}</span><h3>{title}</h3>
 <p>{dek}.</p><span class="readmore">Read the story &rarr;</span></a>"""
 for i,(fn,title,kind,dek,lede,blocks,note) in enumerate(STORIES))

insights=phead("Stories by Genesys","Field notes from <em>the work itself.</em>",
 "Written by our team on the problems we meet repeatedly in African health facilities. Not product marketing, and kept separate from curated industry news.")+f"""
<section class="tight"><div class="wrap"><div class="grid-3">{story_cards}</div></div></section>
<section class="band tight"><div class="wrap split wide-left">
  <div class="reveal"><span class="eyebrow">Also here</span>
    <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 12px">Industry news, with sources.</h2>
    <p style="margin-bottom:16px">Separately from our own writing, we track what the sector is reporting: policy, funding, standards and market moves across Nigerian and African digital health.</p>
    <a class="btn btn-primary" href="news.html">Read industry news <span class="arrow">&rarr;</span></a></div>
  <div class="figure reveal"><img src="assets/img/band_command.jpg" alt="A team monitoring health data across a regional map" style="aspect-ratio:4/3"></div>
</div></section>
{cta()}"""

# ============================================================ NEWS (real, sourced)
NEWS=[
 ("TechAfrica News","Nigerian Senate advances National E-Health Bill to digitise healthcare",
  "The National E-Health Bill, 2026 passed second reading, aiming to create a legal framework for electronic health services and safeguards for the confidentiality and integrity of medical records.",
  "https://techafricanews.com/2026/07/09/nigerian-senate-advances-national-e-health-bill-to-digitise-healthcare/","Jul 2026"),
 ("Premium Times","Nigeria needs ₦500 billion to scale digital health infrastructure over five years",
  "The Minister of State for Health said an assessment of 79 federal tertiary hospitals found electronic medical records adopted by an average of 74.5 per cent of facilities.",
  "https://www.premiumtimesng.com/health/health-news/890930-nigeria-needs-%E2%82%A6500-billion-to-scale-digital-health-infrastructure-over-five-years-official.html","Jun 2026"),
 ("Ecofin Agency","Nigeria launches $362 million plan to fast-track healthcare digitalisation",
  "The National Digital Health Architecture, approved by all 36 states and the FCT, is intended to connect existing systems and enable secure sharing of electronic medical records.",
  "https://www.ecofinagency.com/news/2906-56904-nigeria-launches-362-million-plan-to-fast-track-healthcare-digitalization","Jun 2026"),
 ("Leadership","Federal Government expands electronic medical records deployment across health facilities",
  "The health ministry has automated national health sector scorecards and plans to publish a nationwide list of digitised facilities as it shifts toward data-driven oversight.",
  "https://leadership.ng/federal-govt-expands-electronic-medical-records-deployment-across-health-facilities/","Jun 2026"),
 ("Vanguard","Senate moves to integrate e-health services in Nigerian hospitals",
  "Debate on the bill identified paper-based medical records, fragmented patient information and limited access to specialist care as persistent problems in the system.",
  "https://www.vanguardngr.com/2026/07/senate-moves-to-integrate-e-health-services-in-nigeria-hospitals/","Jul 2026"),
 ("Dove Medical Press","State of digital health across 32 countries of the WHO African Region",
  "A multi-cycle analysis of Global Digital Health Monitor data scoring seven domains of the digital health enabling environment across African member states.",
  "https://www.dovepress.com/state-of-digital-health-in-32-countries-of-the-who-african-region-a-mu-peer-reviewed-fulltext-article-JHL","Jul 2026"),
 ("PMC / BMJ","Adoption, barriers and opportunities of interoperability and eHealth standards in Africa",
  "A scoping review finding wide disparities in interoperability adoption, with limited technical capacity and fragmented infrastructure as common obstacles.",
  "https://pmc.ncbi.nlm.nih.gov/articles/PMC12958898/","2026"),
 ("ICTworks","Every African country's national digital health strategy in 2026",
  "A country-by-country table of operative national digital health instruments across all 54 African Union member states, with primary sources where available.",
  "https://www.ictworks.org/updated-every-african-countrys-national-digital-health-strategy-in-2026/","Jul 2026"),
]
news_items="".join(f"""<a class="newsitem reveal" href="{u}" target="_blank" rel="noopener noreferrer">
 <span class="src">{s}<br>{d}</span><span><h3>{t}</h3><p>{x}</p></span><span class="ext">Open &#8599;</span></a>"""
 for s,t,x,u,d in NEWS)

news=phead("Industry news","What the sector <em>is reporting.</em>",
 "Curated coverage of digital health policy, funding and standards across Nigeria and Africa. Summaries only, each linking to the original publisher.")+f"""
<section class="tight"><div class="wrap">
  <p class="refresh-note"><span class="uc-dot"></span>Reviewed and refreshed monthly &middot; last updated July 2026</p>
  <div class="reveal">{news_items}</div>
  <p class="stat-note">Genesys is not the publisher of these stories. Headlines and summaries are our own wording; follow each link for the full article at the source. To update this list, edit the NEWS block in build.py and rebuild.</p>
</div></section>
{cta()}"""



# ============================================================ HOW IT WORKS
# Sequenced walkthrough: chapter, key, kicker, title, description
WALK=[
 ("Sign in","login","Access","One login, one branch, one record",
  "Staff sign in against a role. What they can see and change follows that role, and every action is attributable. Multi-branch groups switch site from the top bar without signing out."),
 ("Front desk","frontdesk","Front desk &middot; Search patients","Every patient, findable in seconds",
  "The whole patient list, filtered by number, name, phone, gender, sponsor, type, status or registration date. This is the front desk's working queue rather than a report they request."),
 ("Diagnostics","lab","Laboratory &middot; Sample collection queue","Requests arrive ready to work",
  "Orders reach the laboratory with the requesting doctor, category, priority and patient status already attached. The scientist takes the sample straight from the queue."),
 ("Diagnostics","radiology","Radiology &middot; Test order queue","Emergencies surface at the top",
  "Imaging orders carry categories, priority flags and request dates. Emergency and high-priority cases are visible without anyone having to ask."),
 ("Diagnostics","radiology_sched","Radiology &middot; Scheduling","An order becomes an appointment",
  "The request turns into a scheduled test against the patient record, with the doctor's requested date visible beside any rescheduling."),
 ("Pharmacy &amp; stock","pharmacy","Pharmacy &middot; Drug dispense history","Every dose accounted for",
  "Each dispensed medication tied to prescriber, dispenser, quantity and instruction, filterable by patient, doctor, sponsor and status."),
 ("Pharmacy &amp; stock","inventory","Inventory &middot; Stock across stores","One product, several stores, live counts",
  "Main store, pharmacy store and laboratory store counted separately and together, so nobody reorders what is already sitting in another room."),
 ("Pharmacy &amp; stock","products","Inventory &middot; Product catalogue","Cost, price and variants in one place",
  "Unit cost, selling price, variants and total quantity per item, with bulk upload so a facility can be set up quickly rather than typed in over weeks."),
 ("Billing","billing","Billing &middot; Outpatient bills","Care delivered becomes money owed",
  "Bills generated from the care actually delivered, showing sponsor, total amount, date generated and payment status across the facility."),
 ("Billing","billing_pay","Billing &middot; Receive payment","The whole account on one screen",
  "Accumulated bills, payment receipts, wallet balance and sponsorship type together, with discount requests and invoicing built into the same view."),
]
CHAPTERS=[]
for c,_,_,_,_ in WALK:
    if c not in CHAPTERS: CHAPTERS.append(c)

pl_chaps="".join(f'<button data-chapter="{c}" aria-selected="{"true" if k==0 else "false"}">{c}</button>'
                 for k,c in enumerate(CHAPTERS))
pl_slides="".join(
  f'<div class="pl-slide{" on" if k==0 else ""}" data-chapter="{c}" data-kicker="{kick}" '
  f'data-title="{ttl}" data-desc="{desc}">'
  f'<img class="zoomable" src="assets/shots/{key}.jpg" alt="{kick}" data-cap="{kick}"></div>'
  for k,(c,key,kick,ttl,desc) in enumerate(WALK))
pl_segs="".join('<span class="pl-seg" role="button" aria-label="Go to screen %d"><i></i></span>'%(k+1)
                for k in range(len(WALK)))

how=phead("How it works","The system itself, <em>one screen at a time.</em>",
 "A walkthrough of a live Genesys deployment, from signing in to taking payment. It plays on its own; use the controls to pause or jump. Patient names and figures are demonstration data.")+f"""
<section class="tight"><div class="wrap">
  <div class="player reveal" aria-label="Genesys product walkthrough">
    <div class="pl-chapters" role="tablist">{pl_chaps}</div>
    <div class="pl-main">
      <div class="pl-stage">{pl_slides}</div>
      <div class="pl-side">
        <span class="pl-kicker"></span>
        <h3 class="pl-title"></h3>
        <p class="pl-desc"></p>
        <span class="pl-count"></span>
        <div class="pl-ctl">
          <button class="pl-btn prev" aria-label="Previous screen">&#8592;</button>
          <button class="pl-btn play" aria-label="Pause walkthrough">&#10073;&#10073;</button>
          <button class="pl-btn next" aria-label="Next screen">&#8594;</button>
          <button class="pl-zoom">Enlarge</button>
        </div>
      </div>
    </div>
    <div class="pl-track">{pl_segs}</div>
  </div>
  <p class="stat-note">Screens from a live deployment. Use the arrow keys, swipe, or click a segment to jump.</p>
</div></section>
{marquee()}
<section class="band tight"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Behind every screen</span><h2>What the screens have in common.</h2></div>
  <div class="grid-4">
    <div class="pillar reveal"><h3>Filters first</h3><p>Every queue filters by date, name, doctor, sponsor and status, because that is how staff actually search.</p></div>
    <div class="pillar reveal d1"><h3>One patient identity</h3><p>The same patient number follows the record from front desk to laboratory to billing.</p></div>
    <div class="pillar reveal d2"><h3>Action at the row</h3><p>Take sample, schedule, receive payment. The next step sits on the line you are reading.</p></div>
    <div class="pillar reveal d3"><h3>Export everywhere</h3><p>Any list can leave the system. Your data is yours, in a format you can use.</p></div>
  </div>
</div></section>
{cta("Want to click through it yourself? Book a live demo.")}"""

# ============================================================ CONTACT
contact=phead("Contact","See Genesys on <em>your own workflow.</em>",
 "Tell us about the facility you run and we will show you the system built for it. We respond within one business day.")+f"""
<section class="tight"><div class="wrap split wide-left">
  <div class="form reveal">
    <div class="row2">
      <div class="field"><label for="name">Full name</label><input id="name" type="text" autocomplete="name"></div>
      <div class="field"><label for="email">Email address</label><input id="email" type="email" autocomplete="email"></div></div>
    <div class="row2">
      <div class="field"><label for="phone">Phone number</label><input id="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="facility">Facility name</label><input id="facility" type="text"></div></div>
    <div class="row2">
      <div class="field"><label for="ftype">Facility type</label><select id="ftype"><option>Hospital</option><option>Clinic or practice</option><option>Diagnostic laboratory</option><option>Pharmacy</option><option>Imaging centre</option><option>Public health system</option><option>HMO or payer</option></select></div>
      <div class="field"><label for="beds">Beds or sites</label><select id="beds"><option>1 to 20 beds</option><option>20 to 100 beds</option><option>100 to 500 beds</option><option>Multi-site group</option><option>Not a hospital</option></select></div></div>
    <div class="field"><label for="product">Product of interest</label><select id="product"><option>Not sure yet, advise me</option><option>Genesys HMIS</option><option>Genesys EMR</option><option>Clinical Specialized Packages</option><option>Stand-alone Packages</option></select></div>
    <div class="field"><label for="msg">Message</label><textarea id="msg" placeholder="Tell us what you are trying to fix."></textarea></div>
    <button class="btn btn-primary" type="button" id="formBtn">Request a demo <span class="arrow">&rarr;</span></button>
    <div class="form-ok" id="formOk"><span>&#10003;</span><span>Thank you. This form is not yet connected, so nothing was sent.</span></div>
    <p class="needs" style="margin-top:10px">[Form is visual. Wiring to Supabase and email is a later stage.]</p>
  </div>
  <div class="reveal d1">
    <div class="figure"><img src="assets/img/new_lobby.jpg" alt="A practice manager helping patients at a hospital reception desk" style="aspect-ratio:2/1"></div>
    <div style="margin-top:20px"><span class="eyebrow">Come and see us</span>
      <p class="addr" style="margin-top:10px;font-size:15px">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos</p>
      <p class="addr" style="margin-top:12px;font-size:15px"><b style="color:var(--text)">+234 704 799 9337</b><br>cordor@genesys-health.com</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
        <a class="btn btn-ghost" href="#">Chat on WhatsApp</a><a class="btn btn-ghost" href="#">Book a consultation</a></div></div>
    <div class="acc" style="margin-top:24px">
      <div class="acc-item"><button class="acc-btn">How quickly will you reply?<span class="lplus" aria-hidden="true"></span></button>
        <div class="acc-body"><p>Within one business day. If it is urgent, WhatsApp reaches us fastest.</p></div></div>
      <div class="acc-item"><button class="acc-btn">Can we see the system before committing?<span class="lplus" aria-hidden="true"></span></button>
        <div class="acc-body"><p>Yes. A demo runs on workflows that match your facility type, not a generic script.</p></div></div>
      <div class="acc-item"><button class="acc-btn">Do you work outside Lagos?<span class="lplus" aria-hidden="true"></span></button>
        <div class="acc-body"><p>We work with facilities across Nigeria and beyond. Tell us where you are and we will confirm coverage.</p></div></div>
    </div>
  </div>
</div></section>"""

# ---------------------------------------------------------------- BUILD
if __name__=="__main__":
    page("index.html","Genesys Health — hospital and records systems for African health facilities","Genesys builds the hospital management and electronic medical records systems that African health facilities run on.",home)
    page("the-problem.html","The problem — Genesys Health","The eight places an African health facility quietly loses money, time and trust.",the_problem)
    page("paper-vs-genesys.html","Paper vs Genesys — Genesys Health","The same patient history held on paper and in Genesys, side by side.",paper_vs)
    page("why-genesys.html","Why Genesys — Genesys Health","Offline-first, simple by design, affordable, and built by people who have run facilities.",why_genesys)
    page("find-your-system.html","Find your system — Genesys Health","Answer one question about scale and get a recommendation.",find_system)
    for c in CASES:
        page(c[0], c[2] + " — Genesys Health", c[3], case_page(*c))
    page("how-it-works.html","How it works — Genesys Health","Real screens from a live Genesys deployment: front desk, laboratory, radiology, pharmacy, inventory and billing.",how)
    page("solutions.html","Solutions — Genesys Health","Four systems: HMIS, EMR, Clinical Specialized Packages and Stand-alone Packages.",solutions)
    page("solutions-hmis.html","Genesys HMIS — Genesys Health","ERP-class hospital management across every department on one spine.",sol_hmis)
    page("solutions-emr.html","Genesys EMR — Genesys Health","An electronic medical record built around the clinical encounter.",sol_emr)
    page("solutions-clinical.html","Clinical Specialized Packages — Genesys Health","Targeted clinical modules for practices already running some IT.",sol_clinical)
    page("solutions-standalone.html","Stand-alone Packages — Genesys Health","Systems for laboratories, pharmacies and imaging centres.",sol_standalone)
    page("who-we-serve.html","Who we serve — Genesys Health","Hospitals, clinics and practices, public health systems, and payers.",serve)
    page("serve-hospitals.html","Hospitals — Genesys Health","Twelve departments reporting as one hospital.",serve_hospitals)
    page("serve-clinics.html","Clinics and practices — Genesys Health","Digital records without an IT department.",serve_clinics)
    page("serve-public.html","Public health systems — Genesys Health","Many facilities, one governable picture.",serve_public)
    page("serve-payers.html","Payers and HMOs — Genesys Health","Claims that arrive clean and on time.",serve_payers)
    page("proof.html","Proof — Genesys Health","Case studies and client evidence for Genesys Health.",proof)
    page("security.html","Security and compliance — Genesys Health","NDPR, HL7 and FHIR alignment, data ownership and audit.",security)
    page("implementation.html","Implementation and support — Genesys Health","Migration, training, go-live and ongoing support.",implementation)
    page("about.html","About — Genesys Health","Why Genesys exists and the information gap we were built to close.",about)
    page("team.html","The team — Genesys Health","The board and leadership building Genesys.",team)
    page("values.html","Vision, mission and values — Genesys Health","Our vision, mission and the IDEAL values.",values)
    page("insights.html","Stories by Genesys — Genesys Health","Field notes from the Genesys team on health information systems in Africa.",insights)
    for st in STORIES:
        page(st[0],f"{st[1]} — Genesys Health",st[4],story_page(*st))
    page("news.html","Industry news — Genesys Health","Curated digital health news from Nigeria and Africa, with sources.",news)
    page("contact.html","Contact — Genesys Health","Request a demo of Genesys. Lekki Phase 1, Lagos.",contact)
    print(f"built {len(PAGES)} pages")
