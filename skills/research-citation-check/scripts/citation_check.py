#!/usr/bin/env python3
"""DOI and BibTeX citation checks with CrossRef metadata fallback."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import requests


DOI_RE = re.compile(r"10\.\d{4,9}/[^\s,}\]\)\"']+")


def bibtex_escape(value: str) -> str:
    return value.replace("{", "").replace("}", "").strip()


def crossref_metadata(doi: str, timeout: int = 15) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "research-skills-kit/0.1"})
    response.raise_for_status()
    msg = response.json()["message"]
    authors = []
    for author in msg.get("author", []):
        family = author.get("family", "")
        given = author.get("given", "")
        if family:
            authors.append(f"{family}, {given}".strip().strip(","))
    year = ""
    for key in ("published-print", "published-online", "issued"):
        parts = msg.get(key, {}).get("date-parts", [[]])
        if parts and parts[0]:
            year = str(parts[0][0])
            break
    return {
        "doi": doi,
        "title": (msg.get("title") or [""])[0],
        "author": " and ".join(authors),
        "journal": (msg.get("container-title") or [""])[0],
        "year": year,
        "volume": msg.get("volume", ""),
        "number": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "url": msg.get("URL", f"https://doi.org/{doi}"),
    }


def to_bibtex(meta: dict) -> str:
    first = re.sub(r"\W+", "", (meta.get("author", "unknown").split(" and ")[0].split(",")[0] or "unknown"))
    key = f"{first}_{meta.get('year', 'nd')}"
    fields = [
        ("title", meta.get("title")),
        ("author", meta.get("author")),
        ("journal", meta.get("journal")),
        ("year", meta.get("year")),
        ("volume", meta.get("volume")),
        ("number", meta.get("number")),
        ("pages", meta.get("pages")),
        ("doi", meta.get("doi")),
        ("url", meta.get("url")),
    ]
    body = "\n".join(f"  {k} = {{{bibtex_escape(str(v))}}}," for k, v in fields if v)
    return f"@article{{{key},\n{body}\n}}\n"


def extract_bibtex_dois(path: Path) -> list[str]:
    return sorted(set(DOI_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))))


def main() -> None:
    parser = argparse.ArgumentParser(description="Check citation identifiers and BibTeX metadata.")
    parser.add_argument("--doi", action="append", default=[])
    parser.add_argument("--bibtex", type=Path)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/citations"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dois = list(args.doi)
    if args.bibtex:
        dois.extend(extract_bibtex_dois(args.bibtex))
    dois = sorted(set(d.strip().rstrip(".") for d in dois if d.strip()))

    records = []
    bib_entries = []
    for doi in dois:
        record = {"doi": doi, "status": "NEEDS_MANUAL_REVIEW"}
        if args.offline:
            record["status"] = "OFFLINE_NOT_VERIFIED"
        else:
            try:
                meta = crossref_metadata(doi)
                record.update(meta)
                record["status"] = "VERIFIED"
                bib_entries.append(to_bibtex(meta))
            except Exception as exc:
                record["error"] = str(exc)
                record["status"] = "DOI_UNRESOLVED"
        records.append(record)

    if bib_entries:
        (args.out_dir / "references.bib").write_text("\n".join(bib_entries), encoding="utf-8")
    (args.out_dir / "citation_report.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    lines = ["# Citation Report", "", f"Total DOI records: `{len(records)}`", ""]
    lines += ["| DOI | Status | Title |", "| --- | --- | --- |"]
    for record in records:
        lines.append(f"| `{record['doi']}` | `{record['status']}` | {record.get('title', '')} |")
    (args.out_dir / "citation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.out_dir / "citation_report.md")


if __name__ == "__main__":
    main()

