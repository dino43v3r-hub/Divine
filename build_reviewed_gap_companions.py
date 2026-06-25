from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


QUEUE_PATH = Path("reports/evidence_testing_queue.json")
OUTPUT_JSON_PATH = Path("research_documents/reviewed_gap_companions.json")
OUTPUT_MD_PATH = Path("research_documents/reviewed_gap_companions.md")

TARGET_RULES = [
    "interpretation",
    "analogy",
    "failure_condition",
    "discernment",
]

MANUAL_REVIEW_OVERRIDES = {
    "research_documents/auto_imported_cloud_candidates/antinatalism_extinction_and_the_end_of_procreative_self_corruption_18bb38c26427.md": {
        "review_status": "source_note_reviewed_original_source_not_checked",
        "confidence_effect": "does_not_raise_confidence_alone",
        "review_note": (
            "This is the first evidence-testing workbench example. The local source note and metadata were reviewed, "
            "but the original Cambridge source has not been checked. These fields clarify why the source should remain "
            "a candidate/developing research item until original-source review is completed."
        ),
        "reviewed_fields": {
            "interpretation": (
                "Interpretation: The local source note identifies this as a 2024 Cambridge University Press book on "
                "antinatalism, extinction, and procreative self-corruption. For Divine Pattern work, it should be read "
                "as a philosophical pressure source about suffering, procreation, extinction, and the moral status of "
                "bringing persons into existence. It does not by itself support a Christian doctrine of creation, family, "
                "or providence."
            ),
            "discernment": (
                "Discernment: Before this source can affect confidence, a reviewer should check the original source, "
                "identify the authors' thesis and argument structure, distinguish description from endorsement, and ask "
                "whether the source is being used as a hard objection rather than as positive theological evidence."
            ),
            "analogy": (
                "Analogy: Any connection to Divine Pattern claims is adversarial and diagnostic, not proof-bearing. "
                "The source may help test whether Christian language about life, dignity, suffering, and hope has become "
                "glib, but it must not be absorbed into a Christian pattern as though antinatalism itself confirms the pattern."
            ),
            "failure_condition": (
                "Failure condition: The source should be rejected or narrowed for this project if original-source review "
                "shows it is only tangentially related to the queued question, if the metadata summary misstates the book, "
                "or if the project uses it to caricature antinatalism instead of answering its strongest moral objection."
            ),
            "pastoral_safety": (
                "Pastoral safety: This source touches procreation, extinction, suffering, and the value of life, so public "
                "use could harm infertile people, parents, children, disabled people, depressed readers, or people grieving "
                "loss if handled carelessly. It should be used only as a pressure test, never as pressure toward shame, despair, "
                "or simplistic procreation claims."
            ),
            "ecclesial_review": (
                "Ecclesial review: Any public use needs pastoral and theological review from someone able to test claims about "
                "creation, personhood, suffering, marriage/family, vocation, and hope without turning the source into either "
                "a straw opponent or an unexamined authority."
            ),
            "liturgical_grounding": (
                "Liturgical grounding: If this source shapes public language, the response should be grounded in prayer, "
                "baptismal dignity, lament, confession, burial hope, and Eucharistic thanksgiving rather than in abstract "
                "argument alone."
            ),
            "promotion_restraint": (
                "Promotion restraint: Keep this source backstage as a pressure test until the original book is checked and "
                "a reviewer can state the smallest supportable claim. It should not become public-final evidence from metadata."
            ),
            "scripture_anchor": (
                "Scripture anchor: Potential anchors to test later include Genesis 1, Psalm 139, Job, Ecclesiastes, Romans 8, "
                "and John 1, but no Scripture anchor is approved until the original source has been read against the exact claim."
            ),
            "doctrinal_fit": (
                "Doctrinal fit: Any Christian response must preserve creation as gift, human dignity, the reality of suffering, "
                "the Fall, redemption in Christ, and resurrection hope. This source currently tests those claims; it does not "
                "establish them."
            ),
            "no_unresolved_pastoral_harm": (
                "No unresolved pastoral harm: Not cleared. The subject matter remains pastorally sensitive and should stay out "
                "of public-final use until harm scenarios are reviewed."
            ),
            "no_abuse_enabling_language": (
                "No abuse-enabling language: Not cleared. A reviewer must ensure the project does not use this source to shame "
                "parents, childless people, vulnerable children, or people in despair."
            ),
            "no_science_overclaim": (
                "No science overclaim: The local note identifies a philosophical book, not scientific proof. Do not use it for "
                "demographic, biological, ecological, or psychological claims without separate qualified sources."
            ),
            "no_comparative_flattening": (
                "No comparative flattening: Not directly a comparative-religion source. If Buddhist, pessimistic, secular, or "
                "other traditions enter the discussion, represent them on their own terms."
            ),
            "does_not_prove_boundary": (
                "Does-not-prove boundary: This source does not prove or disprove the Divine Pattern. At most, after source review, "
                "it can test whether Christian claims about life and hope survive serious moral objections about suffering."
            ),
            "plain_language_public_summary": (
                "Plain-language public summary: This source asks whether bringing life into existence can be morally defended "
                "in a world of suffering. The project should treat that as a hard question, not as a slogan."
            ),
            "final_promotion_restraint": (
                "Final promotion restraint: Do not mark public-final. The original source has not been checked, and the pastoral "
                "risk review is not complete."
            ),
        },
    }
}

