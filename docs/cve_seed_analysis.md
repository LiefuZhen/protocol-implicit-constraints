# CVE And Advisory Seed Analysis

This file expands the T1 survey into T2-ready seed material. It does **not** claim that every CVE below is already an implicit-constraint violation. Each item is a candidate that needs T2 review against standard text, patch, root cause, and implementation behavior.

## Evidence Sources Used

| Source | Use |
|---|---|
| NVD CVE pages | Public vulnerability descriptions, affected versions, references, CWE labels, CVSS. |
| RFC Editor / IETF Datatracker | Stable protocol standard text and download locations. |
| OASIS MQTT specifications | MQTT standard text for MQTT 3.1.1/5.0. |
| Local ProtocolGuard paper PDF | Motivation example and baseline method: rule extraction, static slicing, assertion/fuzzing validation. |

## Summary Table

| Seed | Protocol | Implementation | Public source | Mechanism | Likely direction | Current T2 status |
|---|---|---|---|---|---|---|
| ProtocolGuard ClientId example | MQTT | Sol | ProtocolGuard paper DOI: https://dx.doi.org/10.14722/ndss.2026.240521 | CONNECT ClientId | `purpose_mechanism_gap`, `ambiguous_capability_scope` | Strong seed |
| CVE-2023-0809 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2023-0809 | Non-CONNECT initial packet | `boundary_silence` | Candidate |
| CVE-2023-28366 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2023-28366 | QoS 2 duplicate message IDs | `state_consistency` | Candidate |
| CVE-2021-34431 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2021-34431 | Crafted MQTT v5 CONNECT | `boundary_silence`, `parser_unambiguity` | Candidate |
| CVE-2024-10525 | MQTT | libmosquitto | https://nvd.nist.gov/vuln/detail/CVE-2024-10525 | SUBACK without reason codes | `message_cardinality_consistency` | Strong seed |
| CVE-2025-34468 | CoAP | libcoap | https://nvd.nist.gov/vuln/detail/CVE-2025-34468 | Proxy hostname/address resolution | `boundary_silence` | Weak protocol-compliance seed |
| CVE-2026-29013 | CoAP | libcoap | https://nvd.nist.gov/vuln/detail/CVE-2026-29013 | OSCORE CBOR unwrap parsing | `parser_unambiguity` | Candidate |
| CVE-2025-40778 | DNS | BIND 9 | https://nvd.nist.gov/vuln/detail/CVE-2025-40778 | Answer acceptance/cache injection | `security_boundary_preservation` | Strong seed |
| RFC 9267 anti-pattern examples | DNS | Multiple | https://www.rfc-editor.org/rfc/rfc9267.txt | compression pointer, label length, record count | `parser_unambiguity`, `boundary_silence` | Direction seed |

## MQTT Detailed Seeds

### ProtocolGuard ClientId Silent Truncation

The ProtocolGuard paper uses a Sol MQTT implementation example where an oversized ClientId is copied into a fixed-size buffer and silently truncated. MQTT 3.1.1 allows ClientIds between 1 and 23 UTF-8 bytes and permits servers to allow longer ClientIds. The implicit issue is that accepting a longer identifier cannot collapse distinct identities into the same internal client/session identity.

| Field | Analysis |
|---|---|
| Standard area | MQTT 3.1.1 Section 3.1.3.1 Client Identifier |
| Candidate implicit constraint | If a broker accepts an oversized ClientId, it must preserve the complete identifier or explicitly reject it; it must not silently truncate it into an identity collision. |
| Bound goal | Client identity uniqueness, session management, message routing. |
| Why implicit | The standard's MAY allowance for longer IDs does not spell out storage/normalization obligations, but the identifier purpose requires uniqueness preservation. |
| T2 action | Recheck MQTT text and Sol code; create a minimal non-exploit walkthrough comparing long ClientIds. |

### CVE-2023-0809: Mosquitto Initial Packet Resource Allocation

