#!/usr/bin/env python3
"""Repository smoke test for research-skills-kit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "smoke"


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], cwd=ROOT, check=True)


def make_fixture() -> Path:
    rng = np.random.default_rng(42)
    groups = np.repeat(["control", "low", "high"], 30)
    dose = np.tile(np.arange(30), 3)
    response = np.concatenate([
        rng.normal(10.0, 1.2, 30),
        rng.normal(11.5, 1.4, 30),
        rng.normal(13.2, 1.5, 30),
    ])
    biomarker = response * 2.1 + rng.normal(0, 2, 90)
    sex = np.tile(["female", "male"], 45)
    df = pd.DataFrame({
        "group": groups,
        "dose": dose,
        "response": response.round(3),
        "biomarker": biomarker.round(3),
        "sex": sex,
    })
    OUT.mkdir(parents=True, exist_ok=True)
    data = OUT / "experiment.csv"
    df.to_csv(data, index=False)
    return data


def assert_exists(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        raise AssertionError(f"Missing or empty output: {path}")


def main() -> None:
    data = make_fixture()
    py = sys.executable

    run([py, ROOT / "skills/research-eda/scripts/research_eda.py", data, "--group", "group", "--out-dir", OUT / "eda"])
    run([py, ROOT / "skills/research-statistics/scripts/research_statistics.py", data, "--dv", "response", "--group", "group", "--predictors", "biomarker,sex", "--out-dir", OUT / "statistics"])
    run([py, ROOT / "skills/research-power/scripts/research_power.py", "--test", "t_ind", "--effect-size", "0.5", "--power", "0.8", "--out-dir", OUT / "power"])
    run([py, ROOT / "skills/research-figure/scripts/research_figure.py", data, "--x", "biomarker", "--y", "response", "--group", "group", "--out-base", OUT / "figures/figure1"])
    run([py, ROOT / "skills/research-figure/scripts/figure_qa.py", OUT / "figures/figure1.svg", OUT / "figures/figure1.png", "--out", OUT / "figures/figure_qa_report.md"])

    bib = OUT / "sample.bib"
    bib.write_text(
        "@article{harris2020,\n"
        "  title={Array programming with NumPy},\n"
        "  author={Harris, Charles R.},\n"
        "  year={2020},\n"
        "  doi={10.1038/s41586-020-2649-2}\n"
        "}\n",
        encoding="utf-8",
    )
    run([py, ROOT / "skills/research-citation-check/scripts/citation_check.py", "--bibtex", bib, "--offline", "--out-dir", OUT / "citations"])
    run([py, ROOT / "skills/research-results-audit/scripts/results_audit.py", OUT / "statistics/statistical_results.md", "--hash", OUT / "statistics/group_test.csv", OUT / "figures/figure1.svg", "--out-dir", OUT / "audit"])

    expected = [
        OUT / "eda/eda_report.md",
        OUT / "statistics/statistical_results.md",
        OUT / "statistics/group_test.csv",
        OUT / "power/power_report.md",
        OUT / "power/power_curve.png",
        OUT / "figures/figure1.svg",
        OUT / "figures/figure1.pdf",
        OUT / "figures/figure1.png",
        OUT / "figures/figure1.tiff",
        OUT / "figures/figure_qa_report.md",
        OUT / "citations/citation_report.md",
        OUT / "audit/results_audit.md",
    ]
    for path in expected:
        assert_exists(path)

    svg = (OUT / "figures/figure1.svg").read_text(errors="ignore")
    if svg.count("<text") <= 0:
        raise AssertionError("SVG text was not preserved as editable text.")

    print("smoke test PASS")


if __name__ == "__main__":
    main()

