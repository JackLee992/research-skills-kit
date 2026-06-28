# Research Skills Kit

Practical Codex skills for everyday research work:

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
    skills/research-eda \
    skills/research-statistics \
    skills/research-power \
    skills/research-figure \
    skills/research-citation-check \
    skills/research-results-audit
```

Open a new Codex conversation after installation so the skill cache refreshes.

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
skills/
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
