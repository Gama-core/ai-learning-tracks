#!/usr/bin/env python3
"""NCP-AAI certification simulator.

Stdlib only. Run `./sim.py` for the menu, or see `./sim.py --help`.

Modes
  exam      Full timed mock exam, weighted to the published blueprint.
  practice  Untimed, immediate feedback + explanation. Optionally per-domain.
  drill     Re-ask what you got wrong, weakest domains first.
  stats     Per-domain mastery and exam history.
  cram      Print every question's explanation for a domain (reading mode).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK_DIR = ROOT / "bank"
BLUEPRINT = ROOT / "blueprint.json"
CHEATS = ROOT / "cheatsheet.json"
CASE_DIR = ROOT / "cases"
CONCEPTS = ROOT / "concepts.json"
HISTORY = ROOT / ".history.json"

LABELS = "ABCD"
PASS_MARK = 0.75
MIN_ATTEMPTS = 4   # Below this, a concept's accuracy is noise, not a signal.


# ---------------------------------------------------------------- presentation

class C:
    """ANSI colors, disabled when not a TTY or NO_COLOR is set."""

    _on = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
    RESET = "\033[0m" if _on else ""
    BOLD = "\033[1m" if _on else ""
    DIM = "\033[2m" if _on else ""
    GREEN = "\033[32m" if _on else ""
    RED = "\033[31m" if _on else ""
    YELLOW = "\033[33m" if _on else ""
    CYAN = "\033[36m" if _on else ""
    ACCENT = "\033[36m" if _on else ""
    MAGENTA = "\033[35m" if _on else ""


def wrap(text: str, width: int = 88, indent: str = "") -> str:
    out, line = [], indent
    for word in text.split():
        if len(line) + len(word) + 1 > width and line.strip():
            out.append(line.rstrip())
            line = indent + word + " "
        else:
            line += word + " "
    out.append(line.rstrip())
    return "\n".join(out)


def cells(text: str, width: int) -> list:
    """Wrap one cell to `width`, returning its lines."""
    lines, line = [], ""
    for word in str(text).split():
        if len(line) + len(word) + (1 if line else 0) > width:
            if line:
                lines.append(line)
            # A single word longer than the column: hard-split it.
            while len(word) > width:
                lines.append(word[:width])
                word = word[width:]
            line = word
        else:
            line = f"{line} {word}" if line else word
    lines.append(line)
    return lines or [""]


def print_table(head: list, rows: list, total: int = 88, gap: int = 2) -> None:
    """Column-aligned table with per-cell wrapping and no truncation."""
    n = len(head)
    avail = total - gap * (n - 1) - 2
    natural = [max(len(str(r[i])) for r in [head] + rows) for i in range(n)]

    if sum(natural) <= avail:
        widths = natural
    else:
        # Share the space in proportion to how much each column actually needs,
        # with a floor so no column collapses to a word per line.
        floor = 12
        scale = avail / sum(natural)
        widths = [max(floor, int(w * scale)) for w in natural]
        # Give any rounding slack (or take any overshoot) from the widest column.
        widest = widths.index(max(widths))
        widths[widest] += avail - sum(widths)

    sep = " " * gap
    print("  " + sep.join(f"{C.BOLD}{h:<{widths[i]}}{C.RESET}" for i, h in enumerate(head)))
    print("  " + C.DIM + "-" * (sum(widths) + gap * (n - 1)) + C.RESET)
    for row in rows:
        cols = [cells(row[i], widths[i]) for i in range(n)]
        for ln in range(max(len(c) for c in cols)):
            out = []
            for i, col in enumerate(cols):
                text = col[ln] if ln < len(col) else ""
                if i == 0 and ln == 0:
                    out.append(f"{C.BOLD}{text:<{widths[i]}}{C.RESET}")
                elif i == 0:
                    out.append(f"{text:<{widths[i]}}")
                else:
                    out.append(f"{C.DIM if i and ln else ''}{text:<{widths[i]}}{C.RESET if i and ln else ''}")
            print("  " + sep.join(out).rstrip())


def rule(char: str = "-", width: int = 88) -> str:
    return C.DIM + char * width + C.RESET


def bar(frac: float, width: int = 24) -> str:
    frac = max(0.0, min(1.0, frac))
    filled = round(frac * width)
    color = C.GREEN if frac >= PASS_MARK else C.YELLOW if frac >= 0.6 else C.RED
    return f"{color}{'█' * filled}{C.DIM}{'·' * (width - filled)}{C.RESET}"


def clear() -> None:
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")


# ------------------------------------------------------------------- data load

@dataclass
class Question:
    id: str
    domain: str
    type: str
    difficulty: str
    stem: str
    choices: list
    answer: list
    explanation: str
    tags: list
    ref: str
    scenario: str = ""
    case: str = ""
    case_title: str = ""

    @property
    def answer_labels(self) -> str:
        return "".join(LABELS[i] for i in sorted(self.answer))


def load_blueprint() -> dict:
    bp = json.loads(BLUEPRINT.read_text())
    bp["by_id"] = {d["id"]: d for d in bp["domains"]}
    return bp


def load_questions(include_cases: bool = True) -> list:
    qs = []
    for path in sorted(BANK_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        for raw in data["questions"]:
            qs.append(Question(domain=data["domain"], **raw))
    if include_cases and CASE_DIR.exists():
        for path in sorted(CASE_DIR.glob("*.json")):
            case = json.loads(path.read_text())
            for raw in case["questions"]:
                qs.append(Question(scenario=case["scenario"], case=case["id"],
                                   case_title=case["title"], **raw))
    if not qs:
        sys.exit(f"No questions found in {BANK_DIR}")
    return qs


def load_concepts() -> tuple:
    """Return (concepts, tag -> [concept ids]). Concepts are a diagnostic layer
    over the blueprint: a question's concepts are derived from its tags."""
    if not CONCEPTS.exists():
        return [], {}
    concepts = json.loads(CONCEPTS.read_text())["concepts"]
    index: dict = {}
    for c in concepts:
        for tag in c["tags"]:
            index.setdefault(tag, []).append(c["id"])
    return concepts, index


