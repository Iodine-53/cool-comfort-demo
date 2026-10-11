# Cool Comfort Heating & Cooling — demo website ("THE NUMBER FIRST")

Prospect: **Cool Comfort Heating And Cooling** — HVAC, Tampa FL · (813) 680-5348 · contact@coolcomfortflorida.com
Real site: coolcomfortflorida.com (thin 2023-era WordPress one-pager, awkward copy, no online booking).
Status: **local preview only — NOT deployed, NOT pitched**. Demo photos are AI-generated illustrations, noted in the footer.
Planned alias (meta only, not deployed): https://cool-comfort-heating-cooling-demo-iodine-53s-projects.vercel.app/

Serve: `cd ~/workspace/tampa-leads/demos/cool-comfort && python3 -m http.server 8941`

## Concept
**THE NUMBER FIRST.** The hero leads with the cost answer, not the form and not the company: an operable replacement-cost instrument (home-size slider + system-type chips) that live-rewrites a giant mono price range. Zero asks to use it — the number is the offer, the form is the mechanism.

Deviation from the brief's suggestion, stated plainly: the brief proposed a "Type your ZIP — see your range in 30 seconds" flow and an operable booking card as the two signature options. Both are already shipped by siblings (air-turbulencia runs the ZIP→range widget; air-turbulencia AND air-stream both run the operable booking card). This demo takes the third, unclaimed lane: the price instrument itself is the hero, driven by home size + system type instead of ZIP.

## Art-direction triple
**plainspoken / sunlit / numbers-first**
- *plainspoken* — 5th-grade copy, spoken sentences, honest ranges with the variables named; no jargon, no brochure voice.
- *sunlit* — warm sand ground `#faf6ef`, ink `#171310`, Tampa-midday warmth; one flame accent `#e4572e` used **only on primary CTAs** (5.01:1 with ink text).
- *numbers-first* — mono numerals dominate: the giant range, from-prices, license, hours, stats all set in IBM Plex Mono.

Type: Chivo (400/500/700/900 — display + body, self-hosted woff2) + IBM Plex Mono (400/500/600 — utility). Two families, no generic sans. One hand-written `--ease: cubic-bezier(.19,1,.22,1)`; **one reveal type: blur-to-sharp**, gated on `html.js` (fully readable with JS off); 1px borders, sharp corners except pill CTAs; zero drop shadows; film grain on the dark stat band.

## Deliberately broken convention
No photo fan across the hero (the playbook house pattern) — the hero's dominant visual is typographic: the pain headline plus the giant live price figure. No testimonial section either: proof lives only beside decisions (one real review under the hero trust line, two real reviews beside the estimate form). One italic-serif swap was skipped in favour of the two-family cap — emphasis is done with the mono face instead.

## Signature interactive element
1. **Replacement-cost instrument** (hero): sq-ft slider (1,200–3,200) + system chips (Split / Heat pump / Package / Mini-split) → giant live mono range (`$5,900–$7,900` default at 1,800 sq ft split), with a per-type footnote. Server-rendered default so JS-off still shows a real number. Math: split `lo=3900+sqft*1.10, hi=5200+sqft*1.50` (rounded to $100); heat pump +$1,000/+$1,200; package −$400; mini-split flat $3,800–$5,500.
2. **Before/after job slider** (Nielsen rules): 50% start, visible ≥44px grip with arrows, persistent BEFORE/AFTER labels, click-to-jump, keyboard arrows in 5% steps, hand-drawn marker caption.
3. **3-field estimate form → mailto handoff**: name/phone/symptom composes an email to contact@coolcomfortflorida.com; the line under the button says exactly that.
4. **Live Tampa-time chip** in the header ("OPEN NOW · 9:47 AM ET" / "OPENS 7 AM ET"), static "7 AM–10 PM DAILY" fallback.

