from __future__ import annotations

import json
import re
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


REFERENCES_DIR = Path("references")
REPORTS_DIR = Path("reports")
RESEARCH_DIR = Path("research_documents")
REFERENCES_PATH = REFERENCES_DIR / "references.json"
FINDINGS_REPORT_PATH = REPORTS_DIR / "cloud_research_findings_report.txt"
CLOUD_SUMMARY_PATH = RESEARCH_DIR / "cloud_references_summary.md"


QUERY_SETS = {
    "trinity": [
        "Trinity Father Son Holy Spirit practical theology",
        "Nicene Creed Trinity Father Son Holy Spirit",
        "Trinitarian theology creation redemption sanctification",
    ],
    "unresolved_suffering": [
        "theodicy unresolved suffering lament pastoral care",
        "lament grief trauma pastoral theology",
        "unanswered prayer suffering practical theology",
    ],
    "quantum_science_guardrails": [
        "quantum mechanics measurement uncertainty philosophy of science",
        "quantum physics theology overclaim",
        "physics probability uncertainty philosophy science",
    ],
    "music_math": [
        "music theory interval ratios consonance tension resolution",
        "mathematics of music harmony ratios",
        "acoustics consonance dissonance music perception",
    ],
    "politics_justice": [
        "political theology justice mercy public life",
        "religion public ethics justice poverty oppression",
    ],
    "art_beauty": [
        "theology art beauty symbol meaning",
        "aesthetics theology beauty imagination",
    ],
    "technology_ethics": [
        "AI ethics human dignity theology technology",
        "technology ethics human dignity community",
    ],
    "theologians_cross_era": [
        "Athanasius Trinity Augustine Trinity Aquinas grace Luther theology Calvin church Barth revelation Bonhoeffer discipleship Moltmann hope",
        "patristic medieval reformation modern contemporary theologians Trinity creation Christology pneumatology",
        "Irenaeus Athanasius Augustine Aquinas Luther Calvin Barth Bonhoeffer Moltmann theology",
    ],
}


def read_json(path: Path, default):
    if not path.exists():
        return default

    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def fetch_json(url: str, timeout: int = 30):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, timeout: int = 30):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_text(value: str, limit: int = 700):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def source_id(source: dict):
    raw = source.get("doi") or source.get("url") or source.get("title", "")
    return re.sub(r"\s+", " ", raw.strip().lower())


def add_source(sources_by_id: dict, source: dict):
    key = source_id(source)
    if not key:
        return False

    if key in sources_by_id:
        existing = sources_by_id[key]
        existing_tags = set(existing.get("tags", []))
        existing_tags.update(source.get("tags", []))
        existing["tags"] = sorted(existing_tags)
        return False

    source["id"] = key
    sources_by_id[key] = source
    return True


def source_quality(source: dict):
    provider = source.get("provider", "")
    source_type = source.get("source_type", "")
    title = source.get("title", "").lower()
    summary = source.get("summary", "").lower()
    text = f"{title} {summary}"

    if "arxiv" in provider.lower():
        return "scholarly preprint"
    if "crossref" in provider.lower() or "openalex" in provider.lower():
        return "scholarly metadata"
    if source_type == "counterargument":
        return "counterargument"
    if any(term in text for term in ["maybe", "proof of god", "quantum proves"]):
        return "speculative-risk"
    return "reference metadata"


