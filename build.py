#!/usr/bin/env python3
"""Build the Genesys static site: 7 tabbed pages, shared nav/footer."""
import pathlib, re

OUT = pathlib.Path(__file__).parent
TABS = [
    ("index.html",       "Home"),
    ("solutions.html",   "Solutions"),
    ("who-we-serve.html","Who we serve"),
    ("proof.html",       "Proof"),
    ("about.html",       "About"),
    ("insights.html",    "Insights"),
    ("contact.html",     "Contact"),
]

LOGO = '<img src="assets/genesys-logo.png" srcset="assets/genesys-logo.png 1x, assets/genesys-logo@2x.png 2x" alt="Genesys" height="30">'

def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>"""

def nav(current):
    tabs = "".join(
        f'<a class="tab" href="{h}"{" aria-current=\"page\"" if h==current else ""}>{l}</a>'
        for h, l in TABS)
    return f"""
<header class="nav">
  <div class="wrap nav-top">
    <a class="brand" href="index.html" aria-label="Genesys Health home">{LOGO}</a>
    <div class="nav-actions">
      <span class="lang" title="French coming soon"><b>EN</b> / FR</span>
      <a class="btn btn-primary" href="contact.html">Request a demo</a>
    </div>
  </div>
  <div class="wrap"><nav class="tabs" aria-label="Main">{tabs}</nav></div>
</header>"""

def cta(heading="See Genesys running on your own facility's workflow."):
    return f"""
<section class="tight">
  <div class="wrap">
    <div class="cta reveal">
      <h2>{heading}</h2>
      <div style="display:flex;gap:11px;flex-wrap:wrap">
        <a class="btn btn-white" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
        <a class="btn btn-ghost" href="contact.html">Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""

FOOT = f"""
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="brand" style="margin-bottom:12px">{LOGO}</div>
        <p class="addr">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos<br><br>+234 903 600 1000<br>info@genesys-health.com</p>
      </div>
      <div class="fcol"><h4>Solutions</h4>
        <a href="solutions.html">Genesys HMIS</a><a href="solutions.html">Genesys EMR</a>
        <a href="solutions.html">Clinical Packages</a><a href="solutions.html">Stand-alone Packages</a></div>
      <div class="fcol"><h4>Company</h4>
        <a href="about.html">About</a><a href="about.html">The team</a>
        <a href="proof.html">Proof</a><a href="insights.html">Insights</a></div>
      <div class="fcol"><h4>Stay in the loop</h4>
        <p class="addr" style="margin-bottom:4px">News on Genesys and African health tech.</p>
        <div class="news"><input type="email" placeholder="Your email address" aria-label="Email address"><button type="button">&rarr;</button></div></div>
    </div>
    <div class="foot-base">
      <span>&copy; 2026 Genesys Health Information Systems Limited.</span>
      <span>Privacy &middot; Terms &middot; Sitemap</span>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>"""

def page(fname, title, desc, body, extra=""):
    html = head(title, desc) + nav(fname) + body + extra + FOOT
    (OUT / fname).write_text(html)
    return fname

# ---------------------------------------------------------------- HOME
BLEEDS = [
    ("Fragmented record management","The history exists; nobody can find it in time.","record loss"),
    ("No reliable data for decisions","The facility is flown blind.","blind spend"),
    ("Financial misappropriation","Revenue leaks between the point of service and the ledger.","revenue leak"),
    ("Time management","Clinician hours consumed by clerical work.","lost hours"),
    ("Unmanaged cost centres","Nobody knows which department loses money.","hidden cost"),
    ("Procurement management","Stockouts standing beside expiries.","dead stock"),
    ("HMO management","Claims delayed, denied, or never filed.","unpaid claims"),
    ("Quality of care management","Outcomes unmeasured, therefore unimproved.","flat outcomes"),
]
ledger_rows = "".join(
    f'<div class="row"><div><span class="name">{n}</span><span class="csq">{c}</span></div>'
    f'<span class="tag">{t}</span></div>' for n, c, t in BLEEDS)