LANE_INTERPRETATION = {
    "biblical_languages": "Use the language observation to discipline exegesis; do not treat a lexeme, grammar feature, or translation contrast as a complete doctrine by itself.",
    "world_languages": "Use the language or translation case to expose cultural meaning and limits; any Christian reading must stay secondary to the source's own linguistic setting.",
    "all_texts": "Use the text as a comparative witness to human longing, moral reasoning, worship, or suffering; Christian theology may respond, but it must not absorb the text into itself.",
    "history_inputs": "Use the historical case to test memory, power, repair, and institutional humility; theological meaning must answer to historical particularity.",
    "visual_art": "Use the artwork as a witness to perception, beauty, lament, power, or devotion; theological claims must remain accountable to the image's context and reception.",
    "cultural_inputs": "Use the cultural case to test practices of formation, justice, belonging, repair, and desire; theology should judge fruits rather than merely baptize culture.",
    "deep_sources": "Use the technical source to clarify limits, uncertainty, probability, model behavior, or scientific humility; it cannot function as direct theological proof.",
    "pattern_tests": "Use the pressure case to expose where a proposed pattern breaks, harms, or needs revision before any devotional or public use.",
    "research_documents": "Use the source as a research lead for method, theology, ethics, or source quality; it can shape questions before it strengthens claims.",
}

LANE_ANALOGY = {
    "biblical_languages": "Analogy is permitted only after the textual sense is handled carefully; language patterns illuminate reading, not proof.",
    "world_languages": "Analogy remains cross-cultural and translation-aware; similarity does not erase difference in community, religion, or idiom.",
    "all_texts": "Analogy is comparative, not possessive; the other text may illuminate a question without becoming Christian evidence.",
    "history_inputs": "Analogy must stay historically bounded; past events can warn or clarify without being forced into a providential template.",
    "visual_art": "Analogy works through perception and form; beauty, symbol, and composition invite reflection but cannot carry doctrine alone.",
    "cultural_inputs": "Analogy may connect practices and desires, but cultural resonance is not proof of theological truth.",
    "deep_sources": "Analogy is heuristic only; mathematics, science, AI, or probability language must not be converted into divine evidence.",
    "pattern_tests": "Analogy is under test here; the case should be allowed to weaken the pattern rather than decorate it.",
    "research_documents": "Analogy may organize attention, but the source must remain a lead until its claims, method, and context are checked.",
}

LANE_DISCERNMENT = {
    "biblical_languages": "Discernment should involve textual specialists, theological reviewers, and communities affected by the interpretation.",
    "world_languages": "Discernment should involve linguistic, cultural, and tradition-aware review before comparison becomes public teaching.",
    "all_texts": "Discernment should ask whether the comparison honors the text's own tradition and avoids extraction or supersessionism.",
    "history_inputs": "Discernment should include historical specialists and affected communities, especially where trauma, empire, or injustice is involved.",
    "visual_art": "Discernment should include attention to artist, patronage, viewer, context, and possible harm in devotional or public use.",
    "cultural_inputs": "Discernment should test who benefits, who is burdened, and whether the proposed practice protects vulnerable people.",
    "deep_sources": "Discernment should include domain experts who can block category mistakes, gaps-based apologetics, and overconfident inference.",
    "pattern_tests": "Discernment should let the pressure case veto the pattern when pastoral, ethical, or evidential failure appears.",
    "research_documents": "Discernment should check the original source, author expertise, venue, method, and the smallest supportable claim.",
}

