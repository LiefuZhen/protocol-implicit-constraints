# Project Workflow

This workflow follows the research plan in `方案设计.md`: use CVE evidence to derive generation directions, then apply those directions to standards before implementation validation.

## Task Dependency Graph From PPT

The final PPT image makes T1 and T6 the upstream work for later tasks:

| Task | What to do | Deliverable | Estimate | Depends on |
|---|---|---|---|---|
| T1 | List verifiable RFC/protocol standards and pick 2-3 pilots. | Candidate protocol list and recommended pilots. | 2.0d | - |
| T6 | Build repository and define candidate-constraint data format. | Repository, example JSON, README. | 0.5d | - |
| T2 | Pull CVEs, filter explicit violations, review and classify. | Vulnerability count, implicit-CVE list with shape, kappa if double labeled. | 2.0d | T1, T6 |
| T3 | Abstract implicit CVE causes into generation directions. | Direction set v0 and feasibility argument. | 1.5d | T2 |
| T7 | Write direction prompt and generate RFC candidate constraints. | Prompt v0, candidate constraints, manual review. | 1.0d | T3, T6 |
| T4 | Find 2-3 independent implementations and trace one input. | Candidate implementations and build notes. | 2.0d | T1 |
| T5 | Manually inspect one known CVE through detection, cross-impl, and PoC. | End-to-end walkthrough. | 1.5d | T4 |

This repository therefore does more than store templates. T1/T6 must already provide:

- verifiable standard/RFC links;
- concrete candidate CVE records;
- seed implicit-constraint hypotheses;
- candidate-constraint JSON records;
- implementation records for later T4/T5;
- safety rules for private handling of PoC and undisclosed details.

## T1 Protocol Survey

Goal: identify 2-3 pilot protocols with public standards, available implementations, enough CVE/advisory material, and realistic validation paths.

Output:

- `docs/protocol_survey.md`
- `docs/cve_seed_analysis.md`
- `docs/implicit_constraint_types.md`
- protocol profiles under `protocols/<protocol>/`
- initial implementation and CVE candidates

## T2 CVE Filtering

Goal: collect CVEs and decide whether they are protocol-related, standard-compliance-related, and explicit or implicit.

Filtering steps:

1. Locate the affected protocol mechanism, message, field, or state.
2. Map the bug to relevant standard text.
3. Decide whether a clear explicit rule directly covers the behavior.
4. Keep cases where the root cause appears to involve silence, ambiguity, conflict, or purpose-mechanism gaps.

Output:

- reviewed CVE JSON records
- evidence links to NVD, advisories, patches, and issues
- notes explaining why each case is kept or rejected
- optional double-labeling result such as Cohen's kappa if two reviewers classify a sample

## T3 Direction Abstraction

Goal: abduct from filtered CVEs and cluster recurring standard-defect patterns into constraint-generation directions.

Output:

- reviewed direction records
- seed prompt for later constraint generation
- mapping from CVE evidence to directions

## T7 Constraint Generation Trial

Goal: apply seed directions to target standards and generate candidate implicit constraints before implementation checking.

Output:

- candidate constraints under `protocols/<protocol>/constraints/`
- direction-to-standard traceability
- independent review notes for constraint correctness

## T4 Implementation Preparation

Goal: lock implementation targets and record build/run/test-input methods.

Output:

- implementation records under `protocols/<protocol>/implementations/`
- version pins and reproducibility notes
- input construction plan

## T5 Validation Walkthrough

Goal: validate candidates through spec-vs-implementation analysis, cross-implementation comparison, manual adjudication, and PoC walkthrough where disclosure-safe.

Output:

- validation notes
- confirmed/non-confirmed candidate status
- safe reproduction summaries
- disclosure-sensitive PoC details kept out of public/private GitHub unless explicitly approved
