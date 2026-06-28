---
name: research-results-audit
description: Use when auditing statistical result reports, checking p-value wording, effect-size reporting, causal language, multiple comparisons, assumption caveats, reproducibility hashes, or manuscript Results claims.
---

# Research Results Audit

Use this skill after analysis and before drafting final Results or Discussion text.

## Workflow

```bash
python skills/research-results-audit/scripts/results_audit.py \
  outputs/statistics/statistical_results.md \
  --hash outputs/statistics/anova.csv outputs/figures/figure1.svg \
  --out-dir outputs/audit
```

## Checks

- p-values reported without effect sizes.
- Significant/non-significant wording problems.
- Causal verbs in observational analyses.
- Missing assumption caveats.
- Missing reproducibility hash evidence.
- Multiple comparison warnings.

## Output

`results_audit.md` should become the final pre-writing checkpoint. Fix severe warnings before using the result text in a paper.

