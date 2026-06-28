# 抖音视频涉及 Skills 的 GitHub 仓库清单

整理时间：2026-06-28
来源视频分析文档：`/Users/jacklee/develop/daillyTasks/openvideo_douyin_research_skills_analysis.md`
整理原则：只收录能在 GitHub 上确认到仓库的 skill / 工具；名称相同但无法确认就是视频原仓库的，单独标为“相近/需复核”。

## 一、确认度高：与视频名称或画面信息直接匹配

| 视频中名称 | GitHub 仓库 | 仓库性质 | 匹配依据 | 备注 |
| --- | --- | --- | --- | --- |
| `K-Dense-AI / claude-scientific-skills` | https://github.com/K-Dense-AI/scientific-agent-skills | 科研 Agent Skills 库 | 视频截图中的 `K-Dense-AI/claude-scientific-skills` 当前指向/对应 `K-Dense-AI/scientific-agent-skills`；仓库描述为科学 agent skills 库 | 覆盖生信、化学、医学、统计、数据库等；视频第二条主要讲这个 |
| `Nature-skills` / `Nature Figure` | https://github.com/Yuan1z0825/nature-skills | Nature 风格论文写作/科研绘图 skills | 仓库名精确匹配 `Nature-skills`；仓库内确认有 `skills/nature-figure/SKILL.md` | 第一条视频中的 `Nature Figure` 和第四条清单中的 `Nature-skills` 都可归到这里优先复核 |
| `Academic Research Skills` | https://github.com/Imbad0202/academic-research-skills-codex | Codex-native 学术研究 skills 套件 | 仓库名和第四条清单名称匹配；仓库描述为 Codex-native Academic Research Skills | 另有 Claude Code 版：https://github.com/Imbad0202/academic-research-skills |
| `PaperSpine` | https://github.com/WUBING2023/PaperSpine | 论文结构/论证/改写 skills | 仓库名精确匹配；仓库内有多个 `paper-spine-*` 的 `SKILL.md` | 用于拆论文论证主线、修改稿件、引用支撑等 |
| `Image to Editable PPT` | https://github.com/ningzimu/image-to-editable-ppt-skill | Codex skill | 仓库名和视频中的“image to editable ppt”匹配；仓库内有 `skills/image-to-editable-ppt/SKILL.md` | 第一条视频中用于把机制图转为可编辑 PPT；复杂图仍需人工修 |
| `Caveman Claude` | https://github.com/amanattar/caveman-claude-skill | Claude skill | 仓库名精确匹配；仓库根目录有 `SKILL.md` | 第三条视频中用于压缩表达、减少 token；README 说明约可减少 75% 词量 |
| `pyPRISM` | https://github.com/usnistgov/pyPRISM | Python 科研计算库，不是 skill | 第一条视频画面明确使用 `pyPRISM`，仓库为同名 Python 包 | 视频里把它用于生成 GraphPad/Prism 可编辑图的流程；实际用途是 PRISM 计算框架，科研绘图前要复核适用性 |
| `Skills CLI` / `skills.sh` 生态 | https://github.com/anthropics/skills | Agent Skills 公共仓库 | 第三条视频截图出现 `npx skills find/add/check/update` 和 `skills.sh`；该仓库 README 指向 `skills.sh` | 这是官方/公共 skills 参考库，不等同于某一个科研 skill |

## 二、确认度中：有同名或高度相近仓库，但需人工复核是否就是视频原作者所指

| 视频中名称 | 候选 GitHub 仓库 | 仓库性质 | 为什么收录 | 复核建议 |
| --- | --- | --- | --- | --- |
| `Skill Creator` | https://github.com/FrancyJGLisboa/agent-skill-creator | 跨平台 agent skill creator | 仓库描述是把工作流转为可复用 AI agent skills，且根目录有 `SKILL.md` | 第三条视频里的 `Skill Creator` 也可能指某个内置/平台自带 skill；安装前先看 README 和 `SKILL.md` |
| `Skill Creator` | https://github.com/inbharatai/claude-skills/tree/main/skills/skill-creator | skill 集合中的单个 skill | 目录精确为 `skills/skill-creator/SKILL.md` | 适合作为同名 skill 的备选 |
| `LaTeX Writer` | https://github.com/inbharatai/claude-skills/tree/main/skills/latex-writer | skill 集合中的单个 skill | 目录精确为 `skills/latex-writer/SKILL.md` | 第四条只给了名称，未给仓库；这是可复核同名候选 |
| `LaTeX Writer` | https://github.com/EvolvingLMMs-Lab/lmms-lab-writer | Agentic LaTeX Writer 应用 | 仓库描述为 Agentic LaTeX Writer | 更像应用/编辑器，不是单个 Codex skill；如果目标是写论文 LaTeX，可作为工具候选 |
| `Grant Writer` | https://github.com/inbharatai/claude-skills/tree/main/skills/grant-writer | skill 集合中的单个 skill | 目录精确为 `skills/grant-writer/SKILL.md` | 第四条只给名称；这是同名 skill 候选 |
| `Grant Writer` | https://github.com/HuiyuLi-2000/Chinese-Grant-Writer-Skills | 中文基金申请书 skills 集 | 仓库描述覆盖 NSFC/NSSFC/省部级申请书写作，仓库内有多个 `fund-*` 的 `SKILL.md` | 更适合中文基金/国自然场景 |
| `Grant Writer` | https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/research-grants | K-Dense 科研 grants skill | K-Dense 仓库内有 `skills/research-grants/SKILL.md` | 如果已经采用 K-Dense 科研 skill 库，这个更统一 |
| `Survey Builder` | https://github.com/AlterLab-IEU/AlterLab-FC-Skills/tree/main/skills/rma/alterlab-rma-survey-builder | 调研方法相关 survey builder skill | 目录名包含 `survey-builder` 且有 `SKILL.md` | 偏传播/研究方法场景；是否适合科研问卷要看 `SKILL.md` |
| `Survey Builder` | https://github.com/inbharatai/claude-skills/tree/main/skills/survey-designer | skill 集合中的 survey designer | 目录名为 `survey-designer/SKILL.md` | 名称不是 builder，但用途相近 |
| `Paper RAG` | https://github.com/Guangwen0429/paper-rag | 学术论文 RAG 工具 | 仓库名精确为 `paper-rag`，描述为 Citation-Grounded Academic QA | 不是已确认的 `SKILL.md` skill 仓库；更像应用/工具 |
| `Cite Verify` | https://github.com/uu999/CiteVerify | 引用真伪/相关性检查工具 | 仓库名精确为 `CiteVerify`，描述为检查参考文献真伪性、引用相关性 | 不是已确认的 `SKILL.md` skill 仓库；可作为引用核验工具候选 |
| `Cite Verify` / 引文核验 | https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/citation-management | K-Dense 引文管理 skill | K-Dense 仓库内有 `skills/citation-management/SKILL.md`，含 citation validation 脚本 | 名称不是 `Cite Verify`，但功能相关 |