def search_crossref(query: str, tag: str, limit: int = 5):
    url = (
        "https://api.crossref.org/works?"
        + urllib.parse.urlencode({"query": query, "rows": str(limit), "select": "DOI,title,author,published-print,published-online,URL,abstract,type"})
    )
    payload = fetch_json(url)
    results = []

    for item in payload.get("message", {}).get("items", []):
        title = " ".join(item.get("title") or []).strip()
        if not title:
            continue

        published = item.get("published-print") or item.get("published-online") or {}
        date_parts = published.get("date-parts") or []
        year = date_parts[0][0] if date_parts and date_parts[0] else None
        authors = item.get("author") or []
        author_names = []
        for author in authors[:3]:
            name = " ".join(part for part in [author.get("given"), author.get("family")] if part)
            if name:
                author_names.append(name)

        results.append(
            {
                "title": clean_text(title, 250),
                "authors": author_names,
                "year": year,
                "url": item.get("URL", ""),
                "doi": item.get("DOI", ""),
                "provider": "Crossref",
                "source_type": item.get("type", "scholarly metadata"),
                "tags": [tag],
                "summary": clean_text(item.get("abstract", "")),
                "copyright_note": "Metadata and short abstract summary only; do not store full copyrighted text.",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def search_openalex(query: str, tag: str, limit: int = 5):
    url = (
        "https://api.openalex.org/works?"
        + urllib.parse.urlencode({"search": query, "per-page": str(limit)})
    )
    payload = fetch_json(url)
    results = []

    for item in payload.get("results", []):
        title = item.get("display_name", "")
        if not title:
            continue

        authorships = item.get("authorships") or []
        author_names = [
            authorship.get("author", {}).get("display_name", "")
            for authorship in authorships[:3]
            if authorship.get("author", {}).get("display_name")
        ]
        url = item.get("primary_location", {}).get("landing_page_url") or item.get("doi") or item.get("id", "")

        results.append(
            {
                "title": clean_text(title, 250),
                "authors": author_names,
                "year": item.get("publication_year"),
                "url": url,
                "doi": item.get("doi", ""),
                "provider": "OpenAlex",
                "source_type": item.get("type", "scholarly metadata"),
                "tags": [tag],
                "summary": clean_text(item.get("abstract_inverted_index") and "OpenAlex abstract metadata available."),
                "copyright_note": "Metadata only; do not store full copyrighted text.",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def search_arxiv(query: str, tag: str, limit: int = 5):
    url = (
        "https://export.arxiv.org/api/query?"
        + urllib.parse.urlencode({"search_query": f"all:{query}", "start": "0", "max_results": str(limit)})
    )
    text = fetch_text(url)
    root = ET.fromstring(text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []

    for entry in root.findall("atom:entry", ns):
        title = clean_text(entry.findtext("atom:title", default="", namespaces=ns), 250)
        if not title:
            continue

        authors = [
            clean_text(author.findtext("atom:name", default="", namespaces=ns), 120)
            for author in entry.findall("atom:author", ns)[:3]
        ]
        authors = [author for author in authors if author]
        published = entry.findtext("atom:published", default="", namespaces=ns)

        results.append(
            {
                "title": title,
                "authors": authors,
                "year": published[:4] if published else None,
                "url": entry.findtext("atom:id", default="", namespaces=ns),
                "doi": "",
                "provider": "arXiv",
                "source_type": "scholarly preprint",
                "tags": [tag],
                "summary": clean_text(entry.findtext("atom:summary", default="", namespaces=ns)),
                "copyright_note": "Open preprint metadata and short summary only.",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def collect_sources():
    existing = read_json(REFERENCES_PATH, {"sources": []})
    sources_by_id = {source_id(source): source for source in existing.get("sources", []) if source_id(source)}
    new_count = 0
    errors = []

    for tag, queries in QUERY_SETS.items():
        for query in queries:
            collectors = [search_crossref, search_openalex]
            if "quantum" in tag or "science" in tag or "music_math" in tag:
                collectors.append(search_arxiv)

            for collector in collectors:
                try:
                    for source in collector(query, tag):
                        source["quality"] = source_quality(source)
                        if add_source(sources_by_id, source):
                            new_count += 1
                except Exception as exc:
                    errors.append(f"{collector.__name__} failed for {tag}: {exc}")

    sources = sorted(sources_by_id.values(), key=lambda item: (item.get("tags", []), item.get("title", "")))
    save_json(
        REFERENCES_PATH,
        {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source_count": len(sources),
            "sources": sources,
        },
    )
    write_reports(sources, new_count, errors)


def write_reports(sources: list[dict], new_count: int, errors: list[str]):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    tag_counts = {}
    quality_counts = {}
    for source in sources:
        for tag in source.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        quality = source.get("quality", "unknown")
        quality_counts[quality] = quality_counts.get(quality, 0) + 1

    lines = [
        "Cloud Research Findings Report",
        "==============================",
        "",
        f"Updated: {datetime.now(timezone.utc).isoformat()}",
        f"Total references: {len(sources):,}",
        f"New references this run: {new_count:,}",
        "",
        "Guardrails",
        "----------",
        "- Store metadata, source links, summaries, and short allowed snippets only.",
        "- Do not copy full copyrighted articles, books, or song lyrics.",
        "- Treat search results as candidate references until reviewed.",
        "- Keep quantum/science claims tied to qualified sources and stated limits.",
        "",
        "Reference Tags",
        "--------------",
    ]
    lines.extend(f"- {tag}: {count:,}" for tag, count in sorted(tag_counts.items()))
    lines.extend(["", "Quality Counts", "--------------"])
    lines.extend(f"- {quality}: {count:,}" for quality, count in sorted(quality_counts.items()))

    lines.extend(["", "Recent Candidate Sources", "------------------------"])
    for source in sources[-30:]:
        tags = ", ".join(source.get("tags", []))
        authors = ", ".join(source.get("authors", []))
        lines.append(f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'})")
        lines.append(f"  Tags: {tags}")
        if authors:
            lines.append(f"  Authors: {authors}")
        lines.append(f"  Source: {source.get('provider')} | {source.get('quality')}")
        if source.get("url"):
            lines.append(f"  URL: {source['url']}")

    if errors:
        lines.extend(["", "Collector Errors", "----------------"])
        lines.extend(f"- {error}" for error in errors)

    FINDINGS_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    summary_lines = [
        "# Cloud References Summary",
        "",
        "This file is generated by internet_source_collector.py so the main analyzer can include reference metadata in pattern analysis.",
        "It stores summaries and citations only, not full copyrighted source text.",
        "",
    ]

    for source in sources[-80:]:
        summary = source.get("summary") or "No summary available in metadata."
        summary_lines.extend(
            [
                f"## {source.get('title', 'Untitled')}",
                "",
                f"- Tags: {', '.join(source.get('tags', []))}",
                f"- Provider: {source.get('provider')}",
                f"- Quality: {source.get('quality')}",
                f"- URL: {source.get('url')}",
                "",
                textwrap.fill(summary, width=100),
                "",
            ]
        )

    CLOUD_SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")


def main():
    collect_sources()
    print(f"References saved to: {REFERENCES_PATH}")
    print(f"Findings report saved to: {FINDINGS_REPORT_PATH}")
    print(f"Analyzer summary saved to: {CLOUD_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
