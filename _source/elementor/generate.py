"""Write Elementor import files to elementor/dist/.

python3 elementor/generate.py [--media-month 2026/11]

--media-month is the WordPress uploads folder (year/month) the four files in
dist/media/ were uploaded to. Elementor fetches images by URL on import.
"""
import argparse
import json
import shutil
from pathlib import Path

from lib import (BODY, CORAL, HEAD, INK, LINE, MUTED, PAPER, RED, RED_TINT, SOFT, TEXT, WHITE, badge, box, btn, con, eid,
                 eyebrow, faq, gap, grid, h, html, icon_val, img, link, px, section, seed, tabs, template, ticks, txt, typ,
                 widget)

HERE = Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument("--media-month", default="2026/11")
args = ap.parse_args()

UP = "https://theautodoorexperts.com.au/wp-content/uploads/"
THUMB = UP + "elementor/thumbs/"
MEDIA = UP + args.media_month + "/"
I = {
    "logo": UP + "2025/12/Logo-Footer.png",
    "city": THUMB + "10-rjfx8u41yedmwyhwqmwhw4meqz3e6d0sku8ui2yedc.webp",
    "warehouse": UP + "2026/02/6-768x480.webp",
    "hotel": THUMB + "7-rjfx2in40hq8vbobmwks4q0uzq8kflxr1kdcd4bo74.webp",
    "tech": THUMB + "2-rjfx77u26o5ux4uk6xpmljbtx32mx4lfotsqqxct34.webp",
    "handshake": THUMB + "9-rjfx5pbf6a387r1r1a59kx33gqjciol05bykwvln40.webp",
    "pharmacy": THUMB + "store-rjkdrpv7e58djsck4l8bduijnrpxbms73nfbo2js5c.webp",
    "office": UP + "2026/01/work-done-687x1024.jpg",
    "public": THUMB + "doors-rhx8d6ajhfx101iw0u2s2f372cefbb7cygypyh17i8.jpg",
    "health": MEDIA + "ind-healthcare.jpg",
    "aged": MEDIA + "ind-agedcare.jpg",
    "shop": MEDIA + "ind-shopping.jpg",
    "service": MEDIA + "svc-maintenance.jpg",
}
PHONE = "1300 829 998"
TEL = "tel:1300829998"
FORM_TITLE = "Auto Door Quote"
QUOTE = "/contact-us/?service={}#quote"

INDUSTRIES = [
    ("hospitals", "Hospitals & medical", "fa-hospital", "health", "Wide automatic sliding entrance at a medical centre",
     "Patient access can't wait for a repair.",
     "Touch points spread infection, and beds need wide, reliable openings.",
     ["Touchless activation", "Wide clearances for beds and wheelchairs", "Priority 24/7 response"]),
    ("aged-care", "Aged care", "fa-hand-holding-heart", "aged", "Automatic sliding doors at an aged care facility",
     "Residents move slowly. Their doors should too.",
     "Standard settings close too soon on walkers and wheelchairs.",
     ["Slower, gentler operation", "Longer hold-open, wider detection", "Disability access and NDIS compliant"]),
    ("retail-centres", "Shopping centres", "fa-shopping-cart", "shop", "Shopping centre entrance with automatic sliding doors",
     "A broken entrance on a Saturday stops trade.",
     "Thousands of cycles a week wear belts and sensors fast.",
     ["Heavy-duty, high-cycle operators", "Telescopic doors for maximum width", "Bi-annual service plans"]),
    ("pharmacies", "Pharmacies", "fa-pills", "pharmacy", "Technicians installing an automatic sliding door at a pharmacy",
     "Busy all day, secure all night.",
     "Constant use by day, and locking that must work every night.",
     ["Fast, touchless sliding doors", "Secure after-hours locking", "Keypads and access control"]),
    ("warehouses", "Warehouses", "fa-warehouse", "warehouse", "Automatic sliding personnel door on a warehouse building",
     "Retail-grade doors don't survive forklifts.",
     "Dust, heat and pallet traffic wreck shopfront operators.",
     ["Industrial-rated operators", "Dust-protected sensors", "Heavy-duty tracks"]),
    ("hotels", "Hotels", "fa-concierge-bell", "hotel", "Frameless automatic sliding doors opening into a hotel lobby",
     "Your entrance is the first impression.",
     "A noisy, juddering door makes a beautiful lobby feel cheap.",
     ["Frameless glass, slim operators", "Quiet, smooth operation", "Finishes matched to your property"]),
    ("offices", "Offices & retail", "fa-building", "office", "Technicians handing over a new entrance at an office building",
     "Professional entrances, sensible budgets.",
     "You need reliability without paying for heavy-duty kit.",
     ["Cost-effective sliding and swing", "Retrofits for existing doors", "Fit-out coordination"]),
    ("government", "Government & NDIS", "fa-landmark", "public", "Automatic doors on public building frontages",
     "Accessible for everyone, audit-ready every time.",
     "Accessibility obligations and regular compliance audits.",
     ["AS 5007 compliant installs", "NDIS and disability access", "Written service records"]),
]


