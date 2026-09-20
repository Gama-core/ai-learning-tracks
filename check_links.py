#!/usr/bin/env python3
"""Check every URL in the study material still resolves.

NVIDIA restructures its docs regularly; this catches it before you follow a
dead reference mid-study. Exit code 1 if anything is broken.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# Hosts that rate-limit automated checks. A 429 from these is not a dead link.
TOLERATE_429 = {"certificationpractice.com"}


def sources() -> dict:
    """Map every URL to the files that reference it."""
    found: dict = {}
    for path in [ROOT / "RESOURCES.md", ROOT / "README.md", ROOT / "CHEATSHEET.md"]:
        if path.exists():
            for url in re.findall(r"https?://[^\s)>\]|\"]+", path.read_text()):
                found.setdefault(url.rstrip(".,"), set()).add(path.name)
    for path in list((ROOT / "bank").glob("*.json")) + list((ROOT / "cases").glob("*.json")):
        data = json.loads(path.read_text())
        for q in data["questions"]:
            found.setdefault(q["ref"], set()).add(path.name)
    return found


def check(url: str, timeout: int = 20) -> tuple:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return url, resp.status, ""
    except urllib.error.HTTPError as exc:
        return url, exc.code, exc.reason
    except Exception as exc:                       # DNS, TLS, timeout
        return url, 0, type(exc).__name__


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-j", "--jobs", type=int, default=8)
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    refs = sources()
    urls = sorted(refs)
    print(f"Checking {len(urls)} URLs across the study material...")

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(check, urls))

    broken, tolerated = [], []
    for url, status, reason in results:
        if status == 200:
            continue
        host = url.split("/")[2] if "://" in url else ""
        if status == 429 and any(host.endswith(h) for h in TOLERATE_429):
            tolerated.append((url, status))
            continue
        broken.append((url, status, reason, sorted(refs[url])))

    for url, status in tolerated:
        print(f"  rate-limited (not a failure)  {url}")
    for url, status, reason, where in broken:
        print(f"  BROKEN {status or 'ERR'}  {url}")
        print(f"         referenced by: {', '.join(where)}")

    if broken:
        print(f"\n{len(broken)} broken link(s).")
        sys.exit(1)
    if not args.quiet:
        print(f"All {len(urls)} links OK"
              f"{f' ({len(tolerated)} rate-limited)' if tolerated else ''}.")


if __name__ == "__main__":
    main()