NVD describes Mosquitto before 2.0.16 allocating excessive memory based on malicious initial packets that are not CONNECT packets. This maps naturally to MQTT connection-state handling: the first client packet should establish protocol identity and session state; malformed initial packets should not drive unbounded allocation.

| Field | Analysis |
|---|---|
| Public description | Excessive allocation from malicious initial non-CONNECT packets. |
| Candidate standard area | MQTT CONNECT packet and fixed-header Remaining Length handling. |
| Candidate implicit constraint | Before allocating payload-sized state for a new connection, a broker must validate that the initial packet is a legal CONNECT packet and that its Remaining Length is acceptable for the connection phase. |
| Bound goal | Connection-state consistency and DoS resistance. |
| Explicit/implicit status | `unknown` until MQTT text and patch are reviewed; likely boundary-silence plus explicit first-packet semantics. |
| T2 action | Read Mosquitto 2.0.16 patch/release notes and determine whether the bug is protocol-state compliance or generic resource-throttling. |

### CVE-2023-28366: Mosquitto QoS 2 Duplicate Message ID Memory Leak

NVD describes a Mosquitto broker memory leak when clients send many QoS 2 messages with duplicate message IDs and fail to respond to PUBREC. The root cause includes EAGAIN mishandling, so it may be partly implementation/resource management rather than pure protocol compliance.

| Field | Analysis |
|---|---|
| Public description | Remote abuse through many QoS 2 messages with duplicate message IDs and missing PUBREC response. |
| Candidate standard area | MQTT QoS 2 packet identifier and PUBREC/PUBREL/PUBCOMP state. |
| Candidate implicit constraint | Duplicate QoS 2 Packet Identifiers and incomplete handshakes must not create unbounded duplicate state or leak state across retransmission/error paths. |
| Bound goal | Exactly-once delivery state consistency and resource lifecycle. |
| Explicit/implicit status | `unknown`; may become `ambiguous` because the NVD root cause mentions libc send EAGAIN. |
| T2 action | Inspect patch and advisory to separate protocol-state invariant from memory-management bug. |

### CVE-2021-34431: Mosquitto MQTT v5 Crafted CONNECT Memory Leak

NVD describes a memory leak when an authenticated MQTT v5 client sends a crafted CONNECT message to Mosquitto 1.6-2.0.10. This is a candidate for MQTT v5 property/CONNECT parser boundary review, but the current public summary is not enough to assert an implicit constraint.

| Field | Analysis |
|---|---|
| Public description | Authenticated MQTT v5 client sends crafted CONNECT; broker leaks memory; DoS possible. |
| Candidate standard area | MQTT 5.0 CONNECT properties and connection re-authentication/session transition. |
| Candidate implicit constraint | A second or malformed CONNECT in an authenticated/session context must be rejected or cleanly transition without leaking allocated parsing/session state. |
| Bound goal | Session lifecycle consistency and DoS resistance. |
| Explicit/implicit status | `unknown`; keep as seed only. |
| T2 action | Review Eclipse bug 573191 and patch to identify exact malformed field. |

### CVE-2024-10525: libmosquitto SUBACK Reason Code Cardinality

NVD describes libmosquitto clients making out-of-bounds memory access when a malicious broker sends a crafted SUBACK with no reason codes. This is a strong seed for field-cardinality consistency: a callback that reports subscription results must not assume reason codes exist unless the SUBACK payload actually contains them.

| Field | Analysis |
|---|---|
| Public description | Crafted SUBACK with no reason codes causes OOB access in `on_subscribe` callback. |
| Candidate standard area | MQTT 5.0 SUBACK packet payload / reason-code list; MQTT 3.1.1 SUBACK return codes. |
| Candidate implicit constraint | SUBACK reason-code/result cardinality must be validated against the subscription result list before callback indexing. |
| Bound goal | Request-response correspondence and memory-safe protocol parsing. |
| Why useful | This converts a memory-safety CVE into a protocol-structure hypothesis: count/list correspondence is the standard-side oracle to verify. |
| T2 action | Compare MQTT 3.1.1 and 5.0 SUBACK layouts; inspect patch `8ab20b4...`. |

