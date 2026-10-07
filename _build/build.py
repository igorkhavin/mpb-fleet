"""Builds every page of mpbfleet.com. Run from the repo root:  python3 _build/build.py
(Folders starting with _ are not published by GitHub Pages.)"""
import json, os, html

SITE = "https://mpbfleet.com"
PHONE, TEL = "(916) 533-1695", "+19165331695"
EMAIL = "mpbfleet@gmail.com"
FORM = f"https://formsubmit.co/{EMAIL}"
ADDR1, ADDR2 = "11432 Elks Cir, Ste B", "Rancho Cordova, CA 95742"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23c8102e'/%3E"
           "%3Ctext x='32' y='42' font-family='Arial' font-weight='800' font-size='24' fill='white' text-anchor='middle'%3EMPB%3C/text%3E%3C/svg%3E")

I = {  # small inline icons
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "text": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.3-1.3a4 4 0 0 1-5-5L14 2l-2.5 2.5 3.2 1.8z"/><path d="M3 21l6-6"/></svg>',
 "person": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
 "van": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 16V7a1 1 0 0 1 1-1h11l4 4h3a1 1 0 0 1 1 1v5h-2"/><path d="M14 6v4h4"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/></svg>',
 "go": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
}

INDUSTRIES = [
  dict(slug="hvac", name="HVAC", plural="HVAC companies", unit=("Van 03","Ford Transit with ladder rack","AC season"),
       h1="No van, no service call.",
       sub="When a service van is down in July, the calls don't stop. We get HVAC vans and pickups back on the road first.",
       vehicles="service vans, box vans and pickups with ladder racks",
       pains=[("Summer can't wait","When it's 105° out, a van in the shop costs you jobs every hour. Fleet vehicles go to the front of our line."),
              ("Heavy loads, hard brakes","Vans carrying condensers and tools wear brakes, suspension and tires fast. We catch it at the inspection."),
              ("Racks and dings","Ladder racks, side scrapes and backing damage. Body and paint are done in the same building as the mechanical work.")]),
  dict(slug="plumbing", name="Plumbing", plural="plumbing companies", unit=("Van 11","Ram ProMaster service van","Emergency calls"),
       h1="A plumber without a van is a missed call.",
       sub="Emergency calls go to whoever shows up first. We keep plumbing vans ready to roll.",
       vehicles="service vans, box trucks and pickups",
       pains=[("Emergency-ready","Drop keys after hours and we start first thing, so the van is back before the next emergency."),
              ("Weight and wear","Pipe, jetters and water heaters are heavy. We keep brakes, suspension and tires in spec."),
              ("One invoice","Every van's repairs on one monthly statement, on Net 30 terms up to $5,000.")]),
  dict(slug="electrical", name="Electrical", plural="electrical contractors", unit=("Truck 05","Ford F-250 utility body","Crew on standby"),
       h1="Your electricians bill by the hour. Your van shouldn't cost them hours.",
       sub="Priority repair for electrical contractor fleets in Rancho Cordova and Sacramento.",
       vehicles="service vans, pickups with racks and utility bodies",
       pains=[("Crew downtime","A van in the shop means a crew standing around. Priority service gets them back on the job."),
              ("Charging and starting","Inverters, lights and tools drain batteries and charging systems. Free diagnostics find it fast."),
              ("Approve by text","You get a digital estimate before any work and approve it from your phone.")]),
  dict(slug="pest-control", name="Pest control", plural="pest control companies", unit=("Truck 02","Toyota Tacoma with spray rig","Route day"),
       h1="Routes don't wait.",
       sub="Missed stops mean unhappy customers. We keep pest control trucks running their routes.",
       vehicles="pickups, small trucks and vans",
       pains=[("Route-day reliability","Free pickup and drop-off, so a tech doesn't lose a route day driving to the shop."),
              ("High mileage","Stop-and-go routes are hard on brakes, transmissions and cooling. We stay ahead of it."),
              ("Clean, professional trucks","Dings and faded paint make a bad first impression. Body and paint, in-house.")]),
  dict(slug="landscaping", name="Landscaping", plural="landscaping companies", unit=("Truck 09","Chevy Silverado 2500, tows a trailer","Peak season"),
       h1="Trucks that pull all day.",
       sub="Landscape trucks tow trailers and haul heavy loads. We keep them working through the season.",
       vehicles="pickups and light-duty trucks that tow trailers",
       pains=[("Towing wear","Trailer loads work transmissions, brakes and cooling hard. We inspect what towing wears out."),
              ("Trailer wiring","Lights and brake connections that fail an inspection. We fix them on the truck side."),
              ("Season peaks","Spring and fall are packed. Priority service keeps crews moving.")]),
  dict(slug="rental-cars", name="Car rental", plural="car rental locations", unit=("Car 21","Toyota Camry, rear bumper damage","Booked Friday"),
       h1="A parked car earns $0.",
       sub="Every day a car sits in a shop, it isn't on rent. Fast mechanical and collision turnaround for rental fleets.",
       vehicles="cars, SUVs, minivans and passenger vans",
       pains=[("Collision turnaround","Body, paint and frame in-house, so a damaged car is back on rent sooner."),
              ("Between-rental fixes","Brakes, tires, warning lights and alignment, with priority so the car is ready for the next rental."),
              ("Buying more cars?","Pre-purchase inspections before you add a vehicle to the fleet.")]),
  dict(slug="property-management", name="Property management", plural="property management companies", unit=("Truck 04","Ford F-150 maintenance truck","Work orders waiting"),
       h1="Maintenance techs need wheels.",
       sub="Work orders pile up when a maintenance truck is down. We keep property management vehicles on the road.",
       vehicles="pickups, vans and small trucks",
       pains=[("No surprise bills","Nothing over your approval limit without your OK, and every repair itemized by vehicle."),
              ("Multiple properties, one shop","One contact and one monthly invoice for every vehicle you run."),
              ("Easy drop-off","Free pickup and drop-off, plus an after-hours key drop.")]),
  dict(slug="delivery", name="Delivery & courier", plural="delivery and courier companies", unit=("Van 14","Mercedes Sprinter cargo van","Route at 6 AM"),
       h1="Every hour parked is a missed delivery.",
       sub="High-mileage delivery vans need fast, reliable service. We get them back on route first.",
       vehicles="cargo vans, Sprinter-style vans and cars",
       pains=[("Miles add up fast","Brakes, tires, fluids and suspension wear out on delivery routes. Inspections catch it early."),
              ("Back on route first","Fleet vehicles go to the front of the line, with free diagnostics."),
              ("Dock and parking dings","Body and paint repair in-house, so vans look professional.")]),
]

