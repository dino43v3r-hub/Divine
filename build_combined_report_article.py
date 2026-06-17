from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/combined_web_article.html")
MARKDOWN_OUTPUT_PATH = Path("reports/combined_web_article.md")
FRICTION_LAYERS_PATH = Path("research_documents/friction_layers.json")
THEOLOGICAL_FOUNDATIONS_PATH = Path("research_documents/theological_foundations.json")
PATTERN_DISTORTION_PATH = Path("research_documents/pattern_distortion_layer.json")
CHRISTOLOGICAL_LAYER_PATH = Path("research_documents/christological_layer.json")
HISTORICAL_WITNESSES_PATH = Path("research_documents/historical_witnesses.json")
MYSTERY_LAYER_PATH = Path("research_documents/mystery_layer.json")
PROJECT_ARCHITECTURE_PATH = Path("research_documents/project_architecture.json")

REPORTS = [
    {
        "title": "AI Knowledge Backend",
        "path": Path("reports/ai_backend_report.txt"),
        "intro": "How the retrieval index, knowledge graph, and review rules help the project reason carefully.",
    },
    {
        "title": "Reader Book",
        "path": Path("reports/divine_pattern_reader_book.txt"),
        "intro": "The most reader-facing explanation of the developing pattern families.",
    },
    {
        "title": "Disciplined Theological Assistant",
        "path": Path("reports/disciplined_theological_assistant_report.txt"),
        "intro": "The practical-theology posture: cautious, sourced, and accountable.",
    },
    {
        "title": "Summary",
        "path": Path("reports/divine_pattern_summary_report.txt"),
        "intro": "The current high-level state of the project.",
    },
    {
        "title": "Top Five Pattern Families",
        "path": Path("reports/top_five_divine_patterns_report.txt"),
        "intro": "The leading pattern candidates and how they are being pressure-tested.",
    },
    {
        "title": "Research Report",
        "path": Path("reports/divine_pattern_research_report.txt"),
        "intro": "The broader analysis output from the corpus.",
    },
    {
        "title": "Pattern Candidates",
        "path": Path("reports/divine_pattern_candidates_report.txt"),
        "intro": "Candidate patterns that need source review and counter-readings before confidence rises.",
    },
    {
        "title": "Pressure Tests",
        "path": Path("reports/divine_pattern_test_report.txt"),
        "intro": "Where the leading claims face suffering, injustice, failure, practical use, and science guardrails.",
    },
    {
        "title": "Deep Source Review",
        "path": Path("reports/deep_source_review_report.txt"),
        "intro": "Science, quantum, suffering, and other high-caution source checks.",
    },
    {
        "title": "Theologian Pattern Design",
        "path": Path("reports/theologian_pattern_design_report.txt"),
        "intro": "Cross-era theologian evidence, disagreements, and pressure points.",
    },
    {
        "title": "Cross-Layer Reasoning",
        "path": Path("reports/cross_layer_reasoning_report.txt"),
        "intro": "How lanes interact across theology, language, history, art, psychology, culture, and practice.",
    },
    {
        "title": "Cultural Patterns",
        "path": Path("reports/cultural_pattern_relationships_report.txt"),
        "intro": "Culture, justice, technology, ecology, health, education, and community.",
    },
    {
        "title": "Music Notes",
        "path": Path("reports/music_note_patterns_report.txt"),
        "intro": "Musical structure, tension, resolution, and analogy boundaries.",
    },
    {
        "title": "Music Lyrics",
        "path": Path("reports/music_lyric_patterns_report.txt"),
        "intro": "Lyric and genre patterns handled without copying copyrighted lyrics.",
    },
]

ARTICLE_LEAD = [
    "This page is not meant to behave like a raw report dump. It is a guided reading of the project: what the system thinks it is seeing, what still needs review, and what kind of faithful response the evidence may invite.",
    "The core discipline is simple: retrieve sources before making claims, keep rival explanations visible, test every pattern against suffering and injustice, and refuse to let machine scores settle truth.",
    "The full generated reports remain available in each section, but they are folded away so the main article can be read in order.",
]

