// Divine Core Phase 3.
// This lightweight reasoning layer is intentionally isolated from existing app
// behavior. Divine Core reasons only; it should not write final user-facing
// prose. Shepherd, Book Report, Scholar, Bible Study, and future tools should
// use separate composers tailored to their own audience and interface.

(function attachDivineReasoningCore(globalScope) {
  const DEFAULT_NEXT_LAYER = "composer-specific-synthesis";

  function asArray(value) {
    if (Array.isArray(value)) {
      return value.filter(Boolean);
    }

    return value ? [value] : [];
  }

  function summarizePattern(pattern) {
    if (!pattern) {
      return {
        title: "No pattern supplied",
        summary: "The reasoning context needs a pattern before stronger claims can be made.",
        observedSignals: []
      };
    }

    if (typeof pattern === "string") {
      return {
        title: pattern.slice(0, 80),
        summary: pattern,
        observedSignals: []
      };
    }

    return {
      title: pattern.title || pattern.name || pattern.id || "Untitled pattern",
      summary: pattern.summary || pattern.description || pattern.claim || "No summary supplied.",
      observedSignals: asArray(pattern.signals || pattern.observedSignals || pattern.evidence)
    };
  }

  function includesAny(text, terms) {
    return terms.some((term) => text.includes(term));
  }

  function normalizeVoiceName(voice) {
    return String(voice || "").trim().toLowerCase();
  }

  function splitSelectedVoices(selectedVoices) {
    const voices = asArray(selectedVoices).map(normalizeVoiceName).filter(Boolean);
    const traditionKeys = ["anglican", "reformed", "orthodox", "catholic", "lutheran", "evangelical"];
    const councilKeys = ["nicaea", "chalcedon"];
    const creedKeys = ["apostles", "apostlescreed", "nicene", "nicenecreed", "athanasian", "athanasiancreed"];

    return {
      raw: voices,
      traditions: voices.filter((voice) => traditionKeys.includes(voice)),
      councils: voices.filter((voice) => councilKeys.includes(voice)),
      creeds: voices.filter((voice) => creedKeys.includes(voice)),
      theologians: voices.filter(
        (voice) => !traditionKeys.includes(voice) && !councilKeys.includes(voice) && !creedKeys.includes(voice)
      )
    };
  }

  function buildScriptureFrame(scriptureThemes) {
    const themes = asArray(scriptureThemes);

    return {
      themes,
      primaryQuestion: themes.length
        ? "How do these Scripture themes clarify, limit, or correct the pattern?"
        : "Which Scripture themes should be examined before interpreting this pattern?",
      cautions: [
        "Do not infer doctrine from a pattern without Scripture.",
        "Read themes in canonical and pastoral context."
      ]
    };
  }

  function buildCreedFrame(text) {
    return {
      suggestedCreeds: [
        includesAny(text, ["trinity", "father", "son", "spirit"]) ? "athanasianCreed" : "apostlesCreed",
        includesAny(text, ["christ", "jesus", "incarnation", "resurrection"]) ? "niceneCreed" : "apostlesCreed"
      ].filter((value, index, array) => array.indexOf(value) === index),
      primaryQuestion: "Does the interpretation fit the basic grammar of historic Christian confession?",
      guardsAgainst: [
        "vague theism replacing Trinitarian faith",
        "pattern recognition being treated as doctrine without confession"
      ]
    };
  }

  function buildCouncilFrame(text, voiceGroups) {
    const suggestedCouncils = [];

    if (includesAny(text, ["christ", "jesus", "son", "incarnation"])) {
      suggestedCouncils.push("nicaea", "chalcedon");
    }

    voiceGroups.councils.forEach((council) => {
      if (!suggestedCouncils.includes(council)) {
        suggestedCouncils.push(council);
      }
    });

    return {
      suggestedCouncils,
      primaryQuestion: "Does this preserve the Church's tested boundaries around Christ and the Trinity?",
      cautions: [
        "Use councils as doctrinal guardrails, not as a replacement for Scripture.",
        "Avoid making every pattern a conciliar issue."
      ]
    };
  }

  function buildTraditionFrame(voiceGroups) {
    const traditions = voiceGroups.traditions;

    return {
      selectedTraditions: traditions,
      sharedPosture: "Let traditions cross-check reasoning with Scripture, doctrine, worship, and pastoral wisdom.",
      likelyUse: traditions.length
        ? "Use selected traditions as accountable lenses, not as final composers."
        : "Use broad shared Christian wisdom until a tradition is selected."
    };
  }

  function buildTheologianFrame(voiceGroups) {
    const theologians = voiceGroups.theologians;

    return {
      selectedTheologians: theologians,
      sharedPosture: "Use theologians as reasoning companions whose emphases and cautions can test the pattern.",
      likelyUse: theologians.length
        ? "Compare the selected theologians for convergences, tensions, and pastoral warnings."
        : "No theologian-specific lens supplied; rely on canonical, creedal, council, and tradition frames."
    };
  }

  function buildAgreementSignals(text, scriptureThemes, voiceGroups) {
    const trinitarianSignal = includesAny(text, ["father", "son", "spirit", "trinity"]);
    const christSignal = includesAny(text, ["christ", "jesus", "incarnation", "cross"]);
    const graceSignal = includesAny(text, ["grace", "mercy", "forgiveness", "gospel"]);
    const resurrectionSignal = includesAny(text, ["resurrection", "new creation", "life everlasting"]);

    return {
      scriptureDoctrineBridge: asArray(scriptureThemes).length ? "scripture-themes-supplied" : "needs-scripture-themes",
      trinitarianReference: trinitarianSignal ? "present" : "not-yet-explicit",
      christologicalReference: christSignal ? "present" : "not-yet-explicit",
      graceAndGospel: graceSignal ? "present" : "not-yet-explicit",
      resurrectionHope: resurrectionSignal ? "present" : "not-yet-explicit",
      ecclesialBreadth: voiceGroups.raw.length > 2 ? "broad-cross-check" : voiceGroups.raw.length ? "limited-cross-check" : "fallback-needed"
    };
  }

  function buildChallengeQuestions(input, patternSummary, agreementSignals) {
    const questions = [
      "What does Scripture clearly affirm, deny, or leave open here?",
      "Does this pattern lead toward love of God and neighbor?",
      "What would creeds, councils, traditions, and theologians each guard against?"
    ];

    if (input.userQuestion) {
      questions.unshift("What is the user's question asking for: comfort, correction, explanation, or discernment?");
    }

    if (patternSummary.observedSignals.length === 0) {
      questions.push("What concrete evidence or context is still missing?");
    }

    if (agreementSignals.trinitarianReference === "not-yet-explicit") {
      questions.push("How does this connect to the Father, Son, and Holy Spirit without forcing the pattern?");
    }

    if (agreementSignals.christologicalReference === "not-yet-explicit") {
      questions.push("How does this remain centered on Christ rather than generic spirituality?");
    }

    return questions;
  }

  function buildConfidenceSignals(patternSummary, scriptureThemes, voiceGroups, agreementSignals) {
    const signalCount = patternSummary.observedSignals.length;
    const themeCount = asArray(scriptureThemes).length;
    const voiceCount = voiceGroups.raw.length;

    return {
      patternEvidence: signalCount > 2 ? "moderate" : signalCount > 0 ? "early" : "thin",
      scriptureGrounding: themeCount > 1 ? "multiple-themes" : themeCount === 1 ? "single-theme" : "not-supplied",
      ecclesialCrossCheck: voiceCount > 2 ? "broad" : voiceCount > 0 ? "limited" : "fallback-needed",
      doctrinalClarity:
        agreementSignals.trinitarianReference === "present" && agreementSignals.christologicalReference === "present"
          ? "explicit"
          : "needs-review",
      overall: signalCount > 0 && themeCount > 0 ? "provisional" : "exploratory"
    };
  }

  function buildComposerGuidance(confidenceSignals) {
    return {
      role: "reasoning-context-only",
      instruction: "Do not compose final user-facing prose from Divine Core directly.",
      handoff: "Pass this structure to a product-specific composer for Shepherd, Book Report, Scholar, or Bible Study.",
      toneCaution:
        confidenceSignals.overall === "exploratory"
          ? "Composer should use tentative language and ask for more context."
          : "Composer may summarize provisional reasoning with clear caveats."
    };
  }

  function chooseNextLayer(confidenceSignals, agreementSignals) {
    if (
      agreementSignals.trinitarianReference === "not-yet-explicit" ||
      agreementSignals.christologicalReference === "not-yet-explicit"
    ) {
      return "creedal-doctrine-check";
    }

    if (confidenceSignals.scriptureGrounding === "not-supplied") {
      return "scripture-theme-mapping";
    }

    if (confidenceSignals.ecclesialCrossCheck === "fallback-needed") {
      return "tradition-and-theologian-cross-check";
    }

    return DEFAULT_NEXT_LAYER;
  }

  function buildReasoningTrace(voiceGroups, challengeQuestions, confidenceSignals, nextRecommendedLayer) {
    const layersUsed = [
      "patternSummary",
      "scriptureFrame",
      "creedFrame",
      "councilFrame",
      "traditionFrame",
      "theologianFrame",
      "agreementSignals",
      "confidenceSignals",
      "composerGuidance"
    ];
    const challengeLayerTriggered = nextRecommendedLayer !== DEFAULT_NEXT_LAYER;

    return {
      layersUsed,
      selectedVoices: voiceGroups.raw,
      challengeLayerTriggered,
      confidenceSummary: [
        "overall:",
        confidenceSignals.overall,
        "scripture:",
        confidenceSignals.scriptureGrounding,
        "ecclesial:",
        confidenceSignals.ecclesialCrossCheck,
        "doctrine:",
        confidenceSignals.doctrinalClarity
      ].join(" "),
      composerSafe: true,
      challengeQuestionCount: challengeQuestions.length
    };
  }

  function buildDivineReasoningContext(input) {
    const safeInput = input || {};
    const patternSummary = summarizePattern(safeInput.pattern);
    const voiceGroups = splitSelectedVoices(safeInput.selectedVoices);
    const combinedText = [
      patternSummary.title,
      patternSummary.summary,
      ...patternSummary.observedSignals,
      ...asArray(safeInput.scriptureThemes),
      safeInput.userQuestion || ""
    ].join(" ").toLowerCase();
    const scriptureFrame = buildScriptureFrame(safeInput.scriptureThemes);
    const creedFrame = buildCreedFrame(combinedText);
    const councilFrame = buildCouncilFrame(combinedText, voiceGroups);
    const traditionFrame = buildTraditionFrame(voiceGroups);
    const theologianFrame = buildTheologianFrame(voiceGroups);
    const agreementSignals = buildAgreementSignals(combinedText, safeInput.scriptureThemes, voiceGroups);
    const challengeQuestions = buildChallengeQuestions(safeInput, patternSummary, agreementSignals);
    const confidenceSignals = buildConfidenceSignals(
      patternSummary,
      safeInput.scriptureThemes,
      voiceGroups,
      agreementSignals
    );
    const composerGuidance = buildComposerGuidance(confidenceSignals);
    const nextRecommendedLayer = chooseNextLayer(confidenceSignals, agreementSignals);
    const reasoningTrace = buildReasoningTrace(
      voiceGroups,
      challengeQuestions,
      confidenceSignals,
      nextRecommendedLayer
    );

    return {
      patternSummary,
      scriptureFrame,
      creedFrame,
      councilFrame,
      traditionFrame,
      theologianFrame,
      agreementSignals,
      challengeQuestions,
      confidenceSignals,
      composerGuidance,
      nextRecommendedLayer,
      reasoningTrace
    };
  }

  const api = Object.freeze({
    buildDivineReasoningContext
  });

  globalScope.DivineReasoningCore = api;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window);
