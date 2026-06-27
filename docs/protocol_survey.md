# T1 Protocol Survey: RFC-Verifiable Pilots For Implicit Protocol Constraints

> Project: **Security Between the Lines** - CVE-driven constraint-generation directions for protocol implicit compliance bug detection.  
> Focus: choose 2-3 pilot protocols, list verifiable standards/RFCs and download locations, collect CVE/advisory seeds, and define experiment paths aligned with `方案设计.md` and the ProtocolGuard paper.

## 1. Survey Goal

T1 should produce protocols that can support the full research chain:

1. collect protocol-related CVEs and advisories;
2. filter cases caused by implicit constraint violations;
3. abduct why the standard allowed the bug to happen;
4. abstract constraint-generation directions;
5. apply those directions to protocol standards before implementation checking;
6. validate candidates with cross-implementation behavior, manual adjudication, and PoC walkthroughs.

The key idea inherited from `方案设计.md` is not to freely ask an LLM to "find hidden rules." Instead, we first derive **constraint-generation directions** from real CVE evidence, then use those directions to search the "between the lines" parts of a target standard: silence, ambiguity, conflict, and purpose-mechanism gaps.

## 2. Selection Criteria

| Dimension | Requirement | Why it matters |
|---|---|---|
| Public standard | Public RFC/OASIS/ISO text with stable HTML/TXT/PDF download. | Needed for `spec_ref` and reproducible standard alignment. |
| Open implementations | At least 2 independent implementations. | Needed for cross-implementation validation. |
| CVE/advisory material | CVEs, advisories, patches, or issues related to protocol behavior. | Needed for CVE abduction and direction abstraction. |
| Moderate complexity | Message structure can be understood and test inputs can be generated. | Avoids spending T1/T2 entirely on build and environment work. |
| Implicit constraint potential | Identifiers, lengths, parsing ambiguity, state matching, cache/security boundaries, or error handling. | These are likely places for "security between the lines." |
| Baseline relevance | Appears in or is comparable to ProtocolGuard/RFCAudit-style work. | Helps later related-work and baseline discussion. |

## 3. Terminology Table

| Term | Chinese | Short definition | Research use |
|---|---|---|---|
| protocol non-compliance bug | 协议合规缺陷 | Implementation behavior deviates from standard behavior or standard-implied protocol goals. | Main defect class. |
| explicit constraint | 显式约束 | Direct MUST/SHALL/range/format requirement in a standard. | Baseline extraction target. |
| implicit constraint | 隐式约束 | Requirement implied by protocol purpose, context, or consistency, but not directly stated as a strict rule. | Main research target. |
| constraint-generation direction | 约束生成方向 | CVE-derived instruction for where to look in a standard and how to infer a constraint. | Stage I artifact. |
| boundary silence | 边界沉默 | Normal path is specified, malformed/extreme cases are underspecified. | Seed direction. |
| purpose-mechanism gap | 目的与机制脱节 | Standard states a purpose but does not fully specify the mechanism needed to preserve it. | Seed direction. |
| cross-reference conflict | 交叉引用冲突 | Sections describe the same entity or behavior inconsistently. | Seed direction. |
| ambiguous capability scope | 含糊能力范围声明 | Standard says support/allow without defining support limits. | Seed direction. |
| cross-implementation validation | 跨实现验证 | Same candidate behavior/input is checked across independent implementations. | Candidate validation. |
| constraint-level precision | 约束层精确率 | Fraction of generated constraints that are true standard-side requirements. | Prevents oracle-loop errors. |

## 4. Protocol Candidate Matrix

| Protocol | Standard type | Core standards | Downloads | Open implementations | CVE/advisory material | Difficulty | Implicit constraint potential | Recommendation |
|---|---|---|---|---|---|---|---|---|
| MQTT | OASIS/ISO | MQTT 3.1.1, MQTT 5.0 | OASIS HTML/PDF | Many | Medium | Low | High | Pilot 1, plus ProtocolGuard motivation case |
| CoAP | IETF RFC | RFC 7252, 7641, 7959, 8323 | RFC Editor / Datatracker | Many | Medium | Medium | Medium-high | Pilot 2, best RFC starting point |
| DNS | IETF RFC | RFC 1034, 1035, 6891, 7766, 9267, 9520 | RFC Editor / Datatracker | Many | High | High | Very high | High-value backup; scope narrowly |
| FTP | IETF RFC | RFC 959, 3659 | RFC Editor | Many | Medium | Medium | Medium | RFC fallback |
| TLS | IETF RFC | RFC 8446 | RFC Editor | Many | High | High | High | Not first round |
| QUIC | IETF RFC | RFC 9000 series | RFC Editor | Many | Medium-high | High | High | Not first round |

