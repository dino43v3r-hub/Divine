const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const {
  AUTHORITY_BOUNDARY,
  GOVERNING_PRINCIPLE,
  buildDraftProfile,
  createNextDraft
} = require("./createDailySourceDraft.js");
const {
  deriveMaturity,
  validateProfile
} = require("./validateSourceProfiles.js");

const schema = JSON.parse(fs.readFileSync(path.join(__dirname, "schemas", "source-profile.schema.json"), "utf8"));
let passed = 0;

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function scaffold() {
  return buildDraftProfile({
    name: "Test Work",
    author: "Test Author",
    category: "test-category"
  });
}

function makeEvidenceReady(profile) {
  profile.sourceObservations = [{
    observation: "The reviewed scope presents a test observation.",
    sourceLocations: ["Test section 1"],
    evidenceNote: "This test note records an observation without endorsing it."
  }];
  profile.interpretiveSynthesis.summary = "The test observation may form a tentative relationship.";
  profile.interpretiveSynthesis.ambiguities = ["The test evidence permits more than one reading."];
  profile.scripturalDoctrinalEvaluation.scripture = [{
    reference: "Test canonical reference",
    relationship: "qualification",
    note: "The test reference qualifies the tentative relationship."
  }];
  profile.scripturalDoctrinalEvaluation.neededQualifications = ["A test qualification remains necessary."];
  profile.provenanceAndReview.scope = "Test scope only";
  profile.provenanceAndReview.sourceLocationsReviewed = ["Test section 1"];
  profile.provenanceAndReview.originalSourceChecked = true;
  profile.provenanceAndReview.evidenceNotes = ["Direct test-source inspection recorded for validator coverage."];
  return profile;
}

function makeEvaluated(profile) {
  makeEvidenceReady(profile);
  profile.divineCoreAssessment.summary = "The test assessment remains provisional and revisable.";
  profile.divineCoreAssessment.potentialContributions = ["A test contribution may warrant examination."];
  profile.divineCoreAssessment.theologicalCautions = ["Do not treat test content as doctrine."];
  profile.divineCoreAssessment.unresolvedTensions = ["A test tension remains unresolved."];
  return profile;
}

function run(name, test) {
  test();
  passed += 1;
  console.log("PASS " + name);
}

function expectValid(profile, maturity) {
  const result = validateProfile(profile, schema);
  assert.deepStrictEqual(result.errors, []);
  assert.strictEqual(result.derivedMaturity, maturity);
  return result;
}

run("valid scaffold", () => {
  const profile = scaffold();
  profile.profileMaturity = "scaffold";
  expectValid(profile, "scaffold");
});

run("valid developing profile", () => {
  const profile = scaffold();
  profile.profileMaturity = "developing";
  profile.interpretiveSynthesis.summary = "A tentative test synthesis exists but evidence remains incomplete.";
  expectValid(profile, "developing");
});

run("valid evidence-ready profile", () => {
  const profile = makeEvidenceReady(scaffold());
  profile.profileMaturity = "evidence-ready";
  expectValid(profile, "evidence-ready");
});

run("valid evaluated profile", () => {
  const profile = makeEvaluated(scaffold());
  profile.profileMaturity = "evaluated";
  expectValid(profile, "evaluated");
});

run("maturity overstatement failure", () => {
  const profile = scaffold();
  profile.profileMaturity = "developing";
  const result = validateProfile(profile, schema);
  assert(result.errors.some((error) => error.includes("overstates derived maturity scaffold")));
});

run("conservative understatement warning", () => {
  const profile = makeEvidenceReady(scaffold());
  profile.profileMaturity = "developing";
  const result = validateProfile(profile, schema);
  assert.deepStrictEqual(result.errors, []);
  assert(result.warnings.some((warning) => warning.includes("understates derived maturity evidence-ready")));
});

