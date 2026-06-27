# Implicit Constraint Types And Generation Directions

This document is a **working seed taxonomy** for T1/T6. Per the research design, the final direction set should be derived from reviewed CVE abduction in T3. These seed directions are useful for bootstrapping T2/T7 and for writing consistent JSON records.

## Direction Matrix

| Direction ID | Chinese name | Where to look in the standard | Reverse-inference question | Typical bug shape | False-positive risk |
|---|---|---|---|---|---|
| `boundary_silence` | 边界沉默 / 欠定义 | Normal cases are specified, malformed/extreme/invalid cases are not. | If the abnormal case is accepted, which protocol goal breaks? | oversized length, malformed first packet, invalid option encoding, pointer out of bounds | Some standards intentionally leave error handling to implementations. |
| `purpose_mechanism_gap` | 目的与机制脱节 | A field's purpose is stated, but required implementation behavior is incomplete. | What minimum behavior is required to preserve the stated purpose? | identifier truncation, request-response mismatch, cache poisoning | The purpose may be advisory unless tied to explicit protocol semantics. |
| `cross_reference_conflict` | 前后矛盾 / 交叉引用不一致 | Same field/state is described in multiple sections with inconsistent limits or meanings. | Which interpretation preserves safety/interoperability? | parser accepts one section's boundary but violates another | Could be standard ambiguity rather than implementation defect. |
| `ambiguous_capability_scope` | 能力/范围声明含糊 | Standard says MAY allow/support but does not define support extent. | If partial support is allowed, what behavior must still not happen? | silent truncation, half-supported options, unsupported extension treated as valid | MAY language can make hard defect claims weaker. |
| `state_consistency` | 状态一致性 | Message sequence, transaction ID, token, session, retransmission, or cache state. | What state relation must remain invariant across messages? | duplicate QoS 2 packet IDs leak state; ACK/RST matched to wrong endpoint | Requires dynamic context and cross-implementation validation. |
| `parser_unambiguity` | 解析无歧义 | Binary encodings, length fields, compression, nested encodings, CBOR/option parsing. | Can one byte sequence be interpreted in two incompatible ways? | DNS label byte treated as pointer; malformed CBOR read beyond buffer | Some cases are pure memory safety, not standard compliance. |
| `message_cardinality_consistency` | 字段数量一致性 | Request/response lists, reason-code arrays, option repetitions, counts. | Does the number of returned items match the triggering request or declared count? | SUBACK reason-code count mismatch | Need exact standard section for count relation. |
| `security_boundary_preservation` | 安全边界保持 | Cache, authority, bailiwick, origin, endpoint identity, OSCORE context. | What data must not cross trust boundaries? | DNS unsolicited RR cache injection; OSCORE context confusion | Often spread across RFCs/BCPs, not one sentence. |

## How To Use These Directions

1. Start from the protocol profile and standard sections.
2. Locate suspicious text or mechanisms using the direction matrix.
3. Generate a `candidate_constraint` record only when the constraint can bind to a protocol goal.
4. Mark strength:
   - `L1`: violation necessarily breaks the bound protocol goal;
   - `L2`: likely robustness/interoperability expectation.
5. Keep `status: candidate` until independent review.

## Examples

| Protocol | Direction | Candidate constraint |
|---|---|---|
| MQTT | `purpose_mechanism_gap` | Accepting long ClientIds must not silently truncate distinct client identities into one internal ID. |
| MQTT | `message_cardinality_consistency` | SUBACK reason-code count must be validated before callback code indexes it. |
| CoAP | `state_consistency` | Token and endpoint context must preserve request-response association. |
| DNS | `parser_unambiguity` | A compression pointer must resolve within packet bounds and must not form a loop. |
| DNS | `security_boundary_preservation` | Resolver cache must not accept forged out-of-bailiwick or unsolicited records as trusted data. |
