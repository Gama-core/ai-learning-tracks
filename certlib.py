#!/usr/bin/env python3
"""Learning-track discovery, shared by the simulator and the build scripts.

Each track is a directory under tracks/ holding its own topic blueprint,
question bank, cases, cheat sheets and concept taxonomy. Nothing in the tooling
knows which field it is working on beyond what it reads from there.

A track may declare a `certification` block when its topics happen to align with
a published exam. That is alignment metadata, not the point of the track.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACKS_DIR = ROOT / "tracks"
PROGRESS_DIR = ROOT / ".progress"
DEFAULT_FILE = PROGRESS_DIR / "last-track"


class Track:
    """One learning track's content, resolved from tracks/<id>/."""

    def __init__(self, track_id: str):
        self.id = track_id
        self.dir = TRACKS_DIR / track_id
        if not self.dir.is_dir():
            sys.exit(f"No track '{track_id}'. Available: "
                     + ", ".join(t.id for t in available()))
        self.blueprint_path = self.dir / "blueprint.json"
        self.concepts_path = self.dir / "concepts.json"
        self.cheats_path = self.dir / "cheatsheet.json"
        self.bank_dir = self.dir / "bank"
        self.case_dir = self.dir / "cases"
        self.progress_path = PROGRESS_DIR / f"{track_id}.json"

    @property
    def blueprint(self) -> dict:
        return json.loads(self.blueprint_path.read_text())

    @property
    def meta(self) -> dict:
        return self.blueprint["track"]

    @property
    def name(self) -> str:
        return self.meta["name"]

    @property
    def tagline(self) -> str:
        return self.meta.get("tagline", "")

    @property
    def certification(self) -> dict | None:
        """The exam this track's topics align with, if any."""
        return self.meta.get("certification")

    def counts(self) -> dict:
        bank = sum(len(json.loads(p.read_text())["questions"])
                   for p in self.bank_dir.glob("*.json"))
        cases = sorted(self.case_dir.glob("*.json")) if self.case_dir.is_dir() else []
        case_q = sum(len(json.loads(p.read_text())["questions"]) for p in cases)
        return {"bank": bank, "cases": len(cases), "case_questions": case_q,
                "total": bank + case_q}


def available() -> list:
    """Every track directory that has a blueprint, in directory order."""
    if not TRACKS_DIR.is_dir():
        return []
    return [Track(p.name) for p in sorted(TRACKS_DIR.iterdir())
            if (p / "blueprint.json").is_file()]


def remember(track_id: str) -> None:
    PROGRESS_DIR.mkdir(exist_ok=True)
    DEFAULT_FILE.write_text(track_id)


def resolve(track_id: str | None = None) -> Track:
    """Pick a track: the one asked for, the last one used, or the first."""
    tracks = available()
    if not tracks:
        sys.exit(f"No tracks found under {TRACKS_DIR}")
    if track_id:
        return Track(track_id)
    if DEFAULT_FILE.is_file():
        last = DEFAULT_FILE.read_text().strip()
        if any(t.id == last for t in tracks):
            return Track(last)
    return tracks[0]


# Backwards-compatible aliases for the previous certification-centric naming.
Cert = Track
