# OpenVideo 抖音科研 / Codex Skills 信息提炼

分析时间：2026-06-28
分析目标：从 4 条抖音视频 / 图文作品中提炼“科研、Codex、Claude Code skill”相关的具体信息。语音信息不足时，补充分析关键帧、OCR 和图文原图。

## 总结

这 4 条内容共同指向一个趋势：科研工作中的 AI 使用正在从“问答聊天”转向“把具体流程沉淀成 skill / agent workflow”。视频里提到的高频场景包括科研绘图、GraphPad/Prism 可编辑图生成、机制图转 PPT、文献/数据/代码/论文润色自动化、科研技能库检索与安装、以及面向科研的 Claude Code skills 清单。

最值得马上整理成自己工作流的是：

1. 科研绘图：用 `Nature Figure` 这类 skill 从原始数据生成 Nature 风格图表，并输出可编辑 / 投稿前处理用的文件。
2. 可编辑图表：用 `pyPRISM` 生成 GraphPad Prism 可打开的文件，适合后续手动调颜色、线型、形状。
3. 机制图转换：用 `Image to Editable PPT` 把机制图转成 PPT 可编辑对象，但复杂图细节会丢失，不能当成最终稿。
4. Codex 基础 skill：先理解 skill 是可复用流程包，再用 `Skill Creator`、`find skills / Skills CLI`、`Caveman Claude` 一类工具减少重复工作。
5. 科研 skill 库：`K-Dense-AI/claude-scientific-skills` 展示了覆盖生信、药物发现、蛋白质组学、临床研究、医学影像、统计可视化等方向的科学技能集合。

## 1. 胖胖的科研笔记：Codex Skills 搞定科研绘图全流程

来源：`https://v.douyin.com/16yECC1l53c/`
作者：胖胖的科研笔记（全网同名）
标题：不骗你真有用 #科研 #硕士 #博士 #skills #科研绘图
素材类型：视频，94.17 秒，有音频
OpenVideo 证据：完整视频下载成功，ASR + OCR + 12 张关键帧

### 核心信息

这条视频把“科研绘图”拆成 3 个阶段：

1. 用 `Nature Figure` 生成科研图。
2. 用 Codex 生成 GraphPad Prism 可以打开和编辑的图。
3. 把复杂机制图转换为可编辑 PPT。

### `Nature Figure` 的作用

画面标题写的是“codex skills 搞定科研绘图全流程”，并列出 `nature figure` 的优缺点：

- 适合自然科学领域。
- 可以输入实验数据，直接得到图表。
- 可以生成 `SVG` 可编辑格式。
- 不应直接用于投稿，需要人工核验和后处理。

画面示例中，用户上传了 `260621.xlsx`，提示类似“这是我的数据，根据这个数据生成符合 Nature 期刊的图”。输出包含：

- Nature 风格时间趋势图。
- `SVG` 可编辑版。
- `600 dpi TIFF`。
- 图注。
- 质控说明。

### GraphPad / Prism 可编辑图

视频第二段解决的问题是：如何让 Codex 生成 GraphPad 可以打开的图。

画面中给出的思路：

- 让 Codex 安装并验证 Python 库 `pyPRISM`。
- 阅读文档：`https://pyprism.readthedocs.io/en/latest/index.html`。
- 上传数据表，例如 `260621.xlsx`。
- 给一个参考截图，要求按参考风格画图。
- 输出 Prism 文件，同时生成 Python 风格预览和 Prism 原生预览。

画面中出现的结果信息包括：

- 安装并验证 `pyPRISM 1.0.3`。
- 使用 `pyPRISM.Domain` 建立计算网格。
- 根据表格数据绘制蓝色 / 红色曲线。
- 生成可编辑、打开后自带配色的 Prism 文件。

注意点：画面注释提到 `pyPRISM` 是拟合 / 计算库，GraphPad 导出的 Excel 数据不一定包含完整拟合模型参数，因此需要结合理论、官方资料和 GitHub 资料核验。

### 复杂机制图转可编辑 PPT

第三段标题是“机制图如何变成可编辑格式？- image to editable ppt”。画面中使用的提示类似：

> Image to Editable PPT 帮我把这个图变成可编辑的格式

它可以把机制图转换成 PPT 里的可编辑对象，但视频明确展示了限制：

- 对复杂机制图，转换出来的细节不够细。
- 如果没有配置 OCR/token，可能只能用边缘检测和粗略结构识别。
- 适合做初稿、拆解、局部重画参考，不适合直接作为最终科研图。

### 可复用做法

推荐把这条视频整理成一个自己的 Codex skill：

- 输入：原始实验数据、目标期刊风格、参考图、需要的输出格式。
- 流程：先生成 Nature 风格草图，再导出 SVG/TIFF，再生成 Prism 可编辑文件，最后人工校验统计、图注和投稿规范。
- 质量门槛：所有图表都需要人工检查统计逻辑、坐标轴、显著性、图例、单位和是否能投稿。

## 2. 拉钩仙人：Claude Scientific Skills / K-Dense 科研技能库

