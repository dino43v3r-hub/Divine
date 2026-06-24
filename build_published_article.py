from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


OUTPUT_PATH = Path("reports/published/final_book_report.md")
DAILY_IMAGE_ALIAS_PATH = Path("reports/published/daily_pattern_image.svg")
REFERENCES_PATH = Path("references/references.json")
DAILY_DIGEST_PATH = Path("references/daily_research_digest.json")
KNOWLEDGE_INDEX_PATH = Path("reports/knowledge_retrieval_index.json")
REVIEW_AUDIT_PATH = Path("reports/review_rules_audit.json")
REVIEW_GAP_QUEUE_PATH = Path("reports/review_gap_queue.json")
FRICTION_LAYERS_PATH = Path("research_documents/friction_layers.json")
THEOLOGICAL_FOUNDATIONS_PATH = Path("research_documents/theological_foundations.json")
REVELATION_LAYER_PATH = Path("research_documents/revelation_layer.json")
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
        "common": "Every person matters before they produce, perform, succeed, or impress anyone.",
        "theologian_judgment": "Theologians should judge this pattern by whether it protects the image of God in weak, wounded, disabled, poor, unborn, elderly, imprisoned, displaced, and overlooked people.",
        "evaluation_question": "Does this pattern make ordinary people more likely to honor human dignity in daily life?",
        "weakens_if": "It weakens if dignity becomes a slogan while real vulnerable people remain ignored or ranked by usefulness.",
        "candidate": "God gives persons dignity before usefulness; the faithful response is truthful worship, humble love, justice for vulnerable people, patient repair, and faithful refusal to rank people by performance.",
    },
    "Cross And Reversal Pattern": {
        "movement": "Power -> Humility | Violence -> Forgiveness | Suffering -> Redemption | Death -> Resurrection",
        "thesis": "The cross is read as God's judgment on violent power and God's mercy for wounded people.",
        "common": "God's way of saving does not flatter power; it tells the truth, protects the harmed, and lets hope come through mercy and resurrection.",
        "theologian_judgment": "Theologians should judge this pattern by whether it keeps the cross centered on Christ without romanticizing pain or asking victims to carry injustice quietly.",
        "evaluation_question": "Does this pattern help people tell the truth about harm while moving toward mercy, justice, and hope?",
        "weakens_if": "It weakens if cross-language protects abusers, silences lament, or treats suffering itself as holy.",
        "candidate": "God reveals holy love by reversing coercive power through the cross; the faithful response is truth-telling, humble repentance, justice for harmed people, patient repair, and faithful mercy without denial.",
    },
    "Creation-To-Consciousness Pattern": {
        "movement": "Physical Order -> Life -> Consciousness -> Moral Awareness -> Worship",
        "thesis": "Creation, life, mind, moral awareness, and worship are explored as layered gifts.",
        "common": "Creation invites wonder, but wonder should turn into humility, care for bodies, and responsibility for the world.",
        "theologian_judgment": "Theologians should judge this pattern by whether it honors creation as gift without turning science, intelligence, or consciousness into a ladder of superiority.",
        "evaluation_question": "Does this pattern create wonder and responsibility without pretending science mechanically proves worship?",
        "weakens_if": "It weakens if it ignores evolution, animal suffering, ecological loss, disability, or natural explanations.",
        "candidate": "God gives ordered creation, life, consciousness, and moral awareness as gifts; the faithful response is humble wonder, truthful stewardship, just care for bodies and creation, patient learning, and worshipful faithfulness.",
    },
    "Trinity-As-Behavior Pattern": {
        "movement": "Father Creates -> Son Redeems -> Spirit Transforms",
        "thesis": "Doctrine is tested by practice: receiving life as gift, following Christ, and discerning Spirit-led transformation.",
        "common": "True doctrine should become visible as love, humility, holiness, unity, service, and patient faithfulness.",
        "theologian_judgment": "Theologians should judge this pattern by whether Father, Son, and Spirit remain distinct and united while the practical fruit stays accountable to Scripture, creed, and worship.",
        "evaluation_question": "Does this pattern keep the Trinity Christian, concrete, and fruitful rather than vague or controlling?",
        "weakens_if": "It weakens if the Trinity becomes a metaphor for group energy, authoritarian control, modalism, or three separate gods.",
        "candidate": "God's triune work appears as creation received, redemption followed, and Spirit-led transformation tested by truth, love, humility, justice, worship, patience, and faithfulness.",
    },
    "Providence And Contingency Pattern": {
        "movement": "Stable Law -> Contingent Events -> Emergent Complexity -> Meaningful History",
        "thesis": "Providence is treated as trust inside contingency, not certainty about hidden causes.",
        "common": "Faithfulness means trusting God and acting well without pretending we know why every event happened.",
        "theologian_judgment": "Theologians should judge this pattern by whether it teaches trust, prayer, repentance, courage, and service while leaving room for grief, chance, mystery, and unfinished history.",
        "evaluation_question": "Does this pattern help ordinary people act faithfully inside uncertainty?",
        "weakens_if": "It weakens if it explains tragedy too neatly, blames victims, denies chance, or borrows science language beyond its scope.",
        "candidate": "God's providence is discerned as faithful trust inside lawful but contingent history; the faithful response is truthful humility, just action, patient endurance, worship, and faithfulness without pretending to know every cause.",
    },
}

