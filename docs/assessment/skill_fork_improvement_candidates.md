# 科研 Skills Fork 改造候选清单

整理时间：2026-06-28
基础评测文档：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/research_skill_evaluation_report.md`
目标：挑出值得 fork/抽取/重写的 skill，改造成适合本机 Codex、科研写作、实验数据分析和论文作图的高可用 skills。

## 结论先行

最值得做的不是 fork 一个大仓库后全部维护，而是新建一个精选仓库，例如：

`JackLee992/research-skills-practical`

仓库只放高频科研闭环：

1. `research-eda`
2. `research-statistics`
3. `research-power`
4. `research-figure`
5. `research-citation-check`
6. `research-results-audit`
7. `research-writing-lite`
8. `paper-spine-lite`，可作为第二阶段

这样比直接 fork K-Dense 的 147 个 skill 更容易维护，也更符合实际科研工作流：数据体检 -> 统计 -> 样本量 -> 作图 -> 引用核验 -> 结果审计 -> 论文段落。

## 一、最值得优先改造

### 1. K-Dense 统计/作图组合

来源：

- https://github.com/K-Dense-AI/scientific-agent-skills
- license：MIT
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/scientific-agent-skills`

相关 skill：

- `statistical-analysis`
- `statistical-power`
- `scientific-visualization`
- `exploratory-data-analysis`

为什么值得改：

- 已经实测可跑真实数据。
- 有 Python 脚本，不只是提示词。
- 能生成 EDA、统计表、power curve、论文图。
- 小补丁就能明显提高稳定性。

本次实测暴露的问题：

- `pingouin` 列名兼容：旧示例常写 `p-unc`，当前版本输出 `p_unc`。
- `check_figure_size()` 返回 NumPy 标量，直接写 JSON 会失败。
- SVG 默认可能把文字转成 path，需要显式设置 `svg.fonttype = none`。
- Levene 方差齐性失败时，skill 应自动建议 Welch ANOVA / Games-Howell / 非参数敏感性分析。
- EDA analyzer 只做基础体检，缺少科研问题导向的后续建议。

建议改造成：

| 新 skill | 改造内容 |
| --- | --- |
| `research-eda` | CSV/XLSX 一键体检；缺失值、异常值、分组计数、相关性、推荐统计路线；输出 Markdown + CSV + 可选图 |
| `research-statistics` | 自动选择 t-test/ANOVA/Welch/非参数/回归；统一 p-value 列名兼容；输出 APA/Nature 风格结果段 |
| `research-power` | 统一样本量、MDE、power curve；支持 dropout、multiple-comparison、cluster design 注释 |
| `research-figure` | 合并 K-Dense 导出工具 + Nature figure contract；自动检查尺寸、空图、SVG 可编辑文本、色盲友好 |

优先级：P0。
改造难度：低到中。
预期收益：最高。

### 2. Nature Figure

来源：

- https://github.com/Yuan1z0825/nature-skills
- license：Apache 2.0
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/nature-skills`

相关 skill：

- `nature-figure`

为什么值得改：

- 作图前的 figure contract 非常好：核心结论、证据链、图类型、导出格式。
- 很适合与 K-Dense 的绘图脚本合并。
- 本次实测发现它的原则能直接抓出 SVG 文字不可编辑问题。

建议改造：

- 抽取 `figure-contract`、`backend gate`、`QA contract`，合并进我们的 `research-figure`。
- 默认 Python 路线增加：
  - `svg.fonttype = none`
  - `pdf.fonttype = 42`
  - SVG `<text>` 数量检查
  - PDF/SVG/PNG/TIFF 文件存在和大小检查
  - matplotlib/seaborn 版本记录
- 增加 `figure_qa.py`：
  - 检查是否空白图
  - 检查宽高是否符合 Nature/Science/Cell/自定义 mm 规格
  - 检查是否有可编辑文本
  - 检查是否有过多单色系或红绿冲突
  - 输出 `figure_qa_report.md`

优先级：P0。
改造难度：中。
预期收益：很高。

### 3. Citation Management

来源：

- https://github.com/K-Dense-AI/scientific-agent-skills
- license：MIT
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/scientific-agent-skills/skills/citation-management`

