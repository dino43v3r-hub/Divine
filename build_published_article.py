from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/published/final_book_report.md")
DAILY_IMAGE_PATH = Path("reports/published/daily_pattern_image.svg")
REFERENCES_PATH = Path("references/references.json")
DAILY_DIGEST_PATH = Path("references/daily_research_digest.json")
KNOWLEDGE_INDEX_PATH = Path("reports/knowledge_retrieval_index.json")
REVIEW_AUDIT_PATH = Path("reports/review_rules_audit.json")
FRICTION_LAYERS_PATH = Path("research_documents/friction_layers.json")
THEOLOGICAL_FOUNDATIONS_PATH = Path("research_documents/theological_foundations.json")
PATTERN_DISTORTION_PATH = Path("research_documents/pattern_distortion_layer.json")
CHRISTOLOGICAL_LAYER_PATH = Path("research_documents/christological_layer.json")
HISTORICAL_WITNESSES_PATH = Path("research_documents/historical_witnesses.json")
MYSTERY_LAYER_PATH = Path("research_documents/mystery_layer.json")
PROJECT_ARCHITECTURE_PATH = Path("research_documents/project_architecture.json")
THEOLOGICAL_METHOD_PATH = Path("research_documents/theological_method_guardrails.json")
CREEDAL_GUARDRAILS_PATH = Path("research_documents/creedal_guardrails.json")
NEGATIVE_CASES_PATH = Path("research_documents/negative_case_records.json")
ETHICAL_HARM_AUDIT_PATH = Path("research_documents/ethical_harm_audit.json")
PRIESTLY_DISCERNMENT_PATH = Path("research_documents/priestly_discernment_layer.json")
SOURCE_REVIEW_STATUS_PATH = Path("research_documents/source_review_status.json")
CLAIM_LEDGER_CONNECTIONS_PATH = Path("research_documents/claim_ledger_connections.json")
TRADITION_LABELS_PATH = Path("research_documents/tradition_claim_labels.json")
DOES_NOT_PROVE_PATH = Path("research_documents/does_not_prove_boundaries.json")
SCIENCE_GUARDRAIL_PATH = Path("research_documents/science_guardrail_layer.json")

SOURCE_REPORTS = {
    "findings": Path("reports/divine_pattern_findings.md"),
    "gap_queue": Path("reports/review_gap_queue.md"),
    "backend": Path("reports/ai_backend_report.txt"),
    "summary": Path("reports/divine_pattern_summary_report.txt"),
    "top_patterns": Path("reports/top_five_divine_patterns_report.txt"),
    "tests": Path("reports/divine_pattern_test_report.txt"),
    "deep": Path("reports/deep_source_review_report.txt"),
    "theologians": Path("reports/theologian_pattern_design_report.txt"),
    "reader": Path("reports/divine_pattern_reader_book.txt"),
}

