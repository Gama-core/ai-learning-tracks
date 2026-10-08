#!/usr/bin/env python3
"""Validate a learning track's content. Run after editing bank/*.json."""
import json
import re
import sys
from pathlib import Path

import certlib

ROOT = Path(__file__).resolve().parent
TRACK = certlib.resolve(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None)
bp = json.loads(TRACK.blueprint_path.read_text())
domains = {d["id"]: d for d in bp["domains"]}

errors, warnings, seen_ids, counts = [], [], set(), {}

for path in sorted(TRACK.bank_dir.glob("*.json")):
    try:
        bank = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON — {exc}")
        continue

    domain = bank.get("domain")
    if domain not in domains:
        errors.append(f"{path.name}: domain '{domain}' is not in blueprint.json")
        continue
    if path.stem != domain:
        errors.append(f"{path.name}: filename does not match domain '{domain}'")

    prefix = domains[domain]["prefix"]
    counts[domain] = len(bank["questions"])

    for q in bank["questions"]:
        qid = q.get("id", "<missing id>")
        where = f"{path.name}:{qid}"
        if qid in seen_ids:
            errors.append(f"{where}: duplicate id")
        seen_ids.add(qid)
        if not re.fullmatch(rf"{prefix}-\d{{3}}", qid):
            errors.append(f"{where}: id should look like {prefix}-001")
        for field in ("type", "difficulty", "stem", "choices", "answer",
                      "explanation", "tags", "ref"):
            if field not in q:
                errors.append(f"{where}: missing '{field}'")
        if errors and errors[-1].startswith(where + ": missing"):
            continue
        if q["type"] not in ("single", "multi"):
            errors.append(f"{where}: type must be 'single' or 'multi'")
        if q["difficulty"] not in ("easy", "medium", "hard"):
            errors.append(f"{where}: difficulty must be easy/medium/hard")
        if len(q["choices"]) != 4:
            errors.append(f"{where}: needs exactly 4 choices, has {len(q['choices'])}")
        if len(set(q["choices"])) != len(q["choices"]):
            errors.append(f"{where}: duplicate choice text")
        if not q["answer"] or any(not isinstance(a, int) or not 0 <= a < 4 for a in q["answer"]):
            errors.append(f"{where}: answer indices must be 0-3")
        elif len(set(q["answer"])) != len(q["answer"]):
            errors.append(f"{where}: repeated answer index")
        elif (len(q["answer"]) > 1) != (q["type"] == "multi"):
            errors.append(f"{where}: type '{q['type']}' disagrees with "
                          f"{len(q['answer'])} answer(s)")
        if q["type"] == "multi" and "TWO" not in q["stem"].upper():
            warnings.append(f"{where}: multi-select stem does not say 'Select TWO'")
        if len(q["explanation"]) < 120:
            warnings.append(f"{where}: explanation is thin ({len(q['explanation'])} chars)")
        if not str(q["ref"]).startswith("http"):
            errors.append(f"{where}: ref must be a URL")
        if not q["tags"]:
            warnings.append(f"{where}: no tags")

# ---- case studies --------------------------------------------------------
case_dir = TRACK.case_dir
case_q = 0
if case_dir.exists():
    for path in sorted(case_dir.glob("*.json")):
        try:
            case = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: invalid JSON — {exc}")
            continue
        if path.stem != case.get("id"):
            errors.append(f"{path.name}: filename does not match id '{case.get('id')}'")
        if len(case.get("scenario", "")) < 200:
            warnings.append(f"{path.name}: scenario is thin "
                            f"({len(case.get('scenario', ''))} chars)")
        if len(case.get("questions", [])) < 3:
            errors.append(f"{path.name}: a case needs at least 3 linked questions")
        for q in case.get("questions", []):
            qid = q.get("id", "<missing>")
            where = f"{path.name}:{qid}"
            case_q += 1
            if qid in seen_ids:
                errors.append(f"{where}: duplicate id")
            seen_ids.add(qid)
            if not re.fullmatch(rf"{case['id']}-\d+", qid):
                errors.append(f"{where}: id should look like {case['id']}-1")
            if q.get("domain") not in domains:
                errors.append(f"{where}: domain '{q.get('domain')}' not in blueprint")
            if len(q.get("choices", [])) != 4:
                errors.append(f"{where}: needs exactly 4 choices")
            if (len(q.get("answer", [])) > 1) != (q.get("type") == "multi"):
                errors.append(f"{where}: type disagrees with answer count")
            if not str(q.get("ref", "")).startswith("http"):
                errors.append(f"{where}: ref must be a URL")
            if len(q.get("explanation", "")) < 120:
                warnings.append(f"{where}: explanation is thin")

