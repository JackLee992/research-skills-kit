#!/usr/bin/env python3
"""QA checks for publication figure exports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def inspect_file(path: Path) -> dict:
    info = {"file": str(path), "exists": path.exists(), "size_bytes": path.stat().st_size if path.exists() else 0}
    if not path.exists():
        info["status"] = "missing"
        return info
    if path.suffix.lower() == ".svg":
        text = path.read_text(errors="ignore")
        info["svg_text_elements"] = text.count("<text")
        info["svg_path_elements"] = text.count("<path")
        info["editable_text_ok"] = info["svg_text_elements"] > 0
    if path.suffix.lower() in {".png", ".tif", ".tiff", ".jpg", ".jpeg"}:
        img = Image.open(path).convert("RGB")
        arr = np.asarray(img)
        info["width_px"], info["height_px"] = img.size
        info["pixel_std"] = float(arr.std())
        info["nonblank_ok"] = bool(arr.std() > 1.0)
    return info


def main() -> None:
    parser = argparse.ArgumentParser(description="Check exported figure files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("outputs/figures/figure_qa_report.md"))
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    rows = [inspect_file(path) for path in args.files]
    problems = []
    for row in rows:
        if not row.get("exists"):
            problems.append(f"Missing file: {row['file']}")
        if row.get("size_bytes", 0) == 0:
            problems.append(f"Empty file: {row['file']}")
        if row.get("editable_text_ok") is False:
            problems.append(f"SVG has no editable text: {row['file']}")
        if row.get("nonblank_ok") is False:
            problems.append(f"Raster appears blank: {row['file']}")

    lines = [
        "# Figure QA Report",
        "",
        f"Overall status: `{'PASS' if not problems else 'CHECK'}`",
        "",
        "## Files",
        "",
        "| File | Size | Key checks |",
        "| --- | ---: | --- |",
    ]
    for row in rows:
        checks = []
        if "svg_text_elements" in row:
            checks.append(f"text={row['svg_text_elements']}")
        if "pixel_std" in row:
            checks.append(f"pixel_std={row['pixel_std']:.2f}")
        lines.append(f"| `{row['file']}` | {row.get('size_bytes', 0)} | {', '.join(checks) or 'exists'} |")
    if problems:
        lines += ["", "## Problems", "", *[f"- {p}" for p in problems]]
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    args.out.with_suffix(".json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()