def label(text, color=RED, mb=6):
    return h(text.upper(), "p", (11.8, None, None), color, 600, BODY, 1, 1.4, mb=mb)


def quote_section():
    side = con(
        eyebrow("Free site inspection & quote", "#FF8C8F"),
        h("Tell us what's happening.", color=WHITE),
        txt("The right team gets your request straight away and calls you back.", (17, None, None), SOFT, mt=20, mb=40, max_w=360),
        con(badge("fa-phone-alt", "rgba(255,255,255,0.16)", WHITE, 52, 20, 26),
            con(txt("Door stuck right now? Call 24/7", (14, None, None), WHITE, 1.3),
                h(PHONE, "p", (32, 28, 26), WHITE, 800, HEAD, 1.1, -0.3)),
            row=True, gp=16, pad=box(18, 20), bg=RED, radius=22, align="center", href=TEL, cls="ade-callblock"),
        con(txt("Open 24 hours, 7 days", (15.5, None, None), SOFT),
            txt("Prestons NSW · Australia-wide", (15.5, None, None), SOFT), gp=6, pad=box(28, 0, 0, 0)),
        w=(38, 100, 100))
    form = con(widget("shortcode", {"shortcode": f'[contact-form-7 title="{FORM_TITLE}"]'}),
               bg=WHITE, radius=22, pad=(48, 36, box(32, 22)), cls="ade-formcard",
               w=(54, 100, 100))
    return section(con(side, form, row=True, dirs=("column", "column"), gp=(0, 48, 40), justify="space-between", align="flex-start"),
                   bg=INK, anchor="quote")


def page_hero(crumb, kicker, title, lead, media, alt, buttons=(), dark=False):
    bg, fg, sub = (INK, WHITE, SOFT) if dark else (PAPER, INK, MUTED)
    copy = con(
        txt(f'<p><a href="/">Home</a> &nbsp;/&nbsp; {crumb}</p>', (13.8, None, None), sub, cls="ade-crumbs", mb=20),
        eyebrow(kicker, "#FF8C8F" if dark else RED),
        h(title, "h1", (56, 44, 34), fg, 800, HEAD, 1.04, -1.2),
        txt(lead, (18.5, 17.5, 17), sub, mt=24, max_w=460),
        *buttons, w=(52, 100, 100), justify="center")
    pic = con(img(media, alt, (480, 440, 280), 22), w=(42, 100, 100))
    return section(con(copy, pic, row=True, dirs=("column", "column"), gp=(0, 36, 32), justify="space-between", align="center"),
                   bg=bg, pad=(96, 72, 56))


def btn_row(*bs, top=40):
    return con(*bs, row=True, gp=12, wrap=True, pad=box(top, 0, 0, 0), dirs=(None, "row"))


def head(kicker, title, intro=None):
    left = con(eyebrow(kicker), h(title), w=(56, 100, 100))
    if not intro:
        return con(left, pad=box(0, 0, 72, 0), extra={"padding_mobile": box(0, 0, 44, 0)})
    return con(left, con(txt(intro, (17, None, None), MUTED), w=(36, 100, 100)), row=True, dirs=("column", "column"),
               gp=(0, 16, 16), justify="space-between", align=("flex-end", "flex-start", "flex-start"),
               pad=box(0, 0, 72, 0), extra={"padding_mobile": box(0, 0, 44, 0)})


def card(fa, title, text=None, href=None, size=(19, None, None)):
    kids = [badge(fa), h(title, "h3", size, INK, 700, HEAD, 1.3, 0, mt=20)]
    if text:
        kids.append(txt(text, (16, None, None), MUTED, mt=8))
    return con(*kids, pad=box(36, 28), bg=WHITE, border=LINE, radius=22, href=href, cls="ade-card" + (" ade-lift" if href else ""))


def post_grid(count, cols=3, pagination=False):
    s = {"query_source": "post", "query_posts_per_page": count, "layout_select": "fitRows",
         "layout_columns": str(cols), "layout_columns_tablet": "2", "layout_columns_mobile": "1",
         "layout_gutter_hr": px(28), "layout_gutter_vr": px(44), "layout_filters": "",
         "layout_pagination": "yes" if pagination else "", "_css_classes": "ade-postgrid",
         "grid_elements": [{"_id": eid(), "element_select": "title", "element_location": "below", "element_display": "block", "element_title_tag": "h3"},
                           {"_id": eid(), "element_select": "date", "element_location": "below", "element_display": "block"}]}
    return widget("wpr-grid", s)


def faq_section(kicker, title, items, bg=None):
    return section(con(con(eyebrow(kicker), h(title), w=(36, 100, 100)), con(faq(items), w=(56, 100, 100)), row=True,
                       dirs=("column", "column"), gp=(0, 32, 32), justify="space-between"), bg=bg)


def case_section(text, title, buttons):
    return section(
        con(con(eyebrow("Case study · Prestons, NSW", "#FF8C8F"),
                widget("counter", {"starting_number": 0, "ending_number": 80, "suffix": "%", "duration": 1200,
                                   "thousand_separator": "", "number_color": CORAL, "_css_classes": "ade-counter",
                                   **typ((150, 120, 96), 800, HEAD, 0.9, -5, prefix="typography_number")}),
                h(title, size=(32, 28, 23), color=WHITE, weight=700, lh=1.2, ls=-0.4, mt=12), w=(52, 100, 100)),
            con(txt(text, (18, 17.5, 17), SOFT, 1.7), btn_row(*buttons, top=32), w=(38, 100, 100)),
            row=True, dirs=("column", "column"), gp=(0, 40, 32), justify="space-between", align="center"),
        bg=INK)


