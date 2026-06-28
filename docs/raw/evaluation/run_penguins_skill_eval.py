#!/usr/bin/env python3
"""Small, reproducible skill evaluation using the Palmer Penguins dataset."""

from __future__ import annotations

import json
import math
import sys
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats


BASE = Path(__file__).resolve().parent
REPOS = BASE / "repos"
INPUTS = BASE / "inputs"
OUTPUTS = BASE / "outputs"

DATA_URL = (
    "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/"
    "master/inst/extdata/penguins.csv"
)
DATA_PATH = INPUTS / "penguins.csv"

K_SKILLS = REPOS / "scientific-agent-skills" / "skills"
sys.path.insert(0, str(K_SKILLS / "statistical-analysis" / "scripts"))
sys.path.insert(0, str(K_SKILLS / "statistical-power" / "scripts"))
sys.path.insert(0, str(K_SKILLS / "scientific-visualization" / "scripts"))

from assumption_checks import check_homogeneity_of_variance, check_normality_per_group  # noqa: E402
from figure_export import check_figure_size, save_publication_figure  # noqa: E402
from power import mde, power, sample_size  # noqa: E402
from style_presets import configure_for_journal, set_color_palette  # noqa: E402


def p_fmt(p: float) -> str:
    if pd.isna(p):
        return "NA"
    if p < 0.001:
        return "< .001"
    return f"= {p:.3f}"


def get_p(row: pd.Series) -> float:
    """Return a p-value from either old or new Pingouin column naming."""
    for key in ("p-unc", "p_unc", "p-val", "pval", "p"):
        if key in row.index:
            return float(row[key])
    raise KeyError(f"No p-value column found in: {list(row.index)}")


