from __future__ import annotations

import json
import os
import re
import time
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from socket import timeout as SocketTimeoutError
from urllib.error import HTTPError


REFERENCES_DIR = Path("references")
REPORTS_DIR = Path("reports")
RESEARCH_DIR = Path("research_documents")
REFERENCES_PATH = REFERENCES_DIR / "references.json"
DAILY_DIGEST_PATH = REFERENCES_DIR / "daily_research_digest.json"
SEARCH_STRATEGY_PATH = REFERENCES_DIR / "next_search_strategy.json"
TAVILY_USAGE_PATH = REFERENCES_DIR / "tavily_usage.json"
FINDINGS_REPORT_PATH = REPORTS_DIR / "cloud_research_findings_report.txt"
CLOUD_SUMMARY_PATH = RESEARCH_DIR / "cloud_references_summary.md"
DAILY_EVALUATION_QUEUE_PATH = RESEARCH_DIR / "daily_evaluation_queue.md"

BING_WEB_SEARCH_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BRAVE_WEB_SEARCH_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
TAVILY_SEARCH_ENDPOINT = "https://api.tavily.com/search"
DEFAULT_SEARXNG_BASE_URL = ""
EUROPE_PMC_SEARCH_ENDPOINT = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
PUBMED_ESEARCH_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
INTERNET_ARCHIVE_ADVANCED_SEARCH_ENDPOINT = "https://archive.org/advancedsearch.php"
OPENCITATIONS_INDEX_ENDPOINT = "https://api.opencitations.net/index/v2"
OPEN_WEB_PROVIDERS = {"Bing Web Search", "Brave Search", "SearXNG", "Tavily Search"}
SCHOLARLY_METADATA_PROVIDERS = {
    "Crossref",
    "OpenAlex",
    "Europe PMC",
    "PubMed",
}

TRUSTED_OPEN_WEB_DOMAINS = [
    ".edu",
    ".gov",
    ".ac.uk",
    "archive.org",
    "loc.gov",
    "bl.uk",
    "worldcat.org",
    "jstor.org",
    "plato.stanford.edu",
    "iep.utm.edu",
    "metmuseum.org",
    "getty.edu",
    "britishmuseum.org",
    "louvre.fr",
    "vatican.va",
    "newadvent.org",
    "ccel.org",
    "sacred-texts.com",
    "gutenberg.org",
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "soundcloud.com",
    "spotify.com",
    "podcasts.apple.com",
]

