from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import re
from pathlib import Path


RESEARCH_DIR = Path("research_documents")
PATTERN_INPUTS_DIR = Path("pattern_inputs")
MUSIC_LYRICS_DIR = Path("music_lyrics")
MUSIC_NOTES_DIR = Path("music_notes")
CULTURAL_INPUTS_DIR = Path("cultural_inputs")
VISUAL_ART_DIR = Path("visual_art")
HISTORY_DIR = Path("history_inputs")
WORLD_LANGUAGES_DIR = Path("world_languages")
BIBLICAL_LANGUAGES_DIR = Path("biblical_languages")
ALL_TEXTS_DIR = Path("all_texts")
PSYCHOLOGY_INPUTS_DIR = Path("psychology_inputs")
OTHER_RELIGIOUS_TEXTS_DIR = Path("other_religious_texts")
MODERN_LITERATURE_DIR = Path("modern_literature")
HUMAN_STORIES_DIR = Path("human_stories")
PATTERN_TESTS_DIR = Path("pattern_tests")
DEEP_SOURCE_DIR = Path("deep_sources")
THEOLOGIANS_DIR = Path("theologians")
REPORTS_DIR = Path("reports")
DAILY_DIGEST_PATH = Path("references") / "daily_research_digest.json"
SEARCH_STRATEGY_PATH = Path("references") / "next_search_strategy.json"
REFERENCES_PATH = Path("references") / "references.json"
REPORT_PATH = REPORTS_DIR / "divine_pattern_research_report.txt"
PATTERN_CANDIDATES_PATH = REPORTS_DIR / "divine_pattern_candidates_report.txt"
DISCOVERED_PATTERNS_PATH = REPORTS_DIR / "discovered_patterns_report.txt"
MUSIC_PATTERNS_PATH = REPORTS_DIR / "music_lyric_patterns_report.txt"
MUSIC_NOTE_PATTERNS_PATH = REPORTS_DIR / "music_note_patterns_report.txt"
CULTURAL_PATTERNS_PATH = REPORTS_DIR / "cultural_pattern_relationships_report.txt"
CROSS_LAYER_REASONING_PATH = REPORTS_DIR / "cross_layer_reasoning_report.txt"
PATTERN_TEST_REPORT_PATH = REPORTS_DIR / "divine_pattern_test_report.txt"
DEEP_SOURCE_REVIEW_PATH = REPORTS_DIR / "deep_source_review_report.txt"
THEOLOGIAN_REPORT_PATH = REPORTS_DIR / "theologian_pattern_design_report.txt"
SUMMARY_REPORT_PATH = REPORTS_DIR / "divine_pattern_summary_report.txt"
TOP_PATTERNS_PATH = REPORTS_DIR / "top_five_divine_patterns_report.txt"
DISCIPLINED_ASSISTANT_PATH = REPORTS_DIR / "disciplined_theological_assistant_report.txt"
READER_BOOK_PATH = REPORTS_DIR / "divine_pattern_reader_book.txt"
CLAIM_LEDGER_PATH = RESEARCH_DIR / "claim_ledger.md"
REVIEWED_SOURCE_PACKS_PATH = RESEARCH_DIR / "reviewed_source_packs.md"
SUPPORTED_EXTENSIONS = {".txt", ".md"}


THEMES = {
    "God and Divine Attributes": [
        "god",
        "lord",
        "father",
        "almighty",
        "holy",
        "eternal",
        "infinite",
        "goodness",
        "mercy",
        "grace",
        "love",
        "creator",
    ],
    "Faith and Trust": [
        "faith",
        "trust",
        "belief",
        "believe",
        "hope",
        "assurance",
        "confidence",
        "commitment",
        "obedience",
        "loyalty",
    ],
    "Jesus and Christology": [
        "jesus",
        "christ",
        "son",
        "messiah",
        "incarnation",
        "cross",
        "crucified",
        "resurrection",
        "gospel",
        "savior",
        "lord jesus",
        "word became flesh",
    ],
    "Holy Spirit and Pneumatology": [
        "holy spirit",
        "spirit",
        "comforter",
        "paraclete",
        "pentecost",
        "gift of the spirit",
        "fruits of the spirit",
        "sanctification",
        "inspiration",
        "dwelling",
    ],
    "Creation and Order": [
        "creation",
        "created",
        "creator",
        "order",
        "wisdom",
        "word",
        "logos",
        "law",
        "truth",
        "intelligibility",
    ],
    "Moral Transformation": [
        "sin",
        "repent",
        "repentance",
        "virtue",
        "righteousness",
        "justice",
        "mercy",
        "forgive",
        "forgiveness",
        "grace",
        "salvation",
    ],
    "Theology and Logos": [
        "logos",
        "divine",
        "creation",
        "truth",
        "order",
        "meaning",
        "wisdom",
        "word",
        "revelation",
    ],
    "Spirituality and Worship": [
        "worship",
        "prayer",
        "faith",
        "spiritual",
        "ritual",
        "sacred",
        "transcendence",
        "religion",
        "belief",
    ],
    "Biology and Neuroscience": [
        "genetic",
        "genetics",
        "biology",
        "brain",
        "neurology",
        "neural",
        "neurotheology",
        "embodied",
        "consciousness",
    ],
    "Physics and Natural Law": [
        "physics",
        "physical",
        "law of nature",
        "laws of nature",
        "gravity",
        "energy",
        "matter",
        "cosmos",
        "universe",
        "space",
        "time",
        "causality",
        "symmetry",
    ],
    "Mathematics and Intelligibility": [
        "mathematics",
        "mathematical",
        "number",
        "geometry",
        "equation",
        "probability",
        "statistics",
        "ratio",
        "logic",
        "structure",
        "pattern",
        "prediction",
    ],
    "Mathematical Theophany": [
        "theophany",
        "self-disclosure",
        "manifestation",
        "sign",
        "mathematical order",
        "pattern",
        "symmetry",
        "logic",
        "infinity",
        "beauty",
        "elegance",
        "harmony",
    ],
    "Quantum Physics and Uncertainty": [
        "quantum",
        "wavefunction",
        "wave function",
        "uncertainty",
        "heisenberg",
        "measurement",
        "superposition",
        "probability density",
        "entanglement",
        "observer",
        "particle",
    ],
    "Anthropology and Culture": [
        "anthropology",
        "culture",
        "cultural",
        "tradition",
        "community",
        "behavior",
        "human",
        "society",
        "symbol",
    ],
    "AI and Pattern Recognition": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "pattern",
        "patterns",
        "data",
        "model",
        "analysis",
        "technology",
    ],
    "Philosophy and Meaning": [
        "philosophy",
        "metaphysics",
        "meaning",
        "purpose",
        "ethics",
        "knowledge",
        "intelligibility",
        "reason",
        "experience",
    ],
}


TRINITY_PERSONS = {
    "Father": {
        "terms": [
            "father",
            "god the father",
            "creator",
            "creation",
            "almighty",
            "providence",
            "source",
            "kingdom",
            "heavenly father",
        ],
        "role": "Source, Creator, giver of being, providential care, and holy authority.",
    },
    "Son": {
        "terms": [
            "son",
            "jesus",
            "christ",
            "son of god",
            "logos",
            "word",
            "incarnation",
            "cross",
            "resurrection",
            "redeemer",
            "savior",
        ],
        "role": "Word/Logos, revelation, incarnation, redemption, reconciliation, and resurrection.",
    },
    "Holy Spirit": {
        "terms": [
            "holy spirit",
            "holy ghost",
            "spirit",
            "comforter",
            "paraclete",
            "presence",
            "pentecost",
            "sanctification",
            "gifts",
            "fruit of the spirit",
            "dwelling",
        ],
        "role": "Living presence, conviction, gifts, communion, sanctification, and transformation.",
    },
}


TRINITARIAN_GUARDRAIL = (
    "Trinitarian guardrail: Father, Son, and Holy Spirit are distinct persons, "
    "not interchangeable symbols; yet they are one God, not three separate gods. "
    "A pattern is stronger when it preserves both distinction and unity."
)


TEST_DOMAINS = {
    "Scripture And Early Christian Logos": [
        "scripture",
        "logos",
        "word",
        "creation",
        "wisdom",
        "providence",
        "john",
        "genesis",
        "paul",
        "early christian",
        "church fathers",
    ],
    "Historical Theology": [
        "historical theology",
        "creation",
        "natural law",
        "providence",
        "trinity",
        "father",
        "son",
        "holy spirit",
        "aquinas",
        "augustine",
        "creed",
    ],
    "Philosophy Of Science": [
        "philosophy of science",
        "law",
        "explanation",
        "causality",
        "realism",
        "regularity",
        "induction",
        "necessity",
        "nature",
    ],
    "Philosophy Of Mathematics": [
        "philosophy of mathematics",
        "mathematics",
        "applicability",
        "indispensability",
        "number",
        "geometry",
        "logic",
        "structure",
        "prediction",
    ],
    "Mathematical Theophany": [
        "theophany",
        "self-disclosure",
        "manifestation",
        "sign",
        "mathematical order",
        "pattern",
        "symmetry",
        "logic",
        "infinity",
        "beauty",
        "elegance",
        "harmony",
        "aesthetic",
    ],
    "Physics And Quantum Mechanics": [
        "physics",
        "quantum",
        "mechanics",
        "wavefunction",
        "measurement",
        "uncertainty",
        "probability",
        "particle",
        "energy",
        "matter",
    ],
    "Cognitive Science": [
        "cognitive science",
        "cognition",
        "pattern recognition",
        "meaning-making",
        "memory",
        "attention",
        "perception",
        "consciousness",
        "mind",
    ],
    "Anthropology And Psychology Of Worship": [
        "anthropology",
        "psychology",
        "worship",
        "ritual",
        "morality",
        "transformation",
        "community",
        "behavior",
        "identity",
        "prosocial",
    ],
    "Visual Art And Symbol": [
        "visual art",
        "painting",
        "icon",
        "image",
        "color",
        "composition",
        "gesture",
        "symbol",
        "beauty",
        "aesthetic",
    ],
    "History And Cultural Memory": [
        "history",
        "historical",
        "era",
        "empire",
        "exile",
        "migration",
        "war",
        "reform",
        "movement",
        "memory",
    ],
    "World Languages And Translation": [
        "language",
        "translation",
        "meaning",
        "semantic",
        "metaphor",
        "idiom",
        "grammar",
        "word order",
        "culture",
        "context",
    ],
    "Biblical Greek And Hebrew": [
        "greek",
        "hebrew",
        "aramaic",
        "septuagint",
        "masoretic",
        "lexicon",
        "lemma",
        "syntax",
        "covenant",
        "hesed",
        "agape",
        "logos",
        "ruach",
        "pneuma",
    ],
}


DIVINE_PATTERN_LAYERS = {
    "Physical Order": {
        "terms": [
            "physical",
            "physics",
            "law",
            "laws of nature",
            "order",
            "creation",
            "universe",
            "cosmos",
            "causality",
            "providence",
        ],
        "question": "Is reality described as ordered, law-like, created, or providential?",
    },
    "Mathematical Structure": {
        "terms": [
            "mathematics",
            "mathematical",
            "number",
            "geometry",
            "equation",
            "logic",
            "structure",
            "prediction",
            "probability",
            "intelligibility",
        ],
        "question": "Does the corpus connect reality with mathematical or logical intelligibility?",
    },
    "Mathematical Theophany": {
        "terms": [
            "theophany",
            "self-disclosure",
            "manifestation",
            "sign",
            "mathematical order",
            "pattern",
            "symmetry",
            "logic",
            "infinity",
            "infinite",
            "beauty",
            "aesthetic",
            "elegance",
            "harmony",
        ],
        "question": "Can mathematical order, pattern, symmetry, logic, infinity, or beauty be read cautiously as possible signs of divine self-disclosure while rival explanations remain in view?",
    },
    "Quantum Probability": {
        "terms": [
            "quantum",
            "uncertainty",
            "probability",
            "wavefunction",
            "measurement",
            "particle",
            "superposition",
            "entanglement",
        ],
        "question": "Does the corpus include disciplined uncertainty rather than simple determinism?",
    },
    "Life And Consciousness": {
        "terms": [
            "life",
            "living",
            "biology",
            "consciousness",
            "mind",
            "brain",
            "human",
            "image of god",
            "soul",
            "breath",
        ],
        "question": "Does the corpus connect ordered reality with life, mind, or personhood?",
    },
    "Meaning And Logos": {
        "terms": [
            "meaning",
            "logos",
            "word",
            "wisdom",
            "truth",
            "revelation",
            "reason",
            "knowledge",
            "purpose",
        ],
        "question": "Does the corpus connect intelligibility with meaning, Logos, wisdom, or truth?",
    },
    "Moral Response": {
        "terms": [
            "moral",
            "morality",
            "sin",
            "justice",
            "mercy",
            "righteousness",
            "repent",
            "forgive",
            "obedience",
            "virtue",
        ],
        "question": "Does the corpus connect meaning with moral accountability or response?",
    },
    "Worship And Community": {
        "terms": [
            "worship",
            "prayer",
            "ritual",
            "church",
            "community",
            "sacrament",
            "baptism",
            "eucharist",
            "faith",
            "discipleship",
        ],
        "question": "Does the corpus connect belief with embodied practice and community?",
    },
    "Transformation": {
        "terms": [
            "transformation",
            "sanctification",
            "holy spirit",
            "spirit",
            "grace",
            "salvation",
            "redemption",
            "resurrection",
            "new life",
            "hope",
        ],
        "question": "Does the corpus connect divine presence with personal or communal change?",
    },
}


DIVINE_PATTERN_CANDIDATES = [
    {
        "name": "Logos Pattern",
        "sequence": "Order -> Intelligibility -> Word/Logos -> Meaning -> Revelation",
        "interpretation": "Reality is not merely structured; it is intelligible. Christian theology interprets this through Logos: the Word through whom creation is ordered and made knowable.",
        "layers": ["Physical Order", "Mathematical Structure", "Meaning And Logos"],
        "evidence_needed": "Scripture on Logos and creation, early Christian Logos theology, philosophy of mathematics, and philosophy of science.",
        "risk": "Do not treat mathematical elegance as automatic proof of Christian doctrine.",
    },
    {
        "name": "Mathematical Theophany Pattern",
        "sequence": "Order -> Pattern -> Symmetry/Logic -> Beauty/Infinity -> Possible Self-Disclosure -> Humble Interpretation",
        "interpretation": "Mathematical order may function as a theophany filter: not proof by itself, but a disciplined way to ask whether intelligibility, symmetry, logic, infinity, and beauty can be received as signs of divine self-disclosure.",
        "layers": ["Physical Order", "Mathematical Structure", "Mathematical Theophany", "Meaning And Logos"],
        "evidence_needed": "Philosophy of mathematics, aesthetics, theology of creation and revelation, history of science, and serious non-theistic or naturalistic interpretations.",
        "risk": "Do not collapse mathematical beauty into revelation, ignore ugly or chaotic realities, or treat subjective aesthetic response as universal evidence.",
    },
    {
        "name": "Creation-To-Consciousness Pattern",
        "sequence": "Physical Order -> Life -> Consciousness -> Moral Awareness -> Worship",
        "interpretation": "The universe contains layers that move from matter and law toward life, mind, responsibility, and worship.",
        "layers": ["Physical Order", "Life And Consciousness", "Moral Response", "Worship And Community"],
        "evidence_needed": "Physics, biology, cognitive science, theological anthropology, and anthropology of worship.",
        "risk": "Avoid implying a simple linear proof from physics to worship.",
    },
    {
        "name": "Trinity-As-Behavior Pattern",
        "sequence": "Father Creates -> Son Redeems -> Spirit Transforms",
        "interpretation": "Christian belief forms a behavioral map: humans receive life, encounter redemption, and are changed into a new way of living.",
        "layers": ["Physical Order", "Meaning And Logos", "Transformation"],
        "evidence_needed": "Creeds, Trinitarian theology, Christology, pneumatology, worship practice, and lived Christian formation.",
        "risk": "Keep the Trinity theological and relational, not merely symbolic psychology.",
    },
    {
        "name": "Moral Transformation Pattern",
        "sequence": "Sin -> Conviction -> Repentance -> Forgiveness -> New Life",
        "interpretation": "Christianity repeatedly frames human behavior as transformable, not fixed. The pattern is moral repair through grace.",
        "layers": ["Moral Response", "Transformation", "Worship And Community"],
        "evidence_needed": "Scripture, Augustine, pastoral theology, moral psychology, forgiveness research, and spiritual formation studies.",
        "risk": "Do not reduce grace to self-improvement psychology.",
    },
    {
        "name": "Worship Embodiment Pattern",
        "sequence": "Belief -> Ritual -> Community -> Identity -> Practice",
        "interpretation": "Worship turns abstract belief into repeated embodied behavior. Prayer, sacrament, singing, confession, and gathering train identity.",
        "layers": ["Worship And Community", "Moral Response", "Transformation"],
        "evidence_needed": "Liturgical theology, ritual studies, anthropology of religion, psychology of habit, and community formation research.",
        "risk": "Do not treat ritual as only social bonding; preserve theological meaning.",
    },
    {
        "name": "Quantum Humility Pattern",
        "sequence": "Law-Like Reality -> Probability -> Uncertainty -> Epistemic Humility",
        "interpretation": "Reality is structured but not fully controllable or reducible to simple mechanism. This supports humility, not mystical overclaiming.",
        "layers": ["Physical Order", "Mathematical Structure", "Quantum Probability"],
        "evidence_needed": "Physicist-authored quantum mechanics sources, philosophy of probability, and theology of providence.",
        "risk": "Never use quantum physics as vague proof of God, prayer, or consciousness.",
    },
    {
        "name": "Providence And Contingency Pattern",
        "sequence": "Stable Law -> Contingent Events -> Emergent Complexity -> Meaningful History",
        "interpretation": "Divine providence may be studied as a theological interpretation of a world that is ordered yet open, lawful yet historically unfolding.",
        "layers": ["Physical Order", "Quantum Probability", "Life And Consciousness", "Meaning And Logos"],
        "evidence_needed": "Historical theology on providence, philosophy of causality, physics, biology, complexity, and history.",
        "risk": "Do not confuse providence with easy prediction or visible control of every event.",
    },
    {
        "name": "Image Of God Pattern",
        "sequence": "Mind -> Symbol -> Moral Agency -> Relationship -> Worship",
        "interpretation": "Human beings are pattern-recognizing, meaning-making, morally accountable, relational creatures. Christianity interprets this through the image of God.",
        "layers": ["Life And Consciousness", "Meaning And Logos", "Moral Response", "Worship And Community"],
        "evidence_needed": "Genesis, theological anthropology, cognitive science, social cognition, moral psychology, and worship studies.",
        "risk": "Do not collapse the image of God into intelligence alone.",
    },
    {
        "name": "Cross And Reversal Pattern",
        "sequence": "Power -> Humility | Violence -> Forgiveness | Suffering -> Redemption | Death -> Resurrection",
        "interpretation": "Jesus introduces a reversal pattern where transformation comes through sacrifice, mercy, and resurrection hope.",
        "layers": ["Meaning And Logos", "Moral Response", "Transformation"],
        "evidence_needed": "Gospels, Pauline theology, creeds, atonement theology, martyrdom studies, and psychology of forgiveness.",
        "risk": "Do not romanticize suffering or ignore injustice.",
    },
    {
        "name": "Spirit Transformation Pattern",
        "sequence": "Presence -> Conviction -> Gifts -> Unity -> Sanctification",
        "interpretation": "The Holy Spirit pattern links divine presence to inner change and communal formation.",
        "layers": ["Worship And Community", "Moral Response", "Transformation"],
        "evidence_needed": "Acts, Pauline letters, pneumatology, spiritual gifts, sanctification, and communal practice.",
        "risk": "Do not reduce the Spirit to emotion or group energy.",
    },
]


LYRIC_ALIGNMENT_PATTERNS = {
    "Lament And Cry For Help": [
        "cry",
        "tears",
        "sorrow",
        "broken",
        "darkness",
        "alone",
        "help",
        "deliver",
        "save me",
        "why",
    ],
    "Praise And Thanksgiving": [
        "praise",
        "glory",
        "hallelujah",
        "thank",
        "bless",
        "sing",
        "joy",
        "rejoice",
        "worship",
    ],
    "Redemption And Rescue": [
        "redeem",
        "redemption",
        "rescue",
        "saved",
        "salvation",
        "forgive",
        "grace",
        "mercy",
        "freedom",
    ],
    "Exile And Homecoming": [
        "exile",
        "wander",
        "wilderness",
        "desert",
        "home",
        "return",
        "promised land",
        "journey",
    ],
    "Creation And Wonder": [
        "stars",
        "heaven",
        "earth",
        "sea",
        "mountain",
        "river",
        "light",
        "breath",
        "creation",
    ],
    "Wisdom And Truth": [
        "truth",
        "wisdom",
        "word",
        "light",
        "way",
        "path",
        "know",
        "understand",
        "meaning",
    ],
    "Spirit And Presence": [
        "spirit",
        "presence",
        "fire",
        "breath",
        "wind",
        "near",
        "inside",
        "within",
        "comfort",
    ],
    "Justice And Mercy": [
        "justice",
        "mercy",
        "poor",
        "oppressed",
        "hungry",
        "prison",
        "peace",
        "righteous",
    ],
    "Sacrifice And Cross": [
        "cross",
        "blood",
        "sacrifice",
        "suffer",
        "wounds",
        "crown",
        "lamb",
        "gave",
    ],
    "Resurrection And Hope": [
        "rise",
        "risen",
        "resurrection",
        "new life",
        "morning",
        "hope",
        "alive",
        "victory",
    ],
    "Covenant And Faithfulness": [
        "covenant",
        "promise",
        "faithful",
        "forever",
        "love",
        "steadfast",
        "never leave",
        "remain",
    ],
}


GENERAL_MUSIC_PATTERNS = {
    "Love And Longing": [
        "love",
        "heart",
        "miss",
        "need",
        "want",
        "hold",
        "kiss",
        "desire",
        "longing",
    ],
    "Loss And Grief": [
        "loss",
        "lost",
        "gone",
        "goodbye",
        "grief",
        "ache",
        "empty",
        "mourning",
        "tears",
    ],
    "Identity And Becoming": [
        "name",
        "self",
        "become",
        "becoming",
        "change",
        "mirror",
        "identity",
        "voice",
        "real",
    ],
    "Freedom And Escape": [
        "free",
        "freedom",
        "escape",
        "run",
        "road",
        "drive",
        "leave",
        "chains",
        "open",
    ],
    "Rebellion And Resistance": [
        "fight",
        "rise",
        "resist",
        "rebel",
        "break",
        "power",
        "system",
        "stand",
        "rage",
    ],
    "Party And Release": [
        "party",
        "dance",
        "night",
        "club",
        "beat",
        "move",
        "fire",
        "lights",
        "drink",
    ],
    "Money And Status": [
        "money",
        "gold",
        "rich",
        "fame",
        "crown",
        "king",
        "queen",
        "status",
        "diamonds",
    ],
    "Home And Belonging": [
        "home",
        "belong",
        "family",
        "town",
        "porch",
        "room",
        "return",
        "roots",
        "together",
    ],
    "Journey And Road": [
        "road",
        "highway",
        "train",
        "walk",
        "miles",
        "map",
        "horizon",
        "journey",
        "path",
    ],
    "Work And Survival": [
        "work",
        "labor",
        "hustle",
        "survive",
        "rent",
        "job",
        "hands",
        "sweat",
        "pay",
    ],
    "Nature And Cosmos": [
        "sun",
        "moon",
        "stars",
        "river",
        "rain",
        "storm",
        "ocean",
        "mountain",
        "sky",
    ],
    "Mortality And Time": [
        "time",
        "age",
        "old",
        "death",
        "grave",
        "clock",
        "years",
        "memory",
        "last",
    ],
    "Healing And Recovery": [
        "heal",
        "healing",
        "recover",
        "breathe",
        "mend",
        "whole",
        "scar",
        "better",
        "again",
    ],
    "Community And Solidarity": [
        "we",
        "us",
        "together",
        "crowd",
        "people",
        "hands",
        "brother",
        "sister",
        "crew",
    ],
}


MUSIC_PATTERN_LAYER_MAP = {
    "Love And Longing": ["Meaning And Logos", "Worship And Community"],
    "Loss And Grief": ["Moral Response", "Transformation"],
    "Identity And Becoming": ["Life And Consciousness", "Transformation"],
    "Freedom And Escape": ["Moral Response", "Transformation"],
    "Rebellion And Resistance": ["Moral Response"],
    "Party And Release": ["Worship And Community"],
    "Money And Status": ["Moral Response"],
    "Home And Belonging": ["Worship And Community"],
    "Journey And Road": ["Meaning And Logos", "Transformation"],
    "Work And Survival": ["Life And Consciousness", "Moral Response"],
    "Nature And Cosmos": ["Physical Order", "Meaning And Logos"],
    "Mortality And Time": ["Life And Consciousness", "Meaning And Logos"],
    "Healing And Recovery": ["Transformation"],
    "Community And Solidarity": ["Worship And Community", "Moral Response"],
}


NOTE_OFFSETS = {
    "C": 0,
    "B#": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "FB": 4,
    "E#": 5,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
    "CB": 11,
}


INTERVAL_NAMES = {
    0: "unison/octave",
    1: "minor second",
    2: "major second",
    3: "minor third",
    4: "major third",
    5: "perfect fourth",
    6: "tritone",
    7: "perfect fifth",
    8: "minor sixth",
    9: "major sixth",
    10: "minor seventh",
    11: "major seventh",
}


CONSONANT_INTERVALS = {0, 3, 4, 5, 7, 8, 9}
TENSION_INTERVALS = {1, 2, 6, 10, 11}


INTERVAL_RATIOS = {
    0: "1:1 or 2:1",
    1: "16:15",
    2: "9:8",
    3: "6:5",
    4: "5:4",
    5: "4:3",
    6: "45:32",
    7: "3:2",
    8: "8:5",
    9: "5:3",
    10: "9:5",
    11: "15:8",
}


MEANING_CONTEXTS = {
    "Creation And Order": [
        "order",
        "create",
        "creation",
        "light",
        "structure",
        "form",
        "world",
        "cosmos",
        "law",
        "ratio",
        "pattern",
    ],
    "Alienation And Lament": [
        "lament",
        "cry",
        "grief",
        "loss",
        "exile",
        "alone",
        "dark",
        "sorrow",
        "death",
        "wound",
        "fear",
    ],
    "Desire And Longing": [
        "love",
        "longing",
        "hunger",
        "desire",
        "search",
        "seek",
        "want",
        "home",
        "belong",
        "heart",
    ],
    "Moral Confrontation": [
        "justice",
        "mercy",
        "sin",
        "repent",
        "forgive",
        "truth",
        "poor",
        "oppressed",
        "prisoner",
        "righteous",
    ],
    "Communal Practice": [
        "worship",
        "prayer",
        "community",
        "together",
        "communion",
        "service",
        "neighbor",
        "hands",
        "voice",
        "song",
    ],
    "Transformation And Hope": [
        "transform",
        "change",
        "heal",
        "hope",
        "resurrection",
        "new",
        "restore",
        "grace",
        "spirit",
        "life",
    ],
}


PRACTICAL_THEOLOGY_USES = {
    "Creation And Order": "Practice attentiveness: notice order, beauty, limits, and responsibility in ordinary work, nature, technology, and relationships.",
    "Alienation And Lament": "Make room for honest lament: name grief without rushing to easy answers, especially in counseling, prayer, music, and community care.",
    "Desire And Longing": "Discern desire: ask what loves are shaping the person, family, church, or culture, and whether those loves are ordered toward life.",
    "Moral Confrontation": "Move from insight to repair: connect truth, justice, repentance, forgiveness, and concrete action for neighbors.",
    "Communal Practice": "Turn belief into embodied habit: worship, service, shared meals, reconciliation, and repeated practices that form character.",
    "Transformation And Hope": "Look for signs of renewal: healing, courage, patience, sobriety, reconciliation, and hope that can be practiced today.",
}


MEANING_STAGE_ORDER = [
    "Creation And Order",
    "Alienation And Lament",
    "Desire And Longing",
    "Moral Confrontation",
    "Communal Practice",
    "Transformation And Hope",
]


CULTURAL_DOMAINS = {
    "Art And Beauty": [
        "art",
        "beauty",
        "image",
        "painting",
        "sculpture",
        "color",
        "form",
        "symbol",
        "imagination",
        "aesthetic",
    ],
    "Politics And Justice": [
        "politics",
        "policy",
        "law",
        "justice",
        "rights",
        "power",
        "government",
        "vote",
        "freedom",
        "oppression",
        "public",
    ],
    "Science And Discovery": [
        "science",
        "experiment",
        "evidence",
        "hypothesis",
        "physics",
        "biology",
        "cosmos",
        "measurement",
        "observation",
        "theory",
    ],
    "Technology And AI": [
        "technology",
        "ai",
        "algorithm",
        "data",
        "machine",
        "automation",
        "computer",
        "model",
        "tool",
    ],
    "Economics And Work": [
        "economy",
        "money",
        "labor",
        "work",
        "job",
        "poverty",
        "wealth",
        "market",
        "wage",
        "survival",
    ],
    "Education And Formation": [
        "education",
        "school",
        "learn",
        "teach",
        "student",
        "wisdom",
        "formation",
        "discipline",
        "knowledge",
    ],
    "Family And Community": [
        "family",
        "home",
        "neighbor",
        "community",
        "children",
        "parent",
        "friend",
        "belong",
        "care",
    ],
    "Health And Suffering": [
        "health",
        "illness",
        "body",
        "medicine",
        "pain",
        "suffering",
        "healing",
        "mental",
        "trauma",
    ],
    "Ecology And Creation Care": [
        "ecology",
        "climate",
        "earth",
        "water",
        "land",
        "animals",
        "environment",
        "stewardship",
        "creation",
    ],
    "Visual Art And Iconography": [
        "visual art",
        "iconography",
        "painting",
        "sculpture",
        "image",
        "composition",
        "color",
        "light",
        "gesture",
        "perspective",
        "symbol",
    ],
    "History And Memory": [
        "history",
        "historical",
        "empire",
        "exile",
        "migration",
        "war",
        "reform",
        "movement",
        "era",
        "memory",
        "archive",
    ],
    "World Languages": [
        "language",
        "translation",
        "semantic",
        "metaphor",
        "idiom",
        "grammar",
        "culture",
        "meaning",
        "word order",
        "interpretation",
        "comparative linguistics",
        "language family",
        "script",
        "oral tradition",
        "poetry",
        "proverb",
    ],
    "Biblical Greek And Hebrew": [
        "greek",
        "hebrew",
        "aramaic",
        "septuagint",
        "masoretic",
        "lemma",
        "lexicon",
        "syntax",
        "logos",
        "agape",
        "hesed",
        "shalom",
        "ruach",
        "pneuma",
    ],
    "Psychology And Human Behavior": [
        "psychology",
        "cognitive",
        "perception",
        "memory",
        "attention",
        "emotion",
        "attachment",
        "trauma",
        "habit",
        "behavior",
        "identity",
        "motivation",
    ],
    "Global Text Traditions": [
        "text",
        "texts",
        "scripture",
        "epic",
        "myth",
        "poetry",
        "proverb",
        "law code",
        "philosophy",
        "wisdom",
        "oral tradition",
        "ritual",
        "commentary",
        "chronicle",
        "folklore",
    ],
}


