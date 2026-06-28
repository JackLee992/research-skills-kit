#!/usr/bin/env python3
"""Generate a publication-oriented research figure from tabular data."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def configure_style() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": 7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.7,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })
    sns.set_theme(context="paper", style="white", font_scale=0.85)
    sns.set_palette(OKABE_ITO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create publication-ready SVG/PDF/PNG/TIFF figures.")
    parser.add_argument("data", type=Path)
    parser.add_argument("--x", required=True)
    parser.add_argument("--y", required=True)
    parser.add_argument("--group")
    parser.add_argument("--kind", choices=["auto", "scatter", "box"], default="auto")
    parser.add_argument("--out-base", type=Path, default=Path("outputs/figures/figure1"))
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    args.out_base.parent.mkdir(parents=True, exist_ok=True)
    df = load_table(args.data).dropna(subset=[args.x, args.y] + ([args.group] if args.group else []))
    configure_style()

    if args.kind == "box" or (args.kind == "auto" and args.group and not pd.api.types.is_numeric_dtype(df[args.x])):
        fig, ax = plt.subplots(figsize=(3.5, 3.0))
        sns.boxplot(data=df, x=args.x, y=args.y, hue=args.group if args.group and args.group != args.x else None, ax=ax, fliersize=0)
        sns.stripplot(data=df, x=args.x, y=args.y, ax=ax, color="0.2", alpha=0.45, size=2.5, jitter=0.2)
    elif args.group:
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), constrained_layout=True)
        ax0, ax1 = axes
        sns.boxplot(data=df, x=args.group, y=args.y, hue=args.group, ax=ax0, fliersize=0, legend=False)
        sns.stripplot(data=df, x=args.group, y=args.y, ax=ax0, color="0.2", alpha=0.4, size=2.3, jitter=0.22)
        ax0.set_xlabel(args.group)
        ax0.set_ylabel(args.y)
        ax0.set_title("Group distribution")
        sns.scatterplot(data=df, x=args.x, y=args.y, hue=args.group, ax=ax1, s=18, alpha=0.72, edgecolor="none")
        sns.regplot(data=df, x=args.x, y=args.y, ax=ax1, scatter=False, color="0.15", line_kws={"lw": 1.2})
        ax1.set_title("Relationship")
        ax = None
    else:
        fig, ax = plt.subplots(figsize=(3.5, 3.0))
        sns.regplot(data=df, x=args.x, y=args.y, ax=ax, scatter_kws={"s": 18, "alpha": 0.72, "edgecolor": "none"})

    if ax is not None:
        ax.set_title(args.title or f"{args.y} by {args.x}")
    elif args.title:
        fig.suptitle(args.title)

    saved = []
    for ext, kwargs in {
        "svg": {},
        "pdf": {},
        "png": {"dpi": 300},
        "tiff": {"dpi": 600},
    }.items():
        path = args.out_base.with_suffix(f".{ext}")
        fig.savefig(path, bbox_inches="tight", facecolor="white", **kwargs)
        saved.append(path)
    plt.close(fig)

    svg_text = args.out_base.with_suffix(".svg").read_text(errors="ignore").count("<text")
    report = [
        "# Figure Export Report",
        "",
        f"Input: `{args.data}`",
        f"Rows plotted: `{len(df)}`",
        f"SVG editable text elements: `{svg_text}`",
        "",
        "Saved files:",
        *[f"- `{p}`" for p in saved],
        "",
    ]
    args.out_base.with_name(args.out_base.name + "_export_report.md").write_text("\n".join(report), encoding="utf-8")
    print(args.out_base.with_suffix(".png"))


if __name__ == "__main__":
    main()