# ------------------------------------------------------------------ pages
def page_home():
    intents = [
        ("fa-exclamation-triangle", "My door stopped working", "/emergency-breakdown-service/", True),
        ("fa-door-open", "Install a new door", QUOTE.format("New%20door"), False),
        ("fa-calendar-check", "Book maintenance", QUOTE.format("Maintenance"), False),
        ("fa-cog", "Find a spare part", QUOTE.format("Spare%20parts"), False),
    ]
    cards = []
    for fa, t, url, alert in intents:
        cards.append(con(badge(fa, RED if alert else PAPER, WHITE if alert else INK, 44, 18, 12),
                         h(t, "p", (15.5, None, None), INK, 600, BODY, 1.25, 0, cls="ade-intent__t"),
                         row=True, gp=12, align="center", pad=box(14), bg=RED_TINT if alert else WHITE,
                         border="#F0B7B5" if alert else LINE, radius=14, href=url, cls="ade-intent ade-lift", min_h=72,
                         extra={"flex_direction_mobile": "row"}))
    copy = con(eyebrow("Automatic door specialists"),
               h(f'Automatic doors that keep your business <span style="color:{RED}">moving</span>.', "h1", (66, 50, 37), INK, 800, HEAD, 1.04, -1.6),
               txt("Installation, 24/7 repairs and maintenance for commercial buildings across Australia.", (18.5, 17.5, 17), MUTED, mt=24, mb=40, max_w=460),
               grid(*cards, cols=(2, 2, 1), gp=12), w=(52, 100, 100), justify="center")
    door = con(img(I["city"], "Automatic sliding glass doors on a city street frontage", (620, 560, 400)),
               html('<span class="ade-pane ade-pane--l"></span><span class="ade-pane ade-pane--r"></span>', "ade-panes"),
               cls="ade-door", bg=INK, radius=22)
    call = con(txt("Breakdown line open now", (12.5, None, None), MUTED, 1.2),
               h(PHONE, "p", (19, None, None), INK, 800, HEAD, 1.1, 0), href=TEL, bg=WHITE, radius=14, pad=box(12, 18),
               cls="ade-float", shadow=True)
    media = con(door, call, w=(42, 100, 100), cls="ade-heromedia")
    proof = grid(*[con(badge(fa, "transparent", RED, 28, 22, 0),
                       txt(f"<p><strong>{a}</strong><br>{b}</p>", (14.5, None, None), MUTED, 1.35, cls="ade-proof__t"),
                       row=True, gp=12, align="center", pad=box(22, 20), bg=WHITE, extra={"flex_direction_mobile": "row"})
                   for fa, a, b in [("fa-clock", "24/7", "breakdown service"), ("fa-shield-alt", "AS 5007", "compliant"),
                                    ("fa-truck", "Australia-wide", "coverage"), ("fa-file-alt", "Free", "site inspection")]],
                 cols=(4, 2, 2), gp=1, cls="ade-proof")
    hero = section(con(copy, media, row=True, dirs=("column", "column"), gp=(0, 44, 40), justify="space-between", align="center"),
                   con(proof, pad=(box(96, 0, 0, 0), box(64, 0, 0, 0), box(48, 0, 0, 0))),
                   bg=PAPER, pad=(96, 72, 48))

    panels = []
    for slug, name, fa, key, alt, title, prob, tk in INDUSTRIES:
        body = con(h(title, "h3", (23, 21, 20), INK, 700, HEAD, 1.25, 0),
                   con(label("The problem"), txt(prob, (16, None, None), MUTED, 1.55), pad=box(24, 0)),
                   ticks(tk),
                   btn(f"More on {name.lower()}", f"/industries/#{slug}", "ghost", "fa-arrow-right", cls="ade-more"),
                   w=(58, 100, 100), pad=(box(52, 48), box(36, 32), box(32, 26)), justify="center", gp=4)
        pic = con(img(I[key], alt, (500, 340, 220)), w=(42, 100, 100))
        panels.append((name, fa, con(pic, body, row=True, dirs=("column", "column"), bg=WHITE, border=LINE, radius=22,
                                     shadow=True, cls="ade-panel", title=name)))
    industries = section(head("Industries", "Every building has a different door problem.", "Pick yours to see what goes wrong, and how we fix it."),
                         tabs(panels))

    svc = [("fa-exclamation-triangle", "Emergency Breakdown", "Stuck open or shut? We answer 24/7.", "Get help now", "/emergency-breakdown-service/", True),
           ("fa-door-open", "Sales & Installation", "Sliding, swing and retrofit doors.", "Learn more", "/sales-and-installation/", False),
           ("fa-calendar-check", "Maintenance", "Planned servicing that prevents failures.", "Learn more", "/periodic-maintenance/", False),
           ("fa-cog", "Spare Parts", "Sensors, belts, motors and more.", "Learn more", "/spare-parts/", False)]
    svc_cards = []
    for fa, t, d, cta, url, dark in svc:
        svc_cards.append(con(badge(fa, RED if dark else PAPER, WHITE if dark else INK, 52, 22, 14),
                             h(t, "h3", (22, 21, 20), WHITE if dark else INK, 700, HEAD, 1.25, 0, mt=20),
                             txt(d, (16, None, None), "#B9BEC6" if dark else MUTED, mt=10, mb=18),
                             h(f"{cta} →", "p", (15.5, None, None), "#FF8C8F" if dark else RED, 600, BODY, 1.2, 0),
                             pad=box(36, 28), bg=INK if dark else WHITE, border=INK if dark else LINE, radius=22, href=url, cls="ade-lift",
                             justify="flex-start"))
    services = section(head("What we do", "One team for the whole life of your door."), grid(*svc_cards), bg=PAPER)

    case = case_section("A busy retail centre was calling us out every month. Two planned visits a year changed that: worn parts now get replaced before they fail.",
                        "fewer emergency callouts after switching to a bi-annual service plan.",
                        [btn("See maintenance plans", "/periodic-maintenance/"),
                         btn("Read the story", "/how-a-prestons-retail-centre-automatic-door-maintenance/", "light")])
    faqs = faq_section("FAQs", "Straight answers.", [
        ("Are your doors compliant with Australian Standards?", "Yes. Every door we install or service is checked against AS 5007, with a written report for your records."),
        ("Can you automate the doors we already have?", "Often, yes. Retrofit operators can be added to existing swing or sliding doors after a site inspection."),
        ("How often should automatic doors be serviced?", "Twice a year for most commercial sites: once before summer, once before winter."),
        ("Do you service doors you didn't install?", "Yes. We repair, service and supply parts for most automatic doors."),
    ])
    blog = section(con(con(eyebrow("From the blog"), h("Know your doors."), w=(60, 100, 100)),
                       btn("All articles", "/blog/", "ghost", "fa-arrow-right"), row=True, dirs=(None, "column"), justify="space-between",
                       align=("flex-end", None, "flex-start"), gp=(0, None, 20), pad=box(0, 0, 56, 0)),
                   post_grid(3), bg=PAPER)
    return [hero, industries, services, case, faqs, blog, quote_section()]


