from collections import Counter, defaultdict
import json
import math
import re
from pathlib import Path


REPORTS_DIR = Path("reports")
RESEARCH_DIR = Path("research_documents")

INDEX_PATH = REPORTS_DIR / "knowledge_retrieval_index.json"
GRAPH_PATH = REPORTS_DIR / "knowledge_graph.json"
AUDIT_PATH = REPORTS_DIR / "review_rules_audit.json"
REPORT_PATH = REPORTS_DIR / "ai_backend_report.txt"

SUPPORTED_EXTENSIONS = {".md", ".txt"}

SOURCE_LANES = {
    "research_documents": RESEARCH_DIR,
    "source_packs": RESEARCH_DIR / "source_packs",
    "biblical_languages": Path("biblical_languages"),
    "world_languages": Path("world_languages"),
    "all_texts": Path("all_texts"),
    "other_religious_texts": Path("other_religious_texts"),
    "theologians": Path("theologians"),
    "history_inputs": Path("history_inputs"),
    "visual_art": Path("visual_art"),
    "cultural_inputs": Path("cultural_inputs"),
    "psychology_inputs": Path("psychology_inputs"),
    "human_stories": Path("human_stories"),
    "modern_literature": Path("modern_literature"),
    "deep_sources": Path("deep_sources"),
    "pattern_tests": Path("pattern_tests"),
}

PATTERN_NAMES = [
    "Image Of God Pattern",
    "Cross And Reversal Pattern",
    "Creation-To-Consciousness Pattern",
    "Trinity-As-Behavior Pattern",
    "Providence And Contingency Pattern",
    "Holy Spirit Gifts Pattern",
    "Other Religious Comparative Witness",
    "Science Analogy Guardrail",
    "Mathematical Theophany Pattern",
]

REVIEW_RULES = {
    "evidence": ["evidence:", "source reviewed", "supports", "primary text", "original-source"],
    "interpretation": ["interpretation:", "christian theology", "theological reading"],
    "discernment": ["discernment:", "test", "communal", "accountability", "discern"],
    "analogy": ["analogy:", "analogy only", "illuminate", "not proof"],
    "practical_use": ["practical use:", "boundary:", "repair", "justice", "love", "worship"],
    "counter_reading": ["counter-reading", "counterargument", "rival explanation", "pressure"],
    "failure_condition": ["failure condition", "weaken", "revise", "reject"],
    "machine_label_boundary": [
        "machine labels",
        "automated labels",
        "route attention",
        "not settle truth",
        "none_until_human_review",
    ],
}

STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "also",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "can",
    "cannot",
    "context",
    "counter",
    "does",
    "each",
    "from",
    "have",
    "into",
    "must",
    "needs",
    "not",
    "only",
    "other",
    "over",
    "pattern",
    "pressure",
    "reading",
    "review",
    "reviewed",
    "source",
    "supports",
    "that",
    "the",
    "their",
    "them",
    "then",
    "these",
    "this",
    "through",
    "under",
    "until",
    "use",
    "when",
    "where",
    "while",
    "with",
    "without",
}


def read_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_documents():
    seen = set()
    for lane, directory in SOURCE_LANES.items():
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if path in seen:
                continue
            seen.add(path)
            yield lane, path


def tokenize(text):
    tokens = re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())
    return [token for token in tokens if token not in STOPWORDS]


def normalize_id(text):
    value = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return value[:120] or "node"


