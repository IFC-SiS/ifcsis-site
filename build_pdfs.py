# -*- coding: utf-8 -*-
"""Generate the print one-pager PDF from the SAME source file as the web page."""
import os, glob, html, subprocess
from build_papers import parse, render_body, ROOT

NAVY, GOLD, TEAL = "#1F3050", "#C9A227", "#2E9B8E"
PRINT_CSS = """
@page { size: Letter; margin: 0.72in 0.8in; }
body { font-family: Carlito, Calibri, sans-serif; font-size: 12pt; line-height: 1.42;
       color: #1a1a1a; margin: 0; text-align: left; }
.org { font-size: 8.5pt; font-weight: 700; color: %s; letter-spacing: .09em; margin: 0 0 5px; }
.rule { border: 0; border-top: 2.5px solid %s; margin: 0 0 13px; }
h1 { font-size: 20pt; font-weight: 700; color: %s; margin: 0 0 4px; }
.sub { font-size: 12.5pt; font-style: italic; color: %s; margin: 0 0 3px; }
.meta { font-size: 10pt; color: #555; margin: 0 0 15px; }
h2 { font-size: 12pt; font-weight: 700; color: %s; margin: 13px 0 4px; }
p { margin: 0 0 8px; }
.ask { border-top: 1px solid #ccc; margin-top: 16px; padding-top: 10px; font-size: 11pt; }
.ask strong { color: %s; }
.foot { font-size: 9.5pt; color: #555; margin-top: 9px; }
""" % (NAVY, GOLD, NAVY, TEAL, NAVY, NAVY)

def build(path):
    slug = os.path.splitext(os.path.basename(path))[0]
    m, body, tail = parse(path)
    h = ['<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s</style></head><body>' % PRINT_CSS]
    h.append('<p class="org">INTERNATIONAL FOUNDATION FOR CHILD-SAFE INTERNET STANDARDS</p><hr class="rule">')
    h.append('<h1>%s</h1>' % html.escape(m["title"]))
    h.append('<p class="sub">%s</p>' % html.escape(m["subtitle"]))
    h.append('<p class="meta">%s &nbsp;&middot;&nbsp; %s</p>' % (html.escape(m["kind"]), html.escape(m["date"])))
    h.append(render_body(body))
    h.append('<div class="ask">')
    if tail:
        h.append('<p>%s</p>' % html.escape(tail))
    h.append('<p><strong>To request the full paper, write to shknudson@ifcsis.org.</strong></p>')
    h.append('<p class="foot">Read this note online at ifcsis.org/papers/%s/ &nbsp;&middot;&nbsp; '
             'The classification schema is published, versioned and open to review at standard.ifcsis.org.</p>' % slug)
    h.append('</div></body></html>')

    tmp = "/tmp/%s_print.html" % slug
    open(tmp, "w", encoding="utf-8").write("\n".join(h))
    out = os.path.join(ROOT, "docs", "IFC-SiS_%s_%s_1p.pdf" % (m["id"], slug.replace("-", "_").title().replace("_The_", "_the_")))
    out = os.path.join(ROOT, "docs", os.path.basename(m["pdf"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["wkhtmltopdf", "--enable-local-file-access", "-q",
                    "-T", "0", "-B", "0", "-L", "0", "-R", "0", tmp, out], check=True)
    return out

if __name__ == "__main__":
    for p in sorted(glob.glob(os.path.join(ROOT, "papers", "src", "*.txt"))):
        o = build(p)
        pg = subprocess.run(["pdfinfo", o], capture_output=True, text=True).stdout
        pages = [l for l in pg.splitlines() if l.startswith("Pages")]
        print("%-52s %s" % (os.path.basename(o), pages[0] if pages else "?"))
