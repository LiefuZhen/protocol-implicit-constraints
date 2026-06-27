# protocol-implicit-constraints

This repository supports **protocol implicit constraint research** for the project:

> Security Between the Lines: CVE-driven implicit constraint generation for protocol compliance bug detection.

The repository is not a public vulnerability database. It is a research workspace for collecting protocol-related CVE evidence, identifying implicit standard constraints, abstracting constraint-generation directions, and preparing later implementation validation.

## Research Workflow

The current workflow is:

1. **CVE collection**: collect protocol-related CVEs, advisories, patches, issues, and PoC references.
2. **Implicit violation filtering**: decide whether a CVE is related to standard compliance and whether the violated constraint is explicit or implicit.
3. **CVE abduction**: analyze why the bug could happen and where the standard is silent, ambiguous, underspecified, or internally inconsistent.
4. **Direction generation**: abstract recurring abduction patterns into constraint-generation directions.
5. **Candidate constraint generation**: apply the directions to target standards and generate candidate implicit constraints before implementation checking.
6. **Implementation validation**: compare candidate constraints against implementations, then use cross-implementation validation, manual adjudication, and PoC walkthroughs.

## Pilot Protocols

The current T1 pilot protocols are:

- **MQTT**: first pilot and ProtocolGuard motivation case; OASIS/ISO rather than IETF RFC.
- **CoAP**: first RFC-based pilot; moderate complexity and IoT-oriented.
- **DNS**: high-value RFC backup; should initially be scoped to message parsing, compression pointers, label length, or cache boundaries.

## Safety And Disclosure

Keep the GitHub repository **private by default**. Do not upload undisclosed PoCs, exploit code, private vulnerability details, vendor-sensitive notes, or reproduction steps that could enable abuse. Use placeholders until disclosure status is clear.

## Directory Layout

| Path | Purpose |
|---|---|
| `docs/` | Survey, workflow, and terminology documents. |
| `schema/` | JSON field templates for CVE records, implementations, protocol profiles, candidate constraints, and seed direction examples. |
| `prompts/` | Prompt templates for CVE abduction, direction abstraction, and constraint generation. |
| `protocols/` | Per-protocol workspace for standards, CVEs, implementations, constraints, and notes. |
| `examples/` | Minimal example JSON records that follow the templates. |
| `scripts/` | Utility scripts, including JSON validation. |
| `review/` | Meeting notes and review records. |

## JSON Validation

Run:

```bash
python scripts/validate_json.py
```

On Windows PowerShell, if `python` is not on PATH, use the bundled runtime or your local Python installation.
