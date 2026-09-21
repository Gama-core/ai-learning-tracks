#!/usr/bin/env python3
"""Certification discovery, shared by the simulator and the build scripts.

Each certification is a directory under certs/ holding its own blueprint,
question bank, cases, cheat sheets and concept taxonomy. Nothing in the tooling
knows which certification it is working on beyond what it reads from there.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERTS_DIR = ROOT / "certs"
PROGRESS_DIR = ROOT / ".progress"
DEFAULT_FILE = PROGRESS_DIR / "last-cert"


class Cert:
    """One certification's content, resolved from certs/<id>/."""

    def __init__(self, cert_id: str):
        self.id = cert_id
        self.dir = CERTS_DIR / cert_id
        if not self.dir.is_dir():
            sys.exit(f"No certification '{cert_id}'. Available: "
                     + ", ".join(c.id for c in available()))
        self.blueprint_path = self.dir / "blueprint.json"
        self.concepts_path = self.dir / "concepts.json"
        self.cheats_path = self.dir / "cheatsheet.json"
        self.bank_dir = self.dir / "bank"
        self.case_dir = self.dir / "cases"
        self.progress_path = PROGRESS_DIR / f"{cert_id}.json"

    @property
    def blueprint(self) -> dict:
        return json.loads(self.blueprint_path.read_text())

    @property
    def name(self) -> str:
        return self.blueprint["exam"]["name"]

    @property
    def code(self) -> str:
        return self.blueprint["exam"].get("code", self.id)

    def counts(self) -> dict:
        bank = sum(len(json.loads(p.read_text())["questions"])
                   for p in self.bank_dir.glob("*.json"))
        cases = sorted(self.case_dir.glob("*.json")) if self.case_dir.is_dir() else []
        case_q = sum(len(json.loads(p.read_text())["questions"]) for p in cases)
        return {"bank": bank, "cases": len(cases), "case_questions": case_q,
                "total": bank + case_q}


def available() -> list:
    """Every certification directory that has a blueprint, in name order."""
    if not CERTS_DIR.is_dir():
        return []
    found = [Cert(p.name) for p in sorted(CERTS_DIR.iterdir())
             if (p / "blueprint.json").is_file()]
    return found


def remember(cert_id: str) -> None:
    PROGRESS_DIR.mkdir(exist_ok=True)
    DEFAULT_FILE.write_text(cert_id)


def resolve(cert_id: str | None = None) -> Cert:
    """Pick a certification: the one asked for, the last one used, or the only one."""
    certs = available()
    if not certs:
        sys.exit(f"No certifications found under {CERTS_DIR}")
    if cert_id:
        return Cert(cert_id)
    if DEFAULT_FILE.is_file():
        last = DEFAULT_FILE.read_text().strip()
        if any(c.id == last for c in certs):
            return Cert(last)
    return certs[0]
