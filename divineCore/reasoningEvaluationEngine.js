// Divine Core Phase 4.
// This development-focused evaluator scores reasoning quality before any
// application consumes Divine Core. It stays rule-based and does not generate
// final user-facing prose.

(function attachReasoningEvaluationEngine(globalScope) {
  function clampScore(score) {
    return Math.max(0, Math.min(100, score));
  }

  function asArray(value) {
    return Array.isArray(value) ? value.filter(Boolean) : [];
  }

  function scoreScriptureCoverage(reasoningContext) {
    const notes = [];
    const themes = asArray(reasoningContext.scriptureFrame && reasoningContext.scriptureFrame.themes);
    let score = 35;

    if (themes.length >= 3) {
      score += 45;
      notes.push("Multiple canonical themes are present.");
    } else if (themes.length > 0) {
      score += 25;
      notes.push("Some Scripture themes are present, but coverage is still narrow.");
    } else {
      notes.push("No Scripture themes were supplied.");
    }

    if (reasoningContext.agreementSignals &&
      reasoningContext.agreementSignals.scriptureDoctrineBridge === "scripture-themes-supplied") {
      score += 10;
      notes.push("Scripture and doctrine are explicitly bridged.");
    }

    if (asArray(reasoningContext.challengeQuestions).some((question) => question.includes("Scripture"))) {
      score += 10;
      notes.push("Challenge questions keep Scripture in view.");
    }

    return {
      score: clampScore(score),
      notes
    };
  }

  function scoreDoctrinalConsistency(reasoningContext) {
    const notes = [];
    const signals = reasoningContext.agreementSignals || {};
    const creedCount = asArray(reasoningContext.creedFrame && reasoningContext.creedFrame.suggestedCreeds).length;
    const councilCount = asArray(reasoningContext.councilFrame && reasoningContext.councilFrame.suggestedCouncils).length;
    let score = 40;

    if (signals.trinitarianReference === "present") {
      score += 20;
      notes.push("Trinitarian reference is explicit.");
    } else {
      notes.push("Trinitarian reference is not yet explicit.");
    }

    if (signals.christologicalReference === "present") {
      score += 20;
      notes.push("Christological reference is explicit.");
    } else {
      notes.push("Christological reference is not yet explicit.");
    }

    if (creedCount > 0) {
      score += 10;
      notes.push("Creedal review is represented.");
    }

    if (councilCount > 0) {
      score += 10;
      notes.push("Council guardrails are represented.");
    }

    return {
      score: clampScore(score),
      notes
    };
  }

  function scoreEcclesialSupport(reasoningContext) {
    const notes = [];
    const selectedTraditions = asArray(reasoningContext.traditionFrame && reasoningContext.traditionFrame.selectedTraditions);
    const selectedTheologians = asArray(
      reasoningContext.theologianFrame && reasoningContext.theologianFrame.selectedTheologians
    );
    let score = 30;

    if (selectedTraditions.length) {
      score += 25;
      notes.push("At least one tradition lens is selected.");
    } else {
      notes.push("No tradition lens is selected.");
    }

    if (selectedTheologians.length) {
      score += 25;
      notes.push("At least one theologian lens is selected.");
    } else {
      notes.push("No theologian lens is selected.");
    }

    if ((reasoningContext.agreementSignals || {}).ecclesialBreadth === "broad-cross-check") {
      score += 20;
      notes.push("Ecclesial cross-check is broad.");
    } else {
      notes.push("Ecclesial cross-check is limited or fallback-based.");
    }

    return {
      score: clampScore(score),
      notes
    };
  }

  function scoreTheologicalBalance(reasoningContext) {
    const notes = [];
    const signals = reasoningContext.agreementSignals || {};
    let score = 45;

    if (signals.graceAndGospel === "present") {
      score += 15;
      notes.push("Grace and gospel are visible.");
    } else {
      notes.push("Grace and gospel are not yet explicit.");
    }

    if (signals.resurrectionHope === "present") {
      score += 15;
      notes.push("Resurrection hope is visible.");
    } else {
      notes.push("Resurrection hope is not yet explicit.");
    }

    if ((reasoningContext.confidenceSignals || {}).overall === "provisional") {
      score += 10;
      notes.push("Reasoning remains provisional rather than overconfident.");
    }

    if ((reasoningContext.composerGuidance || {}).role === "reasoning-context-only") {
      score += 15;
      notes.push("Composer boundary is preserved.");
    }

    return {
      score: clampScore(score),
      notes
    };
  }

  function assessNovelty(reasoningContext) {
    const notes = [];
    const confidenceSignals = reasoningContext.confidenceSignals || {};
    const doctrinalClarity = confidenceSignals.doctrinalClarity;
    const scriptureGrounding = confidenceSignals.scriptureGrounding;
    const ecclesialCrossCheck = confidenceSignals.ecclesialCrossCheck;

    if (doctrinalClarity === "explicit" && scriptureGrounding !== "not-supplied" && ecclesialCrossCheck === "broad") {
      notes.push("The reasoning is strongly tied to Scripture, doctrine, and broad ecclesial support.");
      return {
        level: "historic",
        notes
      };
    }

    if (scriptureGrounding !== "not-supplied" && ecclesialCrossCheck !== "fallback-needed") {
      notes.push("The reasoning extends from supplied sources but still needs stronger cross-checking.");
      return {
        level: "supported extension",
        notes
      };
    }

    notes.push("The reasoning lacks enough Scripture or ecclesial support to treat as more than speculative.");
    return {
      level: "speculative",
      notes
    };
  }

  function assessPastoralRisk(reasoningContext) {
    const notes = [];
    const combinedText = [
      reasoningContext.patternSummary && reasoningContext.patternSummary.title,
      reasoningContext.patternSummary && reasoningContext.patternSummary.summary,
      reasoningContext.userQuestion
    ].join(" ").toLowerCase();
    const highRiskTerms = ["suicide", "self-harm", "abuse", "violence", "unsafe"];
    const distressTerms = ["abandoned", "despair", "ashamed", "afraid", "suffering", "silence"];

    if (highRiskTerms.some((term) => combinedText.includes(term))) {
      notes.push("High-risk pastoral language is present.");
      return {
        level: "high",
        notes
      };
    }

    if (distressTerms.some((term) => combinedText.includes(term))) {
      notes.push("Distress language is present; composer should be careful and non-triumphalistic.");
      return {
        level: "moderate",
        notes
      };
    }

    notes.push("No obvious high-risk pastoral language detected.");
    return {
      level: "low",
      notes
    };
  }

  function buildComposerHints(evaluation) {
    const hints = [
      "Keep final prose outside Divine Core.",
      "Preserve caveats where scores are below 70."
    ];

    if (evaluation.pastoralRisk.level !== "low") {
      hints.push("Use especially gentle, non-accusatory pastoral language.");
    }

    if (evaluation.noveltyAssessment.level === "speculative") {
      hints.push("Do not present the pattern as doctrinally established.");
    }

    if (evaluation.scriptureCoverage.score < 70) {
      hints.push("Ask the composer to request or supply stronger Scripture grounding.");
    }

    return hints;
  }

  function evaluateReasoningContext(reasoningContext) {
    const evaluation = {
      scriptureCoverage: scoreScriptureCoverage(reasoningContext || {}),
      doctrinalConsistency: scoreDoctrinalConsistency(reasoningContext || {}),
      ecclesialSupport: scoreEcclesialSupport(reasoningContext || {}),
      theologicalBalance: scoreTheologicalBalance(reasoningContext || {}),
      noveltyAssessment: assessNovelty(reasoningContext || {}),
      pastoralRisk: assessPastoralRisk(reasoningContext || {}),
      recommendedComposerHints: []
    };

    evaluation.recommendedComposerHints = buildComposerHints(evaluation);

    return evaluation;
  }

  const api = Object.freeze({
    evaluateReasoningContext
  });

  globalScope.DivineReasoningEvaluationEngine = api;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window);
