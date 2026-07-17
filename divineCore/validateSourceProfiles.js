// Dependency-free structural and semantic validation for versioned Divine Core
// source profiles. Human review is stewardship metadata and never affects the
// derived maturity calculation or reasoning eligibility.

const fs = require("fs");
const path = require("path");
const {
  AUTHORITY_BOUNDARY,
  GOVERNING_PRINCIPLE
} = require("./createDailySourceDraft.js");

const MATURITY_ORDER = ["scaffold", "developing", "evidence-ready", "evaluated"];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function resolveRef(rootSchema, ref) {
  if (!ref.startsWith("#/")) {
    throw new Error("Only local JSON Schema references are supported: " + ref);
  }

  return ref.slice(2).split("/").reduce((value, segment) => {
    const decoded = segment.replace(/~1/g, "/").replace(/~0/g, "~");
    return value && value[decoded];
  }, rootSchema);
}

function valueType(value) {
  if (Array.isArray(value)) return "array";
  if (value === null) return "null";
  return typeof value;
}

function validateAgainstSchema(value, schema, rootSchema, location = "$") {
  const errors = [];
  const activeSchema = schema.$ref ? resolveRef(rootSchema, schema.$ref) : schema;

  if (!activeSchema) {
    return [location + ": unresolved schema reference"];
  }

  if (Object.prototype.hasOwnProperty.call(activeSchema, "const") && value !== activeSchema.const) {
    errors.push(location + ": must equal " + JSON.stringify(activeSchema.const));
  }

  if (activeSchema.enum && !activeSchema.enum.includes(value)) {
    errors.push(location + ": must be one of " + activeSchema.enum.join(", "));
  }

  if (activeSchema.type && valueType(value) !== activeSchema.type) {
    errors.push(location + ": expected " + activeSchema.type + ", received " + valueType(value));
    return errors;
  }

  if (activeSchema.type === "string" && activeSchema.minLength && value.length < activeSchema.minLength) {
    errors.push(location + ": must contain at least " + activeSchema.minLength + " character(s)");
  }

  if (activeSchema.type === "array") {
    value.forEach((item, index) => {
      errors.push(...validateAgainstSchema(item, activeSchema.items || {}, rootSchema, location + "[" + index + "]"));
    });
  }

  if (activeSchema.type === "object") {
    for (const required of activeSchema.required || []) {
      if (!Object.prototype.hasOwnProperty.call(value, required)) {
        errors.push(location + ": missing required property " + required);
      }
    }

    for (const [key, child] of Object.entries(value)) {
      const propertySchema = activeSchema.properties && activeSchema.properties[key];
      if (propertySchema) {
        errors.push(...validateAgainstSchema(child, propertySchema, rootSchema, location + "." + key));
      } else if (activeSchema.additionalProperties === false) {
        errors.push(location + ": unexpected property " + key);
      }
    }
  }

  return errors;
}

function isSubstantiveString(value) {
  if (typeof value !== "string") return false;
  const normalized = value.trim();
  if (!normalized) return false;
  return !(
    /^draft prompt:/i.test(normalized) ||
    /^placeholder\b/i.test(normalized) ||
    /^\[.*(?:placeholder|work title|author|scope|reference|location|theme|reading|tension|claim).*[\]]$/i.test(normalized) ||
    /^(todo|tbd|unknown|not yet reviewed)$/i.test(normalized)
  );
}

function hasSubstantiveArray(values) {
  return Array.isArray(values) && values.some(isSubstantiveString);
}

function isSubstantiveObservation(observation) {
  return observation &&
    isSubstantiveString(observation.observation) &&
    hasSubstantiveArray(observation.sourceLocations) &&
    isSubstantiveString(observation.evidenceNote);
}

function isSubstantiveScriptureEntry(entry) {
  return entry &&
    isSubstantiveString(entry.reference) &&
    isSubstantiveString(entry.note);
}