MEDIA_SOURCE_MARKERS = {
    "video": [
        "video",
        "youtube.com",
        "youtu.be",
        "vimeo.com",
        "lecture recording",
        "documentary",
        "interview video",
    ],
    "podcast": [
        "podcast",
        "audio",
        "episode",
        "spotify.com",
        "podcasts.apple.com",
        "soundcloud.com",
        "sermon audio",
    ],
    "image": [
        "image",
        "photo",
        "photograph",
        "painting",
        "icon",
        "iconography",
        "gallery",
        "museum object",
        "visual archive",
    ],
}


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
    "visual_media_patterns": [
        "religious art images iconography visual theology image archive",
        "museum collection sacred art icon lament beauty theology",
        "photography documentary faith suffering justice visual testimony",
    ],
    "podcast_testimony_patterns": [
        "podcast faith testimony grief repair transformation episode",
        "Christian podcast suffering justice forgiveness testimony interview",
        "religion podcast conversion spiritual experience discernment transcript",
    ],
    "video_teaching_patterns": [
        "video lecture theology suffering justice practical theology",
        "documentary faith grief justice repair Christian theology video",
        "sermon video spiritual formation Holy Spirit discernment transcript",
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
    "world_language_source_sampling": [
        "world Christianity translation local language theology source study",
        "indigenous language Christian theology translation oral tradition source",
        "African Asian Latin American Christian language translation theology",
    ],
    "biblical_languages": [
        "biblical Hebrew Greek lemma syntax theology translation",
        "Septuagint Hebrew Bible Greek translation semantics theology",
        "logos pneuma ruach hesed agape shalom biblical theology",
    ],
    "biblical_language_source_depth": [
        "biblical Hebrew ruach hesed shalom source context scholarly article",
        "New Testament Greek pneuma logos agape source context scholarly article",
        "Septuagint translation Hebrew Greek theological terms source study",
    ],
    "psychology_patterns": [
        "psychology trauma attachment religion transformation hope",
        "moral psychology forgiveness repentance habit formation",
        "cognitive science religion ritual identity community transformation",
    ],
    "pattern_perception_divine_response": [
        "psychology pattern perception religious meaning divine agency",
        "cognitive science religion pattern recognition agency detection",
        "apophenia meaning making religious experience psychology divine patterns",
    ],
    "global_text_traditions": [
        "sacred texts wisdom literature lament justice transformation comparative religion",
        "world scriptures wisdom traditions suffering justice hope",
        "oral tradition myth epic proverb ritual moral order comparative theology",
    ],
    "modern_literature_meaning": [
        "modern literature theology suffering grace conversion narrative scholarly",
        "novel drama poetry religious meaning suffering justice hope literary criticism",
        "modern memoir spiritual transformation religious experience literary study",
    ],
    "cultural_practice_patterns": [
        "ritual cultural practice justice mercy community transformation anthropology",
        "public culture religion ethics community repair source study",
        "religion culture practice formation justice cross cultural anthropology",
    ],
    "general_research_methods": [
        "interdisciplinary theology research method evidence counterargument source review",
        "comparative theology methodology source review counterargument",
        "religion science humanities interdisciplinary research method evidence",
    ],
    "interreligious_dream_testimony": [
        "interreligious dreams visions Jesus conversion testimony scholarly study",
        "religious conversion dreams visions Jesus testimonies comparative religion research",
        "dreams visions conversion testimony Christianity anthropology religion",
    ],
    "holy_spirit_gifts_global": [
        "gifts of the Holy Spirit global Christianity Pentecostal charismatic anthropology",
        "spiritual gifts healing prophecy tongues discernment cross cultural Christianity",
        "charismatic gifts world Christianity interreligious discernment spiritual experiences",
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
    "trinity": ["theologians", "research_documents"],
    "unresolved_suffering": ["pattern_tests", "deep_sources", "psychology_inputs", "human_stories"],
    "quantum_science_guardrails": ["deep_sources", "pattern_tests"],
    "music_math": ["music_notes", "deep_sources"],
    "politics_justice": ["cultural_inputs", "history_inputs"],
    "art_beauty": ["visual_art", "cultural_inputs"],
    "visual_media_patterns": ["visual_art", "human_stories", "cultural_inputs", "pattern_tests"],
    "podcast_testimony_patterns": ["human_stories", "psychology_inputs", "theologians", "pattern_tests"],
    "video_teaching_patterns": ["theologians", "human_stories", "cultural_inputs", "pattern_tests"],
    "history_memory": ["history_inputs", "theologians"],
    "world_languages_translation": ["world_languages", "all_texts"],
    "world_language_source_sampling": ["world_languages", "all_texts", "other_religious_texts"],
    "biblical_languages": ["biblical_languages", "research_documents/christian_sources"],
    "biblical_language_source_depth": ["biblical_languages", "research_documents/christian_sources", "all_texts"],
    "psychology_patterns": ["psychology_inputs", "human_stories"],
    "pattern_perception_divine_response": ["psychology_inputs", "pattern_tests", "human_stories", "deep_sources"],
    "global_text_traditions": ["all_texts", "other_religious_texts", "modern_literature"],
    "modern_literature_meaning": ["modern_literature", "all_texts", "human_stories"],
    "cultural_practice_patterns": ["cultural_inputs", "history_inputs", "psychology_inputs"],
    "general_research_methods": ["research_documents", "deep_sources"],
    "interreligious_dream_testimony": ["other_religious_texts", "human_stories", "theologians"],
    "holy_spirit_gifts_global": ["theologians", "other_religious_texts", "human_stories", "psychology_inputs"],
    "technology_ethics": ["cultural_inputs"],
    "theologians_cross_era": ["theologians", "research_documents/christian_sources"],
}


TEXT_LAYER_ROUTES = {
    "theologians": ["athanasius", "augustine", "aquinas", "luther", "calvin", "barth", "bonhoeffer", "moltmann", "theologian", "trinity"],
    "visual_art": ["art", "beauty", "aesthetic", "icon", "iconography", "visual", "image", "photo", "gallery", "museum"],
    "history_inputs": ["history", "historical", "memory", "empire", "reform", "chronicle"],
    "world_languages": ["translation", "language", "semantics", "metaphor", "grammar"],
    "biblical_languages": ["hebrew", "greek", "septuagint", "logos", "pneuma", "ruach", "hesed"],
    "all_texts": ["sacred text", "scripture", "wisdom", "myth", "epic", "ritual", "oral tradition"],
    "psychology_inputs": ["psychology", "trauma", "attachment", "habit", "cognitive", "identity"],
    "other_religious_texts": ["comparative religion", "quran", "hindu", "buddhist", "islam", "judaism"],
    "modern_literature": ["modern literature", "novel", "fiction", "poetry", "drama", "memoir"],
    "human_stories": ["case study", "testimony", "lived experience", "pastoral", "counseling", "podcast", "interview", "documentary"],
    "deep_sources": ["quantum", "physics", "science", "peer review", "counterargument"],
    "pattern_tests": ["suffering", "injustice", "overclaim", "unanswered", "abuse", "counterargument"],
}


LAYER_REVIEW_PROMPTS = {
    "theologians": "Check named theologian, era, primary source, doctrine, disagreement, and pressure point.",
    "visual_art": "Review actual image/form, composition, symbol, context, beauty, lament, source rights, and counter-reading.",
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


def detect_media_kind(source: dict):
    text = source_text(source)
    url = (source.get("url") or "").lower()
    combined = f"{text} {url}"
    for kind, markers in MEDIA_SOURCE_MARKERS.items():
        if any(marker in combined for marker in markers):
            return kind
    return ""


def add_media_review_fields(source: dict):
    media_kind = detect_media_kind(source)
    if not media_kind:
        return source

    source["media_kind"] = media_kind
    source["requires_multimodal_review"] = True
    source["confidence_effect"] = "none_until_caption_transcript_or_human_review"
    source["media_review_prompt"] = (
        "Evaluate the actual media, not only the title/snippet. Capture a short "
        "caption or transcript note, source context, rights status, smallest "
        "allowed claim, and at least one counter-reading before strengthening a pattern."
    )
    if source.get("source_type") in {"open web result", "open web result via Tavily", "open web result via SearXNG"}:
        source["source_type"] = f"{media_kind} candidate"
    return source


def read_json(path: Path, default):
    if not path.exists():
        return default

    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def request_timeout_seconds():
    try:
        return max(1, int(os.getenv("SEARCH_REQUEST_TIMEOUT_SECONDS", "12")))
    except ValueError:
        return 12


def arxiv_timeout_seconds():
    try:
        return max(5, int(os.getenv("ARXIV_REQUEST_TIMEOUT_SECONDS", "25")))
    except ValueError:
        return 25


def opencitations_enrichment_limit():
    try:
        return max(0, int(os.getenv("OPENCITATIONS_ENRICHMENT_LIMIT", "25")))
    except ValueError:
        return 25


def auto_approve_review_queue_enabled():
    return provider_enabled("AUTO_APPROVE_REVIEW_QUEUE", default=False)


def auto_approve_min_score():
    try:
        return max(0, int(os.getenv("AUTO_APPROVE_MIN_SCORE", "7")))
    except ValueError:
        return 7


def auto_approve_open_web_enabled():
    return provider_enabled("AUTO_APPROVE_OPEN_WEB", default=False)


def auto_approve_warnings_enabled():
    return provider_enabled("AUTO_APPROVE_WITH_WARNINGS", default=False)


def provider_enabled(env_name: str, default: bool = True):
    value = os.getenv(env_name)
    if value is None:
        return default

    return value.strip().lower() not in {"0", "false", "no", "off"}


def fetch_json(url: str, timeout: int | None = None):
    timeout = request_timeout_seconds() if timeout is None else timeout
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_json_with_headers(url: str, headers: dict[str, str], timeout: int | None = None):
    timeout = request_timeout_seconds() if timeout is None else timeout
    request_headers = {
        "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)"
    }
    request_headers.update(headers)
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def post_json_with_headers(url: str, payload: dict, headers: dict[str, str], timeout: int | None = None):
    timeout = request_timeout_seconds() if timeout is None else timeout
    request_headers = {
        "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)",
        "Content-Type": "application/json",
    }
    request_headers.update(headers)
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=request_headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, timeout: int | None = None):
    timeout = request_timeout_seconds() if timeout is None else timeout
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DivinePatternResearchBot/0.1 (metadata-only research collector)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def searxng_base_url():
    return (os.getenv("SEARXNG_BASE_URL") or DEFAULT_SEARXNG_BASE_URL).rstrip("/")


def searxng_base_urls():
    configured = os.getenv("SEARXNG_BASE_URLS")
    if configured:
        return [url.strip().rstrip("/") for url in configured.split(",") if url.strip()]

    return [searxng_base_url()] if searxng_base_url() else []


def request_delay_seconds():
    try:
        return max(0.0, float(os.getenv("SEARCH_DELAY_SECONDS", "0.2")))
    except ValueError:
        return 0.2


def polite_delay():
    delay = request_delay_seconds()
    if delay:
        time.sleep(delay)


def tavily_daily_limit():
    try:
        return max(0, int(os.getenv("TAVILY_DAILY_SEARCH_LIMIT", "5")))
    except ValueError:
        return 5


def tavily_max_results():
    try:
        return max(1, min(10, int(os.getenv("TAVILY_MAX_RESULTS", "3"))))
    except ValueError:
        return 3


def tavily_today():
    return datetime.now(timezone.utc).date().isoformat()


def tavily_usage():
    usage = read_json(TAVILY_USAGE_PATH, {"days": {}})
    if "days" not in usage:
        usage["days"] = {}
    return usage


def tavily_searches_used_today():
    today_usage = tavily_usage().get("days", {}).get(tavily_today(), {})
    return int(today_usage.get("searches_used", 0) or 0)


def tavily_searches_remaining_today():
    return max(0, tavily_daily_limit() - tavily_searches_used_today())


def record_tavily_search(query: str, tag: str, credits_used: int = 1):
    usage = tavily_usage()
    today = tavily_today()
    today_usage = usage["days"].setdefault(
        today,
        {"searches_used": 0, "credits_used": 0, "queries": []},
    )
    today_usage["searches_used"] = int(today_usage.get("searches_used", 0) or 0) + 1
    today_usage["credits_used"] = int(today_usage.get("credits_used", 0) or 0) + credits_used
    today_usage.setdefault("queries", []).append(
        {
            "tag": tag,
            "query": query,
            "credits_used": credits_used,
            "searched_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_json(TAVILY_USAGE_PATH, usage)


def tavily_daily_query_keys():
    limit = tavily_daily_limit()
    if limit <= 0:
        return set()

    query_keys = [(tag, query) for tag, queries in QUERY_SETS.items() for query in queries]
    if not query_keys:
        return set()

    start = (datetime.now(timezone.utc).date().toordinal() * limit) % len(query_keys)
    return {query_keys[(start + offset) % len(query_keys)] for offset in range(min(limit, len(query_keys)))}


def read_search_strategy():
    strategy = read_json(
        SEARCH_STRATEGY_PATH,
        {
            "priority_lanes": [],
            "query_modifiers": [],
            "suggested_queries": [],
        },
    )
    if not isinstance(strategy, dict):
        return {
            "priority_lanes": [],
            "query_modifiers": [],
            "suggested_queries": [],
        }
    return strategy


def clean_query_fragment(value: str, limit: int = 90):
    value = re.sub(r"[^A-Za-z0-9 ,:/.'-]+", " ", value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def strategy_query_pairs(strategy: dict):
    pairs = []
    for item in strategy.get("suggested_queries", []):
        if not isinstance(item, dict):
            continue
        tag = item.get("tag")
        query = clean_query_fragment(item.get("query", ""), 180)
        if tag in QUERY_SETS and query:
            pairs.append((tag, query))
    return pairs


def expand_queries_with_strategy(strategy: dict):
    query_map = {tag: list(queries) for tag, queries in QUERY_SETS.items()}
    applied_modifiers = []
    priority_lanes = [
        clean_query_fragment(lane, 60)
        for lane in strategy.get("priority_lanes", [])
        if isinstance(lane, str)
    ][:6]
    modifiers = [
        clean_query_fragment(modifier, 50)
        for modifier in strategy.get("query_modifiers", [])
        if isinstance(modifier, str)
    ][:8]
    modifiers = [modifier for modifier in modifiers if modifier]

    if modifiers:
        focus_tags = []
        for tag, queries in QUERY_SETS.items():
            if any(lane in TAG_LAYER_ROUTES.get(tag, []) for lane in priority_lanes):
                focus_tags.append(tag)
        if not focus_tags:
            focus_tags = list(QUERY_SETS)[:6]

        for tag in focus_tags[:8]:
            base_query = query_map[tag][0]
            for modifier in modifiers[:2]:
                query = clean_query_fragment(f"{base_query} {modifier}", 180)
                if query and query not in query_map[tag]:
                    query_map[tag].append(query)
                    applied_modifiers.append(modifier)

    for tag, query in strategy_query_pairs(strategy):
        if query not in query_map[tag]:
            query_map[tag].insert(0, query)

    return query_map, list(dict.fromkeys(applied_modifiers))


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

    add_media_review_fields(source)
    if key in sources_by_id:
        existing = sources_by_id[key]
        existing_tags = set(existing.get("tags", []))
        existing_tags.update(source.get("tags", []))
        existing["tags"] = sorted(existing_tags)
        add_media_review_fields(existing)
        add_layer_routing(existing)
        return False

    source["id"] = key
    add_layer_routing(source)
    sources_by_id[key] = source
    return True


def count_by_provider(sources: list[dict]):
    counts = {}
    for source in sources:
        provider = source.get("provider") or "unknown"
        counts[provider] = counts.get(provider, 0) + 1
    return counts


def layer_balance_status(layer_counts: dict[str, int]):
    if not layer_counts:
        return []

    max_count = max(layer_counts.values())
    if max_count <= 0:
        return []

    thin_threshold = max(1, int(max_count * 0.25))
    return [
        (layer, count)
        for layer, count in sorted(layer_counts.items(), key=lambda item: (item[1], item[0]))
        if count < thin_threshold
    ]


def source_quality(source: dict):
    provider = source.get("provider", "")
    source_type = source.get("source_type", "")
    title = source.get("title", "").lower()
    summary = source.get("summary", "").lower()
    text = f"{title} {summary}"

    if "arxiv" in provider.lower():
        return "scholarly preprint"
    if provider in SCHOLARLY_METADATA_PROVIDERS:
        return "scholarly metadata"
    if provider in OPEN_WEB_PROVIDERS:
        return "open web result"
    if source_type == "counterargument":
        return "counterargument"
    if any(term in text for term in ["maybe", "proof of god", "quantum proves"]):
        return "speculative-risk"
    return "reference metadata"


def is_trusted_open_web_source(source: dict):
    url = (source.get("url") or "").lower()
    return any(domain in url for domain in TRUSTED_OPEN_WEB_DOMAINS)


def source_text(source: dict):
    return " ".join(
        [
            source.get("title", ""),
            source.get("summary", ""),
            " ".join(source.get("tags", [])),
            source.get("source_type", ""),
        ]
    ).lower()


def count_corroborating_sources(source: dict, sources: list[dict]):
    """Count other scholarly candidates that share tags or routed layers."""
    source_key = source.get("id") or source_id(source)
    source_tags = set(source.get("tags", []))
    source_layers = set(source.get("layer_routes", []))
    corroborating = 0

    for other in sources:
        other_key = other.get("id") or source_id(other)
        if other_key == source_key:
            continue
        if not (SCHOLARLY_METADATA_PROVIDERS | {"arXiv"}).intersection({other.get("provider", "")}):
            continue

        shared_tags = source_tags.intersection(other.get("tags", []))
        shared_layers = source_layers.intersection(other.get("layer_routes", []))
        if shared_tags or shared_layers:
            corroborating += 1

    return corroborating


def score_automated_evidence(source: dict, sources: list[dict]):
    """Estimate evidence strength from metadata, corroboration, and risk signals."""
    score = 0
    reasons = []
    warnings = []
    provider = source.get("provider", "")
    source_type = (source.get("source_type") or "").lower()
    text = source_text(source)
    citation_count = int(source.get("citation_count") or 0)
    corroborating = count_corroborating_sources(source, sources)

    if provider in SCHOLARLY_METADATA_PROVIDERS:
        score += 2
        reasons.append("scholarly metadata provider")
    elif provider == "arXiv":
        score += 1
        reasons.append("scholarly preprint provider")
    elif provider in OPEN_WEB_PROVIDERS:
        score += 0
        reasons.append("broad open-web search result")

    if is_trusted_open_web_source(source):
        score += 2
        reasons.append("trusted archive, university, government, museum, library, or public-domain domain")

    if source.get("doi"):
        score += 2
        reasons.append("DOI or stable scholarly identifier present")

    if source.get("authors"):
        score += 1
        reasons.append("author metadata present")

    if source.get("year"):
        score += 1
        reasons.append("publication year present")

    if any(term in source_type for term in ["journal", "article", "book", "chapter", "proceedings"]):
        score += 1
        reasons.append("recognized scholarly source type")

    if source.get("summary") and "no summary available" not in source.get("summary", "").lower():
        score += 1
        reasons.append("summary or abstract metadata available")

    if citation_count >= 100:
        score += 3
        reasons.append("high citation signal")
    elif citation_count >= 25:
        score += 2
        reasons.append("moderate citation signal")
    elif citation_count > 0:
        score += 1
        reasons.append("some citation signal")

    if corroborating >= 10:
        score += 3
        reasons.append("many routed corroborating candidates")
    elif corroborating >= 3:
        score += 2
        reasons.append("several routed corroborating candidates")
    elif corroborating > 0:
        score += 1
        reasons.append("at least one routed corroborating candidate")

    if any(term in text for term in ["counterargument", "critique", "limitation", "overclaim"]):
        score += 1
        reasons.append("counterargument or limitation language present")

    if any(term in text for term in ["proof of god", "quantum proves", "maybe", "possibly"]):
        score -= 3
        warnings.append("speculative or overclaim language detected")

    if source.get("requires_multimodal_review"):
        warnings.append("media candidate: inspect image/video/audio and capture caption or transcript before strengthening claims")
        if provider in OPEN_WEB_PROVIDERS:
            score -= 1

    if source.get("is_retracted"):
        score -= 8
        warnings.append("source metadata indicates retraction")

    if provider == "arXiv":
        warnings.append("preprint status: use cautiously until peer-reviewed or corroborated")
    if provider in OPEN_WEB_PROVIDERS and not is_trusted_open_web_source(source):
        warnings.append("open-web result: require corroboration before strengthening claims")

    if score >= 10:
        label = "strong_scholarly_candidate"
        use = "may increase confidence after claim-scope and counterargument checks"
    elif score >= 7:
        label = "moderate_scholarly_candidate"
        use = "can support cautious working claims when corroborated"
    elif score >= 4:
        label = "weak_scholarly_candidate"
        use = "use as a lead or question generator, not strong evidence"
    else:
        label = "do_not_strengthen_claim"
        use = "do not use to increase confidence without stronger corroboration"

    return {
        "score": score,
        "label": label,
        "corroborating_source_count": corroborating,
        "truth_assessment": label,
        "evaluation_use": use,
        "reasons": reasons[:8],
        "warnings": warnings[:5],
    }


def add_automated_evidence(source: dict, sources: list[dict]):
    add_media_review_fields(source)
    assessment = score_automated_evidence(source, sources)
    source["automated_evidence_score"] = assessment["score"]
    source["automated_evidence_label"] = assessment["label"]
    source["truth_assessment"] = assessment["truth_assessment"]
    source["corroborating_source_count"] = assessment["corroborating_source_count"]
    source["automated_evidence_reasons"] = assessment["reasons"]
    source["automated_evidence_warnings"] = assessment["warnings"]
    source["evaluation_use"] = assessment["evaluation_use"]
    source["review_status"] = f"machine_assessed_{assessment['label']}"
    return source


def add_auto_review_approval(source: dict):
    """Optionally auto-approve low-risk candidates for review routing only."""
    source.pop("auto_review_approval", None)
    source.pop("auto_review_approval_scope", None)
    source.pop("auto_review_approval_reasons", None)
    source.pop("auto_review_approval_warnings", None)
    source.pop("confidence_effect", None)

    if not auto_approve_review_queue_enabled():
        return source

    score = int(source.get("automated_evidence_score") or 0)
    label = source.get("automated_evidence_label", "not_scored")
    provider = source.get("provider", "")
    warnings = source.get("automated_evidence_warnings", [])
    is_open_web = provider in OPEN_WEB_PROVIDERS
    trusted_open_web = is_trusted_open_web_source(source)
    reasons = []
    blockers = []

    if score >= auto_approve_min_score():
        reasons.append(f"automated score >= {auto_approve_min_score()}")
    else:
        blockers.append(f"automated score below {auto_approve_min_score()}")

    if label in {"strong_scholarly_candidate", "moderate_scholarly_candidate"}:
        reasons.append(f"label is {label}")
    else:
        blockers.append(f"label {label} is not eligible")

    if source.get("doi"):
        reasons.append("stable DOI present")
    elif source.get("authors") and source.get("year"):
        reasons.append("author and year metadata present")
    elif trusted_open_web:
        reasons.append("trusted open-web domain present")
    else:
        blockers.append("missing DOI or author/year metadata")

    if warnings and not auto_approve_warnings_enabled():
        blockers.append("automated warning present")

    if is_open_web and not (auto_approve_open_web_enabled() and trusted_open_web):
        blockers.append("open-web source requires manual review")

    if blockers:
        source["auto_review_approval"] = "not_auto_approved"
        source["auto_review_approval_scope"] = "manual_review_required"
        source["auto_review_approval_warnings"] = blockers[:6]
        source["confidence_effect"] = "none_until_human_review"
        return source

    source["auto_review_approval"] = "approved_for_review_queue"
    source["auto_review_approval_scope"] = (
        "routing_and_queue_only_not_claim_confidence"
    )
    source["auto_review_approval_reasons"] = reasons[:6]
    source["confidence_effect"] = "none_until_human_review"
    source["review_status"] = "auto_approved_for_review_queue"
    return source


def route_layers_for_source(source: dict):
    add_media_review_fields(source)
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
                "citation_count": item.get("cited_by_count", 0),
                "is_retracted": item.get("is_retracted", False),
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
    text = fetch_text(url, timeout=arxiv_timeout_seconds())
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


def search_europe_pmc(query: str, tag: str, limit: int = 5):
    url = EUROPE_PMC_SEARCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "query": query,
            "pageSize": str(limit),
            "format": "json",
            "resultType": "core",
            "synonym": "true",
        }
    )
    payload = fetch_json(url)
    results = []

    for item in payload.get("resultList", {}).get("result", []):
        title = item.get("title", "")
        if not title:
            continue

        authors = [
            clean_text(author.strip(), 120)
            for author in (item.get("authorString") or "").split(",")[:3]
            if author.strip()
        ]
        full_text_urls = (item.get("fullTextUrlList") or {}).get("fullTextUrl") or [{}]
        url = item.get("doi") and f"https://doi.org/{item.get('doi')}"
        url = url or full_text_urls[0].get("url")
        url = url or (item.get("pmid") and f"https://pubmed.ncbi.nlm.nih.gov/{item.get('pmid')}/")
        url = url or item.get("id", "")

        results.append(
            {
                "title": clean_text(title, 250),
                "authors": authors,
                "year": item.get("pubYear"),
                "url": url,
                "doi": item.get("doi", ""),
                "provider": "Europe PMC",
                "source_type": item.get("pubType", "scholarly metadata"),
                "citation_count": item.get("citedByCount", 0),
                "tags": [tag],
                "summary": clean_text(item.get("abstractText", "")),
                "copyright_note": "Metadata and short abstract summary only; do not store full copyrighted text.",
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def search_pubmed(query: str, tag: str, limit: int = 5):
    search_url = PUBMED_ESEARCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": query,
            "retmax": str(limit),
            "retmode": "json",
            "sort": "relevance",
        }
    )
    search_payload = fetch_json(search_url)
    ids = search_payload.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    polite_delay()
    summary_url = PUBMED_ESUMMARY_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        }
    )
    summary_payload = fetch_json(summary_url)
    results = []

    for pmid in summary_payload.get("result", {}).get("uids", []):
        item = summary_payload.get("result", {}).get(pmid, {})
        title = item.get("title", "")
        if not title:
            continue

        authors = [
            clean_text(author.get("name", ""), 120)
            for author in (item.get("authors") or [])[:3]
            if author.get("name")
        ]
        article_ids = item.get("articleids") or []
        doi = next((entry.get("value") for entry in article_ids if entry.get("idtype") == "doi"), "")
        pub_types = item.get("pubtype") or ["scholarly metadata"]

        results.append(
            {
                "title": clean_text(title, 250),
                "authors": authors,
                "year": (item.get("pubdate") or "")[:4] or None,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "doi": doi,
                "provider": "PubMed",
                "source_type": pub_types[0],
                "tags": [tag],
                "summary": clean_text(item.get("source", "")),
                "copyright_note": "Metadata only; do not store full copyrighted text.",
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def search_internet_archive(query: str, tag: str, limit: int = 5):
    url = INTERNET_ARCHIVE_ADVANCED_SEARCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "q": query,
            "fl[]": ["identifier", "title", "creator", "date", "description", "mediatype"],
            "rows": str(limit),
            "page": "1",
            "output": "json",
        },
        doseq=True,
    )
    payload = fetch_json(url)
    results = []

    for item in payload.get("response", {}).get("docs", []):
        title = item.get("title", "")
        if isinstance(title, list):
            title = " ".join(title)
        if not title:
            continue

        creators = item.get("creator") or []
        if isinstance(creators, str):
            creators = [creators]
        description = item.get("description", "")
        if isinstance(description, list):
            description = " ".join(str(part) for part in description)

        results.append(
            {
                "title": clean_text(title, 250),
                "authors": [clean_text(author, 120) for author in creators[:3] if author],
                "year": str(item.get("date", ""))[:4] or None,
                "url": f"https://archive.org/details/{item.get('identifier')}",
                "doi": "",
                "provider": "Internet Archive",
                "source_type": f"archive.org {item.get('mediatype', 'metadata')}",
                "tags": [tag],
                "summary": clean_text(description),
                "copyright_note": "Archive metadata and short description only; review item rights before use.",
                "review_status": "unreviewed_daily_candidate",
                "evaluation_use": "candidate lead only until original source review and counterargument check",
                "date_accessed": datetime.now(timezone.utc).date().isoformat(),
            }
        )

    return results