def concepts_of(q: Question, index: dict) -> set:
    return {cid for tag in q.tags for cid in index.get(tag, [])}


def concept_stats(questions: list, hist: dict, concepts: list, index: dict) -> dict:
    """Per-concept bank size, attempts and accuracy."""
    out = {c["id"]: {"bank": 0, "attempts": 0, "correct": 0, "seen": 0}
           for c in concepts}
    for q in questions:
        rec = hist["questions"].get(q.id, {})
        for cid in concepts_of(q, index):
            st = out[cid]
            st["bank"] += 1
            if rec.get("seen"):
                st["seen"] += 1
                st["attempts"] += rec["seen"]
                st["correct"] += rec["correct"]
    for st in out.values():
        st["acc"] = st["correct"] / st["attempts"] if st["attempts"] else None
    return out


def load_cases() -> list:
    if not CASE_DIR.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(CASE_DIR.glob("*.json"))]


# ---------------------------------------------------------------- history/state

def load_history() -> dict:
    if HISTORY.exists():
        try:
            return json.loads(HISTORY.read_text())
        except json.JSONDecodeError:
            pass
    return {"exams": [], "questions": {}}


def save_history(hist: dict) -> None:
    HISTORY.write_text(json.dumps(hist, indent=2))


MAX_INTERVAL = 21   # An exam weeks away; never park a question longer than this.


def schedule(rec: dict, correct: bool) -> None:
    """SM-2, adapted: binary grade, capped interval, shorter second step.

    A miss resets the question to due today. A hit pushes it out by an
    interval that grows with the item's ease factor.
    """
    grade = 5 if correct else 2
    ease = rec.get("ease", 2.5)
    ease += 0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)
    rec["ease"] = round(max(1.3, min(2.8, ease)), 3)

    if not correct:
        rec["reps"] = 0
        rec["interval"] = 0
    else:
        rec["reps"] = rec.get("reps", 0) + 1
        if rec["reps"] == 1:
            rec["interval"] = 1
        elif rec["reps"] == 2:
            rec["interval"] = 3
        else:
            rec["interval"] = min(MAX_INTERVAL,
                                  max(1, round(rec.get("interval", 1) * rec["ease"])))
    rec["due"] = (date.today() + timedelta(days=rec["interval"])).isoformat()


