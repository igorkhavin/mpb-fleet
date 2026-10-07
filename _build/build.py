"""Builds the MPB Fleet subpages. Run from the repo root: python3 _build/build.py
(Folders starting with _ are not published by GitHub Pages.)"""
import json, os, html

SITE = "https://mpbfleet.com"
PHONE, TEL = "(916) 533-1695", "+19165331695"
EMAIL = "mpbfleet@gmail.com"
FORM = f"https://formsubmit.co/{EMAIL}"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%23111'/%3E"
           "%3Ctext x='32' y='43' font-family='Arial' font-weight='700' font-size='26' fill='%23c8102e' text-anchor='middle'%3EMPB%3C/text%3E%3C/svg%3E")

INDUSTRIES = [
  dict(slug="hvac", name="HVAC", plural="HVAC companies",
       h1='No van, <em>no service call.</em>',
       sub="When a service van is down in July, the calls don't stop. We get HVAC vans and pickups back on the road first.",
       vehicles="service vans, box vans and pickups with ladder racks",
       pains=[("Summer can't wait","When it's 105° out, a van in the shop costs you jobs every hour. Fleet vehicles go to the front of our line."),
              ("Heavy loads, hard brakes","Vans carrying condensers and tools wear brakes, suspension and tires fast. We catch it at the inspection."),
              ("Racks and dings","Ladder racks, side scrapes and backing damage. Body and paint are done in the same building as the mechanical work.")]),
  dict(slug="plumbing", name="Plumbing", plural="plumbing companies",
       h1='A plumber without a van is <em>a missed call.</em>',
       sub="Emergency calls go to whoever shows up first. We keep plumbing vans ready to roll.",
       vehicles="service vans, box trucks and pickups",
       pains=[("Emergency-ready","Drop keys after hours and we start first thing, so the van is back before the next emergency."),
              ("Weight and wear","Pipe, jetters and water heaters are heavy. We keep brakes, suspension and tires in spec."),
              ("One invoice","Every van's repairs on one monthly statement, on Net 30 terms up to $5,000.")]),
  dict(slug="electrical", name="Electrical", plural="electrical contractors",
       h1='Your electricians bill by the hour. <em>Your van shouldn\'t cost them hours.</em>',
       sub="Priority repair for electrical contractor fleets in Rancho Cordova and Sacramento.",
       vehicles="service vans, pickups with racks and utility bodies",
       pains=[("Crew downtime","A van in the shop means a crew standing around. Priority service gets them back on the job."),
              ("Charging and starting","Inverters, lights and tools drain batteries and charging systems. Free diagnostics find it fast."),
              ("Approve by text","You get a digital estimate before any work and approve it from your phone.")]),
  dict(slug="pest-control", name="Pest control", plural="pest control companies",
       h1='Routes <em>don\'t wait.</em>',
       sub="Missed stops mean unhappy customers. We keep pest control trucks running their routes.",
       vehicles="pickups, small trucks and vans",
       pains=[("Route-day reliability","Free pickup and drop-off, so a tech doesn't lose a route day driving to the shop."),
              ("High mileage","Stop-and-go routes are hard on brakes, transmissions and cooling. We stay ahead of it."),
              ("Clean, professional trucks","Dings and faded paint make a bad first impression. Body and paint, in-house.")]),
  dict(slug="landscaping", name="Landscaping", plural="landscaping companies",
       h1='Trucks that pull <em>all day.</em>',
       sub="Landscape trucks tow trailers and haul heavy loads. We keep them working through the season.",
       vehicles="pickups and light-duty trucks that tow trailers",
       pains=[("Towing wear","Trailer loads work transmissions, brakes and cooling hard. We inspect what towing wears out."),
              ("Trailer wiring","Lights and brake connections that fail an inspection. We fix them on the truck side."),
              ("Season peaks","Spring and fall are packed. Priority service keeps crews moving.")]),
  dict(slug="rental-cars", name="Car rental", plural="car rental locations",
       h1='A parked car <em>earns $0.</em>',
       sub="Every day a car sits in a shop, it isn't on rent. Fast mechanical and collision turnaround for rental fleets.",
       vehicles="cars, SUVs, minivans and passenger vans",
       pains=[("Collision turnaround","Body, paint and frame in-house, so a damaged car is back on rent sooner."),
              ("Between-rental fixes","Brakes, tires, warning lights and alignment, with priority so the car is ready for the next rental."),
              ("Buying more cars?","Pre-purchase inspections before you add a vehicle to the fleet.")]),
  dict(slug="property-management", name="Property management", plural="property management companies",
       h1='Maintenance techs <em>need wheels.</em>',
       sub="Work orders pile up when a maintenance truck is down. We keep property management vehicles on the road.",
       vehicles="pickups, vans and small trucks",
       pains=[("No surprise bills","Nothing over your approval limit without your OK, and every repair itemized by vehicle."),
              ("Multiple properties, one shop","One contact and one monthly invoice for every vehicle you run."),
              ("Easy drop-off","Free pickup and drop-off, plus an after-hours key drop.")]),
  dict(slug="delivery", name="Delivery & courier", plural="delivery and courier companies",
       h1='Every hour parked is <em>a missed delivery.</em>',
       sub="High-mileage delivery vans need fast, reliable service. We get them back on route first.",
       vehicles="cargo vans, sprinter-style vans and cars",
       pains=[("Miles add up fast","Brakes, tires, fluids and suspension wear out on delivery routes. Inspections catch it early."),
              ("Back on route first","Fleet vehicles go to the front of the line, with free diagnostics."),
              ("Dock and parking dings","Body and paint repair in-house, so vans look professional.")]),
]

