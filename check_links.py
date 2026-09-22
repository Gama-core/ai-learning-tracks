#!/usr/bin/env python3
"""Check every URL in the study material still resolves.

NVIDIA restructures its docs regularly; this catches it before you follow a
dead reference mid-study. Exit code 1 if anything is broken.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import certlib

ROOT = Path(__file__).resolve().parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# Requires a signed-in session, so an anonymous check proves nothing.
SKIP_HOSTS = {"claude.ai"}

# A 403 or 429 means the host refused the robot, not that the page is gone.
# Reported, never fatal. A 404, 410, 5xx or DNS failure is a real break.
BLOCKED_CODES = {401, 403, 429}

# Hosts that refuse datacenter traffic with a 404 instead of a 403, making a
# block indistinguishable from a dead page. Kept deliberately tiny: each entry
# is a host verified by hand to serve the page correctly to a normal browser.
# fda.gov: returns 200 from a residential connection, 404 from GitHub runners.
BLOCKS_WITH_404 = {"fda.gov"}


def is_placeholder(url: str) -> bool:
    """Skip illustrative URLs in documentation samples (https://..., example.com)."""
    return ("..." in url or url.rstrip("/.") in {"https:/", "http:/"}
            or len(url) < 14 or "example.com" in url)


def sources() -> dict:
    """Map every URL to the files that reference it."""
    found: dict = {}
    docs = [ROOT / "README.md"]
    for track in certlib.available():
        docs += [track.dir / "RESOURCES.md", track.dir / "CHEATSHEET.md"]
    for path in docs:
        if path.exists():
            for url in re.findall(r"https?://[^\s)>\]|\"]+", path.read_text()):
                found.setdefault(url.rstrip(".,"), set()).add(path.name)
    for track in certlib.available():
        paths = list(track.bank_dir.glob("*.json"))
        if track.case_dir.is_dir():
            paths += list(track.case_dir.glob("*.json"))
        for path in paths:
            for q in json.loads(path.read_text())["questions"]:
                found.setdefault(q["ref"], set()).add(f"{track.id}/{path.name}")
    return found


def check(url: str, timeout: int = 20, attempts: int = 3) -> tuple:
    """Fetch a URL, retrying transient failures.

    A timeout, reset connection or 5xx is not evidence that a page is gone, and
    a single-shot check turns one bad moment into a failed build. Only a stable
    result is reported.
    """
    last = (url, 0, "unknown")
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, resp.status, ""
        except urllib.error.HTTPError as exc:
            last = (url, exc.code, exc.reason)
            if exc.code < 500:                     # 404, 403, 429: a real answer
                return last
        except Exception as exc:                   # DNS, TLS, timeout, reset
            last = (url, 0, type(exc).__name__)
        if attempt < attempts - 1:
            time.sleep(1.5 * (attempt + 1) + random.random())
    return last


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-j", "--jobs", type=int, default=8)
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    refs = sources()
    skipped = [u for u in refs
               if is_placeholder(u) or any(h in u.split("/")[2] for h in SKIP_HOSTS)]
    for u in skipped:
        refs.pop(u)
    urls = sorted(refs)
    print(f"Checking {len(urls)} URLs across the study material"
          f"{f' ({len(skipped)} skipped: placeholders and auth-only)' if skipped else ''}...")

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(check, urls))

    broken, tolerated = [], []
    for url, status, reason in results:
        if status == 200:
            continue
        host = url.split("/")[2] if "://" in url else ""
        if status in BLOCKED_CODES or (
                status == 404 and any(host.endswith(h) for h in BLOCKS_WITH_404)):
            tolerated.append((url, status))
            continue
        broken.append((url, status, reason, sorted(refs[url])))

    for url, status in tolerated:
        print(f"  {status} blocked the checker, not verified  {url}")
    for url, status, reason, where in broken:
        print(f"  BROKEN {status or 'ERR'}  {url}")
        print(f"         referenced by: {', '.join(where)}")

    if broken:
        print(f"\n{len(broken)} broken link(s).")
        sys.exit(1)
    if not args.quiet:
        print(f"All {len(urls)} links OK"
              f"{f' ({len(tolerated)} unverifiable: host blocked the checker)' if tolerated else ''}.")


if __name__ == "__main__":
    main()
