// Divine Core Phase 1.
// This lightweight reasoning layer is intentionally isolated from existing app
// behavior. Later phases can use it as a shared foundation for Divine Pattern,
// Shepherd, Divine Scholar, Bible Study, and future tools.

(function attachDivineReasoningCore(globalScope) {
  const DEFAULT_NEXT_LAYER = "scripture-and-voice-profile-review";

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

  function buildBiblicalTheologyFrame(scriptureThemes) {
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

  function buildEcclesialWisdomFrame(selectedVoices) {
    const voices = asArray(selectedVoices);

    return {
      selectedVoices: voices,
      sharedPosture: "Test the pattern with historic Christian confession, pastoral charity, and humility.",
      likelyUse: voices.length
        ? "Use the selected voices as reasoning lenses, not as authorities above Scripture."
        : "Begin with creedal boundaries and a fallback shared Christian wisdom profile."
    };
  }

  function buildDoctrineCheck(patternSummary, scriptureThemes) {
    const combinedText = [
      patternSummary.title,
      patternSummary.summary,
      ...asArray(scriptureThemes)
    ].join(" ").toLowerCase();

    const trinitarianSignal = ["father", "son", "spirit", "christ", "jesus"].some((term) =>
      combinedText.includes(term)
    );
    const resurrectionSignal = ["resurrection", "new creation", "life everlasting"].some((term) =>
      combinedText.includes(term)
    );
    const graceSignal = ["grace", "mercy", "forgiveness", "gospel"].some((term) =>
      combinedText.includes(term)
    );

    return {
      creedalFit: trinitarianSignal ? "has-explicit-christian-reference" : "needs-creedal-review",
      graceAndGospel: graceSignal ? "present" : "not-yet-explicit",
      resurrectionHope: resurrectionSignal ? "present" : "not-yet-explicit",
      cautions: [
        "Check claims against the Nicene and Apostles' Creeds before treating them as doctrine.",
        "Keep descriptive pattern recognition distinct from theological proof."
      ]
    };
  }

  function buildChallengeQuestions(input, patternSummary, doctrineCheck) {
    const questions = [
      "What does Scripture clearly affirm, deny, or leave open here?",
      "Does this pattern lead toward love of God and neighbor?",
      "What would historic Christian confession guard against in this interpretation?"
    ];

    if (input.userQuestion) {
      questions.unshift("What is the user's question asking for: comfort, correction, explanation, or discernment?");
    }

    if (patternSummary.observedSignals.length === 0) {
      questions.push("What concrete evidence or context is still missing?");
    }

    if (doctrineCheck.creedalFit === "needs-creedal-review") {
      questions.push("How does this connect to the Father, Son, and Holy Spirit without forcing the pattern?");
    }

    return questions;
  }

  function buildConfidenceSignals(patternSummary, scriptureThemes, selectedVoices) {
    const signalCount = patternSummary.observedSignals.length;
    const themeCount = asArray(scriptureThemes).length;
    const voiceCount = asArray(selectedVoices).length;

    return {
      patternEvidence: signalCount > 2 ? "moderate" : signalCount > 0 ? "early" : "thin",
      scriptureGrounding: themeCount > 1 ? "multiple-themes" : themeCount === 1 ? "single-theme" : "not-supplied",
      ecclesialCrossCheck: voiceCount > 1 ? "multiple-voices" : voiceCount === 1 ? "single-voice" : "fallback-needed",
      overall: signalCount > 0 && themeCount > 0 ? "provisional" : "exploratory"
    };
  }

  function chooseNextLayer(confidenceSignals, doctrineCheck) {
    if (doctrineCheck.creedalFit === "needs-creedal-review") {
      return "creedal-doctrine-check";
    }

    if (confidenceSignals.scriptureGrounding === "not-supplied") {
      return "scripture-theme-mapping";
    }

    if (confidenceSignals.ecclesialCrossCheck === "fallback-needed") {
      return "theologian-profile-cross-check";
    }

    return DEFAULT_NEXT_LAYER;
  }

  function buildDivineReasoningContext(input) {
    const safeInput = input || {};
    const patternSummary = summarizePattern(safeInput.pattern);
    const biblicalTheologyFrame = buildBiblicalTheologyFrame(safeInput.scriptureThemes);
    const ecclesialWisdomFrame = buildEcclesialWisdomFrame(safeInput.selectedVoices);
    const doctrineCheck = buildDoctrineCheck(patternSummary, safeInput.scriptureThemes);
    const challengeQuestions = buildChallengeQuestions(safeInput, patternSummary, doctrineCheck);
    const confidenceSignals = buildConfidenceSignals(
      patternSummary,
      safeInput.scriptureThemes,
      safeInput.selectedVoices
    );

    return {
      patternSummary,
      biblicalTheologyFrame,
      ecclesialWisdomFrame,
      doctrineCheck,
      challengeQuestions,
      confidenceSignals,
      nextRecommendedLayer: chooseNextLayer(confidenceSignals, doctrineCheck)
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
