from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/published/final_book_report.md")
REFERENCES_PATH = Path("references/references.json")
DAILY_DIGEST_PATH = Path("references/daily_research_digest.json")
KNOWLEDGE_INDEX_PATH = Path("reports/knowledge_retrieval_index.json")
FRICTION_LAYERS_PATH = Path("research_documents/friction_layers.json")
THEOLOGICAL_FOUNDATIONS_PATH = Path("research_documents/theological_foundations.json")
PATTERN_DISTORTION_PATH = Path("research_documents/pattern_distortion_layer.json")
CHRISTOLOGICAL_LAYER_PATH = Path("research_documents/christological_layer.json")
HISTORICAL_WITNESSES_PATH = Path("research_documents/historical_witnesses.json")
MYSTERY_LAYER_PATH = Path("research_documents/mystery_layer.json")
PROJECT_ARCHITECTURE_PATH = Path("research_documents/project_architecture.json")

SOURCE_REPORTS = {
    "backend": Path("reports/ai_backend_report.txt"),
    "summary": Path("reports/divine_pattern_summary_report.txt"),
    "top_patterns": Path("reports/top_five_divine_patterns_report.txt"),
    "tests": Path("reports/divine_pattern_test_report.txt"),
    "deep": Path("reports/deep_source_review_report.txt"),
    "theologians": Path("reports/theologian_pattern_design_report.txt"),
    "reader": Path("reports/divine_pattern_reader_book.txt"),
}

TOP_PATTERN_NAMES = [
    "Image Of God Pattern",
    "Cross And Reversal Pattern",
    "Creation-To-Consciousness Pattern",
    "Trinity-As-Behavior Pattern",
    "Providence And Contingency Pattern",
]

PATTERN_PROFILES = {
    "Image Of God Pattern": {
        "movement": "Mind -> Symbol -> Moral Agency -> Relationship -> Worship",
        "thesis": "Human dignity is treated as gift before performance.",
        "candidate": "God gives persons dignity before usefulness; the faithful response is truthful worship, humble love, justice for vulnerable people, patient repair, and faithful refusal to rank people by performance.",
    },
    "Cross And Reversal Pattern": {
        "movement": "Power -> Humility | Violence -> Forgiveness | Suffering -> Redemption | Death -> Resurrection",
        "thesis": "The cross is read as God's judgment on violent power and God's mercy for wounded people.",
        "candidate": "God reveals holy love by reversing coercive power through the cross; the faithful response is truth-telling, humble repentance, justice for harmed people, patient repair, and faithful mercy without denial.",
    },
    "Creation-To-Consciousness Pattern": {
        "movement": "Physical Order -> Life -> Consciousness -> Moral Awareness -> Worship",
        "thesis": "Creation, life, mind, moral awareness, and worship are explored as layered gifts.",
        "candidate": "God gives ordered creation, life, consciousness, and moral awareness as gifts; the faithful response is humble wonder, truthful stewardship, just care for bodies and creation, patient learning, and worshipful faithfulness.",
    },
    "Trinity-As-Behavior Pattern": {
        "movement": "Father Creates -> Son Redeems -> Spirit Transforms",
        "thesis": "Doctrine is tested by practice: receiving life as gift, following Christ, and discerning Spirit-led transformation.",
        "candidate": "God's triune work appears as creation received, redemption followed, and Spirit-led transformation tested by truth, love, humility, justice, worship, patience, and faithfulness.",
    },
    "Providence And Contingency Pattern": {
        "movement": "Stable Law -> Contingent Events -> Emergent Complexity -> Meaningful History",
        "thesis": "Providence is treated as trust inside contingency, not certainty about hidden causes.",
        "candidate": "God's providence is discerned as faithful trust inside lawful but contingent history; the faithful response is truthful humility, just action, patient endurance, worship, and faithfulness without pretending to know every cause.",
    },
}