BENEFITS = [("Priority service","Fleet vehicles go to the front of the line."),
            ("Free pickup & drop-off","We pick up your vehicle and bring it back when it's done."),
            ("10% off labor","Mechanical, electrical, paint, body and frame. Also 10% off alignments and tire mount & balance."),
            ("Free diagnostics","Standard diagnostics at no charge on every fleet vehicle."),
            ("Approve by text","A digital estimate before any work, with a pre-approval limit you set."),
            ("After-hours key drop","Drop off after hours; we start first thing in the morning."),
            ("2 free tows a month","Light-duty, within 25 miles, to MPB, during business hours."),
            ("1-year / 12K warranty","On our labor and new parts, mechanical and collision.")]

def esc(t): return html.escape(t, quote=True)

def head(title, desc, path, extra="", noindex=False):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{FAVICON}">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{SITE}{path}">'}
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap">
<link rel="stylesheet" href="/styles.css">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="MPB Fleet Services home"><span class="mark">MPB</span><span><b>MPB Fleet Services</b><small>MPB Auto Repair &amp; Body Collision</small></span></a>
    <nav class="nav" aria-label="Site">
      <a href="/#services">Services</a>
      <a href="/#benefits">Benefits</a>
      <a href="/#who">Industries</a>
      <a href="/credit-application/">Net 30</a>
      <a href="/#area">Service area</a>
    </nav>
    <div class="cta"><a class="btn line call" href="tel:{TEL}">{PHONE}</a><a class="btn red" href="/#request">Free inspection</a></div>
  </div>
