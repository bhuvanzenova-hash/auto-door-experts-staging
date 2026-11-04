"""Assemble the static preview: src/pages/*.html + src/partials + src/blog -> repo root.

Page files start with a meta comment:
<!--meta title="..." description="..." nav="home" -->
and may use <!--@name--> markers for any partial in src/partials (plus the
generated <!--@latest-posts-->). Blog listing and article pages are generated
from src/blog/posts.json + src/blog/content/<slug>.html (see tools/import_blog.py).
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT.parent  # hosts serve the repo root, so pages are built there

# Cleaner labels than the importer's keyword guess, and shorter display titles.
TOPIC_FIX = {
    "automatic-doors-sydney-nsw-service-areas": "Guide",
    "automatic-door-maintenance": "Maintenance",
    "the-hidden-costs-of-ignoring-your-commercial-doors-annual-service": "Maintenance",
    "how-a-prestons-retail-centre-automatic-door-maintenance": "Case study",
    "5-services-you-should-expect-from-a-professional-automatic-door-company": "Guide",
}
TOPICS = ["Maintenance", "Repairs", "Compliance", "Buying guide", "Industry guide", "Case study", "Guide"]


def esc(s):
    return html.escape(s, quote=True)


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def load_posts():
    posts = json.loads((SRC / "blog/posts.json").read_text())
    for p in posts:
        p["topic"] = TOPIC_FIX.get(p["slug"], p["topic"])
        p["short"] = re.split(r"\s+\|\s+", p["title"])[0]
        p["url"] = f"blog-{p['slug']}.html"
    return posts


def card(p, lazy=True):
    return f'''<a class="pcard" href="{p["url"]}" data-topic="{esc(p["topic"])}">
  <span class="pcard__img"><img src="{p["image"]}" alt="" {'loading="lazy" ' if lazy else ''}width="1200" height="675"></span>
  <span class="pcard__topic">{esc(p["topic"])}</span>
  <h3 class="pcard__title">{esc(p["short"])}</h3>
  <span class="pcard__meta">{nice_date(p["date"])} · {p["minutes"]} min read</span>
</a>'''


def latest_posts(posts):
    return '<div class="posts">' + "".join(card(p) for p in posts[:3]) + "</div>"


def blog_index(posts):
    lead, rest = posts[0], posts[1:]
    used = [t for t in TOPICS if any(p["topic"] == t for p in posts)]
    chips = '<button class="fchip" aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button class="fchip" aria-pressed="false" data-filter="{esc(t)}">{esc(t)}</button>' for t in used)
    return f'''<!--meta title="Blog | The Auto Door Experts" description="Guides on automatic door maintenance, repairs, AS 5007 compliance, costs and choosing the right door for your building." nav="blog" -->
<section class="phero phero--blog">
  <div class="wrap">
    <p class="eyebrow">Blog</p>
    <h1 class="h1">Know your <em>doors.</em></h1>
    <p class="lead">Practical guides from the technicians who fix them.</p>
  </div>
</section>

<section class="sec sec--blog">
  <div class="wrap">
    <a class="feature" href="{lead["url"]}">
      <span class="feature__img"><img src="{lead["image"]}" alt="" width="1200" height="675" fetchpriority="high"></span>
      <span class="feature__body">
        <span class="pcard__topic">Latest · {esc(lead["topic"])}</span>
        <h2 class="h2">{esc(lead["short"])}</h2>
        <p>{esc(lead["excerpt"])}</p>
        <span class="pcard__meta">{nice_date(lead["date"])} · {lead["minutes"]} min read</span>
      </span>
    </a>

    <div class="filters" role="group" aria-label="Filter articles by topic">{chips}</div>
    <div class="posts posts--grid" data-posts>
{chr(10).join(card(p) for p in rest)}
    </div>
    <p class="filters__empty" data-empty hidden>No articles in this topic yet.</p>
  </div>
</section>

<!--@quote-->
'''


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def prepare_body(raw):
    # drop the article's own "Table of Contents" block; the sidebar builds one
    raw = re.sub(r"<h2>(?:<strong>)?\s*Table of Contents\s*(?:</strong>)?</h2>\s*<(ol|ul)>.*?</\1>", "", raw, flags=re.S | re.I)
    raw = re.sub(r"<h([234])><strong>(.*?)</strong></h\1>", r"<h\1>\2</h\1>", raw)
    raw = re.sub(r"<table>", '<div class="table-wrap"><table>', raw)
    raw = raw.replace("</table>", "</table></div>")
    raw = re.sub(r'<a href="(https?://(?!theautodoorexperts)[^"]+)">', r'<a href="\1" target="_blank" rel="noopener nofollow">', raw)
    toc, seen = [], set()

    def add_id(m):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        sid = slugify(text) or "section"
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, html.unescape(text)))
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    raw = re.sub(r"<h2>(.*?)</h2>", add_id, raw)
    return raw, toc


def post_page(p, posts):
    body, toc = prepare_body((SRC / f"blog/content/{p['slug']}.html").read_text())
    toc_html = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t in toc if t.lower() not in ("introduction",))
    related = [x for x in posts if x["topic"] == p["topic"] and x["slug"] != p["slug"]]
    related += [x for x in posts if x not in related and x["slug"] != p["slug"]]
    return f'''<!--meta title="{esc(p["short"])} | The Auto Door Experts" description="{esc(p["excerpt"])}" nav="blog" -->
<div class="progress" aria-hidden="true"><span data-progress></span></div>
<article class="article">
  <header class="article__head">
    <div class="wrap wrap--narrow">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="blog.html">Blog</a></nav>
      <span class="pcard__topic">{esc(p["topic"])}</span>
      <h1 class="article__title">{esc(p["short"])}</h1>
      <p class="article__meta">{nice_date(p["date"])} · {p["minutes"]} min read · The Auto Door Experts</p>
    </div>
  </header>
  <div class="wrap wrap--mid"><img class="article__cover" src="{p["image"]}" alt="" width="1200" height="675" fetchpriority="high"></div>

  <div class="wrap article__layout">
    <div class="prose" data-prose>
{body}
    </div>
    <aside class="article__aside">
      {f'<nav class="toc" aria-label="On this page"><p class="toc__h">On this page</p><ol>{toc_html}</ol></nav>' if toc_html else ''}
      <div class="helpcard">
        <p class="helpcard__h">Door playing up?</p>
        <p>Talk to a technician, 24/7.</p>
        <a class="btn btn--red btn--block" href="tel:1300829998"><svg class="ic"><use href="#i-phone"/></svg>1300 829 998</a>
        <a class="btn btn--ghost btn--block" href="#quote">Request a quote</a>
      </div>
    </aside>
  </div>
</article>

<section class="sec sec--paper" aria-labelledby="rel-title">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2 id="rel-title" class="h2">Keep reading.</h2>
      <a class="link sec__more" href="blog.html">All articles <svg class="ic"><use href="#i-arrow"/></svg></a>
    </div>
    <div class="posts">{"".join(card(x) for x in related[:3])}</div>
  </div>
</section>

<!--@quote-->
'''


def render(raw, partials, shell):
    meta = dict(re.findall(r'(\w+)="([^"]*)"', re.match(r"<!--meta(.*?)-->", raw, re.S).group(1)))
    body = re.sub(r"<!--meta.*?-->\s*", "", raw, count=1, flags=re.S)
    out = shell.replace("{{title}}", meta["title"]).replace("{{description}}", meta["description"])
    out = out.replace("{{body}}", body)
    for name, part in partials.items():
        out = out.replace(f"<!--@{name}-->", part)
    # mark the active nav item
    return out.replace(f'data-nav="{meta.get("nav", "")}"', 'data-nav aria-current="page"')


def main():
    partials = {p.stem: p.read_text() for p in (SRC / "partials").glob("*.html")}
    shell = partials.pop("shell")
    posts = load_posts()
    partials["latest-posts"] = latest_posts(posts)

    # every .html in the repo root is generated; clear them so removed pages don't linger
    for old in OUT.glob("*.html"):
        old.unlink()

    pages ={page.name: page.read_text() for page in sorted((SRC / "pages").glob("*.html"))}
    pages["blog.html"] = blog_index(posts)
    for p in posts:
        pages[p["url"]] = post_page(p, posts)
    for name, raw in pages.items():
        (OUT / name).write_text(render(raw, partials, shell))
    print(f"built {len(pages)} pages ({len(posts)} articles)")


if __name__ == "__main__":
    main()