## Playbook moves applied
Pain-opening H1 ("AC out? Cool again by tonight." — 31 chars, 5th grade) + audience + price anchor + two front doors in a sticky strip (bare `tel:` vs "Get my written quote"); customer-vocabulary nav (AC repair / System replacement / Tune-ups / Emergency); named enemy ("Not a phone quote that triples on install day"); insider-ritual headline ("500-micron vacuum. Every single install."); stake-ladder process (written quote = price final; Manual J = no oversized short-cycler; we pull the permit = you sign nothing; pay when the air is cold); decision ladder titled as the visitor's own decisions ("1. Can it be repaired, or is it a replacement?", "2. What does it cost, and what moves the number?", "3. Who shows up at the door?"); bento services with from-prices + durations (exactly 6 cells, no orphan); "5 signs your AC is dying" symptom section with quiet inline CTAs; FAQ with FAQPage schema + honest 2026 ranges + cost-of-inaction; two-tier service areas (Same-day: Tampa core, Ybor City, Hyde Park, Westshore / Next-day: Carrollwood, New Tampa, Riverview, Brandon); their real specials from their own site (10% off replacements, $99 maintenance, 30% off recharge); dark stat band with outlined cards; one motif propagated (price ticket: eyebrows, bullets, divider rows, sticky-bar icon, logo mark, favicon); hand-drawn favicon (flame in ticket, accent on ink); og-image.jpg 1200×630 cropped from the hero; full OG/Twitter meta with absolute planned-alias URLs; two visual registers (loud red panic strip / Mercury-calm money section with "0% APR · payments from $89/mo"); kill list clean (no autoplay, no popups, no chat widget, no modal before dial); sticky mobile bottom bar (Call + Book Online, number printed, slides up past hero, hides at final CTA); tap targets ≥44px; accessibility six-check (one H1, labels on all inputs, alt text, contrast ≥4.5 on CTAs, focus-visible rings, JS-off facts verified).

## Distinctness vs siblings
- ally-hvac ("TURNKEY"): accountability frame, payment-estimator slider, HUD-annotated condenser, green-ink/copper, Oswald. Mine: no estimator-as-financing (mine is upfront cost, hero-placed), no HUD chips, no photo hero at all, warm sand/flame/Chivo.
- air-turbulencia ("AIRFLOW"): dispatch console, operable booking card, ZIP→range widget, "dispatch line that goes to voicemail" enemy, "We measure the load" ritual, wind-current motif. Mine: no booking card, no ZIP, different enemy, different ritual ("500-micron vacuum"), price-ticket motif.
- air-stream ("Air, Engineered"): no-photo hero + operable booking card, ice-cyan, Archivo, airflow-lines motif, calm/fast/cool. Mine: operable hero is a price instrument not a booking card, warm register, different motif and type.
- anchor-air: heat-vs-cool navy/ice-cyan with particles. Mine shares nothing with it.

## Placeholder-data caveats (flagged, footer-disclosed)
- **Phone settled 2026-10-10:** the lead list said 813-592-4209, but their live site, Birdeye/GBP listing, and the Pinellas County Accela licensed-professional record for COOL COMFORT HEATING AND COOLING, LLC (11104 Bloomington Dr) all print 813-680-5348 — demo now uses 813-680-5348 everywhere.
- **Real, used verbatim:** business name, email contact@coolcomfortflorida.com, FL license #CAC1821452, hours 7 AM–10 PM daily, the two review excerpts (Brett D. re: Jared; Alicia F. re: John), the three specials (10% off replacements, $99 maintenance, 30% off recharge).
- **Invented placeholders:** ★4.7 / 300+ reviews, 2,400+ jobs, 10-yr workmanship warranty, 0% APR from $89/mo, all from-prices except the tune-up anchor ($129 repair, $5,900 replacement, $6,900 heat pump, $3,800 mini-split, $89 diagnostic), the calculator's exact ranges (grounded in published 2026 Florida data: $3,900–$8,000 installed statewide, 16–18 SEER2 +$800–$1,500, Tampa avg repair $353 per Angi, 30–40% post-2025 refrigerant-transition uplift), Jared's bio (name is real, NATE/11-yrs invented), job captions/neighborhoods on photos.

