"""Static site generator for toplevelrenovation.com.
Run from the repo root:  python3 -I tools/build.py
Writes index.html, one .html per page (Cloudflare Pages serves /kitchens from
kitchens.html), projects/*.html, 404.html, _redirects, sitemap.xml, robots.txt."""
import html, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from content import PHONE, TEL, EMAIL, HIC, REVIEWS, TOWNS, PROCESS, GENERAL_FAQ, SERVICES
from projects import PROJECTS

DOMAIN = 'https://www.toplevelrenovation.com'
IMG = json.load(open(os.path.join(ROOT, 'tools', 'image-manifest.json')))
P = {p['slug']: p for p in PROJECTS}
SV = {s['slug']: s for s in SERVICES}
KIND_LABEL = {'kitchen': 'Kitchen', 'bath': 'Bathroom', 'home': 'Whole home', 'exterior': 'Exterior', 'commercial': 'Commercial'}
KIND_PICK = {'kitchen': 'Kitchen', 'bath': 'Bathroom', 'home': 'Whole home', 'exterior': 'Deck / outdoor', 'commercial': 'Commercial'}
e = html.escape
PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'

BUSINESS = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": DOMAIN + "/#business",
  "name": "Top Level Renovation, Inc.", "telephone": "+1-732-538-9379", "email": EMAIL, "url": DOMAIN + "/",
  "image": DOMAIN + "/images/hero-wide.jpg", "logo": DOMAIN + "/images/logo-mark.png",
  "description": "Full-service remodeling company in Monmouth County, NJ: kitchens, bathrooms, whole-home renovations, additions, roofing, siding, decks and commercial work.",
  "address": {"@type": "PostalAddress", "streetAddress": "3411 Rose Ave", "addressLocality": "Ocean Township", "addressRegion": "NJ", "postalCode": "07712", "addressCountry": "US"},
  "areaServed": ["Monmouth County, NJ"] + [t + ", NJ" for t in TOWNS], "openingHours": "Mo-Fr 08:00-17:00",
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "89"},
  "sameAs": ["https://www.instagram.com/toplevelrenovation/"]}


def place(p):
    bits = [b for b in (p.get('town'), p.get('date')) if b]
    return ' · '.join(bits) if bits else 'Monmouth County'


def thumb(slug, n=1):
    return f'/images/p/{slug}/{n:02d}-t.jpg'


# ---------------------------------------------------------------- layout
def nav_links():
    svc = ''.join(f'<a href="/{s["slug"]}">{e(s["nav"])}</a>' for s in SERVICES)
    return f'''<nav class="nav" aria-label="Main">
      <div class="nav__drop"><button type="button" aria-expanded="false" aria-controls="navSvc">Services <span aria-hidden="true">▾</span></button>
        <div class="nav__panel" id="navSvc">{svc}</div></div>
      <a href="/projects">Projects</a>
      <a href="/#reveal">Before &amp; After</a>
      <a href="/reviews">Reviews</a>
      <a href="/about-us">About</a>
      <a href="/contact">Contact</a>
    </nav>'''


def sheet():
    svc = ''.join(f'<a href="/{s["slug"]}" data-close>{e(s["nav"])}</a>' for s in SERVICES)
    return f'''<div class="sheet" id="sheet" hidden>
  <div class="sheet__scrim" data-close></div>
  <nav class="sheet__panel" aria-label="Mobile">
    <div class="sheet__grab" aria-hidden="true"></div>
    <p class="sheet__label">Services</p>
    <div class="sheet__svc">{svc}</div>
    <a href="/projects" data-close><span>01</span>Projects</a>
    <a href="/#reveal" data-close><span>02</span>Before &amp; After</a>
    <a href="/reviews" data-close><span>03</span>Reviews</a>
    <a href="/about-us" data-close><span>04</span>About</a>
    <a href="/contact" data-close><span>05</span>Contact</a>
    <a class="btn btn--gold" href="#estimate" data-close>Get a Free Estimate</a>
    <a class="sheet__call" href="tel:{TEL}">or call {PHONE}</a>
  </nav>
</div>'''


TICKER_ITEMS = ['★ 4.9 on Google · 89 reviews', f'Licensed &amp; insured · NJ HIC #{HIC}', 'One project manager, start to finish', 'BBB Accredited', 'Monmouth County · 15+ years']