来源：`https://v.douyin.com/M0rcanywEfw/`
作者：拉钩仙人
标题：ai还是太全面了…快学吧 别毕业就失业了
素材类型：图文，3 张图片，无视频音轨
OpenVideo 证据：下载到 3 张图，OCR + 原图查看

### 核心信息

这条图文展示的是 GitHub 仓库：

`K-Dense-AI / claude-scientific-skills`

画面文案强调：

- “今天做 skills 分享，一个全面的生信分析 skills。”
- “内置 177 个 skills，基因组到蛋白组基本全都能做。”
- “扔给 AI 解决代码问题。”
- “AI 正在打破很多人自以为是的壁垒，只有不断积累，人类独有的能力是做好 AI 掌控者。”

### 覆盖领域

截图中的 README 显示，这套 skills 覆盖多个科学领域：

- 生物信息学与基因组学：序列分析、单细胞 RNA 测序、基因调控网络、变异注释、系统发育分析。
- 化学信息学与药物发现：分子性质预测、虚拟筛选、ADMET 分析、分子对接、先导优化。
- 蛋白质组学与质谱：LC-MS/MS 处理、肽鉴定、光谱匹配、蛋白质定量。
- 临床研究与精准医疗：临床试验、药物基因组学、变异解读、药物安全、临床决策支持、治疗计划。
- 医疗 AI 与临床机器学习：电子健康记录分析、生理信号处理、医学影像、临床预测模型。
- 医学影像与数字病理：DICOM 处理、整张幻灯片图像分析、计算病理学、放射学工作流程。
- 机器学习与人工智能：深度学习、强化学习、时间序列、模型可解释性、贝叶斯方法。
- 材料科学与化学：晶体结构分析、相图、代谢建模、计算化学。
- 物理与天文学：天文数据分析、坐标变换、宇宙学计算、符号数学、物理计算。
- 工程与仿真：离散事件模拟、多目标优化、代谢工程、系统建模、过程优化。
- 数据分析与可视化：统计分析、网络分析、时间序列、发表质量数据、大规模数据处理、EDA。
- 地理空间科学与遥感：卫星影像处理、GIS 分析、空间统计、地形分析、地球观测机器学习。
- 实验室自动化：液体处理协议、实验室设备控制、工作流自动化、LIMS 集成。
- 研究方法论：假设生成、科学头脑风暴、批判性思维、资助申请、学者评估。

### 示例任务

截图中能看到的示例包括：

- Single-Cell RNA-seq：目标是综合分析 10X Genomics 数据，并结合公共数据。
- Multi-Omics Biomarker Discovery：整合 RNA-seq、蛋白组学和代谢组学，用于预测患者结局。

这条内容没有展开安装步骤，主要价值是提示：科研人可以从“通用聊天”切换到“科学工具库 + workflow skill”的使用方式。

## 3. 小徐读博记：Codex 基础 Skill

来源：`https://v.douyin.com/Ul5jI9odtTQ/`
作者：小徐读博记
标题：是谁还不会用codex 第一期-基础skill
素材类型：视频，121.17 秒，有音频
OpenVideo 证据：完整视频下载成功，ASR + OCR + 关键帧补抽

### 核心信息

视频的主旨是：不要只把 AI 当聊天工具，Codex 更像能替你做事的 AI 助手。作者说自己会把重复工作交给 Codex，例如：

- 文献整理。
- 数据处理。
- 代码修改。
- 论文语言润色。

新手使用 Codex 的关键不是一开始问复杂问题，而是理解 `skill`：它是给 Codex 装的技能包，把固定流程沉淀下来，下次直接按流程执行。

### 推荐先了解的 3 个 skill / 工具

#### 1. Skill Creator

关键帧显示：

`Skill Creator` 是一个用来创建或更新 Codex 技能的指导型技能。

它主要帮助用户把以下内容整理成可复用的 `skill` 文件夹：

- 重复任务。
- 专业流程。
- 工具集成。
- `SKILL.md` 内容和 YAML frontmatter。
- `references/`、`scripts/`、`assets/` 等资源结构。
- UI 元数据，例如 `agents/openai.yaml`。

适合场景：

- 你经常处理同类论文、同类数据、同类图表或同类文案。
- 你有一套固定步骤，但每次都要重新讲给 Codex。
- 你想把一个流程变成“可自动加载知识和流程”的技能包。

#### 2. Find Skills / Skills CLI

关键帧显示“find skills”和 Skills CLI 的说明：

- `npx skills find [query]`：按关键词或交互方式搜索 skills。
- `npx skills add <package>`：从 GitHub 或其他来源安装 skill。
- `npx skills check`：检查 skill 更新。
- `npx skills update`：更新已安装 skills。
- 浏览地址：`https://skills.sh/`。

适合场景：

- 你问“有没有做 X 的 skill”。
- 你希望 Codex 帮你为当前任务找合适的 skill。
- 你需要处理表格、整理文献、生成 PPT 等任务，但不知道该装哪个 skill。