DEFAULT_CANDIDATE_PATTERN = {
    "name": "Integrated Gift-And-Faithfulness Pattern",
    "movement": "Gift -> Recognition -> Responsibility -> Sacrificial Love -> Repair -> Worshipful Faithfulness",
    "candidate": "God gives life, dignity, order, mercy, and transformation as gifts; human beings are invited to answer those gifts with truthful worship, humble love, justice, repair, patience, and faithful action.",
    "basis": "No single pattern family clearly outranks the others in the current analyzed corpus, so the report presents an integrated candidate pattern.",
    "counts": {},
}


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def read_friction_layers() -> list[dict]:
    payload = read_json(FRICTION_LAYERS_PATH)
    records = payload.get("friction_layers", [])
    return records if isinstance(records, list) else []


def read_layer(path: Path) -> dict:
    return read_json(path)


def current_candidate_pattern(index: dict) -> dict:
    counts = {name: {"documents": 0, "review_notes": 0, "score": 0} for name in TOP_PATTERN_NAMES}
    for document in index.get("documents", []):
        patterns = set(document.get("patterns", []))
        for name in TOP_PATTERN_NAMES:
            if name not in patterns:
                continue
            review_notes = int(document.get("review_note_count") or 0)
            counts[name]["documents"] += 1
            counts[name]["review_notes"] += review_notes
            counts[name]["score"] += 1 + min(review_notes, 25)

    ranked = sorted(
        counts.items(),
        key=lambda item: (item[1]["score"], item[1]["documents"], item[1]["review_notes"], item[0]),
        reverse=True,
    )
    if not ranked or ranked[0][1]["score"] == 0:
        return dict(DEFAULT_CANDIDATE_PATTERN)

    top_name, top_counts = ranked[0]
    second_score = ranked[1][1]["score"] if len(ranked) > 1 else 0
    if second_score and top_counts["score"] < second_score * 1.25:
        result = dict(DEFAULT_CANDIDATE_PATTERN)
        result["basis"] = (
            "The current analyzed corpus is balanced across several pattern families, "
            "so the report keeps the broader integrated candidate rather than forcing one winner."
        )
        result["counts"] = counts
        return result

    profile = PATTERN_PROFILES[top_name]
    return {
        "name": top_name,
        "movement": profile["movement"],
        "candidate": profile["candidate"],
        "basis": (
            f"This wording is selected from the current retrieval index because {top_name} "
            f"has the strongest pattern-support score in the analyzed corpus."
        ),
        "counts": counts,
    }


def find_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith(prefix):
            return line.strip()
    return ""


def extract_backend_stats(text: str) -> dict[str, str]:
    return {
        "indexed": find_line(text, "- Indexed documents:").replace("- ", ""),
        "text_documents": find_line(text, "- Indexed text documents:").replace("- ", ""),
        "media_assets": find_line(text, "- Indexed media assets:").replace("- ", ""),
        "nodes": find_line(text, "- Graph nodes:").replace("- ", ""),
        "edges": find_line(text, "- Graph edges:").replace("- ", ""),
        "multimodal_review": find_line(text, "- Multimodal assets needing review:").replace("- ", ""),
        "strongest": find_line(text, "Backend: theologians"),
        "patterns": find_line(text, "Backend: Image Of God Pattern"),
        "rules": find_line(text, "Backend: discernment"),
    }