def head(title, desc, path, image='/images/hero-wide.jpg', ld=(), preload=None):
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    pre = ''.join(f'<link rel="preload" as="image" href="{h}"{m}>\n' for h, m in (preload or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{DOMAIN}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{DOMAIN}{image}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta name="theme-color" content="#121110">
<link rel="icon" href="/images/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&amp;family=Manrope:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
{pre}<link rel="stylesheet" href="/styles.css">
{lds}</head>'''


def top():
    t = ''.join(f'<span>{x}</span><i aria-hidden="true"></i>' for x in TICKER_ITEMS)
    t2 = ''.join(f'<span aria-hidden="true">{x}</span><i aria-hidden="true"></i>' for x in TICKER_ITEMS)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="ticker" aria-label="Highlights"><div class="ticker__track">{t}{t2}</div></div>
<header class="hdr" id="hdr">
  <div class="hdr__in">
    <a href="/" class="brand" aria-label="Top Level Renovation, home">
      <img src="/images/logo-mark.png" alt="" width="200" height="150">
      <span class="brand__word"><b>Top Level</b><small>Renovation, Inc.</small></span>
    </a>
    {nav_links()}
    <div class="hdr__cta">
      <a class="hdr__phone" href="tel:{TEL}">{PHONE_SVG}{PHONE}</a>
      <a class="btn btn--gold btn--sm" href="#estimate">Free Estimate</a>
      <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="sheet"><span></span><span></span></button>
    </div>
  </div>
</header>
{sheet()}
<main id="main">'''


def estimate(preselect='', heading='Tell us about your project.', sub='Answer three quick questions and we\'ll call you to set up a free in-home consult.'):
    opts = [('Kitchen', 'Kitchen'), ('Bathroom', 'Bathroom'), ('Whole home', 'Whole home'), ('Addition', 'Addition'), ('Roofing / siding', 'Roof / siding'), ('Deck / outdoor', 'Deck / outdoor'), ('Commercial', 'Commercial'), ('Something else', 'Something else')]
    o = ''.join(f'<label><input type="radio" name="project" value="{e(v)}"><span>{e(l)}</span></label>' for v, l in opts)
    pre = f' data-preselect="{e(preselect)}"' if preselect else ''
    return f'''<section class="estimate" id="estimate">
  <div class="wrap est__grid">
    <div class="est__copy" data-reveal>
      <p class="eyebrow eyebrow--light">Free estimate</p>
      <h2>{heading} <span class="gold">60 seconds.</span></h2>
      <p class="lede">{sub}</p>
      <ul class="est__list"><li>No-pressure, in-home consultation</li><li>Clear written proposal</li><li>Licensed &amp; insured · HIC #{HIC}</li></ul>
      <a class="est__call" href="tel:{TEL}"><small>Rather talk now?</small>{PHONE}</a>
    </div>
    <form class="quiz" id="quiz" novalidate{pre}>
      <div class="quiz__top"><span id="quizCount">Step 1 of 3</span><div class="quiz__bar"><i id="quizBar" style="width:33.3%"></i></div></div>
      <fieldset class="quiz__step is-on" data-step="1"><legend>What are we building?</legend><div class="opts">{o}</div></fieldset>
      <fieldset class="quiz__step" data-step="2"><legend>When would you like to start?</legend>
        <div class="opts opts--row"><label><input type="radio" name="when" value="As soon as possible"><span>ASAP</span></label><label><input type="radio" name="when" value="1-3 months"><span>1–3 months</span></label><label><input type="radio" name="when" value="3-6 months"><span>3–6 months</span></label><label><input type="radio" name="when" value="Just planning"><span>Just planning</span></label></div>
        <p class="quiz__sub">Rough budget <small>(optional, helps us plan)</small></p>
        <div class="opts opts--row"><label><input type="radio" name="budget" value="Under $25K"><span>Under $25K</span></label><label><input type="radio" name="budget" value="$25K-$50K"><span>$25–50K</span></label><label><input type="radio" name="budget" value="$50K-$100K"><span>$50–100K</span></label><label><input type="radio" name="budget" value="$100K+"><span>$100K+</span></label></div>
      </fieldset>
      <fieldset class="quiz__step" data-step="3"><legend>Where should we send your estimate?</legend>
        <div class="fields">
          <label class="f"><span>Full name</span><input name="fullname" autocomplete="name" required></label>
          <label class="f"><span>Phone</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" required></label>
          <label class="f"><span>Email</span><input name="email" type="email" autocomplete="email"></label>
          <label class="f"><span>Town</span><input name="town" autocomplete="address-level2" placeholder="e.g. Middletown"></label>
          <label class="f f--full"><span>Anything we should know? <small>(optional)</small></span><textarea name="notes" rows="3"></textarea></label>
        </div>
      </fieldset>
      <div class="quiz__step quiz__done" data-step="4" hidden><div class="done__ic" aria-hidden="true">✓</div><h3>Thanks, we've got it.</h3>
        <p>This is a preview site, so the form isn't connected yet. To reach the team today, call <a href="tel:{TEL}">{PHONE}</a>.</p></div>
      <p class="quiz__err" id="quizErr" role="alert"></p>
      <div class="quiz__nav"><button type="button" class="btn btn--line-light" id="quizBack" hidden>← Back</button><button type="button" class="btn btn--gold" id="quizNext">Next <span aria-hidden="true">→</span></button></div>
    </form>
  </div>
</section>'''


def bottom():
    svc = '<br>'.join(f'<a href="/{s["slug"]}">{e(s["nav"])}</a>' for s in SERVICES)
    return f'''</main>
<footer class="ftr">
  <div class="wrap ftr__grid">
    <div class="ftr__brand">
      <img src="/images/logo-mark.png" alt="Top Level Renovation" width="120" height="90" loading="lazy">
      <p>Family-run remodeling for Monmouth County homes, from one room to the whole house.</p>
    </div>
    <div><h3>Visit &amp; call</h3><p>3411 Rose Ave<br>Ocean Township, NJ 07712</p><p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Mon–Fri · 8am–5pm<br>Saturday · by appointment</p></div>
    <div><h3>Services</h3><p>{svc}</p></div>
    <div><h3>Company</h3><p><a href="/projects">Projects</a><br><a href="/reviews">Reviews</a><br><a href="/about-us">About us</a><br><a href="/contact">Contact</a><br><a href="/#reveal">Before &amp; after</a></p></div>
  </div>
  <div class="wrap ftr__base">
    <span>© 2026 Top Level Renovation, Inc. · Licensed &amp; insured · NJ HIC #{HIC}</span>
    <span>Careers: send your résumé to <a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <span>Website by Smart Marketing</span>
  </div>
</footer>
<nav class="dock" aria-label="Quick actions">
  <a href="tel:{TEL}">{PHONE_SVG}Call</a>
  <a class="dock__main" href="#estimate">Free estimate</a>
  <a href="/projects"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3zM12 5v14" fill="none" stroke="currentColor" stroke-width="2"/></svg>Projects</a>
</nav>
<dialog class="lb" id="lb" aria-label="Project photo">
  <img id="lbImg" alt="">
  <button class="lb__x" data-lb="close" aria-label="Close">×</button>
  <button class="lb__nav lb__prev" data-lb="prev" aria-label="Previous photo">‹</button>
  <button class="lb__nav lb__next" data-lb="next" aria-label="Next photo">›</button>
  <span class="lb__count" id="lbCount"></span>
</dialog>
<script src="/app.js" defer></script>
</body>
</html>
'''


def crumbs(items):
    """items: [(label, path)], last one is the current page."""
    li = ''.join(f'<li><a href="{p}">{e(l)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{e(l)}</li>' for i, (l, p) in enumerate(items))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l, "item": DOMAIN + p} for i, (l, p) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{li}</ol></nav>', ld


def page_hero(crumb_html, eyebrow, h1, lede, img, alt, ctas=True, small=False):
    c = f'''<div class="phero__ctas"><a class="btn btn--gold btn--lg" href="#estimate">Get my free estimate <span aria-hidden="true">→</span></a><a class="btn btn--ghost btn--lg" href="tel:{TEL}">Call {PHONE}</a></div>''' if ctas else ''
    return f'''<section class="phero{' phero--sm' if small else ''}">
  <div class="phero__media" aria-hidden="true"><img src="{img}" alt="" fetchpriority="high"></div>
  <div class="phero__shade" aria-hidden="true"></div>
  <div class="wrap phero__in">
    {crumb_html}
    <p class="eyebrow eyebrow--light">{e(eyebrow)}</p>
    <h1 class="phero__h">{e(h1)}</h1>
    <p class="phero__sub">{e(lede)}</p>
    {c}
    <a class="rating-chip" href="/reviews"><span class="stars" aria-hidden="true">★★★★★</span><b>4.9</b> from 89 Google reviews</a>
  </div>
  <span class="sr-only">{e(alt)}</span>
</section>'''


def gallery(slugs_or_photos, group='gallery'):
    """Photo grid with lightbox. Accepts [(slug, n)] tuples."""
    out = []
    for i, (slug, n) in enumerate(slugs_or_photos):
        p = P[slug]
        size = ' g--big' if i == 0 else (' g--wide' if i % 5 == 3 else '')
        out.append(f'<button class="g{size}" data-kind="{" ".join(p["kinds"])}" data-src="/images/p/{slug}/{n:02d}.jpg"><img src="{thumb(slug, n)}" alt="{e(p["title"])}: photo {n}" loading="lazy"><span>{e(p["title"])}</span></button>')
    return f'<div class="gallery" id="{group}" data-lb-group>{"".join(out)}</div>'


def pcards(slugs, chips=False, grid_id='pcards'):
    cards = []
    for s in slugs:
        p = P[s]
        n = len(IMG[s]['photos'])
        tag = ' <em>Before &amp; after</em>' if ('before' in IMG[s]['extra'] or 'stage-1' in IMG[s]['extra'] or 'composite' in IMG[s]['extra']) else ''
        cards.append(f'''<a class="pcard" href="/projects/{s}" data-kind="{" ".join(p["kinds"])}" data-reveal>
      <span class="pcard__img"><img src="{thumb(s)}" alt="{e(p["title"])}" loading="lazy"><span class="pcard__n">{n} photos</span></span>
      <span class="pcard__body"><small>{e(KIND_LABEL[p["kinds"][0]])} · {e(place(p))}</small><b>{e(p["title"])}</b>{tag}</span></a>''')
    ch = ''
    if chips:
        kinds = [('all', 'All'), ('kitchen', 'Kitchens'), ('bath', 'Baths'), ('home', 'Whole home'), ('exterior', 'Exterior'), ('commercial', 'Commercial')]
        ch = '<div class="chips" role="group" aria-label="Filter projects" data-for="%s">' % grid_id + ''.join(
            f'<button class="chip{" is-on" if k == "all" else ""}" aria-pressed="{"true" if k == "all" else "false"}" data-filter="{k}">{l}</button>' for k, l in kinds) + '</div>'
    return ch, f'<div class="pcards" id="{grid_id}">{"".join(cards)}</div>'


def ba_block(slug, compact=False):
    p, ex = P[slug], IMG[slug]['extra']
    base = f'/images/p/{slug}/'
    cap = f'<figcaption><b>{e(p["title"])}</b> · {e(place(p))} <a href="/projects/{slug}">See the project →</a></figcaption>'
    if 'stage-1' in ex:
        return f'''<figure class="bafig">
      <div class="scrub" data-simple style="--s:0">
        <img src="{base}stage-1.jpg" alt="Before: the worn roof seen from a drone" loading="lazy" data-stage="0">
        <img src="{base}stage-2.jpg" alt="During: the old roof torn off down to the decking" loading="lazy" data-stage="1">
        <img src="{base}stage-3.jpg" alt="After: the finished roof" loading="lazy" data-stage="2">
        <ol class="scrub__stages" aria-hidden="true"><li>Before</li><li>Tear-off</li><li>Finished</li></ol>
        <input class="scrub__range" type="range" min="0" max="200" value="0" aria-label="Scrub through the roof job: before, tear-off, finished">
      </div>{cap}</figure>'''
    if 'composite' in ex:
        b = a = base + 'composite.jpg'; comp = ' is-comp'
    elif 'before' in ex:
        b, a, comp = base + 'before.jpg', base + 'after.jpg', ''
    else:
        return ''
    return f'''<figure class="bafig">
      <div class="ba{comp}" data-simple style="--p:50%">
        <img class="ba__img ba__after" src="{a}" alt="After: {e(p["title"])}" loading="lazy">
        <div class="ba__clip"><img class="ba__img ba__before" src="{b}" alt="Before: the same space before the remodel" loading="lazy"></div>
        <span class="ba__tag ba__tag--b">Before</span><span class="ba__tag ba__tag--a">After</span>
        <div class="ba__handle" aria-hidden="true"><span>‹ ›</span></div>
        <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
      </div>{cap}</figure>'''


def reviews_block(tags, n=3, dark=True, title='What our clients say', link=True):
    rs = [r for r in REVIEWS if set(r['tags']) & set(tags)][:n] or REVIEWS[:n]
    cards = ''.join(f'''<figure class="rcard{' rcard--feature' if r.get('feature') and i == 0 else ''}"><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>{e(r["text"])}</blockquote><figcaption><b>{e(r["name"])}</b> · {e(r["job"])}</figcaption></figure>''' for i, r in enumerate(rs))
    lk = '<a class="rv-link" href="/reviews">Read more reviews <span aria-hidden="true">→</span></a>' if link else ''
    return f'''<section class="reviews reviews--sub">
  <div class="wrap">
    <div class="sec-head sec-head--row" data-reveal><div><p class="eyebrow eyebrow--light">Reviews</p><h2>{e(title)} <span class="gold">4.9★</span></h2></div>{lk}</div>
    <div class="rv rv--sub" id="rv{"".join(tags)}">{cards}</div>
  </div>
</section>'''


def process_block():
    li = ''.join(f'<li><span class="steps__n">{i}</span><div><h3>{e(h)}</h3><p>{e(t)}</p></div></li>' for i, (h, t) in enumerate(PROCESS, 1))
    return f'''<section class="how how--sub">
  <div class="wrap how__grid how__grid--solo">
    <div class="sec-head" data-reveal><p class="eyebrow">How we work</p><h2>One team. One project manager. <span class="u">One text thread.</span></h2>
      <p class="lede">The same five steps on every job, and one person who knows your project by name from the first visit to the final walkthrough.</p></div>
    <ol class="steps" id="steps">{li}</ol>
  </div>
</section>'''


def faq_block(items, title='Questions we hear a lot'):
    d = ''.join(f'<details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(items))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'''<section class="faq" id="faq">
  <div class="wrap faq__grid">
    <div class="sec-head" data-reveal><p class="eyebrow">FAQ</p><h2>{e(title)}</h2>
      <p class="lede">Something else? Call <a href="tel:{TEL}">{PHONE}</a>. You'll get a real person, Monday to Friday, 8 to 5.</p></div>
    <div class="qa">{d}</div>
  </div>
</section>''', ld


def areas_block():
    t = ''.join(f'<li>{e(x)}</li>' for x in TOWNS)
    return f'''<section class="areas" aria-labelledby="areasH"><div class="wrap areas__in" data-reveal>
  <div><p class="eyebrow">Where we work</p><h2 id="areasH">Your neighbors in Monmouth County.</h2><p class="lede">Based on the Shore and building across the county, and beyond for the right project.</p></div>
  <ul class="towns">{t}</ul></div></section>'''


def write(path, html_text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(html_text)


# ---------------------------------------------------------------- pages
def build_home():
    main = open(os.path.join(ROOT, 'tools', 'home_main.html')).read()
    h = head('Kitchen & Bathroom Remodeling Monmouth County NJ | Top Level Renovation',
             f"Monmouth County's 4.9-star remodeling team. Kitchens, bathrooms, whole-home renovations, additions, roofing and decks, designed and built by one team with one project manager. Licensed & insured, NJ HIC #{HIC}. Free estimates: {PHONE}.",
             '/', ld=[BUSINESS], preload=[('/images/hero-tall.jpg', ' media="(max-width: 760px)"'), ('/images/hero-wide.jpg', ' media="(min-width: 761px)"')])
    write('index.html', h + '\n' + top() + '\n' + main + estimate() + '\n' + bottom())


def build_service(s):
    path = '/' + s['slug']
    cr, cld = crumbs([('Home', '/'), (s['nav'], path)])
    scope = ''.join(f'<li data-reveal><b>{e(h)}</b><span>{e(t)}</span></li>' for h, t in s['scope'])
    intro = ''.join(f'<p>{e(x)}</p>' for x in s['intro'])
    side = s['projects'][0] if s['projects'] else None
    side_img = f'<a class="intro__img" href="/projects/{side}"><img src="/images/p/{side}/02.jpg" alt="{e(P[side]["title"])}" loading="lazy"><span>{e(P[side]["title"])} · {e(place(P[side]))}</span></a>' if side else ''
    bas = ''.join(ba_block(x) for x in s['ba'])
    ba_sec = f'''<section class="reveal reveal--sub"><div class="wrap">
    <div class="sec-head" data-reveal><p class="eyebrow eyebrow--light">Before &amp; after</p><h2>Drag to see the <span class="gold">difference.</span></h2><p class="lede">Real {e(s["noun"])} projects, real photos, same rooms.</p></div>
    <div class="ba-grid{' ba-grid--two' if len(s['ba']) > 1 else ''}">{bas}</div></div></section>''' if bas else ''
    _, cards = pcards(s['projects'], grid_id='pcards-' + s['key'])
    photos = []
    for slug in s['projects']:
        for ph in IMG[slug]['photos'][1:3]:
            photos.append((slug, int(ph['f'])))
    gal = gallery(photos[:10], group='gallery-' + s['key']) if len(photos) >= 4 else ''
    faq, fld = faq_block(s['faq'] + GENERAL_FAQ[:2], f'{s["nav"]} questions')
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s['h1'], "serviceType": s['nav'], "provider": {"@id": DOMAIN + "/#business"},
                  "areaServed": "Monmouth County, NJ", "url": DOMAIN + path, "description": s['desc']}
    others = ''.join(f'<a href="/{o["slug"]}"><img src="{o["hero"].replace(".jpg", "-t.jpg") if "/images/p/" in o["hero"] else o["hero"]}" alt="" loading="lazy"><b>{e(o["nav"])}</b></a>' for o in SERVICES if o['slug'] != s['slug'])
    body = f'''{page_hero(cr, 'Monmouth County, NJ · Design + Build', s["h1"], s["lede"], s["hero"], s["hero_alt"])}
<section class="intro"><div class="wrap intro__grid">
  <div class="prose" data-reveal><p class="eyebrow">{e(s["nav"])}</p><h2>Designed around how you live. <span class="u">Built to last.</span></h2>{intro}
    <p class="intro__ctas"><a class="btn btn--line" href="#estimate">Plan my {e(s["nav"].lower().rstrip("s") if s["key"] in ("kitchen","bath") else "project")} <span aria-hidden="true">→</span></a></p></div>
  {side_img}
</div></section>
<section class="scope"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">What we do</p><h2>Everything your {e(s["noun"])} project needs, <span class="u">one team.</span></h2></div>
  <ul class="scope__grid">{scope}</ul>
</div></section>
{ba_sec}
<section class="work work--sub"><div class="wrap">
  <div class="sec-head sec-head--row" data-reveal><div><p class="eyebrow">Recent projects</p><h2>{e(s.get("projects_title", "Recent " + s["noun"] + " projects"))}</h2></div><a class="rv-link rv-link--dark" href="/projects">All projects <span aria-hidden="true">→</span></a></div>
  {cards}
  {gal}
</div></section>
{process_block()}
{reviews_block([s["key"], "general"] if s["key"] not in ("roof", "deck") else ["exterior"], n=3)}
{faq}
<section class="related"><div class="wrap"><p class="eyebrow">More services</p><div class="related__row">{others}</div></div></section>
{estimate(s["pick"], heading=f'Planning a {s["nav"].lower().rstrip("s") if s["key"] in ("kitchen","bath") else s["nav"].lower()} project?' if s["key"] in ("kitchen","bath") else 'Tell us about your project.')}'''
    h = head(s['title'], s['desc'], path, image=s['hero'], ld=[BUSINESS, service_ld, cld, fld], preload=[(s['hero'], '')])
    write(s['slug'] + '.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_projects_index():
    cr, cld = crumbs([('Home', '/'), ('Projects', '/projects')])
    order = [p['slug'] for p in PROJECTS]
    ch, cards = pcards(order, chips=True)
    body = f'''{page_hero(cr, 'Our work', 'Recent remodeling projects', 'Real Monmouth County homes, photographed after (and often before) we finished. Pick a project to see every photo.', '/images/p/navy-galley-kitchen/01.jpg', 'Navy galley kitchen', ctas=False, small=True)}
<section class="work work--index"><div class="wrap">
  <div class="sec-head sec-head--row" data-reveal><div><p class="eyebrow">{len(order)} projects</p><h2>Kitchens, baths, whole homes &amp; more.</h2></div>{ch}</div>
  {cards}
</div></section>
{reviews_block(["general"], n=3)}
{estimate()}'''
    h = head('Remodeling Projects in Monmouth County, NJ | Top Level Renovation',
             'Before-and-after photos of recent kitchen, bathroom, whole-home, roofing, deck and commercial projects by Top Level Renovation in Monmouth County, NJ.',
             '/projects', image='/images/p/navy-galley-kitchen/01.jpg', ld=[BUSINESS, cld])
    write('projects.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_project(p):
    s, path = p['slug'], '/projects/' + p['slug']
    cr, cld = crumbs([('Home', '/'), ('Projects', '/projects'), (p['title'], path)])
    photos = IMG[s]['photos']
    meta = ''.join(f'<li><small>{k}</small><b>{e(v)}</b></li>' for k, v in [('Project', ' + '.join(KIND_LABEL[k] for k in p['kinds'])), ('Location', p.get('town') or 'Monmouth County area'), ('Completed', p.get('status') or p.get('date') or 'Recent')] if v)
    ba = ba_block(s)
    ba_sec = f'<section class="reveal reveal--sub reveal--project"><div class="wrap"><div class="sec-head" data-reveal><p class="eyebrow eyebrow--light">Before &amp; after</p><h2>Drag to see the <span class="gold">difference.</span></h2></div><div class="ba-grid">{ba}</div></div></section>' if ba else ''
    reel = ''
    if p.get('reel'):
        reel = f'''<div class="preel"><figure class="reel"><video preload="none" muted playsinline loop poster="/images/p/{s}/02.jpg" src="/video/{p["reel"]}.mp4" aria-label="{e(p["title"])} video"></video>
      <button class="reel__play" aria-label="Play the {e(p["title"])} video"><span aria-hidden="true">▶</span></button><figcaption><b>Watch the video</b><small>{e(place(p))}</small></figcaption></figure></div>'''
    g = ''.join(f'<button class="g{" g--big" if i == 0 else ""}" data-src="/images/p/{s}/{ph["f"]}.jpg"><img src="/images/p/{s}/{ph["f"]}-t.jpg" alt="{e(p["title"])}: photo {i + 1} of {len(photos)}" width="{ph["w"]}" height="{ph["h"]}" loading="{"eager" if i < 3 else "lazy"}"></button>' for i, ph in enumerate(photos))
    related = [x['slug'] for x in PROJECTS if x['slug'] != s and set(x['kinds']) & set(p['kinds'])][:3]
    _, rc = pcards(related, grid_id='related')
    svc = {'kitchen': 'kitchens', 'bath': 'bathrooms', 'home': 'home-renovations', 'commercial': 'commercial', 'exterior': 'roofing-and-siding' if 'roof' in s else 'decks-and-outdoor'}[p['kinds'][0]]
    note = '<p class="pnote">Status: in progress. We\'ll add the finished photos when the job wraps.</p>' if p.get('status') else ''
    body = f'''<section class="pintro"><div class="wrap">
  {cr}
  <div class="pintro__grid">
    <div data-reveal><p class="eyebrow">{e(KIND_LABEL[p["kinds"][0]])} project</p><h1 class="pintro__h">{e(p["title"])}</h1><p class="lede">{e(p["summary"])}</p>{note}
      <p class="intro__ctas"><a class="btn btn--gold" href="#estimate">Start a project like this <span aria-hidden="true">→</span></a><a class="btn btn--line" href="/{svc}">{e(SV[svc]["nav"])} <span aria-hidden="true">→</span></a></p></div>
    <ul class="pmeta" data-reveal>{meta}</ul>
  </div>
</div></section>
<section class="pgal"><div class="wrap"><div class="gallery gallery--project" data-lb-group>{g}</div>{reel}</div></section>
{ba_sec}
<section class="work work--sub"><div class="wrap"><div class="sec-head sec-head--row" data-reveal><div><p class="eyebrow">Keep browsing</p><h2>Similar projects</h2></div><a class="rv-link rv-link--dark" href="/projects">All projects <span aria-hidden="true">→</span></a></div>{rc}</div></section>
{estimate(KIND_PICK[p["kinds"][0]] if "roof" not in s else "Roofing / siding", heading='Want something like this?')}'''
    desc = f'{p["title"]}{" in " + p["town"] + ", NJ" if p.get("town") else ""} by Top Level Renovation. {p["summary"]}'[:300]
    h = head(f'{p["title"]}{" · " + p["town"] + " NJ" if p.get("town") else ""} | Top Level Renovation Projects', desc, path, image=f'/images/p/{s}/01.jpg', ld=[cld])
    write(f'projects/{s}.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_about():
    cr, cld = crumbs([('Home', '/'), ('About us', '/about-us')])
    values = [('Experience', 'Our skilled team brings years of hands-on knowledge to every project, from concept to completion.'),
              ('Local expertise', "Based in Monmouth County, we know the area's homes, weather and building requirements. We're your neighbors."),
              ('Quality', 'Quality is the cornerstone of our work: the finest materials we can source and methods that last.'),
              ('Licensed & insured', f'Fully licensed and insured in New Jersey, HIC #{HIC}, and BBB Accredited.'),
              ('Client-centric', 'We listen, communicate clearly throughout the project and tailor the work to your vision and budget.'),
              ('Track record', 'From single bathrooms to whole homes and commercial spaces, we let our work speak for itself.')]
    v = ''.join(f'<li data-reveal><b>{e(h)}</b><span>{e(t)}</span></li>' for h, t in values)
    team = [('Alberto', 'Owner', 'From the very first consultation, Alberto completely understood my vision.'),
            ('Pat', 'Project Manager', 'Our project manager, Pat, was onsite regularly to check on progress.'),
            ('Karla', 'Office Manager', 'Their office manager, Karla, kept things very organized.'),
            ('Jackie', 'Design', 'I met Jackie who helped guide me with some key design ideas.')]
    t = ''.join(f'<li data-reveal><span class="team__av" aria-hidden="true">{n[0]}</span><b>{e(n)}</b><small>{e(r)}</small><q>{e(q)}</q></li>' for n, r, q in team)
    body = f'''{page_hero(cr, 'About Top Level Renovation', 'Concentrated efforts to build better.', 'A family-run remodeling company serving Monmouth County for over 15 years, where more of your money goes into the work itself.', '/images/camelot-living.jpg', 'Bright living room remodeled by Top Level Renovation', small=True)}
<section class="intro"><div class="wrap intro__grid">
  <div class="prose" data-reveal><p class="eyebrow">Our story</p><h2>Full-service remodeling, <span class="u">personal service.</span></h2>
    <p>Top Level Renovation, Inc. is a full-service remodeling, renovation and repair company that has become a go-to in Monmouth County for high-quality craftsmanship, whatever the size of the job.</p>
    <p>As a family-run business, we give our clients more personal service. Without the overhead of bigger, less flexible remodeling companies, more of your hard-earned money goes into the work itself.</p>
    <p>Every project gets one project manager who coordinates the trades, keeps you updated, usually by group text, and makes sure the job site is left clean at the end of every day. It's the thing our clients mention most in their reviews.</p></div>
  <a class="intro__img" href="/projects/sage-primary-bath"><img src="/images/p/sage-primary-bath/02.jpg" alt="Sage primary bath" loading="lazy"><span>Sage Primary Bath · August 2026</span></a>
</div></section>
<section class="team"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">The team</p><h2>The people our clients <span class="u">mention by name.</span></h2><p class="lede">Quotes from our Google reviews.</p></div>
  <ul class="team__grid">{t}</ul>
</div></section>
<section class="scope"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">Why clients choose us</p><h2>Six reasons, <span class="u">one standard.</span></h2></div>
  <ul class="scope__grid">{v}</ul>
</div></section>
{process_block()}
{reviews_block(["general"], n=3)}
{areas_block()}
<section class="careers"><div class="wrap careers__in" data-reveal><div><p class="eyebrow">Careers</p><h2>Want to build with us?</h2><p class="lede">To apply, send a cover letter and your résumé to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div></div></section>
{estimate()}'''
    h = head('About Top Level Renovation | Family-Run Remodeling in Monmouth County, NJ',
             f'Top Level Renovation is a family-run, full-service remodeling company in Monmouth County, NJ. One project manager per job, licensed & insured, NJ HIC #{HIC}, BBB Accredited.',
             '/about-us', image='/images/camelot-living.jpg', ld=[BUSINESS, cld])
    write('about-us.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_reviews():
    cr, cld = crumbs([('Home', '/'), ('Reviews', '/reviews')])
    cards = ''.join(f'''<figure class="rcard{' rcard--feature' if r.get('feature') else ''}" data-reveal><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>{e(r["text"])}</blockquote><figcaption><b>{e(r["name"])}</b> · {e(r["job"])}</figcaption></figure>''' for r in REVIEWS)
    body = f'''{page_hero(cr, 'Reviews', '4.9 stars from 89 Google reviews.', 'Kitchens, baths, porches, siding and whole homes. Here is what Monmouth County homeowners say about working with our team.', '/images/p/navy-galley-kitchen/02.jpg', 'Navy galley kitchen', ctas=False, small=True)}
<section class="rsummary"><div class="wrap rsummary__in" data-reveal>
  <div class="rsummary__score"><b>4.9</b><span class="stars" aria-hidden="true">★★★★★</span><small>89 Google reviews</small></div>
  <p>What clients mention most: <b>one project manager</b> who coordinates everything, <b>constant communication</b> by group text, <b>tile work and craftsmanship</b>, and a <b>clean home at the end of every day</b>.</p>
  <a class="btn btn--line" href="https://www.google.com/search?q=Top+Level+Renovation+NJ+reviews" target="_blank" rel="noopener">Read all reviews on Google <span aria-hidden="true">↗</span></a>
</div></section>
<section class="reviews reviews--all"><div class="wrap"><div class="rgrid">{cards}</div></div></section>
{estimate(heading='Join our happy clients.')}'''
    h = head('Reviews | Top Level Renovation · 4.9★ Remodeling Contractor in Monmouth County, NJ',
             'Read what Monmouth County homeowners say about Top Level Renovation: 4.9 stars from 89 Google reviews for kitchens, baths, whole homes, porches and siding.',
             '/reviews', ld=[BUSINESS, cld])
    write('reviews.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_contact():
    cr, cld = crumbs([('Home', '/'), ('Contact', '/contact')])
    cards = [('Call', f'<a href="tel:{TEL}">{PHONE}</a>', 'Mon–Fri, 8am–5pm'), ('Email', f'<a href="mailto:{EMAIL}">{EMAIL}</a>', 'We reply on business days'),
             ('Visit', '3411 Rose Ave<br>Ocean Township, NJ 07712', 'Saturday by appointment'), ('Licensed', f'NJ HIC #{HIC}', 'Fully insured · BBB Accredited')]
    c = ''.join(f'<li data-reveal><small>{k}</small><b>{v}</b><span>{s}</span></li>' for k, v, s in cards)
    hero_html = page_hero(cr, 'Contact', "Let's talk about your project.", "Call, email or answer three quick questions below, and we'll set up a free in-home consult.", '/images/p/cream-kitchen-dark-island/01.jpg', 'Cream kitchen with dark island', small=True)
    body = f'''{hero_html}
<section class="contact"><div class="wrap contact__grid">
  <ul class="ccards">{c}</ul>
  <div class="map" data-reveal><iframe title="Map: 3411 Rose Ave, Ocean Township, NJ" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=3411+Rose+Ave,+Ocean+Township,+NJ+07712&amp;output=embed"></iframe></div>
</div></section>
{estimate(heading='Get your free estimate.')}
{areas_block()}'''
    h = head('Contact Top Level Renovation | Free Remodeling Estimates in Monmouth County, NJ',
             f'Contact Top Level Renovation for a free in-home estimate. Call {PHONE}, email {EMAIL}, or visit 3411 Rose Ave, Ocean Township, NJ. Mon–Fri 8am–5pm.',
             '/contact', ld=[BUSINESS, cld])
    write('contact.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_404():
    links = ''.join(f'<a href="/{s["slug"]}">{e(s["nav"])}</a>' for s in SERVICES)
    body = f'''<section class="e404"><div class="wrap e404__in">
  <p class="eyebrow">404</p><h1 class="pintro__h">This page moved or doesn't exist.</h1>
  <p class="lede">Our website just got a full rebuild, so some old links point to pages that have moved. Try one of these:</p>
  <div class="e404__links"><a class="btn btn--gold" href="/">Homepage</a><a class="btn btn--line" href="/projects">Projects</a><a class="btn btn--line" href="/contact">Contact</a></div>
  <div class="related__row related__row--text">{links}</div>
</div></section>
{estimate()}'''
    h = head('Page not found | Top Level Renovation', 'This page could not be found.', '/404')
    write('404.html', h + '\n' + top() + '\n' + body + '\n' + bottom())


def build_meta():
    # Old Wix URLs -> new pages. Service slugs kept their original paths.
    old_projects = {
        '/2-abbey-lane-marlboro': 'marlboro-full-home-remodel', '/oceanport-kitchen': 'oceanport-kitchen', '/72-tindall-rd-middletown': 'middletown-kitchen',
        '/33-stavola-road': 'middletown-marble-bath', '/33-goose-neck-point-rd-oceanport': 'oceanport-roof-replacement', '/82-leedsville-dr-lincroft': 'lincroft-kitchen',
        '/17-belle': 'manalapan-kitchen', '/backyard-marlboro': 'marlboro-composite-deck', '/160-newbury-rd-howell': 'howell-whole-home',
        '/11-cooper-ave-long-branch': 'long-branch-primary-bath', '/80-poplar-ave-wlb': 'open-plan-first-floor'}
    lines = ['# Old Wix URLs -> new site (301). Service pages kept their original paths.',
             '/services / 301', '/gallery /projects 301', '/members / 301', '/blog / 301', '/blog-feed.xml / 301', '/post/* / 301',
             '/items /projects 301', '/items/* /projects 301', '/renovations /home-renovations 301', '/home /  301']
    lines += [f'{o} /projects/{n} 301' for o, n in old_projects.items()]
    for o in ['/114-riverbank-burlington', '/24-thornly-rd-eatontown', '/38-newman-springs-red-bank', '/5-majestic-ave-lincroft', '/8-burke-drive-farmingdale', '/82-broadway-freehold', '/mount-holly']:
        lines.append(f'{o} /projects 301')
    open(os.path.join(ROOT, '_redirects'), 'w').write('\n'.join(lines).replace('  301', ' 301') + '\n')
    urls = ['/', '/projects', '/about-us', '/reviews', '/contact'] + ['/' + s['slug'] for s in SERVICES] + ['/projects/' + p['slug'] for p in PROJECTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    return urls


if __name__ == '__main__':
    build_home()
    for s in SERVICES: build_service(s)
    build_projects_index()
    for p in PROJECTS: build_project(p)
    build_about(); build_reviews(); build_contact(); build_404()
    urls = build_meta()
    print(f'built {len(urls)} pages + 404')