def esc(t): return html.escape(t, quote=True)

def head(title, desc, path, extra="", noindex=False):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="icon" href="{FAVICON}">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{SITE}{path}">'}
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Public+Sans:wght@400;500;600;800&display=swap">
<link rel="stylesheet" href="/styles.css">
{extra}</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/">MPB <span>FLEET</span> SERVICES</a>
    <nav class="nav" aria-label="Site">
      <a href="/#services">Services</a>
      <a href="/#benefits">Fleet benefits</a>
      <a href="/#who">Industries</a>
      <a href="/credit-application/">Net 30</a>
      <a href="/#request">Free inspection</a>
    </nav>
    <a class="btn red" href="tel:{TEL}">Call<span class="num">&nbsp;{PHONE}</span></a>
  </div>
</header>
'''

def footer():
    links = "".join(f'<a href="/{i["slug"]}/">{esc(i["name"])}</a>' for i in INDUSTRIES)
    return f'''<footer>
  <div class="wrap" style="flex-direction:column;gap:14px">
    <div class="flinks"><b style="color:#fff">Fleet service for:</b>{links}<a href="/credit-application/">Net 30 application</a></div>
    <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap">
      <span>© 2026 MPB Auto Repair and Body Collision · 11432 Elks Cir, Ste B, Rancho Cordova, CA 95742 · {PHONE}</span>
      <span>Fleet terms per the MPB Fleet Service Agreement. Credit subject to approval. BAR ARD 308450.</span>
    </div>
  </div>