ROUTES = [
    ("Path 01","I run a hospital","50 to 500 beds. You need to see where the money goes and know the business outlives you.","See the hospital path"),
    ("Path 02","I run a small practice","A clinic, lab or pharmacy. You need something affordable you can run without an IT department.","See the practice path"),
    ("Path 03","I run a public health system","A ministry or agency. You need scale across facilities and data you can govern.","Book a consultation"),
    ("Path 04","I am a payer","An HMO or insurer. You need claims that arrive clean and on time.","Book a consultation"),
]
route_cards = "".join(
    f'<a class="route reveal" href="who-we-serve.html"><div><span class="rk">{k}</span><h3>{h}</h3>'
    f'<p>{p}</p></div><span class="go">{g} &rarr;</span></a>' for k, h, p, g in ROUTES)

home = f"""
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Health information systems &middot; Lekki, Lagos</span>
    <h1>Run the whole hospital <em>from one record.</em></h1>
    <p class="sub">Genesys builds the hospital management and electronic medical records systems that African health facilities run on, from a single clinic to a multi-site group. Engineered for real power and real bandwidth.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="contact.html">Request a demo <span class="arrow">&rarr;</span></a>
      <a class="btn btn-ghost" href="#chooser">Find the system that fits my practice</a>
    </div>
    <div class="figure hero-band">
      <img src="assets/img/hero.jpg" alt="Genesys specialists reviewing connected hospital, laboratory, pharmacy and records data across a map of Africa" width="1600" height="533">
    </div>
    <div class="trust">
      <span class="jv">Backed by Vatebra and Realms</span>
      <span class="chip">Offline-first</span><span class="chip">NDPR-aligned</span>
      <span class="chip">HL7 / FHIR</span><span class="chip">ICD-10 ready</span>
    </div>
  </div>
</section>

<section style="background:var(--surface);border-block:1px solid var(--border)">
  <div class="wrap split wide-left">
    <div class="reveal">
      <span class="eyebrow">The real diagnosis</span>
      <h2 style="font-size:clamp(26px,3.6vw,42px);margin:10px 0 14px">African healthcare rarely fails for want of skill. It fails for want of <em style="color:var(--blue);font-style:italic">information.</em></h2>
      <p style="margin-bottom:14px">Records sit in paper, spreadsheets and disconnected systems. Managers cannot see what is happening in their own facility until it has already cost them. It is why so many African health businesses do not survive past the first generation.</p>
      <p class="muted">Every line here is a place a facility loses money, time or trust. Genesys is built to close them.</p>
    </div>
    <div class="ledger reveal">{ledger_rows}
      <p class="ledger-foot">8 bleeds. One system built to close each one.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Start where you sit</span>
      <h2>Four ways in. One system underneath.</h2>
      <p>The bleeds look different depending on where you stand. Pick your seat and we will show you the path that fits.</p>
    </div>
    <div class="grid-4">{route_cards}</div>
  </div>
</section>

<section class="tight" id="chooser">
  <div class="wrap">
    <div class="chooser reveal">
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
    </div>
  </div>
</section>

<section class="tight" style="background:var(--surface);border-block:1px solid var(--border)">
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
    <div class="figure reveal">
      <img src="assets/img/analytics.jpg" alt="A clinician working with a live health data dashboard" width="1600" height="533">
    </div>
  </div>
</section>
{cta()}"""