</header>
'''

def footer():
    links = "".join(f'<a href="/{i["slug"]}/">{esc(i["name"])}</a>' for i in INDUSTRIES)
    return f'''<footer>
  <div class="wrap">
    <div class="flinks"><b>Fleet service for</b>{links}<a href="/credit-application/">Net 30 application</a></div>
    <div class="fine">
      <span>© 2026 MPB Auto Repair and Body Collision, {ADDR1}, {ADDR2}. {PHONE}</span>
      <span>Fleet terms per the MPB Fleet Service Agreement. Credit subject to approval. BAR ARD 308450.</span>
    </div>
  </div>
</footer>
<nav class="bar" aria-label="Quick contact">
  <a class="btn line" href="tel:{TEL}">{I["phone"]}Call</a>
  <a class="btn line" href="sms:{TEL}">{I["text"]}Text</a>
  <a class="btn red" href="/#request">Free inspection</a>
</nav>
<script>
(function(){{var b=document.querySelector('.board');if(!b)return;var li=[].slice.call(b.querySelectorAll('li'));
if(matchMedia('(prefers-reduced-motion: reduce)').matches){{li.forEach(function(l){{l.classList.add('on')}});return}}
li.forEach(function(l,i){{setTimeout(function(){{l.classList.add('on')}},350+i*420)}})}})();
</script>
</body>
</html>
'''

def board(unit, model, note):
    steps = [("done","Picked up at your yard","Free pickup, so no driver loses the morning","7:30 AM"),
             ("done","Inspected, estimate texted","Every line item, before any work starts","9:05 AM"),
             ("done","Approved by text","Under your pre-approval limit, we just start","9:12 AM"),
             ("now","In a priority bay","Fleet vehicles go to the front of the line","9:30 AM"),
             ("","Back at your yard","One line on your monthly Net 30 invoice","2:45 PM")]
    rows = "".join(f'<li class="{c}"><span class="dot">{I["check"].replace("currentColor","#fff")}</span><span><strong>{a}</strong><small>{b}</small></span><time>{t}</time></li>' for c,a,b,t in steps)
    return f'''<div>
        <div class="board" role="img" aria-label="Example: how a fleet vehicle moves through MPB in one day, from pickup at 7:30 AM to back at your yard at 2:45 PM.">
          <header><div><b>{esc(unit)}</b><span>{esc(model)}</span></div><span class="plate">{esc(note)}</span></header>
          <ol>{rows}</ol>
          <footer>Back on the road the same day <span>Brake job example</span></footer>
        </div>
        <p class="board-note">Example of a routine brake job. Bigger repairs take longer; you always see the estimate first.</p>
      </div>'''

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
        <label>How many vehicles?
          <select name="Fleet size" required>
            <option value="">Choose</option><option>1–2</option><option>3–5</option><option>6–10</option><option>11–25</option><option>26+</option>
          </select>
        </label>
        <label>What kind?
          <select name="Vehicle types">
            <option>Vans</option><option>Pickups</option><option>Cars / SUVs</option><option>A mix</option>
          </select>
        </label>
        <label class="full">Business name<input name="Business" required autocomplete="organization"></label>
        <label>Your name<input name="Name" required autocomplete="name"></label>
        <label>Phone<input name="Phone" type="tel" required autocomplete="tel" inputmode="tel"></label>
        <label class="full">Email <small>Optional</small><input name="email" type="email" autocomplete="email"></label>
        <label class="full">Anything we should know? <small>Optional: current issues, or a vehicle you're thinking of buying</small><textarea name="Notes"></textarea></label>
        <div class="full"><button class="btn red" type="submit">Request my free inspection</button></div>
        <p class="note full">We'll call within one business day to set a time. Your information stays with MPB.</p>
      </form>'''

def request_section(industry=""):
    pts = ["Every vehicle inspected, no limit","A written report on each vehicle","Free diagnostics included","We can pick the vehicles up"]
    li = "".join(f'<li>{I["check"]}{p}</li>' for p in pts)
    return f'''<section id="request" class="request">
    <div class="wrap">
      <div>
        <div class="head" style="margin-bottom:0">
          <p class="kicker">Free fleet inspection</p>
          <h2>See where your fleet stands.</h2>
          <p>Tell us a little about your vehicles. We'll call within one business day to set a time. No obligation.</p>
        </div>
        <ul>{li}</ul>
        <p style="margin-top:28px;color:var(--steel)">Rather talk? Call or text <a href="tel:{TEL}"><b>{PHONE}</b></a> and ask for Igor.</p>
      </div>
      {inspection_form(industry)}
    </div>
  </section>'''

