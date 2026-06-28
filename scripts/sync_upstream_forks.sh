#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

entries=(
  "upstreams/scientific-agent-skills|JackLee992/scientific-agent-skills|K-Dense-AI/scientific-agent-skills|main"
  "upstreams/nature-skills|JackLee992/nature-skills|Yuan1z0825/nature-skills|main"
  "upstreams/academic-research-skills-codex|JackLee992/academic-research-skills-codex|Imbad0202/academic-research-skills-codex|main"
  "upstreams/PaperSpine|JackLee992/PaperSpine|WUBING2023/PaperSpine|main"
  "upstreams/image-to-editable-ppt-skill|JackLee992/image-to-editable-ppt-skill|ningzimu/image-to-editable-ppt-skill|main"
)

cd "$ROOT"
git submodule update --init --recursive --depth 1

for entry in "${entries[@]}"; do
  IFS="|" read -r path fork source branch <<< "$entry"
  echo "==> $fork"
  if command -v gh >/dev/null 2>&1; then
    gh repo sync "$fork" --source "$source" --branch "$branch" || {
      echo "Could not fast-forward sync $fork from $source. Resolve in the fork, then rerun." >&2
      exit 1
    }
  fi
  git -C "$path" fetch origin "$branch" --depth 1
  git -C "$path" checkout "$branch"
  git -C "$path" pull --ff-only origin "$branch"
done

echo
echo "Submodules are synced. If any submodule commit changed, review and commit the pointer in the parent repo."