def page_emergency():
    return [
        page_hero("Emergency Breakdown", "On call 24/7", f'Door stuck? <span style="color:{CORAL}">We\'re on our way.</span>',
                  "One call gets a technician and a fully stocked van heading to you.", I["tech"],
                  "Technician repairing the operator on an automatic sliding door",
                  [con(con(badge("fa-phone-alt", "rgba(255,255,255,0.18)", WHITE, 52, 20, 26),
                           con(txt("Tap to call, day or night", (13.5, None, None), WHITE, 1.3),
                               h(PHONE, "p", (32, 28, 26), WHITE, 800, HEAD, 1.05, 0)),
                           row=True, gp=16, align="center", pad=box(16, 28, 16, 16), bg=RED, radius=999, href=TEL,
                           extra={"flex_direction_mobile": "row"}, cls="ade-callblock ade-fit"),
                       row=True, pad=box(32, 0, 0, 0), extra={"flex_direction_mobile": "row"})], dark=True),
        section(head("What we fix", "If it's powered and it's a door, we can get it moving."),
                grid(card("fa-door-closed", "Stuck open or closed"), card("fa-hand-paper", "Sensor faults"),
                     card("fa-cog", "Motor or control board"), card("fa-bolt", "Power or access systems"))),
        section(head("How it works", 'From "it\'s broken" to "it\'s fixed".'),
                grid(*[step(n, t, d) for n, t, d in [("01", "Call us", "Tell a technician what the door is doing."),
                                                     ("02", "We dispatch", "A stocked van heads to your site."),
                                                     ("03", "Safe, then fixed", "Made safe first, then repaired.")]], cols=(3, 3, 1)),
                bg=PAPER),
        section(con(con(eyebrow("While you wait"), h("Keep people clear. Don't force the panels."),
                        txt("Forcing a stuck door can damage the belt and motor. If you can, snap a photo of what it's doing.", mt=24), w=(50, 100, 100)),
                    con(label("Stop it happening again", mb=10),
                        h("One retail centre cut callouts by 80% with two planned services a year.", "p", (21, None, 19), INK, 700, HEAD, 1.35, 0, mb=24),
                        btn("See maintenance plans", "/periodic-maintenance/", "ghost", "fa-arrow-right"),
                        pad=box(40, 36), bg=PAPER, radius=22, w=(40, 100, 100)),
                    row=True, dirs=("column", "column"), gp=(0, 36, 32), justify="space-between", align="center")),
        quote_section(),
    ]


def step(n, title, text=None):
    kids = [widget("heading", {"title": n, "header_size": "span", "title_color": RED, "_css_classes": "ade-stepn",
                               **typ(15, 800, HEAD, 1)}), h(title, "h3", (18, None, None), INK, 700, HEAD, 1.3, 0, mt=18)]
    if text:
        kids.append(txt(text, (16, None, None), MUTED, mt=8))
    return con(*kids, pad=box(36, 28), bg=WHITE, border=LINE, radius=22)


