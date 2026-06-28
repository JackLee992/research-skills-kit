# 科研 Skills 改造进度

更新时间：2026-06-28
仓库：`JackLee992/research-skills-kit`
目标：把视频和实测中高价值的科研 skills 改造成本机 Codex 可安装、可复现、可长期维护的精选 skills kit。

## 阶段结论

第一阶段已经完成并调整架构：上游完整能力通过 fork + submodule 管理，本仓库提供路由 skill 和验证过的本地增强层。

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| OpenVideo 信息提炼 | 完成 | 4 条抖音视频 / 图文的信息、技能名、用途和本地证据已归档。 |
| GitHub 仓库确认 | 完成 | 已确认 K-Dense、Nature-skills、Academic Research Skills、PaperSpine、Image to Editable PPT 等仓库。 |
| 实测评估 | 完成 | 用 Palmer Penguins 数据跑 EDA、统计、power、作图、结果审计。 |
| Fork / 改造候选分析 | 完成 | P0/P1/P2/P3 候选已整理。 |
| 上游 fork 创建 | 完成 | 已 fork K-Dense、Nature-skills、Academic Research Skills Codex、PaperSpine、Image to Editable PPT。 |
| Submodule 管理 | 完成 | `upstreams/` 已指向 JackLee992 名下 fork。 |
| 第一阶段 kit 落地 | 完成 | 1 个上游路由 skill + 6 个本地增强 skills 已实现、验证、提交并推送。 |
| 本机安装 | 完成 | 6 个本地增强 skills 已安装到 `~/.codex/skills`；路由 skill 可从本仓库安装。 |

## 上游 Fork / Submodule 状态

| Fork | Submodule path | 当前指针 | 用途 |
| --- | --- | --- | --- |
| `JackLee992/scientific-agent-skills` | `upstreams/scientific-agent-skills` | `9c9bd2e` | K-Dense 全量科学 skills，含 EDA、统计、power、可视化、citation。 |
| `JackLee992/nature-skills` | `upstreams/nature-skills` | `6edea02` | Nature 风格作图、写作、引用、审稿、回复。 |
| `JackLee992/academic-research-skills-codex` | `upstreams/academic-research-skills-codex` | `36cc610` | Academic Research Suite / experiment validation。 |
| `JackLee992/PaperSpine` | `upstreams/PaperSpine` | `a7fe540` | PaperSpine 论文结构、改写、引用、LaTeX、审计。 |
| `JackLee992/image-to-editable-ppt-skill` | `upstreams/image-to-editable-ppt-skill` | `698b16f` | Image to Editable PPT。 |

## 已落地 Skills

| Skill | 状态 | 来源思路 | 已实现能力 | 验证证据 |
| --- | --- | --- | --- | --- |
| `research-upstream-router` | 已落地 | fork + submodule 调用完整上游子 skills | 按任务路由到 K-Dense、Nature、ARS、PaperSpine、Image-to-PPT 子 skills；安装后自带上游清单 helper | `quick_validate.py`、`tests/router_tool_test.py`、`scripts/list_upstream_skills.py --profile core` |
| `research-eda` | 已落地 | K-Dense `exploratory-data-analysis` | CSV/XLSX 数据体检、缺失值、数值摘要、相关矩阵、分组计数、Markdown 报告 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/penguins_eda_report.md` |
| `research-statistics` | 已落地 | K-Dense `statistical-analysis` + Stats Sanity 思路 | 正态性、方差齐性、t-test/ANOVA/非参数、效应量、OLS 回归、结果段落 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/penguins_statistical_results.md` |
| `research-power` | 已落地 | K-Dense `statistical-power` | 样本量、power curve、MDE/功效规划报告 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/power_curve_points.csv` |
| `research-figure` | 已落地 | Nature Figure + K-Dense visualization | SVG/PDF/PNG/TIFF 导出、可编辑文字设置、图像 QA、空图检测 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/penguins_nature_figure.svg` |
| `research-citation-check` | 已落地 | K-Dense `citation-management` + Cite Verify 思路 | DOI/BibTeX 解析、CrossRef 校验、BibTeX 输出、离线状态标记 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/citation_online_report.md` |
| `research-results-audit` | 已落地 | ARS experiment-agent validate 思路 | p-value、效应量、因果措辞、假设检查、文件 hash 审计 | `tests/smoke_test.py`、`docs/raw/evaluation/outputs/ars_experiment_validation_report.md` |

## 当前验证记录

最近一次发布前验证：

```bash
.venv/bin/python tests/smoke_test.py
for d in skills/*; do python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d"; done
.venv/bin/python -m compileall -q skills tests
```

验证结果：

- smoke test：`smoke test PASS`
- 6 个 `SKILL.md`：全部 `Skill is valid!`
- Python 编译检查：退出码 0
- 从 GitHub 临时安装验证：6 个 skills 均能安装并包含 `SKILL.md`

## 改造候选 Backlog

| 优先级 | 候选 | 建议动作 | 当前状态 |
| --- | --- | --- | --- |
| P1 | `research-writing-lite` | 输入已有数据、图、统计报告、引用，生成 Results / Methods / Discussion 初稿；每个 claim 绑定证据 | 未开始 |
| P1 | `research-lit-review` | 可复现检索协议，记录数据库、检索式、日期、返回数量、纳排标准 | 未开始 |
| P2 | `figure-to-pptx` | 从 SVG/PDF/PNG 和图注生成科研汇报 PPT，不走扫描页反向重构 | 未开始 |
| P2 | `paper-spine-lite` | 把 PaperSpine 的论文结构方法论改成纯 Markdown/JSON intake，无 PowerShell UI gate | 未开始 |
| P3 | `research-latex-writer` | 从结果、图、BibTeX 生成 LaTeX，并编译/解析错误日志 | 未开始 |
| P3 | `grant-writing-cn` | 面向国自然/中文基金的轻量写作与检查流程 | 未开始 |
| 不建议 | `caveman-claude` 科研化 | 只作为 token 压缩辅助，不进入科研主流程 | 暂停 |

## 上游 Patch 候选

| 上游 | Patch 方向 | 备注 |
| --- | --- | --- |
| K-Dense scientific-agent-skills | `p-unc` / `p_unc` 兼容、NumPy scalar JSON 序列化、统计路线建议 | 适合开小 PR。 |
| Nature-skills | SVG 可编辑文本默认设置、figure QA 检查、色盲友好检查 | 适合 PR 或在本仓库继续增强。 |
| Image to Editable PPT | 科研图转 PPT 的轻量路径 | 更像二阶段新 skill，不一定回流上游。 |
| PaperSpine | 纯 CLI / Markdown fallback，去掉 PowerShell UI hard gate | 工程量较大，适合先做 lite 重写。 |

## 下一步建议

1. 给每个已落地 skill 增加一个 `examples/` 目录，放最小输入和预期输出。
2. 把 `tests/smoke_test.py` 拆成分 skill 的 smoke tests，再保留一个全链路 test。
3. 做 `research-writing-lite`，把当前统计报告、图注、引用报告变成论文 Results/Methods 初稿。
4. 给 `research-citation-check` 增加 PubMed/arXiv/OpenAlex fallback。
5. 给 `research-figure` 增加色盲友好、DPI、字体嵌入和 journal preset 检查。