def extract_lane_line(text: str, lane: str) -> str:
    pattern = re.compile(rf"^- {re.escape(lane)}: .+$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(0).replace("- ", "") if match else ""


def compact_lane_table(backend_text: str) -> list[str]:
    lanes = [
        "theologians",
        "all_texts",
        "other_religious_texts",
        "history_inputs",
        "biblical_languages",
        "world_languages",
        "deep_sources",
        "pattern_tests",
        "visual_art",
        "cultural_inputs",
    ]
    return [line for lane in lanes if (line := extract_lane_line(backend_text, lane))]


def pattern_section(name: str) -> tuple[str, str, str, str, str]:
    sections = {
        "Image Of God Pattern": (
            PATTERN_PROFILES["Image Of God Pattern"]["movement"],
            PATTERN_PROFILES["Image Of God Pattern"]["thesis"],
            "It is strongest where language, theology, history, and vulnerable communities all pressure the same claim: persons must not be ranked by usefulness, intelligence, status, race, caste, health, or productivity.",
            "It weakens wherever dignity becomes conditional or where the project talks about humanity in the abstract while ignoring disability, poverty, migration, incarceration, or racialized harm.",
            "The faithful response is protection: listen first, defend the vulnerable, make worship and community accessible, and refuse usefulness-based love.",
        ),
        "Cross And Reversal Pattern": (
            PATTERN_PROFILES["Cross And Reversal Pattern"]["movement"],
            PATTERN_PROFILES["Cross And Reversal Pattern"]["thesis"],
            "It is strongest when passion texts, trauma theology, liberation theology, martyr memory, and abuse-pressure cases are read together.",
            "It collapses if suffering is romanticized, if victims are asked to forgive without justice, or if cross-language protects perpetrators.",
            "The faithful response is truth with boundaries: name harm, protect victims, seek repair, and let hope arrive without silencing lament.",
        ),
        "Creation-To-Consciousness Pattern": (
            PATTERN_PROFILES["Creation-To-Consciousness Pattern"]["movement"],
            PATTERN_PROFILES["Creation-To-Consciousness Pattern"]["thesis"],
            "It is strongest when creation texts, ecology, disability theology, philosophy of mind, and science guardrails are held together.",
            "It weakens if science becomes proof, consciousness becomes superiority, animal suffering is ignored, or disabled people are treated as lesser images of God.",
            "The faithful response is wonder without domination: care for bodies, honor creaturely limits, protect creation, and worship without contempt for weakness.",
        ),
        "Trinity-As-Behavior Pattern": (
            PATTERN_PROFILES["Trinity-As-Behavior Pattern"]["movement"],
            PATTERN_PROFILES["Trinity-As-Behavior Pattern"]["thesis"],
            "It is strongest when Scripture, creeds, worship, global church testimony, and abuse safeguards all remain visible.",
            "It fails if Father, Son, and Spirit become vague symbols, group energy, three separate gods, or a tool for spiritual control.",
            "The faithful response is accountable love: test every practice by holiness, humility, justice, unity, service, and fruit over time.",
        ),
        "Providence And Contingency Pattern": (
            PATTERN_PROFILES["Providence And Contingency Pattern"]["movement"],
            PATTERN_PROFILES["Providence And Contingency Pattern"]["thesis"],
            "It is strongest when Job, Ecclesiastes, exile, migration, probability, history, and public suffering are allowed to complicate easy explanations.",
            "It weakens when tragedy is explained too neatly, victims are blamed, chance is denied, or quantum language is used as a shortcut to divine action.",
            "The faithful response is humble action: pray, plan, serve, grieve, repent, and act faithfully without pretending to know every reason.",
        ),
    }
    return sections[name]


def bulletize(lines: list[str]) -> list[str]:
    return [f"- {line}" for line in lines if line]


def format_counts(counts: dict, limit: int = 6) -> str:
    if not counts:
        return "none recorded"
    items = sorted(counts.items(), key=lambda item: (-int(item[1] or 0), item[0]))[:limit]
    return ", ".join(f"{name}: {int(count):,}" for name, count in items)


def latest_cloud_discovery_lines(digest: dict, reference_catalog: dict) -> list[str]:
    source_count = reference_catalog.get("source_count")
    if source_count is None:
        source_count = len(reference_catalog.get("sources", []))

    search_strategy = digest.get("search_strategy", {})
    lines = [
        f"Retained cloud candidate references: {int(source_count or 0):,}",
        f"Brand-new candidate references this run: {int(digest.get('new_count', 0) or 0):,}",
        f"New provider mix: {format_counts(digest.get('new_provider_counts', {}))}",
        f"New routed layers: {format_counts(digest.get('new_layer_counts', {}))}",
        f"Media candidates this run: {format_counts(digest.get('new_media_candidate_counts', {}))}",
    ]

    if search_strategy:
        run_index = search_strategy.get("discovery_run_index")
        page_window = search_strategy.get("discovery_window_pages")
        if run_index or page_window:
            lines.append(
                f"Discovery pagination: run index {run_index or 'not recorded'} across {page_window or 'unknown'} page window(s)"
            )

    updated_at = digest.get("updated_at")
    if updated_at:
        lines.append(f"Latest collector update: {updated_at}")

    return lines


def newest_source_lines(digest: dict, limit: int = 5) -> list[str]:
    sources = digest.get("new_sources", [])
    if not sources:
        return ["- No brand-new sources were added in the latest collector run."]

    lines = []
    for source in sources[:limit]:
        tags = ", ".join(source.get("tags", [])) or "untagged"
        routes = ", ".join(source.get("layer_routes", [])) or "unrouted"
        media = source.get("media_kind")
        media_note = f"; media: {media}" if media else ""
        lines.append(
            f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'}) | {source.get('provider', 'unknown provider')} | tags: {tags} | routes: {routes}{media_note}"
        )
    return lines


def friction_layer_lines(records: list[dict]) -> list[str]:
    if not records:
        return ["- No friction layer records have been added yet."]

    lines = []
    for record in records:
        tags = ", ".join(record.get("tags", [])) or "untagged"
        related_layers = ", ".join(record.get("related_layers", [])) or "not linked yet"
        score = record.get("evidence_score", "unrated")
        lines.extend(
            [
                f"### {record.get('title', 'Untitled Friction Record')}",
                "",
                f"**Evidence Score:** {score}",
                "",
                f"**Evidence Effect:** {record.get('evidence_effect', 'unrated')}",
                "",
                f"**Evidence Value:** {record.get('evidence_value', 'unrated')}",
                "",
                f"**Insight Value:** {record.get('insight_value', 'unrated')}",
                "",
                f"**Confidence:** {record.get('confidence', 'unrated')}",
                "",
                f"**Review Status:** {record.get('review_status', 'unreviewed')}",
                "",
                f"**Resolution Status:** {record.get('resolution_status', 'unrated')}",
                "",
                f"**Domain:** {record.get('domain', 'Unspecified')}",
                "",
                f"**Observation:** {record.get('observation', '')}",
                "",
                f"**Pattern:** {record.get('pattern', '')}",
                "",
                f"**Distortion:** {record.get('distortion', '')}",
                "",
                f"**Friction Point:** {record.get('friction_point', '')}",
                "",
                f"**Alternative Explanations:** {', '.join(record.get('alternative_explanations', []))}",
                "",
                f"**Non-Christian Resolution:** {record.get('non_christian_resolution', '')}",
                "",
                f"**Christian Resolution:** {record.get('christian_resolution', '')}",
                "",
                f"**Transformation Result:** {record.get('transformation_result', '')}",
                "",
                f"**Divine Pattern Insight:** {record.get('divine_pattern_insight', '')}",
                "",
                f"**Failure Risk:** {record.get('failure_risk', '')}",
                "",
                f"**Source Review Note:** {record.get('source_review_note', '')}",
                "",
                f"**Related Layers:** {related_layers}",
                "",
                f"**Tags:** {tags}",
                "",
            ]
        )
    return lines


def theological_foundations_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Theological foundations layer is missing."]

    lines = [
        f"**Mission:** {layer.get('mission_statement', '')}",
        "",
        f"**Authority boundary:** {layer.get('authority_boundary', '')}",
        "",
        "Principles:",
    ]
    lines.extend(f"- {item}" for item in layer.get("principles", []))
    definitions = layer.get("definitions", {})
    lines.extend(["", "Definitions:"])
    for name, definition in definitions.items():
        lines.append(f"- **{name}:** {definition}")
    lines.extend(["", "Interpretive order:"])
    lines.extend(f"- {item}" for item in layer.get("interpretive_order", []))
    return lines


def architecture_lines(layer: dict) -> list[str]:
    architecture = layer.get("architecture", {}) if layer else {}
    if not architecture:
        return ["Project architecture layer is missing."]

    lines = []
    for heading, items in architecture.items():
        lines.extend([f"### {heading}", ""])
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    return lines


def distortion_layer_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No pattern distortion records yet."]

    lines = [layer.get("purpose", ""), ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('original_pattern', 'Pattern')} -> {record.get('distortion', 'Distortion')}",
                "",
                f"**Cause:** {record.get('cause', '')}",
                "",
                f"**Consequences:** {record.get('consequences', '')}",
                "",
                f"**Biblical Examples:** {', '.join(record.get('biblical_examples', []))}",
                "",
                f"**Restoration Path:** {record.get('restoration_path', '')}",
                "",
            ]
        )
    return lines


