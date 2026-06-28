---
name: research-citation-check
description: Use when checking DOI, PMID, arXiv, BibTeX, Markdown references, citation metadata, duplicate bibliography entries, unresolved DOIs, or manuscript reference accuracy.
---

# Research Citation Check

Use this skill before submitting or sharing a manuscript draft.

## Workflow

Check DOIs:

```bash
python skills/research-citation-check/scripts/citation_check.py \
  --doi 10.1038/s41586-020-2649-2 --out-dir outputs/citations
```

Check a BibTeX file:

```bash
python skills/research-citation-check/scripts/citation_check.py \
  --bibtex references.bib --out-dir outputs/citations
```

Use `--offline` when network access is unavailable; unresolved online metadata must be marked as needing review.

## Outputs

| File | Purpose |
| --- | --- |
| `references.bib` | Normalized generated BibTeX when DOI metadata is available |
| `citation_report.md` | Human-readable verification report |
| `citation_report.json` | Structured verification data |

## Common Mistakes

- Do not invent metadata for unresolved citations.
- Do not treat web-search snippets as stronger than DOI/CrossRef/PubMed/arXiv metadata.
- Do not silently merge duplicate titles with different DOIs.

