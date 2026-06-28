---
name: research-eda
description: Use when exploring scientific CSV/XLSX experiment data, checking missingness, variable types, outliers, correlations, group counts, and deciding what statistical analysis should happen next.
---

# Research EDA

Use this skill before statistical testing or figure making.

## Workflow

1. Identify the data file and create an output directory.
2. Run the bundled analyzer:
   ```bash
   python skills/research-eda/scripts/research_eda.py data.csv --out-dir outputs/eda
   ```
3. Read `eda_report.md` before choosing tests or plots.
4. Treat the report as triage, not a final statistical conclusion.

## Outputs

| File | Purpose |
| --- | --- |
| `eda_report.md` | Human-readable summary and next-step suggestions |
| `missing_values.csv` | Missingness counts and percentages |
| `numeric_summary.csv` | Numeric distribution summaries |
| `correlation_matrix.csv` | Numeric correlations when enough numeric columns exist |

## Common Mistakes

- Do not impute or drop data silently. Record what was removed and why.
- Do not run confirmatory tests from EDA alone. Use `research-statistics`.
- Do not hide missing group levels; group counts often explain later failures.

