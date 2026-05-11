import json
import os
from pathlib import Path
from urllib import error, request


MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
REPORT_PATH = Path("reports/divine_pattern_research_report.txt")
SYNTHESIS_PATH = Path(
    "research_documents/christian_sources/god_and_human_behavior_science_synthesis.md"
)
OUTPUT_PATH = Path("reports/ai_evidence_review.txt")


def read_text(path):
    """Read a text file if it exists."""
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8", errors="replace")


def trim_text(text, max_characters=45_000):
    """Keep prompts small enough for a first prototype."""
    if len(text) <= max_characters:
        return text

    return text[:max_characters] + "\n\n[Text trimmed for AI review.]"


def build_prompt():
    """Create a critique prompt from the current research report."""
    report = trim_text(read_text(REPORT_PATH))
    synthesis = trim_text(read_text(SYNTHESIS_PATH), max_characters=25_000)

    return f"""
You are reviewing an interdisciplinary research project about God, faith,
Christian theology, human behavior, ritual, neuroscience, anthropology,
and AI pattern recognition.

Your job is not to prove or disprove God.
Your job is to critique the evidence and separate:
1. source-backed findings,
2. plausible hypotheses,
3. weak or speculative claims,
4. missing evidence,
5. better research questions.

Use careful language. Do not overclaim. Treat every proposed pattern as a
research hypothesis unless the evidence directly supports it.

Return the review with these sections:

- Executive Summary
- Strongest Source-Backed Patterns
- Weak Or Speculative Claims
- Missing Evidence
- Relationships Worth Testing
- Suggested Research Plan
- Plain-English Conclusion

CURRENT ANALYZER REPORT:
{report}

SOURCE-BACKED SYNTHESIS NOTE:
{synthesis}
""".strip()


def call_openai(prompt):
    """Call the OpenAI Responses API using only the Python standard library."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Set it first, then run this script again."
        )

    body = {
        "model": MODEL,
        "instructions": (
            "You are a careful interdisciplinary research assistant. "
            "You cite uncertainty clearly and avoid unsupported conclusions."
        ),
        "input": prompt,
    }

    api_request = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {details}") from exc

    output_text = payload.get("output_text")
    if output_text:
        return output_text

    return json.dumps(payload, indent=2)


def save_review(review):
    """Save the AI critique report."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(review, encoding="utf-8")


def main():
    prompt = build_prompt()
    review = call_openai(prompt)
    save_review(review)

    print("AI evidence review complete.")
    print(f"Model used: {MODEL}")
    print(f"Review saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

