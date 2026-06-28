# Penguins Dataset EDA

Source CSV: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv

- Raw rows: 344
- Raw columns: 8
- Complete rows for main body-mass analysis: 342

## Missing Values

|                   |   missing_n |   missing_pct |
|:------------------|------------:|--------------:|
| sex               |          11 |           3.2 |
| bill_length_mm    |           2 |           0.6 |
| bill_depth_mm     |           2 |           0.6 |
| flipper_length_mm |           2 |           0.6 |
| body_mass_g       |           2 |           0.6 |
| species           |           0 |           0   |
| island            |           0 |           0   |
| year              |           0 |           0   |

## Numeric Summary

|                   |   count |    mean |    std |    min |     25% |     50% |    75% |    max |
|:------------------|--------:|--------:|-------:|-------:|--------:|--------:|-------:|-------:|
| bill_length_mm    |     342 |   43.92 |   5.46 |   32.1 |   39.22 |   44.45 |   48.5 |   59.6 |
| bill_depth_mm     |     342 |   17.15 |   1.97 |   13.1 |   15.6  |   17.3  |   18.7 |   21.5 |
| flipper_length_mm |     342 |  200.92 |  14.06 |  172   |  190    |  197    |  213   |  231   |
| body_mass_g       |     342 | 4201.75 | 801.95 | 2700   | 3550    | 4050    | 4750   | 6300   |
| year              |     344 | 2008.03 |   0.82 | 2007   | 2007    | 2008    | 2009   | 2009   |

## Species x Sex Counts

| species   | sex    |   n |
|:----------|:-------|----:|
| Adelie    | female |  73 |
| Adelie    | male   |  73 |
| Adelie    | nan    |   6 |
| Chinstrap | female |  34 |
| Chinstrap | male   |  34 |
| Gentoo    | female |  58 |
| Gentoo    | male   |  61 |
| Gentoo    | nan    |   5 |

## Correlation Matrix

|                   |   bill_length_mm |   bill_depth_mm |   flipper_length_mm |   body_mass_g |
|:------------------|-----------------:|----------------:|--------------------:|--------------:|
| bill_length_mm    |            1     |          -0.235 |               0.656 |         0.595 |
| bill_depth_mm     |           -0.235 |           1     |              -0.584 |        -0.472 |
| flipper_length_mm |            0.656 |          -0.584 |               1     |         0.871 |
| body_mass_g       |            0.595 |          -0.472 |               0.871 |         1     |

## Data-Quality Notes

- Missingness is concentrated in sex and morphometric fields; rows with missing analysis fields were removed for confirmatory tests.
- Body mass and flipper length are strongly positively correlated, so plots should show individual points rather than only means.
- Species is imbalanced but still has enough observations for a small demonstration analysis.