CULTURAL_DOMAIN_LAYER_MAP = {
    "Art And Beauty": ["Meaning And Logos", "Worship And Community"],
    "Politics And Justice": ["Moral Response", "Worship And Community"],
    "Science And Discovery": ["Physical Order", "Mathematical Structure", "Meaning And Logos"],
    "Technology And AI": ["Mathematical Structure", "Moral Response"],
    "Economics And Work": ["Life And Consciousness", "Moral Response"],
    "Education And Formation": ["Meaning And Logos", "Transformation"],
    "Family And Community": ["Worship And Community", "Transformation"],
    "Health And Suffering": ["Life And Consciousness", "Transformation"],
    "Ecology And Creation Care": ["Physical Order", "Moral Response"],
    "Visual Art And Iconography": ["Meaning And Logos", "Moral Response", "Worship And Community"],
    "History And Memory": ["Meaning And Logos", "Moral Response", "Transformation"],
    "World Languages": ["Meaning And Logos", "Worship And Community"],
    "Biblical Greek And Hebrew": ["Meaning And Logos", "Worship And Community", "Transformation"],
    "Psychology And Human Behavior": ["Life And Consciousness", "Moral Response", "Transformation"],
    "Global Text Traditions": ["Meaning And Logos", "Moral Response", "Worship And Community", "Transformation"],
}


PRACTICAL_DOMAIN_USES = {
    "Art And Beauty": "Use art to reveal what people love, fear, remember, and hope for; then ask what kind of formation that beauty produces.",
    "Politics And Justice": "Use the pattern to move political anger toward truth, neighbor-love, justice, accountability, and practical repair.",
    "Science And Discovery": "Use science as disciplined wonder: observe order carefully while staying humble about what the evidence can and cannot claim.",
    "Technology And AI": "Use tools ethically: ask whether technology serves human dignity, truth, community, and responsible stewardship.",
    "Economics And Work": "Apply the pattern to labor and money by asking whether systems protect dignity, reduce exploitation, and support real flourishing.",
    "Education And Formation": "Treat learning as formation, not just information: knowledge should shape wisdom, character, and service.",
    "Family And Community": "Look for practices that rebuild belonging: listening, forgiveness, shared responsibility, care, and truthful love.",
    "Health And Suffering": "Respond to suffering with truthful lament, practical care, patience, and hope without minimizing pain.",
    "Ecology And Creation Care": "Connect creation order to stewardship: beauty and interdependence should lead to responsibility.",
    "Visual Art And Iconography": "Read visual form as meaning: ask how image, color, gesture, and composition reveal desire, lament, worship, power, or hope.",
    "History And Memory": "Place patterns in time: test whether a pattern survives historical complexity, conflict, reform, memory, and unintended consequences.",
    "World Languages": "Use translation carefully: compare semantic range, metaphor, grammar, and cultural context before turning a word match into a conclusion.",
    "Biblical Greek And Hebrew": "Use original-language study as a depth check: examine lemma, syntax, covenant language, and translation range before making theological claims.",
    "Psychology And Human Behavior": "Use psychology to examine perception, attachment, habit, trauma, desire, and change without reducing faith to mental process.",
    "Global Text Traditions": "Compare sacred, philosophical, poetic, legal, oral, and wisdom texts as witnesses to human longing, moral order, suffering, community, and transformation.",
    "Other Religious Texts": "Compare non-Christian sacred and wisdom traditions on their own terms, looking for shared human patterns and real theological difference.",
    "Modern Literature": "Use modern novels, drama, memoir, and poetry through summaries and public-domain material, not copied copyrighted text, to test narrative recurrence and limits.",
    "Human Stories": "Use lived stories as practical witnesses: grief, repair, addiction, injustice, forgiveness, vocation, community, and transformation.",
}


SYNTHESIS_SOURCE_DIRS = {
    "Visual Art": VISUAL_ART_DIR,
    "History": HISTORY_DIR,
    "World Languages": WORLD_LANGUAGES_DIR,
    "Biblical Greek And Hebrew": BIBLICAL_LANGUAGES_DIR,
    "All Texts": ALL_TEXTS_DIR,
    "Psychology And Other Texts": PSYCHOLOGY_INPUTS_DIR,
    "Other Religious Texts": OTHER_RELIGIOUS_TEXTS_DIR,
    "Modern Literature": MODERN_LITERATURE_DIR,
    "Human Stories": HUMAN_STORIES_DIR,
}


SOURCE_LANE_TARGETS = {
    "biblical_languages": {
        "minimum": 12,
        "target": 30,
        "review_cap": 60,
        "purpose": "original-language depth before using Greek, Hebrew, Aramaic, or translation claims",
    },
    "world_languages": {
        "minimum": 12,
        "target": 30,
        "review_cap": 60,
        "purpose": "global translation, metaphor, oral tradition, and language-family breadth",
    },
    "all_texts": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "sacred, wisdom, legal, poetic, ritual, oral, and philosophical comparison",
    },
    "other_religious_texts": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "respectful comparison across traditions without flattening differences",
    },
    "theologians": {
        "minimum": 30,
        "target": 75,
        "review_cap": 120,
        "purpose": "primary-text theology and disagreements across eras",
    },
    "history_inputs": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "power, conflict, memory, reform, and consequences",
    },
    "visual_art": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "image, form, gesture, beauty, lament, glory, and iconography",
    },
    "psychology_inputs": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "pattern perception, attachment, trauma, habit, desire, identity, and repair",
    },
    "human_stories": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "lived grief, repair, vocation, community, and transformation",
    },
    "cultural_inputs": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "politics, economics, technology, ecology, health, work, and education",
    },
    "modern_literature": {
        "minimum": 12,
        "target": 30,
        "review_cap": 60,
        "purpose": "narrative recurrence and limits through literature summaries",
    },
    "deep_sources": {
        "minimum": 20,
        "target": 50,
        "review_cap": 90,
        "purpose": "math, statistics, science, suffering, and counterargument guardrails",
    },
    "pattern_tests": {
        "minimum": 20,
        "target": 45,
        "review_cap": 75,
        "purpose": "pressure tests that challenge claims without becoming the whole project",
    },
    "research_documents": {
        "minimum": 20,
        "target": 45,
        "review_cap": 75,
        "purpose": "method, cloud review, claim rules, ledgers, and synthesis policy",
    },
}


SYNTHESIS_LANE_KEYS = {
    "Visual Art": "visual_art",
    "History": "history_inputs",
    "World Languages": "world_languages",
    "Biblical Greek And Hebrew": "biblical_languages",
    "All Texts": "all_texts",
    "Psychology And Other Texts": "psychology_inputs",
    "Other Religious Texts": "other_religious_texts",
    "Modern Literature": "modern_literature",
    "Human Stories": "human_stories",
}


CAUTIOUS_CONFIDENCE_GLOSSARY = [
    (
        "high internal signal",
        "the current corpus strongly repeats the pattern, but it is still not proof",
    ),
    (
        "well-represented hypothesis",
        "the pattern has broad source coverage and should now face source review and counter-readings",
    ),
    (
        "early complete hypothesis",
        "every required layer appears, but the weakest layer is still thin",
    ),
    (
        "partial hypothesis",
        "some layers appear and others are missing, so synthesis must wait",
    ),
    (
        "reviewed evidence",
        "source-specific support has been checked against counterarguments and lane balance",
    ),
    (
        "discernment question",
        "useful for prayer, pastoral reflection, and communal testing, but not a conclusion",
    ),
    (
        "analogy only",
        "illuminating comparison that cannot carry proof-level weight",
    ),
]


PRACTICAL_THEOLOGY_LOOP = [
    ("Notice", "attend to the actual situation before explaining it"),
    ("Name", "tell the truth about gift, harm, longing, beauty, sin, or suffering"),
    ("Discern", "test the possible meaning with scripture, community, reason, prayer, and counter-readings"),
    ("Practice", "choose a small embodied act of repentance, repair, service, worship, courage, or care"),
    ("Review", "look for fruit over time: love, truth, humility, justice, patience, and hope"),
]


PATTERN_PRESSURE_PROFILES = {
    "Logos Pattern": {
        "best_use": "shows how order, intelligibility, word, wisdom, and revelation can be studied together",
        "hardest_pressure": "language-context tests and science/math overclaim tests",
        "weakens_if": "word matches replace exegesis, or mathematical beauty is treated as doctrine",
        "daily_use": "ask what truth is being revealed and what response wisdom requires",
    },
    "Creation-To-Consciousness Pattern": {
        "best_use": "connects creation, life, personhood, responsibility, and worship",
        "hardest_pressure": "evolution, suffering, disability, consciousness, and image-of-God reduction tests",
        "weakens_if": "it implies a simple ladder from physics to worship",
        "daily_use": "honor embodied life, dignity, vocation, and stewardship in ordinary choices",
    },
    "Trinity-As-Behavior Pattern": {
        "best_use": "keeps creation, redemption, and transformation relational and practical",
        "hardest_pressure": "Trinitarian doctrine, other religious comparison, and spiritual misuse tests",
        "weakens_if": "Father, Son, and Holy Spirit become symbols rather than persons",
        "daily_use": "receive life, follow Christ, and seek Spirit-led transformation in community",
    },
    "Moral Transformation Pattern": {
        "best_use": "connects conviction, repentance, forgiveness, repair, and new life",
        "hardest_pressure": "abuse, cheap grace, unresolved harm, and failed repair tests",
        "weakens_if": "it pressures victims to forgive without justice or safety",
        "daily_use": "practice confession, accountability, repair, and mercy without denial",
    },
    "Worship Embodiment Pattern": {
        "best_use": "shows how belief becomes habit, ritual, community, and identity",
        "hardest_pressure": "empty ritual, coercive community, trauma, and institutional failure tests",
        "weakens_if": "ritual is treated as only social bonding or as control",
        "daily_use": "turn prayer, gathering, song, sacrament, and service into faithful formation",
    },
    "Quantum Humility Pattern": {
        "best_use": "supports epistemic humility about causality, probability, and control",
        "hardest_pressure": "qualified physics, logic, scale, and category-mistake tests",
        "weakens_if": "quantum language is used to prove prayer, consciousness, or God",
        "daily_use": "remain humble where evidence is limited and avoid false certainty",
    },
    "Providence And Contingency Pattern": {
        "best_use": "studies a world that is ordered yet historically open and contingent",
        "hardest_pressure": "evil, chance, failed prediction, and no-visible-repair tests",
        "weakens_if": "providence is reduced to prediction or control of every event",
        "daily_use": "act faithfully in uncertainty without pretending to know every cause",
    },
    "Image Of God Pattern": {
        "best_use": "connects mind, symbol, moral agency, relationship, dignity, and worship",
        "hardest_pressure": "disability, dementia, trauma, oppression, and intelligence-reduction tests",
        "weakens_if": "the image of God is collapsed into ability, status, or intelligence",
        "daily_use": "treat every person as bearing dignity before performance or usefulness",
    },
    "Cross And Reversal Pattern": {
        "best_use": "faces power, suffering, mercy, forgiveness, resurrection hope, and reversal",
        "hardest_pressure": "unresolved suffering, injustice, violence, and romanticized suffering tests",
        "weakens_if": "it asks people to accept harm instead of seeking truth and justice",
        "daily_use": "choose humility, truth, forgiveness with boundaries, and hope without denial",
    },
    "Spirit Transformation Pattern": {
        "best_use": "links presence, conviction, gifts, unity, sanctification, and communal fruit",
        "hardest_pressure": "false discernment, manipulation, spectacle, abuse, and cross-cultural testimony tests",
        "weakens_if": "the Holy Spirit becomes emotion, group energy, status, or coercion",
        "daily_use": "test gifts by love, service, humility, truth, and the fruit of the Spirit",
    },
}


PATTERN_FORMATION_PROFILES = {
    "Image Of God Pattern": {
        "human_problem": "People are often measured by usefulness, intelligence, productivity, beauty, tribe, or power. The pattern asks whether every person has a deeper dignity before any performance.",
        "biblical_grounding": "Begin with Genesis 1:26-28, Genesis 2, Psalm 8, the incarnation, and New Testament language about renewal in Christ. Add theologians on image, likeness, dignity, vocation, disability, and communion.",
        "scholarly_conversation": "Needs theological anthropology, disability theology, cognitive science, moral psychology, social cognition, and critiques of reducing personhood to rational ability.",
        "cross_cultural_listening": "Compare how cultures name personhood, kinship, ancestors, moral agency, honor, shame, body, and community without assuming every tradition means the same thing by dignity.",
        "pressure_test": "Test against dementia, disability, racism, caste, poverty, trauma, slavery, exploitation, and any theology that quietly ranks human worth.",
        "practical_response": "Treat the person in front of you as bearing dignity before achievement. Practice listening, protection, patience, advocacy, and worship that includes the weak and overlooked.",
    },
    "Cross And Reversal Pattern": {
        "human_problem": "Human beings often trust power, victory, revenge, and control. The cross confronts the assumption that God is revealed only through visible success.",
        "biblical_grounding": "Ground in the passion narratives, Isaiah's servant songs, Philippians 2, 1 Corinthians 1-2, Romans 5-8, and resurrection witness. Include atonement debates and martyrdom traditions carefully.",
        "scholarly_conversation": "Needs biblical theology, atonement theology, trauma theology, liberation theology, forgiveness research, and critiques of suffering being romanticized.",
        "cross_cultural_listening": "Compare stories of sacrifice, shame, honor, nonviolence, martyrdom, resistance, and communal memory while preserving the uniqueness of the Christian resurrection claim.",
        "pressure_test": "Test against abuse, domestic violence, spiritual manipulation, state violence, unanswered grief, and situations where appeals to sacrifice protect the powerful.",
        "practical_response": "Practice humility, truth-telling, forgiveness with boundaries, justice for victims, and hope that does not deny wounds.",
    },
    "Providence And Contingency Pattern": {
        "human_problem": "People want to know whether their lives are guided or random, especially when events feel accidental, painful, or beyond control.",
        "biblical_grounding": "Ground in Joseph, Job, Esther, Psalms, wisdom literature, Jesus' teaching on providence, Acts, and Pauline language about hope and groaning. Include classical and modern providence debates.",
        "scholarly_conversation": "Needs philosophy of causality, theology of providence, history, complexity, probability, science limits, and careful distinctions between meaning, cause, and prediction.",
        "cross_cultural_listening": "Compare fate, karma, destiny, providence, chance, ancestral guidance, and wisdom traditions without pretending they are identical.",
        "pressure_test": "Test against evil, tragedy, failed prediction, survivor bias, random loss, unanswered prayer, and attempts to explain every event too neatly.",
        "practical_response": "Act faithfully inside uncertainty. Pray, plan, serve, grieve, and choose wisdom without claiming to know every hidden cause.",
    },
    "Trinity-As-Behavior Pattern": {
        "human_problem": "Faith can become abstract if it does not shape how people receive life, follow Christ, and live by the Spirit in community.",
        "biblical_grounding": "Ground in baptismal language, Matthew 28:19, John 14-17, Romans 8, 2 Corinthians 13:14, Ephesians, creeds, and theologians who preserve distinction and unity.",
        "scholarly_conversation": "Needs Trinitarian doctrine, Christology, pneumatology, liturgical theology, spiritual formation, and critiques of reducing the Trinity to a psychological symbol.",
        "cross_cultural_listening": "Compare how Christian communities across cultures pray, baptize, worship, serve, and describe the Spirit's work without collapsing local practice into one model.",
        "pressure_test": "Test against modalism, tritheism, vague symbolism, authoritarian claims of divine authority, and spiritual experiences that lack fruit.",
        "practical_response": "Receive creation as gift, follow Christ in concrete obedience, and test Spirit-led change by love, holiness, humility, unity, and service.",
    },
    "Creation-To-Consciousness Pattern": {
        "human_problem": "Modern people often feel split between matter and meaning, science and faith, body and soul, observation and worship.",
        "biblical_grounding": "Ground in Genesis, Psalms of creation, wisdom literature, John 1, Colossians 1, Romans 8, and doctrines of creation, image of God, vocation, and worship.",
        "scholarly_conversation": "Needs physics, biology, cognitive science, philosophy of mind, theology of creation, ecological theology, and critique of simplistic ladders from matter to worship.",
        "cross_cultural_listening": "Compare creation stories, ecological traditions, body practices, wisdom texts, and human vocation across cultures while preserving differences in doctrine.",
        "pressure_test": "Test against evolution debates, disability, animal consciousness, ecological loss, suffering in nature, and claims that science mechanically proves worship.",
        "practical_response": "Practice wonder, stewardship, embodied care, learning, humility, and worship that honors creation without confusing creation with the Creator.",
    },
}


LANGUAGE_FAMILY_MARKERS = {
    "Afro-Asiatic": [
        "afro-asiatic",
        "hebrew",
        "arabic",
        "aramaic",
        "amharic",
        "akkadian",
        "coptic",
    ],
    "Indo-European": [
        "indo-european",
        "greek",
        "latin",
        "sanskrit",
        "english",
        "spanish",
        "french",
        "german",
        "russian",
        "persian",
        "hindi",
    ],
    "Sino-Tibetan": [
        "sino-tibetan",
        "chinese",
        "mandarin",
        "classical chinese",
        "tibetan",
        "burmese",
    ],
    "Niger-Congo": [
        "niger-congo",
        "swahili",
        "yoruba",
        "igbo",
        "zulu",
        "xhosa",
        "akan",
    ],
    "Austronesian": [
        "austronesian",
        "malay",
        "indonesian",
        "tagalog",
        "hawaiian",
        "maori",
    ],
    "Dravidian": [
        "dravidian",
        "tamil",
        "telugu",
        "kannada",
        "malayalam",
    ],
    "Turkic": [
        "turkic",
        "turkish",
        "azerbaijani",
        "uzbek",
        "kazakh",
        "uyghur",
    ],
    "Uralic": [
        "uralic",
        "finnish",
        "hungarian",
        "estonian",
        "sami",
    ],
    "Austroasiatic": [
        "austroasiatic",
        "vietnamese",
        "khmer",
        "mon",
    ],
    "Kra-Dai": [
        "kra-dai",
        "thai",
        "lao",
        "zhuang",
    ],
    "Japonic": [
        "japonic",
        "japanese",
        "ryukyuan",
    ],
    "Koreanic": [
        "koreanic",
        "korean",
    ],
    "Mongolic": [
        "mongolic",
        "mongolian",
    ],
    "Indigenous Americas": [
        "nahuatl",
        "maya",
        "quechua",
        "aymara",
        "navajo",
        "cherokee",
        "cree",
        "ojibwe",
        "mapuche",
    ],
    "Australian": [
        "aboriginal",
        "australian language",
        "yolngu",
        "warlpiri",
    ],
    "Papuan": [
        "papuan",
        "tok pisin",
        "hiri motu",
    ],
}


TEXT_TRADITION_MARKERS = {
    "Sacred Scripture": [
        "scripture",
        "sacred text",
        "bible",
        "quran",
        "torah",
        "veda",
        "sutra",
        "tripitaka",
        "avesta",
        "guru granth sahib",
    ],
    "Wisdom And Proverbs": [
        "wisdom",
        "proverb",
        "aphorism",
        "instruction",
        "teaching",
        "counsel",
    ],
    "Epic And Myth": [
        "epic",
        "myth",
        "origin story",
        "hero",
        "cosmogony",
        "creation story",
    ],
    "Philosophy And Ethics": [
        "philosophy",
        "ethics",
        "virtue",
        "metaphysics",
        "reason",
        "good life",
    ],
    "Law And Covenant": [
        "law",
        "code",
        "covenant",
        "contract",
        "justice",
        "judgment",
    ],
    "Poetry And Lament": [
        "poetry",
        "poem",
        "lament",
        "song",
        "hymn",
        "elegy",
    ],
    "Ritual And Liturgy": [
        "ritual",
        "liturgy",
        "prayer",
        "sacrifice",
        "festival",
        "ceremony",
    ],
    "History And Chronicle": [
        "history",
        "chronicle",
        "annals",
        "genealogy",
        "king",
        "empire",
    ],
    "Oral Tradition And Folklore": [
        "oral tradition",
        "folklore",
        "storytelling",
        "ancestor",
        "clan",
        "memory",
    ],
    "Commentary And Interpretation": [
        "commentary",
        "interpretation",
        "exegesis",
        "midrash",
        "tafsir",
        "scholia",
    ],
    "Modern Literature": [
        "modern literature",
        "novel",
        "short story",
        "drama",
        "memoir",
        "fiction",
        "narrator",
        "character",
    ],
    "Human Story And Testimony": [
        "human story",
        "lived story",
        "testimony",
        "case story",
        "interview",
        "memoir",
        "witness",
        "experience",
    ],
}


SYNTHESIS_LENSES = {
    "Surface Vocabulary": [
        "word",
        "term",
        "keyword",
        "phrase",
        "vocabulary",
        "label",
        "definition",
    ],
    "Visual Symbol": [
        "image",
        "icon",
        "painting",
        "composition",
        "color",
        "light",
        "shadow",
        "gesture",
        "symbol",
        "perspective",
    ],
    "Historical Context": [
        "history",
        "historical",
        "era",
        "empire",
        "exile",
        "war",
        "migration",
        "reform",
        "movement",
        "memory",
    ],
    "Language Semantics": [
        "language",
        "translation",
        "semantic",
        "metaphor",
        "idiom",
        "grammar",
        "syntax",
        "lemma",
        "lexicon",
        "meaning",
    ],
    "Original-Language Witness": [
        "greek",
        "hebrew",
        "aramaic",
        "septuagint",
        "masoretic",
        "logos",
        "agape",
        "hesed",
        "shalom",
        "ruach",
        "pneuma",
    ],
    "Psychological Process": [
        "psychology",
        "perception",
        "attention",
        "memory",
        "emotion",
        "attachment",
        "trauma",
        "habit",
        "motivation",
        "identity",
    ],
    "Embodied Practice": [
        "practice",
        "ritual",
        "habit",
        "body",
        "community",
        "relationship",
        "discipline",
        "care",
        "service",
    ],
    "Ethical Consequence": [
        "justice",
        "mercy",
        "responsibility",
        "power",
        "harm",
        "repair",
        "neighbor",
        "accountability",
        "dignity",
    ],
    "Theological Resonance": [
        "god",
        "trinity",
        "father",
        "son",
        "holy spirit",
        "christ",
        "logos",
        "creation",
        "redemption",
        "spirit",
    ],
    "Counter-Reading": [
        "counterargument",
        "objection",
        "alternative",
        "critique",
        "limitation",
        "does not fit",
        "risk",
        "overclaim",
    ],
}


TEST_PRESSURE_TYPES = {
    "Counterexample Pressure": [
        "counterexample",
        "does not fit",
        "breaks the pattern",
        "contradiction",
        "unresolved",
        "meaningless",
        "absurd",
        "random",
        "chaos",
    ],
    "Suffering Without Resolution": [
        "suffering",
        "silence",
        "unanswered",
        "grief",
        "trauma",
        "death",
        "chronic",
        "despair",
        "waiting",
    ],
    "Injustice And Corruption": [
        "injustice",
        "corruption",
        "abuse",
        "oppression",
        "violence",
        "exploitation",
        "racism",
        "poverty",
        "war",
    ],
    "Non-Christian Comparison": [
        "judaism",
        "islam",
        "hindu",
        "buddhist",
        "secular",
        "atheist",
        "humanist",
        "indigenous",
        "stoic",
    ],
    "Science Guardrail": [
        "quantum",
        "physics",
        "evidence",
        "measurement",
        "probability",
        "uncertainty",
        "experiment",
        "peer review",
        "overclaim",
    ],
    "Practical Case Study": [
        "case study",
        "daily life",
        "addiction",
        "marriage",
        "burnout",
        "workplace",
        "family",
        "church hurt",
        "recovery",
    ],
    "Rival Explanation": [
        "rival explanation",
        "alternative explanation",
        "natural explanation",
        "psychological explanation",
        "social explanation",
        "confirmation bias",
        "projection",
        "coincidence",
        "placebo",
    ],
    "Misuse And Weaponization": [
        "misuse",
        "weaponized",
        "manipulation",
        "control",
        "coercion",
        "domination",
        "silence victims",
        "protect institutions",
        "spiritual bypass",
    ],
    "Disconfirming Failure Condition": [
        "failure condition",
        "fails if",
        "would fail",
        "does not hold",
        "not hold",
        "falsify",
        "falsification",
        "disconfirm",
        "disconfirmation",
    ],
}


SOURCE_QUALITY_MARKERS = {
    "Primary Or Classical Source": [
        "scripture",
        "bible",
        "creed",
        "confessions",
        "summa",
        "primary source",
        "original source",
    ],
    "Scholarly Or Scientific Source": [
        "peer review",
        "journal",
        "study",
        "experiment",
        "evidence",
        "physicist",
        "theologian",
        "research",
    ],
    "Practical Lived Source": [
        "case study",
        "testimony",
        "pastoral",
        "counseling",
        "practice",
        "daily life",
        "community",
    ],
    "Reviewed Cloud Reference": [
        "reviewed cloud reference",
        "human reviewed",
        "source reviewed",
        "confirmed source",
        "vetted reference",
    ],
    "Unreviewed Cloud Reference": [
        "generated by internet_source_collector.py",
        "candidate reference",
        "candidate references",
        "search result",
        "cloud reference",
        "daily cloud",
        "unreviewed",
    ],
    "Speculative Source": [
        "maybe",
        "possibly",
        "speculation",
        "hypothesis",
        "could mean",
        "proof of god",
        "quantum proves",
    ],
}


DEEP_SOURCE_AREAS = {
    "Unresolved Suffering": {
        "terms": [
            "suffering",
            "lament",
            "grief",
            "trauma",
            "pain",
            "silence",
            "unanswered prayer",
            "waiting",
            "theodicy",
            "pastoral care",
            "job",
            "psalm",
        ],
        "required_source_types": [
            "Scripture/Theology",
            "Pastoral/Clinical",
            "Lived Case",
            "Counterargument",
        ],
        "guardrail": "Do not rush grief into easy resolution. Look for truthful lament, patient presence, embodied care, and hope without denial.",
    },
    "Quantum And Science Claims": {
        "terms": [
            "quantum",
            "physics",
            "measurement",
            "uncertainty",
            "probability",
            "wavefunction",
            "entanglement",
            "experiment",
            "peer review",
            "mathematics",
        ],
        "required_source_types": [
            "Physicist/Primary Science",
            "Peer-Reviewed/Academic",
            "Philosophy Of Science",
            "Counterargument",
        ],
        "guardrail": "Do not use quantum physics as vague proof of God. Keep science claims tied to evidence, scope, and qualified sources.",
    },
    "Mathematics Statistics And Logic": {
        "terms": [
            "theorem",
            "proof",
            "logic",
            "validity",
            "inference",
            "statistics",
            "statistical",
            "probability",
            "bayes",
            "correlation",
            "causation",
            "sample size",
            "base rate",
        ],
        "required_source_types": [
            "Mathematics/Logic",
            "Statistics/Inference",
            "Peer-Reviewed/Academic",
            "Counterargument",
        ],
        "guardrail": "Do not treat repeated patterns, analogies, or mathematical beauty as proof. Check validity, statistical inference, base rates, and alternative explanations.",
    },
    "Mathematical Theophany And Beauty": {
        "terms": [
            "theophany",
            "self-disclosure",
            "manifestation",
            "sign",
            "mathematical order",
            "pattern",
            "symmetry",
            "logic",
            "infinity",
            "beauty",
            "elegance",
            "harmony",
            "aesthetic",
        ],
        "required_source_types": [
            "Scripture/Theology",
            "Mathematics/Logic",
            "Aesthetics/Beauty",
            "Alternative Interpretation",
            "Counterargument",
        ],
        "guardrail": "Treat mathematical order and beauty as possible signs, not proof. Strengthen the analysis by naming naturalistic, Platonist, constructivist, cognitive, cultural, and aesthetic alternatives.",
    },
}


DEEP_SOURCE_TYPE_MARKERS = {
    "Scripture/Theology": [
        "scripture",
        "bible",
        "psalm",
        "job",
        "lamentations",
        "theology",
        "theodicy",
        "pastoral theology",
    ],
    "Pastoral/Clinical": [
        "pastoral",
        "counseling",
        "clinical",
        "trauma",
        "mental health",
        "care",
        "therapy",
    ],
    "Lived Case": [
        "case study",
        "testimony",
        "lived experience",
        "daily life",
        "community",
        "practice",
    ],
    "Counterargument": [
        "counterargument",
        "objection",
        "critique",
        "challenge",
        "does not prove",
        "alternative explanation",
        "limitation",
    ],
    "Alternative Interpretation": [
        "alternative interpretation",
        "alternative explanation",
        "naturalistic",
        "platonism",
        "platonist",
        "constructivist",
        "formalism",
        "fictionalism",
        "cognitive bias",
        "cultural formation",
        "selection effect",
    ],
    "Physicist/Primary Science": [
        "physicist",
        "experiment",
        "measurement",
        "laboratory",
        "data",
        "equation",
        "primary science",
    ],
    "Peer-Reviewed/Academic": [
        "peer review",
        "journal",
        "academic",
        "study",
        "research",
        "citation",
        "doi",
    ],
    "Philosophy Of Science": [
        "philosophy of science",
        "epistemology",
        "causality",
        "interpretation",
        "model",
        "realism",
        "probability",
    ],
    "Mathematics/Logic": [
        "theorem",
        "proof",
        "axiom",
        "logic",
        "valid",
        "invalid",
        "deduction",
        "induction",
        "category mistake",
        "godel",
        "incompleteness",
        "bayes theorem",
    ],
    "Statistics/Inference": [
        "statistics",
        "statistical",
        "sample size",
        "base rate",
        "correlation",
        "causation",
        "p-value",
        "confidence interval",
        "bayesian",
        "selection bias",
        "false positive",
    ],
    "Aesthetics/Beauty": [
        "beauty",
        "aesthetic",
        "elegance",
        "harmony",
        "proportion",
        "wonder",
        "sublime",
        "fittingness",
    ],
}