DAILY_PATTERN_EXTENSIONS = {
    "Image Of God Pattern": {
        "case_study": "A congregation notices that its most visible ministries praise the productive, articulate, and financially stable, while a disabled member and an elderly caregiver are treated as burdens. This pattern asks whether the church will reorganize its attention around gift, dignity, and belonging before usefulness.",
        "theologian_panel": [
            "Irenaeus would ask whether human life is being received as created for communion with God, not reduced to capacity or status.",
            "Aquinas would ask whether dignity is grounded in God as creator and end, not in usefulness to the community.",
            "Bonhoeffer would ask whether the church protects concrete neighbors, not only an abstract idea of humanity.",
            "James Cone or M. Shawn Copeland would ask whether dignity language confronts racialized and embodied harm or merely decorates the powerful.",
        ],
        "hard_objection": "A skeptic might say dignity language is a social achievement built through rights movements, empathy, law, and shared vulnerability, not evidence of a divine pattern. The report should admit that this rival explanation can account for much of the visible pattern.",
        "confidence_language": "Pastorally useful with limits: strong enough to guide daily practice, but still provisional as a pattern claim.",
        "faithful_response": "Today, honor one person before they are useful to you.",
        "interesting_not_true": "The recurrence of dignity language is interesting, but it becomes theologically responsible only when tested by Christ, Scripture, vulnerable people, and real practice.",
    },
    "Cross And Reversal Pattern": {
        "case_study": "A family wants reconciliation after serious harm, but the harmed person is being pressured to forgive quickly so everyone else can feel better. This pattern asks whether the cross is being used to tell the truth and protect the wounded, or misused to rush pain into silence.",
        "theologian_panel": [
            "Augustine would ask whether love is rightly ordered or whether peace is being confused with avoidance.",
            "Luther would ask whether the theology of the cross is exposing false power rather than baptizing it.",
            "Bonhoeffer would ask whether forgiveness has become cheap grace without repentance or costly repair.",
            "James Cone or Delores Williams would ask whether cross-language liberates the oppressed or asks them to endure more violence.",
        ],
        "hard_objection": "A wounded reader might say this pattern can become spiritually dangerous because Christians have often used suffering language to keep victims quiet. The report should let that objection weaken careless versions of the pattern.",
        "confidence_language": "Beautiful but risky: powerful when centered on Christ and justice, unsafe when used without protection and repair.",
        "faithful_response": "Today, tell the truth about harm without using mercy to erase justice.",
        "interesting_not_true": "Reversal is compelling, but beauty is not proof; this pattern must be judged by whether it protects the harmed and follows Christ.",
    },
    "Creation-To-Consciousness Pattern": {
        "case_study": "A student feels wonder while studying biology, consciousness, and the night sky, but also sees animal suffering, ecological damage, disability, and death. This pattern asks whether wonder can become humility and care without turning creation into a simplistic proof.",
        "theologian_panel": [
            "Athanasius would ask whether creation is being understood through the Word who gives and sustains life.",
            "Aquinas would ask whether natural order points to God without pretending every scientific question has become theology.",
            "John Polkinghorne would ask whether science is being respected on its own terms before theological reflection begins.",
            "Disability theologians would ask whether consciousness and ability are being used to rank creatures or persons.",
        ],
        "hard_objection": "Science, evolution, cognition, and culture can explain much of the movement from order to life to mind without requiring a theological conclusion. The report should not smuggle God in where the evidence only supports wonder and humility.",
        "confidence_language": "Promising but needs pressure: useful for wonder and stewardship, not mature as a proof claim.",
        "faithful_response": "Today, let wonder become care for a body, a creature, or a place.",
        "interesting_not_true": "Awe before creation is interesting, but the pattern stays honest only when natural explanations and suffering remain visible.",
    },
    "Trinity-As-Behavior Pattern": {
        "case_study": "A church says it believes orthodox doctrine, but its common life is anxious, competitive, controlling, and unkind. This pattern asks whether Trinitarian language is becoming worshipful love, humble service, and Spirit-tested fruit, or staying as correct words without visible formation.",
        "theologian_panel": [
            "Gregory of Nazianzus would ask whether Father, Son, and Spirit are confessed without confusion or division.",
            "Augustine would ask whether the doctrine trains love rather than curiosity alone.",
            "Karl Barth would ask whether the pattern begins with God's self-revelation, not a human analogy projected upward.",
            "Zizioulas, Jennings, or Oduyoye would ask whether communion becomes concrete hospitality, justice, and belonging.",
        ],
        "hard_objection": "A critic might say this turns the Trinity into behavior advice, which risks flattening doctrine into ethics. The report should keep the doctrine first and treat behavior as fruit, not as the source or definition of God.",
        "confidence_language": "Developing evidence: fruitful as a practical test, but doctrinally risky if it becomes mere symbolism.",
        "faithful_response": "Today, test one belief by whether it produces humility, love, and service.",
        "interesting_not_true": "Practical fruit is important, but usefulness is not revelation; the pattern must remain accountable to Scripture, creed, and worship.",
    },
    "Providence And Contingency Pattern": {
        "case_study": "Someone loses a job, faces illness, or watches a plan collapse, and friends rush to explain what God must be doing. This pattern asks whether faith can pray, act, grieve, repent, and endure without pretending to know God's hidden reasons.",
        "theologian_panel": [
            "Augustine would ask whether trust in providence is becoming love of God rather than control over explanation.",
            "Calvin would ask whether God's care is being confessed with reverence instead of speculation.",
            "Karl Barth would ask whether providence is being read through Jesus Christ rather than through bare events.",
            "Pastoral and trauma theologians would ask whether the claim is safe for sufferers or whether it blames them.",
        ],
        "hard_objection": "A skeptic might say humans create providence stories to survive uncertainty, reduce anxiety, and impose meaning after the fact. The report should admit that psychology and history can explain many providence claims without proving divine action.",
        "confidence_language": "Pastorally useful with limits: strong as a discipline of trust, weak as an explanation of hidden causes.",
        "faithful_response": "Today, act faithfully without explaining everything.",
        "interesting_not_true": "Meaning inside uncertainty is interesting, but the pattern should stop where grief, chance, and mystery require silence.",
    },
}

