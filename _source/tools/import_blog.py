"""One-off importer: pull every post from the live blog into src/blog/.

Writes src/blog/posts.json (metadata) and src/blog/content/<slug>.html
(sanitised article body), and downloads featured images to assets/img/blog/.
Run with: python3 -I tools/import_blog.py
"""
import html
import json
import re
import subprocess
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://theautodoorexperts.com.au"
UA = {"User-Agent": "Mozilla/5.0"}
RENAME = {"b": "strong", "i": "em", "h1": "h2", "h5": "h4", "h6": "h4"}
KEEP = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "strong", "b", "em", "i", "a", "blockquote",
        "table", "thead", "tbody", "tr", "th", "td", "br"}
VOID = {"br"}
# live URL path -> local preview page
LOCAL = {
    "": "index.html", "about-us": "about-us.html", "contact-us": "contact-us.html",
    "emergency-breakdown-service": "emergency-breakdown-service.html",
    "periodic-maintenance": "periodic-maintenance.html", "spare-parts": "spare-parts.html",
    "sales-and-installation": "sales-and-installation.html", "blog": "blog.html",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def meta(page, prop):
    m = re.search(rf'<meta (?:property|name)="{prop}" content="([^"]*)"', page)
    return html.unescape(m.group(1)) if m else ""


def body_chunk(page):
    start = page.find('<div class="wpr-post-content">')
    if start < 0:
        return ""
    depth, i = 0, start
    for m in re.finditer(r"<(/?)div\b", page[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return page[start: start + m.start()]
    return page[start:]


class Clean(HTMLParser):
    def __init__(self, slugs):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.slugs = [], 0, slugs

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "figure", "img", "svg", "noscript"):
            self.skip += tag not in ("img",)
            return
        if self.skip or tag not in KEEP:
            return
        tag = RENAME.get(tag, tag)
        if tag == "a":
            href = dict(attrs).get("href", "")
            self.out.append(f'<a href="{html.escape(localise(href, self.slugs))}">')
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "figure", "svg", "noscript"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in KEEP or tag in VOID:
            return
        self.out.append(f"</{RENAME.get(tag, tag)}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))


def localise(href, slugs):
    m = re.match(rf"{re.escape(SITE)}/?([^?#]*?)/?(#.*)?$", href)
    if not m:
        return href
    path = m.group(1)
    if path in LOCAL:
        return LOCAL[path]
    if path in slugs:
        return f"blog-{path}.html"
    return href


def tidy(markup):
    markup = re.sub(r"\s+", " ", markup)
    markup = re.sub(r"<(p|li|h[234])>\s*</\1>", "", markup)          # empty blocks
    markup = re.sub(r"\s*(</?(?:h[234]|p|ul|ol|li|table|thead|tbody|tr|blockquote)>)\s*", r"\1", markup)
    markup = re.sub(r"(</(?:h[234]|p|ul|ol|table|blockquote)>)", r"\1\n", markup)
    return markup.strip()


def topic(title):
    t = title.lower()
    for key, label in [("as5007", "Compliance"), ("as 5007", "Compliance"), ("compliance", "Compliance"),
                       ("cost", "Buying guide"), ("price", "Buying guide"), ("choose", "Buying guide"),
                       ("vs", "Buying guide"), ("type", "Buying guide"), ("planning", "Buying guide"),
                       ("buyers", "Buying guide"), ("maint", "Maintenance"), ("service", "Maintenance"),
                       ("repair", "Repairs"), ("sensor", "Repairs"), ("signs", "Repairs"),
                       ("care", "Industry guide"), ("warehouse", "Industry guide"), ("pharmacy", "Industry guide"),
                       ("industry", "Industry guide"), ("fitout", "Industry guide"), ("retail", "Industry guide")]:
        if key in t:
            return label
    return "Guide"


def main():
    sitemap = get(f"{SITE}/post-sitemap.xml")
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    slugs = {u.rstrip("/").rsplit("/", 1)[-1] for u in urls}
    (ROOT / "src/blog/content").mkdir(parents=True, exist_ok=True)
    img_dir = ROOT.parent / "assets/img/blog"
    img_dir.mkdir(parents=True, exist_ok=True)
    posts = []
    for url in urls:
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        page = get(url)
        title = re.split(r"\s[|\-–]\s(?=The Auto Door)", meta(page, "og:title"))[0].strip()
        p = Clean(slugs)
        p.feed(body_chunk(page))
        body = tidy("".join(p.out))
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        img = meta(page, "og:image")
        local_img = ""
        if img:
            raw = img_dir / f"{slug}.src"
            urllib.request.urlretrieve(img, raw) if False else raw.write_bytes(
                urllib.request.urlopen(urllib.request.Request(img, headers=UA), timeout=30).read())
            out = img_dir / f"{slug}.jpg"
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "75", "-Z", "1200",
                            str(raw), "--out", str(out)], check=True, capture_output=True)
            raw.unlink()
            local_img = f"assets/img/blog/{slug}.jpg"
        (ROOT / f"src/blog/content/{slug}.html").write_text(body)
        posts.append({
            "slug": slug, "title": title, "date": meta(page, "article:published_time")[:10],
            "excerpt": meta(page, "og:description") or meta(page, "description"),
            "image": local_img, "topic": topic(title + " " + slug),
            "minutes": max(2, round(words / 220)), "source": url,
        })
        print(f"{slug}: {words} words, {posts[-1]['topic']}")
    posts.sort(key=lambda x: x["date"], reverse=True)
    (ROOT / "src/blog/posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