def offer_section():
    pts = ["Every vehicle in your fleet, no limit","A written report on each one","Free diagnostics on anything we find","No obligation to book a repair"]
    li = "".join(f'<li>{I["check"]}{p}</li>' for p in pts)
    return f'''<div class="offer">
    <div class="wrap">
      <div>
        <h2>Free inspection of your whole fleet.</h2>
        <p>Find out which vehicles need attention before they break down on a job. We can pick them up, too.</p>
        <a class="btn white" href="#request">Book the free inspection</a>
      </div>
      <ul>{li}</ul>
    </div>
  </div>'''

def benefits_section():
    cells = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a,b in BENEFITS)
    return f'''<section id="benefits" class="benefits">
    <div class="wrap">
      <div class="head"><p class="kicker">Every fleet account gets</p><h2>Built for businesses that run on wheels.</h2></div>
      <div class="ben">{cells}</div>
    </div>
  </section>'''

def credit_section():
    pts = ["One monthly invoice, itemized by vehicle","Nothing over your approval limit without your OK","Simple application, reviewed by the owner"]
    li = "".join(f'<li>{I["check"]}{p}</li>' for p in pts)
    return f'''<section class="credit">
    <div class="wrap">
      <div>
        <p class="kicker">MPB partners with your business</p>
        <h2>Fix it now. Pay in 30 days.</h2>
        <ul>{li}</ul>
        <div class="cta"><a class="btn red" href="/credit-application/">Apply for Net 30</a><a class="btn ghost" href="tel:{TEL}">Ask about terms</a></div>
      </div>
      <div class="terms"><span>Net 30 billing</span><div class="big">Up to $5,000</div><span>for approved fleet accounts</span></div>
    </div>
  </section>'''

def industries_section(exclude=None, title="Local fleets of every size.", kicker="Who we work with"):
    cards = "".join(f'<a href="/{i["slug"]}/">{esc(i["name"])}{I["go"]}</a>' for i in INDUSTRIES if i is not exclude)
    return f'''<section id="who" class="who">
    <div class="wrap">
      <div class="head"><p class="kicker">{kicker}</p><h2>{title}</h2><p>From two service vans to dozens of rental cars. No minimum fleet size.</p></div>
      <div class="inds">{cards}</div>
      <p class="also">Also roofing and solar, garage doors, security patrol, contractors, driving schools and home health.</p>
    </div>
  </section>'''

LD_BUSINESS = {"@context":"https://schema.org","@type":"AutoRepair","name":"MPB Fleet Services","alternateName":"MPB Auto Repair and Body Collision",
  "url":SITE+"/","telephone":"+1-916-533-1695","email":EMAIL,
  "address":{"@type":"PostalAddress","streetAddress":ADDR1,"addressLocality":"Rancho Cordova","addressRegion":"CA","postalCode":"95742","addressCountry":"US"},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"18:00"}],
  "areaServed":["Rancho Cordova","Gold River","Mather","Sacramento","Folsom","Citrus Heights","Fair Oaks","Carmichael","Elk Grove","El Dorado Hills"],
  "sameAs":["https://mpbautorepair.com"]}

FAQS = [("Is there a limit on how many vehicles you'll inspect for free?","No. We'll inspect every vehicle in your fleet and give you a written report on each one."),
        ("What kinds of vehicles do you service?","Cars, vans, pickups and light-duty work trucks. We don't service heavy commercial trucks, so your van never waits behind a semi."),
        ("How does billing work?","Approved fleet accounts get Net 30 terms with up to $5,000 in credit and one monthly invoice. You can also pay per visit."),
        ("Will you do work without asking me first?","No. Every repair starts with a digital estimate. You approve by text or email, and you can set a pre-approval limit so small jobs don't wait on a call."),
        ("We already have a shop. Why switch?","You don't have to switch everything. Many fleets use us for overflow, body work, or when their main shop is backed up. The free inspection is a no-risk way to see how we work."),
        ("What if a vehicle breaks down after hours?","Use our after-hours key drop and we'll start first thing. Emergency and after-hours towing is available and billed separately.")]

