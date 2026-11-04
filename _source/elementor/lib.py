"""Small helpers that emit Elementor 3.x JSON (containers + core widgets)."""
import random

RED, RED_DK, RED_TINT = "#D7191F", "#B01217", "#FCEDEC"
INK, TEXT, MUTED = "#14171C", "#2B3038", "#5A626D"
LINE, PAPER, WHITE = "#E3E0D9", "#F6F4EF", "#FFFFFF"
OK, SOFT, CORAL = "#157F4B", "#C3C8CF", "#FF4A50"
HEAD, BODY = "Archivo", "Inter"

_rng = random.Random(5007)


def eid():
    return f"{_rng.randrange(16**7):07x}"


def seed(n):
    _rng.seed(n)


def px(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}


def box(t, r=None, b=None, l=None, unit="px"):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l),
            "isLinked": t == r == b == l}


def gap(col, row=None):
    row = col if row is None else row
    return {"column": str(col), "row": str(row), "isLinked": col == row, "unit": "px", "size": col}


def resp(key, value, wrap=lambda x: x):
    """value is one value, or (desktop, tablet, mobile); None skips a breakpoint."""
    vals = value if isinstance(value, tuple) else (value, None, None)
    out = {}
    for suffix, v in zip(("", "_tablet", "_mobile"), vals):
        if v is not None:
            out[key + suffix] = wrap(v)
    return out


def typ(size, weight=400, font=BODY, lh=None, ls=None, prefix="typography"):
    s = {f"{prefix}_typography": "custom", f"{prefix}_font_family": font, f"{prefix}_font_weight": str(weight)}
    s.update(resp(f"{prefix}_font_size", size, px))
    if lh:
        s[f"{prefix}_line_height"] = px(lh, "em")
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls)
    return s


def icon_val(fa):
    return {"value": f"fas {fa}", "library": "fa-solid"}


