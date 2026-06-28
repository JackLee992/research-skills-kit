#!/usr/bin/env python3
"""Smoke test for the installed research-upstream-router helper."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills" / "research-upstream-router" / "scripts" / "list_upstream_skills.py"


def main() -> int:
    result = subprocess.run(
        [
            sys.executable,
            str(HELPER),
            "--checkout",
            str(ROOT),
            "--profile",
            "core",
            "--format",
            "json",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    rows = json.loads(result.stdout)
    names = {row["name"] for row in rows}
    required = {
        "statistical-analysis",
        "statistical-power",
        "scientific-visualization",
        "nature-figure",
        "academic-research-suite",
        "paper-spine",
        "image-to-editable-ppt",
    }
    missing = sorted(required - names)
    if missing:
        raise AssertionError(f"Missing expected upstream skills: {missing}")
    print(f"router helper PASS ({len(rows)} core skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
