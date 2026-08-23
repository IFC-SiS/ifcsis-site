# -*- coding: utf-8 -*-
from urllib.parse import quote

EMAIL = "shknudson@ifcsis.org"

def req_link(title, docid):
    subject = "Request: %s (%s)" % (title, docid)
    body = "\n".join([
        "Please send: %s (%s)" % (title, docid),
        "",
        "Name:",
        "Organisation:",
        "Role:",
        "Jurisdiction(s) this concerns:",
        "The question you are working on:",
        "",
    ])
    return "mailto:%s?subject=%s&body=%s" % (
        EMAIL, quote(subject, safe=""), quote(body, safe=""))

# id, title, blurb, onepager filename slug
GATED = [
    ("WP-02", "Refusal Is Not Referral",
     "AI systems now occupy relational roles with children &mdash; tutor, confidant, first responder to a disclosure. Roles of that kind have always carried professional duties. Declining to answer is not the same as getting a child to someone who can help, and current deployments do not meet the standard the role implies.",
     "Refusal_Is_Not_Referral"),
    ("WP-03", "The Misallocated Burden",
     "A least-cost-avoider analysis of child-safety cost allocation. Who is best placed to prevent the harm, who is actually bearing the cost of preventing it, and what follows when those are not the same party. The answer is not that anyone is acting in bad faith; it is that the burden has settled in the wrong place.",
     "The_Misallocated_Burden"),
    ("WP-04", "The Demand Side",
     "An identification problem. Demand for child-safety provision has been inferred from instruments that move three variables at the same time, and the confound has never been isolated. The paper argues for what would have to be measured to know, and is careful not to convert that argument into a prediction.",
     "The_Demand_Side"),
    ("NB-01", "Siting the School",
     "A school has a registrar and an address. Enrollment asks who may enter; siting asks what a child crosses to get there. Age assurance is the registrar and says nothing about the environment. Where content was never admitted, there is nothing inside to circumvent &mdash; a property of construction rather than a claim about detection accuracy.",
     "Siting_the_School"),
    ("NB-02", "Fitness to Serve",
     "At a liquor store the customer proves age: one bit, tested once. At a school the adult proves fitness &mdash; checked, credentialed, trained, renewed, revocable &mdash; and the child proves nothing. Children's spaces need the second regime. What that implies for the systems now being placed in front of children.",
     "Fitness_to_Serve"),
    ("NB-03", "A Place to Practise",
     "Written for registry operators. What a protected area inside a national domain would actually require to run &mdash; admission decisions, appeals, eviction, error rates &mdash; and why the operator is the only party positioned at the right layer to hold it.",
     "A_Place_to_Practise"),
]

OPEN = [
    ("EB-02", "The Admission Layer: A Proposal for African Co-Design",
     "Age assurance asks who is entering. Admission asks what is allowed inside. Why an interoperable child-safety metadata standard should be designed in Africa rather than built elsewhere and brought there.",
     "IFC-SiS_EB-02_Admission_Layer_Africa.pdf"),
    ("EB-01", "Additive Namespace Architecture",
     "The short introduction, read against the regimes now in force: the Online Safety Act, the Age Appropriate Design Code and the Digital Services Act. Sets out why the household election rests where Article 5 of the Convention on the Rights of the Child already places it, and the five conditions that separate this from privatised censorship.",
     "IFC-SiS_EB-01_Additive_Namespace_Architecture.pdf"),
    ("GD-01", "Your Country Can Build a Safe Place for Children Online",
     "A short guide for advocates. What to ask your government for, in one sentence, and why a protected area inside your own national domain needs no global permission to create. Written in plain terms, to be handed to someone who has never heard the argument.",
     "IFC-SiS_GD-01_Advocate_Guide.pdf"),
]

out = []
A = out.append

A('<!-- ============ LIBRARY ============ -->')
A('<section data-view="library" hidden>')
A('<div class="wrap">')
A('  <span class="eyebrow">Published work</span>')
A('  <h1 style="font-weight:700;font-size:34px;margin:0 0 18px;max-width:24ch">Read the argument, then take it apart.</h1>')
A('  <p style="margin-bottom:14px">Everything here is released for comment. Critical reactions &mdash; technical, legal, governance-related or empirical &mdash; are more useful to us than supportive ones.</p>')
A('  <p class="muted" style="margin-bottom:36px">Each entry below has a one-page brief you can read here on the site. The full paper is sent on request, so that it can be matched to the jurisdiction and the question you are working on. Work under submission to journals and other publications is not listed.</p>')
A('')
A('  <h2 style="font-weight:600;font-size:20px;margin:0 0 6px">Working papers</h2>')
A('  <p class="muted" style="margin:0 0 22px">One page now; the paper on request. <em>Zoning the Namespace</em>, the theoretical root the rest of the series assumes, is in preparation and available on request in the meantime.</p>')
A('')
A('  <div class="pubs">')
A('')