def christological_layer_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No Christological records yet."]

    lines = [layer.get("purpose", ""), f"Core status: {layer.get('core_status', 'unrated')}", ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('pattern_name', 'Pattern')}",
                "",
                f"**Appearance In Creation:** {record.get('appearance_in_creation', '')}",
                "",
                f"**Appearance In Humanity:** {record.get('appearance_in_humanity', '')}",
                "",
                f"**Distortion:** {record.get('distortion', '')}",
                "",
                f"**Fulfillment In Christ:** {record.get('fulfillment_in_christ', '')}",
                "",
                f"**Restoration Through Christ:** {record.get('restoration_through_christ', '')}",
                "",
                f"**Supporting Scriptures:** {', '.join(record.get('supporting_scriptures', []))}",
                "",
            ]
        )
    return lines


def historical_witness_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No historical witnesses yet."]

    lines = [layer.get("purpose", ""), ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('name', 'Witness')}",
                "",
                f"**Era:** {record.get('era', '')}",
                "",
                f"**Key Themes:** {', '.join(record.get('key_themes', []))}",
                "",
                f"**Relevant Patterns:** {', '.join(record.get('relevant_patterns', []))}",
                "",
                f"**Agreements:** {record.get('agreements', '')}",
                "",
                f"**Disagreements:** {record.get('disagreements', '')}",
                "",
                f"**Citations:** {', '.join(record.get('citations', []))}",
                "",
            ]
        )
    return lines