为什么值得改：

- 已实测 `doi_to_bibtex.py` 能通过 DOI 生成 BibTeX。
- 自带 `validate_citations.py`、`extract_metadata.py`、`format_bibtex.py`。
- 论文写作里引用错误很常见，核验价值高。

本次看到的问题：

- skill 里有不必要的“默认生成科学示意图”建议，会干扰 citation 核心任务。
- 大量流程依赖 `parallel-cli` / Google Scholar scraping，实际环境不一定可用。
- 需要更明确的本地优先路径：DOI/CrossRef/PubMed/arXiv -> BibTeX -> validate -> report。

建议改造成：

`research-citation-check`

核心功能：

- 输入 DOI/PMID/arXiv/BibTeX/Markdown。
- 输出：
  - `references.bib`
  - `citation_validation_report.md`
  - `citation_validation_report.json`
- 每条引用给状态：
  - `VERIFIED`
  - `METADATA_MISMATCH`
  - `MISSING_REQUIRED_FIELDS`
  - `DOI_UNRESOLVED`
  - `NEEDS_MANUAL_REVIEW`
- 默认使用 CrossRef / PubMed / arXiv 官方接口。
- Web 搜索只作为 fallback，并且明确标记。

优先级：P1。
改造难度：中。
预期收益：高。

## 二、高潜力但需要治理

### 4. Scientific Writing / Literature Review

来源：

- https://github.com/K-Dense-AI/scientific-agent-skills
- license：MIT
- 本地路径：
  - `scientific-writing`
  - `literature-review`

为什么值得改：

- 覆盖 IMRAD、引用格式、报告规范、文献综述流程。
- 有模板和 citation style references。
- 和我们前面的统计/图/引用核验能形成完整论文工作流。

主要问题：

- `scientific-writing` 强制每篇 scientific paper 都生成 graphical abstract 和额外 AI 图，不适合严肃科研默认流程。
- `literature-review` 强制每篇综述生成 AI 图，也不稳。
- `literature-review` 把 `parallel-cli` 作为主搜索工具，但本机未确认该工具可用；而且正式综述更应该优先用 PubMed、CrossRef、OpenAlex、Semantic Scholar、arXiv 等可追溯接口。
- 缺少“已有实验结果 -> 结果段落/讨论段落”的轻量模式。

建议改造成：

| 新 skill | 改造内容 |
| --- | --- |
| `research-writing-lite` | 只处理已有结果、图、表、引用；输出 Results/Methods/Discussion 段落；不生成事实和数据 |
| `research-lit-review` | 可复现检索协议；数据库、检索式、纳排标准、PRISMA 流程；不默认生成 AI 图 |

关键原则：

- 禁止虚构数据、p 值、引用。
- 图只在用户明确要求或材料支持时生成。
- 输出必须带 evidence map：每个 claim 对应哪个数据/图/引用。
- 文献检索要记录检索式、日期、数据库、返回数量。

优先级：P1。
改造难度：中到高。
预期收益：高。

### 5. Academic Research Suite / experiment-agent validate

来源：

- https://github.com/Imbad0202/academic-research-skills-codex
- license：CC BY-NC 4.0
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/academic-research-skills-codex`

为什么值得改：

- `experiment-agent validate` 的统计审计结构很好。
- 11 类 fallacy scan 对论文结果解释很有用。
- Material Passport 有利于多阶段追踪。

限制：

- CC BY-NC 4.0，有非商业限制。
- 如果我们要做可公开、可商业使用的通用仓库，不应直接复制大量内容。

建议：

- 个人/非商业 fork 可以保留和改。
- 如果想做 MIT/Apache 的自有仓库，建议“借鉴思想，重写实现”：
  - `research-results-audit`
  - 自己写统计审计模板
  - 自己写 reproducibility hash check
  - 自己写 fallacy checklist

优先级：P1。
改造难度：中。
预期收益：高。
许可风险：中。

## 三、值得二阶段改造

### 6. Image to Editable PPT

来源：

- https://github.com/ningzimu/image-to-editable-ppt-skill
- license：MIT
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/image-to-editable-ppt-skill`