MQTT is not an IETF RFC protocol, so if the project is required to use RFC-only pilots, use **CoAP + DNS scoped parser/compression + FTP fallback**, while keeping MQTT as the ProtocolGuard motivation and comparison case.

## 5. Standards And Download Locations

### 5.1 MQTT Standards

| Standard | Type | Role | HTML | PDF |
|---|---|---|---|---|
| MQTT v3.1.1 | OASIS Standard | Core MQTT 3.1.1 protocol; ClientId, Remaining Length, QoS flows. | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.pdf |
| MQTT v5.0 | OASIS Standard | MQTT 5.0 properties, reason codes, session expiry, enhanced error handling. | https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html | https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.pdf |
| MQTT specification index | Official index | Entry point for MQTT standard versions. | https://mqtt.org/mqtt-specification/ | - |

MQTT is especially useful because ProtocolGuard's motivation example is an MQTT ClientId silent truncation issue. The relevant standard phrase is that a server **MUST allow** ClientIds between 1 and 23 UTF-8 bytes and **MAY allow** longer ClientIds. The hidden issue is not only the length allowance; it is the implicit requirement that accepting a longer identifier must not collapse distinct client identities.

### 5.2 CoAP RFCs

| RFC | Title | Role | HTML | TXT | PDF |
|---|---|---|---|---|---|
| RFC 7252 | The Constrained Application Protocol (CoAP) | Core message format, Message ID, Token, Options, matching. | https://datatracker.ietf.org/doc/html/rfc7252 | https://www.rfc-editor.org/rfc/rfc7252.txt | https://www.rfc-editor.org/rfc/rfc7252.pdf |
| RFC 7641 | Observing Resources in CoAP | Observe extension, subscriptions and notifications. | https://datatracker.ietf.org/doc/html/rfc7641 | https://www.rfc-editor.org/rfc/rfc7641.txt | https://www.rfc-editor.org/rfc/rfc7641.pdf |
| RFC 7959 | Block-Wise Transfers in CoAP | Block1/Block2 transfer, block numbering, size, and reassembly. | https://datatracker.ietf.org/doc/html/rfc7959 | https://www.rfc-editor.org/rfc/rfc7959.txt | https://www.rfc-editor.org/rfc/rfc7959.pdf |
| RFC 8323 | CoAP over TCP, TLS, and WebSockets | Reliable transports and WebSocket binding. | https://datatracker.ietf.org/doc/html/rfc8323 | https://www.rfc-editor.org/rfc/rfc8323.txt | https://www.rfc-editor.org/rfc/rfc8323.pdf |

CoAP is the strongest RFC-based first pilot. It has compact binary messages but enough semantics to exercise implicit constraints: Token matching, Message ID deduplication, ACK/RST context, option encoding, Observe state, and Block-wise reassembly.

### 5.3 DNS RFCs