# ------------------------------------------------------------ SOLUTIONS
SOLS = [
    ("hmis","Genesys HMIS","Large practices",
     "An ERP-class system automating processes across every functional area and department. Records, finance, pharmacy, laboratory, claims and wards run on one spine, so the whole facility reports from a single source.",
     "Whole-facility automation","[deployment time: fact needed]",
     "A clinician and administrator reviewing a hospital-wide dashboard linked to pharmacy, laboratory and inpatient wards"),
    ("emr","Genesys EMR","Small to mid-scale",
     "Mid-level process automation across clinical functional areas. Best suited to practices already running disparate IT that need a clean clinical record at the centre of the consultation.",
     "Clinical workflow","[proof point: fact needed]",
     "A doctor sharing a tablet record with a mother and child during a consultation"),
    ("clinical","Clinical Specialized Packages","Small to mid-scale",
     "Targeted automation for practices that already run IT in some areas and need specific clinical functions brought up to the same standard, without replacing everything at once.",
     "Targeted modules","[module list: fact needed]",
     "A multidisciplinary clinical team reviewing diagnostic imaging together"),
    ("lab","Stand-alone Packages","Non-hospital",
     "For independent players in the healthcare ecosystem, such as diagnostic laboratories, pharmacies and imaging centres, that do not fit routine hospital or clinic classification.",
     "Labs &middot; pharmacies &middot; imaging","[proof point: fact needed]",
     "Two laboratory scientists reviewing results on a diagnostic dashboard"),
]
sol_cards = "".join(f"""
      <article class="card reveal">
        <div class="ph"><img src="assets/img/{img}.jpg" alt="{alt}" width="1600" height="533"></div>
        <div class="body"><span class="fit">{fit}</span><h3>{name}</h3>
          <p class="desc">{desc}</p>
          <div class="meta"><span>{meta}</span><span class="needs">{need}</span></div>
          <a class="go" href="contact.html">Request a demo &rarr;</a></div>
      </article>""" for img, name, fit, desc, meta, need, alt in SOLS)

solutions = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">Solutions</span>
    <h1>Sized to the practice, <em>from paper to full digital operations.</em></h1>
    <p>One taxonomy, four fits. Each closes the same operational bleeds at the scale you actually run.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap"><div class="grid-2">{sol_cards}</div></div>
</section>

<section class="tight" style="background:var(--surface);border-block:1px solid var(--border)">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Also covered</span>
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 12px">Pharmacy, dispensing and stock</h2>
      <p>Stock movement, expiry and dispensing tracked against the same patient record, so procurement stops guessing and stockouts stop standing beside expiries.</p>
    </div>
    <div class="figure reveal"><img src="assets/img/pharmacy.jpg" alt="A pharmacist scanning medication stock into the system" width="1600" height="533"></div>
  </div>
  <div class="wrap split figure-xl">
    <div class="figure reveal" style="order:-1"><img src="assets/img/telemed.jpg" alt="A mother and child on a video consultation with a doctor" width="1600" height="533"></div>
    <div class="reveal">
      <span class="eyebrow">Also covered</span>
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin:10px 0 12px">Telemedicine and remote consultation</h2>
      <p>Remote consultations that write back to the same record, so a visit from a phone is not a visit lost to paper.</p>
      <p class="needs" style="margin-top:8px">[module detail: fact needed]</p>
    </div>
  </div>
</section>
{cta("Not sure which system fits? We will tell you straight.")}"""

# ---------------------------------------------------------- WHO WE SERVE
SERVE = [
    ("hmis","Hospitals","50 to 500 beds",
     "You need to see where the money goes, keep clinicians out of clerical work, and know the business survives its founder. Genesys HMIS puts every department on one spine.",
     "Genesys HMIS"),
    ("emr","Clinics and practices","1 to 100 beds",
     "You need something affordable that runs without an IT department, and a clean clinical record at the centre of every consultation.",
     "Genesys EMR or Clinical Packages"),
    ("board","Public health systems","Ministries and agencies",
     "You need to scale across many facilities, govern the data, and report reliably. Interoperability and data residency are covered on our terms and yours.",
     "Genesys HMIS, multi-facility"),
    ("lab","Payers and HMOs","Insurers and schemes",
     "You need claims that arrive clean and on time, with an audit trail that holds up. Claims workflow is built into the record, not bolted on.",
     "Claims and e-Claim workflow"),
]
serve_cards = "".join(f"""
      <article class="card reveal">
        <div class="ph"><img src="assets/img/{img}.jpg" alt="{name}" width="1600" height="533"></div>
        <div class="body"><span class="fit">{scale}</span><h3>{name}</h3>
          <p class="desc">{desc}</p>
          <div class="meta"><span>Recommended: {rec}</span></div>
          <a class="go" href="contact.html">Talk to us &rarr;</a></div>
      </article>""" for img, name, scale, desc, rec in SERVE)

serve = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">Who we serve</span>
    <h1>Four seats at the table, <em>one system underneath.</em></h1>
    <p>The same operational bleeds look different depending on where you sit. Find the version of the problem that sounds like yours.</p>
  </div>
</section>
<section class="tight">
  <div class="wrap"><div class="grid-2">{serve_cards}</div></div>
</section>
{cta("Tell us where you sit. We will show you the fit.")}"""