为什么值得改：

- CLI 可以安装，`doctor` 和 `prepare` 已跑通。
- Codex OAuth 已可用。
- 对“图片/扫描版 PPT -> 可编辑 PPT”很有价值。

不适合作为第一阶段的原因：

- 完整转换工作流较重。
- OCR token、图像后端、多页 subagent 都会影响稳定性。
- 日常科研作图更应该走 SVG/PDF/TIFF 源文件，而不是图片反向重构。

建议改造方向：

1. 保留原 `image-to-editable-ppt` 作为专用工具。
2. 另做轻量 skill：`figure-to-pptx`
   - 输入 SVG/PDF/PNG + 图注。
   - 优先 SVG/PDF 直接嵌入或转换成 PPT 可编辑对象。
   - 不默认调用图像生成。
   - 目标是科研汇报里的“论文图 -> PPT slide”，不是扫描页重建。

优先级：P2。
改造难度：中到高。
预期收益：中。

### 7. PaperSpine

来源：

- https://github.com/WUBING2023/PaperSpine
- license：MIT
- 本地路径：`/Users/jacklee/develop/daillyTasks/research_skill_evaluation/repos/PaperSpine`

为什么值得改：

- 论文写作方法论很强。
- 分支 skill 完整：intake、research、citation、rewrite、latex、audit。
- MIT，适合 fork。

主要问题：

- Codex orchestrator 在配置缺失时强制先跑 `launch_paperspine_ui.ps1`。
- skill 文档要求 `sandbox_permissions: require_escalated`，而当前环境明确禁止传这个参数。
- macOS/zsh 下 PowerShell TUI 不是顺手路径。
- 全流程过重，不适合快速写论文结果段落或小报告。

建议改造成：

`paper-spine-lite`

核心改法：

- 去掉强制 PowerShell UI gate。
- 增加纯 Markdown/JSON intake fallback。
- 分成轻量模式：
  - `rewrite_existing`
  - `build_from_materials`
  - `results_section`
  - `response_to_reviewers`
- `research_dossier` 和 `citation_support_bank` 可以选配，不必每次强制全跑。
- 保留 `integrity_audit.py`，但让它能对任意 Markdown 产物跑。

优先级：P2。
改造难度：高。
预期收益：高，但不是最短路径。

## 四、不建议 fork，适合重写

### 8. inbharatai LaTeX Writer

来源：

- https://github.com/inbharatai/claude-skills
- license：MIT

问题：

- `latex-writer` 内容过泛。
- 没有科研论文模板、BibTeX 管理、编译日志修复、图表插入、期刊格式等核心细节。

建议：

不要 fork 这个 skill。可以新写：

`research-latex-writer`

功能：

- 从 `results.md + figure + references.bib` 生成 LaTeX。
- 支持 article / beamer / thesis chapter。
- 自动运行 `tectonic` 或 `pdflatex`，解析错误日志。
- 输出 `compile_report.md`。

优先级：P3。
改造难度：中。
预期收益：中。

### 9. Caveman Claude

来源：

- https://github.com/amanattar/caveman-claude-skill

结论：

- 可以保留为 token 压缩模式。
- 不值得作为科研 skill 改造对象。

## 五、推荐 fork/新建策略

### 推荐策略 A：新建精选仓库，而不是直接 fork 大仓

建议仓库名：

`JackLee992/research-skills-practical`

建议结构：

```text
research-skills-practical/
  LICENSE
  NOTICE.md
  README.md
  skills/
    research-eda/
      SKILL.md
      scripts/
      references/
      tests/
    research-statistics/
      SKILL.md
      scripts/
      references/
      tests/
    research-power/
      SKILL.md
      scripts/
      references/
      tests/
    research-figure/
      SKILL.md
      scripts/
      references/
      tests/
    research-citation-check/
      SKILL.md
      scripts/
      references/
      tests/
    research-results-audit/
      SKILL.md
      scripts/
      references/
      tests/
    research-writing-lite/
      SKILL.md
      templates/
      tests/
```