function hasDevelopingContent(profile) {
  const synthesis = profile.interpretiveSynthesis;
  const assessment = profile.divineCoreAssessment;
  const evaluation = profile.scripturalDoctrinalEvaluation;
  const provenance = profile.provenanceAndReview;

  return profile.sourceObservations.some((item) =>
    isSubstantiveString(item.observation) ||
    hasSubstantiveArray(item.sourceLocations) ||
    isSubstantiveString(item.evidenceNote)
  ) ||
    isSubstantiveString(synthesis.summary) ||
    [synthesis.emergingThemes, synthesis.ambiguities, synthesis.alternateReadings, synthesis.counterevidence].some(hasSubstantiveArray) ||
    isSubstantiveString(assessment.summary) ||
    [assessment.potentialContributions, assessment.theologicalCautions, assessment.unresolvedTensions].some(hasSubstantiveArray) ||
    evaluation.scripture.some((entry) => isSubstantiveString(entry.reference) || isSubstantiveString(entry.note)) ||
    [evaluation.canonicalTensions, evaluation.doctrinalAgreements, evaluation.neededQualifications, evaluation.possibleConflicts].some(hasSubstantiveArray) ||
    [provenance.scope, provenance.edition, provenance.translator, provenance.publisher, provenance.publicationYear].some(isSubstantiveString) ||
    hasSubstantiveArray(provenance.sourceLocationsReviewed) ||
    hasSubstantiveArray(provenance.evidenceNotes) ||
    provenance.originalSourceChecked === true;
}

function supportsEvidenceReady(profile) {
  const synthesis = profile.interpretiveSynthesis;
  const evaluation = profile.scripturalDoctrinalEvaluation;
  const provenance = profile.provenanceAndReview;
  const observationsReady = profile.sourceObservations.length > 0 &&
    profile.sourceObservations.every(isSubstantiveObservation);
  const ambiguityVisible = [synthesis.ambiguities, synthesis.alternateReadings, synthesis.counterevidence]
    .some(hasSubstantiveArray);
  const evaluationVisible = [evaluation.canonicalTensions, evaluation.doctrinalAgreements, evaluation.neededQualifications, evaluation.possibleConflicts]
    .some(hasSubstantiveArray);

  return provenance.originalSourceChecked === true &&
    isSubstantiveString(provenance.scope) &&
    hasSubstantiveArray(provenance.sourceLocationsReviewed) &&
    hasSubstantiveArray(provenance.evidenceNotes) &&
    observationsReady &&
    isSubstantiveString(synthesis.summary) &&
    ambiguityVisible &&
    evaluation.scripture.length > 0 &&
    evaluation.scripture.every(isSubstantiveScriptureEntry) &&
    evaluationVisible;
}

function supportsEvaluated(profile) {
  const assessment = profile.divineCoreAssessment;
  return supportsEvidenceReady(profile) &&
    isSubstantiveString(assessment.summary) &&
    hasSubstantiveArray(assessment.potentialContributions) &&
    hasSubstantiveArray(assessment.theologicalCautions) &&
    hasSubstantiveArray(assessment.unresolvedTensions);
}

function deriveMaturity(profile) {
  if (supportsEvaluated(profile)) return "evaluated";
  if (supportsEvidenceReady(profile)) return "evidence-ready";
  if (hasDevelopingContent(profile)) return "developing";
  return "scaffold";
}

