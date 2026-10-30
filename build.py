import json, os, html
from data import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
import shutil
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
for _f in ["style.css","main.js","logo.webp","logo.png","logo-full.png","favicon.png","og-image.png"]:
    shutil.copy(os.path.join(HERE, _f), os.path.join(OUT, "assets", _f))
pages_for_sitemap = []

def esc(s): return html.escape(s, quote=True)

def org_schema():
    return {
      "@context":"https://schema.org","@type":["ProfessionalService","LocalBusiness"],
      "@id":DOMAIN+"/#business","name":"Digital Connect",
      "alternateName":"Digital Connect - Digital Marketing Agency in Naigaon",
      "description":"Digital Connect is a digital marketing agency in Naigaon East, Vasai-Virar offering local SEO, Google Business Profile optimization, Google Ads, Meta ads, social media marketing, website development and lead generation.",
      "url":DOMAIN+"/","telephone":PHONE_INTL,"image":DOMAIN+"/assets/og-image.png","logo":DOMAIN+"/assets/logo-full.png",
      "priceRange":"₹₹",
      "address":{"@type":"PostalAddress","streetAddress":"E Wing, Global Arena, near Sunteck Naigaon","addressLocality":"Naigaon East","addressRegion":"Maharashtra","postalCode":"401208","addressCountry":"IN"},
      "areaServed":[{"@type":"City","name":a} for a in ["Naigaon","Vasai","Virar","Nalasopara","Mira-Bhayandar","Mumbai"]],
      "openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"},
      "founder":{"@type":"Person","name":OWNER,"jobTitle":"Digital Marketer & Founder","description":"Ankit Singh is a digital marketing expert in Naigaon with 4+ years of experience."},
      "hasMap":MAPS,
      "knowsAbout":["Local SEO","Search Engine Optimization","Google Business Profile","Google Ads","Facebook Ads","Instagram Marketing","Social Media Marketing","Website Development","Lead Generation"],
      "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["name"],"url":f"{DOMAIN}/services/{s['slug']}/"}} for s in SERVICES]
    }

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":DOMAIN+u} for i,(n,u) in enumerate(items)]}

def faq_schema(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def head(title, desc, path, schemas, noindex=False, keywords=""):
    url = DOMAIN + path
    s = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schemas)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    if not noindex: pages_for_sitemap.append(path)
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{f'<meta name="keywords" content="{esc(keywords)}">' if keywords else ''}
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="author" content="Digital Connect">
<meta name="theme-color" content="#140726">
<meta name="geo.region" content="IN-MH">
<meta name="geo.placename" content="Naigaon East, Vasai-Virar">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="Digital Connect">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">
<link rel="icon" href="/assets/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{s}
</head>
<body>
'''

def header(active=""):
    dd = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    a = lambda k: ' class="active"' if active==k else ''
    return f'''<div class="topbar">Free growth call for Naigaon &amp; Vasai-Virar businesses. <a href="{WA}?text=Hi%20Digital%20Connect%2C%20I%20want%20a%20free%20growth%20call" target="_blank" rel="noopener">Book on WhatsApp in 2 minutes</a></div>
<header class="header">
 <nav class="container nav" aria-label="Main navigation">
  <a href="/" class="brand" aria-label="Digital Connect home">
   <img src="/assets/logo.webp" alt="Digital Connect logo - digital marketing agency in Naigaon" width="44" height="44">
   <span class="brand-text"><strong>Digital Connect</strong><span>Get more customers online</span></span>
  </a>
  <ul class="menu" id="menu">
   <li><a href="/"{a("home")}>Home</a></li>
   <li class="has-sub"><a href="/services/"{a("services")}>Services ▾</a><ul class="dropdown">{dd}<li><a href="/services/"><b>All services →</b></a></li></ul></li>
   <li><a href="/about/"{a("about")}>About</a></li>
   <li><a href="/#process">Process</a></li>
   <li><a href="/blog/"{a("blog")}>Blog</a></li>
   <li><a href="/contact/"{a("contact")}>Contact</a></li>
  </ul>
  <div class="nav-cta">
   <a class="call-link" href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a>
   <a class="btn btn-primary" href="/contact/">Free Audit</a>
   <button class="burger" aria-label="Open menu" aria-controls="menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
 </nav>