def web_source_from_result(result: dict, provider: str, tag: str):
    title = result.get("name") or result.get("title") or ""
    url = result.get("url") or result.get("link") or ""
    summary = result.get("snippet") or result.get("description") or ""
    if not title or not url:
        return None

    source = {
        "title": clean_text(title, 250),
        "authors": [],
        "year": None,
        "url": url,
        "doi": "",
        "provider": provider,
        "source_type": "open web result",
        "tags": [tag],
        "summary": clean_text(summary),
        "copyright_note": "Open web search metadata and short snippet only; do not store full copyrighted text.",
        "review_status": "unreviewed_web_candidate",
        "evaluation_use": "open web lead only until corroborated by scholarly or trusted sources",
        "date_accessed": datetime.now(timezone.utc).date().isoformat(),
    }
    add_media_review_fields(source)
    return source


def search_bing_web(query: str, tag: str, limit: int = 5):
    api_key = os.getenv("BING_SEARCH_API_KEY")
    if not api_key:
        return []

    url = BING_WEB_SEARCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "q": query,
            "count": str(limit),
            "responseFilter": "Webpages",
            "safeSearch": "Moderate",
            "textFormat": "Raw",
        }
    )
    payload = fetch_json_with_headers(url, {"Ocp-Apim-Subscription-Key": api_key})
    results = []

    for item in payload.get("webPages", {}).get("value", []):
        source = web_source_from_result(item, "Bing Web Search", tag)
        if source:
            results.append(source)

    return results


