// Divine Core Phase 6A.
// Development utility only: creates one empty structured draft profile for
// future Divine Core expansion. It does not connect to Shepherd, the book
// report, UI, or any application behavior, and it never writes source text or
// quotations.

(function runCreateDailySourceDraft() {
  const fs = require("fs");
  const path = require("path");

  const divineCoreDir = __dirname;
  const queuePath = path.join(divineCoreDir, "sourceExpansionQueue.json");
  const draftsDir = path.join(divineCoreDir, "drafts");

  function slugify(value) {
    return String(value)
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function readJson(filePath) {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  }

  function writeJson(filePath, value) {
    fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + "\n", "utf8");
  }

  function buildDraftProfile(source) {
    return {
      name: source.name,
      author: source.author,
      category: source.category,
      status: "draft",
      reasoningMethod: {
        startingPoint: "Draft prompt: identify the source's basic theological starting point without quoting it.",
        coreEmphases: [],
        discernmentQuestions: [],
        pastoralPriorities: [],
        commonWarnings: []
      },
      patternRecognition: {
        looksFor: [],
        strengthens: [],
        guardsAgainst: []
      },
      composerHints: {
        tone: "Draft prompt: describe an appropriate composer tone after review.",
        preferredStructure: [],
        avoid: [
          "do not quote or reproduce source text",
          "do not treat this draft as reviewed",
          "do not generate final user-facing prose"
        ]
      },
      reviewNotes: [
        "Draft generated as a safe empty structure for later human review."
      ]
    };
  }

  function ensureQueueShape(queue) {
    if (!queue || !Array.isArray(queue.sources)) {
      throw new Error("sourceExpansionQueue.json must contain a sources array.");
    }
  }

  function createNextDraft() {
    const queue = readJson(queuePath);
    ensureQueueShape(queue);

    const nextSource = queue.sources.find((source) => !source.drafted);

    if (!nextSource) {
      console.log("No undrafted sources remain in sourceExpansionQueue.json.");
      return;
    }

    fs.mkdirSync(draftsDir, { recursive: true });

    const draftFileName = [
      slugify(nextSource.author),
      slugify(nextSource.name)
    ].filter(Boolean).join("-") + ".json";
    const draftPath = path.join(draftsDir, draftFileName);

    if (fs.existsSync(draftPath)) {
      throw new Error("Draft already exists and will not be overwritten: " + draftPath);
    }

    writeJson(draftPath, buildDraftProfile(nextSource));

    nextSource.drafted = true;
    nextSource.draftFile = "divineCore/drafts/" + draftFileName;
    writeJson(queuePath, queue);

    console.log("Created draft: " + nextSource.draftFile);
  }

  createNextDraft();
})();