SECTION_TAKEAWAYS = {
    "AI Knowledge Backend": [
        "The backend is now acting like a careful librarian: it retrieves, connects, and audits sources before an LLM drafts claims.",
        "Its strongest contribution is restraint. It keeps asking whether a claim has evidence, interpretation, discernment, analogy, practical use, counter-reading, and a failure condition.",
    ],
    "Reader Book": [
        "This is the most human-facing section. It frames the project as a field guide rather than a verdict.",
        "Its best reading posture is practical: what pattern is being noticed, and what faithful action is being invited today?",
    ],
    "Disciplined Theological Assistant": [
        "This section describes the assistant's character: cautious with sources, alert to harm, and unwilling to confuse repeated signals with truth.",
        "It should be read as the operating conscience of the project.",
    ],
    "Summary": [
        "The summary gives the current state of the corpus and the major claim controls.",
        "Use it to see where the project is balanced, where it is overfull, and where it still needs source review.",
    ],
    "Top Five Pattern Families": [
        "The leading patterns are hypotheses under pressure, not final conclusions.",
        "The important question is not which pattern sounds most elegant, but which one survives suffering, injustice, rival explanations, and practical use.",
    ],
    "Research Report": [
        "This is the broad technical sweep of the project.",
        "Read it for signal, but let the review rules decide what deserves confidence.",
    ],
    "Pattern Candidates": [
        "Candidate patterns are named possibilities that still need source packs, counter-readings, and failure conditions.",
        "They are useful because they organize attention, not because they prove themselves.",
    ],
    "Pressure Tests": [
        "This is where attractive ideas meet hard cases.",
        "A pattern gets weaker if it cannot face unresolved suffering, injustice, practical failure, science limits, or better rival explanations.",
    ],
    "Deep Source Review": [
        "This section carries the stricter guardrails, especially around science, quantum theory, and suffering.",
        "Quantum language belongs here as a humility check, not as proof of divine action.",
    ],
    "Theologian Pattern Design": [
        "The theologian lane adds depth across eras, but it also preserves disagreement.",
        "A name or tradition is never enough by itself; primary texts, context, and misuse risks matter.",
    ],
    "Cross-Layer Reasoning": [
        "This section asks whether patterns actually connect across lanes: text, history, language, art, psychology, culture, and practice.",
        "The best cross-layer claims are modest, sourced, and aware of alternatives.",
    ],
    "Cultural Patterns": [
        "Culture shows where theology becomes embodied in systems, habits, power, and repair.",
        "The question is whether a pattern forms truthful love and justice in public life.",
    ],
    "Music Notes": [
        "Music can illuminate pattern, tension, return, and resolution.",
        "Musical beauty remains analogy unless it is connected carefully to evidence and practice.",
    ],
    "Music Lyrics": [
        "The lyrics lane tracks motifs without copying copyrighted lyric collections.",
        "Treat lyric signals as prompts for interpretation, not conclusions.",
    ],
}


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def read_report(path: Path) -> str:
    if not path.exists():
        return f"{path} was not generated."
    return path.read_text(encoding="utf-8", errors="replace")