def search_brave_web(query: str, tag: str, limit: int = 5):
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        return []

    url = BRAVE_WEB_SEARCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {
            "q": query,
            "count": str(limit),
            "safesearch": "moderate",
            "text_decorations": "false",
        }
    )
    payload = fetch_json_with_headers(
        url,
        {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
    )
    results = []

    for item in payload.get("web", {}).get("results", []):
        source = web_source_from_result(item, "Brave Search", tag)
        if source:
            results.append(source)

    return results


def search_tavily_web(query: str, tag: str, limit: int = 5):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or tavily_searches_remaining_today() <= 0:
        return []

    max_results = min(limit, tavily_max_results())
    payload = {
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }
    response = post_json_with_headers(
        TAVILY_SEARCH_ENDPOINT,
        payload,
        {"Authorization": f"Bearer {api_key}"},
    )
    record_tavily_search(query, tag, credits_used=1)
    results = []

    for item in response.get("results", [])[:max_results]:
        source = web_source_from_result(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("content", ""),
            },
            "Tavily Search",
            tag,
        )
        if source:
            source["source_type"] = "open web result via Tavily"
            if item.get("score") is not None:
                source["relevance_score"] = item.get("score")
            results.append(source)

    return results


def search_searxng_web(query: str, tag: str, limit: int = 5, base_url: str | None = None):
    base_url = (base_url or searxng_base_url()).rstrip("/")
    if not base_url:
        return []

    url = base_url + "/search?" + urllib.parse.urlencode(
        {
            "q": query,
            "format": "json",
            "categories": "general",
        }
    )
    payload = fetch_json(url)
    results = []

    for item in payload.get("results", [])[:limit]:
        source = web_source_from_result(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("content", ""),
            },
            "SearXNG",
            tag,
        )
        if source:
            source["source_type"] = "open web result via SearXNG"
            results.append(source)

    return results