# --------------------------------------------------------------- PROOF
proof = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">Proof</span>
    <h1>The record is <em>the argument.</em></h1>
    <p>Named clients, certifications and quantified case studies belong here. We publish only what we can stand behind, and mark clearly what is still to be confirmed.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap split wide-left">
    <div class="quote reveal">
      <p class="q">&ldquo;Our transition was eased by the assistance of the Genesys team. The software is quick and efficient, yet complete.&rdquo;</p>
      <div class="attr"><b>[Attribution needed: name, role, facility]</b>A testimonial ships only with a full name, role and facility. This placeholder holds the slot until that is confirmed.</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">What we can show</span>
      <div style="margin-top:14px">
        <div class="mkrow"><span class="dot"></span><span>Named client logos <span class="needs">[permission needed]</span></span></div>
        <div class="mkrow"><span class="dot"></span><span>Certifications: NDPR &middot; ISO &middot; HL7 <span class="needs">[numbers needed]</span></span></div>
        <div class="mkrow"><span class="dot"></span><span>Anonymised case studies, quantified</span></div>
        <div class="mkrow"><span class="dot"></span><span>Established 2017, Lagos</span></div>
        <div class="mkrow"><span class="dot"></span><span>Deployed across hospitals, labs and pharmacies</span></div>
      </div>
    </div>
  </div>
  <div class="wrap figure-xl">
    <div class="figure reveal">
      <img src="assets/img/datacentre.jpg" alt="Genesys specialists monitoring connected health facility data across Africa" width="1600" height="533">
      <figcaption>Systems running across facilities, monitored centrally.</figcaption>
    </div>
  </div>
</section>

<section class="tight" style="background:var(--surface);border-block:1px solid var(--border)">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Case studies</span>
      <h2>Three slots, ready for real numbers.</h2>
      <p>Each case follows the same shape: the facility, the situation before, what was deployed, and what changed, quantified.</p>
    </div>
    <div class="grid-3">
      <a class="ins reveal" href="contact.html"><span class="k">Case study &middot; fact needed</span><h3>Multi-site hospital group</h3><p>[Facility profile, before state, deployment and measured change to be supplied.]</p></a>
      <a class="ins reveal" href="contact.html"><span class="k">Case study &middot; fact needed</span><h3>Diagnostic laboratory</h3><p>[Facility profile, before state, deployment and measured change to be supplied.]</p></a>
      <a class="ins reveal" href="contact.html"><span class="k">Case study &middot; fact needed</span><h3>Private clinic, single site</h3><p>[Facility profile, before state, deployment and measured change to be supplied.]</p></a>
    </div>
  </div>
