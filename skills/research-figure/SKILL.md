---
name: research-figure
description: Use when making publication-ready scientific plots, manuscript figures, Nature/Science/Cell-style multi-panel figures, SVG/PDF/PNG/TIFF exports, figure QA, colorblind-safe palettes, or editable text checks.
---

# Research Figure

Use this skill when a figure needs to support a manuscript claim.

## Figure Contract

Before plotting, state:

1. Core claim the figure supports.
2. Evidence role of each panel.
3. Target export formats and dimensions.
4. Statistical annotations and sample-size labels.
5. Whether SVG/PDF text must stay editable.

## Workflow

```bash
python skills/research-figure/scripts/research_figure.py data.csv \
  --x flipper_length_mm --y body_mass_g --group species \
  --out-base outputs/figures/figure1

python skills/research-figure/scripts/figure_qa.py \
  outputs/figures/figure1.svg outputs/figures/figure1.png \
  --out outputs/figures/figure_qa_report.md
```

## Defaults

- `svg.fonttype = none` for editable SVG text.
- `pdf.fonttype = 42` for editable TrueType text in PDF.
- White background, colorblind-safe palette, no red/green-only encoding.
- Save SVG, PDF, PNG, and TIFF unless the user asks otherwise.

## Common Mistakes

- Do not export only raster PNG for manuscript work.
- Do not let legends, labels, or annotations overlap data.
- Do not omit source data or sample sizes when the plot summarizes groups.

