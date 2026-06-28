# Research Skills Kit Tracking Docs

本目录保存这次科研 skills 调研、实测、改造决策和原始评测材料，方便后续继续 fork、重写、补测试和追踪进度。

## 文档地图

| 文档 | 用途 |
| --- | --- |
| `sources/openvideo_douyin_research_skills_analysis.md` | 4 条抖音视频 / 图文的 OpenVideo 信息提炼，包括 ASR、OCR、关键帧观察结论。 |
| `sources/openvideo_douyin_skills_github_repos.md` | 视频中涉及 skills / 工具的 GitHub 仓库清单和确认度分级。 |
| `assessment/research_skill_evaluation_report.md` | 用 Palmer Penguins 数据对候选科研 skills 做的实测评估报告。 |
| `assessment/skill_fork_improvement_candidates.md` | 值得 fork、抽取或重写的候选清单与改造建议。 |
| `progress/research_skills_implementation_progress.md` | 当前 `research-skills-kit` 的改造进度、已落地技能、后续 backlog。 |
| `raw/evaluation/README.md` | 实测输入、脚本和输出产物索引。 |
| `raw/openvideo/source_manifest.md` | 抖音原始链接、OpenVideo 本地证据路径和素材处理说明。 |

## 当前落地状态

当前仓库已经落地第一阶段高可用闭环：

1. `research-eda`
2. `research-statistics`
3. `research-power`
4. `research-figure`
5. `research-citation-check`
6. `research-results-audit`

这 6 个 skills 对应的数据分析闭环是：

```text
数据体检 -> 统计检验/回归 -> 样本量/功效 -> 论文图导出/QA -> 引用核验 -> 结果审计
```

## 维护原则

- 上游仓库作为 inspiration / compatibility reference，不直接整仓复制。
- MIT / Apache 来源可以按 license 兼容策略复用小片段；CC BY-NC 来源只借鉴思想，公开仓库内重写实现。
- 每个新增 skill 必须有 `SKILL.md`、可运行脚本或明确操作流程、至少一个 smoke test。
- 对正式科研结论，不把未核验的 skill 输出当成最终事实；统计、图、引用都要留下可复现证据。