def link(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def con(*kids, row=False, dirs=None, w=None, gp=0, pad=0, bg=None, justify=None, align=None, cls=None,
        anchor=None, href=None, radius=None, border=None, shadow=False, wrap=False, tag=None, title=None, grow=False,
        min_h=None, extra=None, inner=True):
    """A flex container. pad may be a number, box() dict, or (desktop, tablet, mobile) of those."""
    s = {"content_width": "full", "flex_direction": "row" if row else "column"}
    if dirs:  # (tablet, mobile) direction overrides
        if dirs[0]:
            s["flex_direction_tablet"] = dirs[0]
        if dirs[1]:
            s["flex_direction_mobile"] = dirs[1]
    if w is not None:
        s.update(resp("width", w, lambda v: px(v, "%")))
    s.update(resp("flex_gap", gp, gap))
    s.update(resp("padding", pad, lambda v: v if isinstance(v, dict) else box(v)))
    if bg:
        s.update(background_background="classic", background_color=bg)
    if justify:
        s.update(resp("flex_justify_content", justify))
    if align:
        s.update(resp("flex_align_items", align))
    if wrap:
        s["flex_wrap"] = "wrap"
    if cls:
        s["css_classes"] = cls
    if anchor:
        s["_element_id"] = anchor
    if href:
        s.update(html_tag="a", link=link(href))
    if tag:
        s["html_tag"] = tag
    if radius is not None:
        s["border_radius"] = box(radius)
    if border:
        s.update(border_border="solid", border_width=box(1), border_color=border)
    if shadow:
        s.update(box_shadow_box_shadow_type="yes",
                 box_shadow_box_shadow={"horizontal": 0, "vertical": 8, "blur": 28, "spread": 0, "color": "rgba(20,23,28,0.10)"})
    if title:
        s["_title"] = title
    if grow:
        s.update(_flex_size="grow")
    if min_h:
        s.update(resp("min_height", min_h, px))
    if extra:
        s.update(extra)
    return {"id": eid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": inner}


def grid(*kids, cols=(4, 2, 1), gp=20, cls=None, extra=None):
    s = {"container_type": "grid", "content_width": "full", "padding": box(0)}
    s.update(resp("grid_columns_grid", cols, lambda n: px(n, "fr")))
    s["grid_rows_grid"] = {"unit": "custom", "size": "auto", "sizes": []}
    s["grid_rows_grid_tablet"] = {"unit": "custom", "size": "auto", "sizes": []}
    s["grid_rows_grid_mobile"] = {"unit": "custom", "size": "auto", "sizes": []}
    s.update(resp("grid_gaps", gp, gap))
    if cls:
        s["css_classes"] = cls
    if extra:
        s.update(extra)
    return {"id": eid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": True}


def section(*kids, bg=None, pad=(144, 110, 88), side=(32, 32, 20), gp=0, anchor=None, cls=None, row=False, align=None):
    """Top-level band: full-bleed background, content boxed to the site width."""
    t, tb, m = pad if isinstance(pad, tuple) else (pad, pad, pad)
    s = {"content_width": "boxed", "boxed_width": px(1176), "flex_direction": "row" if row else "column",
         "padding": box(t, side[0], t, side[0]), "padding_tablet": box(tb, side[1], tb, side[1]),
         "padding_mobile": box(m, side[2], m, side[2]), "flex_gap": gap(gp)}
    if bg:
        s.update(background_background="classic", background_color=bg)
    if anchor:
        s["_element_id"] = anchor
    if cls:
        s["css_classes"] = cls
    if align:
        s["flex_align_items"] = align
    return {"id": eid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": False}


def widget(kind, settings):
    return {"id": eid(), "elType": "widget", "settings": settings, "elements": [], "widgetType": kind}


def h(text, tag="h2", size=(44, 35, 28), color=INK, weight=800, font=HEAD, lh=1.1, ls=-0.8, cls=None, mb=None, mt=None, center=False):
    s = {"title": text, "header_size": tag, "title_color": color}
    s.update(typ(size, weight, font, lh, ls))
    s["_css_classes"] = "ade-h" + (f" {cls}" if cls else "")
    if mb is not None or mt is not None:
        s["_margin"] = box(mt or 0, 0, mb or 0, 0)
    if center:
        s["align"] = "center"
    return widget("heading", s)


def eyebrow(text, color=RED, mb=14):
    return h(text.upper(), "p", (12.5, None, 11.5), color, 600, BODY, 1.2, 1.5, mb=mb)


def txt(html, size=(18, 17, 17), color=MUTED, lh=1.65, mb=None, mt=None, weight=400, max_w=None, cls=None):
    body = html if html.lstrip().startswith("<") else f"<p>{html}</p>"
    s = {"editor": body, "text_color": color, "_css_classes": "ade-txt" + (f" {cls}" if cls else "")}
    s.update(typ(size, weight, BODY, lh))
    if mb is not None or mt is not None:
        s["_margin"] = box(mt or 0, 0, mb or 0, 0)
    if max_w:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = px(max_w)
    return widget("text-editor", s)


def img(url, alt="", heights=None, radius=None, cls=None, fit="cover", width=100, unit="%", href=None):
    s = {"image": {"url": url, "id": "", "size": "", "alt": alt, "source": "library"}, "image_size": "full",
         "width": px(width, unit), "align": "left"}
    if heights:
        s.update(resp("height", heights, px))
        s["object-fit"] = fit
    if radius is not None:
        s["image_border_radius"] = box(radius)
    if cls:
        s["_css_classes"] = cls
    if href:
        s.update(link_to="custom", link=link(href))
    return widget("image", s)


def btn(text, url, style="red", icon=None, big=False, full=False, cls=None):
    p = {"red": (RED, WHITE, RED_DK, WHITE, None, None),
         "ghost": ("transparent", INK, "transparent", INK, LINE, INK),
         "light": ("transparent", WHITE, "rgba(255,255,255,0.06)", WHITE, "rgba(255,255,255,0.35)", WHITE)}[style]
    s = {"text": text, "link": link(url), "background_background": "classic", "background_color": p[0], "button_text_color": p[1],
         "button_background_hover_background": "classic", "button_background_hover_color": p[2], "hover_color": p[3],
         "border_radius": box(999), "text_padding": box(18, 28) if big else box(14, 22),
         "_css_classes": "ade-btn" + (f" {cls}" if cls else "")}
    s.update(typ(17 if big else 15.5, 600, BODY, 1.1))
    if p[4]:
        s.update(border_border="solid", border_width=box(2), border_color=p[4], button_hover_border_color=p[5])
    if icon:
        s.update(selected_icon=icon_val(icon), icon_indent=px(8), icon_align="row")
    if full:
        s["align"] = "justify"
    return widget("button", s)


def badge(fa, bg=RED_TINT, fg=RED, box_px=48, icon_px=20, radius=14):
    s = {"selected_icon": icon_val(fa), "view": "stacked", "shape": "square", "primary_color": bg, "secondary_color": fg,
         "size": px(icon_px), "icon_padding": px((box_px - icon_px) // 2), "border_radius": box(radius), "align": "left",
         "_css_classes": "ade-badge"}
    return widget("icon", s)


def ticks(items, color=TEXT, tick=OK, size=16, space=10):
    s = {"icon_list": [{"_id": eid(), "text": t, "selected_icon": icon_val("fa-check")} for t in items],
         "icon_color": tick, "text_color": color, "icon_size": px(13), "space_between": px(space), "text_indent": px(10),
         "_css_classes": "ade-ticks"}
    s.update(typ(size, 400, BODY, 1.45, prefix="icon_typography"))
    return widget("icon-list", s)


def html(code, cls=None):
    s = {"html": code}
    if cls:
        s["_css_classes"] = cls
    return widget("html", s)


def faq(items):
    kids = [con(txt(a, (16.5, None, 16), MUTED, 1.65, mb=28), title=q, extra={"_title": q}) for q, a in items]
    s = {"items": [{"_id": eid(), "item_title": q} for q, _ in items], "default_state": "all_collapsed",
         "max_items_expended": "one", "faq_schema": "yes", "accordion_item_title_icon": icon_val("fa-plus"),
         "accordion_item_title_icon_active": icon_val("fa-times"), "_css_classes": "ade-faq"}
    w = widget("nested-accordion", s)
    w["elements"] = kids
    return w


def tabs(items, cls="ade-tabs"):
    """items: list of (title, fa, container). Vertical list on desktop, scrolling pills on phones."""
    s = {"tabs": [{"_id": eid(), "tab_title": t, "tab_icon": icon_val(fa)} for t, fa, _ in items],
         "tabs_direction": "inline-start", "tabs_direction_tablet": "block-start", "tabs_direction_mobile": "block-start",
         "tabs_width": px(280), "horizontal_scroll": "enable", "breakpoint_selector": "none", "_css_classes": cls}
    w = widget("nested-tabs", s)
    w["elements"] = [c for _, _, c in items]
    return w


def template(title, kids, kind="page"):
    settings = {"template": "elementor_header_footer", "hide_title": "yes"} if kind == "page" else []
    return {"content": list(kids), "page_settings": settings, "version": "0.4", "title": title, "type": kind}