def extract_title(path, text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem.replace("_", " ").title()


def extract_review_note_count(text):
    match = re.search(r"Reviewed note count:\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def detect_patterns(text):
    lowered = text.lower()
    return [name for name in PATTERN_NAMES if name.lower() in lowered]


def detect_rules(text):
    lowered = text.lower()
    return {
        rule: any(marker in lowered for marker in markers)
        for rule, markers in REVIEW_RULES.items()
    }


def summarize_document(lane, path, text):
    tokens = tokenize(text)
    token_counts = Counter(tokens)
    return {
        "id": normalize_id(str(path.as_posix())),
        "path": path.as_posix(),
        "lane": lane,
        "title": extract_title(path, text),
        "word_count": len(re.findall(r"\S+", text)),
        "review_note_count": extract_review_note_count(text),
        "patterns": detect_patterns(text),
        "rules_present": detect_rules(text),
        "top_terms": [term for term, _ in token_counts.most_common(12)],
        "tokens": token_counts,
    }


def build_retrieval_index(documents):
    doc_count = len(documents)
    document_frequency = Counter()
    for document in documents:
        document_frequency.update(document["tokens"].keys())

    index_documents = []
    inverted_index = defaultdict(list)

    for document in documents:
        token_total = sum(document["tokens"].values()) or 1
        scored_terms = []
        for token, count in document["tokens"].items():
            tf = count / token_total
            idf = math.log((1 + doc_count) / (1 + document_frequency[token])) + 1
            score = round(tf * idf, 6)
            scored_terms.append((token, score, count))

        scored_terms.sort(key=lambda item: (item[1], item[2], item[0]), reverse=True)
        keywords = [
            {"term": term, "score": score, "count": count}
            for term, score, count in scored_terms[:20]
        ]

        slim = {
            "id": document["id"],
            "path": document["path"],
            "lane": document["lane"],
            "title": document["title"],
            "word_count": document["word_count"],
            "review_note_count": document["review_note_count"],
            "patterns": document["patterns"],
            "rules_present": document["rules_present"],
            "keywords": keywords,
        }
        index_documents.append(slim)

        for keyword in keywords[:10]:
            inverted_index[keyword["term"]].append(
                {"document_id": document["id"], "score": keyword["score"]}
            )

    return {
        "backend": "llm_retrieval_knowledge_graph_review_rules",
        "retrieval_strategy": "local tf-idf keyword index; suitable for RAG prompts and source routing",
        "document_count": doc_count,
        "documents": index_documents,
        "inverted_index": dict(sorted(inverted_index.items())),
    }


def add_node(nodes, node_id, label, node_type, **attrs):
    if node_id not in nodes:
        nodes[node_id] = {"id": node_id, "label": label, "type": node_type}
    nodes[node_id].update(attrs)


def add_edge(edges, source, target, relation, **attrs):
    edges.append({"source": source, "target": target, "relation": relation, **attrs})


def build_knowledge_graph(documents):
    nodes = {}
    edges = []

    for lane in SOURCE_LANES:
        add_node(nodes, f"lane:{lane}", lane, "lane")

    for rule in REVIEW_RULES:
        add_node(nodes, f"rule:{rule}", rule, "review_rule")

    for pattern in PATTERN_NAMES:
        add_node(nodes, f"pattern:{normalize_id(pattern)}", pattern, "pattern")

    for document in documents:
        doc_id = f"doc:{document['id']}"
        add_node(
            nodes,
            doc_id,
            document["title"],
            "document",
            path=document["path"],
            lane=document["lane"],
            review_note_count=document["review_note_count"],
        )
        add_edge(edges, doc_id, f"lane:{document['lane']}", "belongs_to_lane")

        for pattern in document["patterns"]:
            add_edge(edges, doc_id, f"pattern:{normalize_id(pattern)}", "mentions_pattern")

        for rule, present in document["rules_present"].items():
            if present:
                add_edge(edges, doc_id, f"rule:{rule}", "satisfies_or_mentions_rule")

    return {
        "backend": "knowledge_graph",
        "graph_policy": "edges support retrieval and review routing; they do not prove theological claims",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def build_review_audit(documents):
    audit_documents = []
    lane_totals = defaultdict(lambda: Counter({"documents": 0, "review_notes": 0}))
    missing_by_rule = defaultdict(list)

    for document in documents:
        lane_totals[document["lane"]]["documents"] += 1
        lane_totals[document["lane"]]["review_notes"] += document["review_note_count"]

        missing = [
            rule for rule, present in document["rules_present"].items() if not present
        ]
        for rule in missing:
            if len(missing_by_rule[rule]) < 25:
                missing_by_rule[rule].append(document["path"])

        if document["review_note_count"] or document["patterns"] or document["lane"] in {
            "source_packs",
            "pattern_tests",
            "research_documents",
        }:
            audit_documents.append(
                {
                    "path": document["path"],
                    "lane": document["lane"],
                    "title": document["title"],
                    "review_note_count": document["review_note_count"],
                    "patterns": document["patterns"],
                    "rules_present": document["rules_present"],
                    "missing_rules": missing,
                }
            )

    return {
        "backend": "review_rules",
        "review_policy": "machine checks route attention; human review decides confidence",
        "lane_totals": {
            lane: dict(counter) for lane, counter in sorted(lane_totals.items())
        },
        "missing_rule_examples": dict(sorted(missing_by_rule.items())),
        "documents": audit_documents,
    }


def create_backend_report(index, graph, audit):
    lane_lines = []
    for lane, totals in audit["lane_totals"].items():
        lane_lines.append(
            f"- {lane}: {totals['documents']} documents; {totals['review_notes']} declared reviewed notes"
        )

    pattern_counts = Counter()
    rule_counts = Counter()
    for document in index["documents"]:
        pattern_counts.update(document["patterns"])
        rule_counts.update(
            rule for rule, present in document["rules_present"].items() if present
        )

    strongest_lanes = sorted(
        audit["lane_totals"].items(),
        key=lambda item: (item[1]["review_notes"], item[1]["documents"]),
        reverse=True,
    )[:4]
    strongest_lane_text = ", ".join(
        f"{lane} ({totals['review_notes']} notes)" for lane, totals in strongest_lanes
    )

    top_patterns = pattern_counts.most_common(5)
    top_pattern_text = ", ".join(
        f"{pattern} ({count})" for pattern, count in top_patterns
    )

    strongest_rules = rule_counts.most_common(4)
    strongest_rule_text = ", ".join(
        f"{rule} ({count})" for rule, count in strongest_rules
    )

    lines = [
        "AI Knowledge Backend Report",
        "===========================",
        "",
        "Opening Conversation",
        "--------------------",
        "Reviewer: What did you build for this project?",
        "Backend: A local LLM-support system: retrieval for finding sources, a knowledge graph for connecting them, and review rules for slowing down overconfident claims.",
        "",
        "Reviewer: Are you deciding what is true?",
        "Backend: No. I route attention. Human review still decides whether a source can affect confidence.",
        "",
        "Reviewer: What should I be most careful about?",
        "Backend: Repeated signals can feel persuasive before they are disciplined. I keep asking for evidence, interpretation, discernment, analogy, practical use, counter-readings, and failure conditions.",
        "",
        "Generated Artifacts",
        "-------------------",
        f"- Retrieval index: `{INDEX_PATH.as_posix()}`",
        f"- Knowledge graph: `{GRAPH_PATH.as_posix()}`",
        f"- Review-rule audit: `{AUDIT_PATH.as_posix()}`",
        f"- Backend report: `{REPORT_PATH.as_posix()}`",
        "",
        "How An LLM Should Use It",
        "------------------------",
        "Reviewer: Suppose an LLM wants to write a claim. What happens first?",
        "Backend: It retrieves source documents before drafting. No source, no confident claim.",
        "",
        "Reviewer: Then what?",
        "Backend: It follows graph edges from documents to lanes, patterns, pressure tests, and review rules.",
        "",
        "Reviewer: And before the claim gets stronger?",
        "Backend: It checks the audit for missing counter-readings, failure conditions, and practical-use boundaries.",
        "",
        "Reviewer: What about automated evidence labels?",
        "Backend: They are triage lights, not verdicts. Green means review me, not believe me.",
        "",
        "Corpus Summary",
        "--------------",
        f"- Indexed documents: {index['document_count']}",
        f"- Graph nodes: {graph['node_count']}",
        f"- Graph edges: {graph['edge_count']}",
        "",
        "Reviewer: Where is the strongest reviewed-note weight right now?",
        f"Backend: {strongest_lane_text or 'No reviewed-note lanes detected yet.'}.",
        "",
        "Reviewer: Which leading patterns are showing up most often?",
        f"Backend: {top_pattern_text or 'No leading pattern mentions detected yet.'}.",
        "",
        "Reviewer: Which review rules are most visible?",
        f"Backend: {strongest_rule_text or 'No review-rule mentions detected yet.'}.",
        "",
        "Lane Coverage",
        "-------------",
        "Backend: Here is the lane map. High counts are invitations to review more carefully, not permission to overclaim.",
        *lane_lines,
        "",
        "Pattern Mentions",
        "----------------",
        "Reviewer: Do these counts prove the patterns?",
        "Backend: No. They show where the corpus is talking. Proof is not what this table does.",
    ]

    if pattern_counts:
        for pattern, count in pattern_counts.most_common():
            lines.append(f"- {pattern}: {count} documents")
    else:
        lines.append("- No leading pattern mentions detected.")

    lines.extend(["", "Review Rule Mentions", "--------------------"])
    lines.extend(
        [
            "Reviewer: What do the review-rule counts tell us?",
            "Backend: They tell us where the project is learning caution. Missing rules mark places for the next human review pass.",
            "",
        ]
    )
    for rule in REVIEW_RULES:
        lines.append(f"- {rule}: {rule_counts.get(rule, 0)} documents")

    lines.extend(
        [
            "",
            "Practical-Theology Gate",
            "-----------------------",
            "Reviewer: When does a pattern become useful?",
            "Backend: When it helps a person become more truthful, loving, humble, just, worshipful, patient, and practically faithful.",
            "",
            "Reviewer: And if it does not do that?",
            "Backend: Then it may still be an interesting pattern, but it has not yet become practical theology.",
            "",
            "Closing Question",
            "----------------",
            "Backend: What faithful response is being invited today?",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    REPORTS_DIR.mkdir(exist_ok=True)

    documents = []
    for lane, path in iter_documents():
        text = read_text(path)
        if text.strip():
            documents.append(summarize_document(lane, path, text))

    index = build_retrieval_index(documents)
    graph = build_knowledge_graph(documents)
    audit = build_review_audit(documents)
    report = create_backend_report(index, graph, audit)

    INDEX_PATH.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")
    GRAPH_PATH.write_text(json.dumps(graph, indent=2, sort_keys=True), encoding="utf-8")
    AUDIT_PATH.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")

    print("AI knowledge backend build complete.")
    print(f"Retrieval index saved to: {INDEX_PATH}")
    print(f"Knowledge graph saved to: {GRAPH_PATH}")
    print(f"Review audit saved to: {AUDIT_PATH}")
    print(f"Backend report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