SVG_SLIDE = '<svg class="ade-art" viewBox="0 0 220 140" aria-hidden="true"><rect x="20" y="14" width="180" height="16" rx="3" fill="#14171C"/><rect x="20" y="30" width="180" height="100" fill="none" stroke="#14171C" stroke-width="3"/><rect x="24" y="34" width="52" height="96" fill="rgba(140,170,195,.28)" stroke="#6d7d8b" stroke-width="2"/><rect x="144" y="34" width="52" height="96" fill="rgba(140,170,195,.28)" stroke="#6d7d8b" stroke-width="2"/><path d="M96 82h-14m0 0 6-6m-6 6 6 6M124 82h14m0 0-6-6m6 6-6 6" fill="none" stroke="#D7191F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_SWING = '<svg class="ade-art" viewBox="0 0 220 140" aria-hidden="true"><rect x="40" y="14" width="140" height="16" rx="3" fill="#14171C"/><rect x="40" y="30" width="140" height="100" fill="none" stroke="#14171C" stroke-width="3"/><path d="M44 34 L112 46 L112 122 L44 130 Z" fill="rgba(140,170,195,.28)" stroke="#6d7d8b" stroke-width="2"/><path d="M60 22 L100 38" stroke="#14171C" stroke-width="4" stroke-linecap="round"/><path d="M150 112a38 38 0 0 0-30-34" fill="none" stroke="#D7191F" stroke-width="3" stroke-linecap="round" stroke-dasharray="4 4"/></svg>'
SVG_RETRO = '<svg class="ade-art" viewBox="0 0 220 140" aria-hidden="true"><rect x="60" y="30" width="100" height="100" fill="none" stroke="#14171C" stroke-width="3"/><rect x="64" y="34" width="92" height="96" fill="#E8DDCB" stroke="#9C8B70" stroke-width="2"/><rect x="70" y="8" width="80" height="16" rx="3" fill="#14171C"/><circle cx="146" cy="84" r="3" fill="#9C8B70"/><path d="M176 60h20M186 50v20" fill="none" stroke="#D7191F" stroke-width="3" stroke-linecap="round"/></svg>'


def page_sales():
    types = [(SVG_SLIDE, "Sliding", "Quiet and space-efficient. Single, bi-parting or telescopic."),
             (SVG_SWING, "Swing", "For spaces where sliding panels won't fit."),
             (SVG_RETRO, "Retrofit", "Automate the doors you already have.")]
    return [
        page_hero("Sales & Installation", "Sales & installation", f'The right door, <span style="color:{RED}">installed right.</span>',
                  "Sliding, swing and retrofit doors, specified for how your entrance is actually used.", I["handshake"],
                  "Technicians handing over a new automatic entrance to a client",
                  [btn_row(btn("Book a free inspection", "#quote", big=True), btn(PHONE, TEL, "ghost", "fa-phone-alt", big=True))]),
        section(head("Door systems", "Three ways in."),
                grid(*[con(html(s, "ade-artwrap"), h(t, "h3", (23, None, 21), INK, 700, HEAD, 1.25, 0, mt=20), txt(d, (16, None, None), MUTED, mt=10),
                           pad=box(36, 32), border=LINE, radius=22) for s, t, d in types], cols=(3, 1, 1))),
        section(head("Process", "Four steps, no surprises."),
                grid(*[step(n, t) for n, t in [("01", "Free site inspection"), ("02", "Clear written quote"),
                                               ("03", "Precision installation"), ("04", "Tested to AS 5007")]]), bg=PAPER),
        quote_section(),
    ]


def page_maintenance():
    checks = ["Safety inspection", "Sensor calibration", "Motor, belt & rollers", "Control diagnostics", "Lubrication & alignment", "AS 5007 report"]
    return [
        page_hero("Maintenance", "Periodic maintenance", f'Fewer breakdowns. <span style="color:{RED}">Fewer surprises.</span>',
                  "Planned servicing that keeps your doors safe, compliant and running.", I["service"],
                  "Technician completing an automatic door service report on a tablet",
                  [btn_row(btn("Get a maintenance quote", "#quote", big=True))]),
        section(con(con(eyebrow("Every visit"), h("A full health check, twice a year."), w=(44, 100, 100)),
                    grid(ticks(checks[:3], INK, RED, 17, 28), ticks(checks[3:], INK, RED, 17, 28), cols=(2, 2, 1), gp=(32, 32, 28), extra={"width": px(48, "%"), "width_tablet": px(100, "%"), "width_mobile": px(100, "%")}),
                    row=True, dirs=("column", "column"), gp=(0, 36, 32), justify="space-between")),
        case_section("Worn parts get replaced during planned downtime, not during peak trading.",
                     "fewer emergency callouts with two planned visits a year.",
                     [btn("Read the story", "/how-a-prestons-retail-centre-automatic-door-maintenance/", "light", "fa-arrow-right")]),
        faq_section("FAQs", "About servicing.", [
            ("How often should doors be serviced?", "Twice a year for most sites. Very busy entrances may need quarterly checks."),
            ("How long does a visit take?", "Usually 45 minutes to 1.5 hours per door. We can come off-peak or before opening."),
            ("Will I get a record for compliance?", "Yes, a written condition report after every visit."),
            ("Is it worth it for one or two doors?", "Yes. One emergency callout often costs more than a year of servicing."),
        ]),
        quote_section(),
    ]