</header>
<main>
'''

def footer():
    sv = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="footer">
 <div class="container">
  <div class="f-grid">
   <div>
    <a href="/" class="brand"><img src="/assets/logo.webp" alt="Digital Connect logo" width="44" height="44" loading="lazy"><span class="brand-text"><strong>Digital Connect</strong><span>Get more customers online</span></span></a>
    <p style="margin-top:18px">Digital Connect is a digital marketing agency in Naigaon East helping businesses across Vasai-Virar and Mumbai get found on Google, run ads that bring enquiries and build websites that convert.</p>
    <p class="areas"><b style="color:#fff">Areas we serve:</b> {", ".join(AREAS)}</p>
   </div>
   <div><h4>Services</h4><ul>{sv}</ul></div>
   <div><h4>Company</h4><ul>
     <li><a href="/">Home</a></li><li><a href="/about/">About Ankit Singh</a></li><li><a href="/services/">All services</a></li>
     <li><a href="/#process">Our process</a></li><li><a href="/blog/">Blog</a></li><li><a href="/#faq">FAQs</a></li><li><a href="/contact/">Contact</a></li>
     <li><a href="{MAPS}" target="_blank" rel="noopener">Google reviews</a></li></ul></div>
   <div><h4>Visit or call us</h4>
    <p>{"<br>".join(ADDRESS_LINES)}</p>
    <p style="margin-top:12px"><a href="tel:{PHONE_INTL}">📞 {PHONE_DISPLAY}</a><br><a href="{WA}" target="_blank" rel="noopener">💬 WhatsApp us</a><br>🕒 Open 24 hours</p>
    <p style="margin-top:12px"><a href="{MAPS}" target="_blank" rel="noopener" style="color:var(--orange-2);font-weight:700">Get directions →</a></p>
   </div>
  </div>
  <div class="f-bottom"><span>© <span id="yr">2026</span> Digital Connect, Naigaon East. All rights reserved.</span><span>Digital marketing agency in Naigaon · Vasai · Virar</span></div>
 </div>
</footer>
<a class="wa-float" href="{WA}?text=Hi%20Digital%20Connect%2C%20I%20want%20to%20grow%20my%20business%20online" target="_blank" rel="noopener" aria-label="Chat with Digital Connect on WhatsApp">{WA_SVG}<span>WhatsApp us</span></a>
<script src="/assets/main.js" defer></script>
</body>
</html>
'''

def lead_form(heading="Get your free growth plan", sub="Share a few details. We reply within a few hours, usually on WhatsApp."):
    opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES)
    return f'''<form class="form" name="lead" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="company_url" data-wa>
  <input type="hidden" name="form-name" value="lead">
  <p hidden><label>Leave empty <input name="company_url"></label></p>
  <h3>{heading}</h3><p>{sub}</p>
  <div class="two">
   <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required autocomplete="name"></div>
   <div class="field"><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel" required pattern="[0-9+ ]{{10,14}}" autocomplete="tel"></div>
  </div>
  <div class="field"><label for="f-biz">Business name &amp; area</label><input id="f-biz" name="business" placeholder="e.g. Sai Clinic, Naigaon East"></div>
  <div class="field"><label for="f-svc">What do you need help with?</label><select id="f-svc" name="service"><option>Not sure, suggest a plan</option>{opts}</select></div>
  <div class="field"><label for="f-msg">Anything else?</label><textarea id="f-msg" name="message" rows="3" placeholder="Your goal, budget or current challenge"></textarea></div>
  <button class="btn btn-primary" type="submit">Get my free plan →</button>
 </form>'''

def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faqs) + '</div>'

def cta_band(title="Ready to get more customers online?", text="Tell us about your business and get a clear, no-jargon growth plan from a digital marketing agency in Naigaon that actually picks up the phone."):
    return f'''<section><div class="container"><div class="cta-band reveal">
  <span class="eyebrow">Let's talk</span><h2>{title}</h2><p>{text}</p>
  <div class="btn-row"><a class="btn btn-primary" href="{WA}?text=Hi%20Digital%20Connect%2C%20I%20want%20a%20free%20growth%20call" target="_blank" rel="noopener">WhatsApp for a free call →</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}">Call {PHONE_DISPLAY}</a></div>
 </div></div></section>'''

def write(path, content):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