</footer>
</body>
</html>
'''

def inspection_form(industry=""):
    hid = f'<input type="hidden" name="Industry" value="{esc(industry)}">' if industry else ""
    subj = f"New fleet inspection request ({industry}) · mpbfleet.com" if industry else "New fleet inspection request · mpbfleet.com"
    return f'''<form class="card" action="{FORM}" method="POST">
        <input type="hidden" name="_subject" value="{esc(subj)}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="{SITE}/thanks.html">
        {hid}
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <label class="full">Business name<input name="Business" required autocomplete="organization"></label>
        <label>Your name<input name="Name" required autocomplete="name"></label>
        <label>Phone<input name="Phone" type="tel" required autocomplete="tel" inputmode="tel"></label>
        <label class="full">Email<input name="email" type="email" autocomplete="email"></label>
        <label>How many vehicles?
          <select name="Fleet size" required>
            <option value="">Choose</option><option>1–2</option><option>3–5</option><option>6–10</option><option>11–25</option><option>26+</option>
          </select>
        </label>
        <label>Best time to reach you
          <select name="Best time"><option>Any time</option><option>Morning</option><option>Afternoon</option></select>
        </label>
        <label class="full">Anything we should know? <small>Vehicle types, current issues, a vehicle you're thinking of buying</small><textarea name="Notes"></textarea></label>
        <div class="full"><button class="btn red" type="submit">Request my free inspection</button></div>
        <p class="note full">Goes straight to our fleet desk. We don't share your information.</p>
      </form>'''

def industry_page(i):
    path = f"/{i['slug']}/"
    title = f"{i['name']} Fleet Repair in Rancho Cordova · MPB Fleet Services"
    desc = (f"Priority fleet repair for {i['plural']} in Rancho Cordova and Sacramento: {i['vehicles']}. "
            "Free fleet inspection, free pickup and drop-off, Net 30 billing.")
    ld = {"@context":"https://schema.org","@type":"Service","name":f"{i['name']} fleet repair and maintenance",
          "serviceType":"Fleet vehicle repair","areaServed":"Rancho Cordova and Sacramento, CA",
          "provider":{"@type":"AutoRepair","name":"MPB Fleet Services","telephone":"+1-916-533-1695",
                      "address":{"@type":"PostalAddress","streetAddress":"11432 Elks Cir, Ste B","addressLocality":"Rancho Cordova","addressRegion":"CA","postalCode":"95742"}}}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    pains = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a,b in i["pains"])
    others = "".join(f'<a href="/{o["slug"]}/">{esc(o["name"])}</a>' for o in INDUSTRIES if o is not i)
    return head(title, desc, path, extra) + f'''
<main id="top">
  <div class="hero">
    <div class="wrap">
      <div>
        <div class="crumbs"><a href="/">MPB Fleet Services</a> · {esc(i['name'])} fleets</div>
        <div class="eyebrow" style="color:#bdbdbd">Fleet service for {esc(i['plural'])} · Rancho Cordova</div>
        <h1 style="margin-top:14px;font-size:clamp(2.4rem,7.5vw,5.2rem)">{i['h1']}</h1>
        <p>{esc(i['sub'])}</p>
        <div class="cta">
          <a class="btn red" href="#request">Book a free fleet inspection</a>
          <a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a>
        </div>
      </div>
      <div class="facts" aria-label="Fleet account at a glance">
        <div><b>Priority</b><span>fleet vehicles go first</span></div>
        <div><b>Free</b><span>pickup &amp; drop-off</span></div>
        <div><b>10% off</b><span>labor on every fleet vehicle</span></div>
        <div><b>Net 30</b><span>billing up to $5,000</span></div>
      </div>
    </div>
  </div>

  <div class="offer">
    <div class="wrap">
      <div class="big">FREE</div>
      <div class="txt"><strong>Inspection of your whole fleet</strong>Every vehicle, a written report on each, plus free diagnostics. No obligation.</div>
      <a class="btn" href="#request">Schedule it</a>
    </div>
  </div>

  <section>
    <div class="wrap">
      <div class="head">
        <div class="eyebrow">Built for {esc(i['plural'])}</div>
        <h2>What we keep running</h2>
        <p>We work on {esc(i['vehicles'])}: maintenance, mechanical, electrical, tires, collision and paint, all in one 12,000 sq ft shop.</p>
      </div>
      <div class="pains">{pains}</div>
    </div>
  </section>

  <section class="benefits">
    <div class="wrap">
      <div class="head"><div class="eyebrow">Every fleet account gets</div><h2>One shop. One contact. One invoice.</h2></div>
      <div class="ben">
        <div><h3>Priority service</h3><p>Fleet vehicles go to the front of the line.</p></div>
        <div><h3>Free pickup &amp; drop-off</h3><p>We pick up your vehicle and bring it back.</p></div>
        <div><h3>10% off labor</h3><p>Mechanical, electrical, paint, body and frame.</p></div>
        <div><h3>Free diagnostics</h3><p>Standard diagnostics at no charge.</p></div>
        <div><h3>Approve by text</h3><p>A digital estimate before any work.</p></div>
        <div><h3>After-hours key drop</h3><p>Drop off at night; we start first thing.</p></div>
        <div><h3>2 free tows a month</h3><p>Light-duty, within 25 miles, business hours.</p></div>
        <div><h3>1-year / 12K warranty</h3><p>On our labor and new parts.</p></div>
      </div>
    </div>
  </section>

  <section class="credit">
    <div class="wrap">
      <div>
        <div class="eyebrow" style="color:#bdbdbd">MPB partners with your business</div>
        <h2 style="margin-top:12px">Net 30 · <span>up to $5,000</span></h2>
      </div>
      <div>
        <p>Fix it now, pay in 30 days. One monthly invoice, itemized by vehicle.</p>
        <p style="margin-top:16px"><a class="btn red" href="/credit-application/">Apply for Net 30</a></p>
      </div>
    </div>
  </section>

  <section id="request" class="request">
    <div class="wrap">
      <div>
        <div class="head" style="margin-bottom:0">
          <div class="eyebrow">Free fleet inspection</div>
          <h2>Request your inspection</h2>
          <p>Tell us about your fleet and we'll call you within one business day to set a time. No obligation.</p>
        </div>
        <ul>
          <li>Every vehicle inspected, no limit</li>
          <li>A written report on each vehicle</li>
          <li>Free diagnostics included</li>
          <li>We can come pick the vehicles up</li>
        </ul>
        <p style="margin:22px 0 0;color:var(--muted)">Rather talk? Call or text <a href="tel:{TEL}"><b>{PHONE}</b></a>.</p>
      </div>
      {inspection_form(i['name'])}
    </div>
  </section>

  <section class="who">
    <div class="wrap">
      <div class="head"><div class="eyebrow">We also work with</div><h2>Other local fleets</h2></div>
      <div class="tags">{others}</div>
    </div>
  </section>