def record(hist: dict, q: Question, correct: bool) -> None:
    rec = hist["questions"].setdefault(q.id, {"seen": 0, "correct": 0, "streak": 0})
    rec["seen"] += 1
    if correct:
        rec["correct"] += 1
        rec["streak"] = rec.get("streak", 0) + 1
    else:
        rec["streak"] = 0
    rec["last"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    schedule(rec, correct)


def migrate(hist: dict) -> None:
    """Give pre-scheduling records a due date so old progress still counts."""
    for rec in hist["questions"].values():
        if "due" in rec:
            continue
        rec.setdefault("ease", 2.5)
        rec.setdefault("reps", rec.get("streak", 0))
        # Unresolved misses come due immediately; settled items get a short delay.
        rec["interval"] = 0 if rec["seen"] > rec["correct"] and rec.get("streak", 0) < 2 else 2
        rec["due"] = (date.today() + timedelta(days=rec["interval"])).isoformat()


def due_pool(questions: list, hist: dict) -> list:
    """Questions scheduled for review on or before today, most overdue first."""
    today = date.today().isoformat()
    out = []
    for q in questions:
        rec = hist["questions"].get(q.id)
        if rec and rec.get("due", "9999") <= today:
            out.append((rec.get("due", today), q))
    out.sort(key=lambda t: t[0])
    return [q for _, q in out]


def due_counts(questions: list, hist: dict) -> dict:
    today = date.today()
    week = (today + timedelta(days=7)).isoformat()
    now, soon, new = 0, 0, 0
    for q in questions:
        rec = hist["questions"].get(q.id)
        if not rec or not rec.get("seen"):
            new += 1
        elif rec.get("due", "9999") <= today.isoformat():
            now += 1
        elif rec.get("due", "9999") <= week:
            soon += 1
    return {"due": now, "week": soon, "new": new}


# -------------------------------------------------------------------- sampling

def weighted_sample(questions: list, bp: dict, n: int, hist: dict | None = None) -> list:
    """Pick n questions apportioned to blueprint weights (largest-remainder)."""
    pool = {}
    for q in questions:
        pool.setdefault(q.domain, []).append(q)

    weights = {d["id"]: d["weight"] for d in bp["domains"] if d["id"] in pool}
    total = sum(weights.values())
    exact = {d: n * w / total for d, w in weights.items()}
    counts = {d: int(v) for d, v in exact.items()}

    # Distribute the remainder to the largest fractional parts.
    short = n - sum(counts.values())
    for d, _ in sorted(exact.items(), key=lambda kv: kv[1] - int(kv[1]), reverse=True):
        if short <= 0:
            break
        counts[d] += 1
        short -= 1

    picked = []
    for domain, want in counts.items():
        avail = pool[domain][:]
        if hist:
            # Prefer questions seen less often, and previously-missed ones.
            def priority(q):
                r = hist["questions"].get(q.id, {})
                missed = r.get("seen", 0) - r.get("correct", 0)
                return (r.get("seen", 0) - missed * 2, random.random())
            avail.sort(key=priority)
        else:
            random.shuffle(avail)
        if want > len(avail):
            # Not enough in this domain; take all and let others absorb the rest.
            picked.extend(avail)
        else:
            picked.extend(avail[:want])

    # Top up if any domain was short of its quota.
    if len(picked) < n:
        rest = [q for q in questions if q not in picked]
        random.shuffle(rest)
        picked.extend(rest[: n - len(picked)])

    random.shuffle(picked)
    return picked[:n]


def shuffle_choices(q: Question) -> Question:
    """Return a copy with choices permuted, so answer position is never memorized."""
    order = list(range(len(q.choices)))
    random.shuffle(order)
    return Question(
        id=q.id, domain=q.domain, type=q.type, difficulty=q.difficulty, stem=q.stem,
        choices=[q.choices[i] for i in order],
        answer=sorted(order.index(a) for a in q.answer),
        explanation=q.explanation, tags=q.tags, ref=q.ref,
        scenario=q.scenario, case=q.case, case_title=q.case_title,
    )


# ------------------------------------------------------------------- asking UI

def render(q: Question, idx: int, total: int, bp: dict, time_left: float | None,
           flagged: bool) -> None:
    dom = bp["by_id"][q.domain]["name"]
    head = f"{C.BOLD}Q{idx}/{total}{C.RESET}  {C.CYAN}{dom}{C.RESET}"
    meta = f"{C.DIM}{q.difficulty}{C.RESET}"
    if flagged:
        meta += f"  {C.YELLOW}⚑ flagged{C.RESET}"
    if time_left is not None:
        mins, secs = divmod(max(0, int(time_left)), 60)
        color = C.RED if time_left < 300 else C.DIM
        meta += f"  {color}{mins:02d}:{secs:02d} left{C.RESET}"
    print(f"\n{head}   {meta}")
    print(rule())
    if q.scenario:
        print(f"{C.MAGENTA}CASE {q.case} · {q.case_title}{C.RESET}")
        print(wrap(q.scenario, indent=C.DIM) + C.RESET)
        print()
    print(wrap(q.stem))
    if q.type == "multi":
        print(f"\n{C.YELLOW}Select TWO answers.{C.RESET}")
    print()
    for i, choice in enumerate(q.choices):
        print(wrap(f"{LABELS[i]}. {choice}", indent="   ")[3:])
    print()


def ask(q: Question, idx: int, total: int, bp: dict, deadline: float | None,
        flagged: set) -> tuple:
    """Return (selection_or_None, action). action in {'answer','quit','back'}."""
    want = len(q.answer)
    while True:
        time_left = deadline - time.time() if deadline else None
        if time_left is not None and time_left <= 0:
            return None, "timeout"
        clear()
        render(q, idx, total, bp, time_left, q.id in flagged)
        hint = "letters" if want == 1 else f"{want} letters, e.g. AC"
        raw = input(f"Answer ({hint})  [f]lag [s]kip [b]ack [q]uit > ").strip()
        cmd = raw.lower()
        if cmd == "q":
            return None, "quit"
        if cmd == "b":
            return None, "back"
        if cmd == "s":
            return [], "answer"
        if cmd == "f":
            flagged.symmetric_difference_update({q.id})
            continue
        picks = sorted({LABELS.index(ch) for ch in raw.upper() if ch in LABELS})
        if not picks:
            continue
        if len(picks) != want:
            print(f"{C.RED}This question needs exactly {want} answer(s).{C.RESET}")
            time.sleep(1.1)
            continue
        return picks, "answer"


def show_feedback(q: Question, picks: list, bp: dict) -> None:
    correct = picks == sorted(q.answer)
    if correct:
        print(f"{C.GREEN}{C.BOLD}✓ Correct{C.RESET}  ({q.answer_labels})")
    else:
        got = "".join(LABELS[i] for i in picks) or "—"
        print(f"{C.RED}{C.BOLD}✗ Incorrect{C.RESET}  you: {got}   "
              f"{C.GREEN}answer: {q.answer_labels}{C.RESET}")
    print()
    print(wrap(q.explanation, indent="  "))
    print(f"\n  {C.DIM}{q.id} · {bp['by_id'][q.domain]['name']} · "
          f"{', '.join(q.tags)}{C.RESET}")
    print(f"  {C.DIM}{q.ref}{C.RESET}")
    print(rule())
    input(f"{C.DIM}Enter to continue{C.RESET} ")


# --------------------------------------------------------------------- scoring

def score_report(results: list, bp: dict, elapsed: float, title: str) -> float:
    total = len(results)
    got = sum(1 for _, picks, q in results if picks == sorted(q.answer))
    frac = got / total if total else 0.0

    clear()
    print(f"\n{C.BOLD}{title}{C.RESET}")
    print(rule("="))
    verdict = (f"{C.GREEN}{C.BOLD}PASS{C.RESET}" if frac >= PASS_MARK
               else f"{C.RED}{C.BOLD}BELOW TARGET{C.RESET}")
    mins, secs = divmod(int(elapsed), 60)
    print(f"\n  Score  {C.BOLD}{got}/{total}  ({frac*100:.1f}%){C.RESET}   {verdict}"
          f"   {C.DIM}target {PASS_MARK*100:.0f}%  ·  time {mins}m{secs:02d}s{C.RESET}\n")

    per = {}
    for _, picks, q in results:
        d = per.setdefault(q.domain, [0, 0])
        d[1] += 1
        if picks == sorted(q.answer):
            d[0] += 1

    print(f"  {C.BOLD}{'Domain':34}{'Wt':>4}  {'Score':>7}  Mastery{C.RESET}")
    ordered = sorted(bp["domains"], key=lambda d: -d["weight"])
    for dom in ordered:
        if dom["id"] not in per:
            continue
        ok, n = per[dom["id"]]
        f = ok / n
        print(f"  {dom['name'][:34]:34}{dom['weight']:>3}%  {ok:>3}/{n:<3}  "
              f"{bar(f)} {f*100:5.1f}%")

    wrong = [(q, picks) for _, picks, q in results if picks != sorted(q.answer)]
    if wrong:
        print(f"\n  {C.BOLD}Missed ({len(wrong)}){C.RESET}")
        for q, picks in wrong:
            got_s = "".join(LABELS[i] for i in picks) or "—"
            print(f"    {C.RED}✗{C.RESET} {q.id}  {C.DIM}{bp['by_id'][q.domain]['name']}"
                  f"  (you {got_s}, correct {q.answer_labels}){C.RESET}")
        print(f"\n  {C.DIM}Run './sim.py drill' to re-ask these.{C.RESET}")

    weak = [d for d in ordered if d["id"] in per and per[d["id"]][0] / per[d["id"]][1] < PASS_MARK]
    if weak:
        print(f"\n  {C.BOLD}Study next, highest exam impact first:{C.RESET}")
        for d in sorted(weak, key=lambda d: -(d["weight"] * (1 - per[d["id"]][0] / per[d["id"]][1]))):
            f = per[d["id"]][0] / per[d["id"]][1]
            print(f"    {C.YELLOW}→{C.RESET} {d['name']} "
                  f"{C.DIM}({f*100:.0f}%, {d['weight']}% of exam){C.RESET}")
            print(wrap(d["scope"], width=80, indent="      " + C.DIM) + C.RESET)
    print()
    return frac


# ----------------------------------------------------------------------- modes

def run_quiz(questions: list, bp: dict, hist: dict, timed: bool,
             feedback: bool, title: str, shuffle: bool = True) -> None:
    questions = [shuffle_choices(q) for q in questions]
    if not shuffle:
        pass  # choice order is still shuffled; only question order is fixed
    deadline = time.time() + bp["exam"]["duration_minutes"] * 60 if timed else None
    started = time.time()
    flagged: set = set()
    answers: dict = {}

    i = 0
    try:
      while i < len(questions):
        q = questions[i]
        picks, action = ask(q, i + 1, len(questions), bp, deadline, flagged)
        if action == "quit":
            if not answers:
                print("\nAborted.\n")
                return
            if input(f"\n{C.YELLOW}Quit and score what you answered? [y/N] {C.RESET}"
                     ).strip().lower() != "y":
                continue
            questions = questions[:i]
            break
        if action == "timeout":
            print(f"\n{C.RED}{C.BOLD}Time expired.{C.RESET}\n")
            time.sleep(1.5)
            break
        if action == "back":
            i = max(0, i - 1)
            continue
        answers[q.id] = picks
        if feedback:
            show_feedback(q, picks, bp)
        i += 1
    except (KeyboardInterrupt, EOFError):
        # Interrupting should not throw away work already done.
        print(f"\n{C.YELLOW}Interrupted — scoring what you answered.{C.RESET}")

    results = [(q.id, answers.get(q.id, []), q) for q in questions if q.id in answers]
    if not results:
        print("\nNothing answered.\n")
        return

    for _, picks, q in results:
        record(hist, q, picks == sorted(q.answer))

    frac = score_report(results, bp, time.time() - started, title)
    hist["exams"].append({
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": title, "score": round(frac, 4),
        "n": len(results), "seconds": round(time.time() - started),
    })
    save_history(hist)

    if not feedback and input(f"{C.DIM}Review every question with explanations? "
                              f"[y/N] {C.RESET}").strip().lower() == "y":
        for _, picks, q in results:
            clear()
            render(q, 0, 0, bp, None, False)
            show_feedback(q, picks, bp)


def mode_exam(args, questions, bp, hist) -> None:
    n = args.count or random.randint(bp["exam"]["question_count_min"],
                                     bp["exam"]["question_count_max"])
    n = min(n, len(questions))
    clear()
    print(f"\n{C.BOLD}{bp['exam']['name']} — Mock Exam{C.RESET}")
    print(rule("="))
    print(f"\n  {n} questions · {bp['exam']['duration_minutes']} minutes · "
          f"target {PASS_MARK*100:.0f}%")
    print(f"  {C.DIM}Weighted to the published blueprint. No feedback until the end.")
    print(f"  [f]lag to mark, [b]ack to revise, [s]kip leaves it blank (counts wrong)."
          f"{C.RESET}\n")
    input(f"{C.BOLD}Enter to start the clock. {C.RESET}")
    run_quiz(weighted_sample(questions, bp, n, hist), bp, hist,
             timed=True, feedback=False, title="Mock exam")


def mode_practice(args, questions, bp, hist) -> None:
    pool = questions
    title = "Practice"
    if getattr(args, "concept", None):
        concepts, index = load_concepts()
        by_id = {c["id"]: c for c in concepts}
        if args.concept not in by_id:
            print(f"{C.BOLD}Concepts{C.RESET}")
            for c in concepts:
                print(f"  {C.CYAN}{c['id']:<26}{C.RESET} {c['name']}")
            sys.exit(f"\nUnknown concept '{args.concept}'.")
        pool = [q for q in questions if args.concept in concepts_of(q, index)]
        title = f"Concept — {by_id[args.concept]['name']}"
        random.shuffle(pool)
        pool = pool[: args.count or len(pool)]
        run_quiz(pool, bp, hist, timed=False, feedback=True, title=title)
        return
    if args.domain:
        pool = [q for q in questions if q.domain == args.domain]
        if not pool:
            sys.exit(f"Unknown domain '{args.domain}'. Options:\n  " +
                     "\n  ".join(d["id"] for d in bp["domains"]))
        title = f"Practice — {bp['by_id'][args.domain]['name']}"
        random.shuffle(pool)
        pool = pool[: args.count or len(pool)]
    else:
        pool = weighted_sample(questions, bp, min(args.count or 15, len(questions)), hist)
    run_quiz(pool, bp, hist, timed=False, feedback=True, title=title)


def mode_drill(args, questions, bp, hist) -> None:
    by_id = {q.id: q for q in questions}
    missed = []
    for qid, rec in hist["questions"].items():
        if qid in by_id and rec["seen"] > rec["correct"] and rec.get("streak", 0) < 2:
            missed.append((rec["seen"] - rec["correct"], by_id[qid]))
    if not missed:
        print(f"\n{C.GREEN}Nothing to drill — no unresolved misses on record.{C.RESET}")
        print(f"{C.DIM}A question leaves the drill list after 2 consecutive correct "
              f"answers.{C.RESET}\n")
        return
    # Weakest domains first, then most-missed questions.
    dom_w = {d["id"]: d["weight"] for d in bp["domains"]}
    missed.sort(key=lambda t: (-dom_w.get(t[1].domain, 0), -t[0]))
    pool = [q for _, q in missed][: args.count or len(missed)]
    print(f"\n{C.BOLD}Drilling {len(pool)} previously-missed question(s).{C.RESET}\n")
    time.sleep(0.8)
    run_quiz(pool, bp, hist, timed=False, feedback=True, title="Drill")


def mode_review(args, questions, bp, hist) -> None:
    """Spaced repetition: everything the scheduler says is due today."""
    pool = due_pool(questions, hist)
    counts = due_counts(questions, hist)
    if not pool:
        print(f"\n{C.GREEN}Nothing due today.{C.RESET}")
        if counts["week"]:
            print(f"{C.DIM}{counts['week']} question(s) come due within a week.{C.RESET}")
        if counts["new"]:
            print(f"{C.DIM}{counts['new']} never attempted — "
                  f"'./sim.py practice' introduces new ones.{C.RESET}")
        print()
        return
    # Weakest domains first among equally overdue items.
    weight = {d["id"]: d["weight"] for d in bp["domains"]}
    pool.sort(key=lambda q: (hist["questions"][q.id].get("due", ""),
                             -weight.get(q.domain, 0)))
    n = args.count or len(pool)
    print(f"\n{C.BOLD}{len(pool)} due today{C.RESET}"
          f"{f' — reviewing {n}' if n < len(pool) else ''}."
          f"  {C.DIM}{counts['week']} more within a week.{C.RESET}\n")
    time.sleep(0.8)
    run_quiz(pool[:n], bp, hist, timed=False, feedback=True, title="Review")


def mode_stats(args, questions, bp, hist) -> None:
    clear()
    print(f"\n{C.BOLD}Readiness{C.RESET}")
    print(rule("="))

    by_dom = {}
    for q in questions:
        by_dom.setdefault(q.domain, []).append(q)

    print(f"\n  {C.BOLD}{'Domain':34}{'Wt':>4}  {'Bank':>5}  {'Seen':>5}  "
          f"{'Acc':>6}  Mastery{C.RESET}")
    weighted_acc, weight_seen = 0.0, 0
    for dom in sorted(bp["domains"], key=lambda d: -d["weight"]):
        qs = by_dom.get(dom["id"], [])
        seen = sum(1 for q in qs if hist["questions"].get(q.id, {}).get("seen"))
        attempts = sum(hist["questions"].get(q.id, {}).get("seen", 0) for q in qs)
        right = sum(hist["questions"].get(q.id, {}).get("correct", 0) for q in qs)
        acc = right / attempts if attempts else 0.0
        if attempts:
            weighted_acc += acc * dom["weight"]
            weight_seen += dom["weight"]
        shown = f"{acc*100:5.1f}%" if attempts else f"{C.DIM}   —  {C.RESET}"
        print(f"  {dom['name'][:34]:34}{dom['weight']:>3}%  {len(qs):>5}  "
              f"{seen:>2}/{len(qs):<2}  {shown}  "
              f"{bar(acc) if attempts else C.DIM + '·' * 24 + C.RESET}")

    if weight_seen:
        est = weighted_acc / weight_seen
        print(f"\n  {C.BOLD}Blueprint-weighted accuracy: {est*100:.1f}%{C.RESET}  "
              f"{C.DIM}(target {PASS_MARK*100:.0f}%; only domains you have "
              f"attempted){C.RESET}")
        if weight_seen < sum(d["weight"] for d in bp["domains"]) * 0.9:
            print(f"  {C.YELLOW}Coverage is partial — this estimate is optimistic "
                  f"until you have attempted every domain.{C.RESET}")

    exams = [e for e in hist["exams"] if e["mode"] == "Mock exam"]
    if exams:
        print(f"\n  {C.BOLD}Mock exam history{C.RESET}")
        for e in exams[-10:]:
            f = e["score"]
            mark = f"{C.GREEN}pass{C.RESET}" if f >= PASS_MARK else f"{C.RED}below{C.RESET}"
            print(f"    {e['at'][:16].replace('T', ' ')}   {f*100:5.1f}%  "
                  f"({int(f*e['n'])}/{e['n']})  {e['seconds']//60}m  {mark}")

    concepts, index = load_concepts()
    if concepts:
        cstats = concept_stats(questions, hist, concepts, index)
        by_id = {c["id"]: c for c in concepts}
        weight = {d["id"]: d["weight"] for d in bp["domains"]}
        scored = [(c["id"], cstats[c["id"]]) for c in concepts
                  if cstats[c["id"]]["attempts"] >= MIN_ATTEMPTS
                  and cstats[c["id"]]["acc"] < PASS_MARK]
        # Rank by exam impact: how wrong, weighted by how much the domain counts.
        scored.sort(key=lambda t: -(1 - t[1]["acc"]) * weight.get(by_id[t[0]]["domain"], 5))
        if scored:
            print(f"\n  {C.BOLD}Weakest concepts{C.RESET}  "
                  f"{C.DIM}ranked by exam impact — accuracy gap x domain weight{C.RESET}")
            for cid, st in scored[:8]:
                c = by_id[cid]
                print(f"    {C.YELLOW}→{C.RESET} {C.BOLD}{c['name']}{C.RESET}  "
                      f"{C.DIM}{st['correct']}/{st['attempts']} · "
                      f"{bp['by_id'][c['domain']]['name']} {weight.get(c['domain'], 0)}%{C.RESET}")
                print(wrap(c["summary"], width=80, indent="        " + C.DIM) + C.RESET)
                print(f"        {C.CYAN}./sim.py practice -c {cid}{C.RESET}"
                      f"{C.DIM}   ·   ./sim.py cheat -d {c['cheat']}{C.RESET}")
        unmeasured = sum(1 for c in concepts
                         if cstats[c["id"]]["attempts"] < MIN_ATTEMPTS)
        if unmeasured:
            print(f"\n  {C.DIM}{unmeasured} of {len(concepts)} concepts not yet measured "
                  f"({MIN_ATTEMPTS}+ attempts needed before accuracy means anything)."
                  f"{C.RESET}")

    counts = due_counts(questions, hist)
    print(f"\n  {C.BOLD}Review schedule{C.RESET}")
    print(f"    {C.YELLOW if counts['due'] else C.DIM}{counts['due']:>4}{C.RESET} due today"
          f"{C.DIM}   './sim.py review'{C.RESET}")
    print(f"    {C.DIM}{counts['week']:>4}{C.RESET} due within 7 days")
    print(f"    {C.DIM}{counts['new']:>4}{C.RESET} never attempted")

    cards = load_cards()
    if cards:
        today = date.today().isoformat()
        cdue = sum(1 for c in cards
                   if hist["questions"].get(c["id"], {}).get("due", "0") <= today)
        print(f"    {C.YELLOW if cdue else C.DIM}{cdue:>4}{C.RESET} flashcard(s) due"
              f"{C.DIM}   './sim.py flash'{C.RESET}")

    stale = sum(1 for qid, r in hist["questions"].items()
                if r["seen"] > r["correct"] and r.get("streak", 0) < 2)
    if stale:
        print(f"\n  {C.YELLOW}{stale}{C.RESET} question(s) in the drill queue "
              f"{C.DIM}— './sim.py drill'{C.RESET}")
    unseen = sum(1 for q in questions if not hist["questions"].get(q.id, {}).get("seen"))
    print(f"  {C.DIM}{unseen} of {len(questions)} questions never attempted.{C.RESET}\n")


def mode_cram(args, questions, bp, hist) -> None:
    pool = questions
    if args.domain:
        pool = [q for q in questions if q.domain == args.domain]
        if not pool:
            sys.exit(f"Unknown domain '{args.domain}'.")
    print(f"\n{C.BOLD}Cram sheet — {len(pool)} item(s){C.RESET}")
    last = None
    for q in sorted(pool, key=lambda q: q.id):
        if q.domain != last:
            last = q.domain
            print(f"\n{rule('=')}\n{C.BOLD}{C.CYAN}{bp['by_id'][q.domain]['name']}"
                  f"{C.RESET}  {C.DIM}({bp['by_id'][q.domain]['weight']}% of exam)"
                  f"{C.RESET}\n{rule('=')}")
        print(f"\n{C.BOLD}{q.id}{C.RESET} {C.DIM}[{', '.join(q.tags)}]{C.RESET}")
        print(wrap(q.stem, indent="  "))
        print(f"  {C.GREEN}→ {'; '.join(q.choices[i] for i in sorted(q.answer))}{C.RESET}")
        print(wrap(q.explanation, indent="    " + C.DIM) + C.RESET)
    print()


def load_cards() -> list:
    """Every cheat-sheet table row becomes a recall card: first cell asks, rest answers."""
    if not CHEATS.exists():
        return []
    cs = json.loads(CHEATS.read_text())
    cards = []
    for sec in cs["sections"]:
        for bi, block in enumerate(sec["blocks"]):
            if block["type"] != "table":
                continue
            for ri, row in enumerate(block["rows"]):
                cards.append({
                    "id": f"FC:{sec['id']}:{bi}:{ri}",
                    "deck": sec["title"],
                    "column": block["head"][0],
                    "prompt": row[0],
                    "answer": " · ".join(row[1:]),
                })
    return cards


def mode_flash(args, questions, bp, hist) -> None:
    """Self-graded recall drill over the cheat sheets, on the same scheduler."""
    cards = load_cards()
    if not cards:
        sys.exit("No cheat-sheet tables found to build cards from.")

    if args.domain:
        cards = [c for c in cards if c["id"].split(":")[1] == args.domain]
        if not cards:
            cs = json.loads(CHEATS.read_text())
            print(f"{C.BOLD}Decks{C.RESET}")
            for sec in cs["sections"]:
                print(f"  {C.CYAN}{sec['id']:<20}{C.RESET} {sec['title']}")
            sys.exit(f"\nUnknown deck '{args.domain}'.")

    today = date.today().isoformat()
    due = [c for c in cards if hist["questions"].get(c["id"], {}).get("due", "0") <= today]
    if not due:
        nxt = min((hist["questions"][c["id"]]["due"] for c in cards
                   if c["id"] in hist["questions"]), default=None)
        print(f"\n{C.GREEN}No cards due.{C.RESET}"
              f"{f' Next on {nxt}.' if nxt else ''}\n")
        return

    random.shuffle(due)
    due = due[: args.count or 20]
    right = 0
    print(f"\n{C.BOLD}{len(due)} card(s).{C.RESET} "
          f"{C.DIM}Recall it, then grade yourself honestly.{C.RESET}")

    try:
        for i, card in enumerate(due, 1):
            clear()
            print(f"\n{C.BOLD}Card {i}/{len(due)}{C.RESET}   "
                  f"{C.CYAN}{card['deck']}{C.RESET}")
            print(rule())
            print(f"{C.DIM}{card['column']}{C.RESET}")
            print(wrap(card["prompt"]))
            input(f"\n{C.DIM}Enter to reveal {C.RESET}")
            print(f"\n{C.GREEN}{wrap(card['answer'], indent='  ')}{C.RESET}")
            print(rule())
            got = input(f"Got it? [{C.GREEN}y{C.RESET}/{C.RED}n{C.RESET}] ").strip().lower()
            ok = got.startswith("y")
            right += ok
            rec = hist["questions"].setdefault(card["id"],
                                               {"seen": 0, "correct": 0, "streak": 0})
            rec["seen"] += 1
            rec["correct"] += ok
            rec["streak"] = rec.get("streak", 0) + 1 if ok else 0
            rec["last"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            schedule(rec, ok)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C.YELLOW}Stopped.{C.RESET}")

    save_history(hist)
    done = right + (len(due) - right)
    print(f"\n{C.BOLD}{right}/{i} recalled.{C.RESET}  "
          f"{C.DIM}Missed cards come back tomorrow.{C.RESET}\n")


def mode_case(args, questions, bp, hist) -> None:
    """Work a whole case study: one scenario, several linked questions."""
    cases = load_cases()
    if not cases:
        sys.exit("No case studies found in cases/")

    pick = args.domain
    if not pick:
        clear()
        print(f"\n{C.BOLD}Case studies{C.RESET}  {C.DIM}one scenario, "
              f"several linked questions{C.RESET}")
        print(rule("="))
        for i, c in enumerate(cases, 1):
            doms = sorted({q["domain"] for q in c["questions"]})
            names = ", ".join(bp["by_id"][d]["name"] for d in doms)
            done = sum(1 for q in c["questions"]
                       if hist["questions"].get(q["id"], {}).get("seen"))
            mark = f"{C.GREEN}✓{C.RESET}" if done == len(c["questions"]) else " "
            print(f"\n  {mark}{C.BOLD}{i:>2}{C.RESET}  {c['title']}  "
                  f"{C.DIM}({len(c['questions'])} questions){C.RESET}")
            print(wrap(names, width=80, indent="      " + C.DIM) + C.RESET)
        sel = input(f"\n{C.BOLD}Case number (Enter for a random one) > {C.RESET}").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(cases):
            chosen = cases[int(sel) - 1]
        else:
            chosen = random.choice(cases)
    else:
        match = [c for c in cases if c["id"].lower() == pick.lower()]
        if not match:
            sys.exit(f"Unknown case '{pick}'. Options: " +
                     ", ".join(c["id"] for c in cases))
        chosen = match[0]

    clear()
    print(f"\n{C.BOLD}{C.MAGENTA}{chosen['id']} · {chosen['title']}{C.RESET}")
    print(rule("="))
    print(wrap(chosen["scenario"]))
    print(f"\n{C.DIM}{len(chosen['questions'])} questions follow. The scenario stays "
          f"on screen.{C.RESET}")
    input(f"\n{C.BOLD}Enter to begin. {C.RESET}")

    qs = [Question(scenario=chosen["scenario"], case=chosen["id"],
                   case_title=chosen["title"], **raw) for raw in chosen["questions"]]
    run_quiz(qs, bp, hist, timed=False, feedback=True,
             title=f"Case {chosen['id']}", shuffle=False)


def mode_concepts(args, questions, bp, hist) -> None:
    """List the concept taxonomy with your measured accuracy on each."""
    concepts, index = load_concepts()
    if not concepts:
        sys.exit("concepts.json not found")
    cstats = concept_stats(questions, hist, concepts, index)
    weight = {d["id"]: d["weight"] for d in bp["domains"]}

    by_domain: dict = {}
    for c in concepts:
        by_domain.setdefault(c["domain"], []).append(c)

    print(f"\n{C.BOLD}Concept taxonomy{C.RESET}  "
          f"{C.DIM}{len(concepts)} concepts across {len(by_domain)} topic areas{C.RESET}")
    for dom in sorted(by_domain, key=lambda d: -weight.get(d, 0)):
        print(f"\n{rule('=')}")
        print(f"{C.BOLD}{C.CYAN}{bp['by_id'][dom]['name']}{C.RESET}  "
              f"{C.DIM}{weight.get(dom, 0)}% of exam{C.RESET}")
        print(rule("="))
        for c in by_domain[dom]:
            st = cstats[c["id"]]
            if st["attempts"] >= MIN_ATTEMPTS:
                acc = f"{st['acc'] * 100:5.1f}%"
                mark = (C.GREEN if st["acc"] >= PASS_MARK
                        else C.YELLOW if st["acc"] >= 0.6 else C.RED)
            else:
                acc, mark = "    — ", C.DIM
            print(f"  {mark}{acc}{C.RESET}  {C.BOLD}{c['name']:<34}{C.RESET}"
                  f"{C.DIM}{st['bank']:>3} q   {c['id']}{C.RESET}")
    print(f"\n{C.DIM}./sim.py practice -c <id>   ·   accuracy shown once a concept has "
          f"{MIN_ATTEMPTS}+ attempts{C.RESET}\n")


def mode_cheat(args, questions, bp, hist) -> None:
    """Condensed reference, rendered for a terminal."""
    if not CHEATS.exists():
        sys.exit("cheatsheet.json not found")
    cs = json.loads(CHEATS.read_text())
    sections = cs["sections"]

    if args.domain:
        want = [s for s in sections if s["id"] == args.domain]
        if not want:
            print(f"{C.BOLD}Sections{C.RESET}")
            for s in sections:
                print(f"  {C.CYAN}{s['id']:<20}{C.RESET} {s['title']}")
            sys.exit(f"\nUnknown section '{args.domain}'.")
        sections = want

    for sec in sections:
        print(f"\n{rule('=')}")
        print(f"{C.BOLD}{C.CYAN}{sec['title']}{C.RESET}")
        print(f"{C.DIM}{sec['kicker']}{C.RESET}")
        print(rule("="))
        for b in sec["blocks"]:
            print()
            if b["type"] == "table":
                print_table(b["head"], b["rows"])
            elif b["type"] == "bullets":
                for item in b["items"]:
                    print(wrap(f"{C.ACCENT}·{C.RESET} {item}", width=86, indent="    ")
                          .replace("    ", "  ", 1))
            else:
                print(wrap(f"{C.YELLOW}▍{C.RESET} {b['text']}", width=86, indent="    ")
                      .replace("    ", "  ", 1))
    print()


def mode_menu(args, questions, bp, hist) -> None:
    while True:
        clear()
        e = bp["exam"]
        print(f"\n{C.BOLD}{e['name']}{C.RESET}  {C.DIM}({e['code']}){C.RESET}")
        print(rule("="))
        print(f"  {C.DIM}{e['duration_minutes']} min · {e['question_count_min']}-"
              f"{e['question_count_max']} questions · ${e['price_usd']} · "
              f"{len(questions)} in local bank{C.RESET}\n")
        print(f"  {C.BOLD}1{C.RESET}  Mock exam        {C.DIM}timed, blueprint-weighted{C.RESET}")
        print(f"  {C.BOLD}2{C.RESET}  Practice         {C.DIM}untimed, explanations as you go{C.RESET}")
        print(f"  {C.BOLD}3{C.RESET}  Practice a domain")
        print(f"  {C.BOLD}4{C.RESET}  Review due       {C.DIM}spaced repetition — what the scheduler says is due{C.RESET}")
        print(f"  {C.BOLD}5{C.RESET}  Readiness stats")
        print(f"  {C.BOLD}6{C.RESET}  Cram sheet       {C.DIM}read every answer + explanation{C.RESET}")
        print(f"  {C.BOLD}7{C.RESET}  Cheat sheets     {C.DIM}condensed reference tables{C.RESET}")
        print(f"  {C.BOLD}8{C.RESET}  Case studies     {C.DIM}one scenario, several linked questions{C.RESET}")
        print(f"  {C.BOLD}9{C.RESET}  Flashcards       {C.DIM}recall drill over the cheat sheets{C.RESET}")
        print(f"  {C.BOLD}0{C.RESET}  Concepts         {C.DIM}taxonomy + per-concept accuracy{C.RESET}")
        print(f"  {C.BOLD}q{C.RESET}  Quit\n")
        choice = input("> ").strip().lower()
        ns = argparse.Namespace(count=None, domain=None, concept=None)
        if choice == "1":
            mode_exam(ns, questions, bp, hist)
        elif choice == "2":
            mode_practice(ns, questions, bp, hist)
        elif choice == "3":
            print()
            for i, d in enumerate(bp["domains"], 1):
                print(f"  {C.BOLD}{i:>2}{C.RESET}  {d['name']:<38}"
                      f"{C.DIM}{d['weight']}%{C.RESET}")
            sel = input("\nDomain number > ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(bp["domains"]):
                ns.domain = bp["domains"][int(sel) - 1]["id"]
                mode_practice(ns, questions, bp, hist)
        elif choice == "4":
            mode_review(ns, questions, bp, hist)
        elif choice == "5":
            mode_stats(ns, questions, bp, hist)
        elif choice == "6":
            mode_cram(ns, questions, bp, hist)
        elif choice == "7":
            cs = json.loads(CHEATS.read_text())
            print()
            for i, sec in enumerate(cs["sections"], 1):
                print(f"  {C.BOLD}{i:>2}{C.RESET}  {sec['title']}")
            sel = input("\nSection number (Enter for all) > ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(cs["sections"]):
                ns.domain = cs["sections"][int(sel) - 1]["id"]
            mode_cheat(ns, questions, bp, hist)
        elif choice == "8":
            mode_case(ns, questions, bp, hist)
        elif choice == "9":
            mode_flash(ns, questions, bp, hist)
        elif choice == "0":
            mode_concepts(ns, questions, bp, hist)
        elif choice in {"q", "quit", "exit"}:
            print()
            return
        else:
            continue
        input(f"{C.DIM}Enter for the menu {C.RESET}")


# ------------------------------------------------------------------------ main

def main() -> None:
    p = argparse.ArgumentParser(
        description="NCP-AAI certification simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  ./sim.py                          menu\n"
               "  ./sim.py exam                     full timed mock (60-70 q, 120 min)\n"
               "  ./sim.py exam -n 20               short timed mock\n"
               "  ./sim.py practice -d nvidia-platform\n"
               "  ./sim.py review                   spaced repetition: what is due today\n"
               "  ./sim.py drill                    re-ask what you missed\n"
               "  ./sim.py stats                    readiness by domain\n"
               "  ./sim.py cram -d safety-ethics-compliance\n"
               "  ./sim.py cheat                    condensed reference tables\n"
               "  ./sim.py cheat -d nvidia-platform\n"
               "  ./sim.py case                     pick a case study\n"
               "  ./sim.py case -d CS03\n"
               "  ./sim.py flash                    flashcards from the cheat sheets\n"
               "  ./sim.py flash -d nvidia-platform\n"
               "  ./sim.py concepts                 concept taxonomy + your accuracy\n"
               "  ./sim.py practice -c kv-cache\n")
    p.add_argument("mode", nargs="?", default="menu",
                   choices=["menu", "exam", "practice", "drill", "stats", "cram", "cheat", "case", "review", "flash", "concepts"])
    p.add_argument("-n", "--count", type=int, help="number of questions")
    p.add_argument("-c", "--concept", help="concept id (see `./sim.py concepts`)")
    p.add_argument("-d", "--domain",
                   help="blueprint domain id, or cheat-sheet section id for `cheat`")
    p.add_argument("--seed", type=int, help="fix the RNG for a reproducible set")
    p.add_argument("--reset", action="store_true", help="erase saved history and exit")
    args = p.parse_args()

    if args.reset:
        HISTORY.unlink(missing_ok=True)
        print("History cleared.")
        return
    if args.seed is not None:
        random.seed(args.seed)

    bp, questions, hist = load_blueprint(), load_questions(), load_history()
    migrate(hist)
    try:
        globals()[f"mode_{args.mode}"](args, questions, bp, hist)
    except (KeyboardInterrupt, EOFError):
        save_history(hist)
        print(f"\n{C.DIM}Progress saved.{C.RESET}\n")


if __name__ == "__main__":
    main()