CONGRUENCE_FILTERS = {
    "Logic Validity Filter": {
        "terms": [
            "logic",
            "validity",
            "invalid",
            "deduction",
            "non sequitur",
            "contradiction",
            "category mistake",
            "equivocation",
        ],
        "rule": "Reject claims where the conclusion does not follow, terms shift meaning, or analogy is treated as identity.",
    },
    "Statistical Inference Filter": {
        "terms": [
            "statistics",
            "statistical",
            "sample size",
            "base rate",
            "correlation",
            "causation",
            "selection bias",
            "false positive",
            "confidence interval",
        ],
        "rule": "Pattern frequency cannot become evidence without sample size, base rates, comparison cases, and bias checks.",
    },
    "Bayesian Humility Filter": {
        "terms": [
            "bayes",
            "bayesian",
            "prior",
            "likelihood",
            "posterior",
            "evidence update",
        ],
        "rule": "New evidence should update confidence modestly and should not jump from compatibility to proof.",
    },
    "Formal Proof Boundary Filter": {
        "terms": [
            "theorem",
            "proof",
            "axiom",
            "incompleteness",
            "godel",
            "undecidable",
            "formal system",
        ],
        "rule": "Mathematical proof applies inside formal systems; it cannot be transferred directly into theology without philosophical argument.",
    },
    "Theophany Interpretation Filter": {
        "terms": [
            "theophany",
            "self-disclosure",
            "manifestation",
            "sign",
            "mathematical order",
            "symmetry",
            "infinity",
            "beauty",
            "elegance",
            "alternative interpretation",
            "naturalistic",
            "platonism",
            "constructivist",
            "formalism",
        ],
        "rule": "Mathematical order, symmetry, logic, infinity, and beauty may be explored as signs of divine self-disclosure only after contrasting non-theistic, Platonist, constructivist, cognitive, and cultural explanations are named.",
    },
    "Physics Scale Filter": {
        "terms": [
            "scale",
            "quantum",
            "classical",
            "macroscopic",
            "relativity",
            "thermodynamics",
            "entropy",
        ],
        "rule": "Do not move from quantum, cosmic, or thermodynamic claims to daily spiritual claims without a justified bridge.",
    },
    "Causality Filter": {
        "terms": [
            "causality",
            "cause",
            "causal",
            "mechanism",
            "correlation",
            "necessary",
            "sufficient",
        ],
        "rule": "Distinguish causation, correlation, compatibility, analogy, and theological interpretation.",
    },
}


THEOLOGICAL_ERAS = {
    "Patristic": [
        "ignatius",
        "irenaeus",
        "athanasius",
        "basil",
        "gregory of nazianzus",
        "gregory of nyssa",
        "augustine",
    ],
    "Medieval": [
        "anselm",
        "aquinas",
        "bonaventure",
        "julian of norwich",
        "catherine of siena",
    ],
    "Reformation": [
        "luther",
        "calvin",
        "zwingli",
        "teresa of avila",
        "john of the cross",
    ],
    "Modern": [
        "schleiermacher",
        "kierkegaard",
        "newman",
        "barth",
        "bonhoeffer",
        "rahner",
        "moltmann",
        "von balthasar",
    ],
    "Contemporary": [
        "james cone",
        "sarah coakley",
        "rowan williams",
        "n. t. wright",
        "willie james jennings",
        "beth felker jones",
    ],
}


THEOLOGICAL_CONCEPTS = {
    "Trinity": [
        "trinity",
        "father",
        "son",
        "holy spirit",
        "one god",
        "three persons",
    ],
    "Creation": [
        "creation",
        "creator",
        "providence",
        "order",
        "being",
    ],
    "Christology": [
        "christ",
        "incarnation",
        "logos",
        "cross",
        "resurrection",
        "atonement",
    ],
    "Pneumatology": [
        "holy spirit",
        "sanctification",
        "presence",
        "gifts",
        "communion",
    ],
    "Theodicy And Suffering": [
        "suffering",
        "evil",
        "lament",
        "theodicy",
        "cross",
    ],
    "Grace And Transformation": [
        "grace",
        "sanctification",
        "virtue",
        "transformation",
        "salvation",
    ],
    "Church And Practice": [
        "church",
        "worship",
        "sacrament",
        "liturgy",
        "community",
    ],
    "Justice And Public Life": [
        "justice",
        "poor",
        "oppression",
        "public",
        "liberation",
    ],
}


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "could",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "into",
    "is",
    "it",
    "not",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "them",
    "this",
    "to",
    "we",
    "with",
    "thou",
    "thee",
    "thy",
    "thine",
    "unto",
    "hath",
    "doth",
    "shall",
    "would",
    "could",
    "may",
    "yet",
    "upon",
    "therefore",
    "wherefore",
    "which",
    "who",
    "when",
    "what",
    "all",
    "but",
    "was",
    "had",
}


TERM_PATTERNS = {}


def find_documents(folder):
    """Find research documents to analyze."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
        and path.name.upper() != "SOURCES.MD"
    )


def find_pattern_inputs(folder):
    """Find user-supplied pattern seed files."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_music_documents(folder):
    """Find user-supplied lyric files to analyze."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_music_note_documents(folder):
    """Find user-supplied music-note files to analyze."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_cultural_documents(folder):
    """Find user-supplied art, politics, science, and culture files."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_pattern_test_documents(folder):
    """Find documents designed to test or challenge the divine pattern."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_deep_source_documents(folder):
    """Find deeper source files for unresolved suffering and quantum/science claims."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_theologian_documents(folder):
    """Find theologian source files across historical eras."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def find_synthesis_documents(folder):
    """Find documents for cross-layer synthesis lanes."""
    if not folder.exists():
        folder.mkdir(parents=True)

    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def read_document(path):
    """Read a research document."""
    return path.read_text(encoding="utf-8-sig", errors="replace")


def reviewed_note_count(text):
    """Estimate how many reviewed notes a source file contributes."""
    declared = re.search(r"Reviewed note count:\s*(\d+)", text, re.IGNORECASE)
    if declared:
        return max(1, int(declared.group(1)))

    table_note_ids = re.findall(r"^\|\s*[A-Z]{2,}-\d+\s*\|", text, flags=re.MULTILINE)
    if table_note_ids:
        return len(table_note_ids)

    return 1


def normalize_title(text):
    """Convert a phrase into a clean pattern title."""
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def split_sentences(text):
    """Split text into sentence-like units."""
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def split_lyric_lines(text):
    """Split lyrics into meaningful lines while ignoring section labels."""
    lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.fullmatch(r"\[[^\]]+\]|\([^\)]+\)", line):
            continue
        lines.append(line)

    return lines


def tokenize(text):
    """Turn text into lowercase words."""
    return re.findall(r"[a-zA-Z][a-zA-Z-]{2,}", text.lower())


def get_term_pattern(term):
    """Get a cached whole-word pattern for a search term."""
    lowered = term.lower()
    if lowered not in TERM_PATTERNS:
        escaped = re.escape(lowered)
        TERM_PATTERNS[lowered] = re.compile(rf"(?<![a-zA-Z]){escaped}(?![a-zA-Z])")

    return TERM_PATTERNS[lowered]


def normalize_lyric_line(line):
    """Normalize a lyric line so repeated refrains can be detected."""
    cleaned = re.sub(r"[^a-zA-Z0-9\s']", "", line.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def parse_note_token(token):
    """Parse a note token such as C4, F#3, Bb5, or A."""
    match = re.fullmatch(r"([A-Ga-g])([#bB]?)(-?\d)?", token.strip())
    if not match:
        return None

    name = (match.group(1).upper() + match.group(2).upper()).strip()
    octave_text = match.group(3)

    if name not in NOTE_OFFSETS:
        return None

    octave = int(octave_text) if octave_text is not None else 4

    return {
        "token": token,
        "name": name,
        "octave": octave,
        "midi": 12 * (octave + 1) + NOTE_OFFSETS[name],
        "pitch_class": NOTE_OFFSETS[name],
    }


def extract_note_events(text):
    """Extract note and chord events from a lightweight text notation."""
    events = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if ":" in stripped:
            stripped = stripped.split(":", 1)[1]

        for chord_text in re.findall(r"\[([^\]]+)\]", stripped):
            notes = [
                parsed
                for parsed in (parse_note_token(token) for token in chord_text.split())
                if parsed
            ]
            if notes:
                events.append({"type": "chord", "notes": notes})

        without_chords = re.sub(r"\[[^\]]+\]", " ", stripped)
        for token in re.findall(r"\b[A-Ga-g](?:#|b|B)?-?\d?\b", without_chords):
            parsed = parse_note_token(token)
            if parsed:
                events.append({"type": "note", "notes": [parsed]})

    return events


def event_root(event):
    """Return the lowest note in an event."""
    return min(event["notes"], key=lambda note: note["midi"])


def interval_class(first_note, second_note):
    """Return the interval class between two notes."""
    return abs(second_note["midi"] - first_note["midi"]) % 12


def melodic_intervals(events):
    """Find interval classes between adjacent melodic events."""
    roots = [event_root(event) for event in events]
    intervals = []

    for first, second in zip(roots, roots[1:]):
        intervals.append(interval_class(first, second))

    return intervals


def harmonic_intervals(events):
    """Find interval classes inside chord events."""
    intervals = []

    for event in events:
        notes = event["notes"]
        if len(notes) < 2:
            continue

        for index, first in enumerate(notes):
            for second in notes[index + 1 :]:
                intervals.append(interval_class(first, second))

    return intervals


def contour_steps(events):
    """Convert adjacent note movement into up, down, and same directions."""
    roots = [event_root(event) for event in events]
    contour = []

    for first, second in zip(roots, roots[1:]):
        difference = second["midi"] - first["midi"]
        if difference > 0:
            contour.append("up")
        elif difference < 0:
            contour.append("down")
        else:
            contour.append("same")

    return contour


def count_return_motifs(events):
    """Count how often note roots return after one intervening event."""
    roots = [event_root(event)["pitch_class"] for event in events]
    return sum(1 for first, third in zip(roots, roots[2:]) if first == third)


def summarize_science_math_relationships(interval_counts, consonance_count, tension_count):
    """Create careful relationship labels from note patterns."""
    relationships = Counter()

    if sum(interval_counts.values()) > 0:
        relationships["Mathematical Structure"] += sum(interval_counts.values())

    if interval_counts.get(7, 0) or interval_counts.get(5, 0):
        relationships["Small Integer Ratios"] += interval_counts.get(7, 0)
        relationships["Small Integer Ratios"] += interval_counts.get(5, 0)

    if interval_counts.get(0, 0):
        relationships["Symmetry And Return"] += interval_counts[0]

    if consonance_count:
        relationships["Acoustic Stability"] += consonance_count

    if tension_count:
        relationships["Tension And Resolution"] += tension_count

    return relationships


def count_meaning_contexts(text):
    """Count meaning-stage language beyond simple theological keywords."""
    counts = {}
    lowercase_text = text.lower()

    for context, terms in MEANING_CONTEXTS.items():
        counts[context] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_cultural_domains(text):
    """Count broad cultural domains such as art, politics, and science."""
    counts = {}
    lowercase_text = text.lower()

    for domain, terms in CULTURAL_DOMAINS.items():
        counts[domain] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_synthesis_lenses(text):
    """Count interpretive lenses that support deeper-than-word synthesis."""
    counts = {}
    lowercase_text = text.lower()

    for lens, terms in SYNTHESIS_LENSES.items():
        counts[lens] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_language_families(text):
    """Count language-family signals for global coverage tracking."""
    counts = {}
    lowercase_text = text.lower()

    for family, terms in LANGUAGE_FAMILY_MARKERS.items():
        counts[family] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_text_traditions(text):
    """Count broad text-tradition signals across world literature."""
    counts = {}
    lowercase_text = text.lower()

    for tradition, terms in TEXT_TRADITION_MARKERS.items():
        counts[tradition] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_pressure_types(text):
    """Count pressure-test categories that challenge a proposed pattern."""
    counts = {}
    lowercase_text = text.lower()

    for pressure_type, terms in TEST_PRESSURE_TYPES.items():
        counts[pressure_type] = sum(
            count_term_lower(lowercase_text, term) for term in terms
        )

    return counts


def count_source_quality_markers(text):
    """Count markers that help estimate source quality and overclaim risk."""
    counts = {}
    lowercase_text = text.lower()

    for marker, terms in SOURCE_QUALITY_MARKERS.items():
        counts[marker] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_deep_source_areas(text):
    """Count which deeper-source areas a file supports."""
    counts = {}
    lowercase_text = text.lower()

    for area, details in DEEP_SOURCE_AREAS.items():
        counts[area] = sum(
            count_term_lower(lowercase_text, term) for term in details["terms"]
        )

    return counts


def count_deep_source_types(text):
    """Count required source types for deeper review."""
    counts = {}
    lowercase_text = text.lower()

    for source_type, terms in DEEP_SOURCE_TYPE_MARKERS.items():
        counts[source_type] = sum(
            count_term_lower(lowercase_text, term) for term in terms
        )

    return counts


def count_congruence_filters(text):
    """Count math, statistics, logic, and physics filters mentioned by a source."""
    counts = {}
    lowercase_text = text.lower()

    for filter_name, details in CONGRUENCE_FILTERS.items():
        counts[filter_name] = sum(
            count_term_lower(lowercase_text, term) for term in details["terms"]
        )

    return counts


def count_theological_eras(text):
    """Count theologian-name signals grouped by historical era."""
    counts = {}
    lowercase_text = text.lower()

    for era, terms in THEOLOGICAL_ERAS.items():
        counts[era] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_theological_concepts(text):
    """Count deeper theological concept signals."""
    counts = {}
    lowercase_text = text.lower()

    for concept, terms in THEOLOGICAL_CONCEPTS.items():
        counts[concept] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def score_deep_source_area(area, source_type_counts, area_count):
    """Score whether a deep-source area has the required support."""
    if area_count <= 0:
        return "not addressed"

    required = DEEP_SOURCE_AREAS[area]["required_source_types"]
    present = [source_type for source_type in required if source_type_counts.get(source_type, 0) > 0]

    if len(present) == len(required):
        return "source-supported"
    if len(present) >= max(2, len(required) - 1):
        return "partially sourced"
    if present:
        return "under-sourced"
    return "claim-risk: no required source type"


def find_meaning_context_evidence(units):
    """Find short snippets supporting each meaning-stage context."""
    evidence = defaultdict(list)

    for unit in units:
        lowercase_unit = unit.lower()
        for context, terms in MEANING_CONTEXTS.items():
            if any(contains_term_lower(lowercase_unit, term) for term in terms):
                if len(evidence[context]) < 3:
                    evidence[context].append(unit[:240])

    return dict(evidence)


def detect_meaning_arc(units):
    """Track whether a text moves through meaning stages over time."""
    if not units:
        return []

    segment_size = max(1, len(units) // 3)
    segments = [
        ("Opening", units[:segment_size]),
        ("Middle", units[segment_size : segment_size * 2]),
        ("Ending", units[segment_size * 2 :]),
    ]
    arc = []

    for label, segment_units in segments:
        segment_text = "\n".join(segment_units)
        counts = Counter(count_meaning_contexts(segment_text))
        strongest = counts.most_common(1)[0] if counts else ("None", 0)
        arc.append(
            {
                "segment": label,
                "context": strongest[0],
                "count": strongest[1],
            }
        )

    return arc


def score_meaning_confidence(context_counts, meaning_arc):
    """Score whether a pattern is more than a loose word match."""
    nonzero_contexts = [context for context, count in context_counts.items() if count > 0]
    arc_contexts = [
        item["context"]
        for item in meaning_arc
        if item["context"] != "None" and item["count"] > 0
    ]
    unique_arc_contexts = set(arc_contexts)

    if len(nonzero_contexts) >= 4 and len(unique_arc_contexts) >= 2:
        return "context-supported pattern"
    if len(nonzero_contexts) >= 3:
        return "plausible meaning pattern"
    if len(nonzero_contexts) >= 2:
        return "thin meaning signal"
    if len(nonzero_contexts) == 1:
        return "word-level signal only"
    return "not enough meaning context"


def create_practical_theology_plan(context_counts):
    """Create practical theology applications from detected meaning contexts."""
    detected = [
        context
        for context in MEANING_STAGE_ORDER
        if context_counts.get(context, 0) > 0
    ]

    if not detected:
        return [
            "No practical theology plan yet. Add more source text, lyrics, notes, or observations with clear context."
        ]

    return [PRACTICAL_THEOLOGY_USES[context] for context in detected]


def infer_layers_from_cultural_domains(domain_counts):
    """Infer divine-pattern layer echoes from cultural domains."""
    layer_counts = Counter()

    for domain, count in domain_counts.items():
        if count <= 0:
            continue

        for layer in CULTURAL_DOMAIN_LAYER_MAP.get(domain, []):
            layer_counts[layer] += count

    return layer_counts


def create_practical_domain_plan(domain_counts):
    """Create practical theology applications from detected cultural domains."""
    detected = [
        domain
        for domain, count in sorted(domain_counts.items(), key=lambda item: item[1], reverse=True)
        if count > 0
    ]

    if not detected:
        return ["No cultural-domain application yet. Add clearer art, politics, science, or daily-life context."]

    return [PRACTICAL_DOMAIN_USES[domain] for domain in detected]


def score_synthesis_depth(lens_counts, meaning_context_counts, layer_counts, meaning_arc):
    """Score whether an analysis is doing synthesis rather than only word matching."""
    active_lenses = [lens for lens, count in lens_counts.items() if count > 0]
    active_meaning = [context for context, count in meaning_context_counts.items() if count > 0]
    active_layers = [layer for layer, count in layer_counts.items() if count > 0]
    arc_contexts = {
        item["context"]
        for item in meaning_arc
        if item["context"] != "None" and item["count"] > 0
    }

    if (
        len(active_lenses) >= 5
        and len(active_meaning) >= 4
        and len(active_layers) >= 4
        and len(arc_contexts) >= 2
    ):
        return "cross-layer synthesis"
    if len(active_lenses) >= 4 and len(active_meaning) >= 3 and len(active_layers) >= 3:
        return "multi-lens understanding"
    if len(active_lenses) >= 3 and len(active_meaning) >= 2:
        return "contextual interpretation"
    if len(active_lenses) >= 2:
        return "early synthesis signal"
    if active_lenses:
        return "lens detected but still word-heavy"
    return "surface signal only"


def score_comparative_validity(analysis):
    """Classify what a non-Christian or extra-biblical witness can actually prove."""
    layer_counts = Counter(analysis.get("layer_counts", {}))
    meaning_counts = Counter(analysis.get("meaning_context_counts", {}))
    lens_counts = Counter(analysis.get("synthesis_lens_counts", {}))
    trinity_counts = Counter(analysis.get("trinity_counts", {}))

    layer_breadth = sum(1 for count in layer_counts.values() if count > 0)
    meaning_breadth = sum(1 for count in meaning_counts.values() if count > 0)
    trinity_breadth = sum(1 for person in TRINITY_PERSONS if trinity_counts.get(person, 0) > 0)
    has_counter_reading = lens_counts.get("Counter-Reading", 0) > 0

    if layer_breadth >= 4 and meaning_breadth >= 4 and has_counter_reading:
        return "strong shared-human pattern; Trinitarian claim still needs Christian sources"
    if layer_breadth >= 3 and meaning_breadth >= 3:
        return "shared-human pattern signal"
    if trinity_breadth >= 2:
        return "explicit Trinitarian overlap; check source context"
    if has_counter_reading:
        return "useful counter-reading, not validation"
    return "too thin for comparative validation"


def create_synthesis_questions(lens_counts, domain_counts, layer_counts):
    """Create follow-up questions that force deeper comparison across layers."""
    questions = []

    if lens_counts.get("Visual Symbol", 0) >= 2:
        questions.append("What does the visual form communicate before any explanation is added?")
    if lens_counts.get("Historical Context", 0) >= 3:
        questions.append("How does the pattern change when placed in its historical conflict, memory, and consequence?")
    if lens_counts.get("Language Semantics", 0) >= 4 or lens_counts.get("Original-Language Witness", 0) >= 2:
        questions.append("What meanings appear, disappear, or shift when translation, grammar, and original-language range are checked?")
    if lens_counts.get("Psychological Process", 0) >= 3:
        questions.append("What human processes are involved: perception, attachment, trauma, habit, desire, identity, or repair?")
    if layer_counts.get("Moral Response", 0) >= 3:
        questions.append("What responsibility, justice, mercy, or repair does this pattern call for?")
    if domain_counts.get("Biblical Greek And Hebrew", 0) >= 2:
        questions.append("Does the original-language evidence support the theological claim, or only suggest a possible reading?")
    if domain_counts.get("Psychology And Human Behavior", 0) >= 3:
        questions.append("Does psychology illuminate the pattern without reducing spiritual meaning to mechanism?")

    if not questions:
        questions.append("What context beyond repeated words would make this interpretation stronger or weaker?")

    return questions


def score_global_coverage(language_family_counts, text_tradition_counts):
    """Score global text coverage without pretending the corpus is complete."""
    family_breadth = sum(1 for count in language_family_counts.values() if count > 0)
    tradition_breadth = sum(1 for count in text_tradition_counts.values() if count > 0)

    if family_breadth >= 10 and tradition_breadth >= 8:
        return "broad global coverage map"
    if family_breadth >= 6 and tradition_breadth >= 5:
        return "developing global coverage map"
    if family_breadth >= 3 and tradition_breadth >= 3:
        return "early global coverage map"
    if family_breadth or tradition_breadth:
        return "starter global coverage map"
    return "no global-language coverage yet"


def score_test_confidence(analysis):
    """Score whether a tested pattern is resilient or fragile."""
    pressure_counts = Counter(analysis["pressure_counts"])
    quality_counts = Counter(analysis["source_quality_counts"])
    meaning_counts = Counter(analysis["meaning_context_counts"])
    trinity_counts = Counter(analysis["trinity_counts"])

    pressure_total = sum(pressure_counts.values())
    quality_total = quality_counts.get("Primary Or Classical Source", 0)
    quality_total += quality_counts.get("Scholarly Or Scientific Source", 0)
    quality_total += quality_counts.get("Practical Lived Source", 0)
    speculative_total = quality_counts.get("Speculative Source", 0)
    meaning_breadth = sum(1 for count in meaning_counts.values() if count > 0)
    trinity_breadth = sum(1 for person in TRINITY_PERSONS if trinity_counts.get(person, 0) > 0)

    score = quality_total + meaning_breadth + trinity_breadth
    score -= speculative_total

    if pressure_total >= 5 and score >= 6:
        return "resilient under pressure"
    if pressure_total >= 3 and score >= 3:
        return "needs deeper review but still plausible"
    if speculative_total > quality_total:
        return "high overclaim risk"
    if pressure_total == 0:
        return "untested confirmation signal"
    return "fragile or incomplete test"


def score_hold_assessment(analysis):
    """Estimate whether the pattern holds after disconfirming friction."""
    pressure_counts = Counter(analysis["pressure_counts"])
    quality_counts = Counter(analysis["source_quality_counts"])
    meaning_counts = Counter(analysis["meaning_context_counts"])
    trinity_counts = Counter(analysis["trinity_counts"])

    friction_total = (
        pressure_counts.get("Disconfirming Failure Condition", 0)
        + pressure_counts.get("Rival Explanation", 0)
        + pressure_counts.get("Misuse And Weaponization", 0)
    )
    pressure_total = sum(pressure_counts.values())
    quality_total = quality_counts.get("Primary Or Classical Source", 0)
    quality_total += quality_counts.get("Scholarly Or Scientific Source", 0)
    quality_total += quality_counts.get("Practical Lived Source", 0)
    meaning_breadth = sum(1 for count in meaning_counts.values() if count > 0)
    trinity_breadth = sum(1 for person in TRINITY_PERSONS if trinity_counts.get(person, 0) > 0)

    if friction_total >= 3 and (meaning_breadth < 2 or trinity_breadth < 2):
        return "does not hold yet under this friction"
    if friction_total >= 6 and meaning_breadth >= 4 and trinity_breadth >= 2 and quality_total >= 3:
        return "holds under added friction"
    if friction_total >= 3 and meaning_breadth >= 3 and trinity_breadth >= 1:
        return "provisionally holds; needs stronger review"
    if pressure_total >= 5:
        return "pressure present but hold question is underdeveloped"
    return "not enough friction to judge hold"


def create_test_recommendations(pressure_counts, source_quality_counts):
    """Recommend next research steps based on test gaps."""
    recommendations = []

    if pressure_counts.get("Suffering Without Resolution", 0) == 0:
        recommendations.append("Add cases where suffering, grief, or unanswered prayer does not resolve quickly.")

    if pressure_counts.get("Non-Christian Comparison", 0) == 0:
        recommendations.append("Add non-Christian and secular comparison sources to identify what is uniquely Trinitarian.")

    if pressure_counts.get("Science Guardrail", 0) == 0:
        recommendations.append("Add physicist-authored sources before making quantum or science-related claims.")

    if pressure_counts.get("Practical Case Study", 0) == 0:
        recommendations.append("Add concrete daily-life case studies so the pattern can be used, not just admired.")

    if pressure_counts.get("Disconfirming Failure Condition", 0) == 0:
        recommendations.append("Name explicit failure conditions so the pattern can be revised or rejected.")

    if pressure_counts.get("Rival Explanation", 0) == 0:
        recommendations.append("Add rival natural, psychological, social, or comparative explanations.")

    if source_quality_counts.get("Speculative Source", 0) > source_quality_counts.get("Scholarly Or Scientific Source", 0):
        recommendations.append("Reduce speculative claims or pair them with stronger sources and counterarguments.")

    if not recommendations:
        recommendations.append("Continue testing with harder cases and outside critique.")

    return recommendations


def contains_term(text, term):
    """Check whether a term appears as a phrase or whole word."""
    return contains_term_lower(text.lower(), term)


def contains_term_lower(lowercase_text, term):
    """Check whether a term appears in already-lowercase text."""
    lowered_term = term.lower()
    if lowered_term not in lowercase_text:
        return False

    return get_term_pattern(lowered_term).search(lowercase_text) is not None


def count_term(text, term):
    """Count phrase or whole-word matches."""
    return count_term_lower(text.lower(), term)


def count_term_lower(lowercase_text, term):
    """Count phrase or whole-word matches in already-lowercase text."""
    lowered_term = term.lower()
    if lowered_term not in lowercase_text:
        return 0

    return len(get_term_pattern(lowered_term).findall(lowercase_text))


def count_theme_matches(text):
    """Count how often each theme appears in a document."""
    counts = {}
    lowercase_text = text.lower()

    for theme, terms in THEMES.items():
        counts[theme] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_trinity_person_matches(text):
    """Count Father, Son, and Holy Spirit language separately."""
    counts = {}
    lowercase_text = text.lower()

    for person, details in TRINITY_PERSONS.items():
        counts[person] = sum(
            count_term_lower(lowercase_text, term) for term in details["terms"]
        )

    return counts


def count_domain_matches(text):
    """Count how often each test domain appears in a document."""
    counts = {}
    lowercase_text = text.lower()

    for domain, terms in TEST_DOMAINS.items():
        counts[domain] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_layer_matches(text):
    """Count how often each divine-pattern layer appears in a document."""
    counts = {}
    lowercase_text = text.lower()

    for layer, details in DIVINE_PATTERN_LAYERS.items():
        counts[layer] = sum(
            count_term_lower(lowercase_text, term) for term in details["terms"]
        )

    return counts


def count_lyric_alignment_matches(text):
    """Count biblical and religious motif language in lyrics."""
    counts = {}
    lowercase_text = text.lower()

    for pattern, terms in LYRIC_ALIGNMENT_PATTERNS.items():
        counts[pattern] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def count_general_music_matches(text):
    """Count broad human motifs that appear across many kinds of music."""
    counts = {}
    lowercase_text = text.lower()

    for pattern, terms in GENERAL_MUSIC_PATTERNS.items():
        counts[pattern] = sum(count_term_lower(lowercase_text, term) for term in terms)

    return counts


def find_evidence_sentences(sentences):
    """Find short evidence snippets for each theme."""
    evidence = defaultdict(list)

    for sentence in sentences:
        lowercase_sentence = sentence.lower()
        for theme, terms in THEMES.items():
            if any(contains_term_lower(lowercase_sentence, term) for term in terms):
                if len(evidence[theme]) < 3:
                    evidence[theme].append(sentence[:280])

    return dict(evidence)


def find_trinity_evidence(sentences):
    """Find evidence snippets for each Trinitarian person."""
    evidence = defaultdict(list)

    for sentence in sentences:
        lowercase_sentence = sentence.lower()
        for person, details in TRINITY_PERSONS.items():
            if any(
                contains_term_lower(lowercase_sentence, term)
                for term in details["terms"]
            ):
                if len(evidence[person]) < 3:
                    evidence[person].append(sentence[:280])

    return dict(evidence)


def find_trinitarian_co_presence(sentences):
    """Find sentence-level places where more than one Trinitarian person appears."""
    co_presence = []

    for sentence in sentences:
        lowercase_sentence = sentence.lower()
        matched = []

        for person, details in TRINITY_PERSONS.items():
            if any(
                contains_term_lower(lowercase_sentence, term)
                for term in details["terms"]
            ):
                matched.append(person)

        if len(matched) >= 2:
            co_presence.append(
                {
                    "persons": matched,
                    "sentence": sentence[:320],
                }
            )

    return co_presence


def find_layer_evidence(sentences):
    """Find evidence snippets for each divine-pattern layer."""
    evidence = defaultdict(list)

    for sentence in sentences:
        lowercase_sentence = sentence.lower()
        for layer, details in DIVINE_PATTERN_LAYERS.items():
            if any(
                contains_term_lower(lowercase_sentence, term)
                for term in details["terms"]
            ):
                if len(evidence[layer]) < 3:
                    evidence[layer].append(sentence[:280])

    return dict(evidence)


def find_lyric_alignment_evidence(lines):
    """Find lyric lines that match biblical or religious motif patterns."""
    evidence = defaultdict(list)

    for line in lines:
        lowercase_line = line.lower()
        for pattern, terms in LYRIC_ALIGNMENT_PATTERNS.items():
            if any(contains_term_lower(lowercase_line, term) for term in terms):
                if len(evidence[pattern]) < 3:
                    evidence[pattern].append(line[:220])

    return dict(evidence)


def find_general_music_evidence(lines):
    """Find lyric lines that match broad music motif patterns."""
    evidence = defaultdict(list)

    for line in lines:
        lowercase_line = line.lower()
        for pattern, terms in GENERAL_MUSIC_PATTERNS.items():
            if any(contains_term_lower(lowercase_line, term) for term in terms):
                if len(evidence[pattern]) < 3:
                    evidence[pattern].append(line[:220])

    return dict(evidence)


def infer_layers_from_music_patterns(general_counts):
    """Infer divine-pattern layer echoes from broad music motifs."""
    layer_counts = Counter()

    for pattern, count in general_counts.items():
        if count <= 0:
            continue

        for layer in MUSIC_PATTERN_LAYER_MAP.get(pattern, []):
            layer_counts[layer] += count

    return layer_counts


def find_refrain_candidates(lines):
    """Find repeated lyric lines that may function like refrains."""
    normalized_to_original = {}
    line_counts = Counter()

    for line in lines:
        normalized = normalize_lyric_line(line)
        if len(normalized) < 5:
            continue

        line_counts[normalized] += 1
        normalized_to_original.setdefault(normalized, line)

    return [
        {
            "line": normalized_to_original[normalized],
            "count": count,
        }
        for normalized, count in line_counts.most_common(8)
        if count >= 2
    ]


def find_question_response_pairs(lines):
    """Find simple question/response patterns in adjacent lyric lines."""
    pairs = []

    for index, line in enumerate(lines[:-1]):
        if "?" not in line:
            continue

        pairs.append(
            {
                "question": line[:180],
                "response": lines[index + 1][:180],
            }
        )

        if len(pairs) >= 5:
            break

    return pairs


def create_lyric_arc(lines):
    """Summarize how the strongest divine-pattern layer moves through a lyric."""
    if len(lines) < 3:
        return []

    segment_size = max(1, len(lines) // 3)
    segments = [
        ("Opening", lines[:segment_size]),
        ("Middle", lines[segment_size : segment_size * 2]),
        ("Ending", lines[segment_size * 2 :]),
    ]
    arc = []

    for label, segment_lines in segments:
        segment_text = "\n".join(segment_lines)
        layer_counts = Counter(count_layer_matches(segment_text))
        pattern_counts = Counter(count_lyric_alignment_matches(segment_text))
        general_counts = Counter(count_general_music_matches(segment_text))
        inferred_counts = infer_layers_from_music_patterns(general_counts)
        layer_counts.update(inferred_counts)
        strongest_layer = layer_counts.most_common(1)[0] if layer_counts else ("None", 0)
        strongest_pattern = pattern_counts.most_common(1)[0] if pattern_counts else ("None", 0)
        strongest_general = (
            general_counts.most_common(1)[0] if general_counts else ("None", 0)
        )

        arc.append(
            {
                "segment": label,
                "layer": strongest_layer[0],
                "layer_count": strongest_layer[1],
                "pattern": strongest_pattern[0],
                "pattern_count": strongest_pattern[1],
                "general_pattern": strongest_general[0],
                "general_pattern_count": strongest_general[1],
            }
        )

    return arc


def find_cross_theme_patterns(sentences):
    """Find sentences where multiple disciplines appear together."""
    patterns = []

    for sentence in sentences:
        matched_themes = []
        lowercase_sentence = sentence.lower()

        for theme, terms in THEMES.items():
            if any(contains_term_lower(lowercase_sentence, term) for term in terms):
                matched_themes.append(theme)

        if len(matched_themes) >= 2:
            patterns.append(
                {
                    "themes": matched_themes,
                    "sentence": sentence[:320],
                }
            )

    return patterns


def analyze_document(path):
    """Analyze one research document."""
    text = read_document(path)
    sentences = split_sentences(text)
    words = [word for word in tokenize(text) if word not in STOP_WORDS]
    meaning_context_counts = count_meaning_contexts(text)
    meaning_arc = detect_meaning_arc(sentences)
    source_quality_counts = count_source_quality_markers(text)

    return {
        "file_name": path.name,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len(words),
        "theme_counts": count_theme_matches(text),
        "trinity_counts": count_trinity_person_matches(text),
        "trinity_evidence": find_trinity_evidence(sentences),
        "trinitarian_co_presence": find_trinitarian_co_presence(sentences),
        "domain_counts": count_domain_matches(text),
        "layer_counts": count_layer_matches(text),
        "top_terms": Counter(words).most_common(15),
        "evidence": find_evidence_sentences(sentences),
        "layer_evidence": find_layer_evidence(sentences),
        "cross_theme_patterns": find_cross_theme_patterns(sentences),
        "source_quality_counts": source_quality_counts,
        "meaning_context_counts": meaning_context_counts,
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "practical_theology_plan": create_practical_theology_plan(
            meaning_context_counts,
        ),
    }


def analyze_music_document(path):
    """Analyze one lyric document for biblical and religious pattern alignment."""
    text = read_document(path)
    lyric_lines = split_lyric_lines(text)
    lyric_text = "\n".join(lyric_lines)
    sentence_units = split_sentences(lyric_text)
    words = [word for word in tokenize(lyric_text) if word not in STOP_WORDS]
    theme_counts = Counter(count_theme_matches(lyric_text))
    trinity_counts = Counter(count_trinity_person_matches(lyric_text))
    layer_counts = Counter(count_layer_matches(lyric_text))
    alignment_counts = Counter(count_lyric_alignment_matches(lyric_text))
    general_counts = Counter(count_general_music_matches(lyric_text))
    meaning_context_counts = count_meaning_contexts(lyric_text)
    meaning_arc = detect_meaning_arc(lyric_lines)
    inferred_layer_counts = infer_layers_from_music_patterns(general_counts)
    combined_layer_counts = Counter(layer_counts)
    combined_layer_counts.update(inferred_layer_counts)
    strongest_theme = theme_counts.most_common(1)[0] if theme_counts else ("None", 0)
    strongest_layer = (
        combined_layer_counts.most_common(1)[0] if combined_layer_counts else ("None", 0)
    )
    strongest_alignment = (
        alignment_counts.most_common(1)[0] if alignment_counts else ("None", 0)
    )
    strongest_general = general_counts.most_common(1)[0] if general_counts else ("None", 0)

    alignment_score = sum(theme_counts.values())
    alignment_score += sum(combined_layer_counts.values())
    alignment_score += sum(alignment_counts.values())
    alignment_score += sum(general_counts.values())

    return {
        "file_name": path.name,
        "characters": len(text),
        "lines": len(lyric_lines),
        "words": len(words),
        "theme_counts": dict(theme_counts),
        "trinity_counts": dict(trinity_counts),
        "trinity_evidence": find_trinity_evidence(lyric_lines),
        "trinitarian_co_presence": find_trinitarian_co_presence(lyric_lines),
        "layer_counts": dict(combined_layer_counts),
        "direct_layer_counts": dict(layer_counts),
        "inferred_layer_counts": dict(inferred_layer_counts),
        "alignment_counts": dict(alignment_counts),
        "general_counts": dict(general_counts),
        "meaning_context_counts": meaning_context_counts,
        "meaning_context_evidence": find_meaning_context_evidence(lyric_lines),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "practical_theology_plan": create_practical_theology_plan(
            meaning_context_counts,
        ),
        "alignment_score": alignment_score,
        "strongest_theme": strongest_theme,
        "strongest_layer": strongest_layer,
        "strongest_alignment": strongest_alignment,
        "strongest_general": strongest_general,
        "top_terms": Counter(words).most_common(12),
        "alignment_evidence": find_lyric_alignment_evidence(lyric_lines),
        "general_evidence": find_general_music_evidence(lyric_lines),
        "layer_evidence": find_layer_evidence(sentence_units + lyric_lines),
        "refrain_candidates": find_refrain_candidates(lyric_lines),
        "question_response_pairs": find_question_response_pairs(lyric_lines),
        "lyric_arc": create_lyric_arc(lyric_lines),
    }


def analyze_music_note_document(path):
    """Analyze note sequences for mathematical and scientific music patterns."""
    text = read_document(path)
    sentences = split_sentences(text)
    events = extract_note_events(text)
    melody_intervals = melodic_intervals(events)
    chord_intervals = harmonic_intervals(events)
    all_intervals = melody_intervals + chord_intervals
    interval_counts = Counter(all_intervals)
    consonance_count = sum(interval_counts[interval] for interval in CONSONANT_INTERVALS)
    tension_count = sum(interval_counts[interval] for interval in TENSION_INTERVALS)
    contour = contour_steps(events)
    contour_counts = Counter(contour)
    return_motifs = count_return_motifs(events)
    science_math_relationships = summarize_science_math_relationships(
        interval_counts,
        consonance_count,
        tension_count,
    )
    meaning_context_counts = count_meaning_contexts(text)
    meaning_arc = detect_meaning_arc(sentences)
    trinity_counts = count_trinity_person_matches(text)

    layer_counts = Counter(
        {
            "Mathematical Structure": sum(interval_counts.values())
            + science_math_relationships.get("Small Integer Ratios", 0)
            + science_math_relationships.get("Symmetry And Return", 0),
            "Physical Order": consonance_count + tension_count,
            "Meaning And Logos": return_motifs + len(set(contour)),
            "Transformation": tension_count,
            "Worship And Community": len([event for event in events if event["type"] == "chord"]),
        }
    )

    return {
        "file_name": path.name,
        "events": len(events),
        "notes": sum(len(event["notes"]) for event in events),
        "chords": len([event for event in events if event["type"] == "chord"]),
        "melodic_intervals": len(melody_intervals),
        "harmonic_intervals": len(chord_intervals),
        "interval_counts": dict(interval_counts),
        "consonance_count": consonance_count,
        "tension_count": tension_count,
        "contour_counts": dict(contour_counts),
        "return_motifs": return_motifs,
        "science_math_relationships": dict(science_math_relationships),
        "layer_counts": dict(layer_counts),
        "trinity_counts": trinity_counts,
        "trinity_evidence": find_trinity_evidence(sentences),
        "trinitarian_co_presence": find_trinitarian_co_presence(sentences),
        "meaning_context_counts": meaning_context_counts,
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "practical_theology_plan": create_practical_theology_plan(
            meaning_context_counts,
        ),
    }


def analyze_cultural_document(path):
    """Analyze art, politics, science, and modern-life notes."""
    text = read_document(path)
    sentences = split_sentences(text)
    words = [word for word in tokenize(text) if word not in STOP_WORDS]
    domain_counts = count_cultural_domains(text)
    trinity_counts = count_trinity_person_matches(text)
    meaning_context_counts = count_meaning_contexts(text)
    meaning_arc = detect_meaning_arc(sentences)
    inferred_layer_counts = infer_layers_from_cultural_domains(domain_counts)
    direct_layer_counts = Counter(count_layer_matches(text))
    combined_layer_counts = Counter(direct_layer_counts)
    combined_layer_counts.update(inferred_layer_counts)

    return {
        "file_name": path.name,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len(words),
        "cultural_domain_counts": domain_counts,
        "trinity_counts": trinity_counts,
        "trinity_evidence": find_trinity_evidence(sentences),
        "trinitarian_co_presence": find_trinitarian_co_presence(sentences),
        "meaning_context_counts": meaning_context_counts,
        "layer_counts": dict(combined_layer_counts),
        "direct_layer_counts": dict(direct_layer_counts),
        "inferred_layer_counts": dict(inferred_layer_counts),
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "practical_theology_plan": create_practical_theology_plan(
            meaning_context_counts,
        ),
        "practical_domain_plan": create_practical_domain_plan(domain_counts),
    }


def analyze_synthesis_document(path, source_lane):
    """Analyze a cross-layer source such as art, history, language, or psychology."""
    text = read_document(path)
    sentences = split_sentences(text)
    words = [word for word in tokenize(text) if word not in STOP_WORDS]
    domain_counts = count_cultural_domains(text)
    lens_counts = count_synthesis_lenses(text)
    language_family_counts = count_language_families(text)
    text_tradition_counts = count_text_traditions(text)
    meaning_context_counts = count_meaning_contexts(text)
    trinity_counts = count_trinity_person_matches(text)
    meaning_arc = detect_meaning_arc(sentences)
    inferred_layer_counts = infer_layers_from_cultural_domains(domain_counts)
    direct_layer_counts = Counter(count_layer_matches(text))
    combined_layer_counts = Counter(direct_layer_counts)
    combined_layer_counts.update(inferred_layer_counts)

    return {
        "file_name": path.name,
        "source_lane": source_lane,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len(words),
        "cultural_domain_counts": domain_counts,
        "synthesis_lens_counts": lens_counts,
        "language_family_counts": language_family_counts,
        "text_tradition_counts": text_tradition_counts,
        "trinity_counts": trinity_counts,
        "global_coverage": score_global_coverage(
            language_family_counts,
            text_tradition_counts,
        ),
        "meaning_context_counts": meaning_context_counts,
        "layer_counts": dict(combined_layer_counts),
        "direct_layer_counts": dict(direct_layer_counts),
        "inferred_layer_counts": dict(inferred_layer_counts),
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "synthesis_depth": score_synthesis_depth(
            lens_counts,
            meaning_context_counts,
            combined_layer_counts,
            meaning_arc,
        ),
        "comparative_validity": score_comparative_validity(
            {
                "layer_counts": dict(combined_layer_counts),
                "meaning_context_counts": meaning_context_counts,
                "synthesis_lens_counts": lens_counts,
                "trinity_counts": trinity_counts,
            }
        ),
        "synthesis_questions": create_synthesis_questions(
            lens_counts,
            domain_counts,
            combined_layer_counts,
        ),
    }


def analyze_pattern_test_document(path):
    """Analyze documents that pressure-test the proposed divine pattern."""
    text = read_document(path)
    sentences = split_sentences(text)
    meaning_context_counts = count_meaning_contexts(text)
    pressure_counts = count_pressure_types(text)
    source_quality_counts = count_source_quality_markers(text)
    trinity_counts = count_trinity_person_matches(text)
    layer_counts = Counter(count_layer_matches(text))
    meaning_arc = detect_meaning_arc(sentences)
    analysis = {
        "file_name": path.name,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len([word for word in tokenize(text) if word not in STOP_WORDS]),
        "pressure_counts": pressure_counts,
        "source_quality_counts": source_quality_counts,
        "meaning_context_counts": meaning_context_counts,
        "trinity_counts": trinity_counts,
        "layer_counts": dict(layer_counts),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "trinity_evidence": find_trinity_evidence(sentences),
        "trinitarian_co_presence": find_trinitarian_co_presence(sentences),
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
    }
    analysis["test_confidence"] = score_test_confidence(analysis)
    analysis["hold_assessment"] = score_hold_assessment(analysis)
    analysis["recommendations"] = create_test_recommendations(
        pressure_counts,
        source_quality_counts,
    )
    return analysis


def analyze_deep_source_document(path):
    """Analyze deeper source files for required support and overclaim risk."""
    text = read_document(path)
    sentences = split_sentences(text)
    area_counts = count_deep_source_areas(text)
    source_type_counts = count_deep_source_types(text)
    congruence_filter_counts = count_congruence_filters(text)
    quality_counts = count_source_quality_markers(text)
    meaning_context_counts = count_meaning_contexts(text)
    pressure_counts = count_pressure_types(text)

    area_scores = {
        area: score_deep_source_area(area, source_type_counts, count)
        for area, count in area_counts.items()
    }

    return {
        "file_name": path.name,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len([word for word in tokenize(text) if word not in STOP_WORDS]),
        "area_counts": area_counts,
        "source_type_counts": source_type_counts,
        "congruence_filter_counts": congruence_filter_counts,
        "source_quality_counts": quality_counts,
        "meaning_context_counts": meaning_context_counts,
        "pressure_counts": pressure_counts,
        "area_scores": area_scores,
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
    }


def analyze_theologian_document(path):
    """Analyze theologian material for pattern-design support."""
    text = read_document(path)
    sentences = split_sentences(text)
    era_counts = count_theological_eras(text)
    concept_counts = count_theological_concepts(text)
    meaning_context_counts = count_meaning_contexts(text)
    trinity_counts = count_trinity_person_matches(text)
    layer_counts = Counter(count_layer_matches(text))
    meaning_arc = detect_meaning_arc(sentences)

    return {
        "file_name": path.name,
        "reviewed_note_count": reviewed_note_count(text),
        "characters": len(text),
        "sentences": len(sentences),
        "words": len([word for word in tokenize(text) if word not in STOP_WORDS]),
        "era_counts": era_counts,
        "concept_counts": concept_counts,
        "meaning_context_counts": meaning_context_counts,
        "trinity_counts": trinity_counts,
        "layer_counts": dict(layer_counts),
        "meaning_arc": meaning_arc,
        "meaning_confidence": score_meaning_confidence(
            meaning_context_counts,
            meaning_arc,
        ),
        "trinity_evidence": find_trinity_evidence(sentences),
        "trinitarian_co_presence": find_trinitarian_co_presence(sentences),
        "meaning_context_evidence": find_meaning_context_evidence(sentences),
    }


def combine_theme_counts(analyses):
    """Combine theme counts across every document."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis["theme_counts"])

    return combined


def combine_trinity_counts(analyses):
    """Combine Father, Son, and Holy Spirit counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("trinity_counts", {}))

    return combined


def combine_trinity_evidence(analyses):
    """Collect evidence snippets for each Trinitarian person."""
    combined = defaultdict(list)

    for analysis in analyses:
        for person, snippets in analysis.get("trinity_evidence", {}).items():
            for snippet in snippets:
                if len(combined[person]) < 4:
                    combined[person].append((analysis["file_name"], snippet))

    return dict(combined)


def combine_trinitarian_co_presence(analyses):
    """Collect snippets where multiple Trinitarian persons appear together."""
    combined = []

    for analysis in analyses:
        for item in analysis.get("trinitarian_co_presence", []):
            if len(combined) < 12:
                combined.append(
                    {
                        "file_name": analysis["file_name"],
                        "persons": item["persons"],
                        "sentence": item["sentence"],
                    }
                )

    return combined


def score_trinitarian_pattern(trinity_counts):
    """Score whether a corpus preserves distinction and unity."""
    present = [person for person in TRINITY_PERSONS if trinity_counts.get(person, 0) > 0]

    if len(present) == 3:
        minimum = min(trinity_counts[person] for person in TRINITY_PERSONS)
        if minimum >= 100:
            return "strong Trinitarian signal"
        if minimum >= 25:
            return "moderate Trinitarian signal"
        return "thin but complete Trinitarian signal"

    if present:
        return "partial Trinitarian signal"

    return "no explicit Trinitarian signal"


def combine_terms(analyses):
    """Combine repeated terms across every document."""
    combined = Counter()

    for analysis in analyses:
        combined.update(dict(analysis["top_terms"]))

    return combined


def combine_domain_counts(analyses):
    """Combine research-domain counts across every document."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis["domain_counts"])

    return combined


def combine_layer_counts(analyses):
    """Combine divine-pattern layer counts across every document."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("layer_counts", {}))

    return combined


def combine_meaning_context_counts(analyses):
    """Combine meaning-stage context counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("meaning_context_counts", {}))

    return combined


def combine_source_quality_counts(analyses):
    """Combine source-quality markers across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("source_quality_counts", {}))

    return combined


def combine_pressure_counts(analyses):
    """Combine pressure-test markers across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("pressure_counts", {}))

    return combined


def parse_claim_ledger(path=CLAIM_LEDGER_PATH):
    """Parse the claim ledger into a small reportable summary."""
    if not path.exists():
        return {"claims": [], "status_counts": Counter(), "kind_counts": Counter()}

    claims = []
    for line in read_document(path).splitlines():
        if not line.startswith("| DP-"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        claim = {
            "id": cells[0],
            "claim": cells[1],
            "kind": cells[2],
            "status": cells[3],
            "evidence_needed": cells[4],
            "pressure_test": cells[5],
        }
        claims.append(claim)

    return {
        "claims": claims,
        "status_counts": Counter(claim["status"] for claim in claims),
        "kind_counts": Counter(claim["kind"] for claim in claims),
    }


def load_reviewed_source_pack_names(path=REVIEWED_SOURCE_PACKS_PATH):
    """Return reviewed source-pack headings from the source-pack document."""
    if not path.exists():
        return []

    pack_names = []
    for line in read_document(path).splitlines():
        if line.startswith("## Pack"):
            pack_names.append(line.lstrip("# ").strip())

    return pack_names


def combine_alignment_counts(analyses):
    """Combine lyric alignment counts across every song."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis["alignment_counts"])

    return combined


def combine_general_music_counts(analyses):
    """Combine broad music motif counts across every song."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis["general_counts"])

    return combined


def combine_cultural_domain_counts(analyses):
    """Combine cultural domain counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("cultural_domain_counts", {}))

    return combined


