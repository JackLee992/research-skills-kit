#!/usr/bin/env python3
"""List or locate forked upstream skills for research-skills-kit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


DEFAULT_REPO_URL = "https://github.com/JackLee992/research-skills-kit.git"

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


def candidate_roots(explicit: str | None) -> list[Path]:
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit).expanduser())
    roots.append(Path.cwd())
    roots.extend(Path(__file__).resolve().parents)
    return roots


def find_checkout(explicit: str | None) -> Path | None:
    for root in candidate_roots(explicit):
        for candidate in [root, *root.parents]:
            if (candidate / ".gitmodules").is_file() and (candidate / "upstreams").exists():
                return candidate
    return None


def ensure_checkout(args: argparse.Namespace) -> Path:
    if args.clone_to:
        dest = Path(args.clone_to).expanduser()
        if dest.exists() and not (dest / ".gitmodules").is_file():
            if any(dest.iterdir()):
                raise SystemExit(f"--clone-to destination exists but is not empty: {dest}")
            should_clone = True
        else:
            should_clone = not dest.exists()
        if should_clone:
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--recurse-submodules",
                    "--shallow-submodules",
                    "--depth",
                    "1",
                    args.repo_url,
                    str(dest),
                ],
                check=True,
            )
        return dest

    checkout = find_checkout(args.checkout)
    if checkout is None:
        raise SystemExit(
            "Could not find a research-skills-kit checkout. Pass --checkout PATH "
            "or clone one with --clone-to PATH."
        )
    return checkout


def init_submodules(checkout: Path) -> None:
    subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive", "--depth", "1"],
        cwd=checkout,
        check=True,
    )


def collect_rows(checkout: Path, profile: str, query: str | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for upstream, rel_root in UPSTREAMS.items():
        base = checkout / rel_root
        if not base.exists():
            continue
        for skill_md in sorted(base.rglob("SKILL.md")):
            rel = skill_md.relative_to(checkout).as_posix()
            if profile == "core" and rel not in CORE_PATHS:
                continue
            name, description = parse_frontmatter(skill_md)
            row = {
                "upstream": upstream,
                "name": name,
                "path": rel,
                "description": description,
            }
            if query:
                haystack = " ".join(row.values()).lower()
                if query.lower() not in haystack:
                    continue
            rows.append(row)
    return rows


def print_table(rows: list[dict[str, str]]) -> None:
    print("| Upstream | Skill | Path | Description |")
    print("| --- | --- | --- | --- |")
    for row in rows:
        print(
            f"| `{row['upstream']}` | `{row['name']}` | "
            f"`{row['path']}` | {row['description']} |"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", help="Path to a research-skills-kit checkout")
    parser.add_argument("--clone-to", help="Clone the full kit here if no checkout exists")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--init-submodules", action="store_true")
    parser.add_argument("--profile", choices=["core", "all"], default="core")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    parser.add_argument("--query", help="Filter by skill name, path, upstream, or description")
    args = parser.parse_args()

    checkout = ensure_checkout(args)
    if args.init_submodules:
        init_submodules(checkout)
    rows = collect_rows(checkout, args.profile, args.query)
    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