def mystery_layer_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No mystery records yet."]

    lines = [layer.get("purpose", ""), f"Categories: {', '.join(layer.get('categories', []))}", ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('topic', 'Mystery')}",
                "",
                f"**Category:** {record.get('category', '')}",
                "",
                f"**What Can Be Known:** {record.get('what_can_be_known', '')}",
                "",
                f"**What Remains Mysterious:** {record.get('what_remains_mysterious', '')}",
                "",
                f"**Supporting Scriptures:** {', '.join(record.get('supporting_scriptures', []))}",
                "",
                f"**Theological Notes:** {record.get('theological_notes', '')}",
                "",
            ]
        )
    return lines


def friction_summary_lines(records: list[dict]) -> list[str]:
    if not records:
        return ["No rated friction records yet."]

    rated = [record for record in records if isinstance(record.get("evidence_score"), int)]
    supportive = sum(1 for record in rated if record["evidence_score"] > 0)
    diagnostic = sum(1 for record in rated if record["evidence_score"] == 0)
    challenging = sum(1 for record in rated if record["evidence_score"] < 0)
    total_score = sum(record["evidence_score"] for record in rated)
    total_insight = sum(record.get("insight_value", 0) for record in records)
    return [
        f"Rated records: {len(rated)}",
        f"Supportive after caution/resolution: {supportive}",
        f"Diagnostic or unresolved friction: {diagnostic}",
        f"Currently weakening or unresolved challenge records: {challenging}",
        f"Net provisional evidence score: {total_score}",
        f"Total insight value: {total_insight}",
    ]


def friction_domain_rollup_lines(records: list[dict]) -> list[str]:
    if not records:
        return ["No domains recorded yet."]

    rollups: dict[str, dict[str, int]] = {}
    for record in records:
        domain = record.get("domain", "Unspecified").split("↔")[0].strip()
        rollup = rollups.setdefault(domain, {"count": 0, "evidence": 0, "insight": 0})
        rollup["count"] += 1
        rollup["evidence"] += int(record.get("evidence_value", record.get("evidence_score", 0)) or 0)
        rollup["insight"] += int(record.get("insight_value", 0) or 0)

    return [
        f"{domain}: {values['count']} record(s), evidence {values['evidence']}, insight {values['insight']}"
        for domain, values in sorted(rollups.items())
    ]