## 三、暂未确认精确 GitHub 仓库

这些名称来自第四条视频的“十大科研 skills”图片，但本次没有找到可以高置信对应的视频原仓库。

| 视频中名称 | 状态 | 可替代候选 |
| --- | --- | --- |
| `Stats Sanity` | 未确认精确仓库 | K-Dense 的 `statistical-analysis` 和 `statistical-power`：https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/statistical-analysis 、https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/statistical-power |
| `Repro Pack` | 未确认精确仓库 | 本次未找到明确的科研/Claude Code/Codex 同名 skill 仓库；搜索结果里有一些 “repro pack” 项目，但不是视频语境下的科研 skill |

## 四、按视频归类

### 1. 胖胖的科研笔记：科研绘图

- `Nature Figure` / `Nature-skills`：https://github.com/Yuan1z0825/nature-skills
- `Image to Editable PPT`：https://github.com/ningzimu/image-to-editable-ppt-skill
- `pyPRISM`：https://github.com/usnistgov/pyPRISM

### 2. 拉钩仙人：Claude Scientific Skills / K-Dense

- K-Dense 科研 skills 总仓库：https://github.com/K-Dense-AI/scientific-agent-skills

### 3. 小徐读博记：Codex 基础 Skill

- `Skill Creator` 候选：https://github.com/FrancyJGLisboa/agent-skill-creator
- `Skill Creator` 备选目录：https://github.com/inbharatai/claude-skills/tree/main/skills/skill-creator
- Skills 公共仓库 / skills.sh 生态：https://github.com/anthropics/skills
- `Caveman Claude`：https://github.com/amanattar/caveman-claude-skill

### 4. AI大铁牛：十大科研 Skills

- `Nature-skills`：https://github.com/Yuan1z0825/nature-skills
- `Academic Research Skills`：https://github.com/Imbad0202/academic-research-skills-codex
- `PaperSpine`：https://github.com/WUBING2023/PaperSpine
- `Paper RAG` 候选：https://github.com/Guangwen0429/paper-rag
- `Cite Verify` 候选：https://github.com/uu999/CiteVerify
- `LaTeX Writer` 候选：https://github.com/inbharatai/claude-skills/tree/main/skills/latex-writer
- `Stats Sanity`：未确认精确仓库；可先看 K-Dense `statistical-analysis`
- `Repro Pack`：未确认精确仓库
- `Survey Builder` 候选：https://github.com/AlterLab-IEU/AlterLab-FC-Skills/tree/main/skills/rma/alterlab-rma-survey-builder
- `Grant Writer` 候选：https://github.com/inbharatai/claude-skills/tree/main/skills/grant-writer

## 五、建议优先级

如果后续要真正安装/试用，建议先按这个顺序：

1. `Nature-skills`：和第一条/第四条都强相关，且包含 `nature-figure`。
2. `Image to Editable PPT`：第一条视频明确展示的机制图转可编辑 PPT。
3. `Academic Research Skills Codex`：面向 Codex 的学术研究套件。
4. `PaperSpine`：论文结构、论证和改写方向明确。
5. `K-Dense scientific-agent-skills`：覆盖面最大，但要按具体任务挑 skill，避免一次性全装后难以管理。
6. `Caveman Claude`：适合高频长对话降低 token 成本，但科研写作正式输出时要切回正常表达。

## 六、核验记录

- 使用 GitHub CLI 查询仓库元数据、默认分支和目录树。
- 已确认多个候选仓库中存在 `SKILL.md` 或明确的 `skills/` 目录。
- 对于视频只给名称但未给地址的条目，按“名称精确度 + 仓库描述 + 是否有 `SKILL.md`”分级。
- GitHub 搜索接口中途触发限流，因此后半段优先用直接仓库读取和目录树核验。
