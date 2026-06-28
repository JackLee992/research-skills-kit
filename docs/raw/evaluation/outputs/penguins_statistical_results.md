# Penguins Statistical Results

Main question: do penguin species differ in body mass, and is body mass associated with flipper length?

## Assumption Checks

### Shapiro-Wilk Normality by Species

| Group     |   N |        W |   p-value | Normal   |
|:----------|----:|---------:|----------:|:---------|
| Adelie    | 151 | 0.980708 |  0.032397 | No       |
| Gentoo    | 123 | 0.985928 |  0.233616 | Yes      |
| Chinstrap |  68 | 0.984494 |  0.560508 | Yes      |

### Levene Homogeneity of Variance

| test   |   statistic |    p_value | is_homogeneous   |   variance_ratio | interpretation                                                                    | recommendation                                |
|:-------|------------:|-----------:|:-----------------|-----------------:|:----------------------------------------------------------------------------------|:----------------------------------------------|
| Levene |     5.12025 | 0.00644508 | False            |          1.72045 | Variances do not appear homogeneous (F = 5.120, p = 0.006, variance ratio = 1.72) | Consider Welch's correction or transformation |

Interpretation: normality is imperfect for one group, and Levene's test suggests unequal variances. Treat the standard ANOVA as a readable baseline, and report Welch/robust or non-parametric sensitivity checks when making a manuscript claim.

## ANOVA

| Source   |          SS |   DF |               MS |       F |   p_unc |      np2 |
|:---------|------------:|-----:|-----------------:|--------:|--------:|---------:|
| species  | 1.46864e+08 |    2 |      7.34321e+07 | 343.626 |       0 |   0.6697 |
| Within   | 7.24435e+07 |  339 | 213698           | nan     |     nan | nan      |

APA-style result: one-way ANOVA found a species effect on body mass, F(2, 339) = 343.63, p < .001, partial eta squared = 0.670.

## Tukey Post-Hoc Comparisons

| A         | B         |   mean_A |   mean_B |      diff |      se |        T |   p_tukey |   cohen |
|:----------|:----------|---------:|---------:|----------:|--------:|---------:|----------:|--------:|
| Adelie    | Chinstrap |  3700.66 |  3733.09 |   -32.426 | 67.5117 |  -0.4803 |    0.8807 | -0.0742 |
| Adelie    | Gentoo    |  3700.66 |  5076.02 | -1375.35  | 56.148  | -24.4952 |    0      | -2.8681 |
| Chinstrap | Gentoo    |  3733.09 |  5076.02 | -1342.93  | 69.8569 | -19.224  |    0      | -2.8868 |

## Non-Parametric Sensitivity Check

| Source   |   ddof1 |       H |   p_unc |
|:---------|--------:|--------:|--------:|
| species  |       2 | 217.599 |       0 |

Kruskal-Wallis sensitivity result: H(2) = 217.60, p < .001.

## Regression Model

Model: `body_mass_g ~ flipper_length_mm + C(species) + C(sex)`, n = 333, adjusted R^2 = 0.865.

| term                    |   estimate |       se |       t |      p |
|:------------------------|-----------:|---------:|--------:|-------:|
| Intercept               |  -365.817  | 532.05   | -0.6876 | 0.4922 |
| C(species)[T.Chinstrap] |   -87.6345 |  46.3473 | -1.8908 | 0.0595 |
| C(species)[T.Gentoo]    |   836.26   |  85.1854 |  9.8169 | 0      |
| C(sex)[T.male]          |   530.381  |  37.8101 | 14.0275 | 0      |
| flipper_length_mm       |    20.0249 |   2.8458 |  7.0367 | 0      |

## Power Analysis

- Required n per group for d = 0.5 at 80% power, alpha = .05: 64
- Required n per group for d = 0.8 at 80% power, alpha = .05: 26
- Minimum detectable d with n = 30 per group at 80% power: 0.736

## Manuscript-Ready Result Snippet

Body mass differed strongly among species in the Palmer Penguins dataset. A one-way ANOVA showed a large species effect on body mass, with non-parametric sensitivity analysis reaching the same conclusion. In a regression model that adjusted for sex and species, flipper length remained positively associated with body mass, supporting a morphology-size relationship rather than a species-only difference.