# ================= HOME =================
def home():
    svc_rows = "".join(f'''<a class="svc-row" href="/services/{s['slug']}/"><span class="ico">{ICONS[s['icon']]}</span><span><h3>{s['name']}</h3><p>{s['short']}</p></span><span class="arrow">→</span></a>''' for s in SERVICES)
    chips = "".join(f'<span class="chip">{i}</span>' for i in INDUSTRIES)
    steps = [("Discover","Your goals, offer and where enquiries are leaking."),("Strategy","A plain 30-day plan for Google, ads or your website."),("Build","Profiles, pages, campaigns and tracking set up right."),("Launch","Go live with clear ownership and weekly checks."),("Optimize","Lower cost per enquiry, not chase vanity clicks.")]
    steps_html = "".join(f'<div class="step reveal"><b>0{i+1}</b><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(steps))
    kw = "digital marketing agency near me, best digital marketing agency Naigaon, top digital marketing agency in Naigaon, digital marketing expert, Ankit Singh digital marketer, lead generation agency Naigaon, social media marketing near me, Facebook marketing, Instagram marketing, SEO analysis near me, Meta ads agency near me Naigaon, Google Ads agency near me"
    body = head("Best Digital Marketing Agency in Naigaon | Digital Connect",
        "Searching for a digital marketing agency near me? Digital Connect is the best digital marketing agency in Naigaon for SEO, Google Ads, Meta ads and lead generation.",
        "/", [org_schema(), {"@context":"https://schema.org","@type":"WebSite","name":"Digital Connect","url":DOMAIN+"/"}, faq_schema(HOME_FAQS)], keywords=kw)
    body += header("home") + f'''
<section class="hero dark">
 <div class="blob b1"></div><div class="blob b2"></div>
 <div class="container">
  <div>
   <h1><span class="eyebrow" style="display:block">Best digital marketing agency in Naigaon</span>Get more customers from <span class="hl">Google, Instagram</span> &amp; your website</h1>
   <p class="lead">Digital Connect is a top digital marketing agency in Naigaon, led by digital marketer Ankit Singh. We help local businesses in Naigaon, Vasai, Virar and Mumbai get found online and turn visitors into real enquiries. Clear plans. Plain language. No jargon.</p>
   <div class="btn-row"><a class="btn btn-primary" href="{WA}?text=Hi%20Digital%20Connect%2C%20I%20want%20a%20free%20growth%20call" target="_blank" rel="noopener">Book a free call →</a><a class="btn btn-ghost" href="/services/">See our services</a></div>
   <div class="hero-badges"><span>⭐ 4.6 on Google</span><span>4+ years experience</span><span>Open 24 hours</span></div>
  </div>
  <div class="hero-card reveal" aria-hidden="true">
   <h3>What we focus on</h3><p>Every plan is measured on the numbers that matter to a business owner.</p>
   <div class="metric"><span>Google Maps visibility</span><b class="up">▲</b></div><div class="bar"><i style="--w:86%"></i></div>
   <div class="metric"><span>Calls &amp; WhatsApp enquiries</span><b class="up">▲</b></div><div class="bar"><i style="--w:78%"></i></div>
   <div class="metric"><span>Cost per enquiry</span><b style="color:var(--orange-2)">▼</b></div><div class="bar"><i style="--w:42%"></i></div>
   <div class="metric"><span>Monthly report</span><b>Plain language</b></div>
  </div>
 </div>
</section>

<section aria-labelledby="proof">
 <div class="container reveal">
  <span class="eyebrow">Proof in numbers</span>
  <h2 id="proof">Results local businesses care about</h2>
  <div class="stats">
   <div class="stat"><strong data-count="4" data-suffix="+">4+</strong><span>Years of experience</span><small>Hands-on digital marketing</small></div>
   <div class="stat"><strong data-count="4.6" data-suffix="★">4.6★</strong><span>Google rating</span><small>From real client reviews</small></div>
   <div class="stat"><strong data-count="8" data-suffix="+">8+</strong><span>Core services</span><small>SEO, ads, social &amp; web</small></div>
   <div class="stat"><strong>24/7</strong><span>Open hours</span><small>WhatsApp us anytime</small></div>
  </div>
 </div>
</section>

<section class="cream" aria-labelledby="how">
 <div class="container">
  <div class="reveal"><span class="eyebrow">Trusted by growing businesses in Vasai-Virar</span>
  <h2 id="how">How we help your business grow</h2>
  <p class="lead">Three plain goals. No buzzwords. Just more of the right people finding you and getting in touch.</p></div>
  <div class="grid-3">
   <div class="goal reveal"><div class="ico">{ICONS['search']}</div><h3>Get found online</h3><p>Show up when people search for what you sell, on Google Search, Google Maps and AI results. Our <a href="/services/local-seo-naigaon/" style="color:var(--purple);font-weight:600">local SEO in Naigaon</a> work starts here.</p></div>
   <div class="goal reveal"><div class="ico">{ICONS['phone']}</div><h3>Turn visits into calls</h3><p>Ads, posts and a clear website that make people reach out to you on call or WhatsApp.</p></div>
   <div class="goal reveal"><div class="ico">{ICONS['chart']}</div><h3>Know what works</h3><p>Simple monthly updates in plain language, so you see where every rupee goes.</p></div>
  </div>
 </div>
</section>

<section class="dark" aria-labelledby="what">
 <div class="container">
  <div class="reveal"><span class="eyebrow">What we do</span>
  <h2 id="what">Digital marketing services in Naigaon &amp; Vasai-Virar</h2>
  <p class="lead">Simple services that bring more people to your business and help them become customers.</p></div>
  <div class="svc-list reveal">{svc_rows}</div>
  <div class="btn-row"><a class="btn btn-ghost" href="/services/">See all services →</a></div>
 </div>
</section>

<section id="process" aria-labelledby="proc">
 <div class="container">
  <div class="reveal"><span class="eyebrow">How we work</span><h2 id="proc">A clear process, not chaos</h2>
  <p class="lead">The same five steps for every client, so you always know what is happening and what comes next.</p></div>
  <div class="steps">{steps_html}</div>
 </div>
</section>

<section class="dark" aria-labelledby="ind">
 <div class="container reveal">
  <span class="eyebrow">Who we help</span><h2 id="ind">Industries we work with</h2>
  <p class="lead">From real estate projects in Naigaon to clinics in Vasai and cafes in Virar, we build campaigns around how your customers buy.</p>
  <div class="marquee"><div class="marquee-track">{chips}{chips}</div></div>
 </div>
</section>

<section class="cream" aria-labelledby="rev">
 <div class="container">
  <div class="review-box reveal">
   <div>
    <div class="rating"><div class="gmark">G</div><div><strong>4.6</strong><div class="stars">★★★★★</div></div></div>
    <p style="margin-top:12px">Rated by real clients on our Google Business Profile.</p>
   </div>
   <div>
    <span class="eyebrow">Google reviews</span>
    <h2 id="rev" style="font-size:2rem">What clients say on Google</h2>
    <p style="margin-top:10px">Read honest feedback from business owners we have worked with, or share your own experience with Digital Connect.</p>
    <div class="btn-row"><a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">Read our Google reviews</a><a class="btn btn-outline" href="{MAPS}" target="_blank" rel="noopener">Write a review</a></div>
   </div>
  </div>
 </div>
</section>

<section class="dark" id="audit" aria-labelledby="plan">
 <div class="container form-wrap">
  <div class="reveal">
   <span class="eyebrow">Free audit</span>
   <h2 id="plan">Tell us about your business. We'll show you a clear plan.</h2>
   <p class="lead">Talk directly with {OWNER}, founder of Digital Connect, about your goals.</p>
   <ul class="checks">
    <li>Free check of your Google Business Profile and website</li>
    <li>Keyword and competitor snapshot for your area</li>
    <li>A simple 30-day action plan, yours to keep</li>
    <li>No contracts or pressure, just honest advice</li>
   </ul>
  </div>
  <div class="reveal">{lead_form()}</div>
 </div>
</section>

<section class="cream" aria-labelledby="near">
 <div class="container content-grid">
  <div class="prose reveal">
   <span class="eyebrow">Searching nearby?</span>
   <h2 id="near">Looking for a digital marketing agency near me in Naigaon?</h2>
   <p>If you are searching for a <b>digital marketing agency near me</b> in Naigaon East, Naigaon West, Vasai or Virar, Digital Connect is right at Global Arena, near Sunteck Naigaon. You can meet us in person, see your plan on screen and talk to the person who actually runs your campaigns.</p>
   <h3>A digital marketing expert you can meet</h3>
   <p>Every strategy is planned by <a href="/about/">Ankit Singh, digital marketer</a> and founder of Digital Connect. As a digital marketing expert with 4+ years of local experience, he knows which channels work for Vasai-Virar buyers.</p>
   <h3>Everything under one roof</h3>
   <ul>
    <li><a href="/services/seo-analysis/">SEO analysis near me</a>: a free check of your website and Google profile</li>
    <li><a href="/services/google-ads-agency-naigaon/">Google Ads agency near me</a> for instant enquiries</li>
    <li><a href="/services/meta-ads-agency-naigaon/">Meta ads agency in Naigaon</a> for Facebook and Instagram leads</li>
    <li><a href="/services/social-media-marketing-naigaon/">Social media marketing near me</a> with reels and posts</li>
    <li><a href="/services/facebook-marketing/">Facebook marketing</a> and <a href="/services/instagram-marketing/">Instagram marketing</a> for local reach</li>
    <li><a href="/services/lead-generation-agency-naigaon/">Lead generation agency in Naigaon</a> for complete lead systems</li>
   </ul>
  </div>
  <aside class="side reveal">
   <h3>Visit Digital Connect</h3>
   <p>E Wing, Global Arena, near Sunteck Naigaon, Naigaon East 401208</p>
   <p style="margin-top:8px">Open 24 hours · ⭐ 4.6 on Google</p>
   <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>
   <a class="btn btn-outline" href="tel:{PHONE_INTL}">Call {PHONE_DISPLAY}</a>
  </aside>
 </div>
</section>

<section id="faq" aria-labelledby="faqh">
 <div class="container">
  <div class="reveal" style="text-align:center"><span class="eyebrow">FAQs</span><h2 id="faqh">Questions about our digital marketing agency</h2></div>
  {faq_html(HOME_FAQS)}
 </div>
</section>

<section aria-labelledby="areas">
 <div class="container light">
  <div class="reveal"><span class="eyebrow">Areas we serve</span><h2 id="areas">Your local digital marketing partner in Vasai-Virar</h2>
  <p class="lead">Based at Global Arena, Naigaon East, we work with businesses across the Vasai-Virar belt and Mumbai's western suburbs.</p>
  <div class="chips">{"".join(f'<span class="chip">📍 {a}</span>' for a in AREAS)}</div></div>
  <iframe class="map reveal" style="margin-top:36px" src="{MAP_EMBED}" title="Digital Connect location on Google Maps, Global Arena, Naigaon East" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
 </div>
</section>
''' + home_blog_section() + cta_band() + footer()
    write("/", body)

# ================= SERVICES INDEX =================
def services_index():
    cats = {}
    for s in SERVICES: cats.setdefault(s["cat"], []).append(s)
    blocks = ""
    for c, items in cats.items():
        cards = "".join(f'<a class="card reveal" href="/services/{s["slug"]}/"><div class="goal" style="padding:0;border:0"><div class="ico">{ICONS[s["icon"]]}</div></div><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="more">Learn more →</span></a>' for s in items)
        blocks += f'<div class="cat"><h2>{c}</h2><div class="cards">{cards}</div></div>'
    bc = breadcrumb([("Home","/"),("Services","/services/")])
    body = head("Digital Marketing Services in Naigaon | Digital Connect",
        "Explore Digital Connect's digital marketing services in Naigaon and Vasai-Virar: local SEO, Google Business Profile, Google Ads, Meta ads, social media, websites and lead generation.",
        "/services/", [org_schema(), bc])
    body += header("services") + f'''
<section class="page-hero dark"><div class="container">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Services</nav>
 <span class="eyebrow">What we do</span>
 <h1>Digital marketing services for local businesses</h1>
 <p class="lead" style="color:#D8CFF0">Practical help to get found online and turn interest into calls and enquiries. Every service from our digital marketing agency in Vasai Virar is built around one goal: more customers for you.</p>
</div></section>
<section style="padding-top:30px"><div class="container">{blocks}</div></section>
''' + cta_band("Not sure which service you need?", "Tell us your goal. We'll recommend the right mix, even if that means starting small.") + footer()
    write("/services/", body)

# ================= SERVICE PAGES =================
def service_page(s):
    prose = ""
    for h, paras in s["body"]:
        prose += f"<h2>{h}</h2>"
        if paras and paras[0] == "__list__":
            prose += "<ul>" + "".join(f"<li>{p}</li>" for p in paras[1:]) + "</ul>"
        else:
            prose += "".join(f"<p>{p}</p>" for p in paras)
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    related = "".join(f'<li><a href="/services/{o["slug"]}/">{o["name"]} →</a></li>' for o in others)
    prose += f'<h2>Why choose Digital Connect?</h2><p>We are a local team in Naigaon East led by {OWNER}, with 4+ years of hands-on experience and a 4.6 star Google rating. You get one point of contact, honest timelines and reports you can actually read. See all our <a href="/services/">digital marketing services</a> or <a href="/about/">learn more about us</a>.</p>'
    path = f"/services/{s['slug']}/"
    svc_schema = {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["name"],"description":s["desc"],"url":DOMAIN+path,
                  "provider":{"@id":DOMAIN+"/#business"},"areaServed":["Naigaon","Vasai","Virar","Nalasopara","Mira-Bhayandar","Mumbai"]}
    bc = breadcrumb([("Home","/"),("Services","/services/"),(s["name"],path)])
    body = head(s["title"], s["desc"], path, [org_schema(), svc_schema, bc, faq_schema(s["faqs"])])
    body += header("services") + f'''
<section class="page-hero dark"><div class="blob b1"></div><div class="container" style="position:relative;z-index:2">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/services/">Services</a> / {s["name"]}</nav>
 <span class="eyebrow">{s["cat"]}</span>
 <h1>{s["h1"]}</h1>
 <p class="lead" style="color:#D8CFF0">{s["intro"]}</p>
 <div class="btn-row"><a class="btn btn-primary" href="{WA}?text={esc(('Hi Digital Connect, I am interested in '+s['name']).replace(' ','%20'))}" target="_blank" rel="noopener">Get a free quote →</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}">Call {PHONE_DISPLAY}</a></div>
</div></section>
<section><div class="container content-grid">
 <article class="prose reveal">{prose}</article>
 <aside class="side">
  <h3>Free {s["name"]} audit</h3><p>Get a quick check of where you stand and what to fix first.</p>
  <a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">WhatsApp us</a>
  <a class="btn btn-outline" href="/contact/">Send an enquiry</a>
  <ul>{related}</ul>
 </aside>
</div></section>
<section class="cream"><div class="container">
 <div style="text-align:center" class="reveal"><span class="eyebrow">FAQs</span><h2>{s["name"]}: common questions</h2></div>
 {faq_html(s["faqs"])}
</div></section>
''' + cta_band() + footer()
    write(path, body)

# ================= ABOUT =================
def about():
    bc = breadcrumb([("Home","/"),("About","/about/")])
    person = {"@context":"https://schema.org","@type":"ProfilePage","url":DOMAIN+"/about/","mainEntity":{"@type":"Person","@id":DOMAIN+"/#ankit-singh","name":OWNER,"jobTitle":"Digital Marketer","description":"Ankit Singh is a digital marketing expert and founder of Digital Connect, a digital marketing agency in Naigaon East with 4+ years of experience.","worksFor":{"@id":DOMAIN+"/#business"},"knowsAbout":["Digital Marketing","SEO","Google Ads","Meta Ads","Facebook Marketing","Instagram Marketing","Lead Generation"],"address":{"@type":"PostalAddress","addressLocality":"Naigaon East","addressRegion":"Maharashtra","addressCountry":"IN"}}}
    body = head("Ankit Singh | Digital Marketer & Expert in Naigaon",
        f"Meet {OWNER}, digital marketer and digital marketing expert from Naigaon, founder of Digital Connect. 4+ years in SEO, Google Ads, Meta ads and lead generation.",
        "/about/", [org_schema(), person, bc])
    body += header("about") + f'''
<section class="page-hero dark"><div class="container">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / About</nav>
 <span class="eyebrow">About us</span>
 <h1>Ankit Singh, digital marketer &amp; founder of Digital Connect</h1>
 <p class="lead" style="color:#D8CFF0">A digital marketing expert from Naigaon who started Digital Connect with a simple idea: local business owners deserve marketing they can understand, measure and trust.</p>
</div></section>
<section><div class="container about-grid">
 <div class="prose reveal">
  <h2>About Digital Connect</h2>
  <p>Digital Connect is a digital marketing agency in Naigaon East, located at Global Arena near Sunteck Naigaon. We help shops, clinics, builders, coaching classes and service businesses across Vasai-Virar get found on Google and turn that attention into calls, WhatsApp messages and walk-ins.</p>
  <p>We keep things simple. No confusing jargon, no long lock-in contracts and no vanity metrics. Just clear plans, honest timelines and monthly reports that show what is working.</p>
  <h2>Why work with a digital marketing expert you can meet</h2><p>When you hire Digital Connect, you work directly with Ankit, not a call centre. He plans your strategy, reviews your numbers every week and explains results in plain language, whether it is <a href="/services/google-ads-agency-naigaon/">Google Ads</a>, <a href="/services/meta-ads-agency-naigaon/">Meta ads</a> or <a href="/services/lead-generation-agency-naigaon/">lead generation</a>.</p><h2>What we believe</h2>
  <ul><li>Local businesses need local expertise</li><li>Every rupee spent should be tracked</li><li>Good marketing builds trust before it asks for the sale</li><li>Owners should always own their accounts and data</li></ul>
  <p>Explore our <a href="/services/">services</a> or <a href="/contact/">contact us</a> for a free audit.</p>
 </div>
 <div class="owner-card reveal">
  <div class="avatar">AS</div>
  <h3 style="font-size:1.6rem">{OWNER}</h3>
  <p style="color:var(--orange-2);font-weight:700;margin-bottom:12px">Digital Marketer · Founder, Digital Connect</p>
  <p>Ankit Singh is a digital marketing expert based in Naigaon. With 4+ years of hands-on experience in local SEO, Google Business Profile management, Google and Meta ads and website development, Ankit personally plans every client strategy. He has worked closely with real estate builders, channel partners and local service businesses across Mira Road, Naigaon and Vasai-Virar.</p>
  <div class="btn-row"><a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Talk to Ankit →</a></div>
 </div>
</div></section>
<section class="cream"><div class="container">
 <div class="stats reveal">
  <div class="stat"><strong data-count="4" data-suffix="+">4+</strong><span>Years of experience</span></div>
  <div class="stat"><strong data-count="4.6" data-suffix="★">4.6★</strong><span>Google rating</span></div>
  <div class="stat"><strong data-count="8" data-suffix="+">8+</strong><span>Core services</span></div>
  <div class="stat"><strong>24/7</strong><span>WhatsApp support</span></div>
 </div>
</div></section>
''' + cta_band() + footer()
    write("/about/", body)

# ================= CONTACT =================
def contact():
    bc = breadcrumb([("Home","/"),("Contact","/contact/")])
    cp = {"@context":"https://schema.org","@type":"ContactPage","url":DOMAIN+"/contact/","mainEntity":{"@id":DOMAIN+"/#business"}}
    body = head("Contact Digital Connect | Digital Marketing in Naigaon",
        f"Contact Digital Connect, digital marketing agency at Global Arena, Naigaon East, Vasai-Virar. Call or WhatsApp {PHONE_DISPLAY} for a free SEO, ads or website audit.",
        "/contact/", [org_schema(), cp, bc])
    body += header("contact") + f'''
<section class="page-hero dark"><div class="container">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Contact</nav>
 <span class="eyebrow">Contact</span>
 <h1>Let's grow your business together</h1>
 <p class="lead" style="color:#D8CFF0">Call, WhatsApp or visit us at Global Arena, Naigaon East. We are open 24 hours and usually reply within a few hours.</p>
</div></section>
<section><div class="container form-wrap light">
 <div class="reveal">
  <h2 style="font-size:2rem">Get in touch</h2>
  <ul class="checks">
   <li><b>Call:</b> <a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a></li>
   <li><b>WhatsApp:</b> <a href="{WA}" target="_blank" rel="noopener">Chat with us now</a></li>
   <li><b>Office:</b> {ADDRESS_ONE}</li>
   <li><b>Hours:</b> Open 24 hours, 7 days</li>
  </ul>
  <iframe class="map" style="margin-top:24px" src="{MAP_EMBED}" title="Map to Digital Connect, Global Arena, Naigaon East" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
 </div>
 <div class="reveal">{lead_form("Request your free audit")}</div>
</div></section>
''' + footer()
    write("/contact/", body)

def thank_you():
    body = head("Thank You | Digital Connect", "Thanks for contacting Digital Connect. We will get back to you shortly.", "/thank-you/", [], noindex=True)
    body += header() + f'''
<section class="page-hero dark" style="min-height:60vh"><div class="container" style="text-align:center">
 <span class="eyebrow">Received ✓</span>
 <h1>Thank you! We'll be in touch soon.</h1>
 <p class="lead" style="color:#D8CFF0;margin:16px auto 0">Your details reached us. Want a faster reply? Send them on WhatsApp too.</p>
 <div class="btn-row" style="justify-content:center"><a id="wa-send" class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Send on WhatsApp →</a><a class="btn btn-ghost" href="/">Back to home</a></div>
</div></section>
<script>try{{var m=sessionStorage.getItem('dc_wa');if(m)document.getElementById('wa-send').href='{WA}?text='+m}}catch(e){{}}</script>
''' + footer()
    write("/thank-you/", body)

def not_found():
    body = head("Page Not Found | Digital Connect", "This page does not exist. Explore Digital Connect's digital marketing services in Naigaon.", "/404", [], noindex=True)
    body += header() + '''<section class="page-hero dark" style="min-height:60vh"><div class="container" style="text-align:center">
 <span class="eyebrow">404</span><h1>Oops, this page is missing</h1>
 <p class="lead" style="color:#D8CFF0;margin:16px auto 0">Let's get you back on track.</p>
 <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/">Go home</a><a class="btn btn-ghost" href="/services/">View services</a></div>
</div></section>''' + footer()
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(body)

# ================= BLOG =================
import re, datetime
from blogs_a import POSTS_A
from blogs_b import POSTS_B
BUILD_DATE = os.environ.get("BUILD_DATE") or (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date().isoformat()  # India time
ALL_POSTS = POSTS_A + POSTS_B
LIVE = sorted([p for p in ALL_POSTS if p["date"] <= BUILD_DATE], key=lambda p: p["date"], reverse=True)

def inline(t):
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)

def md(text):
    out, inlist = [], False
    for line in text.strip().split("\n"):
        line = line.rstrip()
        if not line:
            if inlist: out.append("</ul>" if inlist=="ul" else "</ol>"); inlist=False
            continue
        m = re.match(r'^(\d+)\. (.*)', line)
        if line.startswith("- ") or m:
            tag = "ul" if line.startswith("- ") else "ol"
            if inlist != tag:
                if inlist: out.append("</%s>" % inlist)
                out.append("<%s>" % tag); inlist = tag
            out.append("<li>%s</li>" % inline(line[2:] if tag=="ul" else m.group(2))); continue
        if inlist: out.append("</%s>" % inlist); inlist=False
        if line.startswith("### "): out.append("<h3>%s</h3>" % inline(line[4:]))
        elif line.startswith("## "): out.append("<h2>%s</h2>" % inline(line[3:]))
        else: out.append("<p>%s</p>" % inline(line))
    if inlist: out.append("</%s>" % inlist)
    return "\n".join(out)

def nice(d): return datetime.date.fromisoformat(d).strftime("%d %b %Y")
def words(p): return len(re.sub(r'<.*?>','',md(p["body"])).split())

def post_card(p):
    return f'<a class="card reveal" href="/blog/{p["slug"]}/"><span class="eyebrow" style="margin-bottom:8px">{p["cat"]} · {nice(p["date"])}</span><h3>{p["title"]}</h3><p>{p["excerpt"]}</p><span class="more">Read article →</span></a>'

def blog_index():
    cards = "".join(post_card(p) for p in LIVE)
    bc = breadcrumb([("Home","/"),("Blog","/blog/")])
    bl = {"@context":"https://schema.org","@type":"Blog","name":"Digital Connect Blog","url":DOMAIN+"/blog/","publisher":{"@id":DOMAIN+"/#business"},
          "blogPost":[{"@type":"BlogPosting","headline":p["title"],"url":f"{DOMAIN}/blog/{p['slug']}/","datePublished":p["date"]} for p in LIVE]}
    body = head("Digital Marketing Blog: SEO, Ads & Social Media Tips | Digital Connect",
        "Practical digital marketing tips for Naigaon and Vasai-Virar businesses: local SEO, Google AI Mode, Google Business Profile, Meta ads, Instagram and WhatsApp marketing.",
        "/blog/", [org_schema(), bl, bc])
    body += header("blog") + f"""
<section class="page-hero dark"><div class="container">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Blog</nav>
 <span class="eyebrow">Blog</span>
 <h1>Digital marketing tips for local businesses</h1>
 <p class="lead" style="color:#D8CFF0">Plain-language guides on SEO, Google Business Profile, ads, Instagram and WhatsApp from the Digital Connect team in Naigaon.</p>
</div></section>
<section style="padding-top:60px"><div class="container"><div class="cards">{cards}</div></div></section>
""" + cta_band() + footer()
    write("/blog/", body)

def blog_post(p):
    path = f"/blog/{p['slug']}/"
    others = [o for o in LIVE if o["slug"] != p["slug"]][:4]
    rel = "".join(f'<li><a href="/blog/{o["slug"]}/">{o["title"]}</a></li>' for o in others)
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]} →</a></li>' for s in SERVICES[:6])
    art = {"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],"description":p["desc"],"url":DOMAIN+path,
           "mainEntityOfPage":DOMAIN+path,"datePublished":p["date"],"dateModified":p["date"],"image":DOMAIN+"/assets/og-image.png",
           "keywords":p["kw"],"wordCount":words(p),
           "author":{"@type":"Person","name":OWNER,"url":DOMAIN+"/about/","jobTitle":"Digital Marketer"},
           "publisher":{"@type":"Organization","name":"Digital Connect","logo":{"@type":"ImageObject","url":DOMAIN+"/assets/logo-full.png"}}}
    bc = breadcrumb([("Home","/"),("Blog","/blog/"),(p["title"],path)])
    mins = max(3, round(words(p)/200))
    body = head(p["title"]+" | Digital Connect" if len(p["title"])<45 else p["title"], p["desc"], path, [org_schema(), art, bc, faq_schema(p["faqs"])])
    body += header("blog") + f"""
<section class="page-hero dark"><div class="blob b1"></div><div class="container" style="position:relative;z-index:2">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {p["cat"]}</nav>
 <span class="eyebrow">{p["cat"]}</span>
 <h1>{p["h1"]}</h1>
 <p class="lead" style="color:#D8CFF0">By <a href="/about/" style="color:#fff;font-weight:700">{OWNER}</a>, digital marketer · {nice(p["date"])} · {mins} min read</p>
</div></section>
<section><div class="container content-grid">
 <article class="prose reveal">{md(p["body"])}
  <h2>Frequently asked questions</h2>
  <div class="faq" style="margin-top:10px">{"".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in p["faqs"])}</div>
 </article>
 <aside class="side">
  <h3>Need help with this?</h3><p>Get a free audit from a digital marketing agency in Naigaon.</p>
  <a class="btn btn-primary" href="{WA}?text=Hi%20Digital%20Connect%2C%20I%20read%20your%20blog%20and%20want%20help" target="_blank" rel="noopener">WhatsApp us</a>
  <a class="btn btn-outline" href="/contact/">Free audit</a>
  {f'<h3 style="margin-top:26px;font-size:1.05rem">More articles</h3><ul>{rel}</ul>' if rel else ''}
  <h3 style="margin-top:26px;font-size:1.05rem">Our services</h3><ul>{svc}</ul>
 </aside>
</div></section>
""" + cta_band() + footer()
    write(path, body)

def home_blog_section():
    if not LIVE: return ""
    cards = "".join(post_card(p) for p in LIVE[:3])
    return f"""<section class="cream" aria-labelledby="blogh"><div class="container">
 <div class="reveal"><span class="eyebrow">From the blog</span><h2 id="blogh">Latest digital marketing tips</h2></div>
 <div class="cards">{cards}</div>
 <div class="btn-row"><a class="btn btn-outline" href="/blog/">View all articles →</a></div>
</div></section>"""

def extras():
    import datetime
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{today}</lastmod><priority>{'1.0' if p=='/' else '0.8'}</priority></url>" for p in pages_for_sitemap)
    open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")

home(); services_index()
for s in SERVICES: service_page(s)
about(); contact(); thank_you(); not_found()
blog_index()
for p in LIVE: blog_post(p)
extras()
print('live posts:', len(LIVE), 'scheduled:', len(ALL_POSTS)-len(LIVE))
print("pages:", pages_for_sitemap)