</section>
{cta("Want the detail behind a deployment? Ask us.")}"""

# --------------------------------------------------------------- ABOUT
VALUES = [
    ("Integrity","In everything we do, internally and externally."),
    ("Diligence","We work hard and smart at improving healthcare sustainability in Africa."),
    ("Empathy","We build relationships, with our team and our clients, with empathy."),
    ("Accountability","Our word is our bond. We take responsibility and communicate clearly."),
    ("Loyalty","We are about relationships, and we go the extra mile."),
]
values_html = "".join(f'<div class="value"><b>{n}</b><span>{d}</span></div>' for n, d in VALUES)

MEMBERS = [
    ("mike","Mike Aigbe","Deputy Managing Director, Vatebra Limited",
     "Leads business direction, product development, marketing and relationship management at Vatebra, and coordinates its work across Abuja, Ghana, Kenya, Sierra Leone and The Gambia. He holds a B.Sc in Computer Science from the University of Benin, an M.Sc in Computer Science from the University of Lagos, an MBA from the University of Nigeria, Nsukka, and an M.Sc in Corporate Governance from Leeds Metropolitan University in the United Kingdom.", ""),
    ("olamide","Olamide Okulaja","Chief Executive Officer, Realms Healthcare",
     "A healthcare strategist with a background in health systems and healthcare financing, he brings the operating side of the business to the board, pairing clinical and management insight with deep software experience.",
     "Fuller biography to follow"),
    ("jennifer","Jennifer Kaja","Managing Director, Realms Healthcare",
     "She helps lead the healthcare consulting arm of the business and its work with health facilities across the Genesys client base.",
     "Fuller biography to follow"),
]
member_cards = "".join(f"""
      <article class="card member reveal">
        <div class="portrait" style="border:none;border-bottom:1px solid var(--border);border-radius:0">
          <img src="assets/team/{img}.jpg" alt="{name}, board member" width="560" height="560"></div>
        <div class="body"><span class="mtag">Board member</span><h3>{name}</h3>
          <span class="aff">{role}</span><p class="bio">{bio}</p>
          {f'<span class="todo">{todo}</span>' if todo else ''}</div>
      </article>""" for img, name, role, bio, todo in MEMBERS)

about = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">About</span>
    <h1>A health-tech company <em>with its own team.</em></h1>
    <p>Genesys Health Information Systems Limited was established in Lagos in 2017 to close the information gap that costs African health facilities money, time and trust.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap split wide-left">
    <div class="reveal">
      <h2 style="font-size:clamp(24px,3.2vw,34px);margin-bottom:14px">Why we exist</h2>
      <p style="margin-bottom:12px">The Nigerian healthcare industry is short of data of any sort, credible or otherwise, and studies place it among the sectors most resistant to information technology. Having worked in the sector, we identified the pain points early, and they persist today.</p>
      <p style="margin-bottom:12px">The consequence is blunt. Inefficiencies in management are why so many health businesses do not survive past the first generation.</p>
      <p class="muted">The answer is the same one that transformed engineering, banking, finance and audit: put the information in one place, and let the facility see itself clearly.</p>
    </div>
    <div class="figure reveal"><img src="assets/img/team.jpg" alt="A hospital management team meeting beside a ward" width="1600" height="533"></div>
  </div>
</section>

<section class="tight" style="background:var(--surface);border-block:1px solid var(--border)">
  <div class="wrap grid-2" style="gap:clamp(22px,3.5vw,44px)">
    <div class="reveal">
      <span class="eyebrow">Vision</span>
      <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 10px">To be the leading provider of simple, affordable health technology to public and private health systems in Africa.</h2>
      <span class="eyebrow" style="display:block;margin-top:20px">Mission</span>
      <h2 style="font-size:clamp(21px,2.6vw,27px);margin:8px 0 0">To digitise and optimise healthcare service delivery through unparalleled client-centric service and technology solutions.</h2>
    </div>
    <div class="reveal">
      <span class="eyebrow">Values &middot; IDEAL</span>
      <div style="display:grid;gap:14px;margin-top:14px">{values_html}</div>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">The team</span>
      <h2>The people building Genesys.</h2>
      <p>Our board brings together enterprise software leadership and healthcare operating experience, and sets the direction the company builds against.</p>
    </div>
    <div class="split wide-right reveal" style="margin-bottom:22px;align-items:start">
      <div class="portrait chair"><span class="role-tag">Chairman</span>
        <img src="assets/team/kunle.jpg" alt="Kunle Akinniran, Chairman of the Genesys board" width="560" height="560"></div>
      <div>
        <span class="eyebrow">Chairman of the board</span>
        <h2 style="font-size:clamp(27px,3.6vw,40px);margin:10px 0 4px">Kunle Akinniran</h2>
        <p style="color:var(--blue);font-weight:600;font-size:14.5px;margin-bottom:14px">Managing Director and CEO, Vatebra Limited</p>
        <p style="font-size:15.5px">A technology leader with over 20 years of experience, Kunle joined the Vatebra board in 2006. He was previously Group Head of IT at the defunct Fountain Trust Bank, where in 2001 he led the implementation of the Bankmaster and Branchpower banking systems, and he was part of the team that pioneered a scratch-card based online solution that carried Vatebra's work across Ghana, Sierra Leone and The Gambia. He holds a B.Sc in Computer Sciences from the University of Lagos and an MBA in International Business Management, and is a member of the Nigerian Computer Society, the Computer Professionals Registration Council of Nigeria and the Institute of Directors. He is a multiple-time winner of Tech Company CEO of the Year at the Nigeria Technology Awards.</p>
      </div>
    </div>
    <div class="grid-3">{member_cards}</div>
  </div>
</section>
{cta("Talk to the team behind Genesys.")}"""