| RFC | Title | Role | HTML | TXT | PDF |
|---|---|---|---|---|---|
| RFC 1034 | Domain Names - Concepts and Facilities | DNS concepts and architecture. | https://datatracker.ietf.org/doc/html/rfc1034 | https://www.rfc-editor.org/rfc/rfc1034.txt | https://www.rfc-editor.org/rfc/rfc1034.pdf |
| RFC 1035 | Domain Names - Implementation and Specification | DNS message format, labels, compression, RR format. | https://datatracker.ietf.org/doc/html/rfc1035 | https://www.rfc-editor.org/rfc/rfc1035.txt | https://www.rfc-editor.org/rfc/rfc1035.pdf |
| RFC 6891 | Extension Mechanisms for DNS (EDNS(0)) | EDNS payload size, OPT RR, extension behavior. | https://datatracker.ietf.org/doc/html/rfc6891 | https://www.rfc-editor.org/rfc/rfc6891.txt | https://www.rfc-editor.org/rfc/rfc6891.pdf |
| RFC 7766 | DNS Transport over TCP - Implementation Requirements | DNS over TCP behavior and connection handling. | https://datatracker.ietf.org/doc/html/rfc7766 | https://www.rfc-editor.org/rfc/rfc7766.txt | https://www.rfc-editor.org/rfc/rfc7766.pdf |
| RFC 9267 | Common Implementation Anti-Patterns Related to DNS Resource Record Processing | DNS RR processing anti-patterns and RFC 1035 violation patterns. | https://datatracker.ietf.org/doc/html/rfc9267 | https://www.rfc-editor.org/rfc/rfc9267.txt | https://www.rfc-editor.org/rfc/rfc9267.pdf |
| RFC 9520 | Negative Caching of DNS Resolution Failures | DNS failure negative caching behavior. | https://datatracker.ietf.org/doc/html/rfc9520 | https://www.rfc-editor.org/rfc/rfc9520.txt | https://www.rfc-editor.org/rfc/rfc9520.pdf |

DNS has the richest CVE material, but it is easy to overscope. For the first DNS experiment, keep the scope to **message parsing, compression pointer validation, label/name length, or bailiwick/unsolicited RR handling**.

### 5.4 Backup RFCs

| Protocol | RFC | Title | TXT | First-round recommendation |
|---|---|---|---|---|
| FTP | RFC 959 | File Transfer Protocol | https://www.rfc-editor.org/rfc/rfc959.txt | RFC fallback only |
| FTP | RFC 3659 | Extensions to FTP | https://www.rfc-editor.org/rfc/rfc3659.txt | RFC fallback only |
| TLS | RFC 8446 | The Transport Layer Security (TLS) Protocol Version 1.3 | https://www.rfc-editor.org/rfc/rfc8446.txt | Too complex for first round |
| QUIC | RFC 9000 | QUIC: A UDP-Based Multiplexed and Secure Transport | https://www.rfc-editor.org/rfc/rfc9000.txt | Too complex for first round |

## 6. Candidate Implementations

### 6.1 MQTT

| Implementation | Language | Type | URL | Advantage | Risk |
|---|---|---|---|---|---|
| Mosquitto | C | Broker and client tools | https://github.com/eclipse-mosquitto/mosquitto | Mature, widely used, supports MQTT 3.1/3.1.1/5.0. | Larger codebase. |
| Sol | C | Lightweight broker | https://github.com/codepr/sol | Small codebase; directly related to ProtocolGuard's ClientId example. | Less maintained, not production-grade. |
| NanoMQ | C | Broker | https://github.com/nanomq/nanomq | Modern broker, useful as later comparison. | More features and complexity. |

### 6.2 CoAP

| Implementation | Language | Type | URL | Advantage | Risk |
|---|---|---|---|---|---|
| libcoap | C | Client/server library | https://github.com/obgm/libcoap | Mature and actively used; good for tool-based testing. | Extensions can increase scope. |
| FreeCoAP | C | Client/server/proxy | https://github.com/keith-cullen/FreeCoAP | Small enough for early static reading. | Maintenance status needs confirmation. |
| microcoap | C | Lightweight library | https://github.com/1248/microcoap | Very small parser-oriented codebase. | Limited feature coverage. |
| go-coap | Go | Client/server library | https://github.com/plgd-dev/go-coap | Cross-language comparison. | Different static-analysis toolchain. |

### 6.3 DNS

| Implementation | Language | Type | URL | Advantage | Risk |
|---|---|---|---|---|---|
| Dnsmasq | C | DNS/DHCP/TFTP | https://thekelleys.org.uk/dnsmasq/doc.html | Lightweight relative to BIND; many DNS-related historical issues. | Upstream workflow is not GitHub-first. |
| BIND 9 | C | Authoritative/recursive resolver | https://github.com/isc-projects/bind9 | Classic implementation, many advisories. | Very large codebase. |
| Unbound | C | Recursive resolver | https://github.com/NLnetLabs/unbound | Modern resolver and DNSSEC material. | DNSSEC/recursion complexity. |
| miekg/dns | Go | DNS library | https://github.com/miekg/dns | Easy to generate DNS packets and compare parser behavior. | Not a full resolver. |

