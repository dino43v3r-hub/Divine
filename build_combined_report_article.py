from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/combined_web_article.html")

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


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def read_report(path: Path) -> str:
    if not path.exists():
        return f"{path} was not generated."
    return path.read_text(encoding="utf-8", errors="replace")


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
            html.append(f"<li>{escape(item)}</li>")
            continue

        close_list()

        if kind == "dialogue":
            speaker, _, rest = stripped.partition(":")
            html.append(
                f"<p class=\"dialogue\"><strong>{escape(speaker)}:</strong>{escape(rest)}</p>"
            )
        elif kind == "label":
            html.append(f"<p class=\"label\">{escape(stripped)}</p>")
        else:
            html.append(f"<p>{escape(stripped)}</p>")

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
        body = render_report_text(read_report(report["path"]))
        sections.append(
            f"""
            <section id="{section_id}" class="article-section">
              <p class="section-kicker">{escape(report['path'].as_posix())}</p>
              <h1>{escape(report['title'])}</h1>
              <p class="section-intro">{escape(report['intro'])}</p>
              <div class="report-body">
                {body}
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
    {section_html}
  </main>
</body>
</html>
"""


def main() -> None:
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(build_article(), encoding="utf-8")
    print(f"Combined report article saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