function validateHumanReview(humanReview) {
  const errors = [];
  const hasReviewers = hasSubstantiveArray(humanReview.reviewers);
  const hasComments = hasSubstantiveArray(humanReview.reviewerComments);
  const hasReviewedAt = isSubstantiveString(humanReview.reviewedAt);
  const isoTimestamp = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/;
  const validTimestamp = hasReviewedAt &&
    isoTimestamp.test(humanReview.reviewedAt) &&
    !Number.isNaN(Date.parse(humanReview.reviewedAt));

  if (humanReview.status === "not-reviewed") {
    if (humanReview.reviewers.length || humanReview.reviewerComments.length || humanReview.reviewedAt !== "") {
      errors.push("humanReview not-reviewed metadata must have empty reviewers, reviewerComments, and reviewedAt");
    }
  } else {
    if (!hasReviewers) errors.push("humanReview reviewed states require at least one reviewer");
    if (!validTimestamp) errors.push("humanReview reviewed states require a valid ISO 8601 reviewedAt timestamp");
    if (humanReview.status === "reviewed-with-concerns" && !hasComments) {
      errors.push("humanReview reviewed-with-concerns requires at least one reviewer comment");
    }
  }

  return errors;
}

function validateSemanticProfile(profile) {
  const errors = [];
  const warnings = [];

  if (profile.divineCoreAssessment.authorityBoundary !== AUTHORITY_BOUNDARY) {
    errors.push("divineCoreAssessment.authorityBoundary must match the approved stable authority text");
  }
  if (profile.scripturalDoctrinalEvaluation.governingPrinciple !== GOVERNING_PRINCIPLE) {
    errors.push("scripturalDoctrinalEvaluation.governingPrinciple must match the approved stable governing principle");
  }

  errors.push(...validateHumanReview(profile.provenanceAndReview.humanReview));

  const derivedMaturity = deriveMaturity(profile);
  const storedRank = MATURITY_ORDER.indexOf(profile.profileMaturity);
  const derivedRank = MATURITY_ORDER.indexOf(derivedMaturity);
  if (storedRank > derivedRank) {
    errors.push("profileMaturity " + profile.profileMaturity + " overstates derived maturity " + derivedMaturity);
  } else if (storedRank < derivedRank) {
    warnings.push("profileMaturity " + profile.profileMaturity + " conservatively understates derived maturity " + derivedMaturity);
  }

  return { errors, warnings, derivedMaturity };
}

function validateProfile(profile, schema) {
  const structuralErrors = validateAgainstSchema(profile, schema, schema);
  if (structuralErrors.length) {
    return { errors: structuralErrors, warnings: [], derivedMaturity: null };
  }
  return validateSemanticProfile(profile);
}

function findVersionedProfiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
    .map((entry) => path.join(directory, entry.name))
    .filter((filePath) => {
      const profile = readJson(filePath);
      return profile.schemaVersion !== undefined || profile.profileType !== undefined;
    });
}

function validateAll(options = {}) {
  const divineCoreDir = options.divineCoreDir || __dirname;
  const schemaPath = options.schemaPath || path.join(divineCoreDir, "schemas", "source-profile.schema.json");
  const draftsDir = options.draftsDir || path.join(divineCoreDir, "drafts");
  const schema = readJson(schemaPath);
  const files = findVersionedProfiles(draftsDir);
  const results = files.map((filePath) => ({
    filePath,
    ...validateProfile(readJson(filePath), schema)
  }));
  return { schemaPath, files, results };
}

function runCli() {
  const report = validateAll();
  let failed = false;
  for (const result of report.results) {
    const label = path.relative(process.cwd(), result.filePath);
    result.warnings.forEach((warning) => console.warn("WARNING " + label + ": " + warning));
    result.errors.forEach((error) => {
      failed = true;
      console.error("ERROR " + label + ": " + error);
    });
    if (!result.errors.length) {
      console.log("PASS " + label + " (derived maturity: " + result.derivedMaturity + ")");
    }
  }
  if (!report.files.length) {
    console.log("PASS: no versioned source profiles found");
  }
  if (failed) process.exitCode = 1;
}

module.exports = {
  MATURITY_ORDER,
  deriveMaturity,
  isSubstantiveString,
  validateAgainstSchema,
  validateHumanReview,
  validateProfile,
  validateSemanticProfile,
  validateAll
};

if (require.main === module) {
  runCli();
}