EXCLUDED_REPORTS = {
    "combined_summary_report": {
        "path": Path("reports/combined_summary_report.txt"),
        "reason": "Appears to belong to the disk-cleanup/compiler workflow, so it is excluded from Divine Pattern synthesis.",
    },
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

VISUAL_PROFILES = {
    "Image Of God Pattern": {
        "title": "Image of God",
        "motif": "Dignity before usefulness",
        "colors": ("#f7efe5", "#224c55", "#d18f46", "#7c3f58", "#e0c35a"),
        "nodes": ["Mind", "Symbol", "Agency", "Relation", "Worship"],
    },
    "Cross And Reversal Pattern": {
        "title": "Cross and Reversal",
        "motif": "Power judged by mercy",
        "colors": ("#f2f0ec", "#2d3348", "#8f2d3f", "#d0a44c", "#5f8f70"),
        "nodes": ["Power", "Humility", "Truth", "Mercy", "Hope"],
    },
    "Creation-To-Consciousness Pattern": {
        "title": "Creation to Consciousness",
        "motif": "Order becoming responsibility",
        "colors": ("#eef3ed", "#243b2f", "#6e9a74", "#c47a43", "#416a8b"),
        "nodes": ["Order", "Life", "Mind", "Moral", "Worship"],
    },
    "Trinity-As-Behavior Pattern": {
        "title": "Trinity as Behavior",
        "motif": "Gift, redemption, transformation",
        "colors": ("#f4f1f8", "#28334d", "#b56b45", "#4f7d73", "#d7b957"),
        "nodes": ["Father", "Son", "Spirit", "Fruit", "Service"],
    },
    "Providence And Contingency Pattern": {
        "title": "Providence and Contingency",
        "motif": "Faithfulness inside uncertainty",
        "colors": ("#eef4f7", "#253949", "#4d7890", "#c88a4a", "#8a5a83"),
        "nodes": ["Law", "Chance", "Complexity", "History", "Trust"],
    },
}

DEFAULT_VISUAL_PROFILE = {
    "title": "Gift and Faithfulness",
    "motif": "Pattern with limits attached",
    "colors": ("#f2f0e8", "#263d3f", "#ad6f43", "#5c7893", "#8d4d62"),
    "nodes": ["Gift", "Notice", "Discern", "Repair", "Worship"],
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


def wrap_words(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    return lines[:max_lines]


def daily_visual_profile(candidate_pattern: dict, generated: datetime) -> dict:
    name = candidate_pattern.get("name", "")
    profile = dict(VISUAL_PROFILES.get(name, DEFAULT_VISUAL_PROFILE))
    daily_shift = generated.date().toordinal() % 5
    nodes = profile["nodes"]
    profile["nodes"] = nodes[daily_shift:] + nodes[:daily_shift]
    return profile


def generate_daily_pattern_image(candidate_pattern: dict, digest: dict, audit: dict, generated: datetime) -> Path:
    profile = daily_visual_profile(candidate_pattern, generated)
    bg, ink, warm, cool, gold = profile["colors"]
    date_label = generated.strftime("%B %d, %Y")
    lead_title = profile["title"]
    motif = profile["motif"]
    candidate_lines = wrap_words(candidate_pattern.get("candidate", ""), 74, 3)
    new_count = int(digest.get("new_count", 0) or 0)
    totals = audit.get("confidence_tier_totals", {}) if audit else {}
    developing = int(totals.get("developing_evidence", 0) or 0)
    candidate_leads = int(totals.get("candidate_lead", 0) or 0)

    node_x = [146, 322, 498, 674, 850]
    node_y = [352, 286, 352, 286, 352]
    nodes = []
    lines = []
    for index, label in enumerate(profile["nodes"]):
        x = node_x[index]
        y = node_y[index]
        color = [warm, cool, gold, warm, cool][index]
        nodes.append(
            f'<circle cx="{x}" cy="{y}" r="50" fill="{color}" opacity="0.94"/>'
            f'<circle cx="{x}" cy="{y}" r="62" fill="none" stroke="{ink}" stroke-width="2" opacity="0.25"/>'
            f'<text x="{x}" y="{y + 6}" text-anchor="middle" class="node">{escape(label)}</text>'
        )
        if index:
            lines.append(
                f'<line x1="{node_x[index - 1] + 54}" y1="{node_y[index - 1]}" '
                f'x2="{x - 54}" y2="{y}" stroke="{ink}" stroke-width="4" opacity="0.28"/>'
            )

    quote_lines = []
    for index, line in enumerate(candidate_lines):
        quote_lines.append(
            f'<text x="96" y="{158 + index * 28}" class="body">{escape(line)}</text>'
        )

    variant = generated.date().toordinal() % 3
    if variant == 0:
        background_shape = f'<circle cx="880" cy="108" r="122" fill="{gold}" opacity="0.34"/>'
    elif variant == 1:
        background_shape = f'<path d="M805 42 L940 120 L872 228 L738 150 Z" fill="{gold}" opacity="0.33"/>'
    else:
        background_shape = f'<rect x="748" y="46" width="178" height="178" rx="14" fill="{gold}" opacity="0.31"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="520" viewBox="0 0 1000 520" role="img" aria-labelledby="title desc">
  <title id="title">Daily Divine Pattern Image: {escape(lead_title)}</title>
  <desc id="desc">A daily visual summary connected to the current Divine Pattern findings.</desc>
  <style>
    .eyebrow {{ font: 700 15px Arial, sans-serif; letter-spacing: 0; fill: {ink}; opacity: 0.72; }}
    .title {{ font: 700 45px Georgia, serif; letter-spacing: 0; fill: {ink}; }}
    .subtitle {{ font: 700 22px Arial, sans-serif; letter-spacing: 0; fill: {warm}; }}
    .body {{ font: 18px Arial, sans-serif; letter-spacing: 0; fill: {ink}; }}
    .small {{ font: 15px Arial, sans-serif; letter-spacing: 0; fill: {ink}; opacity: 0.78; }}
    .node {{ font: 700 16px Arial, sans-serif; letter-spacing: 0; fill: #ffffff; }}
  </style>
  <rect width="1000" height="520" fill="{bg}"/>
  <rect x="38" y="34" width="924" height="452" rx="22" fill="#ffffff" opacity="0.50"/>
  {background_shape}
  <path d="M72 420 C190 388 288 452 406 418 C530 382 620 452 746 416 C828 392 884 400 928 424" fill="none" stroke="{cool}" stroke-width="9" opacity="0.18"/>
  <text x="72" y="82" class="eyebrow">Daily pattern image | {escape(date_label)}</text>
  <text x="72" y="132" class="title">{escape(lead_title)}</text>
  <text x="72" y="246" class="subtitle">{escape(motif)}</text>
  {''.join(quote_lines)}
  {''.join(lines)}
  {''.join(nodes)}
  <rect x="72" y="434" width="856" height="34" rx="17" fill="{ink}" opacity="0.08"/>
  <text x="96" y="456" class="small">New leads: {new_count} | Developing evidence: {developing} | Candidate leads: {candidate_leads} | Generated from current findings</text>
</svg>
'''
    DAILY_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    DAILY_IMAGE_PATH.write_text(svg, encoding="utf-8")
    return DAILY_IMAGE_PATH


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


def confidence_tier_lines(audit: dict) -> list[str]:
    totals = audit.get("confidence_tier_totals", {}) if audit else {}
    if not totals:
        return ["- Confidence tiers have not been generated yet. Run `python ai_knowledge_backend.py`."]
    labels = {
        "reviewed_evidence_ready": "ready for human confidence review",
        "developing_evidence": "developing evidence",
        "candidate_lead": "candidate lead only",
        "media_pending_review": "media pending review",
    }
    return [
        f"- {labels.get(tier, tier)}: {int(count):,}"
        for tier, count in sorted(totals.items())
    ]


def rule_coverage_lines(audit: dict) -> list[str]:
    coverage = audit.get("rule_coverage", {}) if audit else {}
    if not coverage:
        return ["- Promotion-rule coverage has not been generated yet."]
    priority = [
        "interpretation",
        "analogy",
        "failure_condition",
        "machine_label_boundary",
        "discernment",
        "evidence",
        "counter_reading",
        "practical_use",
    ]
    lines = []
    for rule in priority:
        values = coverage.get(rule)
        if not values:
            continue
        lines.append(
            f"- {rule}: {int(values.get('present', 0)):,} explicit; {int(values.get('machine_drafted', 0)):,} machine-drafted; {int(values.get('missing', 0)):,} still missing of {int(values.get('total', 0)):,}"
        )
    return lines or ["- No promotion-rule coverage values found."]


def excluded_report_lines() -> list[str]:
    lines = []
    for item in EXCLUDED_REPORTS.values():
        path = item["path"]
        status = "present and excluded" if path.exists() else "not present"
        lines.append(f"- `{path.as_posix()}` ({status}): {item['reason']}")
    return lines


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
                f"**Source Review Stage:** {record.get('source_review_stage', '')}",
                "",
                f"**Primary Source Review:** {record.get('primary_source_review', '')}",
                "",
                f"**Counter-Reading Status:** {record.get('counter_reading_status', '')}",
                "",
                f"**Confidence Review Ready:** {record.get('confidence_review_ready', '')}",
                "",
                f"**Resolution Status:** {record.get('resolution_status', 'unrated')}",
                "",
                f"**Claim Classification:** {record.get('claim_classification', '')}",
                "",
                f"**Domain:** {record.get('domain', 'Unspecified')}",
                "",
                f"**Observation:** {record.get('observation', '')}",
                "",
                f"**Pattern:** {record.get('pattern', '')}",
                "",
                f"**Scripture Anchor:** {', '.join(record.get('scripture_anchor', []))}",
                "",
                f"**Interpretive Status:** {record.get('interpretive_status', '')}",
                "",
                f"**Canonical Context:** {record.get('canonical_context', '')}",
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
                f"**Theological Caution:** {record.get('theological_caution', '')}",
                "",
                f"**Harm Audit:** {record.get('harm_audit', '')}",
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
    checks = layer.get("required_claim_checks", [])
    if checks:
        lines.extend(["", "Required claim checks:"])
        lines.extend(f"- {item}" for item in checks)
    return lines


def theological_method_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Theological method guardrails layer is missing."]

    lines = [
        layer.get("purpose", ""),
        "",
        f"**Core Rule:** {layer.get('core_rule', '')}",
        "",
        "Evidence categories:",
    ]
    for item in layer.get("evidence_categories", []):
        lines.extend(
            [
                f"### {item.get('category', 'Category')}",
                "",
                f"**Question:** {item.get('question', '')}",
                "",
                f"**Required Action:** {item.get('required_action', '')}",
                "",
            ]
        )
    lines.extend(["Confidence rules:"])
    lines.extend(f"- {item}" for item in layer.get("confidence_rules", []))
    lines.extend(["", "Scoring interpretation:"])
    for score, meaning in layer.get("scoring_interpretation", {}).items():
        lines.append(f"- **{score}:** {meaning}")
    lines.extend(["", "Required record fields:"])
    lines.extend(f"- {item}" for item in layer.get("required_record_fields", []))
    return lines


def creedal_guardrail_lines(layer: dict) -> list[str]:
    records = layer.get("core_commitments", []) if layer else []
    if not records:
        return ["Creedal guardrails layer is missing."]

    lines = [layer.get("purpose", ""), ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('doctrine', 'Doctrine')}",
                "",
                f"**Guardrail:** {record.get('guardrail', '')}",
                "",
                f"**Sources:** {', '.join(record.get('sources', []))}",
                "",
            ]
        )
    lines.extend(["Rejection rules:"])
    lines.extend(f"- {item}" for item in layer.get("rejection_rules", []))
    return lines


def negative_case_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No negative case records yet."]

    lines = [layer.get("purpose", ""), "", f"**Use Rule:** {layer.get('use_rule', '')}", ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('title', 'Negative Case')}",
                "",
                f"**Pattern Claim Under Test:** {record.get('pattern_claim_under_test', '')}",
                "",
                f"**Why It Fails Or Weakens:** {record.get('why_it_fails_or_weakens', '')}",
                "",
                f"**Theological Boundary:** {record.get('theological_boundary', '')}",
                "",
                f"**Scripture Anchor:** {', '.join(record.get('scripture_anchor', []))}",
                "",
                f"**Required Revision:** {record.get('required_revision', '')}",
                "",
                f"**Pastoral Warning:** {record.get('pastoral_warning', '')}",
                "",
            ]
        )
    return lines


def ethical_harm_audit_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Ethical harm audit layer is missing."]

    lines = [layer.get("purpose", ""), "", "Audit questions:"]
    lines.extend(f"- {item}" for item in layer.get("audit_questions", []))
    lines.extend(["", "Downgrade triggers:"])
    lines.extend(f"- {item}" for item in layer.get("downgrade_triggers", []))
    lines.extend(["", f"Required fruit: {', '.join(layer.get('required_fruit', []))}"])
    return lines


def priestly_discernment_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Priestly discernment layer is missing."]

    lines = [
        layer.get("purpose", ""),
        "",
        f"**Core Rule:** {layer.get('core_rule', '')}",
        "",
        "Review questions:",
    ]
    lines.extend(f"- {item}" for item in layer.get("review_questions", []))
    lines.extend(["", "Promotion restraints:"])
    lines.extend(f"- {item}" for item in layer.get("promotion_restraints", []))
    lines.extend(["", "Liturgical and sacramental tests:"])
    lines.extend(f"- {item}" for item in layer.get("liturgical_and_sacramental_tests", []))
    lines.extend(["", f"Required fruit: {', '.join(layer.get('required_fruit', []))}"])
    return lines


def source_review_status_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No source review status records yet."]

    lines = [layer.get("purpose", ""), "", f"**Promotion Rule:** {layer.get('promotion_rule', '')}", ""]
    lines.extend(["Status order:"])
    lines.extend(f"- {item}" for item in layer.get("status_order", []))
    lines.append("")
    for record in records:
        lines.extend(
            [
                f"### {record.get('target_id', 'Target')}",
                "",
                f"**Target Type:** {record.get('target_type', '')}",
                "",
                f"**Current Status:** {record.get('current_status', '')}",
                "",
                f"**Next Review Step:** {record.get('next_review_step', '')}",
                "",
                f"**Review Note:** {record.get('review_note', '')}",
                "",
            ]
        )
    return lines


def claim_ledger_connection_lines(layer: dict) -> list[str]:
    claims = layer.get("claims", []) if layer else []
    if not claims:
        return ["No claim ledger connections yet."]

    lines = [layer.get("purpose", ""), "", f"**Connection Rule:** {layer.get('connection_rule', '')}", ""]
    for claim in claims:
        lines.extend(
            [
                f"### {claim.get('id', 'Claim')}",
                "",
                f"**Claim:** {claim.get('claim', '')}",
                "",
                f"**Tradition Label:** {claim.get('tradition_label', '')}",
                "",
                f"**Scripture Anchor:** {', '.join(claim.get('scripture_anchor', []))}",
                "",
                f"**Evidence Links:** {', '.join(claim.get('evidence_links', []))}",
                "",
                f"**Friction Links:** {', '.join(claim.get('friction_links', []))}",
                "",
                f"**Confidence:** {claim.get('confidence', '')}",
                "",
                f"**What Would Weaken It:** {claim.get('what_would_weaken_it', '')}",
                "",
            ]
        )
    return lines


def tradition_label_lines(layer: dict) -> list[str]:
    labels = layer.get("labels", []) if layer else []
    if not labels:
        return ["No tradition labels yet."]

    lines = [layer.get("purpose", ""), ""]
    for label in labels:
        lines.extend(
            [
                f"### {label.get('id', 'label')}",
                "",
                f"**Meaning:** {label.get('meaning', '')}",
                "",
                f"**Examples:** {', '.join(label.get('examples', []))}",
                "",
            ]
        )
    return lines


def does_not_prove_lines(layer: dict) -> list[str]:
    boundaries = layer.get("boundaries", []) if layer else []
    if not boundaries:
        return ["No boundary records yet."]

    lines = [layer.get("purpose", ""), ""]
    for boundary in boundaries:
        lines.extend(
            [
                f"### {boundary.get('claim_limit', 'Limit')}",
                "",
                f"**Why:** {boundary.get('why', '')}",
                "",
            ]
        )
    return lines


def science_guardrail_lines(layer: dict) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No science guardrail records yet."]

    lines = [layer.get("purpose", ""), "", f"**Core Rule:** {layer.get('core_rule', '')}", ""]
    for record in records:
        lines.extend(
            [
                f"### {record.get('topic', 'Science Topic')}",
                "",
                f"**Scientific Domain:** {record.get('scientific_domain', '')}",
                "",
                f"**Guardrail:** {record.get('guardrail', '')}",
                "",
                f"**Theological Use:** {record.get('theological_use', '')}",
                "",
                f"**Misuse Risk:** {record.get('misuse_risk', '')}",
                "",
                f"**Needed Sources:** {', '.join(record.get('needed_sources', []))}",
                "",
            ]
        )
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
                f"**Tradition:** {record.get('tradition', '')}",
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
                f"**Reduction Guardrail:** {record.get('reduction_guardrail', '')}",
                "",
                f"**Research Use:** {record.get('research_use', '')}",
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
        domain = record.get("domain", "Unspecified").replace("<->", "|").split("|")[0].strip()
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
    review_audit = read_json(REVIEW_AUDIT_PATH)
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
    theological_method = read_layer(THEOLOGICAL_METHOD_PATH)
    creedal_guardrails = read_layer(CREEDAL_GUARDRAILS_PATH)
    negative_cases = read_layer(NEGATIVE_CASES_PATH)
    ethical_harm_audit = read_layer(ETHICAL_HARM_AUDIT_PATH)
    priestly_discernment = read_layer(PRIESTLY_DISCERNMENT_PATH)
    source_review_status = read_layer(SOURCE_REVIEW_STATUS_PATH)
    claim_ledger_connections = read_layer(CLAIM_LEDGER_CONNECTIONS_PATH)
    tradition_labels = read_layer(TRADITION_LABELS_PATH)
    does_not_prove = read_layer(DOES_NOT_PROVE_PATH)
    science_guardrail = read_layer(SCIENCE_GUARDRAIL_PATH)

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
        "## Theological Method And Research Guardrails",
        "",
        *theological_method_lines(theological_method),
        "",
        "## Creedal And Rule Of Faith Guardrails",
        "",
        *creedal_guardrail_lines(creedal_guardrails),
        "",
        "## Claim Ledger Connections",
        "",
        *claim_ledger_connection_lines(claim_ledger_connections),
        "",
        "## Tradition And Doctrine Labels",
        "",
        *tradition_label_lines(tradition_labels),
        "",
        "## Source Review Status",
        "",
        *source_review_status_lines(source_review_status),
        "",
        "## Evidence Tiers And Promotion Readiness",
        "",
        "The project now separates candidate leads from sources that are ready for human confidence review. These tiers are not verdicts; they are research routing labels.",
        "",
        *confidence_tier_lines(review_audit),
        "",
        "A source should not strengthen a claim until the promotion-required rules are visible and a human reviewer records a source-specific decision.",
        "",
        "Promotion-rule coverage:",
        "",
        *rule_coverage_lines(review_audit),
        "",
        "## What This Does Not Prove",
        "",
        *does_not_prove_lines(does_not_prove),
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
        "## Negative Case And Failed Pattern Records",
        "",
        *negative_case_lines(negative_cases),
        "## Pastoral And Ethical Harm Audit",
        "",
        *ethical_harm_audit_lines(ethical_harm_audit),
        "## Priestly Discernment Gate",
        "",
        *priestly_discernment_lines(priestly_discernment),
        "## Science Guardrail Layer",
        "",
        *science_guardrail_lines(science_guardrail),
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
            "- Candidate sources are useful for discovery, but they are not reviewed evidence until original-source review, rival explanation, analogy limit, failure condition, and practical-use boundary are recorded.",
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
            "The next growth should not be more volume for its own sake. It should be better review. The strongest next work is to build a gold-standard corpus, add counter-readings from serious rivals, require failure conditions for attractive claims, and make every practical claim answer the same question: does this help people become more truthful, loving, humble, just, worshipful, patient, and faithful?",
            "",
            "The project should use `research_documents/gold_standard_corpus_plan.md`, `research_documents/research_governance_workflow.md`, and `research_documents/external_review_protocol.md` as the human-review operating lane.",
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

    lines.extend(
        [
            "",
            "Excluded generated reports:",
            "",
            *excluded_report_lines(),
        ]
    )

    return "\n".join(lines) + "\n"


def build_short_article() -> str:
    generated_at = datetime.now(timezone.utc)
    generated = generated_at.strftime("%Y-%m-%d %H:%M UTC")
    digest = read_json(DAILY_DIGEST_PATH)
    reference_catalog = read_json(REFERENCES_PATH)
    knowledge_index = read_json(KNOWLEDGE_INDEX_PATH)
    review_audit = read_json(REVIEW_AUDIT_PATH)
    candidate_pattern = current_candidate_pattern(knowledge_index)
    daily_image = generate_daily_pattern_image(candidate_pattern, digest, review_audit, generated_at)
    findings_text = read(Path("reports/divine_pattern_findings.md"))
    friction_layers = read_friction_layers()
    theological_foundations = read_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    priestly_discernment = read_layer(PRIESTLY_DISCERNMENT_PATH)
    does_not_prove = read_layer(DOES_NOT_PROVE_PATH)
    science_guardrail = read_layer(SCIENCE_GUARDRAIL_PATH)

    finding_lines = []
    for line in findings_text.splitlines():
        if line.startswith("### "):
            finding_lines.append(line.replace("### ", "- "))
        if len(finding_lines) >= 7:
            break

    foundation_lines = theological_foundations_lines(theological_foundations)
    boundary_lines = does_not_prove_lines(does_not_prove)
    science_lines = science_guardrail_lines(science_guardrail)

    lines = [
        "# Divine Pattern Research",
        "",
        "## Short Book Report",
        "",
        f"_Generated: {generated}_",
        "",
        "This is the compact reading version. It tells you what the project currently sees, how strong the evidence is, what not to overclaim, and where to look next.",
        "",
        "This report is meant to change day to day. When the collector discovers new sources and the backend re-indexes them, the pattern findings and evidence mix can change with the new material.",
        "",
        f"![Daily pattern image]({daily_image.name})",
        "",
        f"_Daily visual generated from the current leading finding: {candidate_pattern['name']}._",
        "",
        "## Short Answer",
        "",
        "The project does not claim that patterns prove Christianity. It finds recurring patterns across theology, culture, language, suffering, science, art, music, history, and human experience, then asks whether those patterns can be responsibly read through Christian theology.",
        "",
        "The best current posture is: the system finds and explains divine-pattern signals; you evaluate whether they seem true, faithful, useful, or weak.",
        "",
        "## Current Pattern Found",
        "",
        f"**Current candidate divine pattern:** {candidate_pattern['candidate']}",
        "",
        f"**Movement:** {candidate_pattern['movement']}",
        "",
        f"**Selection note:** {candidate_pattern['basis']}",
        "",
        "## Main Divine Patterns Found",
        "",
        *(finding_lines or ["- No pattern findings report has been generated yet."]),
        "",
        "Read the focused pattern report here:",
        "",
        "- `reports/divine_pattern_findings.md`",
        "",
        "## Evidence Status",
        "",
        *confidence_tier_lines(review_audit),
        "",
        "These labels are reading aids, not commands. `candidate_lead` means interesting but early. `developing_evidence` means worth considering carefully. `reviewed_evidence_ready` means it is structured enough for your evaluation.",
        "",
        "## Biggest Current Gaps",
        "",
        *rule_coverage_lines(review_audit)[:5],
        "",
        "The main gap is not source volume. The main gap is clearer separation between evidence, interpretation, analogy, and failure conditions. Machine-drafted companions can close the tracking gap, but they do not raise confidence until source checked.",
        "",
        "The system now writes a gap-fill queue here:",
        "",
        "- `reports/review_gap_queue.md`",
        "",
        "That queue explains why fields are missing and lists the highest-priority sources that need structured companion reviews.",
        "",
        "## Theological Boundary",
        "",
        foundation_lines[0] if foundation_lines else "Pattern recognition is subordinate to Scripture and divine revelation.",
        "",
        "The project keeps this order: Scripture and revelation first, Christ and creedal guardrails next, then source quality, rival explanations, harm checks, mystery, and only then provisional confidence.",
        "",
        "## Priestly Discernment Gate",
        "",
        priestly_discernment.get(
            "core_rule",
            "Pattern claims must pass pastoral, ecclesial, sacramental, and spiritual-fruit review before public use.",
        ),
        "",
        "Before public, devotional, or pastoral use, the project now asks whether a claim would be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority.",
        "",
        "It also asks what ecclesial review is needed and how the claim remains accountable to baptism, Eucharist, confession, anointing, funerals, the church year, and daily prayer without reducing worship to symbolism.",
        "",
        "## What This Does Not Prove",
        "",
        *boundary_lines[:14],
        "",
        "## Science And Quantum Guardrail",
        "",
        science_lines[0] if science_lines else "Science language is a guardrail, not a proof engine.",
        "",
        "Quantum theory, mathematics, neuroscience, and AI pattern recognition may support humility and better reasoning. They should not be used as proof of God, prayer, consciousness, miracles, or providence.",
        "",
        "## Pressure Tests That Matter Most",
        "",
        "- Unresolved suffering",
        "- Spiritual abuse and institutional failure",
        "- Injustice without repair",
        "- Rival explanations from psychology, sociology, biology, culture, politics, and literary form",
        "- Science claims that exceed their source domain",
        "- Other religious traditions being flattened or misread",
        "",
        "## What You Need To Do",
        "",
        "Nothing technical. Read `reports/divine_pattern_findings.md` when you want the current patterns. Your role is simply to evaluate whether the patterns seem true, faithful, useful, or weak.",
        "",
        "## Current Corpus Snapshot",
        "",
        *bulletize(latest_cloud_discovery_lines(digest, reference_catalog)[:3]),
        f"- New candidate references in latest discovery run: {int(digest.get('new_count', 0) or 0):,}",
        "",
        *bulletize(friction_summary_lines(friction_layers)[:4]),
        "",
        "## Detailed Reports",
        "",
        "The detailed generated reports still exist for audit trails and deeper reading:",
        "",
    ]

    for name, path in SOURCE_REPORTS.items():
        status = "available" if path.exists() else "missing"
        lines.append(f"- `{path.as_posix()}` ({status})")

    lines.extend(
        [
            "",
            "Excluded generated reports:",
            "",
            *excluded_report_lines(),
            "",
            "## Bottom Line",
            "",
            "The project is strongest when it gives you patterns with limits attached. The system should surface the pattern; you decide how convincing it is.",
            "",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_short_article(), encoding="utf-8")
    print(f"Published article saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