def search_searxng_web_all(query: str, tag: str, limit: int = 5):
    results = []
    errors = []

    for base_url in searxng_base_urls():
        try:
            results.extend(search_searxng_web(query, tag, limit, base_url=base_url))
            if len(results) >= limit:
                return results[:limit]
        except HTTPError as exc:
            errors.append(f"{base_url}: {exc}")
            if exc.code != 429:
                continue
        except Exception as exc:
            errors.append(f"{base_url}: {exc}")
        finally:
            polite_delay()

    return results[:limit]


def fetch_opencitations_count(kind: str, doi: str):
    url = f"{OPENCITATIONS_INDEX_ENDPOINT}/{kind}/doi:{urllib.parse.quote(doi, safe='/')}"
    payload = fetch_json(url)
    if isinstance(payload, list):
        return len(payload)
    return 0


def enrich_sources_with_opencitations(sources: list[dict], errors: list[str]):
    if not provider_enabled("ENABLE_OPENCITATIONS"):
        return 0

    enriched = 0
    limit = opencitations_enrichment_limit()
    for source in sources:
        if enriched >= limit:
            break
        doi = source.get("doi")
        if not doi or source.get("opencitations_checked_at"):
            continue

        try:
            references_count = fetch_opencitations_count("references", doi)
            citations_count = fetch_opencitations_count("citations", doi)
            source["opencitations_reference_count"] = references_count
            source["opencitations_citation_count"] = citations_count
            if citations_count and not source.get("citation_count"):
                source["citation_count"] = citations_count
            source["opencitations_checked_at"] = datetime.now(timezone.utc).date().isoformat()
            enriched += 1
        except HTTPError as exc:
            errors.append(f"OpenCitations enrichment failed for DOI {doi}: {exc}")
            if exc.code == 429:
                break
        except Exception as exc:
            errors.append(f"OpenCitations enrichment failed for DOI {doi}: {exc}")
            if isinstance(exc, (TimeoutError, SocketTimeoutError)) or "timed out" in str(exc).lower():
                break
        finally:
            polite_delay()

    return enriched


