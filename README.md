# cert-helper

A study tool for learning **AI fields** — generative AI, computer vision and agentic AI —
built around question banks with worked reasoning, spaced repetition, condensed cheat sheets
and a concept-level diagnostic layer.

Two front ends over one content model: a terminal client with no dependencies, and a
self-contained web page you can drop on any static host.

<sub>A [Gama Core](https://www.gamacore.com) project.</sub>

## The three tracks

| Track | Covers | Questions |
|---|---|---|
| **`generative-ai`** — Generative AI Engineering | Prompting, tokenisation and data pipelines, transformer internals, fine-tuning and alignment, RAG | 197 |
| **`computer-vision`** — Computer Vision | Image fundamentals and geometry, CNNs and ViTs, detection, segmentation, video and tracking, edge deployment | 192 |
| **`agentic-ai`** — Agentic AI | Architecture, memory, tool orchestration, evaluation, deployment, safety and human oversight | 323 |

Each track lives under `tracks/<id>/` with its own topic blueprint, bank, cheat sheets and
concept taxonomy. The tooling knows nothing about any particular field beyond what it reads
from there.

**712 questions across three tracks · 340 verified source links · 458 flashcards ·
164 concepts.**

## Certification alignment

The tracks are built to teach the field, not to drill an exam. Where a track's topics happen
to line up with a published certification, it says so and follows that certification's
weights — so it doubles as preparation without that being the point.

| Track | Aligns with | How closely |
|---|---|---|
| `agentic-ai` | [NVIDIA NCP-AAI](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/) | Topic areas and weights follow NVIDIA's published blueprint; the bank covers **52 of its 54** numbered exam objectives |
| `generative-ai` | [IBM Gen AI Engineering](https://www.coursera.org/professional-certificates/ibm-generative-ai-engineering) | Topics map to the ten generative-AI courses (1–3, 10–16), weighted by share of the 91 covered hours |
| `computer-vision` | **Nothing.** No vendor certifies applied computer vision. | The adjacent credentials are multimodal gen AI (NVIDIA NCA-GENM), a cloud exam where vision is 15–20% (Microsoft AI-102), or course badges (OpenCV University). Weights here are editorial judgement — a claim, not a citation. |

If you *are* sitting one of the two exams, `tracks/<id>/RESOURCES.md` covers the specifics,
including NVIDIA's official 20-page study guide and its 54 objectives.

## Quick start

```bash
git clone https://github.com/Gama-core/cert-helper.git
cd cert-helper
./sim.py                       # menu-driven; nothing to install
./sim.py tracks                # list the tracks
./sim.py -k computer-vision    # switch (remembered for next time)
```

Python 3.8+ and nothing else — the terminal client is stdlib only. For the web version,
open `web/<track-id>/index.html`, or upload that single file to a web server.

## Topic weights

Each track's practice sets are apportioned across its topic areas, so effort lands where the
material concentrates.

<details>
<summary><b>Agentic AI</b> — weights follow NVIDIA's published blueprint</summary>

| Topic area | Weight |
|---|---|
| Agent Architecture and Design | 15% |
| Agent Development | 15% |
| Evaluation and Tuning | 13% |
| Deployment and Scaling | 13% |
| Cognition, Planning, and Memory | 10% |
| Knowledge Integration and Data Handling | 10% |
| NVIDIA Platform Implementation | 7% |
| Run, Monitor, and Maintain | 7% |
| Safety, Ethics, and Compliance | 5% |
| Human-AI Interaction and Oversight | 5% |

These reconcile two official NVIDIA sources that disagree. The certification page gives
Deployment 13% and Run/Monitor 5% (summing to 98%); the study guide PDF gives 5% and 7%
(summing to 92%). Taking the higher figure from each sums to **exactly 100%**, so each
document appears to carry one typo. See `tracks/agentic-ai/RESOURCES.md` §0.

</details>

<details>
<summary><b>Generative AI Engineering</b> — weights by share of course hours</summary>

| Topic area | Hours | Weight |
|---|---|---|
| Introduction to Artificial Intelligence | 13 | 14% |
| Generative AI: Introduction and Applications | 8 | 9% |
| Prompt Engineering Basics | 10 | 11% |
| LLM Architecture and Data Preparation | 6 | 7% |
| Foundational Models for NLP and Language Understanding | 10 | 11% |
| Language Modeling with Transformers | 9 | 10% |
| Engineering and Fine-Tuning Transformers | 8 | 9% |
| Advanced Fine-Tuning for LLMs | 9 | 10% |
| AI Agents with RAG and LangChain | 9 | 10% |
| Project: Applications with RAG and LangChain | 9 | 9% |

</details>

<details>
<summary><b>Computer Vision</b> — weights are editorial judgement</summary>

| Topic area | Weight |
|---|---|
| Object Detection | 14% |
| Convolutional Architectures | 12% |
| Training Vision Models | 12% |
| Segmentation | 11% |
| Vision Transformers and Multimodal | 10% |
| Data and Evaluation | 9% |
| Image Fundamentals and Processing | 8% |
| Classical Vision and Geometry | 8% |
| Video and Tracking | 8% |
| Deployment and Edge | 8% |

No vendor publishes a computer vision blueprint, so these reflect where applied CV work
concentrates rather than any published source. Grounded in OpenCV, PyTorch and torchvision
documentation, Ultralytics, COCO's evaluation definition and the primary papers.

</details>

## What's in the box

```
certlib.py           Resolves a track from an id, the last used, or the first.
sim.py               Terminal simulator. Stdlib only.
tests.py             Validates a track's bank, cases, cheat sheets and concepts.
check_links.py       Verifies every reference URL across all tracks.
build_md.py          cheatsheet.json  ->  tracks/<id>/CHEATSHEET.md
build_web.py         everything       ->  web/<id>/{simulator,index}.html
web/template.html    Web simulator source. Edit this, not the generated files.

tracks/<id>/
  blueprint.json     Topic areas with weights, track metadata, page copy, and an
                     optional `certification` block when one aligns.
  concepts.json      Concept taxonomy mapping question tags to diagnosable concepts.
  cheatsheet.json    Condensed reference; every table row also becomes a flashcard.
  bank/*.json        Standalone questions, one file per topic area.
  cases/*.json       Case studies: one scenario, several linked questions.
  RESOURCES.md       Curated free study material. Every link verified in CI.
  STUDY_PLAN.md      A study plan mapped to the weights. (agentic-ai)
  CHEATSHEET.md      Generated. Printable and greppable.

.progress/<id>.json  Your progress, per track. Gitignored.
```

## The terminal simulator

```bash
./sim.py                              # menu (last track used)
./sim.py tracks                       # list tracks
./sim.py -k generative-ai             # switch; remembered for next time
./sim.py exam                         # timed mock: 60-70 q, 120 min, blueprint-weighted
./sim.py exam -n 20                   # short timed mock
./sim.py practice                     # 15 q, untimed, explanation after each
./sim.py practice -d nvidia-platform  # one topic area
./sim.py practice -c kv-cache         # one concept
./sim.py review                       # spaced repetition: whatever is due today
./sim.py drill                        # simpler pass: everything you got wrong
./sim.py case                         # a case study
./sim.py case -d CS03
./sim.py flash                        # flashcards over the cheat sheets
./sim.py flash -d nvidia-platform     # one deck
./sim.py cheat                        # all cheat sheets
./sim.py cheat -d logistics           # one section
./sim.py concepts                     # taxonomy + your accuracy on each
./sim.py cram -d safety-ethics-compliance   # every answer + explanation, no quiz
./sim.py stats                        # readiness by domain and concept
./sim.py --reset                      # wipe progress for the current track
```

During a question: `A`–`D` to answer (two letters for select-two, e.g. `AC`), `f` flag,
`r` reveal the answer and carry on (timed assessments), `b` back, `s` skip, `q` quit and score. Ctrl-C scores what you have answered rather than
discarding it.

### Modes

**Timed assessment** hides feedback until you submit, then scores per domain, lists what you
missed, and orders weak areas by *exam impact* — weight × gap — so a 40% in a 15% domain
outranks a 40% in a 5% one.

**Show answer** works mid-exam. In a timed assessment you can reveal the answer and explanation on
any question — `r` in the terminal, the **Show answer** button or `R` on the web — without
ending the run or stopping the clock. The question locks at that point, so an answer changed
after seeing the key cannot flatter the score.

The report keeps two figures apart:

- **Score** counts blanks as wrong, because the real exam does.
- **Unaided** excludes questions you revealed *before* selecting anything, because those
  measure nothing. Revealing after you had already committed does not affect it — that is
  just reading the explanation early.

A question revealed with nothing selected also enters the review schedule as a miss: you
needed the answer, so you should see it again.

In a feedback session (practice, review, case study) you can stop at any point with
**Finish & score** and be scored on what you answered rather than on the whole set.

**Review** is the retention engine. Every answer, in any mode including flashcards,
schedules the item with an adapted SM-2:

```
hit  → 1 day → 3 days → 8 days → 21 days (capped)
miss → due tomorrow, ease penalised
```

The 21-day cap is deliberate: with an exam weeks out, nothing should be parked longer than
three weeks. `review` asks what is due, most overdue first, heaviest domains breaking ties.

**Case studies** are one scenario with 3–4 linked questions across different domains,
closer to the exam's scenario-heavy style than standalone items. The scenario stays on
screen throughout. Case questions also appear individually in timed assessments, carrying their
scenario with them.

**Flashcards** drill pure recall over the cheat-sheet tables — 206 cards across 13 decks,
including the 18-row NVIDIA product map and the 28-term glossary. Self-graded, same scheduler.

**Concepts** are the diagnostic layer domain scores cannot give you. Domains tell you
*Knowledge Integration is at 62%*; concepts tell you it is **retrieval strategies** at 40%
while **chunking** is fine. Weak concepts are ranked by exam impact and each one hands you
the two commands that close it:

```
→ Agent evaluation  2/9 · Evaluation and Tuning 13%
    Trajectory over outcome, tool correctness, benchmarks, failure attribution.
    ./sim.py practice -c agent-evaluation   ·   ./sim.py cheat -d evaluation
```

A concept needs 4+ attempts before its accuracy is reported at all; below that it is noise.

**Cheat sheets** are condensed reference, not questions: the NVIDIA product map, the RAG
metric table with a needs-ground-truth column, reasoning and memory patterns, serving
metrics, guardrail types, governance frameworks, exam-day logistics, distractor patterns,
and an acronym glossary. Also in `CHEATSHEET.md` and in the web version, which prints.

---

## The web simulator

Same bank, same weighting, usable on a phone. Styled in the Gama Core design system — their
palette (crimson `#C5184B`, blue `#1D98D6`), their typefaces (Space Grotesk / Inter / IBM
Plex Mono), their light and dark themes. Tokens sit at the top of `web/template.html`;
change them there and rebuild.

Four tabs:

| Tab | Holds |
|---|---|
| **Console** | Readiness gauge, the four start-a-session cards, weakest concepts, timed assessment history, coverage |
| **Case studies** | The 10 scenarios, plus links to other people's practice exams |
| **Cheat sheets** | The 13 condensed reference sections. Prints. |
| **Cram sheet** | Every question with its answer and explanation, by topic area |

The console is deliberately status-only — what to do next and what to fix. Content you
browse rather than check lives on the other tabs.

### Mobile

Audited across all seven views (console, case studies, cheat sheets, cram, question,
flashcard, results) at 320 / 360 / 390 / 430px: **no horizontal page scroll at any
combination**. Wide reference tables scroll inside their own container, which is the only
thing allowed to exceed the viewport. Tap targets are at least 40px on tabs and buttons
below 640px.

Two fixes were needed to get there, both worth knowing if you edit the layout:

- Grid and flex children default to `min-width: auto` and refuse to shrink below their
  content's min-content width. The rail was blowing 357px past a 360px viewport until
  `.cols > * { min-width: 0 }` was added.
- `.wrap` carries `overflow-x: clip` as a backstop. `clip` rather than `hidden`, because
  `hidden` would create a scroll container and change the containing block for
  `position: sticky` descendants.

Keys: `A`–`D` answer · `←` `→` move · `F` flag · `R` show the answer (timed assessments) ·
`Enter` check/next. In flashcards, Space to reveal, `Y`/`N` to grade.

---

## Deploying it to a website

**No backend.** Scoring, the spaced-repetition scheduler and every analytic run
client-side. The page makes **zero** runtime network calls — no fetch, no XHR, no
WebSocket — and inlines every question, cheat sheet and concept.

### What to upload

One file:

```
web/<track-id>/index.html
```

One file per track — `web/agentic-ai/index.html`, `web/generative-ai/index.html`. They are
independent pages; host one, the other, or both.

Nothing else. No assets folder, no separate CSS or JS, no images. Every `href`/`src` that
is not already an absolute URL is a JavaScript template literal that resolves at runtime to
an https link baked into the data; nothing resolves against disk.

| You want | Upload to | Visitors get |
|---|---|---|
| A page per track | `/agentic-ai/index.html` | `example.com/agentic-ai/` |
| Under an existing section | `/learn/agentic-ai/index.html` | `example.com/learn/agentic-ai/` |
| A specific filename | `/simulator.html` | `example.com/simulator.html` |

Keeping the name `index.html` inside a folder gives the clean trailing-slash URL with no
server config.

### Two server settings that matter

**Enable compression.** 502 KB raw → **149 KB gzipped**, about 70% off. It is almost all
JSON, so it compresses very well. Apache: `mod_deflate`. nginx: `gzip on;` with `text/html`
in `gzip_types`. Without it, first load on mobile is slow for no reason.

**Do not cache it forever.** `Cache-Control: max-age=3600` or similar — long enough to help
repeat visitors, short enough that an update lands the same day.

### Redeploying

```bash
python3 build_web.py              # all tracks
python3 build_web.py generative-ai    # just one
# re-upload web/<track-id>/index.html
```

Visitor progress lives in their own `localStorage`, keyed by question id, so it survives
the replacement — adding questions does not reset anyone.

### Why two web targets

| File | For | Document |
|---|---|---|
| `web/<id>/simulator.html` | the claude.ai artifact | starts at `<title>` — the platform injects the skeleton |
| `web/<id>/index.html` | your own server | full `<!doctype html>` with charset, viewport, favicon, OG tags |

Serving `simulator.html` directly would render it in **quirks mode** with a guessed
character encoding and no mobile viewport. Use `index.html` off-platform.

Verified served from a plain HTTP server: standards mode (`CSS1Compat`), UTF-8, viewport
honored, no horizontal overflow at 390px, `localStorage` writable, and `window.claude`
absent with no console errors — the cross-device sync path degrades cleanly to local
storage.

### What you give up without a backend

Progress is per-browser and per-device:

- no sync between a visitor's laptop and phone
- clearing site data resets their progress
- no accounts, and no aggregate view of how visitors perform

A backend is only worth adding if you want one of those — in practice the aggregate view is
the one that usually motivates it.

### The one external request

Fonts load from `fonts.googleapis.com`. Everything else is inlined. To work fully offline
or without third-party requests, self-host Space Grotesk, Inter and IBM Plex Mono and swap
the `<link>`; the CSS declares real fallback stacks, so the page stays readable regardless.

---

## Extending the content

Four content files, each with its own shape. After editing any of them, run `tests.py`,
then the relevant build script.

### Questions

Append to the relevant `tracks/<id>/bank/*.json`:

```json
{
  "id": "NP-029",
  "type": "single",
  "difficulty": "medium",
  "stem": "...",
  "choices": ["...", "...", "...", "..."],
  "answer": [2],
  "explanation": "Why the key is right and why each distractor is wrong.",
  "tags": ["nim", "nvidia"],
  "ref": "https://docs.nvidia.com/..."
}
```

`answer` holds 0-based indices; two indices with `"type": "multi"` for select-two. Exactly
four choices. Choice order is reshuffled on every presentation, so you learn the content
rather than the letter.

### Case studies

Drop a file in `tracks/<id>/cases/`, named for its id:

```json
{
  "id": "CS11",
  "title": "Short descriptive name",
  "scenario": "A paragraph or two of situation, with the constraints that make the questions decidable.",
  "questions": [
    { "id": "CS11-1", "domain": "deployment-scaling", "type": "single", "difficulty": "hard",
      "stem": "...", "choices": ["...","...","...","..."], "answer": [1],
      "explanation": "...", "tags": ["..."], "ref": "https://..." }
  ]
}
```

Each question carries its own `domain`, so a case can span the blueprint. `tests.py`
enforces the id format, the four-choice rule, and a minimum of three linked questions.

### Cheat sheets

`tracks/<id>/cheatsheet.json` holds sections of typed blocks — `table`, `bullets` or `note`. Every
table row automatically becomes a flashcard (first cell asks, the rest answers), so adding
a row adds a card. Rebuild with `build_md.py` and `build_web.py`.

### Concepts

`tracks/<id>/concepts.json` maps free-form question tags onto a fixed set of diagnosable
concepts:

```json
{ "id": "kv-cache", "name": "KV cache and prefill", "domain": "deployment-scaling",
  "cheat": "deployment",
  "summary": "The memory term that scales with concurrency; prefix reuse and cache-aware routing.",
  "tags": ["kv-cache", "prefix-caching", "pagedattention", "oom", "prefill", "..."] }
```

Tags stay free-form when authoring; concepts claim them. A question's concepts are the
union over its tags, so adding a question usually needs no extra work — but `tests.py`
**fails** if a tag belongs to no concept, or if a question maps to none. That is what stops
the taxonomy silently drifting out of date as the bank grows. It also warns when a concept
has fewer than four questions, since accuracy on such a concept cannot be reported.

---

## Build and validation

```bash
python3 tests.py [cert]        # validate bank, cases, cheat sheets, concept taxonomy
python3 check_links.py         # verify every reference URL, across all tracks
python3 build_md.py [cert]     # regenerate tracks/<id>/CHEATSHEET.md
python3 build_web.py [cert]    # regenerate web/<id>/{simulator,index}.html
```

Omit the track id and `tests.py` and `build_md.py` act on the current one, while
`build_web.py` builds them all.

`tests.py` is strict where a mistake would be invisible: duplicate ids, wrong choice
counts, a `type` that disagrees with its answer count, a `ref` that is not a URL, a
select-two stem that does not say so, an unclaimed tag, a question with no concept, a
cheat-sheet table row whose width does not match its header, and any topic area with too
few questions to fill a 65-question exam.

`check_links.py` distinguishes a dead link from a blocked robot: 404/410/5xx and DNS
failures fail the run, while 401/403/429 are reported as unverifiable, since some hosts
refuse automated requests while serving browsers normally.

### CI

`.github/workflows/checks.yml` runs on every push and weekly:

- **validate** — `tests.py`, plus a staleness check that fails if `CHEATSHEET.md` or the
  web targets were not rebuilt after their sources changed.
- **links** — `check_links.py`. Non-blocking, because an upstream doc moving is not your
  commit's fault, but you want to know within the week. NVIDIA restructures its
  documentation regularly; this has already caught four dead references.

---

## Where the questions come from

Every question is original, written against primary documentation rather than anyone's
course material. Every explanation links to its source, and all 340 links are verified in CI.

| Track | Grounded in |
|---|---|
| Generative AI | IBM topic pages, Hugging Face and PyTorch docs, LangChain concepts, the original papers — never Coursera's own quiz content, which is the course's assessment and not ours to reproduce |
| Computer Vision | OpenCV, PyTorch and torchvision docs, Ultralytics, COCO's evaluation definition, the primary papers |
| Agentic AI | NVIDIA's published blueprint and 20-page study guide, NVIDIA and framework documentation, the primary papers |

Published third-party guides were used as *coverage intelligence* only — to find which
topics, product names and techniques they report as tested, then to write original items
for the gaps. Their technical claims were checked before anything was written from them;
one guide attributes the **CLASSic** evaluation framework to NVIDIA when it is Aisera's,
and the bank says so.

Other people's practice exams are **linked** — from `RESOURCES.md` and from the web
simulator's *Practice elsewhere* panel — because a second opinion is worth having. Nothing
is copied from them.

Sites advertising **actual**, **real** or **verified** exam questions are deliberately
absent. That content is reconstructed from live exams, breaches the NVIDIA candidate
agreement, is grounds for revoking a credential, and is frequently wrong.

---

## Study plan

[`tracks/agentic-ai/STUDY_PLAN.md`](tracks/agentic-ai/STUDY_PLAN.md) lays out six weeks at roughly 6–8 hours a week: a cold
baseline mock first, heavy domains early, NVIDIA product specifics in week 4, timed timed assessments
only in the last two weeks.

The daily habit that matters most:

```bash
./sim.py review    # due questions
./sim.py flash     # due flashcards
```

That is what makes week 1's work still be there in week 6. Five minutes of review beats
thirty minutes of rereading.

Ship it when `./sim.py stats` shows blueprint-weighted accuracy above 80% with every domain
attempted and no concept below target in a 13–15% topic area.


## Adding a track

Create `tracks/<id>/` with a `blueprint.json` and the tooling picks it up — `certlib.resolve`
discovers any directory there that has one.

`blueprint.json` carries the topic areas with their weights plus a `track` block holding the
metadata and page copy. The web client reads its eyebrow, headline, body text, fact tiles and
footer note from `track.ui` and `track.facts`, so nothing about a field is hard-coded in the
template:

```json
{
  "track": {
    "id": "computer-vision",
    "name": "Computer Vision",
    "tagline": "...",
    "target_pct": 80,
    "assessment_min": 50, "assessment_max": 60, "assessment_minutes": 90,
    "facts": [{"label": "Topic areas", "value": "10"}],
    "ui": {"eyebrow": "...", "hero_title": "...", "hero_body": "... {N} questions ...",
           "assessment_name": "Timed assessment", "readiness_label": "Weighted readiness",
           "footer_note": "..."},
    "certification": {
      "name": "...", "code": "...", "source": "https://...",
      "format": "...", "alignment": "How the topics line up, and how closely."
    }
  },
  "domains": [{"id": "...", "name": "...", "weight": 14, "prefix": "DE", "scope": "..."}]
}
```

`{N}` in `hero_body` is replaced with the question count. Weights should sum to 100. The
`certification` block is **optional** — omit it and the page simply never mentions an exam,
which is the right answer when none exists.

Then add `bank/`, `cheatsheet.json` and `concepts.json`, run `tests.py <id>`, and build. The
case-studies tab hides itself automatically when a track has no `cases/`.