# ------------------------------------------------------------- INSIGHTS
INS = [
    ("Insight","Closing the revenue leak between service and ledger"),
    ("Insight","What offline-first really means in a Nigerian clinic"),
    ("Insight","Preparing a facility for its first digital records system"),
]
NEWS = [
    ("Industry news","Population health management market outlook"),
    ("Industry news","Electronic health record market size projections"),
    ("Industry news","Vaccination and public health programmes across Africa"),
]
ins_cards = "".join(f'<a class="ins reveal" href="#"><span class="k">{k} &middot; fact needed</span><h3>{t}</h3>'
                    f'<p>[Article to be written and managed from the admin panel in a later stage.]</p></a>'
                    for k, t in INS)
news_cards = "".join(f'<a class="ins reveal" href="#"><span class="k">{k} &middot; source needed</span><h3>{t}</h3>'
                     f'<p>[A 40-word summary and an outbound link to the original publisher.]</p></a>'
                     for k, t in NEWS)

insights = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">Insights</span>
    <h1>From the sector <em>we work in.</em></h1>
    <p>Our own writing on health information systems in Africa, kept separate from curated industry news.</p>
  </div>
</section>
<section class="tight">
  <div class="wrap">
    <div class="sec-head reveal"><h2 style="font-size:clamp(23px,3vw,31px)">Written by Genesys</h2></div>
    <div class="grid-3">{ins_cards}</div>
  </div>
</section>
<section class="tight" style="background:var(--surface);border-block:1px solid var(--border)">
  <div class="wrap">
    <div class="sec-head reveal"><h2 style="font-size:clamp(23px,3vw,31px)">Industry news</h2>
      <p>Summaries only, each linking out to the original publisher.</p></div>
    <div class="grid-3">{news_cards}</div>
  </div>
