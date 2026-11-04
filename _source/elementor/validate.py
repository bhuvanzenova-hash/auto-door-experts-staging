"""Static check: every setting in dist/templates/*.json must be a control that exists in the
plugin source. Reads the PHP as text only.

python3 elementor/validate.py <plugins-dir>
"""
import json
import re
import sys
from pathlib import Path

PLUGINS = Path(sys.argv[1])
EL, WPR = PLUGINS / "elementor", PLUGINS / "royal-elementor-addons"
WIDGET_FILES = {
    "heading": [EL / "includes/widgets/heading.php"], "text-editor": [EL / "includes/widgets/text-editor.php"],
    "image": [EL / "includes/widgets/image.php"], "button": [EL / "includes/widgets/button.php", EL / "includes/widgets/traits/button-trait.php"],
    "icon": [EL / "includes/widgets/icon.php"], "icon-list": [EL / "includes/widgets/icon-list.php"],
    "counter": [EL / "includes/widgets/counter.php"], "html": [EL / "includes/widgets/html.php"],
    "shortcode": [EL / "includes/widgets/shortcode.php"], "google_maps": [EL / "includes/widgets/google-maps.php"],
    "nested-tabs": [EL / "modules/nested-tabs/widgets/nested-tabs.php"],
    "nested-accordion": [EL / "modules/nested-accordion/widgets/nested-accordion.php"],
    "wpr-nav-menu": [WPR / "modules/nav-menu/widgets/wpr-nav-menu.php"], "wpr-grid": [WPR / "modules/grid/widgets/wpr-grid.php"],
    "wpr-post-title": [WPR / "modules/theme-builder/post-title/widgets/wpr-post-title.php"],
    "wpr-post-info": [WPR / "modules/theme-builder/post-info/widgets/wpr-post-info.php"],
    "wpr-post-media": [WPR / "modules/theme-builder/post-media/widgets/wpr-post-media.php"],
    "wpr-post-content": [WPR / "modules/theme-builder/post-content/widgets/wpr-post-content.php"],
}
COMMON = [EL / "includes/widgets/common-base.php", EL / "includes/widgets/common.php"]
CONTAINER = [EL / "includes/elements/container.php", WPR / "extensions/wpr-sticky-section.php"]
GROUPS = {
    "typography": ["typography", "font_family", "font_size", "font_weight", "line_height", "letter_spacing", "text_transform"],
    "background": ["background", "color", "image"], "border": ["border", "width", "color"], "box_shadow": ["box_shadow", "box_shadow_type"],
}
SUFFIX = re.compile(r"_(tablet|mobile|laptop|widescreen|tablet_extra|mobile_extra)$")


def controls(files):
    ids, groups = set(), set()
    for f in files:
        if not f.exists():
            print("  (missing source file)", f)
            continue
        src = f.read_text(errors="ignore")
        ids |= set(re.findall(r"add_(?:responsive_)?control\s*\(\s*'([a-zA-Z0-9_-]+)'", src))
        ids |= set(re.findall(r"\$\w+\[\s*'([a-z_]+)'\s*\]\s*=\s*\[", src))
        for m in re.finditer(r"add_group_control\(\s*(\w+)::get_type\(\),\s*\[(.*?)\]\s*\)", src, re.S):
            n = re.search(r"'name'\s*=>\s*'([a-z_-]+)'", m.group(2))
            if n:
                groups.add(n.group(1))
    return ids, groups


def known(key, ids, groups):
    base = SUFFIX.sub("", key)
    if base in ids or base.startswith("_"):
        return base in ids or base in {"_title", "_id"} or base.startswith("_flex")
    for g in groups:
        if base.startswith(g + "_") or base == g:
            return True
    return False


common_ids, common_groups = controls(COMMON)
con_ids, con_groups = controls(CONTAINER)
cache = {w: controls(fs) for w, fs in WIDGET_FILES.items()}
problems = {}
values = {}