def home():
    title = "MPB Fleet Services · Fleet Repair in Rancho Cordova, CA"
    desc = "Fleet maintenance, mechanical, tires, collision and paint for local businesses in Rancho Cordova and Sacramento. Free fleet inspection, priority service, free pickup and Net 30 billing."
    extra = f'<script type="application/ld+json">{json.dumps(LD_BUSINESS)}</script>\n'
    services = [("Maintenance","Oil, fluids, filters, brakes and scheduled service"),
                ("Mechanical & electrical","Engine, transmission, cooling, starting, charging, diagnostics"),
                ("Tires & alignment","Mount, balance and alignment, 10% off for fleets"),
                ("Collision & paint","Body repair, paint and frame straightening in-house"),
                ("Towing","Two free tows a month during business hours"),
                ("Pre-purchase inspections","Check a vehicle before you add it to the fleet")]
    svc = "".join(f'<div><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in services)
    faq = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in FAQS)
    return head(title, desc, "/", extra) + f'''
<main id="top">
  <div class="hero">
    <div class="wrap">
      <div>
        <p class="crumbs">Fleet service from MPB Auto Repair &amp; Body Collision, Rancho Cordova</p>
        <h1>A parked van makes $0.</h1>
        <p class="lede">Every day a work vehicle waits at the shop, your crew loses jobs. Fleet vehicles go to the front of our line, with mechanical and body work under one roof.</p>
        <div class="cta">
          <a class="btn red" href="#request">Request a free fleet inspection</a>
          <a class="btn line" href="tel:{TEL}">{I["phone"]}{PHONE}</a>
        </div>
      </div>
      {board("Van 07","Ford Transit 250 service van","Fleet")}
    </div>
  </div>
  <div class="wrap facts">
    <span><b>12 lifts</b> in a 12,000 sq ft shop</span>
    <span><b>Mechanical, body &amp; paint</b> under one roof</span>
    <span><b>Light-duty only</b>: cars, vans, pickups</span>
    <span><b>BAR licensed</b> ARD 308450</span>
  </div>

  {offer_section()}

  <section>
    <div class="wrap">
      <div class="head"><p class="kicker">Why fleets switch to MPB</p><h2>One shop that does the whole job.</h2></div>
      <div class="why">
        <article><span class="icon">{I["wrench"]}</span><h3>Mechanical and body in one building</h3><p>Brakes, engine work and that dented side panel get fixed in the same visit. Most fleet shops around Sacramento do one or the other.</p></article>
        <article><span class="icon">{I["person"]}</span><h3>You talk to the owner</h3><p>Call or text the fleet line and you reach Igor, not a call center. Questions get answered the same day.</p></article>
        <article><span class="icon">{I["van"]}</span><h3>Built for vans and pickups</h3><p>We're light-duty only. Your service van never waits in line behind a semi.</p></article>
      </div>
    </div>
  </section>

  <section id="services" style="padding-top:0">
    <div class="wrap">
      <div class="head"><p class="kicker">Services</p><h2>Everything your vehicles need.</h2><p>Cars, vans, pickups and light-duty work trucks. No more sending a vehicle to three different shops.</p></div>
      <div class="svc">{svc}</div>
    </div>
  </section>

  {benefits_section()}

  {credit_section()}

  <section id="how">
    <div class="wrap">
      <div class="head"><p class="kicker">How it works</p><h2>From down to back on the road.</h2></div>
      <ol class="steps">
        <li><h3>Free inspection</h3><p>We inspect your whole fleet and give you a written report on every vehicle.</p></li>
        <li><h3>Estimate by text</h3><p>When something needs work, you get a digital estimate to approve from your phone.</p></li>
        <li><h3>Priority repair</h3><p>Your vehicle moves to the front of the line. Mechanical and body work in one place.</p></li>
        <li><h3>Back to work</h3><p>We return it or you pick it up. One monthly invoice on Net 30.</p></li>
      </ol>
    </div>
  </section>

  {industries_section()}

  <section id="area" class="area">
    <div class="wrap">
      <div>
        <div class="head" style="margin-bottom:0">
          <p class="kicker">Service area</p>
          <h2>Based in Rancho Cordova.</h2>
          <p>Right off Sunrise Blvd and Highway 50. Fleet accounts get free pickup and drop-off across our local service area.</p>
        </div>
        <ul class="cities"><li>Rancho Cordova</li><li>Gold River</li><li>Mather</li><li>Sacramento</li><li>Folsom</li><li>Citrus Heights</li><li>Fair Oaks</li><li>Carmichael</li><li>Elk Grove</li><li>El Dorado Hills</li></ul>
        <a class="btn dark" href="https://www.google.com/maps/dir/?api=1&amp;destination=11432+Elks+Cir+Ste+B+Rancho+Cordova+CA+95742">Get directions</a>
      </div>
      <div class="map"><iframe title="Map to MPB at 11432 Elks Cir, Rancho Cordova" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=11432%20Elks%20Cir%20Ste%20B%2C%20Rancho%20Cordova%2C%20CA%2095742&amp;z=13&amp;output=embed"></iframe></div>
    </div>
  </section>

  {request_section()}

  <section id="faq">
    <div class="wrap">
      <div class="head"><p class="kicker">Questions</p><h2>Fleet FAQ.</h2></div>
      <div class="faq">{faq}</div>
    </div>
  </section>

  {contact_section()}
</main>
''' + footer()