</main>
''' + footer()

def credit_page():
    path = "/credit-application/"
    title = "Net 30 Fleet Credit Application · MPB Fleet Services"
    desc = "Apply for Net 30 fleet billing up to $5,000 at MPB Auto Repair & Body Collision in Rancho Cordova. One monthly invoice for your whole fleet."
    return head(title, desc, path) + f'''
<main id="top">
  <div class="hero">
    <div class="wrap" style="grid-template-columns:1fr">
      <div>
        <div class="crumbs"><a href="/">MPB Fleet Services</a> · Net 30 application</div>
        <h1 style="font-size:clamp(2.4rem,7.5vw,5rem)">Net 30 · <em>up to $5,000</em></h1>
        <p style="max-width:52ch">Fix it now, pay in 30 days. Fill this out in about 5 minutes. We'll review it and call you, usually within two business days.</p>
      </div>
    </div>
  </div>

  <section class="request">
    <div class="wrap narrow" style="grid-template-columns:1fr">
      <form class="card" action="{FORM}" method="POST">
        <input type="hidden" name="_subject" value="NET 30 CREDIT APPLICATION · mpbfleet.com">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="{SITE}/application-received.html">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

        <fieldset><legend>Business</legend>
          <label class="full">Legal business name<input name="Legal business name" required autocomplete="organization"></label>
          <label class="full">DBA (if different)<input name="DBA"></label>
          <label class="full">Street address<input name="Street address" required autocomplete="street-address"></label>
          <label>City<input name="City" required autocomplete="address-level2"></label>
          <label>ZIP<input name="ZIP" required inputmode="numeric" autocomplete="postal-code"></label>
          <label>Business type
            <select name="Business type" required><option value="">Choose</option><option>Corporation</option><option>LLC</option><option>Partnership</option><option>Sole proprietor</option><option>Other</option></select>
          </label>
          <label>Years in business
            <select name="Years in business" required><option value="">Choose</option><option>Less than 1</option><option>1–2</option><option>3–5</option><option>6–10</option><option>More than 10</option></select>
          </label>
          <label>Industry<input name="Industry" placeholder="HVAC, plumbing, rental…"></label>
          <label>Business phone<input name="Business phone" type="tel" required inputmode="tel"></label>
        </fieldset>

        <fieldset><legend>Contacts</legend>
          <label>Owner / officer name<input name="Owner name" required></label>
          <label>Title<input name="Owner title"></label>
          <label>Fleet contact name<input name="Fleet contact" required autocomplete="name"></label>
          <label>Fleet contact phone<input name="Fleet contact phone" type="tel" required inputmode="tel" autocomplete="tel"></label>
          <label class="full">Email<input name="email" type="email" required autocomplete="email"></label>
          <label>Accounts payable contact<input name="AP contact"></label>
          <label>AP email<input name="AP email" type="email"></label>
        </fieldset>

        <fieldset><legend>Fleet &amp; credit</legend>
          <label>Number of vehicles
            <select name="Fleet size" required><option value="">Choose</option><option>1–2</option><option>3–5</option><option>6–10</option><option>11–25</option><option>26+</option></select>
          </label>
          <label>Expected monthly repair spend
            <select name="Expected monthly spend"><option value="">Choose</option><option>Under $500</option><option>$500–$1,500</option><option>$1,500–$3,000</option><option>$3,000–$5,000</option><option>Over $5,000</option></select>
          </label>
          <label>Credit amount requested
            <select name="Credit requested" required><option value="">Choose</option><option>$1,000</option><option>$2,500</option><option>$5,000</option></select>
          </label>
          <label>Purchase order required?
            <select name="PO required"><option>No</option><option>Yes</option></select>
          </label>
          <label>Bank name<input name="Bank name"></label>
          <label>Bank city / branch<input name="Bank branch"></label>
          <p class="note full">Please don't type account numbers here. We'll ask for anything else we need by phone.</p>
        </fieldset>

        <fieldset><legend>Trade references</legend>
          <label>Reference 1 · company<input name="Ref 1 company"></label>
          <label>Reference 1 · phone<input name="Ref 1 phone" type="tel" inputmode="tel"></label>
          <label>Reference 2 · company<input name="Ref 2 company"></label>
          <label>Reference 2 · phone<input name="Ref 2 phone" type="tel" inputmode="tel"></label>
        </fieldset>

        <fieldset><legend>Agreement</legend>
          <label class="full check"><input type="checkbox" name="Agrees to terms" value="Yes" required><span>I'm authorized to apply for credit for this business. I agree that approved invoices are due within 30 days, and that MPB may contact the references and bank listed to verify this application. Final terms are set in the MPB Fleet Service Agreement.</span></label>
          <label>Your full name (signature)<input name="Signature" required autocomplete="name"></label>
          <label>Title<input name="Signer title" required></label>
        </fieldset>

        <div class="full"><button class="btn red" type="submit">Submit application</button></div>
        <p class="note full">Goes straight to our fleet desk. Approval isn't automatic; the credit amount is set after review.</p>
      </form>
    </div>
  </section>