## Images (original, AI-generated, trade-literacy audited — 6/6 PASS)
- `images/condenser.jpg` — tech at condenser, horizontal fins, top grille, blue/red gauges, copper lineset through sealed penetration, disconnect + whip, R-454B tank. PASS.
- `images/thermostat.jpg` — gloved hand at smart stat reading 72°F, snowflake icon, plantation shutters, ceiling fan. PASS.
- `images/attic.jpg` — headlamped tech at horizontal air handler, smooth flex-duct curves, mastic at connections, copper lineset, PVC condensate drain. PASS.
- `images/tech.jpg` — tech portrait, navy polo, unbranded badge, Tampa door, plain van. PASS.
- `images/before.jpg` — rusted condenser, bent fins. PASS.
- `images/after.jpg` — new condenser on fresh pad, insulated suction line, disconnect. PASS.

## QA results (qa.py — 70/70 PASS)
View-source facts (phone/email/license/prices/neighborhoods/hours/FAQPage/HVACBusiness), one H1, zero em dashes, 35/35 links non-empty, all images alt-tagged, all 4 inputs labeled, calculator math verified live (2,400 sq ft split → $6,500–$8,800; heat pump adds; mini-split flat), BA slider keyboard moves, contrast (flame 5.01, panic 6.51, body 17.14), desktop height 10046, mobile scrollWidth = 390 (no overflow), burger opens/closes, all tap targets ≥44px, mbar shows after hero / hides at final CTA, mobile header phone visible, JS-off facts all present, reveals complete with no interaction.

### Failures found and fixed
1. **app.js syntax error** (missing paren, line 5) — cascaded into calculator/slider/bar/menu failures; caught via `node --check`, fixed.
2. **Mobile header overflow** — brand + phone pill + burger pushed 8px past 390px; shrunk header contents at ≤560px, `flex:none` on burger/phone pill.
3. **Calc range wrapped mid-number** ("$5,900–" / "7,900") on desktop — `white-space:nowrap`.
4. **Stat numerals wrapped** ("same-"/"day") — `white-space:nowrap` on `.stat-n`.
5. **Mobile hero CTA wrapped the phone number** mid-number — stacked label over sub-label vertically.
6. QA false positives fixed: hidden mnav links measured as 0×0 tap targets (now visible-only); mbar-final check scrolled past the final section (now scrolls to it).

## Substitute QA (playbook: critique parked, claude.ai is the parent's step)
Screenshots staged at `~/workspace/goals/tampa-demo-first-cold-pitch/hidden_files/critique-2026-10-10/cool-comfort-desktop.png` and `cool-comfort-mobile.png`.

- **Five-question friend test (read cold):** (1) What am I buying? AC repair/replacement for Tampa homeowners — clear. (2) Where is the price? Giant range in the first viewport + from-prices on all six cards — clear. (3) Too long? The page is long, but it serves a considered purchase (replacement); the emergency path (doors strip → panic strip → sticky bar) never requires scrolling past the fold. Judged acceptable, not cut. (4) Why trust? Real license, real reviews, real specials, tech card — but the ★4.7/300+/2,400+ stats are placeholders, disclosed in footer and here. (5) Exit depth? Highest risk is the money section for emergency visitors — mitigated by the panic strip and sticky bar sitting above it.
- **Blur pass (hero):** first fixation = headline + giant price figure as one dominant blob (the concept's intent: the number IS the headline's partner), second fixation = flame CTA pill. Pass with the noted intent.
- **Read-aloud test:** every headline read aloud once; all pass as spoken sentences ("AC out? Cool again by tonight." / "Fix it, tune it, or swap it." / "5 signs your AC is dying" / "500-micron vacuum. Every single install." / "Hot house? Cold answer: call."). Em-dash constructions rewritten into spoken sentences during the pass.
- **Redesign subtraction audit** (functional inventory, all present): phone (doors, header, hero, panic, sticky bar, footer — every one a direct `tel:`), email (`mailto:` in header, form section, footer), services path (vocab nav + bento + FAQ), trust line under hero CTAs, from-prices, estimate form with named handoff, two-tier service areas, FAQ. Nothing subtracted.

## Watch items / open
- **Design-critique step (claude.ai) NOT done**: generic subagents cannot operate the live browser. Clean staged screenshots are at the critique-2026-10-10 paths above — needs a parent-delegated browser task: upload both to claude.ai (signed-in profile), ask for blunt design criticism + a trade-literacy photo check, record verbatim, fix real points, re-screenshot.
- Phone settled to 813-680-5348 (verified against their site + permit record 2026-10-10).
