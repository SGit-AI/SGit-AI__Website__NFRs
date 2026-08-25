# nfrs.sgit.ai — the non-functional requirements, from the inside

**NFRs** — non-functional requirements — is this project's own operative term for *"the
whole version control, reliability, resilience, security, backups, consistency,
explainability, and documentation."* That sentence is this site's table of contents.

Other sites in the network argue that maintaining non-functional requirements is a scarce
and valuable thing. This one is the same argument from the inside: how the NFRs actually
get done here, including the places where they do not.

Live site: https://nfrs.sgit.ai (GitHub Pages, deployed from `dev`).

## This is a hub

Most NFR topics already have an owner elsewhere in the network, so this site owns the
disciplines with no other home and holds the topic map that says where everything else
lives. It runs under one rule, and the rule is enforced by CI rather than by intention:

> **Link the measurement, never restate it. Generate or date every number.**

## Structure

- `index.html` / `index.md` — the front page and its markdown twin
- `map/` — **the topic map**: every NFR topic, its position, its canonical source, its owning site
- `memory/` — the memory thesis: these sites as a more evolved form of LLM memory
- `network/` — the same set organised by site rather than by topic
- `testing/` `ci/` `documentation/` `ifd/` `resilience/` — the owned practice pages
- `budgets/` `pm/` — discipline published without this estate's figures
- `scorecard/` — the estate against its own eight-item list, with no plain tick in it
- `backups/` — the one NFR with no doctrine, published as an absence
- `shipped/` — what this site asserts versus what it can demonstrate
- `documents/` — reader pages for the source pack · `briefs/` — those sources, verbatim
- `admin/` — comms, release history, build tooling
- `admin/build/chrome.py` — the single definition of nav, footer and the version badge
- `admin/build/validate.js` — the pre-release gate
- `admin/build/gen_documents.py` — generates the `documents/` reader pages
- `admin/build/gen_sitemap.py` — generates `sitemap.xml` from the tree and git dates
- `admin/build/gen_llms_full.py` — generates `llms-full.txt`, the whole set in one fetch
- `assets/site.css` — shared stylesheet (sgit.ai design language)

## Release process

1. Bump `admin/build/version.txt` (vX.Y.Z, exactly once per release) and add a row to
   `admin/versions.html`; update `admin/comms.html` if the state of play changed.
2. `python3 admin/build/gen_documents.py` — only if a source document changed.
3. `python3 admin/build/chrome.py` — propagates the version badge and any nav/footer change
   to every page, and stamps the version into `llms.txt`, `llms-full.txt` and `index.md`.
4. `python3 admin/build/gen_sitemap.py && python3 admin/build/gen_llms_full.py`
5. `node admin/build/validate.js`
6. `git commit -am "site vX.Y.Z: ..." && git push origin dev`

Every push to `dev` runs `.github/workflows/deploy-pages.yml`: validate → auto-tag
(`vX.Y.Z`, verified against `version.txt` and the commit subject, next-minor enforced) →
deploy to GitHub Pages. Pull requests run validation only. Same pipeline as
[SGit-AI__Website](https://github.com/SGit-AI/SGit-AI__Website),
[SGit-AI__Website__PKI](https://github.com/SGit-AI/SGit-AI__Website__PKI) and
[SGit-AI__Website__Graphs](https://github.com/SGit-AI/SGit-AI__Website__Graphs).

## What the gate checks

Beyond the house checks (version agreement, internal links, canonical host, key-leak
tripwire), the gate enforces the two rules this site teaches:

- **Every discipline page must link at least one sibling site.** A page citing nobody has
  either re-measured (forbidden here) or is asserting without provenance.
- **Every page carrying figures must carry an as-of date** in a `<span class="asof">`.

All content CC BY 4.0 unless noted. Code under the repository licence.