DEFAULT_CANDIDATE_PATTERN = {
    "name": "Integrated Gift-And-Faithfulness Pattern",
    "movement": "Gift -> Recognition -> Responsibility -> Sacrificial Love -> Repair -> Worshipful Faithfulness",
    "plain": "The project is testing a pattern in ordinary life without treating it as proof by itself.",
    "theologian_judgment": "Theologians should judge this pattern by Scripture, Christ, doctrine, lived fruit, harm safeguards, and honest limits.",
    "evaluation_question": "Does this pattern help people love God and neighbor truthfully?",
    "weakens_if": "It weakens if it overclaims, harms people, ignores rival explanations, or outruns the sources.",
    "case_study": "An ordinary person notices a recurring theme in life, faith, suffering, or culture. The project asks whether that theme should become faithful practice, remain a question, or be set aside.",
    "theologian_panel": [
        "A faithful theologian would ask whether the pattern begins with Christ rather than fascination with recurrence.",
        "A pastoral theologian would ask whether the pattern protects vulnerable people in real life.",
    ],
    "hard_objection": "A rival explanation may account for the pattern without theology, so the report should not treat recurrence as proof.",
    "confidence_language": "Promising but needs pressure: interesting enough to study, not strong enough to overclaim.",
    "faithful_response": "Today, let the pattern serve truth, love, humility, justice, and worship.",
    "interesting_not_true": "Interesting is not the same as true; the pattern remains secondary and provisional.",
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

DAILY_LETTER_OPENINGS = [
    "I spent today's reading with one question in the foreground:",
    "What stayed with me today was not the amount of material, but the shape of one claim:",
    "Today's thread felt quieter than a headline. It kept asking:",
    "The thing I would hand you from today's work is this:",
    "I found myself circling one pressure point today:",
    "Today's discovery felt less like an answer and more like a test:",
    "If I were sitting across from you with this report open, I would start here:",
]

DAILY_LETTER_CLOSINGS = [
    "That is the piece I would keep close today.",
    "I would not rush it further than that.",
    "That feels like enough truth to carry without forcing the rest.",
    "The pattern is useful only if it becomes gentler, truer, and more responsible in ordinary life.",
    "I would let this one stay practical before I let it become impressive.",
    "That is where the pattern feels most alive to me today.",
    "I would rather keep this humble and usable than grand and brittle.",
]

DAILY_DIARY_LENSES = [
    {
        "name": "ordinary life",
        "question": "Where would this show up before anyone calls it theology?",
        "image_note": "The visual leans toward ordinary practice: a path, a few signs, and one place to begin.",
    },
    {
        "name": "pastoral safety",
        "question": "Could this be spoken gently beside someone who is hurting?",
        "image_note": "The visual leaves more open space, because some patterns should not crowd grief.",
    },
    {
        "name": "theologian pressure",
        "question": "Which trusted voices would slow this down and make it more truthful?",
        "image_note": "The visual gathers the pattern into a conversation rather than a single conclusion.",
    },
    {
        "name": "hard objection",
        "question": "What would make this pattern fail?",
        "image_note": "The visual includes interruption and contrast, because good objections belong on the page.",
    },
    {
        "name": "faithful response",
        "question": "What would a person actually do with this today?",
        "image_note": "The visual points toward one concrete response instead of a finished theory.",
    },
    {
        "name": "mystery",
        "question": "Where should I stop explaining and let the unknown remain?",
        "image_note": "The visual keeps a quiet center, because not every faithful reading ends in closure.",
    },
    {
        "name": "repair",
        "question": "Does this pattern help love become more honest and reparative?",
        "image_note": "The visual emphasizes repair: separated pieces drawn back toward truthful care.",
    },
]

THEOLOGIAN_DAILY_VOICES = [
    {
        "name": "Irenaeus",
        "angle": "creation, communion, and the patient maturing of human life in God",
        "comment": "Irenaeus would ask whether the pattern helps creation move toward communion with God, or whether it merely admires a shape without leading persons toward healing and fullness.",
    },
    {
        "name": "Augustine",
        "angle": "rightly ordered love",
        "comment": "Augustine would ask what this pattern does to love. If it bends love toward God and neighbor, it may be useful; if it bends love back toward pride, control, or curiosity, it needs repentance.",
    },
    {
        "name": "Aquinas",
        "angle": "created order, virtue, and the final end of human life",
        "comment": "Aquinas would ask whether the pattern participates in truth, goodness, and ordered love, while refusing to confuse a created sign with God himself.",
    },
    {
        "name": "Julian of Norwich",
        "angle": "mercy, suffering, and hope without denial",
        "comment": "Julian would listen for whether the pattern can speak mercy without becoming glib about pain. A pattern that cannot sit gently with suffering is not yet wise.",
    },
    {
        "name": "Martin Luther",
        "angle": "the cross as judgment on spiritual boasting",
        "comment": "Luther would press the pattern under the cross and ask whether it exposes false glory or becomes another way for religious people to sound impressive.",
    },
    {
        "name": "Karl Barth",
        "angle": "God's self-revelation in Jesus Christ",
        "comment": "Barth would ask whether the pattern begins with God's revelation in Christ or whether it tries to climb up to God from human observation.",
    },
    {
        "name": "Dietrich Bonhoeffer",
        "angle": "costly discipleship and concrete obedience",
        "comment": "Bonhoeffer would ask what this pattern costs in actual obedience. If it does not become truth, service, courage, and neighbor-love, it remains too abstract.",
    },
    {
        "name": "James Cone",
        "angle": "liberation, the cross, and the oppressed",
        "comment": "Cone would ask whether the pattern stands with people under threat or whether it lets theology remain comfortable while suffering people carry the burden.",
    },
    {
        "name": "Sarah Coakley",
        "angle": "prayer, desire, and contemplative discipline",
        "comment": "Coakley would ask whether the pattern is being purified by prayer, or whether desire is quietly shaping the conclusion before discernment has done its work.",
    },
]


def daily_image_path(generated: datetime) -> Path:
    date_slug = generated.strftime("%Y-%m-%d")
    return DAILY_IMAGE_ALIAS_PATH.with_name(f"daily_pattern_image_{date_slug}.svg")


def daily_reflection_image_path(generated: datetime) -> Path:
    date_slug = generated.strftime("%Y-%m-%d")
    return DAILY_IMAGE_ALIAS_PATH.with_name(f"daily_reflection_image_{date_slug}.svg")


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


def daily_lens(generated: datetime) -> dict:
    return DAILY_DIARY_LENSES[generated.date().toordinal() % len(DAILY_DIARY_LENSES)]


def daily_theologian(generated: datetime) -> dict:
    return THEOLOGIAN_DAILY_VOICES[generated.date().toordinal() % len(THEOLOGIAN_DAILY_VOICES)]


def anglican_1928_reflection(candidate_pattern: dict, lens: dict) -> str:
    pattern_name = candidate_pattern.get("name", "this pattern")
    return (
        "An Anglican priest shaped by the 1928 Book of Common Prayer would not begin by asking whether "
        f"{pattern_name} is clever. He would ask how it sounds after confession, Scripture, the creeds, "
        "the collects, the Holy Communion, and the ordinary offices of prayer. He would want the pattern "
        "to become reverence, repentance, charity, and steady duty. Under today's lens of "
        f"{lens['name']}, he would probably say: test the idea in prayer first, then in conduct; let it "
        "make you more truthful at home, more merciful toward the weak, more faithful in worship, and "
        "less eager to explain what belongs to God."
    )


def generate_daily_pattern_image(candidate_pattern: dict, digest: dict, audit: dict, generated: datetime) -> Path:
    profile = daily_visual_profile(candidate_pattern, generated)
    bg, ink, warm, cool, gold = profile["colors"]
    date_label = generated.strftime("%B %d, %Y")
    lead_title = profile["title"]
    motif = profile["motif"]
    candidate_lines = wrap_words(candidate_pattern.get("candidate", ""), 74, 3)
    lens = daily_lens(generated)
    diary_label = f"Today I am reading through the lens of {lens['name']}: {lens['question']}"

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
  <text x="96" y="456" class="small">{escape(diary_label)}</text>
</svg>
'''
    image_path = daily_image_path(generated)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_text(svg, encoding="utf-8")
    DAILY_IMAGE_ALIAS_PATH.write_text(svg, encoding="utf-8")
    return image_path


def generate_daily_reflection_image(candidate_pattern: dict, generated: datetime) -> Path:
    profile = daily_visual_profile(candidate_pattern, generated)
    lens = daily_lens(generated)
    bg, ink, warm, cool, gold = profile["colors"]
    date_label = generated.strftime("%B %d, %Y")
    variant = generated.date().toordinal() % 5
    title = f"Diary page: {lens['name']}"
    question_lines = wrap_words(lens["question"], 40, 3)
    response_lines = wrap_words(candidate_pattern.get("faithful_response", ""), 34, 3)
    margin_color = [warm, cool, gold, warm, cool][variant]
    card_color = [cool, warm, gold, cool, warm][variant]
    line_y = [126, 158, 190, 222, 254, 286, 318, 350, 382, 414]
    ruled_lines = "".join(
        f'<line x1="124" y1="{y}" x2="576" y2="{y}" stroke="{ink}" stroke-width="1.4" opacity="0.18"/>'
        for y in line_y
    )
    question_svg = "".join(
        f'<text x="146" y="{146 + index * 30}" class="diary">{escape(line)}</text>'
        for index, line in enumerate(question_lines)
    )
    response_svg = "".join(
        f'<text x="638" y="{282 + index * 28}" class="cardtext">{escape(line)}</text>'
        for index, line in enumerate(response_lines)
    )
    day_mark = generated.strftime("%d")
    paper_tilt = [-2, 1, -1, 2, 0][variant]
    card_tilt = [2, -2, 1, -1, 0][variant]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="540" viewBox="0 0 900 540" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">A daily diary page image with notebook paper, margin notes, and an application card.</desc>
  <style>
    .eyebrow {{ font: 700 14px Arial, sans-serif; letter-spacing: 0; fill: {ink}; opacity: 0.68; }}
    .title {{ font: 700 34px Georgia, serif; letter-spacing: 0; fill: {ink}; }}
    .diary {{ font: 23px Georgia, serif; letter-spacing: 0; fill: {ink}; }}
    .label {{ font: 700 13px Arial, sans-serif; letter-spacing: 0; fill: {ink}; opacity: 0.72; }}
    .cardtitle {{ font: 700 22px Arial, sans-serif; letter-spacing: 0; fill: #ffffff; }}
    .cardtext {{ font: 18px Arial, sans-serif; letter-spacing: 0; fill: #ffffff; opacity: 0.94; }}
    .small {{ font: 14px Arial, sans-serif; letter-spacing: 0; fill: {ink}; opacity: 0.70; }}
  </style>
  <rect width="900" height="540" fill="{bg}"/>
  <rect x="0" y="0" width="900" height="540" fill="{ink}" opacity="0.05"/>
  <g transform="rotate({paper_tilt} 340 270)">
    <rect x="82" y="54" width="520" height="430" rx="10" fill="#fffdf7" stroke="{ink}" stroke-width="2" opacity="0.96"/>
    <rect x="82" y="54" width="58" height="430" rx="10" fill="{margin_color}" opacity="0.20"/>
    <line x1="142" y1="72" x2="142" y2="466" stroke="{warm}" stroke-width="2" opacity="0.40"/>
    {ruled_lines}
    <text x="166" y="96" class="eyebrow">Research diary | {escape(date_label)}</text>
    <text x="166" y="126" class="title">{escape(profile["title"])}</text>
    <text x="146" y="146" class="label">Question I carried</text>
    <text x="104" y="108" class="title">{escape(day_mark)}</text>
  </g>
  <g transform="rotate({paper_tilt} 340 270)">
  {question_svg}
    <text x="146" y="310" class="label">Why this page feels different</text>
    <text x="146" y="342" class="diary">{escape(lens["image_note"])}</text>
  </g>
  <g transform="rotate({card_tilt} 714 306)">
    <rect x="606" y="176" width="232" height="206" rx="24" fill="{card_color}" opacity="0.94"/>
    <circle cx="798" cy="216" r="18" fill="#ffffff" opacity="0.22"/>
    <text x="638" y="226" class="cardtitle">Carry this</text>
  {response_svg}
  </g>
  <path d="M664 430 C706 404 766 408 810 442" fill="none" stroke="{ink}" stroke-width="4" opacity="0.18"/>
  <text x="606" y="470" class="small">This image is a diary page, not a pattern map.</text>
</svg>
'''
    image_path = daily_reflection_image_path(generated)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_text(svg, encoding="utf-8")
    DAILY_IMAGE_ALIAS_PATH.with_name("daily_reflection_image.svg").write_text(svg, encoding="utf-8")
    return image_path


def current_candidate_pattern(index: dict, generated_at: datetime | None = None) -> dict:
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
    supported = [(name, values) for name, values in ranked if values["score"] > 0]
    if not supported:
        return dict(DEFAULT_CANDIDATE_PATTERN)

    if generated_at is None:
        generated_at = datetime.now(timezone.utc)
    daily_index = generated_at.date().toordinal() % len(supported)
    top_name, top_counts = supported[daily_index]

    profile = PATTERN_PROFILES[top_name]
    result = {
        "name": top_name,
        "movement": profile["movement"],
        "plain": profile["common"],
        "theologian_judgment": profile["theologian_judgment"],
        "evaluation_question": profile["evaluation_question"],
        "weakens_if": profile["weakens_if"],
        "candidate": profile["candidate"],
        "basis": (
            f"This is today's rotating focus from {len(supported)} supported pattern family/families. "
            f"It has {top_counts['documents']} indexed document(s), {top_counts['review_notes']} review note(s), "
            f"and a support score of {top_counts['score']}. The rotation lets the book report focus on a fresh pattern each day without treating the focus as the final winner."
        ),
        "counts": counts,
    }
    result.update(DAILY_PATTERN_EXTENSIONS.get(top_name, {}))
    return result


def daily_focus_lines(candidate_pattern: dict, include_selection_note: bool = True) -> list[str]:
    lines = [
        f"**Current candidate divine pattern:** {candidate_pattern['candidate']}",
        "",
        f"**In plain language:** {candidate_pattern.get('plain', DEFAULT_CANDIDATE_PATTERN['plain'])}",
        "",
        f"**Today case study:** {candidate_pattern.get('case_study', DEFAULT_CANDIDATE_PATTERN['case_study'])}",
        "",
        "**Theologian panel:**",
        "",
        *[
            f"- {voice}"
            for voice in candidate_pattern.get(
                "theologian_panel",
                DEFAULT_CANDIDATE_PATTERN["theologian_panel"],
            )
        ],
        "",
        f"**Theologian judgment for ordinary readers:** {candidate_pattern.get('theologian_judgment', DEFAULT_CANDIDATE_PATTERN['theologian_judgment'])}",
        "",
        f"**Hard objection:** {candidate_pattern.get('hard_objection', DEFAULT_CANDIDATE_PATTERN['hard_objection'])}",
        "",
        f"**Common-person test:** {candidate_pattern.get('evaluation_question', DEFAULT_CANDIDATE_PATTERN['evaluation_question'])}",
        "",
        f"**Confidence in plain English:** {candidate_pattern.get('confidence_language', DEFAULT_CANDIDATE_PATTERN['confidence_language'])}",
        "",
        f"**What would weaken it:** {candidate_pattern.get('weakens_if', DEFAULT_CANDIDATE_PATTERN['weakens_if'])}",
        "",
        f"**Faithful response today:** {candidate_pattern.get('faithful_response', DEFAULT_CANDIDATE_PATTERN['faithful_response'])}",
        "",
        f"**Why interesting is not the same as true:** {candidate_pattern.get('interesting_not_true', DEFAULT_CANDIDATE_PATTERN['interesting_not_true'])}",
        "",
        f"**Movement:** {candidate_pattern['movement']}",
        "",
    ]
    if include_selection_note:
        lines.extend([f"**Selection note:** {candidate_pattern['basis']}", ""])
    return lines


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
            f"- {rule}: {int(values.get('present', 0)):,} rule-present; {int(values.get('review_companion', 0)):,} reviewed companion; {int(values.get('machine_drafted', 0)):,} machine-drafted; {int(values.get('missing', 0)):,} still missing of {int(values.get('total', 0)):,}"
        )
    return lines or ["- No promotion-rule coverage values found."]


