#!/usr/bin/env python3
"""Inline blueprint.json + bank/*.json into web/template.html -> web/simulator.html.

Run after editing the question bank so the web simulator matches the CLI.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
bp = json.loads((ROOT / "blueprint.json").read_text())

questions = []
for path in sorted((ROOT / "bank").glob("*.json")):
    bank = json.loads(path.read_text())
    for q in bank["questions"]:
        q["domain"] = bank["domain"]
        questions.append(q)

cases = []
for path in sorted((ROOT / "cases").glob("*.json")):
    case = json.loads(path.read_text())
    cases.append({"id": case["id"], "title": case["title"],
                  "scenario": case["scenario"],
                  "questions": [q["id"] for q in case["questions"]]})
    for q in case["questions"]:
        q["case"] = case["id"]
        questions.append(q)

concepts = json.loads((ROOT / "concepts.json").read_text())["concepts"]
cheats = json.loads((ROOT / "cheatsheet.json").read_text())
cards = []
for sec in cheats["sections"]:
    for bi, block in enumerate(sec["blocks"]):
        if block["type"] != "table":
            continue
        for ri, row in enumerate(block["rows"]):
            cards.append({"id": f"FC:{sec['id']}:{bi}:{ri}", "deck": sec["id"],
                          "deckName": sec["title"], "column": block["head"][0],
                          "prompt": row[0], "answer": " · ".join(row[1:])})

payload = {
    "exam": bp["exam"],
    "cheats": cheats,
    "cases": cases,
    "concepts": concepts,
    "cards": cards,
    "domains": [{k: v for k, v in d.items() if k != "note"} for d in bp["domains"]],
    "questions": questions,
}

template = (ROOT / "web" / "template.html").read_text()
marker = "/*__DATA__*/"
if marker not in template:
    raise SystemExit("template.html is missing the /*__DATA__*/ marker")

out = template.replace(marker, json.dumps(payload, separators=(",", ":"), ensure_ascii=False))
dest = ROOT / "web" / "simulator.html"
dest.write_text(out)
print(f"{dest.relative_to(ROOT)}  {len(questions)} questions  "
      f"{len(cases)} cases  {len(cards)} cards  {len(concepts)} concepts  "
      f"{dest.stat().st_size // 1024} KB")
