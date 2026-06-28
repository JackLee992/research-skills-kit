#!/usr/bin/env python3
"""Assumption-aware statistical summaries for research datasets."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def p_text(p: float) -> str:
    if pd.isna(p):
        return "NA"
    if p < 0.001:
        return "< .001"
    return f"= {p:.3f}"


def cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    a = a[~np.isnan(a)]
    b = b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / pooled) if pooled else float("nan")


def eta_squared(groups: list[np.ndarray]) -> float:
    clean = [g[~np.isnan(g)] for g in groups]
    all_values = np.concatenate(clean)
    grand = all_values.mean()
    ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in clean)
    ss_total = sum((x - grand) ** 2 for x in all_values)
    return float(ss_between / ss_total) if ss_total else float("nan")


def normality_by_group(df: pd.DataFrame, dv: str, group: str) -> pd.DataFrame:
    rows = []
    for name, sub in df.groupby(group, dropna=False):
        values = sub[dv].dropna().to_numpy()
        if 3 <= len(values) <= 5000:
            w, p = stats.shapiro(values)
            normal = bool(p > 0.05)
        else:
            w, p, normal = np.nan, np.nan, None
        rows.append({"group": name, "n": len(values), "shapiro_w": w, "p": p, "normal": normal})
    return pd.DataFrame(rows)


def group_analysis(df: pd.DataFrame, dv: str, group: str, out_dir: Path) -> list[str]:
    data = df[[dv, group]].dropna()
    groups = [sub[dv].to_numpy(dtype=float) for _, sub in data.groupby(group)]
    group_names = [str(name) for name, _ in data.groupby(group)]
    lines = ["## Group Comparison", "", f"Dependent variable: `{dv}`", f"Group: `{group}`", ""]

    normality = normality_by_group(data, dv, group)
    normality.to_csv(out_dir / "normality_by_group.csv", index=False)
    lines += ["### Normality", "", normality.round(4).to_markdown(index=False), ""]

    lev_stat, lev_p = stats.levene(*groups) if len(groups) >= 2 else (np.nan, np.nan)
    levene = pd.DataFrame([{"statistic": lev_stat, "p": lev_p, "equal_variance": bool(lev_p > 0.05) if not pd.isna(lev_p) else None}])
    levene.to_csv(out_dir / "levene.csv", index=False)
    lines += ["### Variance Homogeneity", "", levene.round(4).to_markdown(index=False), ""]

    if len(groups) == 2:
        equal_var = bool(lev_p > 0.05) if not pd.isna(lev_p) else False
        t_stat, t_p = stats.ttest_ind(groups[0], groups[1], equal_var=equal_var, nan_policy="omit")
        u_stat, u_p = stats.mannwhitneyu(groups[0], groups[1], alternative="two-sided")
        d = cohen_d(groups[0], groups[1])
        result = pd.DataFrame([{
            "test": "student_t" if equal_var else "welch_t",
            "group_a": group_names[0],
            "group_b": group_names[1],
            "t": t_stat,
            "p": t_p,
            "cohen_d": d,
            "sensitivity_test": "mann_whitney_u",
            "u": u_stat,
            "u_p": u_p,
        }])
        result.to_csv(out_dir / "group_test.csv", index=False)
        lines += ["### Test Result", "", result.round(4).to_markdown(index=False), ""]
        lines += [
            "### Manuscript Snippet",
            "",
            f"A {'Welch ' if not equal_var else ''}independent-samples t-test compared `{dv}` between `{group_names[0]}` and `{group_names[1]}` "
            f"(t = {t_stat:.2f}, p {p_text(t_p)}, Cohen's d = {d:.2f}). "
            f"A Mann-Whitney sensitivity test gave p {p_text(u_p)}.",
            "",
        ]
    elif len(groups) > 2:
        f_stat, f_p = stats.f_oneway(*groups)
        h_stat, h_p = stats.kruskal(*groups)
        eta2 = eta_squared(groups)
        result = pd.DataFrame([{
            "test": "one_way_anova",
            "df_between": len(groups) - 1,
            "df_within": len(data) - len(groups),
            "f": f_stat,
            "p": f_p,
            "eta_squared": eta2,
            "sensitivity_test": "kruskal_wallis",
            "h": h_stat,
            "h_p": h_p,
        }])
        result.to_csv(out_dir / "group_test.csv", index=False)
        lines += ["### Test Result", "", result.round(4).to_markdown(index=False), ""]
        caveat = "Levene's test suggests unequal variances; report Welch/Games-Howell if this is confirmatory. " if lev_p <= 0.05 else ""
        lines += [
            "### Manuscript Snippet",
            "",
            f"A one-way ANOVA found a group effect on `{dv}`, F({len(groups)-1}, {len(data)-len(groups)}) = {f_stat:.2f}, "
            f"p {p_text(f_p)}, eta squared = {eta2:.3f}. {caveat}"
            f"A Kruskal-Wallis sensitivity test gave H = {h_stat:.2f}, p {p_text(h_p)}.",
            "",
        ]
    return lines


def regression_analysis(df: pd.DataFrame, dv: str, predictors: list[str], out_dir: Path) -> list[str]:
    if not predictors:
        return []
    cols = [dv] + predictors
    data = df[cols].dropna().copy()
    terms = []
    for col in predictors:
        if pd.api.types.is_numeric_dtype(data[col]):
            terms.append(f"`{col}`".replace("`", ""))
        else:
            terms.append(f"C({col})")
    formula = f"{dv} ~ " + " + ".join(terms)
    model = smf.ols(formula, data=data).fit()
    coef = pd.DataFrame({
        "term": model.params.index,
        "estimate": model.params.values,
        "se": model.bse.values,
        "t": model.tvalues.values,
        "p": model.pvalues.values,
    })
    coef.to_csv(out_dir / "ols_coefficients.csv", index=False)
    return [
        "## Regression",
        "",
        f"Formula: `{formula}`",
        f"n = {int(model.nobs)}, adjusted R^2 = {model.rsquared_adj:.3f}",
        "",
        coef.round(4).to_markdown(index=False),
        "",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run assumption-aware statistical analysis.")
    parser.add_argument("data", type=Path)
    parser.add_argument("--dv", required=True, help="Dependent variable.")
    parser.add_argument("--group", help="Grouping variable for comparisons.")
    parser.add_argument("--predictors", help="Comma-separated OLS predictors.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/statistics"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = load_table(args.data)
    predictors = [p.strip() for p in (args.predictors or "").split(",") if p.strip()]

    lines = ["# Statistical Results", "", f"Input: `{args.data}`", ""]
    if args.group:
        lines += group_analysis(df, args.dv, args.group, args.out_dir)
    if predictors:
        lines += regression_analysis(df, args.dv, predictors, args.out_dir)
    (args.out_dir / "statistical_results.md").write_text("\n".join(lines), encoding="utf-8")
    print(args.out_dir / "statistical_results.md")


if __name__ == "__main__":
    main()

