# Data Format Convention

This file defines how the repository should record T1/T2/T3/T7 artifacts. The JSON files are intentionally **field templates**, not strict JSON Schema Draft files. The goal is to make records consistent enough for manual review, later scripts, and LLM-assisted analysis.

## File Placement

| Record type | Location | Example |
|---|---|---|
| Protocol profile | `protocols/<protocol>/protocol_profile.json` | `protocols/mqtt/protocol_profile.json` |
| Implementation | `protocols/<protocol>/implementations/<impl_id>.json` | `protocols/mqtt/implementations/mosquitto.json` |
| CVE/advisory seed | `protocols/<protocol>/cves/<cve_id>.json` | `protocols/mqtt/cves/CVE-2024-10525.json` |
| Candidate constraint | `protocols/<protocol>/constraints/<constraint_id>.json` | `protocols/dns/constraints/DNS-IC-0001.json` |
| Direction seed/final direction set | `schema/directions.example.json` or later `directions/*.json` | Seed examples only for now |

## `cve_record` Semantics

`cve_record` is used in T2. It records a vulnerability seed and the current hypothesis about whether it is protocol-related and whether it involves an implicit constraint.

| Field | Meaning | Required review discipline |
|---|---|---|
| `cve_id` | CVE ID or stable advisory ID. | Use real CVE ID when available; use `ADVISORY-...` only for non-CVE sources. |
| `protocol_id` | Short protocol key. | Must match protocol folder name. |
| `implementation` | Affected implementation or library. | Use the implementation record ID when possible. |
| `affected_versions` | Known affected versions from NVD/vendor. | Keep source-derived; do not guess. |
| `summary` | Short vulnerability summary. | Paraphrase from public sources; do not include exploit steps. |
| `related_message_or_field` | Protocol mechanism involved. | Examples: `CONNECT.ClientId`, `SUBACK.reason_codes`, `DNS.compression_pointer`. |
| `related_standard_refs` | Standard sections that may govern the behavior. | If uncertain, write candidate sections and explain in notes. |
| `classification.is_protocol_related` | Whether the behavior is tied to protocol parsing/state/semantics. | `true` can still be out of scope if it is only generic memory safety. |
| `classification.is_standard_compliance_related` | `yes`, `no`, or `unknown`. | Keep `unknown` until standard text and patch align. |
| `classification.explicit_or_implicit` | `explicit`, `implicit`, `ambiguous`, `unknown`, or `out_of_scope`. | Do not force a decision in T1. |
| `implicit_constraint_hypothesis` | Candidate abduction result. | This is a hypothesis, not a final finding. |
| `evidence` | NVD/vendor/patch/PoC links. | Avoid storing undisclosed PoC details. |
| `review_status` | `unreviewed`, `triaged`, `accepted_seed`, `rejected`, `needs_more_evidence`. | Use `accepted_seed` only after T2 review. |

## `candidate_constraint` Semantics

`candidate_constraint` is used in T7. It records an implicit or explicit candidate before implementation validation.

| Field | Meaning | Example |
|---|---|---|
| `id` | Stable local ID. | `MQTT-IC-0004` |
| `protocol_id` | Protocol key. | `mqtt` |
| `source_type` | `implicit`, `explicit`, or `mixed`. | `implicit` |
| `direction.direction_id` | Generation direction. | `purpose_mechanism_gap` |
| `spec_ref` | Standard, section, entity, and quote/summary. | MQTT 5.0 SUBACK payload |
| `statement` | Natural-language constraint. | Reason-code count must match subscription count before callback access. |
| `condition` | When the constraint applies. | Client receives SUBACK from broker. |
| `expected_behavior` | Behavior that would satisfy the constraint. | Validate count before indexing. |
| `violation_pattern` | What a violating implementation looks like. | Reads reason code beyond available payload. |
| `bound_goal` | Protocol goal that makes the constraint meaningful. | Request-response field correspondence. |
| `strength` | `L1` logical necessity or `L2` convention/best practice. | `L1` |
| `status` | `candidate`, `under_review`, `accepted`, `rejected`, `validated`, `ambiguous_spec`. | `candidate` |
| `related_cves` | Evidence seeds connected to the constraint. | `["CVE-2024-10525"]` |
| `related_implementations` | Implementations relevant for validation. | `["mosquitto", "nanomq"]` |

## Strength Rules

| Strength | Meaning | Can it support a defect claim alone? |
|---|---|---|
| `L1` | Logically necessary to preserve a stated protocol goal. | Yes, after independent review and validation. |
| `L2` | Best practice, robustness expectation, or likely interoperability rule. | No; record as suspicious or advisory unless stronger evidence appears. |

## Review Status Rules

| Status | Meaning |
|---|---|
| `candidate` | Generated or hand-seeded, not reviewed. |
| `under_review` | Standard text, patch, and implementation behavior are being checked. |
| `accepted` | Constraint is considered a valid standard-side oracle. |
| `validated` | At least one implementation violation is supported by validation evidence. |
| `ambiguous_spec` | The standard itself is unclear enough that this should be reported as ambiguity, not an implementation bug. |
| `rejected` | Constraint was wrong, too weak, or out of scope. |

## Minimal Creation Workflow

1. Copy the matching template from `schema/`.
2. Fill source URLs and standard references first.
3. Keep `review_status` as `unreviewed` or `candidate`.
4. Run JSON validation.
5. Only after T2/T7 review, change status fields.

```powershell
Copy-Item schema\cve_record.schema.json protocols\mqtt\cves\CVE-XXXX-XXXX.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```
