#!/usr/bin/env python3
"""Compatibility wrapper for the router skill's upstream listing helper."""

from __future__ import annotations

from pathlib import Path
import runpy


HELPER = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "research-upstream-router"
    / "scripts"
    / "list_upstream_skills.py"
)

runpy.run_path(str(HELPER), run_name="__main__")
