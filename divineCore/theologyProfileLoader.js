// Divine Core Phase 1.
// This browser-safe loader is intentionally small and standalone. Later phases
// can share it across Divine Pattern, Shepherd, Divine Scholar, Bible Study,
// and future tools without requiring Node-only filesystem APIs.

(function attachTheologyProfileLoader(globalScope) {
  const theologianProfilePaths = Object.freeze({
    augustine: "divineCore/theologians/augustine.json",
    aquinas: "divineCore/theologians/aquinas.json",
    luther: "divineCore/theologians/luther.json",
    calvin: "divineCore/theologians/calvin.json",
    hooker: "divineCore/theologians/hooker.json",
    barth: "divineCore/theologians/barth.json",
    lewis: "divineCore/theologians/lewis.json"
  });

  const creedProfilePaths = Object.freeze({
    niceneCreed: "divineCore/creeds/niceneCreed.json",
    apostlesCreed: "divineCore/creeds/apostlesCreed.json"
  });

  const fallbackProfile = Object.freeze({
    name: "Fallback Theological Wisdom Profile",
    tradition: "Shared Christian",
    era: "Phase 1 fallback",
    coreEmphases: ["Scripture", "orthodoxy", "charity", "humility"],
    likelyAffirmations: [
      "Christian reasoning should be tested by Scripture and the received faith of the Church.",
      "Pastoral application should hold truth and mercy together."
    ],
    likelyConcerns: [
      "overclaiming beyond the evidence",
      "detaching discernment from Scripture, prayer, and Christian community"
    ],
    discernmentQuestions: [
      "What does Scripture most clearly affirm here?",
      "Does this fit historic Christian confession?",
      "What pastoral fruit is likely to follow?"
    ],
    scriptureEmphases: ["2 Timothy 3:16-17", "John 1:14", "1 Corinthians 13"],
    pastoralWarnings: [
      "Use caution where context is thin.",
      "Prefer humble guidance over certainty that has not been tested."
    ]
  });

  function cloneProfile(profile) {
    return JSON.parse(JSON.stringify(profile));
  }

  function getFallbackProfile(overrides) {
    return Object.assign(cloneProfile(fallbackProfile), overrides || {});
  }

  async function loadProfile(path, options) {
    const fetcher = options && options.fetcher ? options.fetcher : globalScope.fetch;

    if (typeof fetcher !== "function") {
      return getFallbackProfile({
        loadError: "Fetch is unavailable in this runtime.",
        requestedPath: path
      });
    }

    try {
      const response = await fetcher(path);

      if (!response || !response.ok) {
        return getFallbackProfile({
          loadError: "Profile request failed.",
          requestedPath: path,
          status: response ? response.status : undefined
        });
      }

      return await response.json();
    } catch (error) {
      return getFallbackProfile({
        loadError: error && error.message ? error.message : "Profile loading failed.",
        requestedPath: path
      });
    }
  }

  async function loadProfiles(paths, options) {
    const entries = Object.entries(paths || {});
    const loadedProfiles = await Promise.all(
      entries.map(async ([key, path]) => [key, await loadProfile(path, options)])
    );

    return Object.fromEntries(loadedProfiles);
  }

  const api = Object.freeze({
    theologianProfilePaths,
    creedProfilePaths,
    getFallbackProfile,
    loadProfile,
    loadProfiles
  });

  globalScope.DivineTheologyProfileLoader = api;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window);