SLUG = {
    "WP-01":"zoning-the-namespace", "WP-02":"refusal-is-not-referral",
    "WP-03":"the-misallocated-burden", "WP-04":"the-demand-side",
    "NB-01":"siting-the-school", "NB-02":"fitness-to-serve",
    "EB-02":"admission-layer-african-co-design", "NB-03":"a-place-to-practise",
}

def card(docid, title, blurb, slug):
    page = "/papers/%s/" % SLUG[docid]
    A('    <article class="card">')
    A('      <span class="eyebrow">%s &middot; One-page brief</span>' % docid)
    A('      <h3>%s</h3>' % title)
    A('      <p>%s</p>' % blurb)
    A('      <p class="card-actions">')
    A('        <a class="btn btn-sm btn-ghost" href="%s">Read the brief &rarr;</a>' % page)
    A('        <a class="req" href="%s">Request the full paper</a>' % req_link(title, docid))
    A('      </p>')
    A('    </article>')
    A('')

for d in GATED[:3]:
    card(*d)
A('  </div>')
A('')
A('  <h2 style="font-weight:600;font-size:20px;margin:44px 0 6px">Notes and briefs</h2>')
A('  <p class="muted" style="margin:0 0 22px">Shorter work written for a particular audience or question.</p>')
A('')
A('  <div class="pubs">')
A('')
for d in GATED[3:]:
    card(*d)
A('  </div>')
A('')
A('  <h2 style="font-weight:600;font-size:20px;margin:44px 0 6px">Open access</h2>')
A('  <p class="muted" style="margin:0 0 22px">Introductory material, free to download, copy and circulate.</p>')
A('')
A('  <div class="pubs">')
A('')
for docid, title, blurb, fn in OPEN:
    A('    <article class="card">')
    A('      <span class="eyebrow">%s &middot; Open access</span>' % docid)
    A('      <h3>%s</h3>' % title)
    A('      <p>%s</p>' % blurb)
    A('      <p class="card-actions">')
    A('        <a class="btn btn-sm btn-ghost" href="/docs/%s">Download PDF &rarr;</a>' % fn)
    A('      </p>')
    A('    </article>')
    A('')
A('  </div>')
A('')
A('  <div class="note" style="margin-top:44px">')
A('    <h3>Why the full papers are sent rather than posted</h3>')
A('    <p>The longer documents carry material that is specific to a jurisdiction, a sector or an institution &mdash; and in some cases organisational proposals that only make sense once we know who is reading. Rather than post a version written for nobody in particular, we send the one that fits. Tell us the audience and the question in the request and we will reply with the relevant document, usually within a few days. Requests are welcome from critics as readily as from allies.</p>')
A('  </div>')
A('')
A('  <div class="note">')
A('    <h3>Not everything is listed here</h3>')
A('    <p>The foundation maintains further briefs and material written for particular jurisdictions, sectors and audiences, alongside work under submission to journals and other publications and so not published on this page. Any of it is available on request. Write to <a href="mailto:%s">%s</a> describing the audience and the question you are working on, and we will send what fits.</p>' % (EMAIL, EMAIL))
A('  </div>')
A('')
A('  <p class="muted">The controlled vocabulary and machine-readable schema are maintained separately at <a href="https://standard.ifcsis.org">standard.ifcsis.org</a>. Comments and corrections: <a href="mailto:%s">%s</a></p>' % (EMAIL, EMAIL))
A('</div>')
A('</section>')

open('/home/claude/site/library_section.html', 'w', encoding='utf-8').write("\n".join(out))

css = """.card-actions{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;margin:16px 0 0}
.card-actions .req{font:600 12.5px/1 'IBM Plex Sans',sans-serif;color:var(--accent-soft);text-decoration:none;border-bottom:1px solid var(--line-2);padding-bottom:2px}
.card-actions .req:hover{color:var(--accent);border-color:var(--accent)}"""
open('/home/claude/site/library_css.txt', 'w', encoding='utf-8').write(css)
print("written")