def combine_synthesis_lens_counts(analyses):
    """Combine cross-layer synthesis lens counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("synthesis_lens_counts", {}))

    return combined


def combine_language_family_counts(analyses):
    """Combine language-family coverage signals across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("language_family_counts", {}))

    return combined


def combine_text_tradition_counts(analyses):
    """Combine text-tradition coverage signals across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("text_tradition_counts", {}))

    return combined


def combine_theological_era_counts(analyses):
    """Combine theologian-era counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("era_counts", {}))

    return combined


def combine_theological_concept_counts(analyses):
    """Combine theological concept counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("concept_counts", {}))

    return combined


def combine_layer_evidence(analyses):
    """Collect evidence snippets for each divine-pattern layer."""
    combined = defaultdict(list)

    for analysis in analyses:
        for layer, snippets in analysis["layer_evidence"].items():
            for snippet in snippets:
                if len(combined[layer]) < 4:
                    combined[layer].append((analysis["file_name"], snippet))

    return dict(combined)


def create_lane_balance_records(
    research_analyses,
    cultural_analyses,
    test_analyses,
    deep_source_analyses,
    theologian_analyses,
    synthesis_analyses,
):
    """Compare analyzed source-lane counts with target bands."""
    def count_notes(analyses):
        return sum(analysis.get("reviewed_note_count", 1) for analysis in analyses)

    actuals = Counter(
        {
            "research_documents": count_notes(research_analyses),
            "cultural_inputs": count_notes(cultural_analyses),
            "pattern_tests": count_notes(test_analyses),
            "deep_sources": count_notes(deep_source_analyses),
            "theologians": count_notes(theologian_analyses),
        }
    )

    for analysis in synthesis_analyses:
        lane_key = SYNTHESIS_LANE_KEYS.get(analysis.get("source_lane"))
        if lane_key:
            actuals[lane_key] += analysis.get("reviewed_note_count", 1)

    records = []
    for lane, target in SOURCE_LANE_TARGETS.items():
        actual = actuals.get(lane, 0)
        if actual < target["minimum"]:
            status = "below minimum - prioritize"
        elif actual > target["review_cap"]:
            status = "above review cap - pause unless thin lanes are growing"
        elif actual < target["target"]:
            status = "developing toward target"
        else:
            status = "healthy target range"

        records.append(
            {
                "lane": lane,
                "actual": actual,
                "minimum": target["minimum"],
                "target": target["target"],
                "review_cap": target["review_cap"],
                "purpose": target["purpose"],
                "status": status,
            }
        )

    return records


def append_lane_balance_section(lines, records):
    """Append human-readable lane balance target results."""
    lines.extend(["", "Source Lane Balance", "-------------------"])
    lines.append(
        "The assistant should not strengthen broad claims while relevant lanes are thin."
    )

    for record in records:
        lines.append(
            f"- {record['lane']}: {record['actual']:,} notes; target {record['minimum']:,}-{record['target']:,}, review cap {record['review_cap']:,}; {record['status']}. Purpose: {record['purpose']}."
        )

    priority = [
        record["lane"]
        for record in records
        if record["status"].startswith("below minimum")
    ]
    if priority:
        lines.append(
            "Priority lanes before stronger claims: " + ", ".join(priority[:8]) + "."
        )
    else:
        lines.append(
            "No lane is below its minimum target, but broad claims still need source-specific review."
        )


def append_claim_ledger_section(lines, ledger):
    """Append a compact claim-ledger snapshot."""
    claims = ledger["claims"]
    lines.extend(["", "Claim Ledger Snapshot", "---------------------"])
    if not claims:
        lines.append("- No claim ledger found yet.")
        return

    lines.append(
        "Claims are split by status so evidence, interpretation, discernment, analogy, and practice do not blur together."
    )
    for status, count in ledger["status_counts"].most_common():
        lines.append(f"- {status}: {count:,}")

    lines.append("Claims that should not be promoted without more review:")
    for claim in claims:
        if claim["status"] in {
            "research_question_only",
            "analogy_only",
            "discernment_question",
            "weakened_or_limited",
        }:
            lines.append(
                f"- {claim['id']} ({claim['status']}): {claim['claim']} Pressure: {claim['pressure_test']}"
            )


def append_cautious_confidence_section(lines):
    """Append the confidence language used by reports."""
    lines.extend(["", "Cautious Confidence Language", "----------------------------"])
    for label, definition in CAUTIOUS_CONFIDENCE_GLOSSARY:
        lines.append(f"- {label}: {definition}.")


def append_practical_theology_section(lines):
    """Append practical theology guidance for daily use."""
    lines.extend(["", "Practical Theology Use", "----------------------"])
    lines.append(
        "A divine pattern becomes useful only when it helps people love God and neighbor truthfully in ordinary life."
    )
    lines.append("Practice loop:")
    for step, description in PRACTICAL_THEOLOGY_LOOP:
        lines.append(f"- {step}: {description}.")
    lines.append(
        "Use it for family conflict, work, grief, spiritual gifts, interreligious encounter, justice, creativity, and pattern perception; review the fruit before strengthening the claim."
    )


def append_reviewed_source_packs_section(lines, pack_names):
    """Append reviewed source-pack status."""
    lines.extend(["", "Reviewed Source Packs", "---------------------"])
    if not pack_names:
        lines.append("- No reviewed source-pack document found yet.")
        return

    lines.append(
        "Each source pack ties a claim to primary sources, interpreters, counter-readings, pressure tests, and practical use."
    )
    for pack_name in pack_names:
        lines.append(f"- {pack_name}")


def append_growth_plan_section(
    lines,
    digest,
    ranked_patterns,
    pressure_counts,
    lane_records,
    ledger,
    pack_names,
):
    """Append concrete next steps for making the report and knowledge set stronger."""
    priority_lanes = [
        record
        for record in lane_records
        if record["status"].startswith("below minimum")
        or record["status"].startswith("developing")
    ]
    capped_lanes = [
        record for record in lane_records if record["status"].startswith("above review cap")
    ]
    top_patterns = [item["candidate"]["name"] for item in ranked_patterns[:5]]
    new_sources = digest.get("new_sources", [])
    new_layer_counts = Counter(digest.get("new_layer_counts", {}))
    new_evidence_counts = Counter(digest.get("new_automated_evidence_counts", {}))
    claim_status_counts = ledger.get("status_counts", Counter())
    weak_claim_count = sum(
        claim_status_counts.get(status, 0)
        for status in [
            "research_question_only",
            "analogy_only",
            "discernment_question",
            "weakened_or_limited",
        ]
    )
    newest_active_lanes = [
        "visual_art",
        "cultural_inputs",
        "theologians",
        "all_texts",
        "history_inputs",
    ]
    strongest_pressures = [
        pressure for pressure, count in pressure_counts.most_common(5) if count > 0
    ]

    lines.extend(
        [
            "",
            "What This Needs To Grow",
            "-----------------------",
            "The report gets stronger when it grows the knowledge set in a balanced way: more source review, harder pressure tests, clearer rival explanations, and better links between evidence and practical theology.",
            "",
            "Immediate next work:",
        ]
    )

    if priority_lanes:
        for record in priority_lanes[:6]:
            needed = max(0, record["target"] - record["actual"])
            lines.append(
                f"- Grow {record['lane']}: add about {needed:,} more reviewed notes toward the target. Purpose: {record['purpose']}."
            )
    else:
        lines.append(
            "- Lane counts are not below target, so the next growth should be depth: reviewed sources, counterarguments, and claim-specific source packs."
        )

    if capped_lanes:
        paused = ", ".join(record["lane"] for record in capped_lanes[:5])
        lines.append(
            f"- Slow down broad collection in overfull lanes ({paused}) until thinner lanes and source review catch up."
        )

    lines.extend(["", "Knowledge set it should build next:"])
    if top_patterns:
        lines.append(
            "- Build one reviewed source pack for each leading pattern: "
            + ", ".join(top_patterns)
            + "."
        )
    lines.append(
        "- Turn the newest active lanes into reviewed evidence instead of leaving them as cloud candidates: "
        + ", ".join(newest_active_lanes)
        + "."
    )
    if new_sources:
        review_count = min(7, len(new_sources))
        lines.append(
            f"- Review the {review_count:,} newest candidate references by original source, author expertise, publication context, and counterargument before they affect confidence."
        )
    else:
        lines.append(
            "- Add new candidate references only where they answer a named research gap; do not collect more material just to make the report longer."
        )

    lines.extend(["", "What it needs to test harder:"])
    if strongest_pressures:
        lines.append(
            "- Keep testing the leading patterns against the strongest current pressure areas: "
            + ", ".join(strongest_pressures)
            + "."
        )
    else:
        lines.append("- Add explicit pressure tests before calling any pattern strong.")
    lines.append(
        "- Add rival explanations from psychology, sociology, history, textual criticism, comparative religion, and ordinary pattern perception."
    )
    lines.append(
        "- Add failure conditions: name what evidence would weaken, revise, or reject each proposed divine pattern."
    )

    lines.extend(["", "What it needs to clarify before claiming a divine pattern:"])
    lines.append(
        "- Separate evidence, interpretation, discernment, analogy, and practical use in every major claim."
    )
    if weak_claim_count:
        lines.append(
            f"- Revisit {weak_claim_count:,} claim-ledger items that are still questions, analogies, discernment claims, or weakened claims."
        )
    else:
        lines.append("- Keep the claim ledger current so weak claims do not quietly become conclusions.")
    lines.append(
        f"- Expand reviewed source packs from {len(pack_names):,} current packs toward one pack per major claim and one pack per top pattern."
    )
    if new_evidence_counts:
        lines.append(
            "- Convert automated evidence labels into human review decisions; machine scores should route attention, not settle truth."
        )

    lines.extend(
        [
            "",
            "Growth rule: the next version should become less impressed by repeated signals and more disciplined about reviewed sources, counter-readings, and whether the pattern produces truthful love, justice, humility, worship, and repair.",
            "",
        ]
    )


LANE_SEARCH_TAGS = {
    "biblical_languages": ["biblical_languages", "biblical_language_source_depth"],
    "world_languages": ["world_languages_translation", "world_language_source_sampling"],
    "all_texts": ["global_text_traditions"],
    "other_religious_texts": ["global_text_traditions", "interreligious_dream_testimony"],
    "theologians": ["theologians_cross_era", "trinity"],
    "history_inputs": ["history_memory", "politics_justice"],
    "visual_art": ["art_beauty", "visual_media_patterns"],
    "psychology_inputs": ["psychology_patterns", "pattern_perception_divine_response"],
    "human_stories": ["unresolved_suffering", "interreligious_dream_testimony", "podcast_testimony_patterns"],
    "cultural_inputs": ["cultural_practice_patterns", "technology_ethics", "politics_justice"],
    "modern_literature": ["modern_literature_meaning"],
    "deep_sources": ["quantum_science_guardrails", "general_research_methods"],
    "pattern_tests": ["unresolved_suffering", "general_research_methods", "video_teaching_patterns"],
    "research_documents": ["general_research_methods", "trinity"],
}


PATTERN_SEARCH_FOCUS = {
    "Image Of God Pattern": ["image of God dignity disability theology cognitive science"],
    "Cross And Reversal Pattern": ["cross reversal suffering trauma theology liberation"],
    "Providence And Contingency Pattern": ["providence contingency chance tragedy theology"],
    "Trinity-As-Behavior Pattern": ["Trinity spiritual formation liturgy practical theology"],
    "Creation-To-Consciousness Pattern": ["creation consciousness moral agency worship science theology"],
}


PRESSURE_SEARCH_FOCUS = {
    "Suffering Without Resolution": "unresolved suffering lament pastoral theology no repair",
    "Injustice And Corruption": "injustice corruption power repair theological ethics",
    "Practical Case Study": "practical theology case study pastoral ethics daily life",
    "Disconfirming Failure Condition": "failure condition falsification theological method counterargument",
    "Science Guardrail": "science theology guardrail quantum overclaim philosophy science",
}


def build_next_search_strategy(
    digest,
    ranked_patterns,
    pressure_counts,
    lane_records,
    ledger,
    pack_names,
):
    """Convert analyzer recommendations into collector search inputs for the next run."""
    priority_records = [
        record
        for record in lane_records
        if record["status"].startswith("below minimum")
        or record["status"].startswith("developing")
    ]
    priority_records = sorted(
        priority_records,
        key=lambda record: (record["actual"] >= record["target"], record["actual"]),
    )
    priority_lanes = [record["lane"] for record in priority_records[:8]]
    paused_lanes = [
        record["lane"]
        for record in lane_records
        if record["status"].startswith("above review cap")
    ][:8]
    top_patterns = [item["candidate"]["name"] for item in ranked_patterns[:5]]
    weak_statuses = {
        "research_question_only",
        "analogy_only",
        "discernment_question",
        "weakened_or_limited",
    }
    weak_claim_count = sum(
        ledger.get("status_counts", Counter()).get(status, 0)
        for status in weak_statuses
    )

    modifiers = [
        "primary source",
        "counterargument",
        "source review",
        "case study",
        "practical theology",
        "video",
        "podcast",
        "image archive",
        "transcript",
        "caption",
    ]
    if weak_claim_count:
        modifiers.extend(["rival explanation", "failure condition"])
    if not digest.get("new_sources"):
        modifiers.extend(["recent review", "new evidence"])

    suggested_queries = []
    for lane in priority_lanes[:6]:
        tags = LANE_SEARCH_TAGS.get(lane, ["general_research_methods"])
        purpose = next(
            (record["purpose"] for record in priority_records if record["lane"] == lane),
            "source-specific review and counter-reading",
        )
        for tag in tags[:2]:
            suggested_queries.append(
                {
                    "tag": tag,
                    "query": f"{purpose} primary source counterargument",
                    "reason": f"{lane} is a priority lane for the next collector run.",
                }
            )

    for pattern in top_patterns[:5]:
        for query in PATTERN_SEARCH_FOCUS.get(pattern, [])[:1]:
            suggested_queries.append(
                {
                    "tag": "general_research_methods",
                    "query": f"{query} source review counterargument",
                    "reason": f"Build or improve reviewed source pack coverage for {pattern}.",
                }
            )

    for pressure, count in pressure_counts.most_common(5):
        query = PRESSURE_SEARCH_FOCUS.get(pressure)
        if count and query:
            suggested_queries.append(
                {
                    "tag": "general_research_methods",
                    "query": query,
                    "reason": f"Keep testing leading patterns against {pressure}.",
                }
            )

    media_queries = [
        {
            "tag": "visual_media_patterns",
            "query": "religious art image archive iconography visual theology source context counter-reading",
            "reason": "Find graphics/images for multimodal divine-pattern review.",
        },
        {
            "tag": "podcast_testimony_patterns",
            "query": "podcast testimony grief repair transformation faith transcript counterargument",
            "reason": "Find podcast/audio testimony candidates for multimodal review.",
        },
        {
            "tag": "video_teaching_patterns",
            "query": "video lecture documentary theology suffering justice spiritual formation transcript",
            "reason": "Find video candidates for multimodal review.",
        },
    ]
    suggested_queries.extend(media_queries)

    strategy = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "divine_pattern_analyzer.py",
        "purpose": "Feed report recommendations back into the next internet_source_collector.py run.",
        "priority_lanes": priority_lanes,
        "paused_lanes": paused_lanes,
        "top_patterns": top_patterns,
        "query_modifiers": list(dict.fromkeys(modifiers))[:10],
        "suggested_queries": suggested_queries[:30],
        "review_targets": {
            "newest_candidate_reference_count": min(7, len(digest.get("new_sources", []))),
            "weak_or_limited_claim_count": weak_claim_count,
            "current_source_pack_count": len(pack_names),
        },
        "guardrail": "Use these searches to diversify candidate leads, including videos, podcasts, and images; do not strengthen claims until source review, captions/transcripts or direct media observations, and counterarguments are recorded.",
    }
    return strategy


def save_next_search_strategy(strategy):
    SEARCH_STRATEGY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEARCH_STRATEGY_PATH.write_text(
        json.dumps(strategy, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def append_pattern_pressure_competition(lines, ranked_patterns, pressure_counts, limit=5):
    """Append top-pattern competition under shared pressure tests."""
    lines.extend(["", "Top-Five Pattern Competition", "----------------------------"])
    lines.append(
        "The top five should compete under pressure before being merged into one master pattern."
    )
    if pressure_counts:
        top_pressures = ", ".join(
            f"{label} ({count:,})" for label, count in pressure_counts.most_common(5)
        )
        lines.append(f"Current pressure-test material is most concentrated in: {top_pressures}.")
    else:
        lines.append("No pressure-test counts are available yet.")

    for index, item in enumerate(ranked_patterns[:limit], start=1):
        candidate = item["candidate"]
        profile = PATTERN_PRESSURE_PROFILES.get(candidate["name"], {})
        lines.extend(
            [
                "",
                f"{index}. {candidate['name']}",
                f"- Best use: {profile.get('best_use', candidate['interpretation'])}.",
                f"- Hardest pressure: {profile.get('hardest_pressure', candidate['risk'])}.",
                f"- Weakens if: {profile.get('weakens_if', candidate['risk'])}.",
                f"- Practical check: {profile.get('daily_use', 'ask what faithful action this pattern actually produces')}.",
            ]
        )


def append_reader_preface(lines):
    """Append a warm, book-style preface for non-specialist readers."""
    lines.extend(
        [
            "A Reader's Preface",
            "------------------",
            "This report is written for two kinds of readers at once: the person who wants a clear, practical explanation, and the careful student who wants the claims handled responsibly.",
            "The central idea is simple: Christian theology often sees God's work through patterns. Creation gives order. The Word gives meaning. The Spirit makes truth live in people and communities.",
            "But the project must stay honest. A pattern can guide discernment without becoming proof. It can be meaningful without being forced. It can help ordinary life only if it faces grief, injustice, doubt, history, science, and other religious traditions with humility.",
            "",
        ]
    )


def append_how_to_read_this_book(lines):
    """Append an accessible reading guide."""
    lines.extend(
        [
            "How To Read This",
            "----------------",
            "Read this like a field guide, not a verdict. A field guide helps you notice what is there, compare what you are seeing, and avoid mistaking one thing for another.",
            "When the report says evidence, it means source-located support. When it says discernment, it means a prayerful and accountable way of asking what the evidence may mean for life with God and neighbor.",
            "When it says high internal signal, it means the current collection repeats a pattern often. It does not mean the pattern has been proven. The scholarly work is to test the pattern, and the practical work is to ask what faithful response it invites.",
            "",
        ]
    )


def append_everyday_pattern_story(lines):
    """Append a relatable explanation of the divine-pattern movement."""
    lines.extend(
        [
            "The Pattern In Ordinary Life",
            "----------------------------",
            "A divine pattern is not only an idea on a page. It is a way of learning to notice how God may be calling human beings toward truth, love, repair, worship, and hope.",
            "In daily life the movement can be simple:",
            "",
            "Notice -> Name -> Discern -> Practice -> Review",
            "",
            "A parent notices a conflict at home and names the real wound instead of pretending everything is fine. A worker notices a system that treats people like tools and discerns a more just way to act. A grieving person names sorrow honestly and refuses a shallow answer. A community tests spiritual gifts by love, humility, truth, and fruit.",
            "This is practical theology: faith becoming wise action in actual human life.",
            "",
        ]
    )


def append_scholarly_spine(lines):
    """Append the scholarly structure in reader-friendly language."""
    lines.extend(
        [
            "The Scholarly Spine",
            "-------------------",
            "The project is built around several scholarly lenses.",
            "- Biblical typology asks whether earlier people, events, and institutions anticipate later fulfillment without ignoring their original context.",
            "- Redemptive metanarrative asks how creation, fall, covenant, redemption, restoration, and new creation shape the whole story.",
            "- Thematic analysis tracks repeated motifs such as divine pursuit, lament, mercy, judgment, wisdom, worship, and transformation.",
            "- Symbolic and narrative analysis asks what images, rituals, stories, and forms are doing, not only what words appear.",
            "- Digital theology uses computational tools to map patterns, but it must remain accountable to human interpretation, source quality, and theological judgment.",
            "- Practical theology asks whether the pattern helps people live faithfully in grief, work, family, worship, justice, service, and community.",
            "",
        ]
    )


def shorten_for_table(text, width):
    """Shorten text for fixed-width reader tables."""
    if len(text) <= width:
        return text
    return text[: max(0, width - 3)].rstrip() + "..."


def create_signal_bar(count, max_count, width=28):
    """Create a compact ASCII signal bar for text reports."""
    if max_count <= 0 or count <= 0:
        filled = 0
    else:
        filled = max(1, round((count / max_count) * width))
    return "#" * filled + "." * (width - filled)


def append_reader_layer_chart(lines, layer_counts):
    """Append a reader-facing chart of divine-pattern layer signal strength."""
    max_count = max(layer_counts.values(), default=0)
    lines.extend(
        [
            "At-A-Glance Layer Chart",
            "-----------------------",
            "This chart is a navigation aid, not a proof scale. Longer bars show where the current corpus has more internal signal; the guardrails still decide how much weight a signal should carry.",
            "",
            "Layer                         Signal                         Count     Reading",
            "-----                         ------                         -----     -------",
        ]
    )

    for layer in DIVINE_PATTERN_LAYERS:
        count = layer_counts.get(layer, 0)
        bar = create_signal_bar(count, max_count)
        lines.append(
            f"{layer:<29} {bar} {count:>8,}  {score_layer(count)}"
        )

    lines.extend(
        [
            "",
            "Reader note: Mathematical Theophany is deliberately placed between mathematical structure and the rest of the model. It asks whether order, pattern, symmetry, logic, infinity, and beauty may be read as possible signs of divine self-disclosure, while keeping alternative explanations visible.",
            "",
        ]
    )


def append_reader_chapter_map(lines, ranked_patterns, layer_counts, limit=5):
    """Append a compact chapter map before the longer reader chapters."""
    lines.extend(
        [
            "Chapter Map",
            "-----------",
            "Use this as the table of contents for the argument. Each chapter has a main movement, a live pressure test, and a signal level.",
            "",
            "No.  Pattern Family                 Signal   Status",
            "---  --------------                 ------   ------",
        ]
    )

    for index, item in enumerate(ranked_patterns[:limit], start=1):
        candidate = item["candidate"]
        family = shorten_for_table(candidate["name"], 30)
        support = sum(layer_counts.get(layer, 0) for layer in candidate["layers"])
        lines.append(
            f"{index:<4} {family:<30} {support:>7,}  {shorten_for_table(item['status'], 32)}"
        )
        lines.append(f"     Movement: {candidate['sequence']}")
        lines.append(f"     Test: {candidate['risk']}")

    lines.append("")


def append_reader_pattern_chapters(lines, ranked_patterns, layer_counts, limit=5):
    """Append top patterns as short reader-facing chapters."""
    lines.extend(["The Five Leading Pattern Chapters", "---------------------------------"])

    for index, item in enumerate(ranked_patterns[:limit], start=1):
        candidate = item["candidate"]
        profile = PATTERN_PRESSURE_PROFILES.get(candidate["name"], {})
        formation = PATTERN_FORMATION_PROFILES.get(candidate["name"], {})
        practical_response = formation.get(
            "practical_response",
            profile.get("daily_use", "ask what faithful action this pattern actually produces"),
        ).rstrip(".")
        lines.extend(
            [
                "",
                f"Chapter {index}: {candidate['name']}",
                "-" * (len(candidate["name"]) + 11),
                f"In plain language: {candidate['interpretation']}",
                f"Pattern movement: {candidate['sequence']}",
                f"Current reading: {item['status']}.",
                f"Why it matters: {profile.get('best_use', 'it helps organize one part of the larger divine-pattern question')}.",
                f"Human problem: {formation.get('human_problem', 'This pattern matters where ordinary life raises a question the research must face.')}",
                f"Biblical and theological grounding: {formation.get('biblical_grounding', candidate['evidence_needed'])}",
                f"Scholarly conversation: {formation.get('scholarly_conversation', candidate['evidence_needed'])}",
                f"Cross-cultural listening: {formation.get('cross_cultural_listening', 'Compare carefully without flattening difference or forcing agreement.')}",
                f"Where it must be tested: {profile.get('hardest_pressure', candidate['risk'])}.",
                f"Pressure test: {formation.get('pressure_test', profile.get('hardest_pressure', candidate['risk']))}",
                f"Daily-life practice: {practical_response}.",
                "Scholarly note: strengthen this chapter only with reviewed sources, counter-readings, and lane balance.",
                "Layer support in brief:",
            ]
        )
        for layer in candidate["layers"]:
            count = layer_counts.get(layer, 0)
            lines.append(f"- {layer}: {score_layer(count)} ({count:,} signals)")

    lines.append("")


def append_pattern_detection_to_formation(lines):
    """Explain how search remains active and routes into formation."""
    lines.extend(
        [
            "From Pattern Search To Pattern Formation",
            "----------------------------------------",
            "The search engine remains essential. It keeps scanning scripture, theology, culture, history, language, testimony, art, psychology, science, and pressure tests for recurring structures.",
            "The change is what happens next. A discovered pattern should not stop at a score. It should move through this path:",
            "",
            "Detected pattern -> candidate pattern -> formation chapter -> reviewed pattern",
            "",
            "Detected pattern: a repeated signal worth noticing.",
            "Candidate pattern: a named pattern with enough signal to test.",
            "Formation chapter: a reader-facing chapter that adds human problem, biblical grounding, scholarly conversation, cross-cultural listening, pressure test, and practical response.",
            "Reviewed pattern: a pattern strengthened only after source review, counter-readings, and lane balance.",
            "",
        ]
    )


def append_reader_case_studies(lines):
    """Append everyday examples that make the pattern relatable."""
    lines.extend(
        [
            "Everyday Case Studies",
            "---------------------",
            "Family conflict: The pattern begins with attention. What actually happened? Then truth-telling: what wound, sin, fear, or longing needs to be named? Discernment asks whether the next faithful act is apology, patience, boundary, counsel, or repair.",
            "",
            "Work and money: The pattern asks whether order serves dignity. A workplace can be efficient and still unjust. Practical theology asks how truth, service, stewardship, and courage should appear in decisions about labor, power, and responsibility.",
            "",
            "Grief without repair: The pattern must not force hope too quickly. Lament is not failure. A faithful pattern may look like presence, meals, silence, prayer, honest anger, and patient love before any visible resolution appears.",
            "",
            "Spiritual gifts: The project should ask whether gifts build up love and truth. A claimed gift becomes suspect when it produces control, spectacle, fear, pride, or harm. It becomes more credible when it serves, heals, corrects humbly, and strengthens community.",
            "",
            "Other religions and cultures: The pattern should compare respectfully. Christians may ask how God is present beyond explicit naming, but the project must preserve each tradition's own voice and not use other people merely as evidence for a pre-decided conclusion.",
            "",
        ]
    )


def append_reader_guardrails(lines):
    """Append simple scholarly guardrails for everyday readers."""
    lines.extend(
        [
            "Guardrails For A Careful Reader",
            "-------------------------------",
            "1. Do not confuse a repeated pattern with proof.",
            "2. Do not use suffering as a shortcut to a happy ending.",
            "3. Do not use science, math, or quantum language as a shortcut to theology.",
            "4. Do not flatten other religions into Christian language without listening to their own claims.",
            "5. Do not call something the Holy Spirit if it produces coercion, pride, fear, or harm.",
            "6. Do not strengthen a claim until weak source lanes have been developed.",
            "7. Do ask what practice of love, justice, worship, humility, repair, or hope the pattern invites today.",
            "",
        ]
    )


def score_layer(count):
    """Convert a raw layer count into a cautious strength label."""
    if count >= 1000:
        return "high internal signal"
    if count >= 250:
        return "moderate internal signal"
    if count >= 50:
        return "early signal"
    if count > 0:
        return "thin signal"
    return "not detected"


def score_candidate(candidate, layer_counts):
    """Score a candidate pattern from its required layers."""
    layer_scores = [layer_counts.get(layer, 0) for layer in candidate["layers"]]
    present_layers = sum(1 for score in layer_scores if score > 0)
    total_layers = len(candidate["layers"])
    minimum_signal = min(layer_scores) if layer_scores else 0

    if present_layers == total_layers and minimum_signal >= 250:
        return "high internal signal; not proof"
    if present_layers == total_layers and minimum_signal >= 50:
        return "well-represented hypothesis; needs review"
    if present_layers == total_layers:
        return "early complete hypothesis"
    if present_layers > 0:
        return "partial hypothesis"
    return "not detected"


def rank_divine_pattern_candidates(layer_counts):
    """Rank candidate pattern families by breadth and layer signal."""
    ranked = []

    for candidate in DIVINE_PATTERN_CANDIDATES:
        layer_scores = [layer_counts.get(layer, 0) for layer in candidate["layers"]]
        present_layers = sum(1 for score in layer_scores if score > 0)
        layer_total = sum(layer_scores)
        weakest_layer = min(layer_scores) if layer_scores else 0
        breadth_ratio = present_layers / max(1, len(candidate["layers"]))
        score = (breadth_ratio * 100000) + layer_total + weakest_layer
        ranked.append(
            {
                "candidate": candidate,
                "status": score_candidate(candidate, layer_counts),
                "layer_total": layer_total,
                "present_layers": present_layers,
                "total_layers": len(candidate["layers"]),
                "weakest_layer": weakest_layer,
                "score": score,
            }
        )

    return sorted(
        ranked,
        key=lambda item: (
            item["present_layers"] == item["total_layers"],
            item["score"],
            item["layer_total"],
        ),
        reverse=True,
    )


def append_top_pattern_families(lines, ranked_patterns, layer_counts, limit=5):
    """Append concise top-pattern summaries to a report."""
    for index, item in enumerate(ranked_patterns[:limit], start=1):
        candidate = item["candidate"]
        lines.extend(
            [
                "",
                f"{index}. {candidate['name']}",
                "-" * (len(candidate["name"]) + 3),
                f"Status: {item['status']}",
                f"Layer signal total: {item['layer_total']:,}",
                f"Layers present: {item['present_layers']:,}/{item['total_layers']:,}",
                f"Pattern: {candidate['sequence']}",
                f"Interpretation: {candidate['interpretation']}",
                "Layer support:",
            ]
        )
        for layer in candidate["layers"]:
            count = layer_counts.get(layer, 0)
            lines.append(f"- {layer}: {count:,} ({score_layer(count)})")
        lines.extend(
            [
                f"Evidence needed: {candidate['evidence_needed']}",
                f"Risk to avoid: {candidate['risk']}",
            ]
        )


def parse_pattern_seed(path):
    """Extract named patterns and arrow sequences from a user seed file."""
    text = read_document(path)
    lines = [line.strip() for line in text.splitlines()]
    named_patterns = []
    arrow_sequences = []
    mappings = []

    for line in lines:
        if not line:
            continue

        if "->" in line:
            parts = [normalize_title(part) for part in line.split("->")]
            parts = [part for part in parts if part]
            if len(parts) >= 2:
                arrow_sequences.append(parts)

            if len(parts) == 2:
                mappings.append((parts[0], parts[1]))
            continue

        if re.search(r"\bPattern$", line):
            named_patterns.append(normalize_title(line))

    return {
        "file_name": path.name,
        "named_patterns": named_patterns,
        "arrow_sequences": arrow_sequences,
        "mappings": mappings,
    }


def map_step_to_layer(step):
    """Map a seed step to the closest divine-pattern layer."""
    step_text = step.lower()
    best_layer = None
    best_score = 0

    for layer, details in DIVINE_PATTERN_LAYERS.items():
        score = sum(1 for term in details["terms"] if term.lower() in step_text)
        if score > best_score:
            best_layer = layer
            best_score = score

    direct_map = {
        "being": "Physical Order",
        "order": "Physical Order",
        "life": "Life And Consciousness",
        "consciousness": "Life And Consciousness",
        "meaning": "Meaning And Logos",
        "moral response": "Moral Response",
        "worship": "Worship And Community",
        "transformation": "Transformation",
        "father": "Physical Order",
        "creation": "Physical Order",
        "son logos": "Meaning And Logos",
        "son": "Meaning And Logos",
        "logos": "Meaning And Logos",
        "revelation and redemption": "Meaning And Logos",
        "holy spirit": "Transformation",
        "presence and transformation": "Transformation",
    }

    return direct_map.get(step_text, best_layer or "Unmapped")


def discover_patterns_from_seed(pattern_seed, layer_counts):
    """Generate additional pattern candidates from a seed structure."""
    discoveries = []

    for sequence in pattern_seed["arrow_sequences"]:
        layer_path = [map_step_to_layer(step) for step in sequence]
        unique_layers = [layer for layer in dict.fromkeys(layer_path) if layer != "Unmapped"]
        support = sum(layer_counts.get(layer, 0) for layer in unique_layers)

        if len(sequence) >= 3:
            name = f"{sequence[0]}-To-{sequence[-1]} Pattern"
            discoveries.append(
                {
                    "name": name,
                    "sequence": " -> ".join(sequence),
                    "layer_path": unique_layers,
                    "support": support,
                    "interpretation": "This seed sequence suggests a layered movement from "
                    f"{sequence[0]} toward {sequence[-1]}.",
                }
            )

    for source, target in pattern_seed["mappings"]:
        source_layer = map_step_to_layer(source)
        target_layer = map_step_to_layer(target)
        layer_path = list(dict.fromkeys([source_layer, target_layer]))
        support = sum(layer_counts.get(layer, 0) for layer in layer_path)
        discoveries.append(
            {
                "name": f"{source}-As-{target} Pattern",
                "sequence": f"{source} -> {target}",
                "layer_path": layer_path,
                "support": support,
                "interpretation": f"This mapping suggests interpreting {source} through {target}.",
            }
        )

    return discoveries


def discover_layer_bridge_patterns(layer_counts):
    """Generate bridge patterns from strong adjacent layers."""
    layer_order = list(DIVINE_PATTERN_LAYERS)
    discoveries = []

    for first, second, third in zip(layer_order, layer_order[1:], layer_order[2:]):
        first_count = layer_counts.get(first, 0)
        second_count = layer_counts.get(second, 0)
        third_count = layer_counts.get(third, 0)

        if min(first_count, second_count, third_count) <= 0:
            continue

        support = first_count + second_count + third_count
        discoveries.append(
            {
                "name": f"{first}-Through-{second}-To-{third}",
                "sequence": f"{first} -> {second} -> {third}",
                "layer_path": [first, second, third],
                "support": support,
                "interpretation": "This bridge appears where adjacent layers of the divine-pattern model are all represented in the corpus.",
            }
        )

    return discoveries


def create_divine_pattern_summary(layer_counts):
    """Create a responsible conclusion from detected layer evidence."""
    detected_layers = [
        layer for layer in DIVINE_PATTERN_LAYERS if layer_counts.get(layer, 0) > 0
    ]

    if len(detected_layers) == len(DIVINE_PATTERN_LAYERS):
        return (
            "The corpus contains evidence across every layer of the proposed model. "
            "This supports treating layered convergence as a serious research hypothesis, "
            "not as proof of divine reality."
        )

    if detected_layers:
        missing = [
            layer for layer in DIVINE_PATTERN_LAYERS if layer_counts.get(layer, 0) == 0
        ]
        return (
            "The corpus contains partial evidence for the layered model, but more sources "
            "are needed for: "
            + ", ".join(missing)
            + "."
        )

    return "The corpus does not yet contain enough evidence for the layered model."


def create_pattern_candidates_report(analyses):
    """Create a focused report of possible divine-pattern candidates."""
    layer_counts = combine_layer_counts(analyses)

    lines = [
        "Divine Pattern Candidates Report",
        "================================",
        "",
        "Purpose",
        "-------",
        "This report proposes possible divine-pattern candidates from the current corpus.",
        "These are research hypotheses, not proofs. Each candidate should be tested against stronger sources and fair criticism.",
        "",
        "Core Model",
        "----------",
        "Physical Order -> Mathematical Structure -> Mathematical Theophany -> Quantum Probability -> Life And Consciousness -> Meaning And Logos -> Moral Response -> Worship And Community -> Transformation",
        "",
        "Candidate Rankings",
        "------------------",
    ]

    ranked_candidates = rank_divine_pattern_candidates(layer_counts)

    append_top_pattern_families(lines, ranked_candidates, layer_counts, limit=5)

    lines.extend(
        [
            "",
            "Why Top Five Instead Of One",
            "---------------------------",
            "The project should not collapse the divine pattern into only one dominant sequence.",
            "A family of patterns is more honest: Logos, mathematical-theophany, creation-consciousness, Trinity-as-behavior, moral transformation, worship embodiment, cross/reversal, Spirit transformation, and science-humility patterns can each be tested separately.",
            "",
            "Responsible Claim",
            "-----------------",
            "AI can help compare these layers and generate research hypotheses about whether order, intelligibility, moral transformation, and worship form a coherent Christian pattern across reality and human life.",
        ]
    )

    return "\n".join(lines)


def create_top_patterns_report(analyses, synthesis_analyses, test_analyses, deep_source_analyses):
    """Create a concise top-five pattern-family report."""
    all_analyses = analyses + synthesis_analyses + test_analyses + deep_source_analyses
    layer_counts = combine_layer_counts(all_analyses)
    pressure_counts = combine_pressure_counts(test_analyses)
    ranked_patterns = rank_divine_pattern_candidates(layer_counts)

    lines = [
        "Top Five Divine Pattern Families Report",
        "======================================",
        "",
        "A Reader's Opening",
        "------------------",
        "The project is no longer asking for one dominant pattern to explain everything. It is learning to read several possible patterns side by side.",
        "Think of these as five chapters in a larger theological book. Each chapter asks how God's work may be recognized through scripture, history, human experience, and practical life.",
        "The patterns are not conclusions by themselves. They are disciplined hypotheses that must face suffering, other traditions, science limits, language context, history, and ordinary daily life.",
        "",
        "Purpose",
        "-------",
        "This report prevents the project from showing only one dominant pattern.",
        "Each family is a research hypothesis with its own support, limits, practical uses, and pressure tests.",
        "High signal means repeated internal support in the corpus; it does not mean proof.",
        "",
        "Five Chapters In Brief",
        "----------------------",
    ]
    append_reader_pattern_chapters(lines, ranked_patterns, layer_counts, limit=5)
    lines.extend(["", "Research Detail", "---------------"])
    append_top_pattern_families(lines, ranked_patterns, layer_counts, limit=5)
    append_pattern_pressure_competition(lines, ranked_patterns, pressure_counts, limit=5)
    append_cautious_confidence_section(lines)
    append_practical_theology_section(lines)
    lines.extend(
        [
            "",
            "Use Rule",
            "--------",
            "Do not merge these families too quickly. A pattern can be strong in one lane and weak in another.",
            "Treat the top five as separate hypotheses until source balance, counterarguments, and pressure tests justify synthesis.",
        ]
    )
    return "\n".join(lines)


def create_disciplined_theological_assistant_report(
    research_analyses,
    music_analyses,
    note_analyses,
    cultural_analyses,
    test_analyses,
    deep_source_analyses,
    theologian_analyses,
    synthesis_analyses,
):
    """Create the main discipline report for practical theological use."""
    all_analyses = (
        research_analyses
        + music_analyses
        + note_analyses
        + cultural_analyses
        + test_analyses
        + deep_source_analyses
        + theologian_analyses
        + synthesis_analyses
    )
    top_pattern_analyses = (
        research_analyses
        + synthesis_analyses
        + test_analyses
        + deep_source_analyses
        + theologian_analyses
    )
    layer_counts = combine_layer_counts(top_pattern_analyses)
    pressure_counts = combine_pressure_counts(test_analyses)
    source_quality_counts = combine_source_quality_counts(research_analyses)
    ranked_patterns = rank_divine_pattern_candidates(layer_counts)
    ledger = parse_claim_ledger()
    pack_names = load_reviewed_source_pack_names()
    lane_records = create_lane_balance_records(
        research_analyses,
        cultural_analyses,
        test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )

    lines = [
        "Disciplined Theological Assistant Report",
        "=======================================",
        "",
    ]
    append_reader_preface(lines)
    append_how_to_read_this_book(lines)
    append_pattern_detection_to_formation(lines)
    append_everyday_pattern_story(lines)
    append_scholarly_spine(lines)
    lines.extend(
        [
        "Non-Negotiable Guardrail",
        "------------------------",
        "The assistant may say a pattern is visible, supported, reviewed, useful, compatible, or theologically interpreted.",
        "It must not say a pattern is proven merely because repeated language, narrative similarity, scientific analogy, or spiritual testimony appears.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Evidence Versus Discernment",
        "---------------------------",
        "- Evidence: source-located support from texts, history, languages, art, psychology, statistics, theology, testimony, or pressure tests.",
        "- Reviewed evidence: evidence checked against source quality, counter-readings, lane balance, and claim boundaries.",
        "- Theological interpretation: a Christian reading shaped by scripture, doctrine, tradition, reason, and worship.",
        "- Discernment: prayerful, communal, morally accountable interpretation for faithful response.",
        "- Practical theology: the pattern tested in ordinary life by fruit, love, justice, truth, humility, and care.",
        "- Analogy: an illuminating comparison that must stay narrower than proof.",
        "",
        "Current Corpus Shape",
        "--------------------",
        f"Documents analyzed across all lanes: {len(all_analyses):,}",
        f"Top-pattern source documents: {len(top_pattern_analyses):,}",
        f"Pressure-test documents: {len(test_analyses):,}",
        f"Theologian documents: {len(theologian_analyses):,}",
        f"Dedicated synthesis documents: {len(synthesis_analyses):,}",
        ]
    )

    lines.extend(["", "The Main Pattern Chapters", "-------------------------"])
    append_reader_pattern_chapters(lines, ranked_patterns, layer_counts, limit=5)
    append_reader_case_studies(lines)
    append_reader_guardrails(lines)

    lines.extend(["", "Research Detail: Pattern Families", "---------------------------------"])
    append_top_pattern_families(lines, ranked_patterns, layer_counts, limit=5)
    append_pattern_pressure_competition(lines, ranked_patterns, pressure_counts, limit=5)
    append_claim_ledger_section(lines, ledger)
    append_lane_balance_section(lines, lane_records)
    append_reviewed_source_packs_section(lines, pack_names)
    append_cautious_confidence_section(lines)
    append_practical_theology_section(lines)

    lines.extend(["", "Cloud Reference Discipline", "--------------------------"])
    reviewed_cloud = source_quality_counts.get("Reviewed Cloud Reference", 0)
    unreviewed_cloud = source_quality_counts.get("Unreviewed Cloud Reference", 0)
    lines.append(f"- Reviewed cloud-reference markers: {reviewed_cloud:,}")
    lines.append(f"- Unreviewed cloud-reference markers: {unreviewed_cloud:,}")
    lines.append(
        "- Cloud references are leads until the original source, author expertise, date, venue, and counterarguments are checked."
    )

    lines.extend(
        [
            "",
            "Assistant Behavior Rules",
            "------------------------",
            "1. Start by naming the claim type: evidence, interpretation, discernment, analogy, or practical use.",
            "2. Cite or name the source lane before strengthening a claim.",
            "3. Ask which top-five pattern best fits and which pressure test might weaken it.",
            "4. Use other religious traditions respectfully and preserve real differences.",
            "5. Keep gifts of the Holy Spirit accountable to love, truth, humility, community, and fruit.",
            "6. Keep math, statistics, logic, and physics as discipline filters, not shortcuts to proof.",
            "7. Translate patterns into practice only with safeguards against control, denial, abuse, and spiritual bypass.",
            "",
            "One-Sentence Operating Summary",
            "------------------------------",
            "The Divine assistant should map possible divine patterns carefully, test them honestly, interpret them theologically, and help people practice faithful love in daily life without overstating the evidence.",
        ]
    )

    return "\n".join(lines)


def create_reader_book_report(
    research_analyses,
    music_analyses,
    note_analyses,
    cultural_analyses,
    test_analyses,
    deep_source_analyses,
    theologian_analyses,
    synthesis_analyses,
):
    """Create a book-style report for everyday readers with scholarly guardrails."""
    all_analyses = (
        research_analyses
        + music_analyses
        + note_analyses
        + cultural_analyses
        + test_analyses
        + deep_source_analyses
        + theologian_analyses
        + synthesis_analyses
    )
    top_pattern_analyses = (
        research_analyses
        + synthesis_analyses
        + test_analyses
        + deep_source_analyses
        + theologian_analyses
    )
    layer_counts = combine_layer_counts(top_pattern_analyses)
    ranked_patterns = rank_divine_pattern_candidates(layer_counts)
    pressure_counts = combine_pressure_counts(test_analyses)
    daily_digest = read_daily_research_digest()
    reference_catalog_summary = read_reference_catalog_summary()
    ledger = parse_claim_ledger()
    pack_names = load_reviewed_source_pack_names()
    lane_records = create_lane_balance_records(
        research_analyses,
        cultural_analyses,
        test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )

    lines = [
        "The Divine Pattern Reader",
        "=========================",
        "",
        "A Book-Style Guide For Everyday Readers And Careful Students",
        "------------------------------------------------------------",
        "",
    ]
    append_latest_run_snapshot(lines, daily_digest, reference_catalog_summary)
    append_learning_journal_entry(lines, daily_digest, ranked_patterns, pressure_counts)
    append_reader_preface(lines)
    append_how_to_read_this_book(lines)
    append_pattern_detection_to_formation(lines)
    append_everyday_pattern_story(lines)
    append_scholarly_spine(lines)
    append_reader_layer_chart(lines, layer_counts)
    append_reader_chapter_map(lines, ranked_patterns, layer_counts, limit=5)
    append_daily_development_chapter(lines, daily_digest)
    append_reader_pattern_chapters(lines, ranked_patterns, layer_counts, limit=5)
    append_reader_case_studies(lines)

    lines.extend(
        [
            "What The Research Currently Suggests",
            "------------------------------------",
            f"The project has analyzed {len(all_analyses):,} local documents across research, theology, music, culture, pressure tests, source reviews, and synthesis lanes.",
            f"The daily collector has retained {reference_catalog_summary.get('source_count', 0):,} cloud candidate references, including {daily_digest.get('new_count', 0):,} brand-new candidates in the latest run.",
            describe_visible_pattern_families(ranked_patterns),
            "These are best understood as chapters in an ongoing research book. They are not final proof claims.",
            "",
        ]
    )

    append_daily_reference_movement(lines, daily_digest, reference_catalog_summary)
    append_pattern_pressure_competition(lines, ranked_patterns, pressure_counts, limit=5)
    append_claim_ledger_section(lines, ledger)
    append_lane_balance_section(lines, lane_records)
    append_reviewed_source_packs_section(lines, pack_names)
    append_cautious_confidence_section(lines)
    append_reader_guardrails(lines)
    append_growth_plan_section(
        lines,
        daily_digest,
        ranked_patterns,
        pressure_counts,
        lane_records,
        ledger,
        pack_names,
    )

    lines.extend(
        [
            "Closing Practical Rule",
            "----------------------",
            "If a pattern does not help a person become more truthful, loving, humble, just, worshipful, patient, and practically faithful, it has not yet become practical theology.",
            "The report should therefore be read with both a scholar's caution and a disciple's question: what faithful response is being invited today?",
        ]
    )

    return "\n".join(lines)


def create_discovered_patterns_report(analyses, pattern_seeds):
    """Create a report from user-supplied pattern seed text."""
    layer_counts = combine_layer_counts(analyses)
    discoveries = []

    for pattern_seed in pattern_seeds:
        discoveries.extend(discover_patterns_from_seed(pattern_seed, layer_counts))

    discoveries.extend(discover_layer_bridge_patterns(layer_counts))
    discoveries = sorted(discoveries, key=lambda item: item["support"], reverse=True)

    lines = [
        "Discovered Patterns Report",
        "==========================",
        "",
        "Purpose",
        "-------",
        "This report reads user-supplied pattern seed text and generates additional candidate patterns from it.",
        "These are exploratory hypotheses, not conclusions.",
        "",
        "Pattern Seed Files",
        "------------------",
    ]

    if pattern_seeds:
        for pattern_seed in pattern_seeds:
            lines.append(f"- {pattern_seed['file_name']}")
            lines.append(f"  Named patterns found: {len(pattern_seed['named_patterns'])}")
            lines.append(f"  Arrow sequences found: {len(pattern_seed['arrow_sequences'])}")
    else:
        lines.append("- No pattern seed files found yet.")

    lines.extend(["", "Discovered Candidate Patterns", "-----------------------------"])

    if not discoveries:
        lines.append("- No discovered patterns yet. Add .txt or .md seed files to pattern_inputs.")
    else:
        for item in discoveries[:25]:
            lines.extend(
                [
                    "",
                    item["name"],
                    "-" * len(item["name"]),
                    f"Sequence: {item['sequence']}",
                    f"Layer path: {', '.join(item['layer_path']) if item['layer_path'] else 'Unmapped'}",
                    f"Layer support: {item['support']:,}",
                    f"Interpretation: {item['interpretation']}",
                    "Review rule: Treat this as a hypothesis until source-backed evidence is added.",
                ]
            )

    return "\n".join(lines)


def describe_theme_balance(theme_counts):
    """Create a plain-English interpretation of the strongest themes."""
    if not theme_counts:
        return "No themes were detected yet."

    strongest = [theme for theme, count in theme_counts.most_common(3) if count > 0]

    if not strongest:
        return "The documents do not yet contain enough theme language to detect a pattern."

    return (
        "The strongest signal is currently around "
        + ", ".join(strongest)
        + ". This suggests the research set is beginning to connect conceptual, human, and analytical dimensions."
    )


def build_research_questions(theme_counts):
    """Generate research questions from detected themes."""
    questions = [
        "Where do theological claims about order and intelligibility overlap with scientific descriptions of pattern?",
        "Which worship behaviors appear across cultures, and what meanings do those communities attach to them?",
        "What biological or neurological claims are well supported, and which claims should remain speculative?",
        "Can AI help organize patterns without overstating what the evidence proves?",
        "What safeguards are needed so the project studies faith respectfully instead of reducing it to data?",
    ]

    if theme_counts["Biology and Neuroscience"] > 0 and theme_counts["Spirituality and Worship"] > 0:
        questions.append(
            "How do embodied practices such as prayer, music, posture, and ritual relate to spiritual experience?"
        )

    if theme_counts["Theology and Logos"] > 0 and theme_counts["AI and Pattern Recognition"] > 0:
        questions.append(
            "Can pattern-recognition tools help compare ideas of Logos, order, and intelligibility across texts?"
        )

    return questions


def create_report(analyses):
    """Create the divine pattern research report."""
    theme_counts = combine_theme_counts(analyses)
    trinity_counts = combine_trinity_counts(analyses)
    trinity_evidence = combine_trinity_evidence(analyses)
    trinitarian_co_presence = combine_trinitarian_co_presence(analyses)
    domain_counts = combine_domain_counts(analyses)
    layer_counts = combine_layer_counts(analyses)
    layer_evidence = combine_layer_evidence(analyses)
    meaning_context_counts = combine_meaning_context_counts(analyses)
    source_quality_counts = combine_source_quality_counts(analyses)
    repeated_terms = combine_terms(analyses)
    cross_theme_patterns = [
        pattern
        for analysis in analyses
        for pattern in analysis["cross_theme_patterns"]
    ]

    lines = [
        "Divine Pattern Research Report",
        "==============================",
        "",
        "Purpose",
        "-------",
        "This report uses Python as an analytical tool to look for recurring language and cross-disciplinary patterns across theology, spirituality, biology, anthropology, philosophy, and AI.",
        "It does not attempt to prove divine truth. It helps organize evidence, surface connections, and generate better research questions.",
        "Guardrail: word matches are only starting signals. A stronger pattern needs context, movement across a text, and practical meaning.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Overview",
        "--------",
        f"Documents analyzed: {len(analyses):,}",
        f"Total analyzed words: {sum(analysis['words'] for analysis in analyses):,}",
        describe_theme_balance(theme_counts),
        "",
        "Theme Signals",
        "-------------",
    ]

    for theme, count in theme_counts.most_common():
        lines.append(f"- {theme}: {count:,}")

    lines.extend(
        [
            "",
            "Trinitarian Pattern Lens",
            "------------------------",
            f"Signal: {score_trinitarian_pattern(trinity_counts)}",
            "The analyzer treats Father, Son, and Holy Spirit as distinct persons and one God. It looks for each person separately, then checks whether the corpus keeps them relationally connected.",
        ]
    )

    for person in TRINITY_PERSONS:
        count = trinity_counts.get(person, 0)
        lines.append(f"- {person}: {count:,}")
        lines.append(f"  Role: {TRINITY_PERSONS[person]['role']}")

    lines.extend(["", "Trinitarian Evidence Samples", "----------------------------"])
    for person in TRINITY_PERSONS:
        lines.append("")
        lines.append(person)
        lines.append("-" * len(person))
        snippets = trinity_evidence.get(person, [])
        if not snippets:
            lines.append("- No evidence snippets found yet.")
            continue
        for file_name, snippet in snippets[:3]:
            lines.append(f"- {file_name}: {snippet}")

    lines.extend(["", "Trinitarian Co-Presence Samples", "-------------------------------"])
    if trinitarian_co_presence:
        for item in trinitarian_co_presence[:8]:
            lines.append(
                f"- {item['file_name']} ({', '.join(item['persons'])}): {item['sentence']}"
            )
    else:
        lines.append("- No sentence-level co-presence found yet.")

    lines.extend(["", "Meaning Guardrails", "------------------"])
    lines.append(
        "The analyzer now checks whether a pattern has contextual movement, not only repeated vocabulary."
    )
    for context, count in meaning_context_counts.most_common():
        if count > 0:
            lines.append(f"- {context}: {count:,}")

    lines.extend(["", "Source Review Guardrails", "------------------------"])
    reviewed_cloud = source_quality_counts.get("Reviewed Cloud Reference", 0)
    unreviewed_cloud = source_quality_counts.get("Unreviewed Cloud Reference", 0)
    if source_quality_counts:
        for marker, count in source_quality_counts.most_common():
            if count > 0:
                lines.append(f"- {marker}: {count:,}")
    if unreviewed_cloud > reviewed_cloud:
        lines.append(
            "- Cloud references are candidate leads until reviewed against the original source, author qualifications, publication context, and counterarguments."
        )
    else:
        lines.append("- No unreviewed cloud-reference imbalance detected.")

    lines.extend(
        [
            "",
            "Divine Pattern Finder",
            "---------------------",
            "Model: Physical Order -> Mathematical Structure -> Mathematical Theophany -> Quantum Probability -> Life And Consciousness -> Meaning And Logos -> Moral Response -> Worship And Community -> Transformation",
            create_divine_pattern_summary(layer_counts),
            "",
            "Layer Scores:",
        ]
    )

    for layer in DIVINE_PATTERN_LAYERS:
        count = layer_counts.get(layer, 0)
        lines.append(f"- {layer}: {count:,} ({score_layer(count)})")
        lines.append(f"  Test: {DIVINE_PATTERN_LAYERS[layer]['question']}")

    lines.extend(["", "Layer Evidence Samples", "----------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        lines.append("")
        lines.append(layer)
        lines.append("-" * len(layer))
        snippets = layer_evidence.get(layer, [])
        if not snippets:
            lines.append("- No evidence snippets found yet.")
            continue

        for file_name, snippet in snippets[:3]:
            lines.append(f"- {file_name}: {snippet}")

    lines.extend(["", "Hypothesis Test Domains", "-----------------------"])
    for domain, count in domain_counts.most_common():
        status = "needs more sources"
        if count >= 500:
            status = "strongly represented"
        elif count >= 100:
            status = "represented"
        elif count >= 25:
            status = "lightly represented"

        lines.append(f"- {domain}: {count:,} ({status})")

    lines.extend(["", "Repeated Terms", "--------------"])
    for term, count in repeated_terms.most_common(20):
        lines.append(f"- {term}: {count:,}")

    lines.extend(["", "Cross-Disciplinary Pattern Candidates", "-------------------------------------"])
    if cross_theme_patterns:
        for pattern in cross_theme_patterns[:15]:
            lines.append(f"- Themes: {', '.join(pattern['themes'])}")
            lines.append(f"  Evidence: {pattern['sentence']}")
    else:
        lines.append("- No cross-theme sentences found yet. Add more research notes or source text.")

    lines.extend(["", "Evidence By Theme", "-----------------"])
    for theme in THEMES:
        lines.append("")
        lines.append(theme)
        lines.append("-" * len(theme))

        found_any = False
        for analysis in analyses:
            snippets = analysis["evidence"].get(theme, [])
            for snippet in snippets[:2]:
                found_any = True
                lines.append(f"- {analysis['file_name']}: {snippet}")

        if not found_any:
            lines.append("- No evidence snippets found yet.")

    lines.extend(["", "Research Questions", "------------------"])
    for index, question in enumerate(build_research_questions(theme_counts), start=1):
        lines.append(f"{index}. {question}")

    lines.extend(
        [
            "",
            "Practical Theology Uses",
            "-----------------------",
        ]
    )
    for index, use in enumerate(create_practical_theology_plan(meaning_context_counts), start=1):
        lines.append(f"{index}. {use}")

    lines.extend(
        [
            "",
            "Recommended Next Steps",
            "----------------------",
            "1. Add theological texts, research notes, article excerpts, and anthropology notes to research_documents.",
            "2. Keep source labels clear so future reports can separate scripture, theology, science, philosophy, and personal notes.",
            "3. Add PDF and Word document support after the text version feels understandable.",
            "4. Later, connect an AI model to summarize, critique, and compare the evidence more deeply.",
            "5. Treat any proposed pattern as a research hypothesis until it is checked against credible sources.",
            "6. Use the Divine Pattern Finder to look for layered convergence, while keeping each layer open to critique.",
        ]
    )

    return "\n".join(lines)


def create_music_patterns_report(research_analyses, music_analyses):
    """Create a report comparing lyrics with biblical and religious patterns."""
    research_theme_counts = combine_theme_counts(research_analyses)
    research_layer_counts = combine_layer_counts(research_analyses)
    lyric_theme_counts = combine_theme_counts(music_analyses)
    lyric_layer_counts = combine_layer_counts(music_analyses)
    lyric_alignment_counts = combine_alignment_counts(music_analyses)
    general_music_counts = combine_general_music_counts(music_analyses)
    music_meaning_counts = combine_meaning_context_counts(music_analyses)
    music_trinity_counts = combine_trinity_counts(music_analyses)

    lines = [
        "Music And Lyric Pattern Alignment Report",
        "========================================",
        "",
        "Purpose",
        "-------",
        "This report looks for patterns across any kind of music or lyrics, then compares those patterns with biblical and other religious themes already used by the research analyzer.",
        "It detects broad human motifs, religious motifs, repeated refrains, question/response movement, and possible spiritual arcs. These are interpretive signals, not proof of author intent.",
        "Guardrail: the report separates broad human meaning from religious vocabulary so secular music is not forced into a religious reading.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Overview",
        "--------",
        f"Lyric documents analyzed: {len(music_analyses):,}",
        f"Total lyric words analyzed: {sum(analysis['words'] for analysis in music_analyses):,}",
        f"Religious research documents used for comparison: {len(research_analyses):,}",
        "",
        "Strongest Lyric Motifs",
        "---------------------",
    ]

    lines.extend(["Broad music motifs:"])
    if general_music_counts:
        for pattern, count in general_music_counts.most_common():
            if count > 0:
                lines.append(f"- {pattern}: {count:,}")
    else:
        lines.append("- No broad music motif signals found yet.")

    lines.extend(["", "Religious motif echoes:"])

    if lyric_alignment_counts:
        for pattern, count in lyric_alignment_counts.most_common():
            if count > 0:
                lines.append(f"- {pattern}: {count:,}")
    else:
        lines.append("- No lyric motif signals found yet.")

    lines.extend(["", "Trinitarian Lens", "----------------"])
    lines.append(f"Signal: {score_trinitarian_pattern(music_trinity_counts)}")
    for person in TRINITY_PERSONS:
        lines.append(f"- {person}: {music_trinity_counts.get(person, 0):,}")

    lines.extend(["", "Meaning Guardrails", "------------------"])
    if music_meaning_counts:
        for context, count in music_meaning_counts.most_common():
            if count > 0:
                lines.append(f"- {context}: {count:,}")
    else:
        lines.append("- No meaning contexts detected yet.")

    lines.extend(["", "Shared Divine-Pattern Layers", "----------------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        lyric_count = lyric_layer_counts.get(layer, 0)
        research_count = research_layer_counts.get(layer, 0)
        if lyric_count or research_count:
            lines.append(
                f"- {layer}: lyrics {lyric_count:,} | religious corpus {research_count:,}"
            )

    lines.extend(["", "Shared Theme Signals", "--------------------"])
    for theme in THEMES:
        lyric_count = lyric_theme_counts.get(theme, 0)
        research_count = research_theme_counts.get(theme, 0)
        if lyric_count or research_count:
            lines.append(
                f"- {theme}: lyrics {lyric_count:,} | religious corpus {research_count:,}"
            )

    ranked_songs = sorted(
        music_analyses,
        key=lambda analysis: analysis["alignment_score"],
        reverse=True,
    )

    lines.extend(["", "Most Aligned Lyric Files", "------------------------"])
    if not ranked_songs:
        lines.append("- No lyric files found yet. Add .txt or .md lyric files to music_lyrics.")
    else:
        for analysis in ranked_songs[:10]:
            lines.append(
                f"- {analysis['file_name']}: score {analysis['alignment_score']:,}; "
                f"strongest broad motif {analysis['strongest_general'][0]} ({analysis['strongest_general'][1]:,}); "
                f"strongest motif {analysis['strongest_alignment'][0]} ({analysis['strongest_alignment'][1]:,}); "
                f"strongest layer {analysis['strongest_layer'][0]} ({analysis['strongest_layer'][1]:,})"
            )

    lines.extend(["", "Per-Lyric Findings", "------------------"])
    if not music_analyses:
        lines.append("- No lyric files found yet.")

    for analysis in ranked_songs:
        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Lines: {analysis['lines']:,}",
                f"Words: {analysis['words']:,}",
                f"Alignment score: {analysis['alignment_score']:,}",
                f"Strongest theme: {analysis['strongest_theme'][0]} ({analysis['strongest_theme'][1]:,})",
                f"Strongest divine-pattern layer: {analysis['strongest_layer'][0]} ({analysis['strongest_layer'][1]:,})",
                f"Strongest broad music motif: {analysis['strongest_general'][0]} ({analysis['strongest_general'][1]:,})",
                f"Strongest lyric motif: {analysis['strongest_alignment'][0]} ({analysis['strongest_alignment'][1]:,})",
                f"Meaning confidence: {analysis['meaning_confidence']}",
                "Repeated refrain candidates:",
            ]
        )

        if analysis["refrain_candidates"]:
            for refrain in analysis["refrain_candidates"][:5]:
                lines.append(f"- {refrain['line']} ({refrain['count']}x)")
        else:
            lines.append("- No repeated refrain lines detected.")

        lines.append("Question/response candidates:")
        if analysis["question_response_pairs"]:
            for pair in analysis["question_response_pairs"][:3]:
                lines.append(f"- Q: {pair['question']}")
                lines.append(f"  R: {pair['response']}")
        else:
            lines.append("- No adjacent question/response pairs detected.")

        lines.append("Lyric arc:")
        for segment in analysis["lyric_arc"]:
            lines.append(
                f"- {segment['segment']}: layer {segment['layer']} ({segment['layer_count']:,}); "
                f"broad motif {segment['general_pattern']} ({segment['general_pattern_count']:,}); "
                f"motif {segment['pattern']} ({segment['pattern_count']:,})"
            )

        lines.append("Meaning arc:")
        for segment in analysis["meaning_arc"]:
            lines.append(
                f"- {segment['segment']}: {segment['context']} ({segment['count']:,})"
            )

        lines.append("Broad music motif evidence samples:")
        found_general_evidence = False
        for pattern, snippets in analysis["general_evidence"].items():
            for snippet in snippets[:2]:
                found_general_evidence = True
                lines.append(f"- {pattern}: {snippet}")

        if not found_general_evidence:
            lines.append("- No broad music motif evidence snippets found yet.")

        lines.append("Religious motif evidence samples:")
        found_evidence = False
        for pattern, snippets in analysis["alignment_evidence"].items():
            for snippet in snippets[:2]:
                found_evidence = True
                lines.append(f"- {pattern}: {snippet}")

        if not found_evidence:
            lines.append("- No motif evidence snippets found yet.")

        lines.append("Practical theology applications:")
        for item in analysis["practical_theology_plan"][:4]:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "Recommended Next Steps",
            "----------------------",
            "1. Add lyric files, song notes, or public-domain lyrics to music_lyrics as .txt or .md files.",
            "2. Keep song title, artist, genre, album, and source notes at the top of each file when possible.",
            "3. Compare sacred, secular, and mixed music separately if you want cleaner results.",
            "4. Treat phrase matches as prompts for interpretation, then check the full song context before drawing conclusions.",
            "5. Do not paste large copyrighted lyric collections unless you have the right to analyze them locally.",
        ]
    )

    return "\n".join(lines)


def create_music_note_patterns_report(research_analyses, note_analyses):
    """Create a report comparing musical notes with science and math patterns."""
    research_layer_counts = combine_layer_counts(research_analyses)
    research_domain_counts = combine_domain_counts(research_analyses)
    combined_interval_counts = Counter()
    combined_layer_counts = Counter()
    combined_relationships = Counter()
    note_meaning_counts = combine_meaning_context_counts(note_analyses)
    note_trinity_counts = combine_trinity_counts(note_analyses)

    for analysis in note_analyses:
        combined_interval_counts.update(analysis["interval_counts"])
        combined_layer_counts.update(analysis["layer_counts"])
        combined_relationships.update(analysis["science_math_relationships"])

    total_consonance = sum(analysis["consonance_count"] for analysis in note_analyses)
    total_tension = sum(analysis["tension_count"] for analysis in note_analyses)
    total_intervals = sum(combined_interval_counts.values())
    consonance_ratio = total_consonance / total_intervals if total_intervals else 0
    tension_ratio = total_tension / total_intervals if total_intervals else 0

    lines = [
        "Music Note Science And Math Pattern Report",
        "==========================================",
        "",
        "Purpose",
        "-------",
        "This report analyzes actual note and chord patterns, then compares their mathematical structure with the science, math, and divine-pattern layers in the research corpus.",
        "It treats musical order as a relationship between number, physical sound, pattern, tension, resolution, and meaning. These are research signals, not theological proof.",
        "Guardrail: note math is analyzed directly, while theological meaning is only suggested when the surrounding composition notes support it.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Overview",
        "--------",
        f"Music-note files analyzed: {len(note_analyses):,}",
        f"Note/chord events analyzed: {sum(analysis['events'] for analysis in note_analyses):,}",
        f"Individual notes analyzed: {sum(analysis['notes'] for analysis in note_analyses):,}",
        f"Intervals analyzed: {total_intervals:,}",
        f"Consonance ratio: {consonance_ratio:.2%}",
        f"Tension ratio: {tension_ratio:.2%}",
        "",
        "Interval Patterns",
        "-----------------",
    ]

    if combined_interval_counts:
        for interval, count in combined_interval_counts.most_common():
            name = INTERVAL_NAMES.get(interval, f"{interval} semitones")
            ratio = INTERVAL_RATIOS.get(interval, "n/a")
            lines.append(f"- {name}: {count:,} | simple ratio: {ratio}")
    else:
        lines.append("- No note intervals found yet. Add note files to music_notes.")

    lines.extend(["", "Science And Math Relationships", "------------------------------"])
    if combined_relationships:
        for relationship, count in combined_relationships.most_common():
            lines.append(f"- {relationship}: {count:,}")
    else:
        lines.append("- No science/math music relationships found yet.")

    lines.extend(["", "Trinitarian Lens", "----------------"])
    lines.append(f"Signal: {score_trinitarian_pattern(note_trinity_counts)}")
    for person in TRINITY_PERSONS:
        lines.append(f"- {person}: {note_trinity_counts.get(person, 0):,}")

    lines.extend(["", "Meaning Guardrails", "------------------"])
    if note_meaning_counts:
        for context, count in note_meaning_counts.most_common():
            if count > 0:
                lines.append(f"- {context}: {count:,}")
    else:
        lines.append("- No meaning contexts detected in note descriptions yet.")

    lines.extend(["", "Shared Divine-Pattern Layers", "----------------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        note_count = combined_layer_counts.get(layer, 0)
        research_count = research_layer_counts.get(layer, 0)
        if note_count or research_count:
            lines.append(
                f"- {layer}: music notes {note_count:,} | religious/science corpus {research_count:,}"
            )

    lines.extend(["", "Relevant Research Domains", "-------------------------"])
    for domain in [
        "Philosophy Of Mathematics",
        "Physics And Quantum Mechanics",
        "Philosophy Of Science",
        "Cognitive Science",
        "Anthropology And Psychology Of Worship",
    ]:
        lines.append(f"- {domain}: corpus signal {research_domain_counts.get(domain, 0):,}")

    ranked = sorted(
        note_analyses,
        key=lambda analysis: sum(analysis["layer_counts"].values()),
        reverse=True,
    )

    lines.extend(["", "Per-Composition Findings", "------------------------"])
    if not ranked:
        lines.append("- No music-note files found yet.")

    for analysis in ranked:
        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Events: {analysis['events']:,}",
                f"Notes: {analysis['notes']:,}",
                f"Chord events: {analysis['chords']:,}",
                f"Melodic intervals: {analysis['melodic_intervals']:,}",
                f"Harmonic intervals: {analysis['harmonic_intervals']:,}",
                f"Consonant intervals: {analysis['consonance_count']:,}",
                f"Tension intervals: {analysis['tension_count']:,}",
                f"Return motifs: {analysis['return_motifs']:,}",
                f"Meaning confidence: {analysis['meaning_confidence']}",
                "Most common intervals:",
            ]
        )

        interval_counts = Counter(analysis["interval_counts"])
        if interval_counts:
            for interval, count in interval_counts.most_common(5):
                lines.append(
                    f"- {INTERVAL_NAMES.get(interval, str(interval))}: {count:,} | ratio {INTERVAL_RATIOS.get(interval, 'n/a')}"
                )
        else:
            lines.append("- No intervals detected.")

        lines.append("Layer interpretation:")
        for layer, count in Counter(analysis["layer_counts"]).most_common():
            if count > 0:
                lines.append(f"- {layer}: {count:,}")

        lines.append("Meaning arc:")
        for segment in analysis["meaning_arc"]:
            lines.append(
                f"- {segment['segment']}: {segment['context']} ({segment['count']:,})"
            )

        lines.append("Practical theology applications:")
        for item in analysis["practical_theology_plan"][:4]:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "Candidate Relationship Pattern",
            "------------------------------",
            "Music notes show a measurable path from physical vibration to mathematical interval, from interval to perceived tension or stability, and from repeated pattern to meaning.",
            "A cautious divine-pattern comparison is: Physical Sound -> Mathematical Ratio -> Ordered Pattern -> Tension And Resolution -> Meaning -> Communal Response.",
            "",
            "Modern-Life Application",
            "-----------------------",
            "Use the pattern as a practical theology lens: listen for where life has order, where tension appears, what kind of resolution is sought, and what practices help people move toward healing, justice, community, and hope.",
        ]
    )

    return "\n".join(lines)


def create_cultural_patterns_report(research_analyses, cultural_analyses):
    """Create a report for art, politics, science, and modern-life domains."""
    research_layer_counts = combine_layer_counts(research_analyses)
    cultural_domain_counts = combine_cultural_domain_counts(cultural_analyses)
    meaning_context_counts = combine_meaning_context_counts(cultural_analyses)
    cultural_layer_counts = combine_layer_counts(cultural_analyses)
    cultural_trinity_counts = combine_trinity_counts(cultural_analyses)

    lines = [
        "Cultural Pattern Relationships Report",
        "=====================================",
        "",
        "Purpose",
        "-------",
        "This report broadens the project beyond music. It compares art, politics, science, technology, economics, family, health, ecology, and education with the same meaning guardrails used for theology and music.",
        "Guardrail: cultural patterns are treated as practical-theology questions, not automatic proof claims.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Overview",
        "--------",
        f"Cultural documents analyzed: {len(cultural_analyses):,}",
        f"Total cultural words analyzed: {sum(analysis['words'] for analysis in cultural_analyses):,}",
        "",
        "Cultural Domains",
        "----------------",
    ]

    if cultural_domain_counts:
        for domain, count in cultural_domain_counts.most_common():
            if count > 0:
                lines.append(f"- {domain}: {count:,}")
    else:
        lines.append("- No cultural domain signals found yet.")

    lines.extend(["", "Trinitarian Lens", "----------------"])
    lines.append(f"Signal: {score_trinitarian_pattern(cultural_trinity_counts)}")
    for person in TRINITY_PERSONS:
        lines.append(f"- {person}: {cultural_trinity_counts.get(person, 0):,}")

    lines.extend(["", "Meaning Guardrails", "------------------"])
    if meaning_context_counts:
        for context, count in meaning_context_counts.most_common():
            if count > 0:
                lines.append(f"- {context}: {count:,}")
    else:
        lines.append("- No meaning contexts found yet.")

    lines.extend(["", "Shared Divine-Pattern Layers", "----------------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        cultural_count = cultural_layer_counts.get(layer, 0)
        research_count = research_layer_counts.get(layer, 0)
        if cultural_count or research_count:
            lines.append(
                f"- {layer}: cultural inputs {cultural_count:,} | religious/science corpus {research_count:,}"
            )

    ranked = sorted(
        cultural_analyses,
        key=lambda analysis: sum(analysis["layer_counts"].values()),
        reverse=True,
    )

    lines.extend(["", "Per-Domain Findings", "-------------------"])
    if not ranked:
        lines.append("- No cultural files found yet. Add .txt or .md files to cultural_inputs.")

    for analysis in ranked:
        domain_counts = Counter(analysis["cultural_domain_counts"])
        strongest_domain = domain_counts.most_common(1)[0] if domain_counts else ("None", 0)

        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Words: {analysis['words']:,}",
                f"Strongest cultural domain: {strongest_domain[0]} ({strongest_domain[1]:,})",
                f"Meaning confidence: {analysis['meaning_confidence']}",
                "Meaning arc:",
            ]
        )

        for segment in analysis["meaning_arc"]:
            lines.append(
                f"- {segment['segment']}: {segment['context']} ({segment['count']:,})"
            )

        lines.append("Layer interpretation:")
        for layer, count in Counter(analysis["layer_counts"]).most_common():
            if count > 0:
                lines.append(f"- {layer}: {count:,}")

        lines.append("Practical theology applications:")
        for item in analysis["practical_theology_plan"][:3]:
            lines.append(f"- {item}")

        lines.append("Practical domain applications:")
        for item in analysis["practical_domain_plan"][:3]:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "Integrated Divine Pattern",
            "-------------------------",
            "The broader pattern is not only song. Human life turns order into meaning through many forms: art gives image to longing, politics tests justice, science studies order, technology tests responsibility, economics tests dignity, health exposes suffering, ecology reveals stewardship, and community practices transformation.",
            "",
            "Candidate sequence:",
            "Physical Order -> Perception -> Symbol/Model -> Tension Or Injustice -> Moral Discernment -> Communal Practice -> Healing And Transformation",
        ]
    )

    return "\n".join(lines)


def create_cross_layer_reasoning_report(
    research_analyses,
    music_analyses,
    note_analyses,
    cultural_analyses,
    test_analyses,
    deep_source_analyses,
    theologian_analyses,
    synthesis_analyses,
):
    """Create a synthesis report that reasons across domains and interpretive lenses."""
    all_analyses = (
        research_analyses
        + music_analyses
        + note_analyses
        + cultural_analyses
        + test_analyses
        + deep_source_analyses
        + theologian_analyses
        + synthesis_analyses
    )
    all_layer_counts = combine_layer_counts(all_analyses)
    all_meaning_counts = combine_meaning_context_counts(all_analyses)
    synthesis_lens_counts = combine_synthesis_lens_counts(synthesis_analyses)
    synthesis_domain_counts = combine_cultural_domain_counts(synthesis_analyses)
    language_family_counts = combine_language_family_counts(synthesis_analyses)
    text_tradition_counts = combine_text_tradition_counts(synthesis_analyses)
    global_coverage_status = score_global_coverage(
        language_family_counts,
        text_tradition_counts,
    )
    depth_counts = Counter(
        analysis.get("synthesis_depth", "not scored") for analysis in synthesis_analyses
    )
    comparative_lanes = {
        "All Texts",
        "Other Religious Texts",
        "Modern Literature",
        "Human Stories",
    }
    comparative_analyses = [
        analysis
        for analysis in synthesis_analyses
        if analysis.get("source_lane") in comparative_lanes
    ]
    comparative_validity_counts = Counter(
        analysis.get("comparative_validity", "not assessed")
        for analysis in comparative_analyses
    )
    comparative_trinity_counts = combine_trinity_counts(comparative_analyses)
    lane_groups = defaultdict(list)

    for analysis in synthesis_analyses:
        lane_groups[analysis["source_lane"]].append(analysis)

    layer_breadth = sum(1 for count in all_layer_counts.values() if count > 0)
    meaning_breadth = sum(1 for count in all_meaning_counts.values() if count > 0)
    lens_breadth = sum(1 for count in synthesis_lens_counts.values() if count > 0)

    if layer_breadth >= 7 and meaning_breadth >= 5 and lens_breadth >= 5:
        synthesis_status = "broad cross-layer synthesis"
    elif layer_breadth >= 5 and meaning_breadth >= 4 and lens_breadth >= 3:
        synthesis_status = "developing multi-domain understanding"
    elif layer_breadth >= 3 and meaning_breadth >= 2:
        synthesis_status = "early cross-domain pattern"
    else:
        synthesis_status = "needs more non-religious and context-rich sources"

    lines = [
        "Cross-Layer Reasoning Report",
        "============================",
        "",
        "Purpose",
        "-------",
        "This report is the deeper synthesis layer. It asks whether the app is seeing context, movement, symbol, language, history, psychology, ethics, and theology together, instead of only matching religious words.",
        "It can use religious and non-religious texts, visual-art notes, historical material, world-language observations, biblical Greek/Hebrew notes, psychology, and other human-behavior sources.",
        "Guardrail: synthesis is a disciplined interpretation, not proof. A pattern gets stronger when multiple lenses converge and when counter-readings are preserved.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Current Synthesis Status",
        "------------------------",
        f"Status: {synthesis_status}",
        f"Total documents across all lanes: {len(all_analyses):,}",
        f"Dedicated synthesis documents: {len(synthesis_analyses):,}",
        f"Active divine-pattern layers: {layer_breadth:,} of {len(DIVINE_PATTERN_LAYERS):,}",
        f"Active meaning contexts: {meaning_breadth:,} of {len(MEANING_CONTEXTS):,}",
        f"Active synthesis lenses: {lens_breadth:,} of {len(SYNTHESIS_LENSES):,}",
        f"Global language/text coverage: {global_coverage_status}",
        "Coverage note: these are coverage-map signals. A language family or tradition is not treated as deeply studied until actual source notes, translation notes, and counter-readings are added.",
        "",
        "Interpretive Lenses",
        "-------------------",
    ]

    if synthesis_lens_counts:
        for lens, count in synthesis_lens_counts.most_common():
            if count > 0:
                lines.append(f"- {lens}: {count:,}")
    else:
        lines.append("- No dedicated synthesis-lens sources found yet.")

    lines.extend(["", "Dedicated Synthesis Domains", "---------------------------"])
    if synthesis_domain_counts:
        for domain, count in synthesis_domain_counts.most_common():
            if count > 0:
                lines.append(f"- {domain}: {count:,}")
    else:
        lines.append("- Add files to visual_art, history_inputs, world_languages, biblical_languages, or psychology_inputs.")

    lines.extend(["", "Language Family Coverage", "------------------------"])
    if language_family_counts:
        for family in LANGUAGE_FAMILY_MARKERS:
            count = language_family_counts.get(family, 0)
            marker = "mapped" if count > 0 else "missing"
            lines.append(f"- {family}: {marker} ({count:,})")
    else:
        lines.append("- No language-family signals found yet.")

    lines.extend(["", "Text Tradition Coverage", "-----------------------"])
    if text_tradition_counts:
        for tradition in TEXT_TRADITION_MARKERS:
            count = text_tradition_counts.get(tradition, 0)
            marker = "mapped" if count > 0 else "missing"
            lines.append(f"- {tradition}: {marker} ({count:,})")
    else:
        lines.append("- No text-tradition signals found yet.")

    lines.extend(["", "Layer Convergence Across All Sources", "------------------------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        count = all_layer_counts.get(layer, 0)
        lines.append(f"- {layer}: {count:,} ({score_layer(count)})")

    lines.extend(["", "Meaning Movement Across All Sources", "-----------------------------------"])
    for context in MEANING_STAGE_ORDER:
        lines.append(f"- {context}: {all_meaning_counts.get(context, 0):,}")

    lines.extend(["", "Synthesis Depth Results", "-----------------------"])
    if depth_counts:
        for label, count in depth_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No dedicated synthesis files scored yet.")

    lines.extend(["", "Comparative Validity Check", "--------------------------"])
    lines.append(
        "Comparative recurrence can support a broad human pattern of order, meaning, moral response, community, and transformation; it does not by itself validate the specifically Christian Trinitarian interpretation."
    )
    if comparative_validity_counts:
        for label, count in comparative_validity_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No comparative text, literature, or human-story files assessed yet.")
    lines.append(
        f"- Comparative Trinitarian signal: {score_trinitarian_pattern(comparative_trinity_counts)}"
    )
    for person in TRINITY_PERSONS:
        lines.append(f"- {person}: {comparative_trinity_counts.get(person, 0):,}")

    lines.extend(["", "Reasoning Rules", "---------------"])
    lines.extend(
        [
            "1. Start with the surface words, but do not stop there.",
            "2. Ask what the form is doing: image, story, rhythm, history, grammar, body, habit, power, or relationship.",
            "3. Compare religious and non-religious sources without forcing them into the same answer.",
            "4. Use psychology to reveal human process, while keeping theology, ethics, and lived practice distinct.",
            "5. Use Greek and Hebrew to check semantic range and syntax before making a doctrinal claim from a translated word.",
            "6. Treat counter-readings as part of the synthesis, not as noise to remove.",
        ]
    )

    lines.extend(["", "Per-Lane Synthesis", "------------------"])
    if not synthesis_analyses:
        lines.append("- No dedicated synthesis files found yet.")

    for lane in SYNTHESIS_SOURCE_DIRS:
        lane_analyses = lane_groups.get(lane, [])
        lane_layers = combine_layer_counts(lane_analyses)
        lane_lenses = combine_synthesis_lens_counts(lane_analyses)
        lane_meaning = combine_meaning_context_counts(lane_analyses)

        lines.extend(["", lane, "-" * len(lane)])
        lines.append(f"Files: {len(lane_analyses):,}")
        strongest_lens = lane_lenses.most_common(1)[0] if lane_lenses else ("None", 0)
        strongest_layer = lane_layers.most_common(1)[0] if lane_layers else ("None", 0)
        strongest_meaning = lane_meaning.most_common(1)[0] if lane_meaning else ("None", 0)
        lines.append(f"Strongest lens: {strongest_lens[0]} ({strongest_lens[1]:,})")
        lines.append(f"Strongest layer: {strongest_layer[0]} ({strongest_layer[1]:,})")
        lines.append(f"Strongest meaning context: {strongest_meaning[0]} ({strongest_meaning[1]:,})")

        for analysis in lane_analyses:
            lines.extend(
                [
                    "",
                    analysis["file_name"],
                    "~" * len(analysis["file_name"]),
                    f"Words: {analysis['words']:,}",
                    f"Meaning confidence: {analysis['meaning_confidence']}",
                    f"Synthesis depth: {analysis['synthesis_depth']}",
                    f"Global coverage: {analysis['global_coverage']}",
                    "Synthesis questions:",
                ]
            )
            if analysis.get("source_lane") in comparative_lanes:
                lines.append(f"Comparative validity: {analysis['comparative_validity']}")
            for question in analysis["synthesis_questions"][:4]:
                lines.append(f"- {question}")

    lines.extend(
        [
            "",
            "Working Synthesis",
            "-----------------",
            "The app should interpret patterns as layered movement: form and context shape perception; perception becomes meaning; meaning exposes tension, beauty, desire, or harm; moral discernment asks what response is required; embodied practice tests whether transformation is real.",
            "",
            "Recommended Next Inputs",
            "-----------------------",
            "1. Add visual-art notes that describe actual composition, color, gesture, and symbol.",
            "2. Add history notes that include era, conflict, power, memory, and consequences.",
            "3. Add world-language and translation notes across many language families, scripts, oral traditions, and cultures.",
            "4. Add biblical Greek/Hebrew notes with lemma, syntax, translation range, and theological caution.",
            "5. Add sacred scripture, wisdom, epic, myth, philosophy, law, poetry, ritual, chronicle, oral tradition, and commentary sources to all_texts.",
            "6. Add other religious texts, modern literature summaries, and human stories with counter-readings before claiming validity.",
            "7. Add psychology or human-behavior notes about perception, attachment, trauma, habit, desire, identity, and repair.",
        ]
    )

    return "\n".join(lines)


def create_pattern_test_report(research_analyses, test_analyses):
    """Create a pressure-test report for the proposed divine pattern."""
    pressure_counts = Counter()
    source_quality_counts = Counter()
    meaning_context_counts = Counter()
    trinity_counts = Counter()
    layer_counts = Counter()

    for analysis in test_analyses:
        pressure_counts.update(analysis["pressure_counts"])
        source_quality_counts.update(analysis["source_quality_counts"])
        meaning_context_counts.update(analysis["meaning_context_counts"])
        trinity_counts.update(analysis["trinity_counts"])
        layer_counts.update(analysis["layer_counts"])

    research_trinity_counts = combine_trinity_counts(research_analyses)
    research_layer_counts = combine_layer_counts(research_analyses)
    confidence_counts = Counter(
        analysis["test_confidence"] for analysis in test_analyses
    )
    hold_counts = Counter(
        analysis["hold_assessment"] for analysis in test_analyses
    )

    lines = [
        "Divine Pattern Pressure-Test Report",
        "===================================",
        "",
        "Purpose",
        "-------",
        "This report tests the proposed divine pattern against counterexamples, unresolved suffering, injustice, non-Christian comparisons, science guardrails, and practical case studies.",
        "A pattern is stronger when it can face pressure without becoming vague, triumphalistic, or overclaimed.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Pattern Being Tested",
        "--------------------",
        "Father creates and sustains order; Son/Logos reveals meaning and redeems disorder; Holy Spirit makes redemption present through communion and transformation.",
        "",
        "Test Overview",
        "-------------",
        f"Test documents analyzed: {len(test_analyses):,}",
        f"Test words analyzed: {sum(analysis['words'] for analysis in test_analyses):,}",
        "",
        "Pressure Types",
        "--------------",
    ]

    if pressure_counts:
        for pressure_type, count in pressure_counts.most_common():
            if count > 0:
                lines.append(f"- {pressure_type}: {count:,}")
    else:
        lines.append("- No pressure-test material found yet.")

    lines.extend(["", "Source Quality Markers", "----------------------"])
    for marker, count in source_quality_counts.most_common():
        if count > 0:
            lines.append(f"- {marker}: {count:,}")

    if not any(source_quality_counts.values()):
        lines.append("- No source-quality markers found yet.")

    lines.extend(["", "Confidence Results", "------------------"])
    if confidence_counts:
        for label, count in confidence_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No tests scored yet.")

    lines.extend(["", "Hold Assessment", "---------------"])
    if hold_counts:
        for label, count in hold_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No hold assessments yet.")

    lines.extend(["", "Trinitarian Test Lens", "---------------------"])
    lines.append(f"Test-set signal: {score_trinitarian_pattern(trinity_counts)}")
    lines.append(f"Research-corpus signal: {score_trinitarian_pattern(research_trinity_counts)}")
    for person in TRINITY_PERSONS:
        lines.append(
            f"- {person}: test set {trinity_counts.get(person, 0):,} | research corpus {research_trinity_counts.get(person, 0):,}"
        )

    lines.extend(["", "Layer Pressure Comparison", "-------------------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        test_count = layer_counts.get(layer, 0)
        research_count = research_layer_counts.get(layer, 0)
        if test_count or research_count:
            lines.append(
                f"- {layer}: test set {test_count:,} | research corpus {research_count:,}"
            )

    lines.extend(["", "Meaning Contexts Under Pressure", "--------------------------------"])
    for context, count in meaning_context_counts.most_common():
        if count > 0:
            lines.append(f"- {context}: {count:,}")

    ranked = sorted(
        test_analyses,
        key=lambda analysis: sum(analysis["pressure_counts"].values()),
        reverse=True,
    )

    lines.extend(["", "Per-Test Findings", "-----------------"])
    if not ranked:
        lines.append("- No test files found yet. Add .txt or .md files to pattern_tests.")

    for analysis in ranked:
        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Words: {analysis['words']:,}",
                f"Meaning confidence: {analysis['meaning_confidence']}",
                f"Test confidence: {analysis['test_confidence']}",
                f"Hold assessment: {analysis['hold_assessment']}",
                "Pressure signals:",
            ]
        )

        for pressure_type, count in Counter(analysis["pressure_counts"]).most_common():
            if count > 0:
                lines.append(f"- {pressure_type}: {count:,}")

        lines.append("Meaning arc:")
        for segment in analysis["meaning_arc"]:
            lines.append(
                f"- {segment['segment']}: {segment['context']} ({segment['count']:,})"
            )

        lines.append("Recommendations:")
        for recommendation in analysis["recommendations"]:
            lines.append(f"- {recommendation}")

    lines.extend(
        [
            "",
            "Current Verdict",
            "---------------",
            "The divine pattern should be treated as a tested research hypothesis only where it survives hard cases: unresolved suffering, injustice, rival interpretations, and science guardrails.",
            "If the pattern only works in uplifting examples, it is too weak. If it can guide truthful lament, justice, humble science, and practical repair, it becomes more useful for daily life and practical theology.",
        ]
    )

    return "\n".join(lines)


def create_deep_source_review_report(deep_source_analyses):
    """Create a stricter review of unresolved suffering and quantum/science sources."""
    area_counts = Counter()
    source_type_counts = Counter()
    congruence_filter_counts = Counter()
    quality_counts = Counter()
    pressure_counts = Counter()

    for analysis in deep_source_analyses:
        area_counts.update(analysis["area_counts"])
        source_type_counts.update(analysis["source_type_counts"])
        congruence_filter_counts.update(analysis.get("congruence_filter_counts", {}))
        quality_counts.update(analysis["source_quality_counts"])
        pressure_counts.update(analysis["pressure_counts"])

    area_scores = {
        area: score_deep_source_area(area, source_type_counts, area_counts.get(area, 0))
        for area in DEEP_SOURCE_AREAS
    }

    lines = [
        "Deep Source Review Report",
        "=========================",
        "",
        "Purpose",
        "-------",
        "This report checks whether unresolved suffering and quantum/science claims have enough source support to be used responsibly in the divine-pattern project.",
        "It intentionally marks claims as under-sourced until the required kinds of evidence are present.",
        "",
        "Deep Source Areas",
        "-----------------",
    ]

    for area, details in DEEP_SOURCE_AREAS.items():
        lines.extend(
            [
                "",
                area,
                "-" * len(area),
                f"Status: {area_scores[area]}",
                f"Area signal: {area_counts.get(area, 0):,}",
                f"Guardrail: {details['guardrail']}",
                "Required source types:",
            ]
        )

        for source_type in details["required_source_types"]:
            count = source_type_counts.get(source_type, 0)
            marker = "present" if count > 0 else "missing"
            lines.append(f"- {source_type}: {marker} ({count:,})")

    lines.extend(["", "All Source-Type Signals", "-----------------------"])
    for source_type, count in source_type_counts.most_common():
        if count > 0:
            lines.append(f"- {source_type}: {count:,}")

    if not any(source_type_counts.values()):
        lines.append("- No deep source type signals found yet.")

    lines.extend(["", "Math / Statistics / Logic Congruence Filters", "------------------------------------------------"])
    for filter_name, details in CONGRUENCE_FILTERS.items():
        count = congruence_filter_counts.get(filter_name, 0)
        marker = "active" if count > 0 else "not detected"
        lines.extend(
            [
                f"- {filter_name}: {marker} ({count:,})",
                f"  Rule: {details['rule']}",
            ]
        )

    lines.extend(["", "Quality And Risk Markers", "------------------------"])
    for marker, count in quality_counts.most_common():
        if count > 0:
            lines.append(f"- {marker}: {count:,}")

    if not any(quality_counts.values()):
        lines.append("- No quality markers found yet.")

    lines.extend(["", "Per-Source Findings", "-------------------"])
    if not deep_source_analyses:
        lines.append("- No deep source files found yet. Add .txt or .md files to deep_sources.")

    for analysis in deep_source_analyses:
        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Words: {analysis['words']:,}",
                "Area scores:",
            ]
        )

        for area, score in analysis["area_scores"].items():
            count = analysis["area_counts"].get(area, 0)
            if count > 0:
                lines.append(f"- {area}: {score} ({count:,})")

        lines.append("Source types:")
        found_type = False
        for source_type, count in Counter(analysis["source_type_counts"]).most_common():
            if count > 0:
                found_type = True
                lines.append(f"- {source_type}: {count:,}")
        if not found_type:
            lines.append("- No required source types detected.")

        active_filters = [
            filter_name
            for filter_name, count in analysis.get("congruence_filter_counts", {}).items()
            if count > 0
        ]
        if active_filters:
            lines.append("Active congruence filters:")
            lines.extend(f"- {filter_name}" for filter_name in active_filters)

    lines.extend(
        [
            "",
            "Use Rules",
            "---------",
            "1. If an area is under-sourced, keep it as a research question, not a conclusion.",
            "2. Quantum/science claims need qualified science sources before they can support any theological comparison.",
            "3. Suffering claims need lament, pastoral care, lived cases, and counterarguments before they can guide practical theology.",
            "4. A source-supported status does not prove the divine pattern; it only means the claim has enough support to discuss responsibly.",
            "5. Math, statistics, logic, and physics filters can block overclaim even when a source sounds impressive.",
        ]
    )

    return "\n".join(lines)


def create_theologian_pattern_design_report(research_analyses, theologian_analyses):
    """Create a report using theologians across eras to improve pattern design."""
    era_counts = combine_theological_era_counts(theologian_analyses)
    concept_counts = combine_theological_concept_counts(theologian_analyses)
    theologian_trinity_counts = combine_trinity_counts(theologian_analyses)
    theologian_layer_counts = combine_layer_counts(theologian_analyses)
    research_layer_counts = combine_layer_counts(research_analyses)

    lines = [
        "Theologian Pattern Design Report",
        "================================",
        "",
        "Purpose",
        "-------",
        "This report uses theologians across eras to deepen pattern design. It looks for continuity, development, and disagreement instead of treating theology as one flat voice.",
        TRINITARIAN_GUARDRAIL,
        "",
        "Overview",
        "--------",
        f"Theologian documents analyzed: {len(theologian_analyses):,}",
        f"Total theologian words analyzed: {sum(analysis['words'] for analysis in theologian_analyses):,}",
        "",
        "Era Coverage",
        "------------",
    ]

    for era in THEOLOGICAL_ERAS:
        lines.append(f"- {era}: {era_counts.get(era, 0):,}")

    lines.extend(["", "Concept Coverage", "----------------"])
    for concept, count in concept_counts.most_common():
        if count > 0:
            lines.append(f"- {concept}: {count:,}")

    if not any(concept_counts.values()):
        lines.append("- No theologian concept signals found yet.")

    lines.extend(["", "Trinitarian Lens", "----------------"])
    lines.append(f"Signal: {score_trinitarian_pattern(theologian_trinity_counts)}")
    for person in TRINITY_PERSONS:
        lines.append(f"- {person}: {theologian_trinity_counts.get(person, 0):,}")

    lines.extend(["", "Layer Comparison", "----------------"])
    for layer in DIVINE_PATTERN_LAYERS:
        theologian_count = theologian_layer_counts.get(layer, 0)
        research_count = research_layer_counts.get(layer, 0)
        if theologian_count or research_count:
            lines.append(
                f"- {layer}: theologians {theologian_count:,} | broader corpus {research_count:,}"
            )

    lines.extend(["", "Per-Source Findings", "-------------------"])
    if not theologian_analyses:
        lines.append("- No theologian files found yet. Add .txt or .md files to theologians.")

    for analysis in theologian_analyses:
        strongest_concept = Counter(analysis["concept_counts"]).most_common(1)
        strongest_era = Counter(analysis["era_counts"]).most_common(1)
        concept_label = strongest_concept[0] if strongest_concept else ("None", 0)
        era_label = strongest_era[0] if strongest_era else ("None", 0)

        lines.extend(
            [
                "",
                analysis["file_name"],
                "-" * len(analysis["file_name"]),
                f"Words: {analysis['words']:,}",
                f"Strongest era signal: {era_label[0]} ({era_label[1]:,})",
                f"Strongest concept signal: {concept_label[0]} ({concept_label[1]:,})",
                f"Meaning confidence: {analysis['meaning_confidence']}",
                "Meaning arc:",
            ]
        )

        for segment in analysis["meaning_arc"]:
            lines.append(
                f"- {segment['segment']}: {segment['context']} ({segment['count']:,})"
            )

    lines.extend(
        [
            "",
            "Pattern Design Guidance",
            "-----------------------",
            "1. Prefer patterns that appear across multiple eras, not only one modern synthesis.",
            "2. Preserve real theological disagreements instead of averaging them away.",
            "3. Give strongest weight to patterns supported by Trinity, creation, Christology, Spirit, suffering, grace, church, and justice together.",
            "4. Use theologians to refine the pattern vocabulary, not to replace scripture, science, or lived testing.",
            "",
            "Candidate design rule:",
            "A stronger divine pattern should show continuity across eras, preserve Father/Son/Spirit distinction and unity, survive suffering and justice questions, and remain useful in practical life.",
        ]
    )

    return "\n".join(lines)


def read_daily_research_digest():
    """Read the latest cloud-collector digest if available."""
    if not DAILY_DIGEST_PATH.exists():
        return {
            "updated_at": "not available",
            "new_count": 0,
            "new_sources": [],
            "errors": [],
        }

    try:
        return json.loads(DAILY_DIGEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "updated_at": "invalid digest",
            "new_count": 0,
            "new_sources": [],
            "errors": ["daily_research_digest.json could not be parsed"],
        }


def read_reference_catalog_summary():
    """Read retained cloud-reference catalog counts for reader-facing reports."""
    if not REFERENCES_PATH.exists():
        return {
            "updated_at": "not available",
            "source_count": 0,
        }

    try:
        catalog = json.loads(REFERENCES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "updated_at": "invalid catalog",
            "source_count": 0,
        }

    return {
        "updated_at": catalog.get("updated_at", "not available"),
        "source_count": catalog.get("source_count", len(catalog.get("sources", []))),
    }


def describe_visible_pattern_families(ranked_patterns, limit=5):
    """Create evidence-sensitive reader language for the current top patterns."""
    names = [item["candidate"]["name"] for item in ranked_patterns[:limit]]
    if not names:
        return "The current corpus does not yet contain enough pattern evidence to name leading chapters."
    if len(names) == 1:
        pattern_text = names[0]
    else:
        pattern_text = ", ".join(names[:-1]) + f", and {names[-1]}"
    return f"The current corpus most visibly repeats pattern families led by {pattern_text}."


def format_counter_preview(values, limit=4):
    """Format the strongest movement counts for compact reader-facing snapshots."""
    counts = Counter(values or {})
    if not counts:
        return "none recorded"
    return ", ".join(f"{name}: {count:,}" for name, count in counts.most_common(limit))


def append_latest_run_snapshot(lines, digest, catalog_summary):
    """Put new run information at the front so every generated preview shows movement."""
    query_modifiers = digest.get("query_modifiers", [])
    modifier_text = ", ".join(query_modifiers[:5]) if query_modifiers else "not recorded"

    lines.extend(
        [
            "Latest Run Snapshot",
            "-------------------",
            f"Collector run: {digest.get('updated_at', 'not available')}",
            f"Retained cloud candidate references: {catalog_summary.get('source_count', 0):,}",
            f"Brand-new candidate references this run: {digest.get('new_count', 0):,}",
            f"Top new routed layers: {format_counter_preview(digest.get('new_layer_counts', {}))}",
            f"New evidence mix: {format_counter_preview(digest.get('new_automated_evidence_counts', {}))}",
            f"New provider mix: {format_counter_preview(digest.get('new_provider_counts', {}))}",
            f"Query modifiers used: {modifier_text}",
            "",
        ]
    )


def append_learning_journal_entry(lines, digest, ranked_patterns, pressure_counts):
    """Write a reflective, evidence-bounded journal entry from the report's current state."""
    tag_counts, layer_counts, quality_counts, developments = create_daily_pattern_developments(digest)
    new_sources = digest.get("new_sources", [])
    top_patterns = [item["candidate"]["name"] for item in ranked_patterns[:3]]
    leading_pattern = top_patterns[0] if top_patterns else "no settled leading pattern"
    supporting_patterns = ", ".join(top_patterns[1:]) if len(top_patterns) > 1 else "no clear secondary pattern yet"
    leading_layer = layer_counts.most_common(1)[0][0] if layer_counts else "no single new layer"
    leading_tag = tag_counts.most_common(1)[0][0] if tag_counts else "no dominant new tag"
    strongest_quality = quality_counts.most_common(1)[0][0] if quality_counts else "unknown source quality"
    pressure_name = pressure_counts.most_common(1)[0][0] if pressure_counts else "the standing pressure tests"

    lines.extend(
        [
            "Journal Entry: What I Am Learning",
            "---------------------------------",
            "I am reading this run as a conversation between what just arrived and what the project already thinks it sees.",
            f"The older pattern map still points first toward {leading_pattern}. Around it, I keep seeing related pressure from {supporting_patterns}.",
            f"The newest material is pulling my attention toward {leading_layer}, especially around {leading_tag}. That does not overturn the older map, but it changes what I should ask next.",
            f"My current thought is this: the new sources are less like final answers and more like fresh witnesses. Their strongest common quality is {strongest_quality}, so I should let them sharpen questions before I let them strengthen claims.",
            f"I also notice that {pressure_name} remains a live test. If the pattern cannot survive that friction, then it is probably only an attractive idea, not a disciplined theological insight.",
            "",
            "What this run makes me wonder:",
        ]
    )

    if developments:
        for development in developments[:4]:
            lines.append(f"- {development}")
    else:
        lines.append("- I do not yet see enough new movement to name a fresh question.")

    lines.extend(["", "What I should do with this learning:"])
    if new_sources:
        lines.append("- Compare the newest source leads against the existing top patterns before changing confidence language.")
        lines.append("- Look for counter-readings that explain the same signals without requiring a divine-pattern interpretation.")
        lines.append("- Promote only reviewed sources from question-shaping material into claim-strengthening evidence.")
    else:
        lines.append("- Treat this as a maintenance run and avoid writing as though new evidence arrived.")

    lines.extend(
        [
            "",
            "Journal guardrail: this is a generated research reflection. It records what the current evidence seems to be teaching the project, not a final judgment.",
            "",
        ]
    )