## 7. CVE And Advisory Seed Table

The following entries are **T1 seed material only**. They must be rechecked in T2 against patches, advisories, standard text, and root cause. Do not treat them as confirmed implicit-constraint samples yet.

| ID / source | Protocol | Implementation | Mechanism | Public reference | Candidate direction | T2 review question |
|---|---|---|---|---|---|---|
| ProtocolGuard ClientId truncation example | MQTT | Sol | CONNECT / Client Identifier | Local `2026-f521-paper.pdf`; DOI: https://dx.doi.org/10.14722/ndss.2026.240521 | purpose-mechanism gap; ambiguous capability scope | If long ClientIds are accepted, does the implementation preserve identity uniqueness instead of silently truncating? |
| CVE-2023-0809 | MQTT | Mosquitto | Initial CONNECT handling / resource use | https://nvd.nist.gov/vuln/detail/CVE-2023-0809 | boundary silence; error handling | Is the bug protocol-state/error-handling related or mainly generic resource exhaustion? |
| CVE-2023-28366 | MQTT | Mosquitto | QoS 2 / Packet Identifier state | https://nvd.nist.gov/vuln/detail/CVE-2023-28366 | state consistency | Can it be mapped to QoS 2 duplicate packet/state cleanup semantics? |
| CVE-2021-34431 | MQTT | Mosquitto | MQTT v5 CONNECT / properties | https://nvd.nist.gov/vuln/detail/CVE-2021-34431 | boundary silence; format consistency | Does the patch correspond to MQTT 5 CONNECT/property semantic validation? |
| CVE-2024-10525 | MQTT | libmosquitto client | SUBACK / reason codes | https://nvd.nist.gov/vuln/detail/CVE-2024-10525 | message format consistency | Must SUBACK reason-code count match subscription count before callback handling? |
| CVE-2025-34468 | CoAP | libcoap | Hostname/address handling | https://nvd.nist.gov/vuln/detail/CVE-2025-34468 | boundary silence; length handling | Is this protocol field length handling or generic API input handling? |
| CVE-2026-29013 | CoAP | libcoap | OSCORE / CBOR handling | https://nvd.nist.gov/vuln/detail/CVE-2026-29013 | extension format parsing | Is OSCORE/CBOR parsing tied to standard compliance or just memory safety? |
| RFC 9267 anti-patterns | DNS | Multiple | RR processing, labels, compression | https://datatracker.ietf.org/doc/html/rfc9267 | boundary silence; parsing ambiguity | Which listed anti-patterns map to CVEs and to RFC 1035 constraints? |
| CVE-2025-40778 | DNS | BIND 9 | Cache / unsolicited RR / bailiwick | https://nvd.nist.gov/vuln/detail/CVE-2025-40778 | purpose-mechanism gap; security boundary | Does the behavior violate an RFC/BCP security boundary or only implementation policy? |

## 8. Pilot 1: MQTT

### Why MQTT

MQTT is the easiest way to run the full thought process quickly. It is small, message-oriented, has several open implementations, and has a direct ProtocolGuard motivation example: oversized ClientIds silently truncated by a broker can collapse distinct client identities.

Although MQTT is OASIS/ISO rather than an IETF RFC, it is valuable because it makes the implicit part very clear: the specification permits longer ClientIds, but the protocol purpose of client identity and session management implies that accepting longer IDs cannot silently map different clients to the same internal identity.

### Standard Locations

| Standard location | Content | Suspicious implicit point |
|---|---|---|
| MQTT 3.1.1 Section 3.1 CONNECT | Client connection request. | First packet must be CONNECT; malformed first-packet handling. |
| MQTT 3.1.1 Section 3.1.3.1 Client Identifier | ClientId identifies client and session state. | If oversized ClientIds are accepted, they must not be silently truncated into identity collisions. |
| MQTT 3.1.1 Section 2.2.3 Remaining Length | Variable-length encoding for remaining packet length. | Encoded length, actual payload, and read boundary must be consistent. |
| MQTT QoS 2 flow | PUBREC/PUBREL/PUBCOMP state. | Duplicate Packet Identifier and state cleanup. |
| MQTT 5.0 Properties | Property length and semantics. | Property count/type/length consistency and reason-code handling. |