def collect_sources():
    existing = read_json(REFERENCES_PATH, {"sources": []})
    sources_by_id = {source_id(source): source for source in existing.get("sources", []) if source_id(source)}
    for source in sources_by_id.values():
        add_media_review_fields(source)
        add_layer_routing(source)
    new_count = 0
    new_sources = []
    errors = []
    unavailable_collectors = set()
    run_provider_counts = {}
    new_provider_counts = {}
    opencitations_enriched_count = 0
    search_strategy = read_search_strategy()
    query_sets, applied_query_modifiers = expand_queries_with_strategy(search_strategy)
    strategy_query_count = len(strategy_query_pairs(search_strategy))
    broad_web_enabled = bool(
        (provider_enabled("ENABLE_BING_WEB") and os.getenv("BING_SEARCH_API_KEY"))
        or (provider_enabled("ENABLE_BRAVE_WEB") and os.getenv("BRAVE_SEARCH_API_KEY"))
        or (provider_enabled("ENABLE_TAVILY_WEB") and os.getenv("TAVILY_API_KEY"))
        or (provider_enabled("ENABLE_SEARXNG") and searxng_base_urls())
    )
    tavily_query_keys = tavily_daily_query_keys()

    for tag, queries in query_sets.items():
        for query in queries:
            collectors = []
            if provider_enabled("ENABLE_CROSSREF"):
                collectors.append(search_crossref)
            if provider_enabled("ENABLE_OPENALEX"):
                collectors.append(search_openalex)
            if provider_enabled("ENABLE_EUROPE_PMC"):
                collectors.append(search_europe_pmc)
            if provider_enabled("ENABLE_PUBMED"):
                collectors.append(search_pubmed)
            if provider_enabled("ENABLE_INTERNET_ARCHIVE"):
                collectors.append(search_internet_archive)
            if "quantum" in tag or "science" in tag or "music_math" in tag:
                if provider_enabled("ENABLE_ARXIV"):
                    collectors.append(search_arxiv)
            if broad_web_enabled:
                if provider_enabled("ENABLE_BING_WEB"):
                    collectors.append(search_bing_web)
                if provider_enabled("ENABLE_BRAVE_WEB"):
                    collectors.append(search_brave_web)
                if (
                    provider_enabled("ENABLE_TAVILY_WEB")
                    and os.getenv("TAVILY_API_KEY")
                    and (tag, query) in tavily_query_keys
                    and tavily_searches_remaining_today() > 0
                ):
                    collectors.append(search_tavily_web)
                if searxng_base_urls():
                    if provider_enabled("ENABLE_SEARXNG"):
                        collectors.append(search_searxng_web_all)

            for collector in collectors:
                if collector.__name__ in unavailable_collectors:
                    continue

                try:
                    for source in collector(query, tag):
                        add_media_review_fields(source)
                        provider = source.get("provider") or collector.__name__
                        run_provider_counts[provider] = run_provider_counts.get(provider, 0) + 1
                        source["quality"] = source_quality(source)
                        if add_source(sources_by_id, source):
                            new_count += 1
                            new_sources.append(source)
                            new_provider_counts[provider] = new_provider_counts.get(provider, 0) + 1
                except HTTPError as exc:
                    errors.append(f"{collector.__name__} failed for {tag}: {exc}")
                    if exc.code == 429:
                        unavailable_collectors.add(collector.__name__)
                except Exception as exc:
                    errors.append(f"{collector.__name__} failed for {tag}: {exc}")
                    if isinstance(exc, (TimeoutError, SocketTimeoutError)) or "timed out" in str(exc).lower():
                        unavailable_collectors.add(collector.__name__)
                finally:
                    polite_delay()

    for source in sources_by_id.values():
        add_media_review_fields(source)
        add_layer_routing(source)

    sources = sorted(sources_by_id.values(), key=lambda item: (item.get("tags", []), item.get("title", "")))
    opencitations_enriched_count = enrich_sources_with_opencitations(sources, errors)
    for source in sources:
        add_automated_evidence(source, sources)
        add_auto_review_approval(source)
    for source in new_sources:
        source_key = source.get("id") or source_id(source)
        if source_key in sources_by_id:
            source.update(sources_by_id[source_key])
    layer_counts = {}
    new_layer_counts = {}
    evidence_counts = {}
    new_evidence_counts = {}
    auto_approval_counts = {}
    new_auto_approval_counts = {}
    media_counts = {}
    new_media_counts = {}
    for source in sources:
        for layer in source.get("layer_routes", []):
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
        label = source.get("automated_evidence_label", "not_scored")
        evidence_counts[label] = evidence_counts.get(label, 0) + 1
        approval = source.get("auto_review_approval", "not_configured")
        auto_approval_counts[approval] = auto_approval_counts.get(approval, 0) + 1
        media_kind = source.get("media_kind")
        if media_kind:
            media_counts[media_kind] = media_counts.get(media_kind, 0) + 1
    for source in new_sources:
        for layer in source.get("layer_routes", []):
            new_layer_counts[layer] = new_layer_counts.get(layer, 0) + 1
        label = source.get("automated_evidence_label", "not_scored")
        new_evidence_counts[label] = new_evidence_counts.get(label, 0) + 1
        approval = source.get("auto_review_approval", "not_configured")
        new_auto_approval_counts[approval] = new_auto_approval_counts.get(approval, 0) + 1
        media_kind = source.get("media_kind")
        if media_kind:
            new_media_counts[media_kind] = new_media_counts.get(media_kind, 0) + 1
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
            "automated_evidence_counts": evidence_counts,
            "new_automated_evidence_counts": new_evidence_counts,
            "auto_review_approval_counts": auto_approval_counts,
            "new_auto_review_approval_counts": new_auto_approval_counts,
            "media_candidate_counts": media_counts,
            "new_media_candidate_counts": new_media_counts,
            "auto_review_approval_setup": {
                "enabled": auto_approve_review_queue_enabled(),
                "min_score": auto_approve_min_score(),
                "open_web_allowed": auto_approve_open_web_enabled(),
                "warnings_allowed": auto_approve_warnings_enabled(),
                "scope": "routing_and_queue_only_not_claim_confidence",
            },
            "run_provider_counts": run_provider_counts,
            "new_provider_counts": new_provider_counts,
            "query_modifiers": applied_query_modifiers,
            "search_strategy": {
                "path": SEARCH_STRATEGY_PATH.as_posix(),
                "updated_at": search_strategy.get("updated_at", "not available"),
                "priority_lanes": search_strategy.get("priority_lanes", [])[:8],
                "suggested_query_count": strategy_query_count,
            },
            "opencitations_enriched_count": opencitations_enriched_count,
            "errors": errors,
        },
    )
    write_reports(
        sources,
        new_count,
        new_sources,
        errors,
        run_provider_counts,
        new_provider_counts,
        opencitations_enriched_count,
        applied_query_modifiers,
        search_strategy,
    )


