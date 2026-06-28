#!/usr/bin/env python3
"""First-pass EDA for small to medium scientific tabular datasets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an EDA report for tabular research data.")
    parser.add_argument("data", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/eda"))
    parser.add_argument("--group", help="Optional grouping column to summarize.")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = load_table(args.data)

    missing = pd.DataFrame({
        "column": df.columns,
        "missing_n": df.isna().sum().values,
        "missing_pct": (df.isna().mean().values * 100).round(2),
        "dtype": [str(df[col].dtype) for col in df.columns],
        "unique_n": [df[col].nunique(dropna=True) for col in df.columns],
    }).sort_values(["missing_n", "column"], ascending=[False, True])
    missing.to_csv(args.out_dir / "missing_values.csv", index=False)

    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        numeric_summary = numeric.describe().T
        numeric_summary["missing_n"] = numeric.isna().sum()
        numeric_summary["skew"] = numeric.skew(numeric_only=True)
        numeric_summary["kurtosis"] = numeric.kurt(numeric_only=True)
        numeric_summary.round(4).to_csv(args.out_dir / "numeric_summary.csv")
    else:
        numeric_summary = pd.DataFrame()

    if numeric.shape[1] >= 2:
        corr = numeric.corr(numeric_only=True).round(4)
        corr.to_csv(args.out_dir / "correlation_matrix.csv")
    else:
        corr = pd.DataFrame()

    categorical_cols = [c for c in df.columns if c not in numeric.columns]
    group_col = args.group if args.group in df.columns else None
    if group_col:
        group_counts = df.groupby(group_col, dropna=False).size().rename("n").reset_index()
        group_counts.to_csv(args.out_dir / "group_counts.csv", index=False)
    else:
        group_counts = pd.DataFrame()

    candidate_dv = numeric.columns.tolist()
    candidate_groups = [c for c in categorical_cols if 2 <= df[c].nunique(dropna=True) <= 12]
    suggestions = []
    if candidate_dv and candidate_groups:
        suggestions.append(
            f"Candidate group comparison: use research-statistics with --dv {candidate_dv[0]} --group {candidate_groups[0]}."
        )
    if len(candidate_dv) >= 2:
        suggestions.append(
            f"Candidate relationship plot/regression: use research-figure with --x {candidate_dv[0]} --y {candidate_dv[1]}."
        )
    if not suggestions:
        suggestions.append("No obvious numeric/group structure detected; inspect the source data manually.")

    summary = {
        "data": str(args.data),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "numeric_columns": candidate_dv,
        "categorical_columns": categorical_cols,
        "candidate_group_columns": candidate_groups,
        "outputs": sorted(p.name for p in args.out_dir.iterdir() if p.is_file()),
    }
    (args.out_dir / "eda_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# EDA Report",
        "",
        f"Input: `{args.data}`",
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        "",
        "## Missingness",
        "",
        missing.to_markdown(index=False),
        "",
    ]
    if not numeric_summary.empty:
        lines += ["## Numeric Summary", "", numeric_summary.round(3).to_markdown(), ""]
    if not corr.empty:
        lines += ["## Correlation Matrix", "", corr.to_markdown(), ""]
    if not group_counts.empty:
        lines += [f"## Group Counts: {group_col}", "", group_counts.to_markdown(index=False), ""]
    lines += ["## Suggested Next Steps", "", *[f"- {item}" for item in suggestions], ""]
    (args.out_dir / "eda_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(args.out_dir / "eda_report.md")


if __name__ == "__main__":
    main()

