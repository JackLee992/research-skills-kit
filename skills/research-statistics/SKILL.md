---
name: research-statistics
description: Use when analyzing experimental data with group comparisons, t-tests, ANOVA, Welch checks, non-parametric sensitivity tests, regression, effect sizes, assumption checks, or manuscript-ready statistical result text.
---

# Research Statistics

Use this skill after EDA and before writing Results text.

## Workflow

1. Choose a dependent variable with `--dv`.
2. Add `--group` for group comparisons.
3. Add `--predictors` for an optional OLS model.
4. Run:
   ```bash
   python skills/research-statistics/scripts/research_statistics.py data.csv \
     --dv body_mass_g --group species --predictors flipper_length_mm,sex \
     --out-dir outputs/statistics
   ```
5. Use `statistical_results.md` and CSV outputs as the source of truth.

## Behavior

- Checks Shapiro-Wilk normality per group when sample sizes permit.
- Checks Levene variance homogeneity.
- Uses Welch-style interpretation when variances are unequal.
- Adds Mann-Whitney or Kruskal-Wallis sensitivity tests.
- Reports effect sizes where possible.

## Common Mistakes

- Do not report p-values without effect sizes.
- Do not call observational associations causal.
- If Levene fails, do not rely on ordinary ANOVA alone.

