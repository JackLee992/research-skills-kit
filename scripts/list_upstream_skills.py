#!/usr/bin/env python3
"""List forked upstream skills managed by this kit."""

from __future__ import annotations

import argparse
from pathlib import Path


UPSTREAMS = {
    "scientific-agent-skills": Path("upstreams/scientific-agent-skills"),
    "nature-skills": Path("upstreams/nature-skills"),
    "academic-research-skills-codex": Path("upstreams/academic-research-skills-codex"),
    "PaperSpine": Path("upstreams/PaperSpine"),
    "image-to-editable-ppt-skill": Path("upstreams/image-to-editable-ppt-skill"),
}

CORE_PATHS = {
    "upstreams/scientific-agent-skills/skills/exploratory-data-analysis/SKILL.md",
    "upstreams/scientific-agent-skills/skills/statistical-analysis/SKILL.md",
    "upstreams/scientific-agent-skills/skills/statistical-power/SKILL.md",
    "upstreams/scientific-agent-skills/skills/scientific-visualization/SKILL.md",
    "upstreams/scientific-agent-skills/skills/citation-management/SKILL.md",
    "upstreams/nature-skills/skills/nature-figure/SKILL.md",
    "upstreams/nature-skills/skills/nature-citation/SKILL.md",
    "upstreams/nature-skills/skills/nature-writing/SKILL.md",
    "upstreams/academic-research-skills-codex/skills/academic-research-suite/SKILL.md",
    "upstreams/PaperSpine/dist/codex/paper-spine/SKILL.md",
    "upstreams/PaperSpine/dist/codex/skills/paper-spine-audit/SKILL.md",
    "upstreams/PaperSpine/dist/codex/skills/paper-spine-rewrite/SKILL.md",
    "upstreams/PaperSpine/dist/codex/skills/paper-spine-citation/SKILL.md",
    "upstreams/image-to-editable-ppt-skill/skills/image-to-editable-ppt/SKILL.md",
}


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return path.parent.name, ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return path.parent.name, ""
    name = path.parent.name
    description = ""
    lines = parts[1].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip("\"'")
            if description in {">", ">-", "|", "|-"}:
                block: list[str] = []
                i += 1
                while i < len(lines):
                    child = lines[i]
                    if child and not child.startswith((" ", "\t")) and ":" in child:
                        i -= 1
                        break
                    block.append(child.strip())
                    i += 1
                description = " ".join(part for part in block if part)
        i += 1
    return name, description


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["core", "all"], default="core")
    args = parser.parse_args()

    root = Path.cwd()
    rows: list[tuple[str, str, str, str]] = []
    for upstream, rel_root in UPSTREAMS.items():
        base = root / rel_root
        if not base.exists():
            continue
        for skill_md in sorted(base.rglob("SKILL.md")):
            rel = skill_md.relative_to(root).as_posix()
            if args.profile == "core" and rel not in CORE_PATHS:
                continue
            name, description = parse_frontmatter(skill_md)
            rows.append((upstream, name, rel, description))

    print("| Upstream | Skill | Path | Description |")
    print("| --- | --- | --- | --- |")
    for upstream, name, rel, description in rows:
        print(f"| `{upstream}` | `{name}` | `{rel}` | {description} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
