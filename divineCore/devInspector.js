// Divine Core Phase 3 developer inspector.
// This tool is for local developer inspection only. Divine Core reasons only;
// it must not write final user-facing prose. Shepherd, Book Report, Scholar,
// Bible Study, and future apps should use their own composers later.

(function attachDivineCoreDevInspector(globalScope) {
  const sampleInputs = [
    {
      label: "I feel abandoned by God.",
      input: {
        pattern: {
          title: "I feel abandoned by God.",
          summary: "A distress pattern where suffering or silence is interpreted as divine absence.",
          signals: ["lament", "fear", "need for mercy"]
        },
        scriptureThemes: ["Fall", "Christ", "New Creation"],
        userQuestion: "I feel abandoned by God.",
        selectedVoices: ["lutheran", "augustine", "lewis"]
      }
    },
    {
      label: "Sacrifice often comes before transformation.",
      input: {
        pattern: {
          title: "Sacrifice often comes before transformation.",
          summary: "A pattern relating costly surrender, obedience, and later renewal.",
          signals: ["sacrifice", "obedience", "transformation"]
        },
        scriptureThemes: ["Christ", "Covenant", "New Creation"],
        userQuestion: "Sacrifice often comes before transformation.",
        selectedVoices: ["nicaea", "reformed", "barth"]
      }
    },
    {
      label: "How does creation reveal order and meaning?",
      input: {
        pattern: {
          title: "Creation, order, and meaning",
          summary: "A question about created order, wisdom, intelligibility, and divine meaning.",
          signals: ["creation", "order", "meaning"]
        },
        scriptureThemes: ["Creation", "Covenant", "Christ"],
        userQuestion: "How does creation reveal order and meaning?",
        selectedVoices: ["anglican", "aquinas", "hooker"]
      }
    }
  ];

  function getReasoningCore() {
    return globalScope.DivineReasoningCore || {};
  }

  function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
      element.textContent = value;
    }
  }

  function renderTrace(trace) {
    const traceList = document.getElementById("trace-list");

    if (!traceList) {
      return;
    }

    traceList.innerHTML = "";

    [
      ["Layers", (trace.layersUsed || []).join(", ")],
      ["Selected voices", (trace.selectedVoices || []).join(", ") || "none"],
      ["Challenge layer", trace.challengeLayerTriggered ? "triggered" : "not triggered"]
    ].forEach(([label, value]) => {
      const item = document.createElement("li");
      item.textContent = label + ": " + value;
      traceList.appendChild(item);
    });
  }

  function renderOutput(context) {
    const trace = context.reasoningTrace || {};

    setText("next-layer", context.nextRecommendedLayer || "none");
    setText("confidence-summary", trace.confidenceSummary || "No confidence summary.");
    setText("composer-safe", trace.composerSafe ? "true" : "false");
    renderTrace(trace);
    setText("json-output", JSON.stringify(context, null, 2));
  }

  function runSample(sample, selectedButton) {
    const core = getReasoningCore();

    if (typeof core.buildDivineReasoningContext !== "function") {
      setText("json-output", "DivineReasoningCore.buildDivineReasoningContext is unavailable.");
      return;
    }

    document.querySelectorAll("#sample-list button").forEach((button) => {
      button.setAttribute("aria-pressed", button === selectedButton ? "true" : "false");
    });

    renderOutput(core.buildDivineReasoningContext(sample.input));
  }

  function renderSamples() {
    const sampleList = document.getElementById("sample-list");

    if (!sampleList) {
      return;
    }

    sampleInputs.forEach((sample, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = sample.label;
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", () => runSample(sample, button));
      sampleList.appendChild(button);

      if (index === 0) {
        runSample(sample, button);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", renderSamples);

  globalScope.DivineCoreDevInspector = Object.freeze({
    sampleInputs
  });
})(typeof globalThis !== "undefined" ? globalThis : window);
