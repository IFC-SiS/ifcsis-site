# -*- coding: utf-8 -*-
"""Generate a standalone, indexable page per one-pager.

Source: papers/src/<slug>.txt   ->   papers/<slug>/index.html
Front matter, then body, then a closing note, separated by lines of '---'.
"""
import os, re, glob, html
from urllib.parse import quote

SITE = "https://ifcsis.org"
EMAIL = "shknudson@ifcsis.org"
ROOT = os.path.dirname(os.path.abspath(__file__))

NAV = """<nav>
  <a class="brand" href="/#/">IFC-SiS</a>
  <ul>
    <li><a href="/#/admission">Admission Layer</a></li>
    <li><a href="/#/standard">Standard</a></li>
    <li><a href="/#/about">About</a></li>
    <li><a href="/#/faq">FAQ</a></li>
    <li><a href="/#/library" aria-current="page">Library</a></li>
  </ul>
  <a class="btn btn-sm" href="/#/contact">Contact</a>
</nav>"""

FOOTER = """<footer>
  <span>International Foundation for Child-Safe internet Standards</span>
  <span>This site sets no cookies and loads no third-party resources.</span>
  <span>&copy; 2026 International Foundation for Child-Safe internet Standards. All rights reserved.</span>
</footer>"""


def parse(path):
    raw = open(path, encoding="utf-8").read()
    parts = re.split(r"^---\s*$", raw, flags=re.M)
    meta = {}
    for line in parts[0].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    body = parts[1].strip() if len(parts) > 1 else ""
    tail = parts[2].strip() if len(parts) > 2 else ""
    return meta, body, tail


def render_body(body):
    out = []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            out.append("<h2>%s</h2>" % html.escape(block[3:].strip()))
        else:
            out.append("<p>%s</p>" % html.escape(block).replace("&#x27;", "'"))
    return "\n".join(out)


def req_link(title, docid):
    subject = "Request: %s (%s)" % (title, docid)
    body = "\n".join([
        "Please send: %s (%s)" % (title, docid), "",
        "Name:", "Organisation:", "Role:",
        "Jurisdiction(s) this concerns:",
        "The question you are working on:", "",
    ])
    return "mailto:%s?subject=%s&amp;body=%s" % (
        EMAIL, quote(subject, safe=""), quote(body, safe=""))


def build(path):
    slug = os.path.splitext(os.path.basename(path))[0]
    m, body, tail = parse(path)
    url = "%s/papers/%s/" % (SITE, slug)
    title, docid = m["title"], m["id"]

    ld = (
        '{"@context":"https://schema.org","@type":"ScholarlyArticle",'
        '"headline":%s,"description":%s,"url":%s,'
        '"author":{"@type":"Organization","name":"International Foundation for Child-Safe internet Standards"},'
        '"publisher":{"@type":"Organization","name":"International Foundation for Child-Safe internet Standards"},'
        '"isPartOf":{"@type":"PublicationIssue","name":"IFC-SiS working papers"}}'
    ) % (
        '"%s"' % title.replace('"', '\\"'),
        '"%s"' % m["description"].replace('"', '\\"'),
        '"%s"' % url,
    )

    h = []
    h.append('<!DOCTYPE html>')
    h.append('<html lang="en">')
    h.append('<head>')
    h.append('<meta charset="utf-8">')
    h.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    h.append('<title>%s — IFC-SiS</title>' % html.escape(title))
    h.append('<meta name="description" content="%s">' % html.escape(m["description"]))
    h.append('<meta name="robots" content="index, follow">')
    h.append('<link rel="canonical" href="%s">' % url)
    h.append('<meta property="og:type" content="article">')
    h.append('<meta property="og:title" content="%s — IFC-SiS">' % html.escape(title))
    h.append('<meta property="og:description" content="%s">' % html.escape(m["description"]))
    h.append('<meta property="og:url" content="%s">' % url)
    h.append('<meta name="citation_title" content="%s">' % html.escape(title))
    h.append('<meta name="citation_publisher" content="International Foundation for Child-Safe internet Standards">')
    h.append('<meta name="citation_public_url" content="%s">' % url)
    h.append('<script type="application/ld+json">%s</script>' % ld)
    h.append('<link rel="stylesheet" href="/assets/site.css">')
    h.append('</head>')
    h.append('<body>')
    h.append('')
    h.append('<div class="status"><strong>Working draft.</strong> Everything on this site is open for public comment and subject to revision.</div>')
    h.append('')
    h.append(NAV)
    h.append('')
    h.append('<main id="main">')
    h.append('<article class="wrap wrap-narrow paper">')
    h.append('  <p class="paper-back"><a href="/#/library">&larr; Library</a></p>')
    h.append('  <span class="eyebrow">%s &middot; %s</span>' % (html.escape(docid), html.escape(m["kind"])))
    h.append('  <h1>%s</h1>' % html.escape(title))
    h.append('  <p class="paper-sub">%s</p>' % html.escape(m["subtitle"]))
    h.append('  <p class="paper-meta">%s</p>' % html.escape(m["date"]))
    h.append('')
    h.append(render_body(body))
    h.append('')
    h.append('  <div class="note paper-ask">')
    if tail:
        h.append('    <p>%s</p>' % html.escape(tail))
    h.append('    <p class="card-actions">')
    h.append('      <a class="btn btn-sm" href="%s">Request the full paper</a>' % req_link(title, docid))
    if m.get("pdf"):
        h.append('      <a class="req" href="%s">Download this page as PDF</a>' % m["pdf"])
    h.append('    </p>')
    h.append('  </div>')
    h.append('')
    h.append('  <p class="muted">The classification schema is published, versioned and open to review at <a href="https://standard.ifcsis.org">standard.ifcsis.org</a>. Comments and corrections: <a href="mailto:%s">%s</a></p>' % (EMAIL, EMAIL))
    h.append('</article>')
    h.append('</main>')
    h.append('')
    h.append(FOOTER)
    h.append('</body>')
    h.append('</html>')

    d = os.path.join(ROOT, "papers", slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(h))
    return slug, url


if __name__ == "__main__":
    for p in sorted(glob.glob(os.path.join(ROOT, "papers", "src", "*.txt"))):
        print("built  %s  ->  %s" % build(p))