</main>
''' + footer()

def simple_page(fname, title, h, p, extra_btn=""):
    return head(title, title, "/"+fname, noindex=True) + f'''
<main><div class="hero"><div class="wrap" style="grid-template-columns:1fr;min-height:60vh;align-content:center">
<div><h1>{h}</h1><p style="max-width:44ch">{p}</p><div class="cta"><a class="btn red" href="/">Back to mpbfleet.com</a>{extra_btn}</div></div>
</div></div></main>
''' + footer()

def main():
    for i in INDUSTRIES:
        os.makedirs(i["slug"], exist_ok=True)
        open(f'{i["slug"]}/index.html', "w").write(industry_page(i))
    os.makedirs("credit-application", exist_ok=True)
    open("credit-application/index.html", "w").write(credit_page())
    call = f'<a class="btn ghost" href="tel:{TEL}">Call now</a>'
    open("thanks.html","w").write(simple_page("thanks.html","Request received · MPB Fleet Services","Got it. <em>Thanks.</em>",
        f"Your inspection request is in. We'll call you within one business day to set a time. Need us sooner? Call or text {PHONE}.", call))
    open("application-received.html","w").write(simple_page("application-received.html","Application received · MPB Fleet Services","Application <em>received.</em>",
        f"Thanks for applying for Net 30. We'll review it and call you, usually within two business days. Questions? Call or text {PHONE}.", call))
    open("404.html","w").write(simple_page("404.html","Page not found · MPB Fleet Services","Wrong <em>turn.</em>",
        "That page doesn't exist. Head back to the homepage or give us a call.", call))
    urls = ["/", "/credit-application/"] + [f'/{i["slug"]}/' for i in INDUSTRIES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-06</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open("sitemap.xml","w").write(sm)
    print("built", len(urls), "indexed pages")

if __name__ == "__main__":
    main()