run("human review is independent of maturity", () => {
  const evaluated = makeEvaluated(scaffold());
  evaluated.profileMaturity = "evaluated";
  evaluated.provenanceAndReview.humanReview.status = "not-reviewed";
  expectValid(evaluated, "evaluated");

  const reviewedScaffold = scaffold();
  reviewedScaffold.provenanceAndReview.humanReview = {
    status: "reviewed",
    reviewers: ["Test Reviewer"],
    reviewerComments: [],
    reviewedAt: "2026-01-01T00:00:00Z"
  };
  assert.strictEqual(deriveMaturity(reviewedScaffold), "scaffold");
  expectValid(reviewedScaffold, "scaffold");
});

run("invalid human-review combinations", () => {
  const notReviewed = scaffold();
  notReviewed.provenanceAndReview.humanReview.reviewers = ["Unexpected Reviewer"];
  assert(validateProfile(notReviewed, schema).errors.some((error) => error.includes("must have empty")));

  const concerns = scaffold();
  concerns.provenanceAndReview.humanReview = {
    status: "reviewed-with-concerns",
    reviewers: ["Test Reviewer"],
    reviewerComments: [],
    reviewedAt: "2026-01-01T00:00:00Z"
  };
  assert(validateProfile(concerns, schema).errors.some((error) => error.includes("requires at least one reviewer comment")));
});

run("invalid source-observation types", () => {
  const profile = scaffold();
  profile.sourceObservations = "not-an-array";
  assert(validateProfile(profile, schema).errors.some((error) => error.includes("sourceObservations: expected array")));
});

run("invalid Scripture-entry types", () => {
  const profile = scaffold();
  profile.scripturalDoctrinalEvaluation.scripture = [{
    reference: "Test reference",
    relationship: "agreement",
    note: ["not-a-string"]
  }];
  assert(validateProfile(profile, schema).errors.some((error) => error.includes("note: expected string")));
});

run("stable authority-text enforcement", () => {
  const authority = scaffold();
  authority.divineCoreAssessment.authorityBoundary = "Changed authority text";
  assert(validateProfile(authority, schema).errors.some((error) => error.includes("approved stable authority text")));

  const governing = scaffold();
  governing.scripturalDoctrinalEvaluation.governingPrinciple = "Changed governing text";
  assert(validateProfile(governing, schema).errors.some((error) => error.includes("approved stable governing principle")));
  assert.strictEqual(scaffold().divineCoreAssessment.authorityBoundary, AUTHORITY_BOUNDARY);
  assert.strictEqual(scaffold().scripturalDoctrinalEvaluation.governingPrinciple, GOVERNING_PRINCIPLE);
});

run("generator output and queue preservation", () => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "divine-source-profile-"));
  try {
    fs.mkdirSync(path.join(tempDir, "drafts"));
    const originalQueue = {
      description: "Test queue",
      sources: [
        { name: "First Test Work", author: "First Test Author", category: "test", drafted: false, draftFile: "" },
        { name: "Second Test Work", author: "Second Test Author", category: "test", drafted: false, draftFile: "" }
      ]
    };
    fs.writeFileSync(path.join(tempDir, "sourceExpansionQueue.json"), JSON.stringify(originalQueue, null, 2) + "\n");
    createNextDraft(tempDir);

    const queue = JSON.parse(fs.readFileSync(path.join(tempDir, "sourceExpansionQueue.json"), "utf8"));
    assert.strictEqual(queue.sources.length, originalQueue.sources.length);
    assert.deepStrictEqual(queue.sources[1], originalQueue.sources[1]);
    assert.strictEqual(queue.sources[0].drafted, true);
    assert.strictEqual(queue.sources[0].draftFile, "divineCore/drafts/first-test-author-first-test-work.json");

    const generatedPath = path.join(tempDir, "drafts", "first-test-author-first-test-work.json");
    const generated = JSON.parse(fs.readFileSync(generatedPath, "utf8"));
    expectValid(generated, "scaffold");
    assert.deepStrictEqual(generated.sourceObservations, []);
    assert.deepStrictEqual(generated.scripturalDoctrinalEvaluation.scripture, []);
    assert.strictEqual(generated.provenanceAndReview.originalSourceChecked, false);
    assert.strictEqual(generated.provenanceAndReview.humanReview.status, "not-reviewed");
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
});

console.log("PASS: " + passed + " focused source-profile tests");
