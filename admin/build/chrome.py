#!/usr/bin/env python3
"""The single definition of this site's nav and footer, and the tool that applies it.

Run from anywhere: python3 admin/build/chrome.py

Every page is hand-written static HTML — that stays true, because a human should
be able to open any file and edit it. What is NOT hand-maintained is the chrome:
the nav row (including the version badge that validate.js requires to agree
everywhere) and the footer columns. Those are defined once here and rewritten in
place across the tree, which is what stops a sixteen-page site from drifting.

Adding a page: add it to NAV or FOOTER if it belongs there, write the file with
any nav/footer block at all, then run this. The block contents are replaced; the
`here` state is set from the page's own path.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()
GH = "https://github.com/SGit-AI/SGit-AI__Website__NFRs"
PARENT = "https://sgit.ai"
PARENT_TITLE = ("sgit.ai — the parent project: the hub this site is the engineering "
                "half of, and the network whose topic map lives here")

# The nav, two levels. Each entry is (label, own page, [(sub-label, href), ...], prefixes).
#
# Two rules the structure has to keep:
#   · A group label is always a link to a real page, never a menu-only stub. Nothing on
#     this site should be reachable only by opening a dropdown.
#   · `prefixes` decides the "here" state, so a page that is not itself in the nav still
#     lights up the group it belongs to.
NAV = [
    ("The map", "map/index.html", [
        ("&#9679; The topic map", "map/index.html"),
        ("The memory thesis", "memory/index.html"),
        ("The network", "network/index.html"),
    ], ("map/", "memory/", "network/")),
    ("Practice", "testing/index.html", [
        ("Testing", "testing/index.html"),
        ("CI pipelines", "ci/index.html"),
        ("Resilience", "resilience/index.html"),
    ], ("testing/", "ci/", "resilience/")),
    ("Documentation", "documentation/index.html", [
        ("The reality system", "documentation/index.html"),
        ("IFD: the methodology", "ifd/index.html"),
    ], ("documentation/", "ifd/")),
    ("Money &amp; work", "budgets/index.html", [
        ("Budgets as a discipline", "budgets/index.html"),
        ("Project management", "pm/index.html"),
    ], ("budgets/", "pm/")),
    ("The honest column", "scorecard/index.html", [
        ("&#9679; The scorecard", "scorecard/index.html"),
        ("Backups: the gap", "backups/index.html"),
        ("What this site ships", "shipped/index.html"),
    ], ("scorecard/", "backups/", "shipped/")),
    ("Site", "documents/index.html", [
        ("The documents", "documents/index.html"),
        ("Comms: tasks &amp; requests", "admin/comms.html"),
        ("Release history", "admin/versions.html"),
        ("Admin &amp; engineering", "admin/index.html"),
    ], ("documents/", "admin/")),
]

FOOTER = [
    ("The hub", [
        ("&#9679; The topic map", "map/index.html"),
        ("The memory thesis", "memory/index.html"),
        ("The scorecard", "scorecard/index.html"),
        ("The network", "network/index.html"),
        ("Backups: the gap", "backups/index.html"),
    ]),
    ("The owned disciplines", [
        ("Testing", "testing/index.html"),
        ("CI pipelines", "ci/index.html"),
        ("Documentation &amp; reality", "documentation/index.html"),
        ("IFD", "ifd/index.html"),
        ("Resilience", "resilience/index.html"),
    ]),
    ("Discipline, not figures", [
        ("Budgets", "budgets/index.html"),
        ("Project management", "pm/index.html"),
        ("What this site ships", "shipped/index.html"),
        ("The documents", "documents/index.html"),
    ]),
    ("Site", [
        ("Comms: tasks &amp; requests", "admin/comms.html"),
        ("Release history", "admin/versions.html"),
        ("llms.txt", "llms.txt"),
        ("llms-full.txt", "llms-full.txt"),
    ]),
]

BLURB = ("The non-functional requirements — version control, reliability, resilience, security, "
         "backups, consistency, explainability and documentation — as this estate actually "
         "practises them, with the topic map that says where everything else lives. Part of the "
         "<a href=\"https://sgit.ai\" style=\"display:inline;padding:0\"><b>sgit.ai</b></a> "
         "network. All content CC BY 4.0.")
PARTNOTE = ('⚠ Hub disclosure: this site links measurements taken by sibling sites and never '
            're-measures them. Every figure here is dated or generated. '
            '<a href="{up}shipped/index.html" style="display:inline;padding:0">What this site '
            'ships, and what it only asserts</a>.')
PARTNOTE_SELF = ('⚠ Hub disclosure: this site links measurements and never re-measures them. '
                 'You are on the page that states what is asserted versus demonstrated.')
NETLINE = ('<a href="https://sgit.ai"><b>↗ sgit.ai</b></a> — the parent project · '
           '<a href="https://sg-compute.sgit.ai">↗ sg-compute.sgit.ai</a> — the platform '
           'artefacts · <a href="https://coding.sgit.ai">↗ coding.sgit.ai</a> — the conventions · '
           '<a href="https://open-source.sgit.ai">↗ open-source.sgit.ai</a> — the villagers '
           'argument · <a href="https://sgit.ai/network/index.html">↗ the network</a>')


def nav_html(rel, up):
    groups = []
    for label, own, subs, prefixes in NAV:
        active = rel == own or any(rel.startswith(pre) for pre in prefixes)
        links = "\n".join(
            f'      <a class="sl{" here" if href == rel else ""}" href="{up}{href}">{text}</a>'
            for text, href in subs)
        groups.append(
            f'    <div class="ni ni-has">\n'
            f'      <a class="nl{" here" if active else ""}" href="{up}{own}">{label}'
            f'<span class="caret">&#9662;</span></a>\n'
            f'      <div class="sub">\n{links}\n      </div>\n'
            f'    </div>')
    rows = "\n".join(groups)
    return (f'<nav class="site"><div class="row">\n'
            f'  <a class="brand" href="{up}index.html">nfrs<span>.sgit.ai</span></a>\n'
            f'  <a class="parent" href="{PARENT}" title="{PARENT_TITLE}">↗ part of <b>sgit.ai</b></a>\n'
            f'  <span class="stage-pill">the hub</span>\n'
            f'  <a class="ver" href="{up}admin/versions.html" title="Site release history">{VERSION}</a>\n'
            f'  <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>\n'
            f'  <div class="nav-items">\n{rows}\n  </div>\n'
            f'  <a class="gh" href="{GH}">★ GitHub</a>\n'
            f'  <script src="{up}assets/nav.js" defer></script>\n'
            f'</div></nav>')


def footer_html(rel, up):
    partnote = PARTNOTE_SELF if rel == "shipped/index.html" else PARTNOTE.format(up=up)
    md_twin = f' · <a href="{up}index.md">this page as markdown</a>' if rel == "index.html" else ""
    cols = "\n".join(
        "  <div>\n"
        f"    <h4>{head}</h4>\n"
        + "\n".join(f'    <a href="{l if l.startswith("http") else up + l}">{t}</a>' for t, l in links)
        + "\n  </div>"
        for head, links in FOOTER)
    return (f'<footer class="site"><div class="cols">\n'
            f'  <div>\n'
            f'    <div class="brandline">nfrs<span>.sgit.ai</span></div>\n'
            f'    <p>{BLURB}</p>\n'
            f'    <p class="netline">{NETLINE}</p>\n'
            f'    <p class="partnote">{partnote}</p>\n'
            f'    <p class="verline">site <a href="{up}admin/versions.html">{VERSION}</a> · '
            f'<a href="{up}admin/index.html">engineering</a>{md_twin}</p>\n'
            f'  </div>\n{cols}\n</div></footer>')


def stamp_text_twins():
    """The version also appears in llms.txt, llms-full.txt and index.md, and
    validate.js enforces that it agrees. Nothing used to SET it there on the
    sibling sites, so it was hand-edited every release — and hand-editing it
    silently missed twice. Own it here instead."""
    out = []
    for name, pattern, repl in (
            ("llms.txt", r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
            ("llms-full.txt", r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
            ("index.md", r"· site v\d+\.\d+\.\d+ ·", f"· site {VERSION} ·")):
        p = ROOT / name
        if not p.exists():
            continue
        t = p.read_text()
        t2, n = re.subn(pattern, repl, t, count=1)
        if n and t2 != t:
            p.write_text(t2)
            out.append(name)
    return out


def main():
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        up = "../" * (len(path.relative_to(ROOT).parts) - 1)
        text = path.read_text()
        before = text
        text, n_nav = re.subn(r'<nav class="site">.*?</nav>', lambda _: nav_html(rel, up),
                              text, count=1, flags=re.S)
        text, n_foot = re.subn(r'<footer class="site">.*?</footer>', lambda _: footer_html(rel, up),
                               text, count=1, flags=re.S)
        if not n_nav or not n_foot:
            print(f"  ! {rel}: missing {'nav' if not n_nav else ''}"
                  f"{' and ' if not n_nav and not n_foot else ''}"
                  f"{'footer' if not n_foot else ''} block", file=sys.stderr)
        if text != before:
            path.write_text(text)
            changed.append(rel)
    changed += stamp_text_twins()
    print(f"chrome: {VERSION} applied — {len(changed)} file(s) updated")
    for c in changed:
        print(f"  · {c}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stdout = None