#### 3. Caveman Claude 类压缩表达 skill

视频口播说第三个 skill 很火，主要作用是压缩表达、减少废话，让 Codex 用更少 token 完成任务。关键帧中示例名为 `Caveman Claude`，对比了：

- Normal Claude：69 tokens。
- Caveman Claude：19 tokens。
- 同样表达约减少 75% 词量。

适合场景：

- 高频、重复、上下文成本高的任务。
- 需要节省 token 的长期对话。
- 希望 Codex 输出更短、更直接的执行指令。

### Skill 安装方式

视频里给了两种方式：

1. 直接让 Codex 安装：在聊天框输入“帮我安装某某 skill”。
2. 搜索到 skill 地址后，把完整地址复制给 Codex，让它安装。

作者也提醒：第一种方式有时效果不稳定，手动提供完整地址会更稳。

## 4. AI大铁牛：十大科研 Skills 清单

来源：`https://v.douyin.com/FNnl3lgKZKI/`
作者：AI大铁牛
标题：告别古法科研，从十个skill开始
素材类型：图文，1 张图片
OpenVideo 证据：下载到 1 张图，OCR + 原图查看

### 图片清单

图片标题是“最强十大科研skills（Claude Code）”，列出：

1. `Nature-skills`
2. `Academic Research Skills`
3. `PaperSpine`
4. `Paper RAG`
5. `Cite Verify`
6. `LaTeX Writer`
7. `Stats Sanity`
8. `Repro Pack`
9. `Survey Builder`
10. `Grant Writer`

### 可提炼用途

图片只给了名称，没有展开功能和安装地址。根据名称可以初步归类：

- 绘图 / 自然科学图表：`Nature-skills`
- 学术研究流程：`Academic Research Skills`
- 论文结构和阅读：`PaperSpine`
- 论文检索问答：`Paper RAG`
- 引文核验：`Cite Verify`
- LaTeX 写作：`LaTeX Writer`
- 统计合理性检查：`Stats Sanity`
- 可复现实验包：`Repro Pack`
- 问卷构建：`Survey Builder`
- 基金 / grant 写作：`Grant Writer`

这些用途是根据名称做的推断，图片本身没有给出详细说明。

## 可落地的个人工作流建议

1. 建一个“科研绘图 skill”：
   - 输入实验数据、参考图、目标期刊、输出格式。
   - 自动生成初稿图、SVG/TIFF、图注、质控说明。
   - 最后强制人工核验统计和投稿规范。

2. 建一个“Prism 图表转换流程”：
   - 让 Codex 安装/调用 `pyPRISM`。
   - 读取数据表和参考图。
   - 输出 Prism 文件、Python 预览和可编辑图。
   - 用 GraphPad 手动调整图形细节。

3. 建一个“文献 / 数据 / 代码重复任务 skill”：
   - 用 `Skill Creator` 把重复步骤写入 `SKILL.md`。
   - 对常见任务沉淀 `references/` 和 `scripts/`。
   - 后续让 Codex 自动加载流程，不再每次重复讲规则。

4. 建一个“科研 skill 目录”：
   - 收集 `Nature-skills`、`Paper RAG`、`Cite Verify`、`Stats Sanity` 等。
   - 对每个 skill 记录：来源、用途、适用任务、安装方式、验证命令。
   - 对没有验证过的 skill 标注“未验证”，不要直接用于正式科研结论。

## OpenVideo 本地分析产物

OpenVideo 工作树：

`/Users/jacklee/develop/openvideo/.worktrees/phase-1-foundation`

本次分析目录：

`/Users/jacklee/develop/openvideo/.worktrees/phase-1-foundation/.openvideo/user-analysis/douyin-research-skills`

视频报告：

- 胖胖的科研笔记：`.openvideo/user-analysis/douyin-research-skills/2026-06-28T12-04-25-103Z-16yecc1l53c/analysis/report.md`
- 小徐读博记：`.openvideo/user-analysis/douyin-research-skills/2026-06-28T12-08-33-295Z-ul5ji9odttq/analysis/report.md`

图文素材：

- 拉钩仙人：`.openvideo/user-analysis/douyin-research-skills/2026-06-28T12-07-42-855Z-m0rcanywefw/input/拉钩仙人/`
- AI大铁牛：`.openvideo/user-analysis/douyin-research-skills/2026-06-28T12-09-17-822Z-fnnl3lgkzki/input/AI大铁牛/`

## 工具记录

- `npm run doctor` 通过，`ffmpeg`、`ffprobe`、`yt-dlp`、`tesseract`、`chi_sim+eng` 均可用。
- 抖音短链需要 fresh cookies；通过 OpenVideo `auth douyin` 导出了登录态。
- `jiji` 下载器需要 Python 3.10+；本次使用 Homebrew Python 3.11 创建了本地 venv。
- 第二条和第四条是图文作品，不是视频，因此没有 ASR；主要依据图片 OCR 和原图视觉检查。
- 第一条和第三条是完整视频，均通过 `jiji` 下载，非 2.6 秒预览片段。