def append_daily_development_chapter(lines, digest):
    """Add reader-facing interpretation of the newest cloud material before stable chapters."""
    tag_counts, layer_counts, quality_counts, developments = create_daily_pattern_developments(digest)
    new_sources = digest.get("new_sources", [])

    lines.extend(
        [
            "Chapter Zero: New Information In This Run",
            "-----------------------------------------",
            "This chapter changes with the latest collector digest. It names what newly arrived or newly re-evaluated cloud material should make the reader watch more carefully.",
            "",
            "Fresh research movements:",
        ]
    )

    for development in developments[:8]:
        lines.append(f"- {development}")

    lines.extend(
        [
            "",
            f"Most active new tags: {format_counter_preview(tag_counts)}",
            f"Most active new layers: {format_counter_preview(layer_counts)}",
            f"Newest source-quality mix: {format_counter_preview(quality_counts)}",
            "",
            "Fresh source leads to review first:",
        ]
    )

    if new_sources:
        ranked_sources = sorted(
            new_sources,
            key=lambda source: (
                source.get("automated_evidence_score", 0),
                source.get("citation_count", 0) or 0,
                str(source.get("title", "")),
            ),
            reverse=True,
        )
        for source in ranked_sources[:6]:
            routes = ", ".join(source.get("layer_routes", [])) or "unrouted"
            lines.append(
                f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'}) | {source.get('provider', 'unknown provider')} | layers: {routes} | review use: {source.get('evaluation_use', 'candidate lead only')}"
            )
    else:
        lines.append("- No brand-new sources were added in the latest collector run.")

    lines.extend(
        [
            "",
            "Reader rule: this new material can change the questions immediately, but it should not strengthen a claim until the original source and counterarguments are reviewed.",
            "",
        ]
    )