优点：

- 安装轻。
- 每个 skill 都能有测试数据和 smoke test。
- 不受 147 个上游 skill 的维护噪音影响。
- 可以同时吸收 MIT/Apache 来源，并避开 CC BY-NC 的商业限制。

### 推荐策略 B：对上游 fork 做 patch，再回流 PR

适合：

- K-Dense 的小 bug：
  - p-value 列名兼容
  - figure size JSON 序列化
  - SVG 可编辑文本默认设置
- Nature Figure 的 QA 增强。

不适合：

- 大幅改写 writing/literature-review 默认理念。
- PaperSpine 的入口流程重构。

## 六、第一阶段建议任务包

### Sprint 1：做一个能直接安装的最小高可用包

目标：7 天内完成一个可安装、可实测的 `research-skills-practical`。

范围：

1. `research-eda`
2. `research-statistics`
3. `research-power`
4. `research-figure`

验收标准：

- 用 Palmer Penguins 数据一键跑通。
- 生成：
  - `eda_report.md`
  - `statistical_results.md`
  - `power_report.md`
  - `figure_qa_report.md`
  - SVG/PDF/PNG/TIFF
- 每个 skill 有 `SKILL.md`、`scripts/`、`tests/fixtures/`。
- 安装到 `~/.codex/skills` 后能在新 Codex 会话触发。

### Sprint 2：补 citation 和 results audit

范围：

1. `research-citation-check`
2. `research-results-audit`

验收标准：

- DOI -> BibTeX 跑通。
- BibTeX/Markdown 引用核验输出报告。
- 统计结果审计能检查：
  - 假设检验
  - 效应量
  - multiple comparison
  - causal wording
  - reproducibility hash

### Sprint 3：写作和 LaTeX

范围：

1. `research-writing-lite`
2. `research-latex-writer`

验收标准：

- 输入已有数据/图/统计报告/引用，生成 Results + Methods + Discussion 初稿。
- 每个 claim 都能追溯到数据、图或引用。
- LaTeX 可编译，并输出编译报告。

## 七、当前建议优先级

| 排名 | 动作 | 原因 |
| --- | --- | --- |
| 1 | 新建 `research-skills-practical` | 最符合我们的实际需求 |
| 2 | 先做 `research-figure` | 本次已经发现并修掉真实 SVG 可编辑性问题 |
| 3 | 做 `research-statistics` | 直接解决 p-value 兼容、Welch/非参数选择 |
| 4 | 做 `research-eda` | 数据到手第一步，高频 |
| 5 | 做 `research-citation-check` | DOI/BibTeX 已实测可用，论文高价值 |
| 6 | 做 `research-results-audit` | 让论文结果不乱写因果和显著性 |
| 7 | 再考虑 PaperSpine Lite | 收益高但工程量大 |

## 八、可以直接执行的下一步

如果决定开工，我建议执行：

```bash
mkdir -p /Users/jacklee/develop/daillyTasks/research-skills-practical
cd /Users/jacklee/develop/daillyTasks/research-skills-practical
git init
```

然后从本次评测脚本中抽取已经跑通的逻辑：

- `/Users/jacklee/develop/daillyTasks/research_skill_evaluation/run_penguins_skill_eval.py`
- K-Dense `assumption_checks.py`
- K-Dense `power.py`
- K-Dense `figure_export.py`
- K-Dense `style_presets.py`
- K-Dense `doi_to_bibtex.py`
- Nature Figure 的 contract/QA 思路

最后创建 GitHub 仓库并推送：

```bash
gh repo create JackLee992/research-skills-practical --private --source=. --remote=origin --push
```

我建议先建私有仓库，等 license/attribution/NOTICE 都整理干净后再决定是否公开。