def write_reports(
    sources: list[dict],
    new_count: int,
    new_sources: list[dict],
    errors: list[str],
    run_provider_counts: dict[str, int],
    new_provider_counts: dict[str, int],
    opencitations_enriched_count: int = 0,
    applied_query_modifiers: list[str] | None = None,
    search_strategy: dict | None = None,
):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    applied_query_modifiers = applied_query_modifiers or []
    search_strategy = search_strategy or {}

    tag_counts = {}
    quality_counts = {}
    layer_counts = {}
    evidence_counts = {}
    auto_approval_counts = {}
    media_counts = {}
    for source in sources:
        for tag in source.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        for layer in source.get("layer_routes", []):
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
        quality = source.get("quality", "unknown")
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
        evidence_label = source.get("automated_evidence_label", "not_scored")
        evidence_counts[evidence_label] = evidence_counts.get(evidence_label, 0) + 1
        approval = source.get("auto_review_approval", "not_configured")
        auto_approval_counts[approval] = auto_approval_counts.get(approval, 0) + 1
        media_kind = source.get("media_kind")
        if media_kind:
            media_counts[media_kind] = media_counts.get(media_kind, 0) + 1

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
        "- Videos, podcasts, and images are candidate evidence only after the actual media is reviewed through captions, transcripts, source context, rights status, and counter-readings.",
        "- Treat search results as candidate references until reviewed.",
        "- Keep quantum/science claims tied to qualified sources and stated limits.",
        "",
        "Online Collection Status",
        "------------------------",
    ]
    if run_provider_counts:
        lines.append("- Online scholarly/indexed metadata returned from provider APIs this run.")
    else:
        lines.append("- No online provider returned candidate metadata this run.")
    if applied_query_modifiers:
        lines.append(
            "- Self-directed query modifiers used this run: "
            + ", ".join(applied_query_modifiers[:8])
            + "."
        )
    if search_strategy.get("priority_lanes"):
        lines.append(
            "- Search strategy priority lanes: "
            + ", ".join(search_strategy.get("priority_lanes", [])[:8])
            + "."
        )

    searxng_errors = [error for error in errors if error.startswith("search_searxng_web")]
    open_web_returned = sum(
        count for provider, count in run_provider_counts.items() if provider in OPEN_WEB_PROVIDERS
    )
    lines.append(
        "- Free/keyless metadata providers available: Crossref, OpenAlex, Europe PMC, PubMed, Internet Archive, and arXiv for science/music queries."
    )
    if provider_enabled("ENABLE_OPENCITATIONS"):
        lines.append(
            f"- OpenCitations DOI enrichment checked {opencitations_enriched_count:,} stored DOI source(s) this run."
        )
    if (
        (provider_enabled("ENABLE_BING_WEB") and os.getenv("BING_SEARCH_API_KEY"))
        or (provider_enabled("ENABLE_BRAVE_WEB") and os.getenv("BRAVE_SEARCH_API_KEY"))
        or (provider_enabled("ENABLE_TAVILY_WEB") and os.getenv("TAVILY_API_KEY"))
        or (provider_enabled("ENABLE_SEARXNG") and searxng_base_urls())
    ):
        lines.append(
            "- Broad web search attempted via SearXNG "
            + f"({', '.join(searxng_base_urls()) or 'not configured'}), Tavily, or configured search API keys."
        )
        if os.getenv("TAVILY_API_KEY") and provider_enabled("ENABLE_TAVILY_WEB"):
            lines.append(
                f"- Tavily budget: {tavily_searches_used_today():,}/{tavily_daily_limit():,} basic searches used today; "
                + f"{tavily_searches_remaining_today():,} remaining."
            )
        if open_web_returned:
            lines.append(f"- Open-web candidates returned this run: {open_web_returned:,}.")
        elif searxng_errors:
            lines.append("- Open-web candidates returned this run: 0; configured SearXNG endpoint(s) rate-limited or rejected the request.")
        else:
            lines.append("- Open-web candidates returned this run: 0.")
    else:
        lines.append("- Broad web search not enabled; set TAVILY_API_KEY, SEARXNG_BASE_URLS, SEARXNG_BASE_URL, BING_SEARCH_API_KEY, or BRAVE_SEARCH_API_KEY to include open WWW search results.")

    if run_provider_counts:
        lines.append("- Provider results returned this run:")
        lines.extend(f"  - {provider}: {count:,}" for provider, count in sorted(run_provider_counts.items()))
    if new_provider_counts:
        lines.append("- Brand-new references added by provider:")
        lines.extend(f"  - {provider}: {count:,}" for provider, count in sorted(new_provider_counts.items()))
    else:
        lines.append("- Brand-new references added by provider: 0.")

    provider_totals = count_by_provider(sources)
    lines.append("- Total stored references by provider:")
    lines.extend(f"  - {provider}: {count:,}" for provider, count in sorted(provider_totals.items()))
    lines.extend(["", "Reference Tags", "--------------"])

    lines.extend(f"- {tag}: {count:,}" for tag, count in sorted(tag_counts.items()))
    lines.extend(["", "Layer Routes", "------------"])
    lines.extend(f"- {layer}: {count:,}" for layer, count in sorted(layer_counts.items()))
    thin_layers = layer_balance_status(layer_counts)
    if thin_layers:
        lines.extend(["", "Layer Balance Watch", "-------------------"])
        lines.append(
            "- These layers are below 25% of the current largest layer count; prioritize direct source notes and targeted searches here:"
        )
        lines.extend(f"  - {layer}: {count:,}" for layer, count in thin_layers)
    lines.extend(["", "Quality Counts", "--------------"])
    lines.extend(f"- {quality}: {count:,}" for quality, count in sorted(quality_counts.items()))
    lines.extend(["", "Media Candidate Counts", "----------------------"])
    if media_counts:
        lines.extend(f"- {kind}: {count:,}" for kind, count in sorted(media_counts.items()))
    else:
        lines.append("- No video, podcast/audio, or image candidates detected yet.")
    lines.extend(["", "Automated Evidence Counts", "-------------------------"])
    lines.extend(f"- {label}: {count:,}" for label, count in sorted(evidence_counts.items()))
    lines.extend(["", "Auto Review Approval Counts", "---------------------------"])
    if auto_approve_review_queue_enabled():
        lines.append(
            "- Auto approval is enabled for review queue/routing only; it does not increase pattern confidence."
        )
        lines.append(f"- Minimum score: {auto_approve_min_score():,}")
        lines.append(f"- Open-web auto approval enabled: {auto_approve_open_web_enabled()}")
        lines.append(f"- Warning-bearing source auto approval enabled: {auto_approve_warnings_enabled()}")
    else:
        lines.append("- Auto approval is disabled.")
    lines.extend(f"- {label}: {count:,}" for label, count in sorted(auto_approval_counts.items()))

    new_tag_counts = {}
    new_layer_counts = {}
    new_media_counts = {}
    for source in new_sources:
        for tag in source.get("tags", []):
            new_tag_counts[tag] = new_tag_counts.get(tag, 0) + 1
        for layer in source.get("layer_routes", []):
            new_layer_counts[layer] = new_layer_counts.get(layer, 0) + 1
        media_kind = source.get("media_kind")
        if media_kind:
            new_media_counts[media_kind] = new_media_counts.get(media_kind, 0) + 1

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

    lines.extend(["", "New Media Candidates", "--------------------"])
    if new_media_counts:
        lines.extend(f"- {kind}: {count:,}" for kind, count in sorted(new_media_counts.items()))
    else:
        lines.append("- No brand-new video, podcast/audio, or image candidates detected this run.")

    lines.extend(["", "Newest Additions This Run", "------------------------"])
    if new_sources:
        for source in new_sources[:30]:
            tags = ", ".join(source.get("tags", []))
            routes = ", ".join(source.get("layer_routes", []))
            lines.append(f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'})")
            lines.append(f"  Tags: {tags}")
            lines.append(f"  Layer routes: {routes}")
            lines.append(f"  Source: {source.get('provider')} | {source.get('quality')}")
            if source.get("media_kind"):
                lines.append(f"  Media candidate: {source.get('media_kind')} | review required before confidence change")
            lines.append(
                f"  Automated evidence: {source.get('automated_evidence_label', 'not_scored')} ({source.get('automated_evidence_score', 0)})"
            )
            lines.append(
                f"  Auto review approval: {source.get('auto_review_approval', 'not_configured')} | confidence effect: {source.get('confidence_effect', 'none_until_human_review')}"
            )
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
        lines.append(
            f"  Automated evidence: {source.get('automated_evidence_label', 'not_scored')} ({source.get('automated_evidence_score', 0)})"
        )
        lines.append(
            f"  Auto review approval: {source.get('auto_review_approval', 'not_configured')} | confidence effect: {source.get('confidence_effect', 'none_until_human_review')}"
        )
        if authors:
            lines.append(f"  Authors: {authors}")
        lines.append(f"  Source: {source.get('provider')} | {source.get('quality')}")
        if source.get("media_kind"):
            lines.append(f"  Media candidate: {source.get('media_kind')} | review required before confidence change")
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
                f"- Media kind: {source.get('media_kind', 'none')}",
                f"- Requires multimodal review: {source.get('requires_multimodal_review', False)}",
                f"- Automated evidence: {source.get('automated_evidence_label', 'not_scored')} ({source.get('automated_evidence_score', 0)})",
                f"- Auto review approval: {source.get('auto_review_approval', 'not_configured')}",
                f"- Auto approval scope: {source.get('auto_review_approval_scope', 'manual_review_required')}",
                f"- Confidence effect: {source.get('confidence_effect', 'none_until_human_review')}",
                f"- Corroborating routed candidates: {source.get('corroborating_source_count', 0)}",
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
        "Media rule: videos, podcasts, and images can be found and queued, but they cannot strengthen a claim until a caption/transcript or direct human/MLLM observation note records what is actually present in the media.",
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
                f"- Media kind: {source.get('media_kind', 'none')}",
                f"- Requires multimodal review: {source.get('requires_multimodal_review', False)}",
                f"- Automated evidence: {source.get('automated_evidence_label', 'not_scored')} ({source.get('automated_evidence_score', 0)})",
                f"- Auto review approval: {source.get('auto_review_approval', 'not_configured')}",
                f"- Auto approval scope: {source.get('auto_review_approval_scope', 'manual_review_required')}",
                f"- Confidence effect: {source.get('confidence_effect', 'none_until_human_review')}",
                f"- Truth assessment: {source.get('truth_assessment', 'not_scored')}",
                f"- Corroborating routed candidates: {source.get('corroborating_source_count', 0)}",
                f"- Year: {source.get('year') or 'n.d.'}",
                f"- URL: {source.get('url')}",
                "",
                textwrap.fill(summary, width=100),
                "",
                "Automated evidence reasons:",
            ]
        )
        for reason in source.get("automated_evidence_reasons", [])[:6]:
            queue_lines.append(f"- {reason}")
        if source.get("auto_review_approval_reasons"):
            queue_lines.append("")
            queue_lines.append("Auto approval reasons:")
            for reason in source.get("auto_review_approval_reasons", [])[:6]:
                queue_lines.append(f"- {reason}")
        if source.get("auto_review_approval_warnings"):
            queue_lines.append("")
            queue_lines.append("Auto approval blockers:")
            for warning in source.get("auto_review_approval_warnings", [])[:6]:
                queue_lines.append(f"- {warning}")
        if source.get("automated_evidence_warnings"):
            queue_lines.append("")
            queue_lines.append("Automated evidence warnings:")
            for warning in source.get("automated_evidence_warnings", [])[:4]:
                queue_lines.append(f"- {warning}")
        if source.get("media_review_prompt"):
            queue_lines.append("")
            queue_lines.append("Media review prompt:")
            queue_lines.append(f"- {source.get('media_review_prompt')}")
        queue_lines.extend(
            [
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