def append_daily_reference_movement(lines, digest, catalog_summary):
    """Append the latest retained-reference movement to the reader book."""
    new_sources = digest.get("new_sources", [])
    new_layer_counts = Counter(digest.get("new_layer_counts", {}))
    new_evidence_counts = Counter(digest.get("new_automated_evidence_counts", {}))

    lines.extend(
        [
            "What Changed In The Latest Collection",
            "-------------------------------------",
            f"Daily collector updated: {digest.get('updated_at', 'not available')}",
            f"Retained cloud candidate references: {catalog_summary.get('source_count', 0):,}",
            f"Brand-new candidate references this run: {digest.get('new_count', 0):,}",
            "",
            "Newest evidence movement by routed layer:",
        ]
    )

    if new_layer_counts:
        for layer, count in new_layer_counts.most_common(8):
            lines.append(f"- {layer}: {count:,}")
    else:
        lines.append("- No routed layers grew in the latest collector run.")

    lines.extend(["", "Newest automated evidence mix:"])
    if new_evidence_counts:
        for label, count in new_evidence_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No new automated evidence scores available for the latest run.")

    lines.extend(["", "Newest sources shaping today's questions:"])
    if new_sources:
        for source in new_sources[:5]:
            routes = ", ".join(source.get("layer_routes", []))
            lines.append(
                f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'}) | layers: {routes} | evidence: {source.get('automated_evidence_label', 'not_scored')}"
            )
    else:
        lines.append("- No brand-new sources were added in the latest collector run.")

    lines.extend(
        [
            "",
            "Reader note: cloud candidates change the research questions immediately, but they should strengthen conclusions only after source review.",
            "",
        ]
    )


