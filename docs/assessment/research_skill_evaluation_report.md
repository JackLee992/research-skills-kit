# 科研 Skills 实测评估报告

评测时间：2026-06-28
评测目录：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation`
测试输入：Palmer Penguins 公开实验观测数据，344 行、8 列。
数据来源：https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv

## 结论先行

这次实测后，真正适合“研究 / 写论文 / 实验数据分析 / 作图”日常高频使用的，不是整个仓库全装，而是少数几个清晰、可复现、能落地产物的 skill。

| 等级 | Skill / 仓库 | 结论 | 推荐用途 |
| --- | --- | --- | --- |
| 高可用 | K-Dense `statistical-analysis` + `statistical-power` + `scientific-visualization` | 有可运行脚本，能接真实 CSV 数据，能产出统计表、power curve、论文图 | 实验数据分析、统计汇报、样本量估算、论文配图 |
| 高可用 | K-Dense `exploratory-data-analysis` | 自带 EDA analyzer 可直接跑 CSV，输出基础质量报告 | 数据到手后的第一轮体检 |
| 高可用 | `nature-figure` | Figure contract 很实用，强制作图前先定义结论、证据链、导出规格 | 论文图、SCI/Nature 风格多面板图 |
| 高可用 | ARS `experiment-agent` validate | 适合审查统计结果、假设、复现性和常见统计谬误 | 写论文前的结果审计 |
| 条件可用 | `image-to-editable-ppt` | CLI 可安装，doctor/prepare 通过；完整转换依赖 OCR/图像后端，工作流重 | 图片/扫描版 PPT 转可编辑 PPT |
| 条件可用 | Academic Research Suite `academic-paper` | 体系完整，但适合长周期论文项目，不适合快速写一个结果段 | 全论文规划、审稿意见、引用检查 |
| 条件偏低 | PaperSpine | 思路严谨，但当前 Codex 路径强依赖交互 UI/PowerShell/权限策略 | 需要改造后再长期使用 |
| 低优先级 | inbharatai `latex-writer` | 内容过泛，没有足够科研写作操作细节 | 不建议作为核心 skill |
| 低优先级 | `caveman-claude-skill` | 压缩表达有用，但不是科研生产 skill | 长对话省 token 的辅助模式 |

## 实测输入与环境

### 数据与问题

使用 Palmer Penguins 数据模拟常见科研流程：

- EDA：检查缺失值、变量类型、数值分布、相关性。
- 统计分析：比较不同企鹅物种的体重差异。
- 假设检查：Shapiro-Wilk 正态性、Levene 方差齐性。
- 敏感性分析：Kruskal-Wallis 非参数检验。
- 回归：体重与鳍长、物种、性别的关系。
- Power：计算中等效应 `d = 0.5` 下 80% power 需要的样本量。
- 作图：导出 Nature double-column 多面板图，含 SVG/PDF/PNG/TIFF。

### Python 环境

- Python 3.11
- pandas 3.0.3
- numpy 2.4.6
- scipy 1.17.1
- statsmodels 0.14.6
- matplotlib 3.11.0
- seaborn 0.13.2
- pingouin 0.6.1

### 仓库快照

| 仓库 | Commit |
| --- | --- |
| https://github.com/K-Dense-AI/scientific-agent-skills | `9c9bd2e` |
| https://github.com/Yuan1z0825/nature-skills | `6edea02` |
| https://github.com/Imbad0202/academic-research-skills-codex | `36cc610` |
| https://github.com/WUBING2023/PaperSpine | `a7fe540` |
| https://github.com/ningzimu/image-to-editable-ppt-skill | `698b16f` |

## 关键产物

| 产物 | 路径 |
| --- | --- |
| 可复现实验脚本 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/run_penguins_skill_eval.py` |
| 手写 EDA 报告 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_eda_report.md` |
| K-Dense EDA analyzer 原生报告 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/kdense_eda_analyzer_penguins.md` |
| 统计结果报告 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_statistical_results.md` |
| ARS validate 风格审计报告 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/ars_experiment_validation_report.md` |
| Nature 风格论文图 PNG | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_nature_figure.png` |
| Nature 风格论文图 SVG | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_nature_figure.svg` |
| Nature 风格论文图 PDF | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_nature_figure.pdf` |
| Nature 风格论文图 TIFF | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_nature_figure.tiff` |
| 图注 | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/penguins_figure_legend.md` |
| Image-to-PPT prepare run | `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/outputs/editppt_runs/20260628-204240-penguins_nature_figure` |

## 实测结果摘要

### 1. K-Dense 统计与作图技能

实测命中的 skill：

- `scientific-agent-skills/skills/statistical-analysis`
- `scientific-agent-skills/skills/statistical-power`
- `scientific-agent-skills/skills/scientific-visualization`
- `scientific-agent-skills/skills/exploratory-data-analysis`

跑通内容：

- `assumption_checks.py` 可导入并跑 Shapiro-Wilk / Levene。
- `power.py` 可计算 sample size、MDE 和 power curve。
- `style_presets.py` / `figure_export.py` 可生成 journal style、导出多格式论文图。
- `eda_analyzer.py` 可直接分析 CSV 并生成 Markdown 报告。

主要统计结果：

- 物种对体重有显著影响：`F(2, 339) = 343.63, p < .001, partial eta squared = 0.670`。
- Kruskal-Wallis 敏感性分析同样显著：`H(2) = 217.60, p < .001`。
- `d = 0.5`、双侧 `alpha = .05`、80% power 需要 `n = 64/group`。
- 回归模型 `body_mass_g ~ flipper_length_mm + species + sex` 调整后 `R^2 = .865`。

实测发现的问题：

- `pingouin` 新版本列名为 `p_unc`，而一些旧示例常写 `p-unc`；脚本中要做兼容。
- `figure_export.check_figure_size()` 返回的结果含 NumPy 标量，直接 `json.dumps` 会报错；需要 default converter。
- EDA analyzer 是好用的“第一轮体检”，但不会自动给出深入研究解释，仍需后续统计分析。

评分：9/10。
推荐安装，但不要全仓库无脑使用；优先挑统计、power、EDA、visualization、citation-management、scientific-writing 这类高频目录。

### 2. Nature Figure

实测命中的 skill：

- `nature-skills/skills/nature-figure`

关键价值：

- 强制先写 figure contract：核心结论、证据链、图类型、后端、导出规格。
- 对 Python/R 后端有严格 gate，避免混用导致图形不可复现。
- 对 Nature/high-impact journal 图的尺寸、可编辑文字、source data、统计标注有明确提醒。

本次输出：

- 多面板 figure：箱线图 + 散点回归 + 均值 CI + power curve。
- 导出 `SVG/PDF/PNG/TIFF`。
- 尺寸检查：Nature double column `182.9 mm x 129.3 mm`，通过。
- 可编辑性检查：第一次导出的 SVG 文字被转成路径；按 `nature-figure` 的 Python fragment 补上 `svg.fonttype = none` 和 `pdf.fonttype = 42` 后，SVG 中保留 `70` 个 `<text>` 元素。

评分：8.5/10。
它本身不是自动画图脚本，而是高质量作图流程约束。和 K-Dense 的绘图脚本组合使用最强。

### 3. Academic Research Suite / Experiment Agent

实测命中的 workflow：

- `academic-research-suite/ars/experiment-agent/WORKFLOW.md`

本次按 validate 模式生成：

- `Material Passport`
- 统计发现表
- warnings
- 11 类统计/方法谬误扫描
- 复现性检查

复现性检查：

同一脚本重跑后，关键结果文件 SHA-256 完全一致：

| 文件 | Hash |
| --- | --- |
| `anova_body_mass_by_species.csv` | `392e7315caba606f20d9c805babf9c382af8e57226adc41809ccc634d2dec58a` |
| `tukey_body_mass_by_species.csv` | `cb32e3ae67dae2e1e0624ec042ab68bc8c034d896cd878317347f2b0a7bf153c` |
| `ols_body_mass_model_coefficients.csv` | `490a374183fbfa3c73eb0f5b18dd7a05706a6ad4a03bbae53c8ad03acc917982` |
| `power_curve_points.csv` | `0063e2198a7b23bec6d435f55fc8e1fc794594473cdf85af2c36e035d81517c9` |
| `penguins_statistical_results.md` | `41796e7b0a41e338d45fef83f445fb80c56f69290f2273693fe2a6e23ea5f072` |

评分：8/10。
适合做论文前的“结果审计员”，尤其能提醒不要把相关写成因果。完整 `academic-paper` pipeline 很重，适合长周期论文项目。

### 4. Image to Editable PPT

实测命中的 skill：

- `image-to-editable-ppt-skill/skills/image-to-editable-ppt`

实测结果：

- `editppt` CLI 可在评测 venv 中安装。
- `editppt --help` 正常。
- `editppt doctor` 正常，显示：
  - Codex OAuth ready
  - image backend = `codex-oauth`
  - text hints = `builtin-ink`
  - `PADDLE_OCR_TOKEN` 未配置
- 用本次论文图 PNG 跑 `editppt prepare` 成功。
- `editppt run next` 进入 `rebuild_page_locally` 阶段。

限制：

- 完整重构前按 skill 要求应先询问是否配置 PaddleOCR token。
- 多页输入需要 page workers/subagents。
- 它是“图片/扫描页转可编辑 PPT”的专门工具，不是日常科研作图工具。

评分：6.5/10。
需要转 PPT 时很有价值；平时写论文和做数据图不建议作为核心。

### 5. PaperSpine

实测结果：

- 仓库内有完整 Codex/Claude/OpenClaw 分发目录。
- 有 `integrity_audit.py`、`translate_guard.py` 等审计脚本。
- 但主 orchestrator 要求配置缺失时优先启动 `launch_paperspine_ui.ps1`，并且在 Codex 说明里要求 `sandbox_permissions: require_escalated`。
- 当前环境的权限策略明确禁止提供 `sandbox_permissions`，而且这是 macOS + zsh 环境，PowerShell UI 不是顺手路径。

评分：5/10。
方法论很强，但当前本机 Codex 使用摩擦偏大。等它有纯 CLI / 非 PowerShell / 非 require_escalated 的入口后再考虑高频使用。

### 6. LaTeX Writer 与 Caveman

`claude-skills/skills/latex-writer`：

- 内容非常泛，只有“写好 LaTeX”的通用原则。
- 没有论文模板、编译检查、BibTeX 规范、错误修复流程等细节。
- 不建议作为科研写作核心 skill。

`caveman-claude-skill`：

- 确实能压缩表达模式。
- 对科研工作流本身帮助有限。
- 可以作为“长对话节省 token”的辅助，不应影响正式论文写作。

## 推荐安装/使用优先级

### 第一优先级：马上值得试

1. K-Dense `statistical-analysis`
2. K-Dense `statistical-power`
3. K-Dense `scientific-visualization`
4. K-Dense `exploratory-data-analysis`
5. Nature `nature-figure`
6. ARS `academic-research-suite`，主要用 experiment validate / citation check / reviewer 类模式

### 第二优先级：按场景启用

1. `image-to-editable-ppt`：只在图片/扫描 PPT 转可编辑 PPT 时用。
2. K-Dense `citation-management`：后续可以单独测引用核验。
3. K-Dense `scientific-writing` / `literature-review`：后续可以用真实论文草稿或 PDF 再测。

### 暂不建议投入

1. inbharatai `latex-writer`
2. PaperSpine 当前版本作为本机主工作流
3. Caveman 作为科研主流程 skill

## 实操建议

建议先把 K-Dense 和 Nature Figure 作为科研数据/作图主线：

1. EDA：K-Dense `exploratory-data-analysis`
2. 统计：K-Dense `statistical-analysis`
3. 样本量：K-Dense `statistical-power`
4. 作图：Nature `nature-figure` + K-Dense `scientific-visualization`
5. 审计：ARS `experiment-agent validate`

这个组合已经能覆盖从“数据到手”到“论文结果段落 + 图 + 复现审计”的完整小闭环。
