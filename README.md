# NCP-AAI prep kit

Study material and a working exam simulator for the **NVIDIA-Certified Professional:
Agentic AI LLMs (NCP-AAI)** exam.

| | |
|---|---|
| Exam | NVIDIA-Certified Professional: Agentic AI LLMs |
| Code | NCP-AAI |
| Format | 60–70 questions, 120 minutes, online remotely proctored (Certiverse) |
| Fee | $200 · valid 2 years |
| Prereq (recommended) | 1–2 years AI/ML, hands-on production agentic work |
| Official page | <https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/> |

NVIDIA does not publish a cut score. This kit targets **75%** so you train with margin.

## What's here

```
blueprint.json      The 10 official topic areas with their published weights.
cheatsheet.json     Condensed reference — source of truth for CHEATSHEET.md and the web page.
CHEATSHEET.md       Generated. 12 sections of tables: product map, metrics, patterns, acronyms.
bank/*.json         256 standalone questions — stem, 4 choices, answer, explanation, source.
cases/*.json        10 case studies — one scenario, 3-4 linked questions each (40 total).
sim.py              Terminal simulator: mock exam, practice, drill, stats, cram.
build_web.py        Rebuilds the web simulator from the bank + cheatsheet.
build_md.py         Rebuilds CHEATSHEET.md from cheatsheet.json.
tests.py            Validates the bank, the cases and the cheat sheets.
check_links.py      Verifies every reference URL still resolves.
web/template.html   Web simulator source (edit this, not simulator.html).
web/simulator.html  Built, self-contained page. Published as an Artifact.
RESOURCES.md        Curated free study material, by domain. All links verified live.
STUDY_PLAN.md       A 6-week plan mapped to the blueprint weights.
.history.json       Your progress (created on first run, not in the repo).
```

## The blueprint

Every practice set is apportioned to these weights, so effort lands where the exam puts it.
With 256 questions, three consecutive 65-question mocks draw almost no repeats.

| # | Topic area | Weight |
|---|---|---|
| 1 | Agent Architecture and Design | 15% |
| 2 | Agent Development | 15% |
| 3 | Evaluation and Tuning | 13% |
| 4 | Deployment and Scaling | 13% |
| 5 | Cognition, Planning, and Memory | 10% |
| 6 | Knowledge Integration and Data Handling | 10% |
| 7 | NVIDIA Platform Implementation | 7% |
| 8 | Run, Monitor, and Maintain | 5% |
| 9 | Safety, Ethics, and Compliance | 5% |
| 10 | Human-AI Interaction and Oversight | 5% |

NVIDIA's published figures sum to 98%; the simulator normalizes them.

## Run the terminal simulator

No dependencies — Python 3.8+ and nothing else.

```bash
./sim.py                              # menu
./sim.py exam                         # timed mock: 60–70 q, 120 min, weighted
./sim.py exam -n 20                   # short timed mock
./sim.py practice                     # 15 q, untimed, explanation after each
./sim.py practice -d nvidia-platform  # one topic area
./sim.py drill                        # re-ask only what you got wrong
./sim.py stats                        # readiness by domain + exam history
./sim.py cram -d safety-ethics-compliance   # read answers and reasoning, no quiz
./sim.py cheat                        # all cheat sheets
./sim.py cheat -d nvidia-platform     # one section
./sim.py --reset                      # wipe progress
```

During a question: `A`–`D` to answer (two letters for select-two, e.g. `AC`),
`f` flag, `b` back, `s` skip, `q` quit and score.

**Exam mode** hides feedback until you submit, then scores per domain, lists what you
missed, and orders your weak areas by *exam impact* (weight × gap) rather than raw score —
a 40% in a 15% domain outranks a 40% in a 5% one.

**Review mode** is the retention engine. Every answer — in any mode, including flashcards —
schedules the item with an adapted SM-2: a miss comes back tomorrow, a hit moves out 1 day,
then 3, then multiplying by the item's ease factor, capped at 21 days so nothing is ever
parked longer than three weeks before an exam. `./sim.py review` asks whatever is due,
most overdue first, heaviest domains breaking ties. `drill` still exists for the simpler
"everything I got wrong" pass.

**Case studies** are one scenario with 3-4 linked questions across different domains —
closer to the exam's scenario-heavy style than standalone items, and they test whether you
can hold a situation in mind across questions. The scenario stays on screen throughout.
Case questions also appear individually in mock exams, carrying their scenario with them.

**Flashcards** drill pure recall over the cheat-sheet tables: 206 cards across 13 decks,
including the 33-row NVIDIA product map and 28 acronyms. Self-graded, on the same
scheduler as the questions.

**Cheat sheets** are condensed reference, not questions: the NVIDIA product map, the RAG
metric table with a needs-ground-truth column, reasoning and memory patterns, serving
metrics and techniques, guardrail types, governance frameworks, distractor patterns, and an
acronym glossary. Twelve sections, in the terminal (`./sim.py cheat`), in the repo
(`CHEATSHEET.md`), and in the web simulator under the **Cheat sheets** tab, which prints.

## Web simulator

Same bank, same weighting, usable on a phone. Progress syncs to your account when
available and falls back to local browser storage.

**<https://claude.ai/artifact/2unx4V43a4bYqe8ysY1uhG>**

Keys: `A`–`D` answer · `←` `→` move · `F` flag · `Enter` check/next.

## Adding questions

Append to the relevant `bank/*.json`. The schema:

```json
{
  "id": "NP-013",
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

`answer` holds 0-based indices; two indices with `"type": "multi"` for select-two.
Exactly four choices. Then:

```bash
python3 tests.py          # validate bank, cases and cheat sheets
python3 check_links.py    # verify every reference URL resolves
python3 build_md.py       # regenerate CHEATSHEET.md from cheatsheet.json
python3 build_web.py      # regenerate web/simulator.html
```

Choice order is reshuffled on every presentation, so you learn the content rather than
the letter.

## Where the questions come from

Every question is original, written against the published blueprint and primary
documentation, and every explanation links to its source. All 89 source links are
verified live.

Other people's practice exams are **linked** from `RESOURCES.md` and from the web
simulator's *Practice elsewhere* panel — a second opinion is worth having. Nothing is
copied from them.

Published third-party guides (Preporato, Whizlabs and similar) were used as *coverage
intelligence* only — to find which topics, product names and techniques they report as
tested, then to write original items for the gaps. No questions were copied from practice
tests, and none from dump sites: those breach the NVIDIA candidate agreement, are grounds
for revoking a credential, and are mostly wrong.

Two claims found in those guides were checked before anything was written from them.
Nemotron 3 and NemoClaw are real and now covered. The **CLASSic** evaluation framework is
real but belongs to Aisera, not NVIDIA — the bank says so, because a guide that implies
otherwise will cost you a point.

## Adding a case study

Drop a file in `cases/`, named for its id:

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
enforces the id format, the four-choice rule, and that a case has at least three questions.

## CI

`.github/workflows/checks.yml` runs on every push and weekly:

- `tests.py` — schema and consistency of every question, case and cheat sheet table.
- A staleness check — fails if `CHEATSHEET.md` or `web/simulator.html` were not rebuilt
  after their sources changed.
- `check_links.py` — reports dead references. Non-blocking, because an upstream doc moving
  is not your commit's fault, but you want to know within the week.