def create_daily_pattern_developments(digest):
    """Turn new daily sources into evolving candidate pattern language."""
    new_sources = digest.get("new_sources", [])
    layer_counts = Counter(digest.get("new_layer_counts", {}))
    evidence_counts = Counter(digest.get("new_automated_evidence_counts", {}))
    tag_counts = Counter(
        tag
        for source in new_sources
        for tag in source.get("tags", [])
    )
    quality_counts = Counter(source.get("quality", "unknown") for source in new_sources)
    text = " ".join(
        " ".join(
            [
                source.get("title", ""),
                " ".join(source.get("tags", [])),
                source.get("summary", ""),
            ]
        )
        for source in new_sources
    ).lower()

    developments = []
    if layer_counts.get("theologians", 0):
        developments.append("Theologian-source candidates grew in the latest collector run; review era, primary source, doctrine, disagreement, and pressure points.")
    if layer_counts.get("visual_art", 0):
        developments.append("Visual-art candidates grew in the latest collector run; examine actual form, composition, symbol, beauty, lament, and counter-reading.")
    if layer_counts.get("history_inputs", 0):
        developments.append("History candidates grew in the latest collector run; test power, harm, reform, memory, consequence, and unfinished repair.")
    if layer_counts.get("world_languages", 0):
        developments.append("World-language candidates grew in the latest collector run; track translation range, metaphor, grammar, culture, and rival readings.")
    if layer_counts.get("biblical_languages", 0):
        developments.append("Biblical-language candidates grew in the latest collector run; check lemma, syntax, canonical context, and scholarly counter-readings.")
    if layer_counts.get("all_texts", 0) or layer_counts.get("other_religious_texts", 0):
        developments.append("Global and comparative text candidates grew in the latest collector run; respect each tradition's own meaning before comparing patterns.")
    if layer_counts.get("psychology_inputs", 0) or layer_counts.get("human_stories", 0):
        developments.append("Psychology or human-story candidates grew in the latest collector run; separate lived repair from overclaimed theological interpretation.")
    if layer_counts.get("deep_sources", 0):
        developments.append("Deep-source candidates grew in the latest collector run; review qualified evidence and counterarguments before strengthening claims.")
    if layer_counts.get("pattern_tests", 0):
        developments.append("Pressure-test candidates grew in the latest collector run; name failure conditions and whether the pattern holds under friction.")

    if tag_counts.get("unresolved_suffering", 0) or any(term in text for term in ["lament", "grief", "trauma", "hope"]):
        developments.append("Lament-to-hope material grew in the latest collector run; test whether hope is patient and non-coercive rather than a quick resolution.")
    if tag_counts.get("biblical_languages", 0) or any(term in text for term in ["hebrew", "greek", "hesed", "logos", "translation"]):
        developments.append("Original-language and translation material grew in the latest collector run; check whether word-level claims survive syntax, genre, and semantic range.")
    if tag_counts.get("psychology_patterns", 0) or any(term in text for term in ["psychology", "attachment", "trauma", "forgiveness", "habit"]):
        developments.append("Psychology and formation material grew in the latest collector run; compare spiritual transformation with habit, attachment, memory, and repair without reducing faith to mechanism.")
    if tag_counts.get("history_memory", 0) or any(term in text for term in ["history", "memory", "empire", "justice", "reparative"]):
        developments.append("Historical-memory material grew in the latest collector run; test whether the pattern can face power, harm, repair, and communal memory.")
    if tag_counts.get("global_text_traditions", 0) or any(term in text for term in ["wisdom", "myth", "oral", "scripture", "ritual"]):
        developments.append("Global text-tradition material grew in the latest collector run; compare patterns across genre and culture before calling them universal.")
    if tag_counts.get("quantum_science_guardrails", 0) or any(term in text for term in ["quantum", "physics", "probability", "measurement"]):
        developments.append("Science-guardrail material grew in the latest collector run; keep any science analogy tied to qualified sources and stated limits.")
    if tag_counts.get("art_beauty", 0) or any(term in text for term in ["beauty", "art", "icon", "image", "aesthetic"]):
        developments.append("Art and beauty material grew in the latest collector run; ask what visual or aesthetic form reveals before translating it into doctrine.")

    if not developments and new_sources:
        developments.append("New candidate sources arrived today, but no dominant pattern family emerged yet. Review titles and summaries manually before increasing confidence.")
    if evidence_counts.get("strong_scholarly_candidate", 0):
        developments.append("High-quality scholarly leads arrived today; use them only for claim-scoped confidence after source review, not absolute proof.")
    if evidence_counts.get("do_not_strengthen_claim", 0):
        developments.append("Some candidates should not strengthen claims yet; keep them as questions or counter-readings.")
    if not new_sources:
        developments.append("No brand-new references were added in the latest collector run. The app re-evaluated the existing candidate set, but the summary should not claim new pattern growth today.")

    return tag_counts, layer_counts, quality_counts, developments


