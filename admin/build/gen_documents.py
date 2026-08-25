#!/usr/bin/env python3
"""Generates the documents/ reader pages from the manifest below.

Run from anywhere: python3 admin/build/gen_documents.py

Each source document lives verbatim under briefs/ and is the source of truth. The
page generated here is presentation: a fixed apparatus (summary, key concepts
linked to where they live on this site, key ideas) and then the raw markdown
rendered in-page. Nothing here rewrites a source document, and no page restates a
figure from one — the hub rule applies to its own sources too.

Adding a document: drop the .md under briefs/, add a DOCS entry, run this, then
chrome.py, then validate.js.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
GH_BLOB = "https://github.com/SGit-AI/SGit-AI__Website__NFRs/blob/dev/briefs/"
PACK = "v0.33.62__nfrs-brief-pack__"

# slug, source filename stem, title, type, date, one-liner, summary,
# [(concept, href)], [idea, ...], on-this-site
DOCS = [
    ("brief", "00__BRIEF",
     "The brief: nfrs.sgit.ai",
     "Commissioning brief", "24 August 2026",
     "The naming verdict, the hub shape, the owns-and-links split, and the scorecard that makes the site credible.",
     "The document that commissioned this site. It settles three things and leaves one open. The name is right because NFR is the corpus's own operative term, already defined in a sentence that lists eight items verbatim, and because the stated audience is agents and technical readers for whom the acronym is precise rather than opaque. The shape is a hub rather than a primitive, because most of the topics already have owners in the network, which produces the owns-versus-links table the site is organised around. And the spine is the villagers sentence read from the inside: other sites argue that maintaining non-functional requirements is scarce and valuable; this one shows what doing it actually looks like, which creates an honesty obligation the brief discharges by instructing that the mixed scorecard be published unsoftened.",
     [("The topic map", "../map/index.html"),
      ("The owns-and-links contract", "../map/index.html#contract"),
      ("The scorecard", "../scorecard/index.html"),
      ("The eight-NFR sentence", "../index.html#definition")],
     ["The acronym is expanded in the first sentence of the front page, and the full phrase is used on first mention per page.",
      "The eight-item definition predates the site by a month and is treated as its table of contents.",
      "A clean scorecard column would be dishonest; the mixed table is the teaching.",
      "Build order: the map first, then the memory thesis, then the strongest owned disciplines."],
     "Implemented as the site's structure. The build order in section 6 is the order the pages were written in."),

    ("topic-map", "01__the-topic-map",
     "The topic map",
     "Hub artefact", "24 August 2026",
     "Every NFR topic: its position in one line, its canonical source, and the site that owns it.",
     "The hub's core artefact and the reason it exists. Each topic gets a position stated in a line, the best source for it, and an owner. Seven are owned outright by this site because they have no other home: testing, CI, documentation, the IFD methodology, budgets as a discipline, project management, and the resilience patterns. Five are linked and never restated, because a sibling site owns them: security domains, serverless and scalability, explainability's grounding ladder, architecture conventions, and the villagers market argument. One is neither, and the document says so plainly: backups is on the estate's own list and has no doctrine anywhere.",
     [("The map itself", "../map/index.html"),
      ("Backups: the gap", "../backups/index.html"),
      ("Linked, never restated", "../map/index.html#linked"),
      ("The network by site", "../network/index.html")],
     ["The rule above the table: when a sibling has measured something, link the measurement rather than paraphrasing it.",
      "A hub that drifts from its spokes is worse than no hub.",
      "Consistency is split across three homes; the recommendation is that this site owns the requirement and names the three rather than merging them.",
      "Backups is dense in mentions and empty in doctrine, which reads as coverage."],
     "Published as /map/, effectively in full. The deconfliction contract is enforced by the pre-release gate, which fails a discipline page that cites no sibling."),

    ("memory-thesis", "02__the-memory-thesis",
     "The memory thesis",
     "Thesis document", "24 August 2026",
     "These sites are a more evolved and focused version of what is usually called LLM memory — and the evidence it was already the design.",
     "Develops one sentence from the commissioning message into an argument. Conventional LLM memory is an accumulation of transcripts, retrieved by similarity, private to one vendor, unversioned, uncurated and invisible to the person it describes. This network is the same function built as publishing: curated briefs, addressable URLs, git versioning, an explicit licence, and a human who can read their own memory. The document's strongest section is the evidence that this was already the design before anybody said it: guides with for_llms in the filename, the markdown twin at every URL, and an agent-access report that diagnosed a memory-retrieval failure in exactly those terms. It closes with three honest limits, of which staleness is the sharpest: in an agent-memory network, a stale page is a false memory.",
     [("The thesis page", "../memory/index.html"),
      ("The evidence it was already the design", "../memory/index.html#evidence"),
      ("Staleness as the failure mode", "../memory/index.html#limits"),
      ("The agent surface", "../llms.txt")],
     ["Memory you can read, cite, version, license and hand to any agent, because it is a website.",
      "Curated memory is opinionated memory: an agent reading these sites inherits the positions, including the wrong ones.",
      "Fourteen sites is itself a retrieval problem, which is what the topic map is for.",
      "The do-not-publish tiers are memory's security model; shipped-versus-asserted pages are its calibration."],
     "Published as /memory/, and recommended to the network hub at sgit.ai, where it would explain all fourteen sites rather than one. That move is listed as proposed and not built."),

    ("owned-disciplines", "03__the-owned-disciplines",
     "The owned disciplines, in depth",
     "Source document", "24 August 2026",
     "Testing, CI, documentation, budgets and project management: position, verbatim material, and counter-evidence for each.",
     "The substance behind five of the map's summaries. Testing gives four non-negotiables and, more usefully, the reason they are affordable here: cheap typed objects make the real thing as easy to compose as a stand-in, so the philosophy and the type system are one decision. CI distils a large pipeline into one rule — build once, verify before naming — with the same shape appearing one level up in machine images that must prove themselves twice. Documentation carries the estate's best single idea. Budgets gives three pillars, all publishable as method with none of the figures. Project management supplies the site's most original page: the brief-and-debrief system, demonstrated across thousands of documents and described as a system nowhere.",
     [("Testing", "../testing/index.html"),
      ("CI pipelines", "../ci/index.html"),
      ("Documentation", "../documentation/index.html"),
      ("Budgets", "../budgets/index.html"),
      ("Project management", "../pm/index.html")],
     ["Every structural guard encodes a rule that was violated at least once.",
      "One source, many consumers, no drift — with the counter-example of a second version file read by nothing.",
      "The rule is right and enforcement is manual, which is the same finding the coding pack reached.",
      "Opportunity cost as a first-class acceptance, with a named owner."],
     "Five site pages, each closing with the counter-evidence this document supplies. The measurements stay linked to the sibling packs that took them."),

    ("site-architecture", "04__site-architecture",
     "Site architecture",
     "Source document", "24 August 2026",
     "Page by page, the house pattern to copy, and the generate-or-date rule.",
     "Short and operational. It instructs copying the pki.sgit.ai house pattern and adding a full-text agent surface, then lists the pages: the front page leading with the expanded acronym and the villagers definition as an epigraph, the map first, the thesis second, the owned disciplines one page each, the scorecard unsoftened, the backups stub published as an absence, and a shipped page distinguishing what the site asserts from what the estate demonstrably does. Its last section names what should be generated rather than written, and states the reason this site needs that rule more than its siblings: it quotes more measurements than any other page in the network, so it has the most to lose from drift.",
     [("How this site is built", "../admin/index.html"),
      ("What this site ships", "../shipped/index.html"),
      ("The pre-release gate", "../admin/index.html#validate"),
      ("llms-full.txt", "../llms-full.txt")],
     ["Copy the house pattern; resist the pull to duplicate what the spokes own.",
      "Generate or date every number.",
      "The topic densities, the scorecard and the map's link targets are all named as things that should be generated.",
      "Publish the build order unresolved."],
     "Followed, with one honest divergence: the scorecard is hand-assembled and dated rather than generated, and the generator is on the proposed list."),

    ("boundaries", "05__boundaries-and-licensing",
     "Boundaries and licensing",
     "Source document", "24 August 2026",
     "CC BY 4.0 site-wide, the do-not-publish list, and the hub's owns-versus-links contract.",
     "The contract the site runs under. Content is CC BY 4.0 throughout; quoted code and the in-repository methodology guides are Apache-2.0 and keep their notices, with the instruction to keep the repository canonical and generate rather than copy. The do-not-publish list is specific rather than gestural: none of the estate's own financial figures in any form, a review naming a private individual, a security review classified as an attack roadmap for live code, live hostnames and account identifiers, and the villagers brief's market statistics, which that brief itself flags as loosely attributed. The network-boundaries section restates the owns-and-links split with one rule above the table.",
     [("What is deliberately not published", "../shipped/index.html#boundaries"),
      ("Licensing", "../shipped/index.html#licensing"),
      ("The deconfliction contract", "../map/index.html#contract"),
      ("The budget boundary in practice", "../budgets/index.html")],
     ["When a sibling pack has measured something, link the measurement; never re-measure and never paraphrase the number.",
      "The budget discipline is publishable; the figures around it are not, anywhere.",
      "The second-source-of-truth rule applies to methodology guides exactly as it does to API references.",
      "House style: every discipline page ends with its counter-evidence, and the eight-NFR list is quoted verbatim wherever the scope is stated."],
     "Applied. The do-not-publish list is restated on the shipped page so a reader meets it without having to open the sources."),

    ("gaps", "06__gaps-and-open-questions",
     "Gaps, open questions and honest tensions",
     "Source document", "24 August 2026",
     "Six things to build fresh, five questions published unresolved, and four tensions the site is asked to keep rather than settle.",
     "The document that keeps the site honest about itself. Six build-fresh items, of which the backups doctrine and the description of how a brief becomes work here are the two with no existing material anywhere. Five open questions, including whether a hub site is worth its drift risk at all, and whether the estate's methodology should be published given that it is a competitive asset. Four tensions the site is instructed to publish rather than resolve, the sharpest being that teaching a practice honestly means teaching the gap between the rule and the practice — which is, in the end, what a non-functional-requirements site is for.",
     [("Backups: the question to answer first", "../backups/index.html#question"),
      ("Should IFD be published at all?", "../ifd/index.html#publish"),
      ("Is a hub worth its drift risk?", "../map/index.html#counter"),
      ("Proposed, and not built", "../shipped/index.html#proposed")],
     ["Decide whether the vault model is already the backup doctrine before writing the doctrine.",
      "The open-source position answers the publish-IFD question yes; say so explicitly rather than assuming it.",
      "The hub teaches what the spokes measured, and curation is the first thing to rot.",
      "An agent that learns the no-mocks rule also learns the coverage reality."],
     "Every item is carried onto the site: the questions are published unresolved, and the build-fresh items appear on the proposed list rather than being quietly dropped."),

    ("pack-readme", "README",
     "The brief pack: how to read it",
     "Pack README", "24 August 2026",
     "The reading order, the four things worth attention, and the hub's one rule.",
     "The pack's own front matter, published for the same reason the site publishes its sources: a reader who wants to check whether the site is faithful to its brief should not have to reconstruct the brief from the site. It gives the reading order, names the scorecard as the credibility move, names the methodology as the most original owned asset, and names the description of how a brief becomes work here as the most original project-management page available. It closes with the rule the whole site is built around.",
     [("The site's own build order", "../shipped/index.html"),
      ("The scorecard", "../scorecard/index.html"),
      ("IFD", "../ifd/index.html"),
      ("How a brief becomes work", "../pm/index.html#system")],
     ["Link the measurement, never restate it; generate or date every number.",
      "A stale page in an agent-memory network is a false memory.",
      "The name is the corpus's own operative term; expand the acronym in sentence one and otherwise ship it."],
     "The site follows the reading order as its build order. The one rule is the one the pre-release gate enforces."),
]


def render(d):
    (slug, stem, title, dtype, date, oneline, summary, concepts, ideas, onsite) = d
    src = f"../briefs/{PACK}{stem}.md"
    gh = f"{GH_BLOB}{PACK}{stem}.md"
    concept_lis = "\n".join(
        f'  <li><a href="{href}"><b>{text}</b></a></li>' for text, href in concepts)
    idea_lis = "\n".join(f'  <li>{i}</li>' for i in ideas)
    body = f'''<main class="doc">
<div class="crumb"><a href="../index.html">nfrs.sgit.ai</a> / <a href="index.html">documents</a> / {slug}</div>
<h1>{title}</h1>

<div class="docmeta">
  <span class="k">Type</span><span class="v">{dtype}</span>
  <span class="k">Version</span><span class="v">v0.33.62</span>
  <span class="k">Date</span><span class="v">{date}</span>
  <span class="k">Author</span><span class="v">Dinis Cruz, via the SG/Send Librarian</span>
  <span class="k">Licence</span><span class="v">CC BY 4.0</span>
  <span class="k">Source</span><span class="v"><a href="{src}">raw markdown</a> · <a href="{gh}">view on GitHub</a></span>
</div>

<h2 id="summary">Summary</h2>
<p>{summary}</p>

<h2 id="concepts">Key concepts</h2>
<ul>
{concept_lis}
</ul>

<h2 id="ideas">Key ideas</h2>
<ul>
{idea_lis}
</ul>

<h2 id="on-site">On this site</h2>
<p>{onsite}</p>

<h2 id="read">Read the document</h2>
<div class="mdread-label">📄 Original document · v0.33.62 · {date} · rendered from the <a href="{src}">raw markdown</a> (the source of truth)</div>
<div class="mdread" id="mdread" data-src="{src}"><noscript><p class="dim">In-page rendering needs JavaScript — <a href="{src}">open the raw markdown</a>.</p></noscript></div>

<div class="pagenav">
  <a href="index.html">← All documents</a>
  <a href="{src}">The raw markdown →</a>
</div>
</main>'''
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — nfrs.sgit.ai</title>
<meta name="description" content="{oneline}">
<link rel="canonical" href="https://nfrs.sgit.ai/documents/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:site_name" content="nfrs.sgit.ai">
<meta property="og:url" content="https://nfrs.sgit.ai/documents/{slug}.html">
<meta property="og:title" content="{title} — nfrs.sgit.ai">
<meta property="og:description" content="{oneline}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="text/markdown" href="{src}" title="The source document">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<nav class="site"><div class="row"></div></nav>

{body}

<footer class="site"><div class="cols"></div></footer>

<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="../assets/mdreader.js"></script>
</body>
</html>
'''
    p = ROOT / "documents" / f"{slug}.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return f"documents/{slug}.html"


def main():
    written = [render(d) for d in DOCS]
    print(f"gen_documents: {len(written)} reader page(s)")
    for w in written:
        print("  ·", w)


if __name__ == "__main__":
    main()