def read_friction_layers() -> list[dict]:
    if not FRICTION_LAYERS_PATH.exists():
        return []
    try:
        payload = json.loads(FRICTION_LAYERS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    records = payload.get("friction_layers", [])
    return records if isinstance(records, list) else []


def read_json_layer(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def first_nonempty_lines(text: str, limit: int = 7) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) <= {"=", "-"}:
            continue
        lines.append(stripped)
        if len(lines) >= limit:
            break
    return lines


def render_inline_code(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    rendered = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{escape(part[1:-1])}</code>")
        else:
            rendered.append(escape(part))
    return "".join(rendered)


def classify_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""
    if set(stripped) <= {"=", "-"} and len(stripped) >= 3:
        return "rule"
    if re.match(r"^\d+\.\s+", stripped):
        return "numbered"
    if stripped.startswith("- "):
        return "bullet"
    if stripped.endswith(":") and len(stripped) < 90:
        return "speaker" if stripped.startswith(("Reviewer:", "Backend:")) else "label"
    if stripped.startswith(("Reviewer:", "Backend:")):
        return "dialogue"
    return "paragraph"


def render_report_text(text: str) -> str:
    html = []
    pending_list = None

    def close_list():
        nonlocal pending_list
        if pending_list:
            html.append(f"</{pending_list}>")
            pending_list = None

    lines = text.splitlines()
    skip_next_rule = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        kind = classify_line(line)

        if skip_next_rule:
            skip_next_rule = False
            if kind == "rule":
                continue

        next_kind = classify_line(lines[index + 1]) if index + 1 < len(lines) else ""
        if stripped and next_kind == "rule":
            close_list()
            level = "h3" if set(lines[index + 1].strip()) <= {"-"} else "h2"
            html.append(f"<{level}>{escape(stripped)}</{level}>")
            skip_next_rule = True
            continue

        if not stripped or kind == "rule":
            close_list()
            continue

        if kind in {"bullet", "numbered"}:
            tag = "ol" if kind == "numbered" else "ul"
            if pending_list != tag:
                close_list()
                html.append(f"<{tag}>")
                pending_list = tag
            item = re.sub(r"^(\d+\.\s+|- )", "", stripped)
            html.append(f"<li>{render_inline_code(item)}</li>")
            continue

        close_list()

        if kind == "dialogue":
            speaker, _, rest = stripped.partition(":")
            html.append(
                f"<p class=\"dialogue\"><strong>{escape(speaker)}:</strong>{escape(rest)}</p>"
            )
        elif kind == "label":
            html.append(f"<p class=\"label\">{render_inline_code(stripped)}</p>")
        else:
            html.append(f"<p>{render_inline_code(stripped)}</p>")

    close_list()
    return "\n".join(html)


def render_friction_layer_html(records: list[dict]) -> str:
    if not records:
        return "<p>No friction layer records have been added yet.</p>"

    cards = []
    for record in records:
        tag_html = "".join(
            f"<span>{escape(tag)}</span>" for tag in record.get("tags", [])
        )
        fields = [
            ("Evidence Score", str(record.get("evidence_score", "unrated"))),
            ("Evidence Effect", record.get("evidence_effect", "unrated")),
            ("Evidence Value", str(record.get("evidence_value", "unrated"))),
            ("Insight Value", str(record.get("insight_value", "unrated"))),
            ("Confidence", record.get("confidence", "unrated")),
            ("Review Status", record.get("review_status", "unreviewed")),
            ("Resolution Status", record.get("resolution_status", "unrated")),
            ("Domain", record.get("domain", "")),
            ("Observation", record.get("observation", "")),
            ("Pattern", record.get("pattern", "")),
            ("Distortion", record.get("distortion", "")),
            ("Friction Point", record.get("friction_point", "")),
            ("Alternative Explanations", ", ".join(record.get("alternative_explanations", []))),
            ("Non-Christian Resolution", record.get("non_christian_resolution", "")),
            ("Christian Resolution", record.get("christian_resolution", "")),
            ("Transformation Result", record.get("transformation_result", "")),
            ("Divine Pattern Insight", record.get("divine_pattern_insight", "")),
            ("Failure Risk", record.get("failure_risk", "")),
            ("Source Review Note", record.get("source_review_note", "")),
        ]
        field_html = "\n".join(
            f"<p><strong>{escape(label)}:</strong> {escape(value)}</p>"
            for label, value in fields
            if value
        )
        cards.append(
            f"""
            <article class="friction-card">
              <h3>{escape(record.get('title', 'Untitled Friction Record'))}</h3>
              {field_html}
              <div class="tag-row">{tag_html}</div>
            </article>
            """
        )
    return "\n".join(cards)


def simple_card_html(title: str, fields: list[tuple[str, str]]) -> str:
    field_html = "\n".join(
        f"<p><strong>{escape(label)}:</strong> {escape(value)}</p>"
        for label, value in fields
        if value
    )
    return f"<article class=\"friction-card\"><h3>{escape(title)}</h3>{field_html}</article>"


def render_foundations_html(layer: dict) -> str:
    if not layer:
        return "<p>Theological foundations layer is missing.</p>"
    principles = "".join(f"<li>{escape(item)}</li>" for item in layer.get("principles", []))
    definitions = "".join(
        f"<p><strong>{escape(name)}:</strong> {escape(definition)}</p>"
        for name, definition in layer.get("definitions", {}).items()
    )
    order = "".join(f"<li>{escape(item)}</li>" for item in layer.get("interpretive_order", []))
    return f"""
      <p>{escape(layer.get('mission_statement', ''))}</p>
      <p><strong>Authority boundary:</strong> {escape(layer.get('authority_boundary', ''))}</p>
      <h3>Principles</h3>
      <ul>{principles}</ul>
      <h3>Definitions</h3>
      {definitions}
      <h3>Interpretive Order</h3>
      <ul>{order}</ul>
    """


def render_architecture_html(layer: dict) -> str:
    architecture = layer.get("architecture", {}) if layer else {}
    if not architecture:
        return "<p>Project architecture layer is missing.</p>"
    blocks = []
    for heading, items in architecture.items():
        list_items = "".join(f"<li>{escape(item)}</li>" for item in items)
        blocks.append(f"<article class=\"friction-card\"><h3>{escape(heading)}</h3><ul>{list_items}</ul></article>")
    return "\n".join(blocks)


def render_distortion_html(layer: dict) -> str:
    return "\n".join(
        simple_card_html(
            f"{record.get('original_pattern', 'Pattern')} -> {record.get('distortion', 'Distortion')}",
            [
                ("Cause", record.get("cause", "")),
                ("Consequences", record.get("consequences", "")),
                ("Biblical Examples", ", ".join(record.get("biblical_examples", []))),
                ("Restoration Path", record.get("restoration_path", "")),
            ],
        )
        for record in layer.get("records", [])
    ) or "<p>No distortion records yet.</p>"


def render_christological_html(layer: dict) -> str:
    return "\n".join(
        simple_card_html(
            record.get("pattern_name", "Pattern"),
            [
                ("Appearance In Creation", record.get("appearance_in_creation", "")),
                ("Appearance In Humanity", record.get("appearance_in_humanity", "")),
                ("Distortion", record.get("distortion", "")),
                ("Fulfillment In Christ", record.get("fulfillment_in_christ", "")),
                ("Restoration Through Christ", record.get("restoration_through_christ", "")),
                ("Supporting Scriptures", ", ".join(record.get("supporting_scriptures", []))),
            ],
        )
        for record in layer.get("records", [])
    ) or "<p>No Christological records yet.</p>"


def render_historical_html(layer: dict) -> str:
    return "\n".join(
        simple_card_html(
            record.get("name", "Witness"),
            [
                ("Era", record.get("era", "")),
                ("Key Themes", ", ".join(record.get("key_themes", []))),
                ("Relevant Patterns", ", ".join(record.get("relevant_patterns", []))),
                ("Agreements", record.get("agreements", "")),
                ("Disagreements", record.get("disagreements", "")),
                ("Citations", ", ".join(record.get("citations", []))),
            ],
        )
        for record in layer.get("records", [])
    ) or "<p>No historical witnesses yet.</p>"


def render_mystery_html(layer: dict) -> str:
    return "\n".join(
        simple_card_html(
            record.get("topic", "Mystery"),
            [
                ("Category", record.get("category", "")),
                ("What Can Be Known", record.get("what_can_be_known", "")),
                ("What Remains Mysterious", record.get("what_remains_mysterious", "")),
                ("Supporting Scriptures", ", ".join(record.get("supporting_scriptures", []))),
                ("Theological Notes", record.get("theological_notes", "")),
            ],
        )
        for record in layer.get("records", [])
    ) or "<p>No mystery records yet.</p>"


def friction_summary_items(records: list[dict]) -> list[str]:
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


def friction_domain_rollup_items(records: list[dict]) -> list[str]:
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


def friction_resolution_rollup_items(records: list[dict]) -> list[str]:
    if not records:
        return ["No resolution statuses recorded yet."]

    counts: dict[str, int] = {}
    for record in records:
        status = record.get("resolution_status", "unrated")
        counts[status] = counts.get(status, 0) + 1
    return [f"{status}: {count}" for status, count in sorted(counts.items())]


def build_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = []
    nav_items = []
    friction_layers = read_friction_layers()
    theological_foundations = read_json_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    project_architecture = read_json_layer(PROJECT_ARCHITECTURE_PATH)
    pattern_distortion = read_json_layer(PATTERN_DISTORTION_PATH)
    christological_layer = read_json_layer(CHRISTOLOGICAL_LAYER_PATH)
    historical_witnesses = read_json_layer(HISTORICAL_WITNESSES_PATH)
    mystery_layer = read_json_layer(MYSTERY_LAYER_PATH)
    friction_summary = "".join(
        f"<li>{escape(item)}</li>" for item in friction_summary_items(friction_layers)
    )
    friction_domains = "".join(
        f"<li>{escape(item)}</li>" for item in friction_domain_rollup_items(friction_layers)
    )
    friction_resolutions = "".join(
        f"<li>{escape(item)}</li>" for item in friction_resolution_rollup_items(friction_layers)
    )

    theological_sections = [
        (
            "theological-foundations",
            "Theological Foundations",
            THEOLOGICAL_FOUNDATIONS_PATH,
            "Scripture and divine revelation are primary; pattern recognition is secondary and supportive.",
            render_foundations_html(theological_foundations),
        ),
        (
            "project-architecture",
            "Project Architecture",
            PROJECT_ARCHITECTURE_PATH,
            "The project is organized around foundation, patterns, distortions, friction, Christology, historical witnesses, and mystery.",
            render_architecture_html(project_architecture),
        ),
        (
            "pattern-distortion-layer",
            "Pattern Distortion Layer",
            PATTERN_DISTORTION_PATH,
            pattern_distortion.get("purpose", ""),
            render_distortion_html(pattern_distortion),
        ),
        (
            "christological-layer",
            "Christological Layer",
            CHRISTOLOGICAL_LAYER_PATH,
            christological_layer.get("purpose", ""),
            render_christological_html(christological_layer),
        ),
        (
            "historical-witnesses",
            "Historical Witnesses",
            HISTORICAL_WITNESSES_PATH,
            historical_witnesses.get("purpose", ""),
            render_historical_html(historical_witnesses),
        ),
        (
            "mystery-layer",
            "Mystery Layer",
            MYSTERY_LAYER_PATH,
            mystery_layer.get("purpose", ""),
            render_mystery_html(mystery_layer),
        ),
    ]

    for section_id, title, path, intro, body in theological_sections:
        nav_items.append(f"<a href=\"#{section_id}\">{escape(title)}</a>")
        sections.append(
            f"""
            <section id="{section_id}" class="article-section">
              <p class="section-kicker">{escape(path.as_posix())}</p>
              <h1>{escape(title)}</h1>
              <p class="section-intro">{escape(intro)}</p>
              <div class="friction-grid">
                {body}
              </div>
            </section>
            """
        )

    for report in REPORTS:
        section_id = slugify(report["title"])
        nav_items.append(
            f"<a href=\"#{section_id}\">{escape(report['title'])}</a>"
        )
        text = read_report(report["path"])
        body = render_report_text(text)
        takeaways = SECTION_TAKEAWAYS.get(report["title"], [])
        takeaway_items = "\n".join(
            f"<li>{escape(item)}</li>" for item in takeaways
        )
        preview_items = "\n".join(
            f"<li>{render_inline_code(line)}</li>" for line in first_nonempty_lines(text)
        )
        sections.append(
            f"""
            <section id="{section_id}" class="article-section">
              <p class="section-kicker">{escape(report['path'].as_posix())}</p>
              <h1>{escape(report['title'])}</h1>
              <p class="section-intro">{escape(report['intro'])}</p>
              <div class="reader-pass">
                <h2>Why This Section Matters</h2>
                <ul>{takeaway_items}</ul>
                <h2>First Signals</h2>
                <ul>{preview_items}</ul>
              </div>
              <details class="full-report">
                <summary>Open the full generated report</summary>
                <div class="report-body">
                  {body}
                </div>
              </details>
            </section>
            """
        )

    nav_items.append("<a href=\"#friction-layer\">Friction Layer</a>")
    sections.append(
        f"""
        <section id="friction-layer" class="article-section">
          <p class="section-kicker">{escape(FRICTION_LAYERS_PATH.as_posix())}</p>
          <h1>Friction Layer</h1>
          <p class="section-intro">Friction is not evidence of failure. Friction is evidence that a pattern has reached the limits of its current explanatory framework and is seeking a deeper resolution.</p>
          <div class="reader-pass">
            <h2>Why This Section Matters</h2>
            <p>This layer records where philosophy, science, culture, or theology creates productive tension with the Divine Pattern framework.</p>
            <h2>Provisional Evidence Summary</h2>
            <ul>{friction_summary}</ul>
            <p>Scale: -2 weakens the claim; -1 creates a serious unresolved challenge; 0 is diagnostic friction; 1 gives modest support with caution; 2 gives moderate support after Christian resolution.</p>
            <h2>Domain Rollup</h2>
            <ul>{friction_domains}</ul>
            <h2>Resolution Status Rollup</h2>
            <ul>{friction_resolutions}</ul>
          </div>
          <div class="friction-grid">
            {render_friction_layer_html(friction_layers)}
          </div>
        </section>
        """
    )

    nav = "\n".join(nav_items)
    section_html = "\n".join(sections)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Divine Pattern Research Article</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17201b;
      --muted: #5b655f;
      --line: #d7ded8;
      --paper: #fbfcfa;
      --band: #eef4ef;
      --accent: #1f6f63;
      --accent-2: #7b3f2a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.62;
    }}
    .hero {{
      min-height: 72vh;
      display: grid;
      align-content: end;
      padding: clamp(32px, 7vw, 92px);
      background:
        linear-gradient(rgba(18, 31, 25, .18), rgba(18, 31, 25, .70)),
        url("https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1800&q=80");
      background-size: cover;
      background-position: center;
      color: white;
    }}
    .hero h1 {{
      max-width: 980px;
      margin: 0 0 16px;
      font-size: clamp(44px, 7vw, 92px);
      line-height: .96;
      letter-spacing: 0;
    }}
    .hero p {{
      max-width: 760px;
      margin: 0;
      font-size: clamp(18px, 2.5vw, 25px);
      color: rgba(255, 255, 255, .92);
    }}
    .meta {{
      margin-top: 28px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: rgba(255, 255, 255, .82);
    }}
    nav {{
      position: sticky;
      top: 0;
      z-index: 2;
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding: 12px clamp(20px, 5vw, 64px);
      background: rgba(251, 252, 250, .96);
      border-bottom: 1px solid var(--line);
      font-family: Arial, sans-serif;
      white-space: nowrap;
    }}
    nav a {{
      color: var(--accent);
      text-decoration: none;
      border: 1px solid var(--line);
      padding: 7px 10px;
      border-radius: 6px;
      background: white;
      font-size: 14px;
    }}
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 40px 20px 80px;
    }}
    .article-section {{
      padding: 44px 0;
      border-bottom: 1px solid var(--line);
    }}
    .section-kicker {{
      margin: 0 0 8px;
      color: var(--accent-2);
      font-family: Arial, sans-serif;
      font-size: 13px;
      letter-spacing: .06em;
      text-transform: uppercase;
    }}
    .article-section h1 {{
      margin: 0 0 8px;
      font-size: clamp(32px, 5vw, 54px);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .section-intro {{
      margin: 0 0 28px;
      color: var(--muted);
      font-size: 20px;
    }}
    .report-body h2 {{
      margin: 34px 0 8px;
      font-size: 28px;
      line-height: 1.15;
    }}
    .report-body h3 {{
      margin: 24px 0 6px;
      font-size: 20px;
      line-height: 1.25;
      color: var(--accent);
    }}
    .report-body p {{
      margin: 10px 0;
      font-size: 18px;
    }}
    .report-body ul,
    .report-body ol {{
      padding-left: 22px;
      margin: 12px 0 18px;
      font-size: 17px;
    }}
    .dialogue {{
      padding: 10px 14px;
      background: var(--band);
      border-left: 4px solid var(--accent);
      border-radius: 0 6px 6px 0;
      font-family: Arial, sans-serif;
      font-size: 16px !important;
    }}
    .label {{
      color: var(--accent-2);
      font-family: Arial, sans-serif;
      font-weight: 700;
    }}
    code {{
      font-family: Consolas, "Courier New", monospace;
      font-size: .92em;
      background: #edf1ee;
      padding: 1px 4px;
      border-radius: 4px;
    }}
    .friction-grid {{
      display: grid;
      gap: 16px;
    }}
    .friction-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      padding: 18px;
    }}
    .friction-card h3 {{
      margin: 0 0 12px;
      color: var(--accent);
      font-size: 22px;
    }}
    .friction-card p {{
      margin: 10px 0;
    }}
    .tag-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}
    .tag-row span {{
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #f8faf8;
      color: var(--muted);
      padding: 4px 9px;
      font-family: Arial, sans-serif;
      font-size: 14px;
    }}
    @media (max-width: 640px) {{
      .hero {{
        min-height: 68vh;
        padding: 28px 20px;
      }}
      nav {{
        padding: 10px 12px;
      }}
      main {{
        padding: 28px 16px 64px;
      }}
      .report-body p {{
        font-size: 17px;
      }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div>
      <h1>Divine Pattern Research</h1>
      <p>A single readable article drawn from the project reports, written with a scholar's caution and a disciple's practical question.</p>
      <div class="meta">Generated {escape(generated)} from repository reports.</div>
    </div>
  </header>
  <nav aria-label="Report sections">
    {nav}
  </nav>
  <main>
    <section class="editor-note">
      <p class="section-kicker">Reader's orientation</p>
      <h1>How To Read This Page</h1>
      {"".join(f"<p>{escape(paragraph)}</p>" for paragraph in ARTICLE_LEAD)}
    </section>
    {section_html}
  </main>
</body>
</html>
"""


def markdown_code(text: str) -> str:
    return text.replace("`", "\\`")


def markdown_foundations_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Theological foundations layer is missing."]
    lines = [
        layer.get("mission_statement", ""),
        "",
        f"Authority boundary: {layer.get('authority_boundary', '')}",
        "",
        "### Principles",
        "",
    ]
    lines.extend(f"- {item}" for item in layer.get("principles", []))
    lines.extend(["", "### Definitions", ""])
    for name, definition in layer.get("definitions", {}).items():
        lines.append(f"- {name}: {definition}")
    lines.extend(["", "### Interpretive Order", ""])
    lines.extend(f"- {item}" for item in layer.get("interpretive_order", []))
    return lines


def markdown_architecture_lines(layer: dict) -> list[str]:
    architecture = layer.get("architecture", {}) if layer else {}
    if not architecture:
        return ["Project architecture layer is missing."]
    lines = []
    for heading, items in architecture.items():
        lines.extend([f"### {heading}", ""])
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    return lines


def markdown_records_lines(layer: dict, title_key: str, fields: list[tuple[str, str]]) -> list[str]:
    records = layer.get("records", []) if layer else []
    if not records:
        return ["No records yet."]
    lines = [layer.get("purpose", ""), ""]
    for record in records:
        title = record.get(title_key, "Record")
        if title_key == "original_pattern":
            title = f"{record.get('original_pattern', 'Pattern')} -> {record.get('distortion', 'Distortion')}"
        lines.extend([f"### {title}", ""])
        for label, key in fields:
            value = record.get(key, "")
            if isinstance(value, list):
                value = ", ".join(value)
            lines.append(f"- {label}: {value}")
        lines.append("")
    return lines


def build_markdown_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    friction_layers = read_friction_layers()
    theological_foundations = read_json_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    project_architecture = read_json_layer(PROJECT_ARCHITECTURE_PATH)
    pattern_distortion = read_json_layer(PATTERN_DISTORTION_PATH)
    christological_layer = read_json_layer(CHRISTOLOGICAL_LAYER_PATH)
    historical_witnesses = read_json_layer(HISTORICAL_WITNESSES_PATH)
    mystery_layer = read_json_layer(MYSTERY_LAYER_PATH)
    lines = [
        "# Divine Pattern Research",
        "",
        "_A GitHub-readable article drawn from the generated reports._",
        "",
        f"Generated: `{generated}`",
        "",
        "## How To Read This Page",
        "",
        *ARTICLE_LEAD,
        "",
        "## Contents",
        "",
    ]

    theological_markdown_sections = [
        ("Theological Foundations", THEOLOGICAL_FOUNDATIONS_PATH, markdown_foundations_lines(theological_foundations)),
        ("Project Architecture", PROJECT_ARCHITECTURE_PATH, markdown_architecture_lines(project_architecture)),
        (
            "Pattern Distortion Layer",
            PATTERN_DISTORTION_PATH,
            markdown_records_lines(
                pattern_distortion,
                "original_pattern",
                [
                    ("Cause", "cause"),
                    ("Consequences", "consequences"),
                    ("Biblical Examples", "biblical_examples"),
                    ("Restoration Path", "restoration_path"),
                ],
            ),
        ),
        (
            "Christological Layer",
            CHRISTOLOGICAL_LAYER_PATH,
            markdown_records_lines(
                christological_layer,
                "pattern_name",
                [
                    ("Appearance In Creation", "appearance_in_creation"),
                    ("Appearance In Humanity", "appearance_in_humanity"),
                    ("Distortion", "distortion"),
                    ("Fulfillment In Christ", "fulfillment_in_christ"),
                    ("Restoration Through Christ", "restoration_through_christ"),
                    ("Supporting Scriptures", "supporting_scriptures"),
                ],
            ),
        ),
        (
            "Historical Witnesses",
            HISTORICAL_WITNESSES_PATH,
            markdown_records_lines(
                historical_witnesses,
                "name",
                [
                    ("Era", "era"),
                    ("Key Themes", "key_themes"),
                    ("Relevant Patterns", "relevant_patterns"),
                    ("Agreements", "agreements"),
                    ("Disagreements", "disagreements"),
                    ("Citations", "citations"),
                ],
            ),
        ),
        (
            "Mystery Layer",
            MYSTERY_LAYER_PATH,
            markdown_records_lines(
                mystery_layer,
                "topic",
                [
                    ("Category", "category"),
                    ("What Can Be Known", "what_can_be_known"),
                    ("What Remains Mysterious", "what_remains_mysterious"),
                    ("Supporting Scriptures", "supporting_scriptures"),
                    ("Theological Notes", "theological_notes"),
                ],
            ),
        ),
    ]

    for title, _, _ in theological_markdown_sections:
        lines.append(f"- [{title}](#{slugify(title)})")
    for report in REPORTS:
        lines.append(f"- [{report['title']}](#{slugify(report['title'])})")
    lines.append("- [Friction Layer](#friction-layer)")

    for title, path, section_lines in theological_markdown_sections:
        lines.extend(["", f"## {title}", "", f"_Source: `{path.as_posix()}`_", ""])
        lines.extend(section_lines)
        lines.append("")

    for report in REPORTS:
        text = read_report(report["path"])
        takeaways = SECTION_TAKEAWAYS.get(report["title"], [])
        preview = first_nonempty_lines(text)

        lines.extend(
            [
                "",
                f"## {report['title']}",
                "",
                f"_Source: `{report['path'].as_posix()}`_",
                "",
                report["intro"],
                "",
                "### Why This Section Matters",
                "",
            ]
        )
        for item in takeaways:
            lines.append(f"- {item}")

        lines.extend(["", "### First Signals", ""])
        for item in preview:
            lines.append(f"- {markdown_code(item)}")

        lines.extend(
            [
                "",
                "<details>",
                f"<summary>Open the full generated report: {report['title']}</summary>",
                "",
                "```text",
                text,
                "```",
                "",
                "</details>",
                "",
            ]
        )

    lines.extend(
        [
            "",
            "## Friction Layer",
            "",
            f"_Source: `{FRICTION_LAYERS_PATH.as_posix()}`_",
            "",
            "Friction is not evidence of failure. Friction is evidence that a pattern has reached the limits of its current explanatory framework and is seeking a deeper resolution.",
            "",
            "### Provisional Evidence Summary",
            "",
        ]
    )
    for item in friction_summary_items(friction_layers):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "Scale: -2 weakens the claim; -1 creates a serious unresolved challenge; 0 is diagnostic friction; 1 gives modest support with caution; 2 gives moderate support after Christian resolution.",
            "",
            "### Domain Rollup",
            "",
        ]
    )
    for item in friction_domain_rollup_items(friction_layers):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "### Resolution Status Rollup",
            "",
        ]
    )
    for item in friction_resolution_rollup_items(friction_layers):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
        ]
    )
    if not friction_layers:
        lines.append("- No friction layer records have been added yet.")
    for record in friction_layers:
        tags = ", ".join(record.get("tags", [])) or "untagged"
        lines.extend(
            [
                f"### {record.get('title', 'Untitled Friction Record')}",
                "",
                f"- Evidence Score: {record.get('evidence_score', 'unrated')}",
                f"- Evidence Effect: {record.get('evidence_effect', 'unrated')}",
                f"- Evidence Value: {record.get('evidence_value', 'unrated')}",
                f"- Insight Value: {record.get('insight_value', 'unrated')}",
                f"- Confidence: {record.get('confidence', 'unrated')}",
                f"- Review Status: {record.get('review_status', 'unreviewed')}",
                f"- Resolution Status: {record.get('resolution_status', 'unrated')}",
                f"- Domain: {record.get('domain', 'Unspecified')}",
                f"- Observation: {record.get('observation', '')}",
                f"- Pattern: {record.get('pattern', '')}",
                f"- Distortion: {record.get('distortion', '')}",
                f"- Friction Point: {record.get('friction_point', '')}",
                f"- Alternative Explanations: {', '.join(record.get('alternative_explanations', []))}",
                f"- Non-Christian Resolution: {record.get('non_christian_resolution', '')}",
                f"- Christian Resolution: {record.get('christian_resolution', '')}",
                f"- Transformation Result: {record.get('transformation_result', '')}",
                f"- Divine Pattern Insight: {record.get('divine_pattern_insight', '')}",
                f"- Failure Risk: {record.get('failure_risk', '')}",
                f"- Source Review Note: {record.get('source_review_note', '')}",
                f"- Tags: {tags}",
                "",
            ]
        )

    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(build_article(), encoding="utf-8")
    MARKDOWN_OUTPUT_PATH.write_text(build_markdown_article(), encoding="utf-8")
    print(f"Combined report article saved to: {OUTPUT_PATH}")
    print(f"GitHub-readable article saved to: {MARKDOWN_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
