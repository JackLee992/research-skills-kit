# Upstream Forks And Submodules

更新时间：2026-06-28

本仓库采用 fork + submodule 的方式管理完整上游 skills 能力：

- 上游完整能力保留在 `upstreams/*`。
- `skills/research-upstream-router` 负责把任务路由到上游子 skills。
- 本仓库已有的 `research-*` skills 作为验证过的本地增强层，不替代完整上游。

## Fork 清单

| 原始上游 | JackLee992 fork | Submodule path | 默认分支 | Skill 数 | 许可备注 |
| --- | --- | --- | --- | --- | --- |
| `K-Dense-AI/scientific-agent-skills` | `JackLee992/scientific-agent-skills` | `upstreams/scientific-agent-skills` | `main` | 147 | MIT |
| `Yuan1z0825/nature-skills` | `JackLee992/nature-skills` | `upstreams/nature-skills` | `main` | 12 | Apache 2.0 |
| `Imbad0202/academic-research-skills-codex` | `JackLee992/academic-research-skills-codex` | `upstreams/academic-research-skills-codex` | `main` | 2 | 非标准 / 需注意非商业限制 |
| `WUBING2023/PaperSpine` | `JackLee992/PaperSpine` | `upstreams/PaperSpine` | `main` | 37 | MIT |
| `ningzimu/image-to-editable-ppt-skill` | `JackLee992/image-to-editable-ppt-skill` | `upstreams/image-to-editable-ppt-skill` | `main` | 1 | MIT |

## 获取完整能力

新 clone：

```bash
git clone --recurse-submodules https://github.com/JackLee992/research-skills-kit.git
cd research-skills-kit
```

已有 clone：

```bash
git submodule update --init --recursive --depth 1
```

查看核心上游子 skills：

```bash
python3 scripts/list_upstream_skills.py --profile core
```

查看全部上游子 skills：

```bash
python3 scripts/list_upstream_skills.py --profile all
```

## 调用方式

当任务需要完整原始能力时，使用 `research-upstream-router`：

1. 先定位 `upstreams/<repo>/<skill>/SKILL.md`。
2. 读取该子 skill 的 `SKILL.md`。
3. 按子 skill 内部说明继续读取相对路径的 `references/`、`scripts/`、`assets/`。
4. 需要执行或验证时，再调用本仓库的本地增强 skills 或脚本。

常用路线：

| 场景 | 首选上游子 skill |
| --- | --- |
| EDA | `upstreams/scientific-agent-skills/skills/exploratory-data-analysis/SKILL.md` |
| 统计分析 | `upstreams/scientific-agent-skills/skills/statistical-analysis/SKILL.md` |
| Power / 样本量 | `upstreams/scientific-agent-skills/skills/statistical-power/SKILL.md` |
| 科研可视化 | `upstreams/scientific-agent-skills/skills/scientific-visualization/SKILL.md` |
| Nature 风格作图 | `upstreams/nature-skills/skills/nature-figure/SKILL.md` |
| 引用管理 | `upstreams/scientific-agent-skills/skills/citation-management/SKILL.md` 或 `upstreams/nature-skills/skills/nature-citation/SKILL.md` |
| 学术研究全流程 | `upstreams/academic-research-skills-codex/skills/academic-research-suite/SKILL.md` |
| 论文结构 / 改写 / 审计 | `upstreams/PaperSpine/dist/codex/paper-spine/SKILL.md` |
| 图片转可编辑 PPT | `upstreams/image-to-editable-ppt-skill/skills/image-to-editable-ppt/SKILL.md` |

## 更新 Fork 和 Submodule 指针

同步 fork 与上游，并更新本地 submodule checkout：

```bash
scripts/sync_upstream_forks.sh
```

如果脚本报告某个 fork 无法 fast-forward，说明你在 fork 上有自己的改造分支或改动，需要先在对应 fork 中手动合并上游。

同步后如果 submodule commit 发生变化：

```bash
git status
git add upstreams/<repo>
git commit -m "Update upstream skill submodule pointers"
git push
```

## 改造原则

- 上游原能力：在 fork 仓库里增强，并保持可向上游回流 PR。
- 本仓库：只维护路由、验证、统一安装说明、轻量增强层和评估材料。
- 不把大上游仓库复制进主仓库，避免丢失 upstream history 和 license 边界。
- 对非商业或非标准许可来源，优先做 wrapper、适配和重写，不直接搬实现。
