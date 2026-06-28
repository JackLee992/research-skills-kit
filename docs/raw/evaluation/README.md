# 实测评估原始材料索引

本目录保存 2026-06-28 科研 skills 实测用到的输入、脚本和主要输出。

## 输入

| 文件 | 说明 |
| --- | --- |
| `inputs/penguins.csv` | Palmer Penguins 公开数据，344 行、8 列。 |

数据来源：

`https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv`

## 脚本

| 文件 | 说明 |
| --- | --- |
| `run_penguins_skill_eval.py` | 原始评测脚本，用 Penguins 数据串起 EDA、统计、power、作图和审计流程。 |

## 输出

| 文件 | 说明 |
| --- | --- |
| `outputs/run_summary.json` | 本次评测的输入规模和输出清单。 |
| `outputs/penguins_eda_report.md` | 手写 EDA 报告。 |
| `outputs/kdense_eda_analyzer_penguins.md` | K-Dense EDA analyzer 风格输出。 |
| `outputs/penguins_statistical_results.md` | 统计结果报告。 |
| `outputs/ars_experiment_validation_report.md` | ARS validate 风格结果审计。 |
| `outputs/anova_body_mass_by_species.csv` | ANOVA 结果。 |
| `outputs/kruskal_body_mass_by_species.csv` | Kruskal-Wallis 敏感性分析结果。 |
| `outputs/levene_body_mass_by_species.csv` | Levene 方差齐性检查。 |
| `outputs/normality_by_species.csv` | 分组 Shapiro-Wilk 正态性检查。 |
| `outputs/ols_body_mass_model_coefficients.csv` | OLS 回归系数。 |
| `outputs/tukey_body_mass_by_species.csv` | Tukey 事后比较。 |
| `outputs/power_curve_points.csv` | 功效曲线数据点。 |
| `outputs/penguins_figure_legend.md` | 图注。 |
| `outputs/penguins_nature_figure.svg` | 可编辑 SVG 论文图。 |
| `outputs/penguins_nature_figure.pdf` | PDF 论文图。 |
| `outputs/penguins_nature_figure.png` | PNG 论文图。 |
| `outputs/citation_online_report.md` | DOI 在线校验报告，验证 `10.1038/s41586-020-2649-2`。 |
| `outputs/citation_online_report.json` | DOI 在线校验结构化结果。 |
| `outputs/citation_online_references.bib` | DOI 在线校验导出的 BibTeX。 |

## 未提交的大文件

`penguins_nature_figure.tiff` 为 600 dpi TIFF，约 53 MB。它没有提交到仓库，原因是体积偏大且可由 `run_penguins_skill_eval.py` 复现。