def page_parts():
    parts = ["Sliding door operators", "Swing door operators", "Control boards", "Motion & safety sensors",
             "Rollers, belts & motors", "Keypads & access control", "Locks and arms", "Mechanical accessories"]
    rows = [con(widget("heading", {"title": f"{i:02d}", "header_size": "span", "title_color": RED, "_css_classes": "ade-stepn", **typ(14.5, 800, HEAD, 1)}),
                h(p, "p", (16.5, None, None), INK, 600, BODY, 1.3, 0),
                row=True, gp=14, align="center", pad=box(18, 20), border=LINE, radius=14, bg=WHITE, extra={"flex_direction_mobile": "row"})
            for i, p in enumerate(parts, 1)]
    return [
        page_hero("Spare Parts", "Spare parts", f'The right part, <span style="color:{RED}">no guesswork.</span>',
                  "Don't know the part number? Send a photo and we'll identify it.", I["pharmacy"],
                  "Technicians fitting a replacement part to an automatic sliding door",
                  [btn_row(btn("Send a photo", "#quote", big=True))]),
        section(head("We supply", "Everything that makes the door move."), grid(*rows, cols=(2, 2, 1), gp=12)),
        quote_section(),
    ]


def page_industries():
    jumps = [btn(n, f"#{s}", "ghost", cls="ade-chip") for s, n, *_ in INDUSTRIES]
    top = section(txt('<p><a href="/">Home</a> &nbsp;/&nbsp; Industries</p>', (13.8, None, None), MUTED, cls="ade-crumbs", mb=20),
                  eyebrow("Industries"),
                  h(f'The right door depends on <span style="color:{RED}">who uses it.</span>', "h1", (56, 44, 34), INK, 800, HEAD, 1.04, -1.2, cls="ade-narrow"),
                  con(*jumps, row=True, wrap=True, gp=8, pad=box(36, 0, 0, 0), extra={"flex_direction_mobile": "row"}),
                  bg=PAPER, pad=(96, 72, 56))
    rows = []
    for i, (slug, name, fa, key, alt, title, prob, tk) in enumerate(INDUSTRIES):
        pic = con(img(I[key], alt, (460, 420, 260), 22), w=(46, 100, 100))
        body = con(h(name, "p", (15.5, None, None), RED, 600, BODY, 1.2, 0, mb=12), h(title),
                   txt(prob, (17.5, None, None), MUTED, mt=24, mb=28, max_w=430), ticks(tk, size=16.5),
                   con(btn("Book a free site assessment", QUOTE.format("New%20door"), "ghost", "fa-arrow-right"), pad=box(32, 0, 0, 0), row=True, extra={"flex_direction_mobile": "row"}),
                   w=(44, 100, 100))
        kids = [pic, body] if i % 2 == 0 else [body, pic]
        rows.append(con(*kids, row=True, dirs=("column", "column"), gp=(0, 32, 28), justify="space-between", align="center",
                        anchor=slug, pad=(box(112, 0), box(72, 0), box(56, 0)), cls="ade-irow"))
    return [top, section(*rows, pad=(40, 24, 16)), quote_section()]


def page_about():
    return [
        page_hero("About", "Australian owned & operated", f'Automatic doors are <span style="color:{RED}">all we do.</span>',
                  "Swing and sliding door specialists focused on safety, accessibility and reliable performance.", I["office"],
                  "Technicians meeting a client outside a completed entrance"),
        section(head("Our promise", "Quality work at a fair price."),
                grid(card("fa-bolt", "Competitive value", "Quality systems, honestly priced."),
                     card("fa-shield-alt", "Trusted technicians", "Proven people, prompt service."),
                     card("fa-cog", "Full-spectrum service", "Sales to servicing, any brand."), cols=(3, 3, 1))),
        section(con(con(img(I["tech"], "Technician adjusting an automatic sliding door operator", (520, 460, 300), 22), w=(46, 100, 100)),
                    con(eyebrow("How we work"), h("We start with how your door is used."),
                        txt("Who walks through it, how often, and what happens if it stops. That's how we pick the right system.", mt=24),
                        btn_row(btn("Book a free inspection", "/contact-us/#quote")), w=(44, 100, 100)),
                    row=True, dirs=("column", "column"), gp=(0, 36, 32), justify="space-between", align="center"), bg=PAPER),
        quote_section(),
    ]


