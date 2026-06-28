---
name: research-upstream-router
description: Use when a research task should use forked upstream skill repositories, original upstream sub-skills, K-Dense, Nature skills, Academic Research Suite, PaperSpine, or Image to Editable PPT from this kit.
---

# Research Upstream Router

## Overview

This skill routes work to forked upstream skill repositories managed as submodules in `upstreams/`. It preserves original upstream capabilities while letting this kit add tested adapters and QA layers.

## Required Flow

1. Locate the `research-skills-kit` checkout. If submodules are missing, run `git submodule update --init --recursive --depth 1`.
2. Pick the upstream and child skill from the routing table below.
3. Read the child `SKILL.md` completely before acting.
4. Follow the child skill's relative references, scripts, and assets from inside that upstream repo.
5. Use local `research-*` skills only as validation/adapters unless the user explicitly asks for the lightweight rewritten flow.

## Routing Table

| Need | Upstream child skill path |
| --- | --- |
| Broad scientific domain skills, bioinformatics, chemistry, clinical, geospatial, statistics, visualization | `upstreams/scientific-agent-skills/skills/<child>/SKILL.md` |
| EDA, stats, power, scientific visualization, citation management | `upstreams/scientific-agent-skills/skills/exploratory-data-analysis`, `statistical-analysis`, `statistical-power`, `scientific-visualization`, `citation-management` |
| Nature-style figures, Nature writing, citation, reviewer, response, paper-to-PPT | `upstreams/nature-skills/skills/<child>/SKILL.md` |
| Deep academic research workflow, experiment validation, paper pipeline | `upstreams/academic-research-skills-codex/skills/academic-research-suite/SKILL.md` |
| PaperSpine paper intake, build, rewrite, citation, LaTeX, audit, translation | `upstreams/PaperSpine/dist/codex/skills/<child>/SKILL.md` or `upstreams/PaperSpine/dist/codex/paper-spine/SKILL.md` |
| Image or scanned figure to editable PowerPoint | `upstreams/image-to-editable-ppt-skill/skills/image-to-editable-ppt/SKILL.md` |

## Fork Policy

- Treat `upstreams/*` as the source of full upstream behavior.
- Make upstream-specific improvements in the forked submodule repo, not by copying large upstream directories into this kit.
- After changing a fork, commit and push inside that submodule, then commit the updated submodule pointer in this kit.
- Keep license limits visible. In particular, Academic Research Skills Codex is marked as non-standard / non-commercial in the tracking docs, so reuse implementation ideas carefully.

## Local Enhancement Layer

The local skills in this kit (`research-eda`, `research-statistics`, `research-power`, `research-figure`, `research-citation-check`, `research-results-audit`) are tested adapters for common workflows. For full original behavior, load the upstream child skill first, then use the local adapter to run reproducible checks or generate normalized reports.