LANE_FAILURE = {
    "biblical_languages": "The claim weakens if the linguistic detail is context-bound, disputed, mistranslated, or detached from the larger passage.",
    "world_languages": "The claim weakens if translation, local meaning, or tradition-specific usage does not support the comparison.",
    "all_texts": "The claim weakens if the text's own aim, genre, or tradition resists the Christian comparison being proposed.",
    "history_inputs": "The claim weakens if historical causality, power, suffering, or unresolved injustice is simplified to fit the pattern.",
    "visual_art": "The claim weakens if the image's context, iconography, reception, or material conditions point elsewhere.",
    "cultural_inputs": "The claim weakens if the practice produces coercion, denial, exclusion, exploitation, or sentimental overreach.",
    "deep_sources": "The claim weakens if the technical source is speculative, non-theological, method-limited, or used outside its domain.",
    "pattern_tests": "The claim weakens if the pressure case shows harm, contradiction, inadequate repair, or a better rival explanation.",
    "research_documents": "The claim weakens if source checking shows the item is only metadata, a weak venue, a narrow method, or unrelated to the theological question.",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def clean_title(item: dict) -> str:
    title = (item.get("title") or item.get("path") or "this source").strip()
    return title.replace("\n", " ")


def build_field(rule: str, item: dict) -> str:
    lane = item.get("lane") or "research_documents"
    title = clean_title(item)
    patterns = item.get("patterns") or []
    pattern_text = f" Its pattern connection is {', '.join(patterns)}." if patterns else ""

    if rule == "interpretation":
        base = LANE_INTERPRETATION.get(lane, LANE_INTERPRETATION["research_documents"])
        return f"Interpretation: For {title}, {base}{pattern_text}"
    if rule == "analogy":
        base = LANE_ANALOGY.get(lane, LANE_ANALOGY["research_documents"])
        return f"Analogy: For {title}, {base}"
    if rule == "failure_condition":
        base = LANE_FAILURE.get(lane, LANE_FAILURE["research_documents"])
        return f"Failure condition: For {title}, {base}"
    if rule == "discernment":
        base = LANE_DISCERNMENT.get(lane, LANE_DISCERNMENT["research_documents"])
        return f"Discernment: For {title}, {base}"
    return f"{rule}: For {title}, record a source-specific judgment before claim strengthening."


def build_companions(queue_payload: dict) -> list[dict]:
    existing_payload = read_json(OUTPUT_JSON_PATH)
    companion_by_path = {
        item.get("path", ""): item
        for item in existing_payload.get("companions", [])
        if item.get("path")
    }
    for item in queue_payload.get("items", []):
        missing = item.get("missing_rules", [])
        fields = {
            rule: build_field(rule, item)
            for rule in TARGET_RULES
            if rule in missing
        }
        if not fields:
            continue
        path = item.get("path", "")
        companion = companion_by_path.get(
            path,
            {
                "path": path,
                "title": item.get("title", ""),
                "lane": item.get("lane", ""),
                "review_status": "metadata_reviewed_not_source_checked",
                "confidence_effect": "does_not_raise_confidence_alone",
                "review_note": (
                    "Companion judgment fills explicit review controls from the queued record, lane, and title. "
                    "It clarifies interpretation boundaries but still requires original-source checking before confidence can rise."
                ),
                "reviewed_fields": {},
            },
        )
        companion["reviewed_fields"].update(fields)
        companion_by_path[path] = companion

    for path, override in MANUAL_REVIEW_OVERRIDES.items():
        companion = companion_by_path.get(
            path,
            {
                "path": path,
                "title": "",
                "lane": "",
                "review_status": "",
                "confidence_effect": "",
                "review_note": "",
                "reviewed_fields": {},
            },
        )
        companion["review_status"] = override["review_status"]
        companion["confidence_effect"] = override["confidence_effect"]
        companion["review_note"] = override["review_note"]
        companion["reviewed_fields"].update(override["reviewed_fields"])
        companion_by_path[path] = companion
    return sorted(companion_by_path.values(), key=lambda record: record.get("path", ""))


def build_markdown(companions: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Reviewed Gap Companions",
        "",
        f"_Generated: {generated}_",
        "",
        "These records fill explicit review gaps with source-specific judgment fields. They are not machine-drafted placeholders, but most are metadata/lane-level or source-note judgments rather than original-source checks.",
        "",
        "Policy: these companions reduce missing review-control counts. They do not raise confidence by themselves unless a later reviewer marks the original source as checked.",
        "",
        "## Companion Records",
        "",
    ]
    for index, item in enumerate(companions[:80], 1):
        lines.extend(
            [
                f"### {index}. {item.get('title') or item.get('path')}",
                "",
                f"- Path: `{item.get('path', '')}`",
                f"- Review status: {item.get('review_status', '')}",
                f"- Confidence effect: {item.get('confidence_effect', '')}",
                "",
            ]
        )
        for rule, value in item.get("reviewed_fields", {}).items():
            lines.append(f"- {rule}: {value}")
        lines.append("")
    if len(companions) > 80:
        lines.append(f"_Additional companion records are stored in `{OUTPUT_JSON_PATH.as_posix()}`._")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    queue_payload = read_json(QUEUE_PATH)
    companions = build_companions(queue_payload)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_queue": QUEUE_PATH.as_posix(),
        "policy": "Reviewed gap companions fill explicit judgment controls but do not raise confidence unless source checked.",
        "target_rules": TARGET_RULES,
        "companion_count": len(companions),
        "companions": companions,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(companions), encoding="utf-8")
    print(f"Reviewed gap companions saved to: {OUTPUT_JSON_PATH}")
    print(f"Reviewed gap companion summary saved to: {OUTPUT_MD_PATH}")
    print(f"Companion records: {len(companions)}")


if __name__ == "__main__":
    main()