def page_contact():
    def c(fa, t, line, url, alert=False):
        return con(badge(fa, "rgba(255,255,255,0.18)" if alert else RED_TINT, WHITE if alert else RED),
                   h(t, "h2", (18, None, None), WHITE if alert else INK, 700, HEAD, 1.3, 0, mt=20),
                   txt(line, (15, None, None), WHITE if alert else MUTED, 1.4, mt=8, cls="ade-breakword"),
                   pad=box(32, 28), bg=RED if alert else WHITE, border=RED if alert else LINE, radius=22, href=url, cls="ade-lift")
    return [
        section(txt('<p><a href="/">Home</a> &nbsp;/&nbsp; Contact</p>', (13.8, None, None), MUTED, cls="ade-crumbs", mb=20),
                eyebrow("Contact"),
                h(f'Let\'s get your doors <span style="color:{RED}">sorted.</span>', "h1", (56, 44, 34), INK, 800, HEAD, 1.04, -1.2, cls="ade-narrow", mb=56),
                grid(c("fa-exclamation-triangle", "Emergency, 24/7", PHONE, TEL, True),
                     c("fa-door-open", "Sales & installation", "sales@theautodoorexperts.com.au", "mailto:sales@theautodoorexperts.com.au"),
                     c("fa-calendar-check", "Maintenance", "maintenance@theautodoorexperts.com.au", "mailto:maintenance@theautodoorexperts.com.au"),
                     c("fa-cog", "Spare parts", "spareparts@theautodoorexperts.com.au", "mailto:spareparts@theautodoorexperts.com.au"),
                     cols=(2, 2, 1)),
                bg=PAPER, pad=(96, 72, 56)),
        quote_section(),
        section(widget("google_maps", {"address": "Prestons NSW 2170", "zoom": px(12), "height": px(360)}), pad=(72, 56, 48)),
    ]


def page_blog():
    return [
        section(eyebrow("Blog"),
                h(f'Know your <span style="color:{RED}">doors.</span>', "h1", (56, 44, 34), INK, 800, HEAD, 1.04, -1.2),
                txt("Practical guides from the technicians who fix them.", mt=24), bg=PAPER, pad=(96, 72, 56)),
        section(post_grid(12, pagination=True)),
        quote_section(),
    ]


def tpl_single():
    meta = widget("wpr-post-info", {"post_info_layout": "horizontal", "post_info_elements": [{"_id": eid(), "post_info_select": "date"}], "_css_classes": "ade-postmeta"})
    aside = con(html('<nav class="ade-toc" aria-label="On this page"></nav>', "ade-tocwrap"),
                con(h("Door playing up?", "p", (19, None, None), WHITE, 700, HEAD, 1.2, 0),
                    txt("Talk to a technician, 24/7.", (15.5, None, None), SOFT, mb=12, mt=8),
                    btn(PHONE, TEL, "red", "fa-phone-alt", full=True),
                    pad=box(28, 24), bg=INK, radius=14, gp=4),
                w=(26, 100, 100), gp=24, cls="ade-aside")
    return [
        section(widget("wpr-post-title", {"post_title_tag": "h1", "_css_classes": "ade-posttitle", "title_color": INK}),
                meta, bg=PAPER, pad=(88, 64, 48), gp=16, cls="ade-posthead"),
        section(con(widget("wpr-post-media", {"featured_media_image_crop_size": "full", "_css_classes": "ade-postmedia"}),
                    pad=box(0, 0, 0, 0)), pad=(0, 0, 0)),
        section(con(con(widget("wpr-post-content", {"_css_classes": "ade-prose"}), w=(66, 100, 100)), aside, row=True,
                    dirs=("column", "column"), gp=(0, 48, 40), justify="space-between", align="flex-start"), pad=(88, 64, 56)),
        section(con(h("Keep reading."), btn("All articles", "/blog/", "ghost", "fa-arrow-right"), row=True, dirs=(None, "column"),
                    justify="space-between", align=("flex-end", None, "flex-start"), gp=(0, None, 20), pad=box(0, 0, 56, 0)),
                post_grid(3), bg=PAPER),
        quote_section(),
    ]


def tpl_header():
    top = con(con(txt(f'<p><span class="ade-dot"></span><strong>24/7 breakdown line</strong><span class="ade-hide-m"> · AS 5007 compliant · Australia-wide</span></p>',
                      (13.5, None, None), "#D9DCE1", 1.2, cls="ade-toptxt"),
                  h(f'<a href="{TEL}">{PHONE}</a>', "p", (13.5, None, None), WHITE, 600, BODY, 1.2, 0, cls="ade-topcall"),
                  row=True, justify="space-between", align="center", pad=box(10, 32), extra={"padding_mobile": box(10, 20), "flex_direction_mobile": "row"},
                  cls="ade-wrap"),
              bg=INK)
    nav = widget("wpr-nav-menu", {"menu_layout": "horizontal", "menu_align": "right", "menu_item_color": INK, "menu_item_color_hover": RED,
                                  "pointer_color_hover": RED, "menu_items_pointer": "none", "mob_menu_display": "tablet", "toggle_btn_color": INK,
                                  "_css_classes": "ade-nav", **typ(15.5, 500, BODY, 1.2, prefix="menu_items_typography")})
    bar = con(img(I["logo"], "The Auto Door Experts", width=88, unit="px", href="/", cls="ade-logo"),
              con(nav, grow=True, row=True, justify="flex-end", align="center", extra={"flex_direction_mobile": "row"}, cls="ade-navwrap"),
              con(btn(PHONE, TEL, "ghost", "fa-phone-alt", cls="ade-hide-t"), btn("Free site inspection", "/contact-us/#quote", cls="ade-hide-m"),
                  row=True, gp=10, align="center", extra={"flex_direction_mobile": "row", "_flex_size": "none"}),
              row=True, gp=(24, 16, 10), align="center", pad=(box(12, 32), box(10, 32), box(8, 20)), bg=WHITE,
              extra={"flex_direction_mobile": "row", "flex_direction_tablet": "row"}, cls="ade-wrap")
    root = con(top, bar, inner=False, extra={"enable_sticky_section": "yes", "position_type": "sticky", "position_location": "top",
                                             "z_index": 40}, cls="ade-header")
    return [root]


