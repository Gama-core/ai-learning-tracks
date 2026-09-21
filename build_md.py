#!/usr/bin/env python3
"""Render cheatsheet.json to CHEATSHEET.md (printable / greppable)."""
import json
from pathlib import Path

import sys
import certlib

ROOT = Path(__file__).resolve().parent
CERT = certlib.resolve(sys.argv[1] if len(sys.argv) > 1 else None)
cs = json.loads(CERT.cheats_path.read_text())

out = [f"# {cs['title']}",
       "",
       "Condensed reference for the NVIDIA-Certified Professional: Agentic AI LLMs exam.",
       "Generated from `cheatsheet.json` by `build_md.py` — edit the JSON, not this file.",
       "Also available in the web simulator under **Cheat sheets**, and in the terminal via",
       "`./sim.py cheat`.",
       ""]

out.append("## Contents")
out.append("")
for i, sec in enumerate(cs["sections"], 1):
    anchor = sec["title"].lower().replace(" ", "-").replace(",", "").replace("/", "")
    out.append(f"{i}. [{sec['title']}](#{anchor}) — *{sec['kicker']}*")
out.append("")

for sec in cs["sections"]:
    out += ["---", "", f"## {sec['title']}", "", f"*{sec['kicker']}*", ""]
    for b in sec["blocks"]:
        if b["type"] == "table":
            out.append("| " + " | ".join(b["head"]) + " |")
            out.append("|" + "---|" * len(b["head"]))
            for row in b["rows"]:
                out.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")
            out.append("")
        elif b["type"] == "bullets":
            out += [f"- {i}" for i in b["items"]] + [""]
        else:
            out += [f"> {b['text']}", ""]

dest = CERT.dir / "CHEATSHEET.md"
dest.write_text("\n".join(out).rstrip() + "\n")
print(f"{dest.relative_to(ROOT)}  {len(cs['sections'])} sections  {dest.stat().st_size // 1024} KB")