# ---- cheat sheet ---------------------------------------------------------
cheat_path = TRACK.cheats_path
cards = 0
if cheat_path.exists():
    cs = json.loads(cheat_path.read_text())
    ids = [sec["id"] for sec in cs["sections"]]
    if len(set(ids)) != len(ids):
        errors.append("cheatsheet.json: duplicate section id")
    for sec in cs["sections"]:
        for bi, block in enumerate(sec["blocks"]):
            where = f"cheatsheet.json:{sec['id']}[{bi}]"
            if block["type"] == "table":
                width = len(block["head"])
                for ri, row in enumerate(block["rows"]):
                    if len(row) != width:
                        errors.append(f"{where}: row {ri} has {len(row)} cells, "
                                      f"header has {width}")
                cards += len(block["rows"])
            elif block["type"] not in ("bullets", "note"):
                errors.append(f"{where}: unknown block type '{block['type']}'")

# ---- concept taxonomy ----------------------------------------------------
concepts_path = TRACK.concepts_path
n_concepts = 0
if concepts_path.exists():
    cons = json.loads(concepts_path.read_text())["concepts"]
    n_concepts = len(cons)
    cheat_ids = {sec["id"] for sec in cs["sections"]} if cheat_path.exists() else set()
    cids, tag_index = set(), {}
    for c in cons:
        where = f"concepts.json:{c['id']}"
        if c["id"] in cids:
            errors.append(f"{where}: duplicate concept id")
        cids.add(c["id"])
        if c["domain"] not in domains:
            errors.append(f"{where}: domain '{c['domain']}' not in blueprint")
        if cheat_ids and c["cheat"] not in cheat_ids:
            errors.append(f"{where}: cheat section '{c['cheat']}' does not exist")
        if not c.get("summary") or not c.get("tags"):
            errors.append(f"{where}: needs a summary and at least one tag")
        for tag in c["tags"]:
            tag_index.setdefault(tag, []).append(c["id"])

    # Every tag a question uses must belong to a concept, or the taxonomy has
    # silently stopped covering the bank.
    used_tags, no_concept, per_concept = set(), [], {c["id"]: 0 for c in cons}
    for path in (list(TRACK.bank_dir.glob("*.json"))
                 + list(TRACK.case_dir.glob("*.json"))):
        for q in json.loads(path.read_text())["questions"]:
            used_tags.update(q["tags"])
            mapped = {cid for t in q["tags"] for cid in tag_index.get(t, [])}
            if not mapped:
                no_concept.append(q["id"])
            for cid in mapped:
                per_concept[cid] += 1

    for tag in sorted(used_tags - set(tag_index)):
        errors.append(f"concepts.json: tag '{tag}' is used by questions but "
                      f"belongs to no concept")
    for qid in no_concept:
        errors.append(f"{qid}: maps to no concept")
    for tag in sorted(set(tag_index) - used_tags):
        warnings.append(f"concepts.json: tag '{tag}' is declared but unused")
    for cid, n in sorted(per_concept.items(), key=lambda kv: kv[1]):
        if n < 4:
            warnings.append(f"concepts.json:{cid}: only {n} question(s) — "
                            f"too thin to report accuracy on")