def tpl_footer():
    col = lambda t, *rows: con(h(t.upper(), "p", (12.5, None, None), WHITE, 600, BODY, 1.2, 1.4, mb=18),
                               txt("".join(f'<p><a href="{u}">{n}</a></p>' for n, u in rows), (15.5, None, None), "#A9AFB8", 1.4, cls="ade-footlinks"))
    grid_ = grid(
        con(img(I["logo"], "The Auto Door Experts", width=120, unit="px", cls="ade-footlogo"),
            txt("Automatic sliding and swing door specialists. Australian owned and operated.", (15, None, None), "#A9AFB8", 1.6, mt=16, max_w=280)),
        col("Services", ("Emergency Breakdown", "/emergency-breakdown-service/"), ("Sales & Installation", "/sales-and-installation/"),
            ("Maintenance", "/periodic-maintenance/"), ("Spare Parts", "/spare-parts/")),
        col("Company", ("Industries", "/industries/"), ("About", "/about-us/"), ("Blog", "/blog/"), ("Contact", "/contact-us/")),
        col("Contact", (PHONE, TEL), ("sales@theautodoorexperts.com.au", "mailto:sales@theautodoorexperts.com.au"), ("Prestons NSW 2170", "#")),
        cols=(4, 2, 1), gp=(40, 40, 32), cls="ade-footgrid")
    base = con(txt("<p>© 2026 The Auto Door Experts</p>", (13.5, None, None), "#A9AFB8"),
               txt('<p><a href="/privacy-policy/">Privacy</a> · <a href="/terms-conditions/">Terms</a> · Not associated with ADIS.</p>', (13.5, None, None), "#A9AFB8", cls="ade-footlinks"),
               row=True, wrap=True, justify="space-between", gp=8, pad=box(24, 0, 0, 0), extra={"border_border": "solid", "border_width": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False}, "border_color": "rgba(255,255,255,0.08)", "margin": box(64, 0, 0, 0), "flex_direction_mobile": "column"})
    snippet = html((HERE / "src/footer-snippet.html").read_text(), "ade-snippet")
    return [section(grid_, base, snippet, bg="#0E1014", pad=(80, 64, 56))]


PAGES = {
    "01-home": ("ADE Home", page_home), "02-emergency-breakdown": ("ADE Emergency Breakdown", page_emergency),
    "03-sales-installation": ("ADE Sales & Installation", page_sales), "04-periodic-maintenance": ("ADE Periodic Maintenance", page_maintenance),
    "05-spare-parts": ("ADE Spare Parts", page_parts), "06-industries": ("ADE Industries", page_industries),
    "07-about": ("ADE About", page_about), "08-contact": ("ADE Contact", page_contact), "09-blog": ("ADE Blog", page_blog),
}
PARTS = {"10-header": ("ADE Header", tpl_header), "11-footer": ("ADE Footer", tpl_footer), "12-single-post": ("ADE Single Post", tpl_single)}


def main():
    dist = HERE / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    (dist / "templates").mkdir(parents=True)
    (dist / "media").mkdir()
    for i, (slug, (title, fn)) in enumerate({**PAGES, **PARTS}.items()):
        seed(i + 100)
        kind = "page" if slug in PAGES else "section"
        data = template(title, fn(), kind)
        (dist / "templates" / f"{slug}.json").write_text(json.dumps(data, ensure_ascii=False))
    for name in ("ind-healthcare.jpg", "ind-agedcare.jpg", "ind-shopping.jpg", "svc-maintenance.jpg"):
        shutil.copy(HERE.parent.parent / "assets/img" / name, dist / "media" / name)
    shutil.copy(HERE / "src/global.css", dist / "global.css")
    shutil.copy(HERE / "src/cf7-form.txt", dist / "contact-form-7-setup.txt")
    shutil.copy(HERE / "src/INSTALL.md", dist / "INSTALL.md")
    # Flat zip for Templates > Saved Templates > Import: only JSON files, all at the top level.
    shutil.make_archive(str(HERE / "auto-door-templates-import"), "zip", dist / "templates")
    shutil.copy(HERE / "auto-door-templates-import.zip", dist / "auto-door-templates-import.zip")
    shutil.make_archive(str(HERE / "auto-door-elementor-package"), "zip", dist)
    print("wrote", len(PAGES) + len(PARTS), "templates; media month", args.media_month)


if __name__ == "__main__":
    main()