def contact_section():
    return f'''<section id="contact" class="contact">
    <div class="wrap">
      <div>
        <p class="kicker" style="color:var(--safety)">Fleet line, call or text</p>
        <a class="phone" href="tel:{TEL}">{PHONE}</a>
        <p>Set up your free inspection or open a fleet account. Ask for Igor.</p>
        <div class="cta"><a class="btn red" href="tel:{TEL}">{I["phone"]}Call now</a><a class="btn ghost" href="sms:{TEL}">{I["text"]}Send a text</a></div>
      </div>
      <dl>
        <dt>Address</dt><dd><a href="https://www.google.com/maps/search/?api=1&amp;query=11432+Elks+Cir+Ste+B+Rancho+Cordova+CA+95742">{ADDR1}<br>{ADDR2}</a></dd>
        <dt>Hours</dt><dd class="hours">Mon–Sat 9 AM–6 PM<br>Sunday closed<br>After-hours key drop</dd>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Main shop</dt><dd><a href="https://mpbautorepair.com">mpbautorepair.com</a></dd>
        <dt>Licensed</dt><dd>Bureau of Automotive Repair ARD 308450</dd>
      </dl>
    </div>
  </section>'''

def industry_page(i):
    path = f"/{i['slug']}/"
    title = f"{i['name']} Fleet Repair in Rancho Cordova · MPB Fleet Services"
    desc = (f"Priority fleet repair for {i['plural']} in Rancho Cordova and Sacramento: {i['vehicles']}. "
            "Free fleet inspection, free pickup and drop-off, Net 30 billing.")
    ld = {"@context":"https://schema.org","@type":"Service","name":f"{i['name']} fleet repair and maintenance",
          "serviceType":"Fleet vehicle repair","areaServed":"Rancho Cordova and Sacramento, CA",
          "provider":{"@type":"AutoRepair","name":"MPB Fleet Services","telephone":"+1-916-533-1695",
                      "address":{"@type":"PostalAddress","streetAddress":ADDR1,"addressLocality":"Rancho Cordova","addressRegion":"CA","postalCode":"95742"}}}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    pains = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a,b in i["pains"])
    u = i["unit"]
    return head(title, desc, path, extra) + f'''
<main id="top">
  <div class="hero">
    <div class="wrap">
      <div>
        <p class="crumbs"><a href="/">MPB Fleet Services</a> / {esc(i['name'])} fleets</p>
        <h1 style="font-size:clamp(2.8rem,8vw,6rem)">{esc(i['h1'])}</h1>
        <p class="lede">{esc(i['sub'])}</p>
        <div class="cta">
          <a class="btn red" href="#request">Request a free fleet inspection</a>
          <a class="btn line" href="tel:{TEL}">{I["phone"]}{PHONE}</a>
        </div>
      </div>
      {board(u[0], u[1], u[2])}
    </div>
  </div>

  <section>
    <div class="wrap">
      <div class="head">
        <p class="kicker">Built for {esc(i['plural'])}</p>
        <h2>What we keep running.</h2>
        <p>We work on {esc(i['vehicles'])}: maintenance, mechanical, electrical, tires, collision and paint, all in one 12,000 sq ft shop.</p>
      </div>
      <div class="pains">{pains}</div>
    </div>
  </section>

  {offer_section()}
  {benefits_section()}
  {credit_section()}
  {request_section(i['name'])}
  {industries_section(exclude=i, title="Other local fleets we keep running.", kicker="We also work with")}
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
        <p class="crumbs"><a href="/">MPB Fleet Services</a> / Net 30 application</p>
        <h1 style="font-size:clamp(2.8rem,8vw,6rem)">Net 30, up to $5,000.</h1>
        <p class="lede" style="max-width:52ch">Fix it now, pay in 30 days. This takes about 5 minutes. We'll review it and call you, usually within two business days.</p>
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
          <label class="full">DBA <small>If different</small><input name="DBA"></label>
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
          <label>Owner or officer name<input name="Owner name" required></label>
          <label>Title<input name="Owner title"></label>
          <label>Fleet contact name<input name="Fleet contact" required autocomplete="name"></label>
          <label>Fleet contact phone<input name="Fleet contact phone" type="tel" required inputmode="tel" autocomplete="tel"></label>
          <label class="full">Email<input name="email" type="email" required autocomplete="email"></label>
          <label>Accounts payable contact<input name="AP contact"></label>
          <label>AP email<input name="AP email" type="email"></label>
        </fieldset>

        <fieldset><legend>Fleet and credit</legend>
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
          <label>Bank city or branch<input name="Bank branch"></label>
          <p class="note full">Please don't type account numbers here. We'll ask for anything else we need by phone.</p>
        </fieldset>

        <fieldset><legend>Trade references</legend>
          <label>Reference 1 company<input name="Ref 1 company"></label>
          <label>Reference 1 phone<input name="Ref 1 phone" type="tel" inputmode="tel"></label>
          <label>Reference 2 company<input name="Ref 2 company"></label>
          <label>Reference 2 phone<input name="Ref 2 phone" type="tel" inputmode="tel"></label>
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

def simple_page(fname, title, h, p):
    return head(title, title, "/"+fname, noindex=True) + f'''