def json_default(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def cohen_d(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().to_numpy()
    b = b.dropna().to_numpy()
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / pooled)


def download_data() -> None:
    INPUTS.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        urllib.request.urlretrieve(DATA_URL, DATA_PATH)


def write_eda_report(df: pd.DataFrame, clean: pd.DataFrame) -> None:
    missing = df.isna().sum().sort_values(ascending=False).rename("missing_n").to_frame()
    missing["missing_pct"] = (missing["missing_n"] / len(df) * 100).round(1)
    numeric_summary = df.select_dtypes(include=[np.number]).describe().T.round(2)
    group_counts = df.groupby(["species", "sex"], dropna=False).size().rename("n").reset_index()
    corr = clean[["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]].corr().round(3)

    md = [
        "# Penguins Dataset EDA",
        "",
        f"Source CSV: {DATA_URL}",
        "",
        f"- Raw rows: {len(df)}",
        f"- Raw columns: {len(df.columns)}",
        f"- Complete rows for main body-mass analysis: {len(clean)}",
        "",
        "## Missing Values",
        "",
        missing.to_markdown(),
        "",
        "## Numeric Summary",
        "",
        numeric_summary.to_markdown(),
        "",
        "## Species x Sex Counts",
        "",
        group_counts.to_markdown(index=False),
        "",
        "## Correlation Matrix",
        "",
        corr.to_markdown(),
        "",
        "## Data-Quality Notes",
        "",
        "- Missingness is concentrated in sex and morphometric fields; rows with missing analysis fields were removed for confirmatory tests.",
        "- Body mass and flipper length are strongly positively correlated, so plots should show individual points rather than only means.",
        "- Species is imbalanced but still has enough observations for a small demonstration analysis.",
        "",
    ]
    (OUTPUTS / "penguins_eda_report.md").write_text("\n".join(md), encoding="utf-8")


def run_statistics(clean: pd.DataFrame) -> dict:
    normality = check_normality_per_group(clean, "body_mass_g", "species", plot=False)
    homogeneity = check_homogeneity_of_variance(clean, "body_mass_g", "species", plot=False)
    anova = pg.anova(data=clean, dv="body_mass_g", between="species", detailed=True, effsize="np2")
    tukey = pg.pairwise_tukey(data=clean, dv="body_mass_g", between="species", effsize="cohen")
    kruskal = pg.kruskal(data=clean, dv="body_mass_g", between="species")

    reg = clean.dropna(subset=["body_mass_g", "flipper_length_mm", "species", "sex"]).copy()
    model = smf.ols("body_mass_g ~ flipper_length_mm + C(species) + C(sex)", data=reg).fit()
    coef = pd.DataFrame(
        {
            "term": model.params.index,
            "estimate": model.params.values,
            "se": model.bse.values,
            "t": model.tvalues.values,
            "p": model.pvalues.values,
        }
    ).round(4)

    groups = {name: g["body_mass_g"] for name, g in clean.groupby("species")}
    d_gentoo_adelie = cohen_d(groups["Gentoo"], groups["Adelie"])

    power_points = pd.DataFrame(
        {
            "n_per_group": list(range(10, 151, 5)),
        }
    )
    power_points["power_d_0_5"] = power_points["n_per_group"].apply(
        lambda n: power("t_ind", effect_size=0.5, nobs1=int(n), alpha=0.05)
    )

    power_summary = {
        "required_n_per_group_d_0_5_power_0_80": int(
            sample_size("t_ind", effect_size=0.5, power=0.80, alpha=0.05)
        ),
        "required_n_per_group_d_0_8_power_0_80": int(
            sample_size("t_ind", effect_size=0.8, power=0.80, alpha=0.05)
        ),
        "minimum_detectable_d_n_30_per_group_power_0_80": round(
            float(mde("t_ind", nobs1=30, power=0.80, alpha=0.05)), 3
        ),
    }

    normality.to_csv(OUTPUTS / "normality_by_species.csv", index=False)
    pd.DataFrame([homogeneity]).to_csv(OUTPUTS / "levene_body_mass_by_species.csv", index=False)
    anova.to_csv(OUTPUTS / "anova_body_mass_by_species.csv", index=False)
    tukey.to_csv(OUTPUTS / "tukey_body_mass_by_species.csv", index=False)
    kruskal.to_csv(OUTPUTS / "kruskal_body_mass_by_species.csv", index=False)
    coef.to_csv(OUTPUTS / "ols_body_mass_model_coefficients.csv", index=False)
    power_points.to_csv(OUTPUTS / "power_curve_points.csv", index=False)

    return {
        "normality": normality,
        "homogeneity": homogeneity,
        "anova": anova,
        "tukey": tukey,
        "kruskal": kruskal,
        "model": model,
        "coef": coef,
        "power_points": power_points,
        "power_summary": power_summary,
        "cohen_d_gentoo_vs_adelie": d_gentoo_adelie,
    }


def write_statistics_report(clean: pd.DataFrame, results: dict) -> None:
    anova_effect = results["anova"].loc[results["anova"]["Source"] == "species"].iloc[0]
    kruskal_row = results["kruskal"].iloc[0]
    model = results["model"]
    power_summary = results["power_summary"]

    md = [
        "# Penguins Statistical Results",
        "",
        "Main question: do penguin species differ in body mass, and is body mass associated with flipper length?",
        "",
        "## Assumption Checks",
        "",
        "### Shapiro-Wilk Normality by Species",
        "",
        results["normality"].to_markdown(index=False),
        "",
        "### Levene Homogeneity of Variance",
        "",
        pd.DataFrame([results["homogeneity"]]).to_markdown(index=False),
        "",
        "Interpretation: normality is imperfect for one group, and Levene's test suggests unequal variances. Treat the standard ANOVA as a readable baseline, and report Welch/robust or non-parametric sensitivity checks when making a manuscript claim.",
        "",
        "## ANOVA",
        "",
        results["anova"].round(4).to_markdown(index=False),
        "",
        f"APA-style result: one-way ANOVA found a species effect on body mass, F({int(anova_effect['DF'])}, {int(results['anova'].iloc[1]['DF'])}) = {anova_effect['F']:.2f}, p {p_fmt(get_p(anova_effect))}, partial eta squared = {anova_effect['np2']:.3f}.",
        "",
        "## Tukey Post-Hoc Comparisons",
        "",
        results["tukey"].round(4).to_markdown(index=False),
        "",
        "## Non-Parametric Sensitivity Check",
        "",
        results["kruskal"].round(4).to_markdown(index=False),
        "",
        f"Kruskal-Wallis sensitivity result: H({int(kruskal_row['ddof1'])}) = {kruskal_row['H']:.2f}, p {p_fmt(get_p(kruskal_row))}.",
        "",
        "## Regression Model",
        "",
        f"Model: `body_mass_g ~ flipper_length_mm + C(species) + C(sex)`, n = {int(model.nobs)}, adjusted R^2 = {model.rsquared_adj:.3f}.",
        "",
        results["coef"].to_markdown(index=False),
        "",
        "## Power Analysis",
        "",
        f"- Required n per group for d = 0.5 at 80% power, alpha = .05: {power_summary['required_n_per_group_d_0_5_power_0_80']}",
        f"- Required n per group for d = 0.8 at 80% power, alpha = .05: {power_summary['required_n_per_group_d_0_8_power_0_80']}",
        f"- Minimum detectable d with n = 30 per group at 80% power: {power_summary['minimum_detectable_d_n_30_per_group_power_0_80']}",
        "",
        "## Manuscript-Ready Result Snippet",
        "",
        "Body mass differed strongly among species in the Palmer Penguins dataset. A one-way ANOVA showed a large species effect on body mass, with non-parametric sensitivity analysis reaching the same conclusion. In a regression model that adjusted for sex and species, flipper length remained positively associated with body mass, supporting a morphology-size relationship rather than a species-only difference.",
        "",
    ]
    (OUTPUTS / "penguins_statistical_results.md").write_text("\n".join(md), encoding="utf-8")


def create_publication_figure(clean: pd.DataFrame, results: dict) -> None:
    configure_for_journal("nature", figure_width="double")
    set_color_palette("okabe_ito")
    sns.set_theme(context="paper", style="white", font_scale=0.85)
    mpl.rcParams.update({
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })

    species_order = ["Adelie", "Chinstrap", "Gentoo"]
    palette = dict(zip(species_order, ["#0072B2", "#E69F00", "#009E73"]))

    fig = plt.figure(figsize=(7.2, 5.1), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.05, 1], height_ratios=[1, 1])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    sns.boxplot(
        data=clean,
        x="species",
        y="body_mass_g",
        order=species_order,
        hue="species",
        palette=palette,
        ax=ax_a,
        width=0.5,
        fliersize=0,
        legend=False,
    )
    sns.stripplot(
        data=clean,
        x="species",
        y="body_mass_g",
        order=species_order,
        ax=ax_a,
        color="0.15",
        alpha=0.45,
        size=2.6,
        jitter=0.22,
    )
    ax_a.set_xlabel("")
    ax_a.set_ylabel("Body mass (g)")
    ax_a.set_title("Species body-mass distributions")

    for species in species_order:
        sub = clean[clean["species"] == species]
        sns.regplot(
            data=sub,
            x="flipper_length_mm",
            y="body_mass_g",
            ax=ax_b,
            scatter_kws={"s": 15, "alpha": 0.55, "color": palette[species], "edgecolor": "none"},
            line_kws={"lw": 1.3, "color": palette[species]},
            ci=95,
            label=species,
        )
    ax_b.set_xlabel("Flipper length (mm)")
    ax_b.set_ylabel("Body mass (g)")
    ax_b.set_title("Body mass scales with flipper length")
    ax_b.legend(title="", frameon=False, fontsize=6)

    means = clean.groupby("species", observed=False)["body_mass_g"].agg(["mean", "sem", "count"]).reindex(species_order)
    ci95 = 1.96 * means["sem"]
    ax_c.errorbar(
        x=np.arange(len(means)),
        y=means["mean"],
        yerr=ci95,
        fmt="o",
        color="black",
        ecolor="black",
        elinewidth=1,
        capsize=3,
        markersize=4,
    )
    ax_c.set_xticks(np.arange(len(means)))
    ax_c.set_xticklabels(species_order)
    ax_c.set_ylabel("Mean body mass (g)")
    ax_c.set_title("Mean +/- 95% CI")
    for idx, (_, row) in enumerate(means.iterrows()):
        ax_c.text(idx, row["mean"] + ci95.iloc[idx] + 90, f"n={int(row['count'])}", ha="center", va="bottom", fontsize=6)

    power_points = results["power_points"]
    ax_d.plot(power_points["n_per_group"], power_points["power_d_0_5"], color="#0072B2", lw=1.8)
    ax_d.axhline(0.80, color="#D55E00", lw=1, ls="--")
    ax_d.axvline(results["power_summary"]["required_n_per_group_d_0_5_power_0_80"], color="0.35", lw=0.9, ls=":")
    ax_d.set_xlabel("n per group")
    ax_d.set_ylabel("Power")
    ax_d.set_ylim(0, 1.02)
    ax_d.set_title("Planning curve for d = 0.5")
    ax_d.text(0.98, 0.08, "alpha = .05", transform=ax_d.transAxes, ha="right", va="bottom", fontsize=6)

    for label, ax in zip(["a", "b", "c", "d"], [ax_a, ax_b, ax_c, ax_d]):
        ax.text(-0.12, 1.08, label, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top", ha="left")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    base = OUTPUTS / "penguins_nature_figure"
    saved = save_publication_figure(fig, base, formats=["svg", "pdf", "png", "tiff"], dpi=600)
    size_check = check_figure_size(fig, journal="nature")
    plt.close(fig)
    svg_text_count = (OUTPUTS / "penguins_nature_figure.svg").read_text(errors="ignore").count("<text")

    legend = [
        "# Figure Legend",
        "",
        "Fig. 1 | Species-level body mass differences and planning implications in Palmer Penguins.",
        "",
        "a, Body mass distributions by species; boxes show the interquartile range and overlaid points show individual penguins. b, Relationship between flipper length and body mass with species-specific linear fits and 95% confidence bands. c, Species means with 95% confidence intervals and sample sizes. d, Two-sided independent-samples power curve for a standardized mean difference of d = 0.5 at alpha = .05.",
        "",
        f"Nature width compliance check: {json.dumps(size_check, indent=2, default=json_default)}",
        "",
        f"SVG editability check: `{svg_text_count}` `<text>` elements detected after setting `svg.fonttype = none`.",
        "",
        "Saved files:",
        *[f"- {path}" for path in saved],
        "",
    ]
    (OUTPUTS / "penguins_figure_legend.md").write_text("\n".join(legend), encoding="utf-8")


def main() -> None:
    download_data()
    df = pd.read_csv(DATA_PATH)
    clean = df.dropna(subset=["species", "body_mass_g", "flipper_length_mm"]).copy()

    write_eda_report(df, clean)
    results = run_statistics(clean)
    write_statistics_report(clean, results)
    create_publication_figure(clean, results)

    summary = {
        "dataset_url": DATA_URL,
        "raw_rows": int(len(df)),
        "analysis_rows": int(len(clean)),
        "outputs": sorted(str(path.relative_to(BASE)) for path in OUTPUTS.glob("*")),
    }
    (OUTPUTS / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