# ---- chapter summaries ---------------------------------------------------
VISUALS = {"spectrum", "ladder", "flow", "topologies", "compare", "map", "cards",
           "stack", "triad", "matrix", "trace", "bar"}
# A chapter should stay a high-level view; past this it is repeating the cheat sheet.
SLIDES_RECOMMENDED = 7
SHAPES = {"single", "supervisor", "hierarchical", "network", "pipeline"}
n_slides = 0
if TRACK.summary_path.exists():
    summary = json.loads(TRACK.summary_path.read_text())
    concept_ids = ({c["id"] for c in json.loads(concepts_path.read_text())["concepts"]}
                   if concepts_path.exists() else set())
    seen_ch = set()
    for ch in summary.get("chapters", []):
        where = f"summary.json:{ch.get('domain')}"
        if ch.get("domain") not in domains:
            errors.append(f"{where}: domain not in blueprint")
        if ch.get("domain") in seen_ch:
            errors.append(f"{where}: chapter appears twice")
        seen_ch.add(ch.get("domain"))
        slides = ch.get("slides", [])
        if len(slides) < 2:
            errors.append(f"{where}: needs at least 2 slides, has {len(slides)}")
        elif len(slides) > SLIDES_RECOMMENDED:
            warnings.append(f"{where}: {len(slides)} slides; {SLIDES_RECOMMENDED} or fewer "
                            f"keeps a chapter high-level")
        # Every concept in the chapter's topic area should surface on some slide,
        # or the summary has silently skipped part of the chapter.
        linked = {cid for s in slides for cid in s.get("concepts", [])}
        if concepts_path.exists():
            for c in json.loads(concepts_path.read_text())["concepts"]:
                if c["domain"] == ch.get("domain") and c["id"] not in linked:
                    warnings.append(f"{where}: concept '{c['id']}' appears on no slide")
        for si, s in enumerate(slides):
            n_slides += 1
            at = f"{where}[{si}]"
            if not s.get("title") or not s.get("lede"):
                errors.append(f"{at}: needs a title and a lede")
            v = s.get("visual", {})
            if v.get("type") not in VISUALS:
                errors.append(f"{at}: unknown visual '{v.get('type')}'")
            if v.get("type") == "topologies":
                for it in v.get("items", []):
                    if it.get("shape") not in SHAPES:
                        errors.append(f"{at}: unknown topology shape '{it.get('shape')}'")
            if v.get("type") == "triad" and len(v.get("nodes", [])) != 3:
                errors.append(f"{at}: a triad needs exactly 3 nodes")
            if v.get("type") == "map":
                for row in v.get("rows", []):
                    if len(row) != 2:
                        errors.append(f"{at}: map rows need 2 cells")
            if v.get("type") == "matrix":
                for row in v.get("rows", []):
                    if len(row) != len(v.get("head", [])):
                        errors.append(f"{at}: matrix row width does not match its header")
            for cid in s.get("concepts", []):
                if cid not in concept_ids:
                    errors.append(f"{at}: concept '{cid}' does not exist")

total = sum(counts.values())
for d in bp["domains"]:
    have = counts.get(d["id"], 0)
    # A 65-question exam should never exhaust a domain's questions.
    need = round(65 * d["weight"] / sum(x["weight"] for x in bp["domains"]))
    if have < need:
        errors.append(f"{d['id']}: {have} questions, but a 65-question exam "
                      f"needs {need}")

print(f"[{TRACK.name}] {total} bank questions across {len(counts)} topic areas, "
      f"{case_q} case questions, {cards} flashcards, {n_concepts} concepts, "
      f"{n_slides} summary slides")
for w in warnings:
    print(f"  warn  {w}")
for e in errors:
    print(f"  FAIL  {e}")
print("OK" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
