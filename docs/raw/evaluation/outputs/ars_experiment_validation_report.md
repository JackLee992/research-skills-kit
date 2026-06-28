## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-06-28
- Verification Status: VERIFIED
- Version Label: validation_v1

## Validation Report

- **Source**: local rerunnable analysis of Palmer Penguins public dataset
- **Overall Confidence**: CAUTION
- **Reason**: primary statistical pattern is strong and reproducible, but the dataset is observational and Levene's test indicates unequal group variances; manuscript claims should remain associational and include robust/non-parametric sensitivity checks.

### Statistical Findings

| Metric | Test | Value | Effect Size | Confidence |
| --- | --- | --- | --- | --- |
| Body mass differs by species | One-way ANOVA | F(2, 339) = 343.63, p < .001 | partial eta squared = 0.670, large | SOLID with variance caveat |
| Body mass differs by species | Kruskal-Wallis sensitivity | H(2) = 217.60, p < .001 | non-parametric confirmation | SOLID |
| Adelie vs Chinstrap | Tukey HSD | p = .881 | Cohen's d = -0.074, negligible | SOLID null-like comparison |
| Adelie vs Gentoo | Tukey HSD | p < .001 | Cohen's d = -2.868, very large | SOLID |
| Chinstrap vs Gentoo | Tukey HSD | p < .001 | Cohen's d = -2.887, very large | SOLID |
| Body mass model | OLS adjusted for species and sex | adjusted R^2 = .865 | flipper length B = 20.025 g/mm, p < .001 | CAUTION because residual diagnostics not fully audited |
| Study planning | Two-sample t-test power | d = 0.5 needs n = 64/group for 80% power | medium effect planning curve | SOLID for planning illustration |

### Warnings

| Type | Detail | Affected |
| --- | --- | --- |
| Assumption | Adelie normality check p = .032; Levene p = .006 suggests unequal variances. | Species ANOVA |
| Causal language | Dataset is observational; do not write that species or flipper length "causes" body mass. | Results/discussion wording |
| Multiple comparisons | Three Tukey post-hoc tests were run; Tukey correction is appropriate for the pairwise family. | Pairwise comparisons |
| Model diagnostics | OLS coefficients are useful, but residual plots and influence checks were not included in this mini-test. | Regression interpretation |

### Fallacy Scan

- **Coverage**: 11/11 fallacy types checked

| Fallacy | Severity | Detail | Recommendation |
| --- | --- | --- | --- |
| Simpson's paradox | NOTE | Species and sex are grouping variables; the current report does not claim an aggregate relationship without subgroup context. | Keep species/sex adjustment in model reporting. |
| Ecological fallacy | NOTE | Analysis is individual penguin level; no group-level inference to individuals was made. | Maintain individual-level wording. |
| Berkson's paradox | NOTE | Sample is a field dataset, not a filtered clinical/admission sample. | Mention dataset scope if used in a manuscript. |
| Collider bias | CAUTION | Sex/species adjustment is sensible, but model structure was not designed from a causal DAG. | Avoid causal interpretation. |
| Base rate neglect | NOTE | No diagnostic sensitivity/specificity or prevalence claim. | N/A |
| Regression to the mean | NOTE | No pre/post extreme-group design. | N/A |
| Survivorship bias | NOTE | Missing sex values exist, but primary body-mass analysis excludes only two rows with missing morphometrics. | Report missingness. |
| Look-elsewhere effect | NOTE | Tests were pre-specified for this evaluation; no cherry-picked significant endpoint was needed. | Keep analysis question explicit. |
| Garden of forking paths | CAUTION | This is exploratory and not preregistered. | Label as demonstration or exploratory analysis. |
| Correlation != causation | CAUTION | Flipper length/body mass relationship is associational. | Use "associated with" / "scales with", not causal verbs. |
| Reverse causality | NOTE | No directional causal claim was made. | Keep causal neutrality. |

### Reproducibility

- **Method**: deterministic re-run of the local analysis script, comparing SHA-256 hashes of key output files
- **Verdict**: REPRODUCIBLE

| Metric/File | Original | Re-run | Diff | Status |
| --- | --- | --- | --- | --- |
| `anova_body_mass_by_species.csv` | `392e7315caba606f20d9c805babf9c382af8e57226adc41809ccc634d2dec58a` | same | 0 | MATCH |
| `tukey_body_mass_by_species.csv` | `cb32e3ae67dae2e1e0624ec042ab68bc8c034d896cd878317347f2b0a7bf153c` | same | 0 | MATCH |
| `ols_body_mass_model_coefficients.csv` | `490a374183fbfa3c73eb0f5b18dd7a05706a6ad4a03bbae53c8ad03acc917982` | same | 0 | MATCH |
| `power_curve_points.csv` | `0063e2198a7b23bec6d435f55fc8e1fc794594473cdf85af2c36e035d81517c9` | same | 0 | MATCH |
| `penguins_statistical_results.md` | `41796e7b0a41e338d45fef83f445fb80c56f69290f2273693fe2a6e23ea5f072` | same | 0 | MATCH |