## CoAP Detailed Seeds

### CVE-2025-34468: libcoap Proxy Hostname Stack Buffer Overflow

NVD describes a stack-based buffer overflow in libcoap address resolution when attacker-controlled hostname data is copied into a fixed 256-byte stack buffer, requiring proxy logic to be enabled. This may be weaker for protocol compliance because hostname resolution can be seen as application/API input rather than CoAP message semantics.

| Field | Analysis |
|---|---|
| Public description | Proxy hostname copied into fixed buffer without bounds check. |
| Candidate standard area | RFC 7252 proxy operation and Proxy-Uri / Uri-Host handling. |
| Candidate implicit constraint | Proxy URI/host input accepted from CoAP requests must be bounded or rejected before address-resolution storage. |
| Bound goal | Safe proxy request handling and parser/resource bounds. |
| T2 risk | Could be classified as generic memory safety, not standard compliance. |
| T2 action | Check whether the hostname comes from CoAP Proxy-Uri/Uri-Host options and whether RFC 7252 defines relevant option length/error behavior. |

### CVE-2026-29013: libcoap OSCORE CBOR Bounds

NVD describes out-of-bounds reads in libcoap OSCORE Appendix B.2 CBOR unwrap handling because `assert()` was used for bounds checking and removed in release builds. This is a good parser-boundary seed: release builds must enforce standard parser bounds, not rely on debug assertions.

| Field | Analysis |
|---|---|
| Public description | Malformed OSCORE options/responses during negotiation trigger CBOR parsing OOB read. |
| Candidate standard area | OSCORE option/CBOR unwrap handling used by CoAP security context negotiation. |
| Candidate implicit constraint | Malformed OSCORE/CBOR structures must be checked by runtime bounds validation in release builds before byte consumption or allocation-size computation. |
| Bound goal | Authenticated context negotiation and parser termination/safety. |
| T2 risk | Need OSCORE RFC section mapping, not only libcoap source. |
| T2 action | Add OSCORE RFC references and inspect commit `b7847c4...`. |

## DNS Detailed Seeds

### RFC 9267: DNS RR Processing Anti-Patterns

RFC 9267 is valuable because it explicitly bridges RFC 1035 DNS message rules to recurring implementation anti-patterns. It notes that RFC 1035's compression scheme can be misimplemented when parsers blindly follow offsets, allow pointer loops, or fail label/name length validation.

| Field | Analysis |
|---|---|
| Standard base | RFC 1035 Section 2.3.4 and Section 4.1.4. |
| Candidate implicit constraint | Compression pointers must resolve within packet bounds, point to valid prior name material, and must not form loops or cause expanded names beyond 255 octets. |
| Bound goal | DNS parser termination, unambiguous name decoding, DoS/RCE prevention. |
| Why useful | RFC 9267 provides a bridge from explicit RFC 1035 format text to implicit parser-safety obligations. |
| T2 action | Select one implementation pair and one malformed-packet class; do not try to cover all DNS resolver behavior. |

### CVE-2025-40778: BIND 9 Forged Data Cache Injection

NVD describes BIND being too lenient when accepting records from answers, allowing forged data to enter cache. This is a strong example of security-boundary preservation: a resolver should not treat unrequested or out-of-scope data as trusted cache material.

| Field | Analysis |
|---|---|
| Public description | Forged data can be injected into cache under certain answer-acceptance circumstances. |
| Candidate standard area | DNS answer processing, authority/additional sections, bailiwick/cache acceptance rules; likely requires RFC plus BCP/ISC advisory review. |
| Candidate implicit constraint | Resolver cache insertion must preserve bailiwick/request relevance and must not accept extraneous untrusted answer records as trusted cache data. |
| Bound goal | Cache integrity and poisoning resistance. |
| Explicit/implicit status | Likely implicit/mixed because cache security boundary spans RFC semantics and resolver policy. |
| T2 action | Read ISC advisory and determine exact acceptance rule; map to RFC/BCP sections before using as oracle. |