def create_divine_pattern_summary_report(
    research_analyses,
    music_analyses,
    note_analyses,
    cultural_analyses,
    test_analyses,
    deep_source_analyses,
    theologian_analyses,
    synthesis_analyses,
):
    """Create a concise summary of the current divine pattern found."""
    daily_digest = read_daily_research_digest()
    daily_tag_counts, daily_layer_counts, daily_quality_counts, daily_developments = create_daily_pattern_developments(
        daily_digest
    )
    daily_evidence_counts = Counter(daily_digest.get("new_automated_evidence_counts", {}))
    research_layer_counts = combine_layer_counts(research_analyses)
    music_meaning_counts = combine_meaning_context_counts(music_analyses)
    cultural_meaning_counts = combine_meaning_context_counts(cultural_analyses)
    synthesis_lens_counts = combine_synthesis_lens_counts(synthesis_analyses)
    language_family_counts = combine_language_family_counts(synthesis_analyses)
    text_tradition_counts = combine_text_tradition_counts(synthesis_analyses)
    source_quality_counts = combine_source_quality_counts(research_analyses)
    top_pattern_layer_counts = combine_layer_counts(
        research_analyses
        + synthesis_analyses
        + test_analyses
        + deep_source_analyses
    )
    top_pattern_rankings = rank_divine_pattern_candidates(top_pattern_layer_counts)
    synthesis_depth_counts = Counter(
        analysis.get("synthesis_depth", "not scored") for analysis in synthesis_analyses
    )
    comparative_lanes = {
        "All Texts",
        "Other Religious Texts",
        "Modern Literature",
        "Human Stories",
    }
    comparative_analyses = [
        analysis
        for analysis in synthesis_analyses
        if analysis.get("source_lane") in comparative_lanes
    ]
    comparative_validity_counts = Counter(
        analysis.get("comparative_validity", "not assessed")
        for analysis in comparative_analyses
    )
    trinity_counts = combine_trinity_counts(research_analyses)
    theologian_concepts = combine_theological_concept_counts(theologian_analyses)

    note_relationships = Counter()
    for analysis in note_analyses:
        note_relationships.update(analysis.get("science_math_relationships", {}))

    pressure_confidence = Counter(
        analysis.get("test_confidence", "not tested") for analysis in test_analyses
    )
    hold_assessments = Counter(
        analysis.get("hold_assessment", "not assessed") for analysis in test_analyses
    )
    pressure_counts = combine_pressure_counts(test_analyses)
    claim_ledger = parse_claim_ledger()
    reviewed_pack_names = load_reviewed_source_pack_names()
    lane_balance_records = create_lane_balance_records(
        research_analyses,
        cultural_analyses,
        test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )

    deep_area_scores = Counter()
    for analysis in deep_source_analyses:
        for area, score in analysis.get("area_scores", {}).items():
            if analysis.get("area_counts", {}).get(area, 0) > 0:
                deep_area_scores[f"{area}: {score}"] += 1

    lines = [
        "Divine Pattern Summary Report",
        "=============================",
        "",
    ]
    append_reader_preface(lines)
    append_how_to_read_this_book(lines)
    lines.extend(
        [
        "Chapter One: What Grew In The Latest Run?",
        "-----------------------------------------",
        "This chapter summarizes the newest retained research movement. The details matter, but the main question is simple: what new material helps the project understand God's pattern more carefully, and what still needs review?",
        "",
        "Latest Collector Development",
        "----------------------------",
        f"Daily collector updated: {daily_digest.get('updated_at', 'not available')}",
        f"Brand-new candidate references this run: {daily_digest.get('new_count', 0):,}",
        "New candidate pattern movements:",
        ]
    )

    for development in daily_developments:
        lines.append(f"- {development}")

    lines.extend(["", "New material by lane:"])
    if daily_tag_counts:
        for tag, count in daily_tag_counts.most_common():
            lines.append(f"- {tag}: {count:,}")
    else:
        lines.append("- No new lanes grew in the latest collector run.")

    lines.extend(["", "New material by routed layer:"])
    if daily_layer_counts:
        for layer, count in daily_layer_counts.most_common():
            lines.append(f"- {layer}: {count:,}")
    else:
        lines.append("- No routed layers grew in the latest collector run.")

    lines.extend(["", "New material quality mix:"])
    if daily_quality_counts:
        for quality, count in daily_quality_counts.most_common():
            lines.append(f"- {quality}: {count:,}")
    else:
        lines.append("- No new source-quality mix available for the latest run.")

    lines.extend(["", "New material automated evidence:"])
    if daily_evidence_counts:
        for label, count in daily_evidence_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No new automated evidence scores available for the latest run.")

    new_sources = daily_digest.get("new_sources", [])
    lines.extend(["", "Newest sources to review:"])
    if new_sources:
        for source in new_sources[:8]:
            tags = ", ".join(source.get("tags", []))
            routes = ", ".join(source.get("layer_routes", []))
            lines.append(
                f"- {source.get('title', 'Untitled')} ({source.get('year') or 'n.d.'}) | tags: {tags} | layers: {routes} | evidence: {source.get('automated_evidence_label', 'not_scored')} ({source.get('automated_evidence_score', 0)})"
            )
    else:
        lines.append("- No brand-new sources to review from the latest collector run.")

    if daily_digest.get("errors"):
        lines.extend(["", "Collector warnings:"])
        for error in daily_digest.get("errors", [])[:6]:
            lines.append(f"- {error}")

    append_everyday_pattern_story(lines)

    lines.extend(
        [
            "",
        "Chapter Two: The Most Visible Divine Pattern",
        "--------------------------------------------",
        "Father creates and sustains ordered reality.",
        "Son / Logos reveals meaning and redeems disorder.",
        "Holy Spirit makes redemption present through communion, healing, and transformation.",
        "",
        "Condensed sequence:",
        "",
        "Physical Order -> Perception -> Meaning -> Tension/Lament -> Moral Discernment -> Community Practice -> Spirit-Led Transformation",
        "",
        "Practical daily-life form:",
        "",
        "Notice -> Name -> Discern -> Practice -> Transform",
        "",
        "Evidence and discernment boundary:",
        "- Evidence can show that a pattern appears in the current corpus.",
        "- Theology can interpret that pattern through scripture, doctrine, tradition, reason, worship, and lived practice.",
        "- Discernment can ask how a person or community should respond before God.",
        "- None of these should be mislabeled as mathematical or scientific proof.",
        "",
        "Why this pattern is currently most visible:",
        "------------------------------------------",
        ]
    )

    lines.extend(["", "Chapter Three: Five Pattern Families", "------------------------------------"])
    append_reader_pattern_chapters(lines, top_pattern_rankings, top_pattern_layer_counts, limit=5)
    lines.extend(["", "Research Detail For The Five Patterns", "-------------------------------------"])
    append_top_pattern_families(lines, top_pattern_rankings, top_pattern_layer_counts, limit=5)
    lines.extend(
        [
            "",
            "Top-five guardrail:",
            "- These are related but distinct candidate families. Do not treat the strongest one as the only divine pattern.",
        ]
    )
    append_pattern_pressure_competition(lines, top_pattern_rankings, pressure_counts, limit=5)
    append_claim_ledger_section(lines, claim_ledger)
    append_lane_balance_section(lines, lane_balance_records)
    append_reviewed_source_packs_section(lines, reviewed_pack_names)
    append_cautious_confidence_section(lines)
    append_practical_theology_section(lines)

    lines.extend(
        [
            f"- Trinitarian signal: {score_trinitarian_pattern(trinity_counts)}",
            f"- Father: {trinity_counts.get('Father', 0):,}",
            f"- Son: {trinity_counts.get('Son', 0):,}",
            f"- Holy Spirit: {trinity_counts.get('Holy Spirit', 0):,}",
            "",
            "Strongest research layers:",
        ]
    )

    for layer, count in research_layer_counts.most_common(6):
        lines.append(f"- {layer}: {count:,}")

    lines.extend(["", "Music-note science/math support:"])
    if note_relationships:
        for relationship, count in note_relationships.most_common(5):
            lines.append(f"- {relationship}: {count:,}")
    else:
        lines.append("- No music-note relationships analyzed yet.")

    lines.extend(["", "Lyric meaning support:"])
    if music_meaning_counts:
        for context, count in music_meaning_counts.most_common(5):
            lines.append(f"- {context}: {count:,}")
    else:
        lines.append("- No lyric meaning contexts analyzed yet.")

    lines.extend(["", "Cultural meaning support:"])
    if cultural_meaning_counts:
        for context, count in cultural_meaning_counts.most_common(5):
            lines.append(f"- {context}: {count:,}")
    else:
        lines.append("- No cultural meaning contexts analyzed yet.")

    lines.extend(["", "Cross-layer synthesis support:"])
    if synthesis_lens_counts:
        for lens, count in synthesis_lens_counts.most_common(6):
            if count > 0:
                lines.append(f"- {lens}: {count:,}")
        for label, count in synthesis_depth_counts.most_common():
            lines.append(f"- Depth: {label}: {count:,}")
    else:
        lines.append("- No dedicated visual art, history, language, biblical-language, or psychology synthesis files analyzed yet.")

    lines.extend(["", "Comparative validity support:"])
    if comparative_validity_counts:
        for label, count in comparative_validity_counts.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No comparative religious-text, literature, or human-story files analyzed yet.")
    lines.append("- Comparative recurrence supports a broad human pattern, not automatic proof of the Trinitarian claim.")

    lines.extend(["", "Global language/text coverage:"])
    lines.append(f"- {score_global_coverage(language_family_counts, text_tradition_counts)}")
    if language_family_counts:
        present_families = [
            family
            for family in LANGUAGE_FAMILY_MARKERS
            if language_family_counts.get(family, 0) > 0
        ]
        lines.append(f"- Language families mapped: {len(present_families):,} of {len(LANGUAGE_FAMILY_MARKERS):,}")
    if text_tradition_counts:
        present_traditions = [
            tradition
            for tradition in TEXT_TRADITION_MARKERS
            if text_tradition_counts.get(tradition, 0) > 0
        ]
        lines.append(f"- Text traditions mapped: {len(present_traditions):,} of {len(TEXT_TRADITION_MARKERS):,}")
        lines.append("- Treat mapped coverage as a research agenda until actual texts and counter-readings are added.")

    lines.extend(["", "Cloud reference review:"])
    reviewed_cloud = source_quality_counts.get("Reviewed Cloud Reference", 0)
    unreviewed_cloud = source_quality_counts.get("Unreviewed Cloud Reference", 0)
    lines.append(f"- Reviewed cloud-reference markers: {reviewed_cloud:,}")
    lines.append(f"- Unreviewed cloud-reference markers: {unreviewed_cloud:,}")
    if unreviewed_cloud > reviewed_cloud:
        lines.append("- Treat cloud references as leads until checked against original sources, author expertise, date, publication venue, and counterarguments.")
    else:
        lines.append("- Cloud-reference review markers are balanced enough for cautious use.")

    lines.extend(["", "Theologian pattern-design support:"])
    if theologian_concepts:
        for concept, count in theologian_concepts.most_common(6):
            if count > 0:
                lines.append(f"- {concept}: {count:,}")
    else:
        lines.append("- No theologian pattern-design sources analyzed yet.")

    lines.extend(["", "Pressure-test result:", "---------------------"])
    if pressure_confidence:
        for label, count in pressure_confidence.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No pressure tests analyzed yet.")

    lines.extend(["", "Hold-under-friction result:", "---------------------------"])
    if hold_assessments:
        for label, count in hold_assessments.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No hold assessments yet.")

    lines.extend(["", "Deep-source result:", "-------------------"])
    if deep_area_scores:
        for label, count in deep_area_scores.most_common():
            lines.append(f"- {label}: {count:,}")
    else:
        lines.append("- No deep-source files analyzed yet.")

    lines.extend(
        [
            "",
            "Guardrails",
            "----------",
            "- This is a research hypothesis, not proof.",
            "- Father, Son, and Holy Spirit are distinct persons and one God.",
            "- Quantum/science claims must stay tied to qualified evidence.",
            "- Unresolved suffering must not be rushed into easy resolution.",
            "- Non-Christian traditions should be compared respectfully, not flattened.",
            "",
            "Modern-Life Application",
            "-----------------------",
            "Use the pattern to ask: What order or gift is present? What tension, suffering, beauty, or injustice must be named? What truth is being revealed? What moral response is called for? What community practice can carry it? What transformation or hope can be practiced today?",
            "",
            "Next Actions",
            "------------",
            "1. Deepen theologian source notes with primary-text references and disagreements across eras.",
            "2. Keep adding source-specific visual art, history, language, biblical-language, all-texts, and psychology notes for cross-layer synthesis.",
            "3. Treat language-family and text-tradition coverage as mapped but not universal until actual source notes and counter-readings are broad enough.",
            "4. Continue adding harder unresolved-suffering case studies, especially where repair remains absent.",
            "5. Keep qualified quantum/science references paired with counterarguments and narrow allowed conclusions.",
            "6. Review routed daily cloud references before promoting any candidate to reviewed evidence.",
            "7. Revise or weaken the pattern wherever pressure tests show it does not hold.",
        ]
    )

    return "\n".join(lines)


def save_text(path, text):
    """Save the generated research report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    documents = find_documents(RESEARCH_DIR)
    pattern_input_documents = find_pattern_inputs(PATTERN_INPUTS_DIR)
    music_documents = find_music_documents(MUSIC_LYRICS_DIR)
    music_note_documents = find_music_note_documents(MUSIC_NOTES_DIR)
    cultural_documents = find_cultural_documents(CULTURAL_INPUTS_DIR)
    pattern_test_documents = find_pattern_test_documents(PATTERN_TESTS_DIR)
    deep_source_documents = find_deep_source_documents(DEEP_SOURCE_DIR)
    theologian_documents = find_theologian_documents(THEOLOGIANS_DIR)
    synthesis_documents_by_lane = {
        lane: find_synthesis_documents(folder)
        for lane, folder in SYNTHESIS_SOURCE_DIRS.items()
    }

    if not documents:
        print("No research documents found.")
        print(f"Add .txt or .md files to: {RESEARCH_DIR}")
        return

    analyses = []
    for document in documents:
        print(f"Analyzing: {document.name}")
        analyses.append(analyze_document(document))

    pattern_seeds = []
    for document in pattern_input_documents:
        print(f"Reading pattern seed: {document.name}")
        pattern_seeds.append(parse_pattern_seed(document))

    music_analyses = []
    for document in music_documents:
        print(f"Analyzing lyric file: {document.name}")
        music_analyses.append(analyze_music_document(document))

    music_note_analyses = []
    for document in music_note_documents:
        print(f"Analyzing music-note file: {document.name}")
        music_note_analyses.append(analyze_music_note_document(document))

    cultural_analyses = []
    for document in cultural_documents:
        print(f"Analyzing cultural file: {document.name}")
        cultural_analyses.append(analyze_cultural_document(document))

    pattern_test_analyses = []
    for document in pattern_test_documents:
        print(f"Analyzing pattern-test file: {document.name}")
        pattern_test_analyses.append(analyze_pattern_test_document(document))

    deep_source_analyses = []
    for document in deep_source_documents:
        print(f"Analyzing deep-source file: {document.name}")
        deep_source_analyses.append(analyze_deep_source_document(document))

    theologian_analyses = []
    for document in theologian_documents:
        print(f"Analyzing theologian file: {document.name}")
        theologian_analyses.append(analyze_theologian_document(document))

    synthesis_analyses = []
    for lane, lane_documents in synthesis_documents_by_lane.items():
        for document in lane_documents:
            print(f"Analyzing {lane} synthesis file: {document.name}")
            synthesis_analyses.append(analyze_synthesis_document(document, lane))

    report = create_report(analyses)
    candidates_report = create_pattern_candidates_report(analyses)
    discovered_patterns_report = create_discovered_patterns_report(analyses, pattern_seeds)
    music_patterns_report = create_music_patterns_report(analyses, music_analyses)
    music_note_patterns_report = create_music_note_patterns_report(
        analyses,
        music_note_analyses,
    )
    cultural_patterns_report = create_cultural_patterns_report(
        analyses,
        cultural_analyses,
    )
    cross_layer_reasoning_report = create_cross_layer_reasoning_report(
        analyses,
        music_analyses,
        music_note_analyses,
        cultural_analyses,
        pattern_test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )
    pattern_test_report = create_pattern_test_report(
        analyses,
        pattern_test_analyses,
    )
    deep_source_review_report = create_deep_source_review_report(deep_source_analyses)
    theologian_pattern_design_report = create_theologian_pattern_design_report(
        analyses,
        theologian_analyses,
    )
    top_patterns_report = create_top_patterns_report(
        analyses,
        synthesis_analyses,
        pattern_test_analyses,
        deep_source_analyses,
    )
    reader_book_report = create_reader_book_report(
        analyses,
        music_analyses,
        music_note_analyses,
        cultural_analyses,
        pattern_test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )
    disciplined_assistant_report = create_disciplined_theological_assistant_report(
        analyses,
        music_analyses,
        music_note_analyses,
        cultural_analyses,
        pattern_test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )
    divine_pattern_summary_report = create_divine_pattern_summary_report(
        analyses,
        music_analyses,
        music_note_analyses,
        cultural_analyses,
        pattern_test_analyses,
        deep_source_analyses,
        theologian_analyses,
        synthesis_analyses,
    )
    strategy_layer_counts = combine_layer_counts(
        analyses
        + synthesis_analyses
        + pattern_test_analyses
        + deep_source_analyses
        + theologian_analyses
    )
    next_search_strategy = build_next_search_strategy(
        read_daily_research_digest(),
        rank_divine_pattern_candidates(strategy_layer_counts),
        combine_pressure_counts(pattern_test_analyses),
        create_lane_balance_records(
            analyses,
            cultural_analyses,
            pattern_test_analyses,
            deep_source_analyses,
            theologian_analyses,
            synthesis_analyses,
        ),
        parse_claim_ledger(),
        load_reviewed_source_pack_names(),
    )
    save_text(REPORT_PATH, report)
    save_text(PATTERN_CANDIDATES_PATH, candidates_report)
    save_text(DISCOVERED_PATTERNS_PATH, discovered_patterns_report)
    save_text(MUSIC_PATTERNS_PATH, music_patterns_report)
    save_text(MUSIC_NOTE_PATTERNS_PATH, music_note_patterns_report)
    save_text(CULTURAL_PATTERNS_PATH, cultural_patterns_report)
    save_text(CROSS_LAYER_REASONING_PATH, cross_layer_reasoning_report)
    save_text(PATTERN_TEST_REPORT_PATH, pattern_test_report)
    save_text(DEEP_SOURCE_REVIEW_PATH, deep_source_review_report)
    save_text(THEOLOGIAN_REPORT_PATH, theologian_pattern_design_report)
    save_text(TOP_PATTERNS_PATH, top_patterns_report)
    save_text(READER_BOOK_PATH, reader_book_report)
    save_text(DISCIPLINED_ASSISTANT_PATH, disciplined_assistant_report)
    save_text(SUMMARY_REPORT_PATH, divine_pattern_summary_report)
    save_next_search_strategy(next_search_strategy)

    print("Divine pattern research analysis complete.")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Candidates saved to: {PATTERN_CANDIDATES_PATH}")
    print(f"Discovered patterns saved to: {DISCOVERED_PATTERNS_PATH}")
    print(f"Music lyric patterns saved to: {MUSIC_PATTERNS_PATH}")
    print(f"Music note patterns saved to: {MUSIC_NOTE_PATTERNS_PATH}")
    print(f"Cultural patterns saved to: {CULTURAL_PATTERNS_PATH}")
    print(f"Cross-layer reasoning saved to: {CROSS_LAYER_REASONING_PATH}")
    print(f"Pattern test report saved to: {PATTERN_TEST_REPORT_PATH}")
    print(f"Deep source review saved to: {DEEP_SOURCE_REVIEW_PATH}")
    print(f"Theologian pattern design saved to: {THEOLOGIAN_REPORT_PATH}")
    print(f"Top five patterns saved to: {TOP_PATTERNS_PATH}")
    print(f"Reader book report saved to: {READER_BOOK_PATH}")
    print(f"Disciplined assistant report saved to: {DISCIPLINED_ASSISTANT_PATH}")
    print(f"Summary report saved to: {SUMMARY_REPORT_PATH}")
    print(f"Next search strategy saved to: {SEARCH_STRATEGY_PATH}")


if __name__ == "__main__":
    main()