</section>
{cta()}"""

# -------------------------------------------------------------- CONTACT
contact = f"""
<section class="phead">
  <div class="wrap">
    <span class="eyebrow">Contact</span>
    <h1>See Genesys on <em>your own workflow.</em></h1>
    <p>Tell us about the facility you run and we will show you the system built for it. We respond within one business day.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap split wide-left">
    <div class="form reveal">
      <div class="row2">
        <div class="field"><label for="name">Full name</label><input id="name" type="text" autocomplete="name"></div>
        <div class="field"><label for="email">Email address</label><input id="email" type="email" autocomplete="email"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="phone">Phone number</label><input id="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="facility">Facility name</label><input id="facility" type="text"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="ftype">Facility type</label>
          <select id="ftype"><option>Hospital</option><option>Clinic or practice</option><option>Diagnostic laboratory</option><option>Pharmacy</option><option>Public health system</option><option>HMO or payer</option></select></div>
        <div class="field"><label for="beds">Beds or sites</label>
          <select id="beds"><option>1 to 20 beds</option><option>20 to 100 beds</option><option>100 to 500 beds</option><option>Multi-site group</option><option>Not a hospital</option></select></div>
      </div>
      <div class="field"><label for="product">Product of interest</label>
        <select id="product"><option>Not sure yet, advise me</option><option>Genesys HMIS</option><option>Genesys EMR</option><option>Clinical Specialized Packages</option><option>Stand-alone Packages</option></select></div>
      <div class="field"><label for="msg">Message</label><textarea id="msg" placeholder="Tell us what you are trying to fix."></textarea></div>
      <button class="btn btn-primary" type="button">Request a demo <span class="arrow">&rarr;</span></button>
      <p class="needs" style="margin-top:10px">[Form is visual. Wiring to Supabase and email is a later stage.]</p>
    </div>
    <div class="reveal">
      <div class="figure"><img src="assets/img/reception.jpg" alt="A Genesys specialist guiding a practice manager at a clinic reception desk" width="1600" height="533"></div>
      <div style="margin-top:20px">
        <span class="eyebrow">Come and see us</span>
        <p class="addr" style="margin-top:10px;font-size:15px">Genesys Health Information Systems Limited<br>21a Fatai Idowu Arobieke Street,<br>Off Admiralty Way, Lekki Phase 1, Lagos</p>
        <p class="addr" style="margin-top:12px;font-size:15px"><b style="color:var(--text)">+234 903 600 1000</b><br>info@genesys-health.com</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
          <a class="btn btn-ghost" href="#">Chat on WhatsApp</a>
          <a class="btn btn-ghost" href="#">Book a consultation</a>
        </div>
      </div>
      <div style="margin-top:22px">
        <div class="step"><span class="n">01</span><div><b>Migration</b><p>Your paper and legacy records are brought across, not abandoned.</p></div></div>
        <div class="step"><span class="n">02</span><div><b>Training</b><p>Staff are trained on the real workflows they will use every day.</p></div></div>
        <div class="step"><span class="n">03</span><div><b>Support</b><p>A response commitment and a named line. <span class="needs">[SLA tiers: fact needed]</span></p></div></div>
        <div class="step"><span class="n">04</span><div><b>Your data stays yours</b><p>Full ownership and export, on request, at any time.</p></div></div>
      </div>
    </div>
  </div>
</section>"""

if __name__ == "__main__":
    page("index.html", "Genesys Health — hospital and records systems for African health facilities",
         "Genesys builds the hospital management and electronic medical records systems that African health facilities run on.", home)
    page("solutions.html", "Solutions — Genesys Health",
         "Genesys HMIS, EMR, Clinical Specialized Packages and Stand-alone Packages, sized to the practice you run.", solutions)
    page("who-we-serve.html", "Who we serve — Genesys Health",
         "Hospitals, clinics and practices, public health systems, and payers.", serve)
    page("proof.html", "Proof — Genesys Health",
         "Case studies, certifications and client evidence for Genesys Health.", proof)
    page("about.html", "About — Genesys Health",
         "Genesys Health Information Systems Limited: why we exist, our vision, mission, values and team.", about)
    page("insights.html", "Insights — Genesys Health",
         "Writing from Genesys on health information systems in Africa, plus curated industry news.", insights)
    page("contact.html", "Contact — Genesys Health",
         "Request a demo of Genesys, or book a consultation. Lekki Phase 1, Lagos.", contact)
    print("built", len(TABS), "pages")
