from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/combined_web_article.html")
MARKDOWN_OUTPUT_PATH = Path("reports/combined_web_article.md")

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


def build_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = []
    nav_items = []

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


def build_markdown_article() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
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

    for report in REPORTS:
        lines.append(f"- [{report['title']}](#{slugify(report['title'])})")

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

    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(build_article(), encoding="utf-8")
    MARKDOWN_OUTPUT_PATH.write_text(build_markdown_article(), encoding="utf-8")
    print(f"Combined report article saved to: {OUTPUT_PATH}")
    print(f"GitHub-readable article saved to: {MARKDOWN_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
