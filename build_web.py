#!/usr/bin/env python3
"""Build the web simulator for each certification under certs/.

Emits two targets per certification into web/<cert-id>/:

  simulator.html  for the claude.ai artifact, where the platform supplies the
                  surrounding document, so this file starts at <title>
  index.html      a complete standalone document for an ordinary web server

Served from a plain web server, simulator.html would render in quirks mode with
a guessed character encoding and no mobile viewport; index.html is the one to
deploy. Pass a certification id to build only that one.
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

import certlib

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "web" / "template.html"
MARKER = "/*__DATA__*/"


def collect(cert) -> dict:
    """Everything the page needs, inlined so it makes no runtime requests."""
    bp = json.loads(cert.blueprint_path.read_text())

    questions = []
    for path in sorted(cert.bank_dir.glob("*.json")):
        bank = json.loads(path.read_text())
        for q in bank["questions"]:
            q["domain"] = bank["domain"]
            questions.append(q)

    cases = []
    if cert.case_dir.is_dir():
        for path in sorted(cert.case_dir.glob("*.json")):
            case = json.loads(path.read_text())
            cases.append({"id": case["id"], "title": case["title"],
                          "scenario": case["scenario"],
                          "questions": [q["id"] for q in case["questions"]]})
            for q in case["questions"]:
                q["case"] = case["id"]
                questions.append(q)

    cheats = json.loads(cert.cheats_path.read_text())
    cards = []
    for sec in cheats["sections"]:
        for bi, block in enumerate(sec["blocks"]):
            if block["type"] != "table":
                continue
            for ri, row in enumerate(block["rows"]):
                cards.append({"id": f"FC:{sec['id']}:{bi}:{ri}", "deck": sec["id"],
                              "deckName": sec["title"], "column": block["head"][0],
                              "prompt": row[0], "answer": " · ".join(row[1:])})

    return {
        "cert": cert.id,
        "exam": bp["exam"],
        "domains": [{k: v for k, v in d.items() if k != "note"} for d in bp["domains"]],
        "questions": questions,
        "cases": cases,
        "cheats": cheats,
        "cards": cards,
        "concepts": json.loads(cert.concepts_path.read_text())["concepts"],
    }


def standalone(page: str, payload: dict) -> str:
    """Wrap the artifact page in a complete document for self-hosting."""
    title = re.search(r"<title>(.*?)</title>", page).group(1)
    mark = re.search(r'<svg viewBox="31\.5[^>]*>.*?</svg>', page, re.S)
    favicon = ""
    if mark:
        icon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="31.5 13 78.5 75.5">'
                + mark.group(0).split(">", 1)[1])
        favicon = ('\n<link rel="icon" href="data:image/svg+xml,'
                   + urllib.parse.quote(icon) + '">')
    desc = (f"Practice simulator for {payload['exam']['name']}. "
            f"{len(payload['questions'])} questions with spaced repetition, "
            f"case studies and cheat sheets.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">{favicon}
<style>
  :root{{padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px)}}
  html,body{{margin:0}}
  body{{font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; background:#fff}}
  img{{max-width:100%}}
  [hidden]{{display:none!important}}
</style>
{page}
</body>
</html>
"""


def build(cert) -> None:
    payload = collect(cert)
    template = TEMPLATE.read_text()
    if MARKER not in template:
        raise SystemExit(f"{TEMPLATE.name} is missing the {MARKER} marker")
    page = template.replace(
        MARKER, json.dumps(payload, separators=(",", ":"), ensure_ascii=False))

    outdir = ROOT / "web" / cert.id
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "simulator.html").write_text(page)
    (outdir / "index.html").write_text(standalone(page, payload))

    kb = (outdir / "index.html").stat().st_size // 1024
    print(f"  {cert.id:12} {len(payload['questions']):>4} questions · "
          f"{len(payload['cases']):>2} cases · {len(payload['cards']):>3} cards · "
          f"{len(payload['concepts']):>2} concepts · {kb} KB")


if __name__ == "__main__":
    targets = [certlib.resolve(sys.argv[1])] if len(sys.argv) > 1 else certlib.available()
    print(f"Building {len(targets)} certification(s) -> web/<cert-id>/")
    for c in targets:
        build(c)
