from collections import Counter, defaultdict
import re
from pathlib import Path


RESEARCH_DIR = Path("research_documents")
PATTERN_INPUTS_DIR = Path("pattern_inputs")
MUSIC_LYRICS_DIR = Path("music_lyrics")
MUSIC_NOTES_DIR = Path("music_notes")
CULTURAL_INPUTS_DIR = Path("cultural_inputs")
PATTERN_TESTS_DIR = Path("pattern_tests")
DEEP_SOURCE_DIR = Path("deep_sources")
REPORTS_DIR = Path("reports")
REPORT_PATH = REPORTS_DIR / "divine_pattern_research_report.txt"
PATTERN_CANDIDATES_PATH = REPORTS_DIR / "divine_pattern_candidates_report.txt"
DISCOVERED_PATTERNS_PATH = REPORTS_DIR / "discovered_patterns_report.txt"
MUSIC_PATTERNS_PATH = REPORTS_DIR / "music_lyric_patterns_report.txt"
MUSIC_NOTE_PATTERNS_PATH = REPORTS_DIR / "music_note_patterns_report.txt"
CULTURAL_PATTERNS_PATH = REPORTS_DIR / "cultural_pattern_relationships_report.txt"
PATTERN_TEST_REPORT_PATH = REPORTS_DIR / "divine_pattern_test_report.txt"
DEEP_SOURCE_REVIEW_PATH = REPORTS_DIR / "deep_source_review_report.txt"
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


def read_document(path):
    """Read a research document."""
    return path.read_text(encoding="utf-8-sig", errors="replace")


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

    return {
        "file_name": path.name,
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
    quality_counts = count_source_quality_markers(text)
    meaning_context_counts = count_meaning_contexts(text)
    pressure_counts = count_pressure_types(text)

    area_scores = {
        area: score_deep_source_area(area, source_type_counts, count)
        for area, count in area_counts.items()
    }

    return {
        "file_name": path.name,
        "characters": len(text),
        "sentences": len(sentences),
        "words": len([word for word in tokenize(text) if word not in STOP_WORDS]),
        "area_counts": area_counts,
        "source_type_counts": source_type_counts,
        "source_quality_counts": quality_counts,
        "meaning_context_counts": meaning_context_counts,
        "pressure_counts": pressure_counts,
        "area_scores": area_scores,
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
        combined.update(analysis["layer_counts"])

    return combined


def combine_meaning_context_counts(analyses):
    """Combine meaning-stage context counts across analyses."""
    combined = Counter()

    for analysis in analyses:
        combined.update(analysis.get("meaning_context_counts", {}))

    return combined


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


def combine_layer_evidence(analyses):
    """Collect evidence snippets for each divine-pattern layer."""
    combined = defaultdict(list)

    for analysis in analyses:
        for layer, snippets in analysis["layer_evidence"].items():
            for snippet in snippets:
                if len(combined[layer]) < 4:
                    combined[layer].append((analysis["file_name"], snippet))

    return dict(combined)


def score_layer(count):
    """Convert a raw layer count into a cautious strength label."""
    if count >= 1000:
        return "strong signal"
    if count >= 250:
        return "moderate signal"
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
        return "strong candidate"
    if present_layers == total_layers and minimum_signal >= 50:
        return "promising candidate"
    if present_layers == total_layers:
        return "early candidate"
    if present_layers > 0:
        return "partial candidate"
    return "not detected"


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
        "Physical Order -> Mathematical Structure -> Quantum Probability -> Life And Consciousness -> Meaning And Logos -> Moral Response -> Worship And Community -> Transformation",
        "",
        "Candidate Rankings",
        "------------------",
    ]

    ranked_candidates = sorted(
        DIVINE_PATTERN_CANDIDATES,
        key=lambda candidate: sum(layer_counts.get(layer, 0) for layer in candidate["layers"]),
        reverse=True,
    )

    for candidate in ranked_candidates:
        status = score_candidate(candidate, layer_counts)
        layer_total = sum(layer_counts.get(layer, 0) for layer in candidate["layers"])

        lines.extend(
            [
                "",
                candidate["name"],
                "-" * len(candidate["name"]),
                f"Status: {status}",
                f"Layer signal total: {layer_total:,}",
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

    lines.extend(
        [
            "",
            "Best Current Candidate",
            "----------------------",
            "The strongest overall pattern is the layered convergence model:",
            "",
            "Being -> Order -> Life -> Consciousness -> Meaning -> Moral Response -> Worship -> Transformation",
            "",
            "Christian interpretation:",
            "",
            "Father -> Creation",
            "Son / Logos -> Revelation and Redemption",
            "Holy Spirit -> Presence and Transformation",
            "",
            "Responsible Claim",
            "-----------------",
            "AI can help compare these layers and generate research hypotheses about whether order, intelligibility, moral transformation, and worship form a coherent Christian pattern across reality and human life.",
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

    lines.extend(
        [
            "",
            "Divine Pattern Finder",
            "---------------------",
            "Model: Physical Order -> Mathematical Structure -> Quantum Probability -> Life And Consciousness -> Meaning And Logos -> Moral Response -> Worship And Community -> Transformation",
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
    quality_counts = Counter()
    pressure_counts = Counter()

    for analysis in deep_source_analyses:
        area_counts.update(analysis["area_counts"])
        source_type_counts.update(analysis["source_type_counts"])
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

    lines.extend(
        [
            "",
            "Use Rules",
            "---------",
            "1. If an area is under-sourced, keep it as a research question, not a conclusion.",
            "2. Quantum/science claims need qualified science sources before they can support any theological comparison.",
            "3. Suffering claims need lament, pastoral care, lived cases, and counterarguments before they can guide practical theology.",
            "4. A source-supported status does not prove the divine pattern; it only means the claim has enough support to discuss responsibly.",
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
    pattern_test_report = create_pattern_test_report(
        analyses,
        pattern_test_analyses,
    )
    deep_source_review_report = create_deep_source_review_report(deep_source_analyses)
    save_text(REPORT_PATH, report)
    save_text(PATTERN_CANDIDATES_PATH, candidates_report)
    save_text(DISCOVERED_PATTERNS_PATH, discovered_patterns_report)
    save_text(MUSIC_PATTERNS_PATH, music_patterns_report)
    save_text(MUSIC_NOTE_PATTERNS_PATH, music_note_patterns_report)
    save_text(CULTURAL_PATTERNS_PATH, cultural_patterns_report)
    save_text(PATTERN_TEST_REPORT_PATH, pattern_test_report)
    save_text(DEEP_SOURCE_REVIEW_PATH, deep_source_review_report)

    print("Divine pattern research analysis complete.")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Candidates saved to: {PATTERN_CANDIDATES_PATH}")
    print(f"Discovered patterns saved to: {DISCOVERED_PATTERNS_PATH}")
    print(f"Music lyric patterns saved to: {MUSIC_PATTERNS_PATH}")
    print(f"Music note patterns saved to: {MUSIC_NOTE_PATTERNS_PATH}")
    print(f"Cultural patterns saved to: {CULTURAL_PATTERNS_PATH}")
    print(f"Pattern test report saved to: {PATTERN_TEST_REPORT_PATH}")
    print(f"Deep source review saved to: {DEEP_SOURCE_REVIEW_PATH}")


if __name__ == "__main__":
    main()
