import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from build_published_article import (
    build_short_article,
    complete_research_state_lines,
    recent_reading_lines,
    recent_sources_for_pattern,
    research_appendix_lines,
)


def finding(status, **overrides):
    record = {
        "candidate_pattern": "Test Pattern",
        "plain_language_description": "A traceable pattern under test.",
        "research_question": "Does the evidence sustain this candidate?",
        "research_strength_status": status,
        "status_rationale": "The current evidence determines this bounded research label.",
        "supporting_evidence": ["Source A supports the bounded observation."],
        "counterevidence": [],
        "rival_explanations": ["A non-theological process may explain the recurrence."],
        "known_limitations": ["The source set is small."],
        "failure_conditions": ["A better rival explanation would weaken the candidate."],
        "unresolved_tensions": [],
        "provenance": ["research/source-a.md"],
        "provenance_status": "traceable",
        "divine_core_interpretation_status": "interpretation_not_evaluated",
        "does_not_prove": ["Recurrence does not prove theological meaning."],
        "public_final_ready": False,
    }
    record.update(overrides)
    return record


def render(*records):
    return "\n".join(complete_research_state_lines({"research_findings": list(records)}))


class ReportingReformTests(unittest.TestCase):
    @patch("build_published_article.generate_daily_reflection_image", return_value=Path("reflection.svg"))
    @patch("build_published_article.generate_daily_pattern_image", return_value=Path("pattern.svg"))
    def test_primary_report_preserves_complete_illustrated_article(self, _pattern_image, _reflection_image):
        output = build_short_article(datetime(2026, 7, 18, tzinfo=timezone.utc))
        expected = (
            "# A Priest Prayer Book Reading Of Image Of God Pattern",
            "![Today's pattern image](pattern.svg)",
            "![Today's reflection image](reflection.svg)",
            "## Today's Office",
            "## The Pattern In The Room",
            "## Today’s Discovery",
            "## What Changed Since Yesterday",
            "## The Theologian Beside The Prayer Book",
            "## The 1928 Prayer Book Test",
            "## Today's Rule Of Life",
            "## Collect",
            "## Research Behind This Reflection",
            "## Recent Reading Behind This Pattern",
            "## Quiet Notes For The Reader",
        )
        positions = [output.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))

    @patch("build_published_article.generate_daily_reflection_image", return_value=Path("reflection.svg"))
    @patch("build_published_article.generate_daily_pattern_image", return_value=Path("pattern.svg"))
    def test_public_ending_replaces_only_complete_inventory(self, _pattern_image, _reflection_image):
        output = build_short_article(datetime(2026, 7, 18, tzinfo=timezone.utc))
        self.assertNotIn("## Complete Research State", output)
        self.assertIn("## Research Behind This Reflection", output)

    @patch("build_published_article.generate_daily_reflection_image", return_value=Path("reflection.svg"))
    @patch("build_published_article.generate_daily_pattern_image", return_value=Path("pattern.svg"))
    def test_quiet_notes_remain_after_readable_ending(self, _pattern_image, _reflection_image):
        output = build_short_article(datetime(2026, 7, 18, tzinfo=timezone.utc))
        self.assertGreater(output.index("## Quiet Notes For The Reader"), output.index("## Recent Reading Behind This Pattern"))

    @patch("build_published_article.generate_daily_reflection_image", return_value=Path("reflection.svg"))
    @patch("build_published_article.generate_daily_pattern_image", return_value=Path("pattern.svg"))
    def test_public_report_links_to_appendix(self, _pattern_image, _reflection_image):
        output = build_short_article(datetime(2026, 7, 18, tzinfo=timezone.utc))
        self.assertIn("final_book_report_research_appendix.md", output)

    def test_recent_source_limit_is_five(self):
        source = {
            "id": "https://doi.org/10.1086/341240",
            "title": "Brains, Bodies, Selves, and Science",
            "url": "https://doi.org/10.1086/341240",
        }
        selected = recent_sources_for_pattern(
            {"name": "Image Of God Pattern"},
            {"new_sources": [source] * 8},
        )
        self.assertLessEqual(len(selected), 5)

    def test_fewer_than_five_recent_sources_are_allowed(self):
        selected = recent_sources_for_pattern(
            {"name": "Image Of God Pattern"},
            {"new_sources": [{"id": "unrelated", "title": "Unrelated", "url": "https://example.invalid"}]},
        )
        self.assertEqual([], selected)

    def test_keyword_only_source_is_not_selected(self):
        selected = recent_sources_for_pattern(
            {"name": "Image Of God Pattern"},
            {"new_sources": [{"id": "keyword-only", "title": "Image God dignity", "url": "https://example.invalid"}]},
        )
        self.assertEqual([], selected)

    def test_untraceable_curated_source_is_excluded(self):
        selected = recent_sources_for_pattern(
            {"name": "Image Of God Pattern"},
            {"new_sources": [{"id": "https://doi.org/10.1086/341240", "title": "Missing URL"}]},
        )
        self.assertEqual([], selected)

    def test_recent_reading_has_relationship_and_readable_explanation(self):
        selected = recent_sources_for_pattern(
            {"name": "Image Of God Pattern"},
            {"new_sources": [{"id": "https://doi.org/10.1086/341240", "title": "Brains, Bodies, Selves, and Science", "url": "https://doi.org/10.1086/341240"}]},
        )
        output = "\n".join(recent_reading_lines(selected))
        self.assertIn("**Qualifies the pattern.**", output)
        self.assertGreaterEqual(len(selected[0]["explanation"].split()), 20)

    def test_appendix_retains_all_structured_fields_and_back_link(self):
        output = "\n".join(research_appendix_lines({"research_findings": [finding("supported_with_qualifications")]}, []))
        for label in (
            "Plain-language description", "Research question", "Research-strength status",
            "Status rationale", "Supporting evidence", "Counterevidence", "Rival explanations",
            "Known limitations", "Failure conditions", "Unresolved tensions", "Provenance",
            "Provenance status", "Divine Core theological interpretation",
            "What this finding does not prove", "Presentation metadata",
        ):
            self.assertIn(label, output)
        self.assertIn("final_book_report.md", output)

    def test_appendix_preserves_recent_source_traceability(self):
        source = {
            "id": "stable-id", "title": "Traceable Source", "url": "https://example.test/source",
            "relationship": "Qualifies the pattern", "automated_evidence_label": "candidate",
            "confidence_effect": "none", "review_status": "pending", "qualification": "Bounded claim.",
        }
        output = "\n".join(research_appendix_lines({"research_findings": [finding("weak_candidate")]}, [source]))
        self.assertIn("stable-id", output)
        self.assertIn("https://example.test/source", output)
        self.assertIn("Qualifies the pattern", output)

    def test_strong_finding_is_visible_with_support(self):
        output = render(finding("strongly_supported_candidate"))
        self.assertIn("Strongly Supported Candidate: Test Pattern", output)
        self.assertIn("Source A supports the bounded observation.", output)

    def test_weak_finding_is_visible_with_cautious_label(self):
        output = render(finding("weak_candidate"))
        self.assertIn("Weak Candidate: Test Pattern", output)
        self.assertIn("The source set is small.", output)

    def test_conflicting_finding_shows_both_sides(self):
        output = render(
            finding(
                "conflicting_evidence",
                counterevidence=["Source B materially opposes the proposal."],
            )
        )
        self.assertIn("Conflicting Evidence: Test Pattern", output)
        self.assertIn("Source A supports", output)
        self.assertIn("Source B materially opposes", output)

    def test_insufficient_evidence_is_a_visible_result(self):
        output = render(
            finding(
                "insufficient_evidence",
                supporting_evidence=[],
                status_rationale="Primary evidence and comparison cases are missing.",
            )
        )
        self.assertIn("Insufficient Evidence: Test Pattern", output)
        self.assertIn("Primary evidence and comparison cases are missing.", output)
        self.assertIn("Incomplete or unavailable.", output)

    def test_pattern_not_supported_is_visible(self):
        output = render(
            finding(
                "pattern_not_supported",
                counterevidence=["The tested evidence does not sustain the proposal."],
            )
        )
        self.assertIn("Pattern Not Supported: Test Pattern", output)
        self.assertIn("does not sustain the proposal", output)

    def test_unresolved_question_shows_tensions_and_needs(self):
        output = render(
            finding(
                "unresolved_research_question",
                unresolved_tensions=["Two live explanations remain indistinguishable."],
                known_limitations=["More discriminating evidence is needed."],
            )
        )
        self.assertIn("Unresolved Research Question: Test Pattern", output)
        self.assertIn("Two live explanations remain indistinguishable.", output)
        self.assertIn("More discriminating evidence is needed.", output)

    def test_not_public_final_ready_still_appears(self):
        output = render(finding("supported_with_qualifications", public_final_ready=False))
        self.assertIn("Supported with Qualifications: Test Pattern", output)
        self.assertIn("`public_final_ready`: `false`", output)
        self.assertIn("does not determine visibility", output)

    def test_unsafe_private_malformed_and_untraceable_records_are_withheld(self):
        output = render(
            finding("weak_candidate", candidate_pattern="Private", private_or_sensitive=True),
            finding("weak_candidate", candidate_pattern="Unsafe", unsafe_to_render=True, withhold_reason="Unauthenticated quotation withheld."),
            "malformed",
            finding("weak_candidate", candidate_pattern="No Provenance", provenance=[]),
        )
        self.assertIn("Safely Withheld Records", output)
        self.assertIn("Private or sensitive research record withheld.", output)
        self.assertIn("Unauthenticated quotation withheld.", output)
        self.assertIn("Malformed research record.", output)
        self.assertIn("Untraceable research record withheld: No Provenance.", output)
        self.assertNotIn("### Weak Candidate: Private", output)


if __name__ == "__main__":
    unittest.main()