def rule_gap_summary(audit: dict, limit: int = 5) -> list[tuple[str, int, int, int, int]]:
    coverage = audit.get("rule_coverage", {}) if audit else {}
    rows = []
    for rule, values in coverage.items():
        missing = int(values.get("missing", 0) or 0)
        machine_drafted = int(values.get("machine_drafted", 0) or 0)
        review_companion = int(values.get("review_companion", 0) or 0)
        present = int(values.get("present", 0) or 0)
        if missing or machine_drafted or review_companion:
            rows.append((rule, missing, machine_drafted, review_companion, present))
    rows.sort(key=lambda item: (item[1], item[2] + item[3], -item[4], item[0]), reverse=True)
    return rows[:limit]


def next_step_lines(audit: dict, queue_payload: dict, candidate_pattern: dict) -> list[str]:
    totals = audit.get("confidence_tier_totals", {}) if audit else {}
    ready = int(totals.get("reviewed_evidence_ready", 0) or 0)
    developing = int(totals.get("developing_evidence", 0) or 0)
    candidate_leads = int(totals.get("candidate_lead", 0) or 0)
    queue_items = queue_payload.get("items", []) if queue_payload else []
    machine_source_check_items = queue_payload.get("machine_source_check_items", []) if queue_payload else []
    machine_source_check_count = int(queue_payload.get("machine_source_check_count", 0) or 0) if queue_payload else 0
    gaps = rule_gap_summary(audit, limit=4)

    lines = [
        "The report is strongest when it tells you exactly where confidence is blocked. Based on the current audit, the next work should be:",
        "",
    ]

    if ready == 0 and developing:
        lines.extend(
            [
                "1. Move one source from `developing_evidence` to `reviewed_evidence_ready`.",
                f"   Right now the project has {developing:,} developing-evidence records and {ready:,} ready-for-review records. Pick one important source connected to `{candidate_pattern.get('name', 'the leading pattern')}` and complete every required control by hand.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "1. Re-check the strongest ready-for-review source.",
                "   Confirm that its evidence, interpretation, counter-reading, failure condition, and pastoral safety are source-specific rather than generic.",
                "",
            ]
        )

    if gaps:
        gap_text = ", ".join(f"`{rule}` ({missing:,} missing)" for rule, missing, _, _, _ in gaps)
        lines.extend(
            [
                "2. Fill the largest explicit review gaps.",
                f"   The current biggest gaps are {gap_text}. These are the places where the report most needs clearer human judgment.",
                "",
            ]
        )

    if queue_items:
        top = queue_items[0]
        missing = ", ".join(top.get("missing_rules", [])[:5]) or "review controls"
        lines.extend(
            [
                "3. Start with the top item in the review queue.",
                f"   First queued source: `{top.get('path', '')}`. Add source-checked companion notes for: {missing}.",
                "",
            ]
        )

    lines.extend(
        [
            "4. Strengthen today's focus pattern with one hard counter-reading.",
            f"   Today's focus pattern is `{candidate_pattern.get('name', 'the current candidate pattern')}`. Add a serious rival explanation from psychology, sociology, history, disability studies, trauma studies, comparative religion, or philosophy, then state what would weaken the pattern.",
            "",
            "5. Add one pastoral use case and one pastoral rejection case.",
            "   Write a short case where the pattern helps faithful practice, and another where it would become unsafe, glib, coercive, or overconfident. This keeps the report priestly instead of merely impressive.",
            "",
            "6. Source-check machine-drafted companions before trusting them.",
            f"   The project currently has {candidate_leads:,} candidate leads and {machine_source_check_count:,} machine-drafted companion record(s) still requiring source-check. Machine drafts can organize the work, but they should not raise confidence until the source has been directly checked.",
        ]
    )
    if machine_source_check_items:
        top_machine = machine_source_check_items[0]
        lines.extend(
            [
                f"   First machine-draft source-check item: `{top_machine.get('path', '')}`.",
            ]
        )
    return lines


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


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def digest_freshness(digest: dict, generated_at: datetime) -> dict:
    updated_at = parse_timestamp(digest.get("updated_at"))
    if updated_at is None:
        return {
            "updated_at": None,
            "age_days": None,
            "is_stale": True,
            "label": "collector snapshot date not recorded",
            "warning": "The daily collector snapshot does not record an update time, so the report cannot prove these numbers changed today.",
        }

    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=timezone.utc)

    age = generated_at - updated_at.astimezone(timezone.utc)
    age_days = max(age.days, 0)
    label = updated_at.strftime("%Y-%m-%d %H:%M UTC")
    if age_days == 0:
        warning = "Collector snapshot is current for this UTC day."
    else:
        warning = (
            f"Collector snapshot is {age_days} day(s) older than this report. "
            "Run the daily collector before publishing if you expect today's counts to move."
        )

    return {
        "updated_at": updated_at,
        "age_days": age_days,
        "is_stale": age_days > 0,
        "label": label,
        "warning": warning,
    }