<main class="hero msg"><div class="wrap">
  <h1>{h}</h1>
  <p class="lede" style="max-width:46ch">{p}</p>
  <div class="cta"><a class="btn red" href="/">Back to mpbfleet.com</a><a class="btn line" href="tel:{TEL}">{I["phone"]}Call {PHONE}</a></div>
</div></main>
''' + footer()

def main():
    open("index.html","w").write(home())
    for i in INDUSTRIES:
        os.makedirs(i["slug"], exist_ok=True)
        open(f'{i["slug"]}/index.html', "w").write(industry_page(i))
    os.makedirs("credit-application", exist_ok=True)
    open("credit-application/index.html", "w").write(credit_page())
    open("thanks.html","w").write(simple_page("thanks.html","Request received · MPB Fleet Services","Got it. Thanks.",
        f"Your inspection request is in. We'll call you within one business day to set a time. Need us sooner? Call or text {PHONE}."))
    open("application-received.html","w").write(simple_page("application-received.html","Application received · MPB Fleet Services","Application received.",
        f"Thanks for applying for Net 30. We'll review it and call you, usually within two business days. Questions? Call or text {PHONE}."))
    open("404.html","w").write(simple_page("404.html","Page not found · MPB Fleet Services","Wrong turn.",
        "That page doesn't exist. Head back to the homepage or give us a call."))
    urls = ["/", "/credit-application/"] + [f'/{i["slug"]}/' for i in INDUSTRIES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-07</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open("sitemap.xml","w").write(sm)
    print("built", len(urls), "indexed pages")

if __name__ == "__main__":
    main()
