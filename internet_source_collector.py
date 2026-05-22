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
DAILY_DIGEST_PATH = REFERENCES_DIR / "daily_research_digest.json"
FINDINGS_REPORT_PATH = REPORTS_DIR / "cloud_research_findings_report.txt"
CLOUD_SUMMARY_PATH = RESEARCH_DIR / "cloud_references_summary.md"
DAILY_EVALUATION_QUEUE_PATH = RESEARCH_DIR / "daily_evaluation_queue.md"


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
        "visual theology iconography symbol lament hope",
    ],
    "history_memory": [
        "historical theology memory trauma justice repair",
        "religion history collective memory suffering hope",
        "church history reform empire injustice theological interpretation",
    ],
    "world_languages_translation": [
        "translation semantics theology metaphor grammar culture",
        "comparative theology translation language semantics sacred texts",
        "world languages sacred texts translation meaning metaphor",
    ],
    "biblical_languages": [
        "biblical Hebrew Greek lemma syntax theology translation",
        "Septuagint Hebrew Bible Greek translation semantics theology",
        "logos pneuma ruach hesed agape shalom biblical theology",
    ],
    "psychology_patterns": [
        "psychology trauma attachment religion transformation hope",
        "moral psychology forgiveness repentance habit formation",
        "cognitive science religion ritual identity community transformation",
    ],
    "global_text_traditions": [
        "sacred texts wisdom literature lament justice transformation comparative religion",
        "world scriptures wisdom traditions suffering justice hope",
        "oral tradition myth epic proverb ritual moral order comparative theology",
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


TAG_LAYER_ROUTES = {
    "trinity": ["theologians", "research_documents", "pattern_tests"],
    "unresolved_suffering": ["pattern_tests", "deep_sources", "psychology_inputs", "human_stories"],
    "quantum_science_guardrails": ["deep_sources", "pattern_tests"],
    "music_math": ["music_notes", "deep_sources"],
    "politics_justice": ["cultural_inputs", "history_inputs", "pattern_tests"],
    "art_beauty": ["visual_art", "cultural_inputs"],
    "history_memory": ["history_inputs", "theologians", "pattern_tests"],
    "world_languages_translation": ["world_languages", "all_texts"],
    "biblical_languages": ["biblical_languages", "research_documents/christian_sources"],
    "psychology_patterns": ["psychology_inputs", "human_stories", "pattern_tests"],
    "global_text_traditions": ["all_texts", "other_religious_texts", "modern_literature"],
    "technology_ethics": ["cultural_inputs", "pattern_tests"],
    "theologians_cross_era": ["theologians", "research_documents/christian_sources"],
}


TEXT_LAYER_ROUTES = {
    "theologians": ["athanasius", "augustine", "aquinas", "luther", "calvin", "barth", "bonhoeffer", "moltmann", "theologian", "trinity"],
    "visual_art": ["art", "beauty", "aesthetic", "icon", "iconography", "visual"],
    "history_inputs": ["history", "historical", "memory", "empire", "reform", "chronicle"],
    "world_languages": ["translation", "language", "semantics", "metaphor", "grammar"],
    "biblical_languages": ["hebrew", "greek", "septuagint", "logos", "pneuma", "ruach", "hesed"],
    "all_texts": ["sacred text", "scripture", "wisdom", "myth", "epic", "ritual", "oral tradition"],
    "psychology_inputs": ["psychology", "trauma", "attachment", "habit", "cognitive", "identity"],
    "other_religious_texts": ["comparative religion", "quran", "hindu", "buddhist", "islam", "judaism"],
    "modern_literature": ["modern literature", "novel", "fiction", "poetry", "drama", "memoir"],
    "human_stories": ["case study", "testimony", "lived experience", "pastoral", "counseling"],
    "deep_sources": ["quantum", "physics", "science", "peer review", "counterargument"],
    "pattern_tests": ["suffering", "injustice", "overclaim", "unanswered", "abuse", "counterargument"],
}


LAYER_REVIEW_PROMPTS = {
    "theologians": "Check named theologian, era, primary source, doctrine, disagreement, and pressure point.",
    "visual_art": "Review actual image/form, composition, symbol, context, beauty, lament, and counter-reading.",
    "history_inputs": "Check era, power, conflict, memory, harmed communities, reform, and unintended consequences.",
    "world_languages": "Track original language, translation range, metaphor, grammar, culture, and rival reading.",
    "biblical_languages": "Check lemma, syntax, canonical context, translation history, and scholarly counter-reading.",
    "all_texts": "Classify text tradition, genre, community context, and whether recurrence is broad or overfit.",
    "psychology_inputs": "Separate psychological/social process from theological interpretation and note clinical limits.",
    "other_religious_texts": "Read the tradition on its own terms; do not flatten it into Christian categories.",
    "modern_literature": "Use summaries or public-domain material only; preserve ambiguity and rival interpretations.",
    "human_stories": "Protect privacy; look for truth, care, justice, repair, and unresolved suffering.",
    "deep_sources": "Verify qualified sources and counterarguments before strengthening science or suffering claims.",
    "pattern_tests": "Name the failure condition and whether the pattern holds, breaks, or needs revision.",
    "cultural_inputs": "Classify the cultural domain and practical consequences before making theological claims.",
    "music_notes": "Check musical structure directly before using it as analogy or theological support.",
    "research_documents": "Use as general research context until a more specific layer is reviewed.",
    "research_documents/christian_sources": "Check Christian source context, doctrine, and source quality.",
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
        add_layer_routing(existing)
        return False

    source["id"] = key
    add_layer_routing(source)
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


def route_layers_for_source(source: dict):
    routes = []

    for tag in source.get("tags", []):
        routes.extend(TAG_LAYER_ROUTES.get(tag, []))

    text = " ".join(
        [
            source.get("title", ""),
            source.get("summary", ""),
            " ".join(source.get("tags", [])),
        ]
    ).lower()

    for layer, terms in TEXT_LAYER_ROUTES.items():
        if any(term in text for term in terms):
            routes.append(layer)

    deduped = []
    for route in routes:
        if route not in deduped:
            deduped.append(route)

    return deduped or ["research_documents"]


def add_layer_routing(source: dict):
    routes = route_layers_for_source(source)
    source["layer_routes"] = routes
    source["primary_layer"] = routes[0]
    source["layer_review_prompts"] = [
        LAYER_REVIEW_PROMPTS.get(
            route,
            "Review source quality, scope, context, and counterarguments.",
        )
        for route in routes[:5]
    ]
    return source


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
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
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
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
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
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def collect_sources():
    existing = read_json(REFERENCES_PATH, {"sources": []})
    sources_by_id = {source_id(source): source for source in existing.get("sources", []) if source_id(source)}
    for source in sources_by_id.values():
        add_layer_routing(source)
    new_count = 0
    new_sources = []
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
                            new_sources.append(source)
                except Exception as exc:
                    errors.append(f"{collector.__name__} failed for {tag}: {exc}")

    for source in sources_by_id.values():
        add_layer_routing(source)

    sources = sorted(sources_by_id.values(), key=lambda item: (item.get("tags", []), item.get("title", "")))
    layer_counts = {}
    new_layer_counts = {}
    for source in sources:
        for layer in source.get("layer_routes", []):
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
    for source in new_sources:
        for layer in source.get("layer_routes", []):
            new_layer_counts[layer] = new_layer_counts.get(layer, 0) + 1
    run_at = datetime.now(timezone.utc).isoformat()
    save_json(
        REFERENCES_PATH,
        {
            "updated_at": run_at,
            "source_count": len(sources),
            "sources": sources,
        },
    )
    save_json(
        DAILY_DIGEST_PATH,
        {
            "updated_at": run_at,
            "new_count": new_count,
            "new_sources": new_sources,
            "layer_counts": layer_counts,
            "new_layer_counts": new_layer_counts,
            "errors": errors,
        },
    )
    write_reports(sources, new_count, new_sources, errors)


def write_reports(sources: list[dict], new_count: int, new_sources: list[dict], errors: list[str]):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    tag_counts = {}
    quality_counts = {}
    layer_counts = {}
    for source in sources:
        for tag in source.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        for layer in source.get("layer_routes", []):
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
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
    lines.extend(["", "Layer Routes", "------------"])
    lines.extend(f"- {layer}: {count:,}" for layer, count in sorted(layer_counts.items()))
    lines.extend(["", "Quality Counts", "--------------"])
    lines.extend(f"- {quality}: {count:,}" for quality, count in sorted(quality_counts.items()))

    new_tag_counts = {}
    new_layer_counts = {}
    for source in new_sources:
        for tag in source.get("tags", []):
            new_tag_counts[tag] = new_tag_counts.get(tag, 0) + 1
        for layer in source.get("layer_routes", []):
            new_layer_counts[layer] = new_layer_counts.get(layer, 0) + 1

    lines.extend(["", "New This Run By Tag", "-------------------"])
    if new_tag_counts:
        lines.extend(f"- {tag}: {count:,}" for tag, count in sorted(new_tag_counts.items()))
    else:
        lines.append("- No brand-new references found this run; reports still re-evaluate the current candidate set.")

    lines.extend(["", "New This Run By Layer Route", "---------------------------"])
    if new_layer_counts:
        lines.extend(f"- {layer}: {count:,}" for layer, count in sorted(new_layer_counts.items()))
    else:
        lines.append("- No brand-new layer routes this run.")

    lines.extend(["", "Newest Additions This Run", "------------------------"])
    if new_sources:
        for source in new_sources[:30]:
            tags = ", ".join(source.get("tags", []))
            routes = ", ".join(source.get("layer_routes", []))
            lines.append(f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'})")
            lines.append(f"  Tags: {tags}")
            lines.append(f"  Layer routes: {routes}")
            lines.append(f"  Source: {source.get('provider')} | {source.get('quality')}")
            if source.get("url"):
                lines.append(f"  URL: {source['url']}")
    else:
        lines.append("- No new additions this run.")

    lines.extend(["", "Recent Candidate Sources", "------------------------"])
    for source in sources[-30:]:
        tags = ", ".join(source.get("tags", []))
        routes = ", ".join(source.get("layer_routes", []))
        authors = ", ".join(source.get("authors", []))
        lines.append(f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'})")
        lines.append(f"  Tags: {tags}")
        lines.append(f"  Layer routes: {routes}")
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
                f"- Layer routes: {', '.join(source.get('layer_routes', []))}",
                f"- Primary layer: {source.get('primary_layer', 'research_documents')}",
                f"- Provider: {source.get('provider')}",
                f"- Quality: {source.get('quality')}",
                f"- URL: {source.get('url')}",
                "",
                textwrap.fill(summary, width=100),
                "",
            ]
        )

    CLOUD_SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")

    queue_lines = [
        "# Daily Evaluation Queue",
        "",
        "This file is generated by internet_source_collector.py every time the daily cloud research workflow runs.",
        "It is an evaluation set of candidate material, not a set of approved conclusions.",
        "",
        "Review rule: unreviewed daily candidates can shape research questions, but they should not increase confidence in a divine pattern until the original source, author expertise, source type, publication context, and counterarguments are checked.",
        "",
        "## Newest Candidate Material",
        "",
    ]

    queued_sources = new_sources or sorted(
        sources,
        key=lambda source: (source.get("date_accessed", ""), source.get("title", "")),
        reverse=True,
    )[:120]

    for source in queued_sources[:120]:
        summary = source.get("summary") or "No summary available in metadata."
        queue_lines.extend(
            [
                f"### {source.get('title', 'Untitled')}",
                "",
                f"- Review status: {source.get('review_status', 'unreviewed_daily_candidate')}",
                f"- Evaluation use: {source.get('evaluation_use', 'candidate lead only')}",
                f"- Tags: {', '.join(source.get('tags', []))}",
                f"- Layer routes: {', '.join(source.get('layer_routes', []))}",
                f"- Primary layer: {source.get('primary_layer', 'research_documents')}",
                f"- Provider: {source.get('provider')}",
                f"- Quality: {source.get('quality')}",
                f"- Year: {source.get('year') or 'n.d.'}",
                f"- URL: {source.get('url')}",
                "",
                textwrap.fill(summary, width=100),
                "",
                "Layer review prompts:",
            ]
        )
        for prompt in source.get("layer_review_prompts", [])[:5]:
            queue_lines.append(f"- {prompt}")
        queue_lines.append("")

    DAILY_EVALUATION_QUEUE_PATH.write_text("\n".join(queue_lines), encoding="utf-8")


def main():
    collect_sources()
    print(f"References saved to: {REFERENCES_PATH}")
    print(f"Findings report saved to: {FINDINGS_REPORT_PATH}")
    print(f"Analyzer summary saved to: {CLOUD_SUMMARY_PATH}")
    print(f"Daily evaluation queue saved to: {DAILY_EVALUATION_QUEUE_PATH}")


if __name__ == "__main__":
    main()
