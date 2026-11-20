# SEO <title> and meta description for every indexable page, keyed by path.
# build.py's head() uses these when present (they also feed og:/twitter: tags).
# Targets: title 50-60 characters (keyword + town/county), description 140-160
# characters ending in a call to action. Check with: python3 tools/seo_meta.py
SEO = {
  '/': (
    'Remodeling Contractor in Monmouth County, NJ | Top Level',
    'Kitchen, bathroom and whole-home remodeling in Monmouth County, NJ. Family-run, licensed and insured, 4.9 stars on Google. Call (732) 538-9379 for an estimate.'),
  '/projects': (
    'Remodeling Projects in Monmouth County, NJ | Top Level',
    'Browse real kitchen, bathroom, whole-home, roofing and deck projects by Top Level Renovation across Monmouth County, NJ. Like what you see? Get a free estimate.'),
  '/about-us': (
    'About Us | Family-Run Remodeling Contractor, Monmouth NJ',
    'Meet Top Level Renovation, a family-run remodeling contractor in Ocean Township serving Monmouth County, NJ. Licensed and insured. Call (732) 538-9379 today.'),
  '/reviews': (
    'Reviews | 4.9-Star Remodeling Contractor in Monmouth NJ',
    'Read what Monmouth County homeowners say about Top Level Renovation: 4.9 stars on Google for kitchens, baths and full remodels. Get your free estimate today.'),
  '/contact': (
    'Contact Us | Free Remodeling Estimate in Monmouth County',
    'Request a free remodeling estimate from Top Level Renovation in Ocean Township, NJ. Serving all of Monmouth County. Call (732) 538-9379 or send us your project.'),
  '/kitchens': (
    'Kitchen Remodeling in Monmouth County, NJ | Top Level',
    'Custom kitchen remodels in Monmouth County, NJ: cabinets, islands, stone counters and new layouts, built by one team. Call (732) 538-9379 for a free estimate.'),
  '/bathrooms': (
    'Bathroom Remodeling in Monmouth County, NJ | Top Level',
    'Bathroom remodels in Monmouth County, NJ: walk-in showers, freestanding tubs, custom tile and vanities, with one project manager. Get your free estimate today.'),
  '/home-renovations': (
    'Whole-Home Renovations in Monmouth County, NJ | Top Level',
    'Whole-home and first-floor renovations in Monmouth County, NJ, from one room to a full gut remodel. One team, one schedule. Call (732) 538-9379 for an estimate.'),
  '/additions': (
    'Home Additions in Monmouth County, NJ | Top Level Renovation',
    'Home additions in Monmouth County, NJ: bedrooms, bigger kitchens, offices and family rooms that blend with your house. Call (732) 538-9379 for a free estimate.'),
  '/roofing-and-siding': (
    'Roofing & Siding in Monmouth County, NJ | Top Level',
    'Roof replacement, siding and gutters in Monmouth County, NJ. Full tear-offs, documented start to finish, licensed and insured. Call (732) 538-9379 today.'),
  '/decks-and-outdoor': (
    'Decks, Patios & Porches in Monmouth County, NJ | Top Level',
    'Composite decks, Trex stairs, patios and covered porches in Monmouth County, NJ, built by the team that remodels the inside. Call (732) 538-9379 today.'),
  '/commercial': (
    'Commercial Renovation in Monmouth County, NJ | Top Level',
    'Commercial build-outs and renovations in Monmouth County, NJ: offices, retail and corridors, framing to finish, on your schedule. Call (732) 538-9379 today.'),
  # ---- projects ----
  '/projects/studs-to-finish-kitchen': (
    'Studs-to-Finish Kitchen Remodel, Monmouth County NJ',
    'A first floor stripped to the studs and rebuilt around a big quartz island with white shaker cabinets. See every photo, then get a free kitchen estimate.'),
  '/projects/navy-galley-kitchen': (
    'Navy Galley Kitchen Remodel in Monmouth County, NJ',
    'A dated galley kitchen turned two-tone: navy lowers, soft-blue uppers, a farmhouse sink and a breakfast nook. See the photos and get a free estimate for yours.'),
  '/projects/sage-primary-bath': (
    'Sage Primary Bathroom Remodel in Monmouth County, NJ',
    'A primary bath with a sage double vanity, brass fixtures, a freestanding tub and a frameless glass shower. See all the photos and get a free estimate for yours.'),
  '/projects/spa-bath-fluted-shower': (
    'Spa Bathroom Remodel with Fluted Shower, Monmouth NJ',
    'A freestanding tub, floating wood vanity, backlit arched mirrors and a fluted-wood walk-in shower. See the before and after, then get a free bathroom estimate.'),
  '/projects/oak-and-brass-bath': (
    'Oak & Brass Bathroom Remodel in Monmouth County, NJ',
    'A warm oak vanity, brushed-brass fixtures, an arched mirror and a walk-in shower with a herringbone niche. See every photo, then get a free estimate for yours.'),
  '/projects/cream-kitchen-dark-island': (
    'Cream Kitchen with Dark Island, Monmouth County NJ',
    'Cream cabinetry with a contrasting dark island, granite counters, lantern pendants and a tile-framed range hood. See the photos and get a free kitchen estimate.'),
  '/projects/white-and-grey-kitchen': (
    'White & Grey Kitchen Remodel in Monmouth County, NJ',
    'White shaker cabinets, a grey tile backsplash, marble-look counters and new stainless appliances. See all the photos, then get a free estimate for your kitchen.'),
  '/projects/hall-bath-refresh': (
    'Hall Bathroom Remodel in Monmouth County, NJ | Top Level',
    'A tired hall bath reworked with a glass walk-in shower, hexagon-tile floor, dark vanity and a tile band. See the before and after and get a free estimate today.'),
  '/projects/brass-and-blue-bath': (
    'Brass & Blue Bathroom Remodel in Monmouth County, NJ',
    'A warm wood double vanity, antique-brass fixtures, a scalloped mosaic backsplash and a blue tile shower. See every photo, then get a free bath estimate.'),
  '/projects/tub-to-tile-bath': (
    'Tub-to-Tile Bathroom Remodel in Monmouth County, NJ',
    'A dated tub surround swapped for large-format tile, a built-in niche and a wood vanity with a stone top. See the before and after and get a free estimate.'),
  '/projects/green-tile-bath': (
    'Green Tile Bathroom Remodel in Monmouth County, NJ',
    'Green subway-tile shower walls with a framed niche, a wood double vanity, brass faucets and matching mirrors. See every photo and get a free estimate.'),
  '/projects/blue-mosaic-bath': (
    'Blue Mosaic Bathroom Remodel in Monmouth County, NJ',
    'A bright bath built around a blue glass-mosaic feature wall, a freestanding tub and a frameless glass shower. See all the photos and get a free estimate today.'),
  '/projects/open-plan-first-floor': (
    'Open-Plan First Floor Remodel in West Long Branch, NJ',
    'An open first floor in West Long Branch, NJ with a white kitchen, navy island, coffee bar, built-ins and a fireplace wall. See the photos and get an estimate.'),
  '/projects/commercial-corridor-build-out': (
    'Commercial Corridor Build-Out in Monmouth County, NJ',
    'A commercial corridor build-out: steel-stud framing, insulation and drywall, floors protected throughout. See the progress photos and get a free quote.'),
  '/projects/middletown-kitchen': (
    'Navy & White Kitchen Remodel in Middletown, NJ | Top Level',
    'A long Middletown, NJ kitchen with navy lowers, white uppers, a barn-door pantry and an island open to the family room. See the photos and get a free estimate.'),
  '/projects/middletown-marble-bath': (
    'Marble & Gold Primary Bathroom in Middletown, NJ | Top Level',
    'A Middletown, NJ primary bath with marble-look walls, a navy vanity, gold fixtures, a soaking tub and glass shower. See every photo, then get a free estimate.'),
  '/projects/marlboro-full-home-remodel': (
    'Full Home Remodel in Marlboro, NJ | Top Level Renovation',
    'A full Marlboro, NJ home remodel: new white kitchen and island, wood-look floors, refreshed bedrooms and baths, painted brick fireplace. Get your free estimate.'),
  '/projects/oceanport-kitchen': (
    'Coastal White Kitchen Remodel in Oceanport, NJ | Top Level',
    'An Oceanport, NJ white kitchen with a long granite island and hardwood floors, open to a living room with a shiplap fireplace. See the photos and get a quote.'),
  '/projects/oceanport-roof-replacement': (
    'Waterfront Roof Replacement in Oceanport, NJ | Top Level',
    'A full tear-off on an Oceanport, NJ waterfront home, documented by drone and finished in charcoal architectural shingles. See the photos and get a quote.'),
  '/projects/lincroft-kitchen': (
    'Warm Wood Kitchen Remodel in Lincroft, NJ | Top Level',
    'A Lincroft, NJ kitchen with rich wood cabinetry, quartz counters, a long seating island and a pot filler over the range. See every photo and get an estimate.'),
  '/projects/manalapan-kitchen': (
    'White Shaker Kitchen Remodel in Manalapan, NJ | Top Level',
    'A Manalapan, NJ white shaker kitchen with an island, glass-front cabinets and open shelving, plus a dark-wall powder room. See the photos and get an estimate.'),
  '/projects/marlboro-composite-deck': (
    'Composite Deck Build in Marlboro, NJ | Top Level Renovation',
    'A large composite deck with black railings and wide stairs across the back of a Marlboro, NJ ranch home. See the photos, then get a free estimate for your deck.'),
  '/projects/howell-whole-home': (
    'Whole-Home Renovation in Howell, NJ | Top Level Renovation',
    'A Howell, NJ whole-home renovation: white kitchen with a blue island, light oak floors, a freestanding-tub primary bath and new bedrooms. Get an estimate.'),
  '/projects/long-branch-primary-bath': (
    'Primary Bathroom Remodel in Long Branch, NJ | Top Level',
    'A Long Branch, NJ primary bath: freestanding tub, large-format wood-look tile and a frameless walk-in shower replace a dated tub deck. Get your free estimate.'),
}

if __name__ == '__main__':
    bad = 0
    for path, (t, d) in SEO.items():
        ok = 50 <= len(t) <= 60 and 140 <= len(d) <= 160
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} T{len(t):>3} D{len(d):>3}  {path}")
    print(len(SEO), 'pages,', bad, 'out of range')