def friction_resolution_rollup_lines(records: list[dict]) -> list[str]:
    if not records:
        return ["No resolution statuses recorded yet."]

    counts: dict[str, int] = {}
    for record in records:
        status = record.get("resolution_status", "unrated")
        counts[status] = counts.get(status, 0) + 1
    return [f"{status}: {count}" for status, count in sorted(counts.items())]


def build_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    texts = {name: read(path) for name, path in SOURCE_REPORTS.items()}
    digest = read_json(DAILY_DIGEST_PATH)
    reference_catalog = read_json(REFERENCES_PATH)
    knowledge_index = read_json(KNOWLEDGE_INDEX_PATH)
    candidate_pattern = current_candidate_pattern(knowledge_index)
    stats = extract_backend_stats(texts["backend"])
    lane_lines = compact_lane_table(texts["backend"])
    friction_layers = read_friction_layers()
    theological_foundations = read_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    pattern_distortion = read_layer(PATTERN_DISTORTION_PATH)
    christological_layer = read_layer(CHRISTOLOGICAL_LAYER_PATH)
    historical_witnesses = read_layer(HISTORICAL_WITNESSES_PATH)
    mystery_layer = read_layer(MYSTERY_LAYER_PATH)
    project_architecture = read_layer(PROJECT_ARCHITECTURE_PATH)

    lines = [
        "# Divine Pattern Research",
        "",
        "## A Book Report For Careful Readers",
        "",
        f"_Generated: {generated}_",
        "",
        "This is the version to read on GitHub. The project still generates detailed machine reports in the background, but this article is the synthesized reading report: what the evidence seems to be saying, what must stay provisional, and what kind of faithful response is being invited.",
        "",
        "The short version: the research does not claim that patterns prove Christianity. It explores recurring patterns in reality and examines how those patterns align with, illuminate, challenge, or are explained by the Christian understanding of God, creation, sin, redemption, and restoration.",
        "",
        "Patterns are treated as evidence, observations, and hypotheses to be tested, not as independent sources of divine authority.",
        "",
        "## Theological Foundations",
        "",
        *theological_foundations_lines(theological_foundations),
        "",
        "## Project Architecture",
        "",
        *architecture_lines(project_architecture),
        "",
        "## Pattern Found So Far",
        "",
        f"**Current candidate divine pattern:** {candidate_pattern['candidate']}",
        "",
        "The clearest movement currently looks like this:",
        "",
        f"- {candidate_pattern['movement']}",
        "",
        f"Selection note: {candidate_pattern['basis']} This can change when future analyzed references shift the strongest reviewed pattern family or show that an integrated pattern is more honest.",
        "",
        "## What Changed",
        "",
        "The project now has three layers working together:",
        "",
        "- A source corpus: biblical languages, world languages, theologians, history, comparative texts, pressure tests, and science guardrails.",
        "- A knowledge backend: retrieval index, knowledge graph, and review-rule audit.",
        "- A public reading layer: this article, which should be read instead of the raw report dump.",
        "",
        "The backend is useful, but it is not the judge. It retrieves and organizes. Human review still decides whether a source should affect confidence.",
        "",
        "## Current Corpus At A Glance",
        "",
        "### Latest Cloud Discovery",
        "",
        *bulletize(latest_cloud_discovery_lines(digest, reference_catalog)),
        "",
        "Newest cloud candidates:",
        "",
        *newest_source_lines(digest),
        "",
        "### Local Reviewed Corpus",
        "",
        *bulletize([stats["indexed"], stats["nodes"], stats["edges"]]),
        *bulletize([stats["text_documents"], stats["media_assets"], stats["multimodal_review"]]),
        "",
        "The strongest reviewed-note weight currently sits in these lanes:",
        "",
        *bulletize(lane_lines[:7]),
        "",
        "This balance matters. A theological claim cannot grow simply because one lane is loud. It needs original-language depth, global translation awareness, theological disagreement, historical pressure, comparative humility, and practical fruit.",
        "",
        "## The Main Thesis",
        "",
        "The project is testing whether Christian theology can responsibly name recurring patterns across Scripture, language, history, culture, suffering, science, and practice. But the word responsibly is doing heavy work.",
        "",
        "A repeated signal is not proof. A beautiful analogy is not revelation. A scientific idea is not a sermon. A theological claim is not mature until it can face grief, injustice, rival explanations, and the question of what love requires today.",
        "",
        "## Pattern Distortion Layer",
        "",
        *distortion_layer_lines(pattern_distortion),
        "## Christological Layer",
        "",
        *christological_layer_lines(christological_layer),
        "## Historical Witnesses",
        "",
        *historical_witness_lines(historical_witnesses),
        "## Mystery Layer",
        "",
        *mystery_layer_lines(mystery_layer),
        "## The Five Leading Pattern Families",
        "",
    ]

    for name in TOP_PATTERN_NAMES:
        movement, thesis, why, risk, response = pattern_section(name)
        lines.extend(
            [
                f"### {name}",
                "",
                f"**Pattern movement:** {movement}",
                "",
                f"**What it says:** {thesis}",
                "",
                f"**Why it matters:** {why}",
                "",
                f"**What would weaken it:** {risk}",
                "",
                f"**Practical response:** {response}",
                "",
            ]
        )

    lines.extend(
        [
            "## Quantum Theory Belongs In The Guardrail Lane",
            "",
            "The new quantum material is useful, but only if it stays disciplined. Quantum theory can teach humility about measurement, probability, uncertainty, and interpretation. It should not be used as proof of God, prayer, consciousness, providence, miracles, or mystical connection.",
            "",
            "The project should treat quantum language as a warning label against overclaiming. If a sentence uses quantum theory to make theology easier than the physics allows, the sentence should be weakened or rewritten.",
            "",
            "## What Still Needs Caution",
            "",
            "- Comparative religion can reveal shared human longing, ritual, wisdom, and moral practice, but it must not flatten real doctrinal differences.",
            "- Theologian sources add depth, but theologians disagree. A famous name is not a settled claim.",
            "- History gives pressure, not decoration. Power, harm, memory, reform, and unfinished repair must stay visible.",
            "- Psychology and sociology can explain many repeated patterns without requiring divine-pattern interpretation.",
            "- Machine labels can route attention, but they cannot settle truth.",
            "",
            "## Friction Layer",
            "",
            "Friction is not evidence of failure. Friction is evidence that a pattern has reached the limits of its current explanatory framework and is seeking a deeper resolution.",
            "",
            "This layer records where philosophy, science, culture, or theology creates productive tension with the Divine Pattern framework. The goal is not to erase the tension, but to preserve it carefully enough that a deeper resolution can be tested.",
            "",
            "### Provisional Evidence Summary",
            "",
            *bulletize(friction_summary_lines(friction_layers)),
            "",
            "Scale: -2 weakens the claim; -1 creates a serious unresolved challenge; 0 is diagnostic friction; 1 gives modest support with caution; 2 gives moderate support after Christian resolution.",
            "",
            "### Domain Rollup",
            "",
            *bulletize(friction_domain_rollup_lines(friction_layers)),
            "",
            "### Resolution Status Rollup",
            "",
            *bulletize(friction_resolution_rollup_lines(friction_layers)),
            "",
            *friction_layer_lines(friction_layers),
            "## What Would Make The Project Better",
            "",
            "The next growth should not be more volume for its own sake. It should be better review. The strongest next work is to keep building source packs for major claims, add counter-readings from serious rivals, and make every practical claim answer the same question: does this help people become more truthful, loving, humble, just, worshipful, patient, and faithful?",
            "",
            "## Final Judgment",
            "",
            "This project is no longer just collecting patterns. It is beginning to develop judgment. That is the important change.",
            "",
            "The best version of the report does not say, 'Look how many signals we found.' It says, 'Here is what the sources may support, here is what they do not support, here is where the claim could fail, and here is the faithful response being invited today.'",
            "",
            "That is the article worth reading.",
            "",
            "## Source Reports Used In The Background",
            "",
            "The following generated reports were read as source material for this synthesis. They are build inputs, not the preferred reading experience:",
            "",
        ]
    )

    for name, path in SOURCE_REPORTS.items():
        status = "available" if path.exists() else "missing"
        lines.append(f"- `{path.as_posix()}` ({status})")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_article(), encoding="utf-8")
    print(f"Published article saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
