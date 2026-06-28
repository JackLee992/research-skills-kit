# Research Skills Kit

Practical Codex skills for everyday research work:

- `research-upstream-router`: route tasks into forked upstream submodule skills.
- `research-eda`: first-pass data quality and variable profiling.
- `research-statistics`: assumption-aware statistical tests and manuscript-ready result snippets.
- `research-power`: sample size, MDE, and power-curve planning.
- `research-figure`: publication figures with SVG/PDF/PNG/TIFF export and QA.
- `research-citation-check`: DOI/BibTeX metadata checks and reference reports.
- `research-results-audit`: statistical wording, causal language, and reproducibility hash audit.

The kit intentionally stays small. It is meant to be installed as a skill pack,
not as a general scientific Python framework.

## Install Into Codex

From a local checkout:

```bash
python3 "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo JackLee992/research-skills-kit \
  --path \
    skills/research-upstream-router \
    skills/research-eda \
    skills/research-statistics \
    skills/research-power \
    skills/research-figure \
    skills/research-citation-check \
    skills/research-results-audit
```

Open a new Codex conversation after installation so the skill cache refreshes.

## Full Upstream Mode

For the complete original upstream skill capabilities, use the forked submodules:

```bash
git clone --recurse-submodules https://github.com/JackLee992/research-skills-kit.git
cd research-skills-kit
python3 scripts/list_upstream_skills.py --profile core
```

Existing checkouts can initialize upstream forks with:

```bash
git submodule update --init --recursive --depth 1
```

See `docs/upstream_forks_and_submodules.md` for the fork map and routing model.

## Local Smoke Test

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python tests/smoke_test.py
```

The smoke test creates a synthetic experiment dataset, runs all local scripts,
and verifies that key Markdown/CSV/figure outputs exist.

## Repository Layout

```text
docs/
  README.md
  upstream_forks_and_submodules.md
  assessment/
  progress/
  raw/
  sources/
skills/
  research-upstream-router/
  research-eda/
  research-statistics/
  research-power/
  research-figure/
  research-citation-check/
  research-results-audit/
tests/
  smoke_test.py
```

Each skill is self-contained and exposes its main reusable script under
`skills/<skill>/scripts/`.

## Research Notes And Tracking

The original OpenVideo extraction, GitHub repo mapping, skill evaluation report,
fork/improvement candidates, implementation progress, and raw evaluation
artifacts are tracked under `docs/`.
