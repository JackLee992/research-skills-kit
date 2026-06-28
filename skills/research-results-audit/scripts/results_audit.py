#!/usr/bin/env python3
"""Audit research result text for statistical and reproducibility risks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


P_RE = re.compile(r"\bp\s*(?:=|<|>)\s*\.?\d+", re.IGNORECASE)
EFFECT_RE = re.compile(r"(cohen|eta|r\^?2|odds ratio|effect size|d\s*=|η|eta squared)", re.IGNORECASE)
CAUSAL_RE = re.compile(r"\b(caused|causes|led to|leads to|resulted in|improved|reduced|increased|decreased)\b", re.IGNORECASE)
ASSUMPTION_RE = re.compile(r"(levene|shapiro|normality|variance|assumption|welch|kruskal|mann-whitney)", re.IGNORECASE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit statistical result prose and output reproducibility.")
    parser.add_argument("report", type=Path)
    parser.add_argument("--hash", nargs="*", type=Path, default=[])
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/audit"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    text = args.report.read_text(encoding="utf-8", errors="ignore")
    warnings = []
    p_values = P_RE.findall(text)
    if p_values and not EFFECT_RE.search(text):
        warnings.append({"severity": "CAUTION", "type": "effect_size_missing", "detail": "p-values detected without obvious effect-size wording."})
    if CAUSAL_RE.search(text):
        warnings.append({"severity": "CAUTION", "type": "causal_language", "detail": "Causal verbs detected; confirm design supports causal inference."})
    if p_values and not ASSUMPTION_RE.search(text):
        warnings.append({"severity": "NOTE", "type": "assumption_context_missing", "detail": "Statistical tests detected without obvious assumption or sensitivity-test wording."})

    hashes = []
    for path in args.hash:
        if path.exists():
            hashes.append({"file": str(path), "sha256": sha256(path), "status": "HASHED"})
        else:
            hashes.append({"file": str(path), "sha256": "", "status": "MISSING"})
            warnings.append({"severity": "CAUTION", "type": "missing_hash_file", "detail": str(path)})

    result = {"report": str(args.report), "p_value_mentions": p_values, "warnings": warnings, "hashes": hashes}
    (args.out_dir / "results_audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    lines = ["# Results Audit", "", f"Report: `{args.report}`", "", f"Overall: `{'PASS' if not warnings else 'CHECK'}`", ""]
    lines += ["## Warnings", ""]
    if warnings:
        lines += ["| Severity | Type | Detail |", "| --- | --- | --- |"]
        for item in warnings:
            lines.append(f"| `{item['severity']}` | `{item['type']}` | {item['detail']} |")
    else:
        lines.append("No warnings detected.")
    if hashes:
        lines += ["", "## Reproducibility Hashes", "", "| File | SHA-256 | Status |", "| --- | --- | --- |"]
        for item in hashes:
            lines.append(f"| `{item['file']}` | `{item['sha256']}` | `{item['status']}` |")
    (args.out_dir / "results_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.out_dir / "results_audit.md")


if __name__ == "__main__":
    main()