def latest_run_count_label(digest: dict, generated_at: datetime) -> str:
    freshness = digest_freshness(digest, generated_at)
    count = int(digest.get("new_count", 0) or 0)
    if freshness["is_stale"]:
        return f"New leads in latest collector run ({freshness['label']}): {count}"
    return f"New leads today: {count}"


def latest_cloud_discovery_lines(digest: dict, reference_catalog: dict, generated_at: datetime) -> list[str]:
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

    freshness = digest_freshness(digest, generated_at)
    lines.append(f"Collector snapshot used for counts: {freshness['label']}")
    lines.append(f"Freshness note: {freshness['warning']}")

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


def revelation_layer_lines(layer: dict) -> list[str]:
    if not layer:
        return ["Revelation layer is missing."]

    lines = [
        layer.get("foundation_statement", ""),
        "",
        f"**Theological flow:** {' -> '.join(layer.get('theological_flow', []))}",
        "",
        "Authority order:",
    ]
    for item in layer.get("authority_order", []):
        lines.append(f"{item.get('rank')}. **{item.get('authority', '')}:** {item.get('use', '')}")
    lines.extend(
        [
            "",
            f"**Acceptance rule:** {layer.get('acceptance_rule', '')}",
            "",
            f"**Beginner summary:** {layer.get('beginner_summary', '')}",
        ]
    )
    outcomes = layer.get("allowed_outcomes", [])
    if outcomes:
        lines.extend(["", "Allowed outcomes:"])
        lines.extend(f"- {item.replace('_', ' ')}" for item in outcomes)
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
    generated_at = datetime.now(timezone.utc)
    generated = generated_at.strftime("%Y-%m-%d %H:%M UTC")
    texts = {name: read(path) for name, path in SOURCE_REPORTS.items()}
    digest = read_json(DAILY_DIGEST_PATH)
    reference_catalog = read_json(REFERENCES_PATH)
    knowledge_index = read_json(KNOWLEDGE_INDEX_PATH)
    review_audit = read_json(REVIEW_AUDIT_PATH)
    candidate_pattern = current_candidate_pattern(knowledge_index, generated_at)
    stats = extract_backend_stats(texts["backend"])
    lane_lines = compact_lane_table(texts["backend"])
    friction_layers = read_friction_layers()
    theological_foundations = read_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    revelation_layer = read_layer(REVELATION_LAYER_PATH)
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
        "## Revelation Layer",
        "",
        *revelation_layer_lines(revelation_layer),
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
        "## Today's Pattern Focus",
        "",
        *daily_focus_lines(candidate_pattern),
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
        *bulletize(latest_cloud_discovery_lines(digest, reference_catalog, generated_at)),
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
    review_gap_queue = read_json(REVIEW_GAP_QUEUE_PATH)
    candidate_pattern = current_candidate_pattern(knowledge_index, generated_at)
    freshness = digest_freshness(digest, generated_at)
    daily_image = generate_daily_pattern_image(candidate_pattern, digest, review_audit, generated_at)
    findings_text = read(Path("reports/divine_pattern_findings.md"))
    friction_layers = read_friction_layers()
    theological_foundations = read_layer(THEOLOGICAL_FOUNDATIONS_PATH)
    revelation_layer = read_layer(REVELATION_LAYER_PATH)
    theological_method = read_layer(THEOLOGICAL_METHOD_PATH)
    pattern_distortion = read_layer(PATTERN_DISTORTION_PATH)
    mystery_layer = read_layer(MYSTERY_LAYER_PATH)
    priestly_discernment = read_layer(PRIESTLY_DISCERNMENT_PATH)
    does_not_prove = read_layer(DOES_NOT_PROVE_PATH)
    science_guardrail = read_layer(SCIENCE_GUARDRAIL_PATH)

    finding_lines = []
    in_pattern_findings = False
    for line in findings_text.splitlines():
        if line == "## Pattern Findings":
            in_pattern_findings = True
            continue
        if not in_pattern_findings:
            continue
        if line.startswith("### "):
            finding_lines.append(line.replace("### ", "- "))
        if len(finding_lines) >= 7:
            break

    foundation_lines = theological_foundations_lines(theological_foundations)
    boundary_lines = does_not_prove_lines(does_not_prove)
    science_lines = science_guardrail_lines(science_guardrail)
    reflection_image = generate_daily_reflection_image(candidate_pattern, generated_at)
    lens = daily_lens(generated_at)
    theologian = daily_theologian(generated_at)
    panel = candidate_pattern.get("theologian_panel", DEFAULT_CANDIDATE_PATTERN["theologian_panel"])
    panel_text = " ".join(panel[:3])
    plain = candidate_pattern.get("plain", DEFAULT_CANDIDATE_PATTERN["plain"])
    objection = candidate_pattern.get("hard_objection", DEFAULT_CANDIDATE_PATTERN["hard_objection"])
    caution = candidate_pattern.get("interesting_not_true", DEFAULT_CANDIDATE_PATTERN["interesting_not_true"])
    response = candidate_pattern.get("faithful_response", DEFAULT_CANDIDATE_PATTERN["faithful_response"])
    response_sentence = response.removeprefix("Today, ").removeprefix("Today ")
    confidence = candidate_pattern.get("confidence_language", DEFAULT_CANDIDATE_PATTERN["confidence_language"])
    diary_lines = [
        "# Divine Pattern Research Diary",
        "",
        f"_Diary entry: {generated_at.strftime('%B %d, %Y')}_",
        "",
        f"![Today's pattern image]({daily_image.name})",
        "",
        f"![Today's reflection image]({reflection_image.name})",
        "",
        "## Morning Note",
        "",
        "I came to the work today with the posture of a priest more than a technician: listening for what may be true, watching for what may harm, and trying not to make a pattern carry more weight than it can bear.",
        "",
        f"The pattern before me is **{candidate_pattern.get('name', 'the current pattern')}**. In plain speech, this is what I see: {plain}",
        "",
        f"I am reading it today through the lens of **{lens['name']}**, and the question that stays with me is: {lens['question']}",
        "",
        "## The Scene In Front Of Me",
        "",
        candidate_pattern.get("case_study", DEFAULT_CANDIDATE_PATTERN["case_study"]),
        "",
        "This is where theology becomes honest. If a pattern cannot enter a room like that with gentleness, patience, and truth, I would rather leave it outside.",
        "",
        "## Question And Answer",
        "",
        f"**Question:** What is this pattern asking me to notice?",
        "",
        f"**Answer:** {candidate_pattern['candidate']}",
        "",
        f"**Question:** What would make me slow down before trusting it?",
        "",
        f"**Answer:** {objection}",
        "",
        f"**Question:** What can I responsibly say today?",
        "",
        f"**Answer:** {confidence}",
        "",
        "## Theologians I Would Want Nearby",
        "",
        panel_text,
        "",
        candidate_pattern.get("theologian_judgment", DEFAULT_CANDIDATE_PATTERN["theologian_judgment"]),
        "",
        "That is the kind of company I want for this project. Not famous names as decoration, but teachers who can slow the mind, purify the claim, and bring it back under Christ.",
        "",
        f"## Today's Chosen Theologian: {theologian['name']}",
        "",
        f"I would especially let {theologian['name']} stand near this pattern today because of {theologian['angle']}. {theologian['comment']}",
        "",
        "## How I Think An Anglican Priest Would Read It",
        "",
        anglican_1928_reflection(candidate_pattern, lens),
        "",
        "## Confession Of Caution",
        "",
        caution,
        "",
        f"What would weaken this pattern is also important: {candidate_pattern.get('weakens_if', DEFAULT_CANDIDATE_PATTERN['weakens_if'])}",
        "",
        "So I do not receive this as proof. I receive it as a disciplined observation, still under Scripture, still under the Church's wisdom, still under the mercy of God.",
        "",
        "## Application For Daily Life",
        "",
        f"Today I would practice it this way: {response_sentence}",
        "",
        "A small application is better than a grand claim. If this pattern is from the neighborhood of truth, it should make someone more truthful, more humble, more just, and more capable of love before it makes anyone feel clever.",
        "",
        "## Closing Prayer",
        "",
        "Lord, let what is true become clear, let what is false lose its shine, and let every pattern bend toward love of You and love of neighbor.",
        "",
        "## Quiet Background",
        "",
        f"Underneath this diary entry, the movement I am tracking is: {candidate_pattern['movement']}. Tomorrow the focus and the diary lens can change, so the entry should not merely repeat itself with a new timestamp.",
        "",
        "The research machinery is still present underneath the page, but I am keeping it out of the foreground. The diary should be the thing you read.",
        "",
    ]
    return "\n".join(diary_lines) + "\n"

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
        "## Input Freshness",
        "",
        f"- Report generated: {generated}",
        f"- Collector snapshot used for discovery counts: {freshness['label']}",
        f"- Freshness note: {freshness['warning']}",
        "",
        f"![Daily pattern image]({daily_image.name})",
        "",
        f"_Daily visual generated from today's rotating focus: {candidate_pattern['name']}._",
        "",
        "## Short Answer",
        "",
        "The project does not claim that patterns prove Christianity or discover God by themselves. It begins with Jesus Christ as God's self-revelation, listens to Scripture as the primary written witness, and then examines recurring patterns across theology, culture, language, suffering, science, art, music, history, and human experience.",
        "",
        "The best current posture is: the system finds possible pattern signals, then tests them under Christ, Scripture, doctrine, Church witness, sin-and-distortion review, serious critique, and mystery. Some conclusions should remain unclear.",
        "",
        "## Today's Pattern Focus",
        "",
        *daily_focus_lines(candidate_pattern),
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
        "The main gap is not source volume. The main gap is clearer separation between evidence, interpretation, analogy, and failure conditions. Reviewed companions now close the named tracking gaps; they still do not raise confidence unless the original source is checked.",
        "",
        "The system now writes a gap-fill queue here:",
        "",
        "- `reports/review_gap_queue.md`",
        "",
        "That queue explains why fields are missing and lists the highest-priority sources that need structured companion reviews.",
        "",
        "## Theological Boundary",
        "",
        "### Christ-Centered Foundation",
        "",
        revelation_layer.get("foundation_statement", foundation_lines[0] if foundation_lines else "Patterns are secondary observations under Christ and Scripture."),
        "",
        f"**Theological flow:** {' -> '.join(revelation_layer.get('theological_flow', ['Christ', 'Scripture', 'Pattern']))}",
        "",
        "### Revelation Authority Order",
        "",
        *[
            f"{item.get('rank')}. **{item.get('authority', '')}:** {item.get('use', '')}"
            for item in revelation_layer.get("authority_order", [])
        ],
        "",
        revelation_layer.get("acceptance_rule", "Patterns are secondary observations and may not become theological claims until tested by Christ, Scripture, doctrine, Church witness, critique, and mystery."),
        "",
        "### Theological Foundations",
        "",
        foundation_lines[0] if foundation_lines else "Pattern recognition is subordinate to Scripture and divine revelation.",
        "",
        "The project keeps this order: Christ first, Scripture as primary written witness, historic Christian doctrine and Church witness, then creation and observed patterns, then human experience and interpretation.",
        "",
        "## Sin, Distortion, Critique, And Mystery Checks",
        "",
        "Every detected pattern must be tested through Creation, Fall, Redemption, and Consummation:",
        "",
        *[f"- **{name}:** {text}" for name, text in pattern_distortion.get("required_framework", {}).items()],
        "",
        "Before accepting a pattern, the project tests it against Scripture, Christ-centered theology, Church history, Augustine, Calvin, Karl Barth, and a possible skeptical or atheist critique.",
        "",
        "The project may faithfully conclude: insufficient evidence, pattern unclear, theological mystery remains, or do not force a conclusion.",
        "",
        theological_method.get("core_rule", "Pattern recognition may support or clarify a claim, but it cannot create doctrine, replace Christ or Scripture, or erase unresolved friction."),
        "",
        mystery_layer.get("interpretive_rule", "The project must be free to stop short of a pattern claim."),
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
        *next_step_lines(review_audit, review_gap_queue, candidate_pattern),
        "",
        "## Current Corpus Snapshot",
        "",
        *bulletize(latest_cloud_discovery_lines(digest, reference_catalog, generated_at)[:5]),
        f"- {latest_run_count_label(digest, generated_at)}",
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