### Candidate Constraints

| Direction | Candidate implicit constraint | Bound goal |
|---|---|---|
| purpose-mechanism gap | If a server accepts an oversized ClientId, it must preserve the complete identifier or explicitly reject it; it must not silently truncate it in a way that maps distinct ClientIds to the same internal identity. | Client identity uniqueness and correct session management. |
| boundary silence | If the initial packet is not CONNECT, the broker should reject or close the connection without allocating unbounded state. | Connection-state consistency and DoS resistance. |
| state consistency | Duplicate QoS 2 Packet Identifiers must not leak state or create duplicate resource ownership. | Exactly-once delivery and resource cleanup. |
| message format consistency | SUBACK reason-code count should match the subscription count before client callback handling. | Request-response field correspondence. |

### Experiment Sketch

| Step | Action | Output |
|---|---|---|
| Standard alignment | Read ClientId, Remaining Length, QoS 2, SUBACK sections. | Standard index. |
| Implementations | Start with Mosquitto + Sol; add NanoMQ later. | Implementation records. |
| Inputs | Use `mosquitto_pub/sub`, raw Python sockets, or packet builders. | Reproducible packet scripts. |
| Validation | Compare accepted/rejected behavior and internal identity/session state. | Candidate status and notes. |

### Recommendation

Use MQTT as **Pilot 1** unless a strict RFC-only rule is imposed. If RFC-only is required, keep MQTT as a motivation/baseline case and move CoAP to Pilot 1.

## 9. Pilot 2: CoAP

### Why CoAP

CoAP is the best first RFC pilot. It is standardized by IETF, IoT-oriented like MQTT, and complex enough to contain meaningful implicit constraints without the overhead of TLS or QUIC.

### Standard Locations

| RFC / section | Content | Suspicious implicit point |
|---|---|---|
| RFC 7252 Section 3 | Message format, header, Token Length, Code, Message ID. | Header and token-length consistency. |
| RFC 7252 Section 4 | Message transmission. | CON/NON/ACK/RST matching and retransmission state. |
| RFC 7252 Section 5.3.1 | Request/response matching. | Token must preserve request-response association. |
| RFC 7252 Section 5.4 | Options. | Option delta/length encoding, order, illegal options. |
| RFC 7641 | Observe. | Subscription/notification/cancel state. |
| RFC 7959 | Block-wise transfer. | Block number, size, more flag, and payload boundary consistency. |

### Candidate Constraints

| Direction | Candidate implicit constraint | Bound goal |
|---|---|---|
| purpose-mechanism gap | If Token is used to match requests and responses, implementations must not truncate, confuse, or incorrectly reuse Tokens across contexts. | Request-response association. |
| state consistency | ACK/RST should only match the corresponding Message ID and endpoint context. | Message acknowledgement and deduplication. |
| boundary silence | Abnormal Option delta/length encodings should be rejected or handled as errors, not reinterpreted as other fields. | Unambiguous parsing. |
| block consistency | Block-wise reassembly must keep block number, size, more flag, and payload boundaries consistent. | Complete resource representation. |

### Experiment Sketch

| Step | Action | Output |
|---|---|---|
| Standard alignment | Index RFC 7252 message format, token, message ID, and options. | Standard index. |
| Implementations | Start with libcoap + FreeCoAP. | Implementation records. |
| Inputs | Use `coap-client/coap-server` and raw UDP payloads. | Packet walkthroughs. |
| Validation | Compare parser and matching behavior across implementations. | Candidate status and notes. |

### Recommendation

Use CoAP as **Pilot 2**, or **Pilot 1** if the project must use RFC-only protocols.

## 10. Pilot 3: DNS

### Why DNS

DNS is the highest-value backup. It has abundant standards, implementations, CVEs, and parsing/security-boundary issues. The risk is scope explosion, so the first DNS work should be narrowed to one sub-area.

Recommended first scope:

- DNS message parser;
- label/name length validation;
- compression pointer validation;
- bailiwick or unsolicited RR handling;
- negative caching or DNSSEC failure caching only if the team is ready for resolver complexity.