def walk(els, name):
    for e in els:
        if e["elType"] == "container":
            ids, groups = con_ids | {"grid_columns_grid", "grid_rows_grid", "grid_gaps", "flex_direction", "flex_gap", "flex_wrap", "flex_justify_content", "flex_align_items", "content_width"}, con_groups | {"background", "border", "box_shadow", "_flex"}
            kind = "container"
        else:
            kind = e["widgetType"]
            if kind not in cache:
                problems.setdefault((kind, "UNKNOWN WIDGET"), set()).add(name)
                continue
            ids, groups = cache[kind][0] | common_ids, cache[kind][1] | common_groups
        for k, v in e["settings"].items():
            if not known(k, ids, groups):
                problems.setdefault((kind, k), set()).add(name)
            if isinstance(v, str):
                values.setdefault((kind, k), set()).add(v)
        walk(e.get("elements", []), name)


for f in sorted(Path(__file__).parent.glob("dist/templates/*.json")):
    walk(json.loads(f.read_text())["content"], f.stem)

print("UNKNOWN SETTINGS" if problems else "All settings match a control in the plugin source.")
for (kind, key), where in sorted(problems.items()):
    print(f"  {kind:18} {key:40} {len(where)} file(s)")

# ---- structure, links and CSS class checks
import subprocess  # noqa: E402

HERE = Path(__file__).parent
SLUGS = {"", "emergency-breakdown-service", "sales-and-installation", "periodic-maintenance", "spare-parts", "industries",
         "about-us", "contact-us", "blog", "privacy-policy", "terms-conditions",
         "how-a-prestons-retail-centre-automatic-door-maintenance"}
bad, seen_classes, raw_all = [], set(), ""
for f in sorted(HERE.glob("dist/templates/*.json")):
    raw = f.read_text()
    raw_all += raw
    ids = []

    def scan(els):
        for e in els:
            ids.append(e["id"])
            st = e["settings"]
            if e.get("widgetType") == "nested-tabs" and len(st["tabs"]) != len(e["elements"]):
                bad.append(f"{f.stem}: tabs/content count mismatch")
            if e.get("widgetType") == "nested-accordion" and len(st["items"]) != len(e["elements"]):
                bad.append(f"{f.stem}: accordion count mismatch")
            for key in ("css_classes", "_css_classes"):
                seen_classes.update(st[key].split() if isinstance(st.get(key), str) else [])
            scan(e.get("elements", []))

    scan(json.loads(raw)["content"])
    if len(ids) != len(set(ids)):
        bad.append(f"{f.stem}: duplicate element ids")
    for path in re.findall(r'(?:"url": "|href=\\?")(/[^"\\#?]*)', raw):
        if path.strip("/") not in SLUGS:
            bad.append(f"{f.stem}: link to unknown page {path}")
print("Structure and internal links OK." if not bad else "\n".join(sorted(set(bad))))

css = (HERE / "src/global.css").read_text()
snippet = (HERE / "src/footer-snippet.html").read_text() + (HERE / "src/cf7-form.txt").read_text()
for cls in sorted(set(re.findall(r"\.(ade-[a-zA-Z0-9_-]+)", css))):
    if cls not in raw_all and cls not in snippet:
        print("  CSS class not used anywhere:", cls)
for cls in sorted(c for c in seen_classes if c.startswith("ade-") and f".{c}" not in css):
    print("  no CSS for class (fine if intentional):", cls)
for cls in sorted(set(re.findall(r"\.((?:e-n|wpcf7|wpr)-[a-zA-Z0-9_-]+)", css))):
    found = subprocess.run(["grep", "-rlF", cls, str(PLUGINS / "elementor/modules"), str(PLUGINS / "contact-form-7"), str(PLUGINS / "royal-elementor-addons/modules")], capture_output=True, text=True).stdout
    print(f"  {'ok ' if found else 'MISSING'} {cls}")
