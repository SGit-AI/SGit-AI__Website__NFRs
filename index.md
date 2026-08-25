# nfrs.sgit.ai — the non-functional requirements, from the inside

> **NFRs** — non-functional requirements — is this project's own operative term for
> *"the whole version control, reliability, resilience, security, backups, consistency,
> explainability, and documentation."* That sentence was written a month before this site
> was conceived, and it is the site's table of contents.

*Source: <https://nfrs.sgit.ai/index.html> · site v0.1.1 · markdown twin of the front page.*

---

Other sites in this network sell the argument that [somebody has to be the
villagers](https://open-source.sgit.ai). This one is the same sentence from the inside:
how the NFRs actually get done here, including where they do not.

## This is a hub, and it behaves like one

| The rule | What it means here |
|---|---|
| **Link the measurement, never restate it** | When a sibling site has measured something, this site links that page. It does not re-measure and does not paraphrase the number. |
| **Generate or date every number** | Every figure carries an as-of date or is generated at build time. The pre-release gate rejects a page that carries figures without one. |
| **Every discipline page ends with its counter-evidence** | A page teaching a practice closes with the measured places that practice failed here. |

The stakes are raised by [the memory thesis](memory/index.html): if these sites are memory
an agent reads, a stale page is not an inconvenience, it is a false memory.

## What this site owns

| Page | The position, in a line |
|---|---|
| [The topic map](map/index.html) | Every NFR topic: what it means here, where the canonical material lives, which site owns it. **Read first.** |
| [Testing](testing/index.html) | No mocks, no patches — and the testing philosophy and the type system are one decision, not two. |
| [CI pipelines](ci/index.html) | Build once, verify before naming. Nothing gets a name until it has passed as an anonymous digest. |
| [Documentation](documentation/index.html) | *If the reality document doesn't list it, it does not exist. Briefs are aspirations, not facts.* |
| [IFD](ifd/index.html) | The named methodology, published outside the estate for the first time. It protects attention, and derives its rules from that. |
| [Resilience](resilience/index.html) | Design for the failure you had. Every mechanism here traces to a named incident. |
| [Budgets](budgets/index.html) | Profitability-first, pre-approve the ladder, budget-on-the-step — with none of this estate's own figures, anywhere. |
| [Project management](pm/index.html) | The project manager is where the register becomes work — plus how a brief becomes work here. |

## The estate, measured against its own eight-item list

*As of 24 August 2026. The full table, with each cell linked to the sibling pack that
measured it, is on [the scorecard](scorecard/index.html).*

| NFR | The estate, measured |
|---|---|
| Version control | ✅ auto-increment tags, the `version` file convention |
| Reliability / resilience | ✅ watchdog, poller, bake-and-verify — **and** a dead workflow nobody noticed |
| Security | ✅ key discipline, allowlists — **and** one disclosed key-in-history incident |
| Backups | ⚠️ **[no doctrine at all](backups/index.html)** |
| Consistency | 🟡 total compliance where a script checks, partial where it does not |
| Explainability | ✅ reality docs, provenance — **and** no evals anywhere |
| Documentation | ✅ a governing rule and a very large corpus — **and** a README describing a repository that does not exist |

Reading down the failure column produces one sentence: **what a machine enforces, holds;
what attention enforces, drifts.** That is the transferable finding of the whole site.

## Why a website, and not a memory feature

> *"The idea of these sites is to provide good briefs for agents to learn about how we work
> and think — **these sites are a more evolved and focused version of what is usually
> called LLM memory**."*

Conventional memory is accumulated transcripts, retrieved by similarity, private to one
vendor, unversioned and invisible to the person it describes. This is the same function
built as publishing: **memory you can read, cite, version, license and hand to any agent,
because it is a website.** [The thesis, its evidence, and its honest
limits](memory/index.html).

## Honest about itself

- [What this site ships](shipped/index.html) — asserted, demonstrated, or proposed-and-not-built, as a table.
- [Backups](backups/index.html) — the one item on the list with nothing behind it, published as an absence.
- [Admin & engineering](admin/index.html) — how the site is built, and the two rules it enforces on itself in CI.

## For agents

- [/llms.txt](llms.txt) — the annotated map, each entry carrying its page's most important fact.
- [/llms-full.txt](llms-full.txt) — the whole document set in one fetch.
- Source documents at constructed URLs: `/briefs/v0.33.62__nfrs-brief-pack__<name>.md`.

---

All content CC BY 4.0. Attribution: Dinis Cruz, with AI co-authorship.
Repository: <https://github.com/SGit-AI/SGit-AI__Website__NFRs>