### Standard Locations

| RFC / section | Content | Suspicious implicit point |
|---|---|---|
| RFC 1035 Section 2.3.4 | Label and domain name length limits. | Label length and complete name length must be enforced consistently. |
| RFC 1035 Section 4.1.4 | Message compression. | Pointer validity, pointer cycles, pointer-label ambiguity. |
| RFC 6891 | EDNS(0). | UDP payload size and OPT RR extension handling. |
| RFC 7766 | DNS over TCP. | Large responses, connection management, fallback behavior. |
| RFC 9267 | RR processing anti-patterns. | Known implementation anti-patterns tied to RFC behavior. |
| RFC 9520 | Negative caching failures. | Failure caching and validation-state consistency. |

### Candidate Constraints

| Direction | Candidate implicit constraint | Bound goal |
|---|---|---|
| parsing ambiguity | A label-length octet must not be interpreted ambiguously as a compression pointer. | Unambiguous DNS message parsing. |
| boundary silence | Compression pointers must point to valid positions within the message and must not form cycles. | Parser termination and DoS resistance. |
| cross-reference consistency | Name length, label length, and RDATA length checks should remain consistent before and after decompression. | Parser consistency. |
| purpose-mechanism gap | A resolver should not cache unsolicited or out-of-bailiwick RR data as trusted answer data. | Cache integrity and poisoning resistance. |

### Experiment Sketch

| Step | Action | Output |
|---|---|---|
| Scope | Start with parser/compression/label length only. | Narrow DNS subproject. |
| Implementations | Dnsmasq + miekg/dns + one of BIND/Unbound later. | Implementation records. |
| Inputs | Use `dnspython`, `miekg/dns`, or raw packet builders. | Packet walkthroughs. |
| Validation | Compare parser acceptance/rejection and decoded names. | Candidate status and notes. |

### Recommendation

Use DNS as **Pilot 3 / high-value backup**. Do not start with full DNS resolver semantics in the first iteration.

## 11. ProtocolGuard-Informed Lessons

The local `2026-f521-paper.pdf` describes ProtocolGuard as extracting normative rules, using LLM-guided static slicing, detecting rule-code semantic inconsistencies, and dynamically verifying candidates through generated assertions and fuzzing. Its evaluation reports 158 non-compliance bugs across 11 implementations and 6 protocols.

For this project, the key lesson is narrower: ProtocolGuard demonstrates that non-compliance bugs matter and can be validated dynamically, but its rule extraction begins from normative rule candidates. The T1 pilots above are chosen to test the additional question from `方案设计.md`: can we systematically generate **implicit** constraints before detection, especially where standards are silent, ambiguous, conflicting, or purpose-heavy but mechanism-light?

## 12. Final Recommendation

Default first-round plan:

| Rank | Protocol | Role | Reason |
|---|---|---|---|
| 1 | MQTT | Main pilot | Fastest to understand; directly aligns with ProtocolGuard ClientId example; strong implicit-constraint story. |
| 2 | CoAP | Main RFC pilot | Best RFC-based starting point; IoT protocol with moderate complexity. |
| 3 | DNS | High-value backup | Rich CVE and implicit-constraint material; must be scoped narrowly. |

RFC-only plan:

| Rank | Protocol | Role | Reason |
|---|---|---|---|
| 1 | CoAP | Main pilot | Most suitable RFC protocol for the first implementation trial. |
| 2 | DNS parser/compression | High-value scoped pilot | Strong implicit constraints if scope is controlled. |
| 3 | FTP | Fallback | Simpler RFC target, but lower novelty. |

## 13. Immediate T2/T3 Action Items

1. Create one `protocol_profile` JSON for MQTT, CoAP, and DNS.
2. For MQTT, review the ProtocolGuard ClientId example and Mosquitto CVE seeds; mark each as explicit, implicit, or out-of-scope.
3. For CoAP, verify libcoap/FreeCoAP build paths and collect issue/advisory material beyond NVD.
4. For DNS, choose one narrow sub-scope before collecting too many resolver-level cases.
5. Keep all CVE entries at `review_status: "unreviewed"` until standard text, patch, and root cause are checked together.
