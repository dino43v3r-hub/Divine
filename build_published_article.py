from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/published/final_book_report.md")

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


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith(prefix):
            return line.strip()
    return ""


def extract_backend_stats(text: str) -> dict[str, str]:
    return {
        "indexed": find_line(text, "- Indexed documents:").replace("- ", ""),
        "nodes": find_line(text, "- Graph nodes:").replace("- ", ""),
        "edges": find_line(text, "- Graph edges:").replace("- ", ""),
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


def pattern_section(name: str) -> tuple[str, str, str, str]:
    sections = {
        "Image Of God Pattern": (
            "Human dignity is treated as gift before performance.",
            "It is strongest where language, theology, history, and vulnerable communities all pressure the same claim: persons must not be ranked by usefulness, intelligence, status, race, caste, health, or productivity.",
            "It weakens wherever dignity becomes conditional or where the project talks about humanity in the abstract while ignoring disability, poverty, migration, incarceration, or racialized harm.",
            "The faithful response is protection: listen first, defend the vulnerable, make worship and community accessible, and refuse usefulness-based love.",
        ),
        "Cross And Reversal Pattern": (
            "The cross is read as God's judgment on violent power and God's mercy for wounded people.",
            "It is strongest when passion texts, trauma theology, liberation theology, martyr memory, and abuse-pressure cases are read together.",
            "It collapses if suffering is romanticized, if victims are asked to forgive without justice, or if cross-language protects perpetrators.",
            "The faithful response is truth with boundaries: name harm, protect victims, seek repair, and let hope arrive without silencing lament.",
        ),
        "Creation-To-Consciousness Pattern": (
            "Creation, life, mind, moral awareness, and worship are explored as layered gifts.",
            "It is strongest when creation texts, ecology, disability theology, philosophy of mind, and science guardrails are held together.",
            "It weakens if science becomes proof, consciousness becomes superiority, animal suffering is ignored, or disabled people are treated as lesser images of God.",
            "The faithful response is wonder without domination: care for bodies, honor creaturely limits, protect creation, and worship without contempt for weakness.",
        ),
        "Trinity-As-Behavior Pattern": (
            "Doctrine is tested by practice: receiving life as gift, following Christ, and discerning Spirit-led transformation.",
            "It is strongest when Scripture, creeds, worship, global church testimony, and abuse safeguards all remain visible.",
            "It fails if Father, Son, and Spirit become vague symbols, group energy, three separate gods, or a tool for spiritual control.",
            "The faithful response is accountable love: test every practice by holiness, humility, justice, unity, service, and fruit over time.",
        ),
        "Providence And Contingency Pattern": (
            "Providence is treated as trust inside contingency, not certainty about hidden causes.",
            "It is strongest when Job, Ecclesiastes, exile, migration, probability, history, and public suffering are allowed to complicate easy explanations.",
            "It weakens when tragedy is explained too neatly, victims are blamed, chance is denied, or quantum language is used as a shortcut to divine action.",
            "The faithful response is humble action: pray, plan, serve, grieve, repent, and act faithfully without pretending to know every reason.",
        ),
    }
    return sections[name]


def bulletize(lines: list[str]) -> list[str]:
    return [f"- {line}" for line in lines if line]


def build_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    texts = {name: read(path) for name, path in SOURCE_REPORTS.items()}
    stats = extract_backend_stats(texts["backend"])
    lane_lines = compact_lane_table(texts["backend"])

    lines = [
        "# Divine Pattern Research",
        "",
        "## A Book Report For Careful Readers",
        "",
        f"_Generated: {generated}_",
        "",
        "This is the version to read on GitHub. The project still generates detailed machine reports in the background, but this article is the synthesized reading report: what the evidence seems to be saying, what must stay provisional, and what kind of faithful response is being invited.",
        "",
        "The short version: the research is getting stronger, but not because it has found a magic pattern. It is getting stronger because it is becoming harder to fool. It now asks for source review, rival explanations, pressure tests, failure conditions, and practical theology before a claim is allowed to grow.",
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
        *bulletize([stats["indexed"], stats["nodes"], stats["edges"]]),
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
        "## The Five Leading Pattern Families",
        "",
    ]

    for name in TOP_PATTERN_NAMES:
        thesis, why, risk, response = pattern_section(name)
        lines.extend(
            [
                f"### {name}",
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
