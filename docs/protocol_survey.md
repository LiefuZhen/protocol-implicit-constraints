# 试点协议调研：面向隐式约束研究的协议选择

> 项目：Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测  
> 本文目标：列出可验证标准/RFC，筛选 2-3 个试点，并说明这些试点如何支撑后续 CVE 筛选、方向归纳、约束生成、实现准备和验证闭环。

## 1. 调研目标

本调研用于筛选能够支撑完整研究链条的协议对象：

1. 能从公开 CVE/advisory 中找到协议相关漏洞；
2. 能把漏洞对齐到 RFC/OASIS/ISO 标准条款；
3. 能判断漏洞背后是否存在隐式约束违背；
4. 能从这些 CVE 中归纳约束生成方向；
5. 能把方向应用到目标标准，生成候选约束；
6. 能找到 2-3 个开源实现做 cross-implementation 验证；
7. 能至少做出一条安全的、非武器化的 walkthrough。

根据 `方案设计.md`，本项目的关键差异点是：不把隐式约束留到检测时让 LLM 随机“涌现”，而是先从 CVE 中归纳方向，再在检测前系统生成候选约束。

## 2. 与研究路线的关系

协议调研和数据格式是后续研究步骤的上游基础：

| 后续步骤 | 上游资料需要提前提供什么 |
|---|---|
| CVE 筛选 | 提供 CVE seed、标准链接和 `cve_record` 格式。 |
| 方向归纳 | 提供隐式违背样例，以及 direction / constraint 关联字段。 |
| 约束生成 | 提供 RFC/OASIS section 和 `candidate_constraint` 格式。 |
| 实现准备 | 提供实现候选和 implementation JSON 格式。 |
| 验证闭环 | 提供可跑通的协议路径，并保证 CVE -> 约束 -> 实现可追溯。 |

因此，本仓库在 `protocols/` 下提供了具体的 CVE seed、候选约束和实现记录。

## 3. 试点选择标准

| 维度 | 要求 | 原因 |
|---|---|---|
| 标准公开 | 有 RFC/OASIS/ISO 或类似公开标准，最好有 HTML/TXT/PDF。 | 方便复核 `spec_ref`。 |
| 实现可得 | 至少 2 个独立开源实现。 | 后续可做 cross-implementation 验证。 |
| CVE/advisory 可得 | 有历史漏洞、公告、patch 或 issue。 | 支撑 CVE 筛选和方向归纳。 |
| 复杂度适中 | 消息结构能看懂，输入能构造。 | 避免第一轮陷入环境和复杂状态机。 |
| 隐式约束明显 | 有标识符、长度、状态、解析歧义、缓存边界等。 | 贴合本项目主题。 |
| 与相关工作可对照 | 最好和 ProtocolGuard/RFCAudit 等有交集。 | 方便写 related work 和 baseline。 |

## 4. 候选协议总表

| 协议 | 标准类型 | 核心标准 | 开源实现 | CVE 素材 | 隐式约束潜力 | 难度 | 推荐结论 |
|---|---|---|---|---|---|---|---|
| MQTT | OASIS/ISO | MQTT 3.1.1, MQTT 5.0 | 多 | 中 | 高 | 低 | 第一主试点 |
| CoAP | IETF RFC | RFC 7252, 7641, 7959, 8323 | 多 | 中 | 中高 | 中 | RFC 主试点 |
| DNS | IETF RFC | RFC 1034, 1035, 6891, 7766, 9267, 9520 | 多 | 高 | 很高 | 高 | 高价值备选 |
| FTP | IETF RFC | RFC 959, 3659 | 多 | 中 | 中 | 中 | RFC 兜底 |
| TLS | IETF RFC | RFC 8446 | 多 | 高 | 高 | 很高 | 后期高价值目标 |
| QUIC | IETF RFC | RFC 9000 系列 | 多 | 中高 | 高 | 很高 | 后期迁移验证目标 |

## 5. 标准与下载地址

### 5.1 MQTT

| 标准 | 类型 | 作用 | 地址 |
|---|---|---|---|
| MQTT v3.1.1 | OASIS Standard | ClientId、Remaining Length、QoS、SUBACK、CONNECT 等核心机制。 | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html |
| MQTT v3.1.1 PDF | OASIS Standard | PDF 版本。 | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.pdf |
| MQTT v5.0 | OASIS Standard | Properties、Reason Code、Session Expiry 等。 | https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html |
| MQTT v5.0 PDF | OASIS Standard | PDF 版本。 | https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.pdf |
| MQTT 规范入口 | 官方索引 | 汇总 MQTT 标准版本。 | https://mqtt.org/mqtt-specification/ |

重点条款：

- MQTT 3.1.1 Section 3.1.3.1 Client Identifier；
- MQTT 3.1.1 Section 2.2.3 Remaining Length；
- MQTT QoS 2 相关流程；
- MQTT 5.0 SUBACK / Properties / Reason Code。

### 5.2 CoAP

| RFC | 名称 | 作用 | TXT |
|---|---|---|---|
| RFC 7252 | The Constrained Application Protocol | CoAP 核心协议：Message ID、Token、Option、ACK/RST。 | https://www.rfc-editor.org/rfc/rfc7252.txt |
| RFC 7641 | Observing Resources in CoAP | Observe 扩展。 | https://www.rfc-editor.org/rfc/rfc7641.txt |
| RFC 7959 | Block-Wise Transfers in CoAP | Block1/Block2 分块传输。 | https://www.rfc-editor.org/rfc/rfc7959.txt |
| RFC 8323 | CoAP over TCP, TLS, and WebSockets | 可靠传输扩展。 | https://www.rfc-editor.org/rfc/rfc8323.txt |

重点条款：

- RFC 7252 Section 3 Message Format；
- RFC 7252 Section 4 Message Transmission；
- RFC 7252 Section 5.3.1 Request/Response Matching；
- RFC 7252 Section 5.4 Options；
- RFC 7641 Observe；
- RFC 7959 Block-wise Transfer。

### 5.3 DNS

| RFC | 名称 | 作用 | TXT |
|---|---|---|---|
| RFC 1034 | Domain Names - Concepts and Facilities | DNS 概念与 resolver 基础。 | https://www.rfc-editor.org/info/rfc1034/ |
| RFC 1035 | Domain Names - Implementation and Specification | DNS 消息格式、label、compression pointer、RR。 | https://www.rfc-editor.org/info/rfc1035/ |
| RFC 6891 | EDNS(0) | DNS 扩展机制。 | https://www.rfc-editor.org/info/rfc6891/ |
| RFC 7766 | DNS over TCP Requirements | DNS over TCP 行为。 | https://www.rfc-editor.org/info/rfc7766/ |
| RFC 9267 | DNS RR Processing Anti-Patterns | DNS RR 处理反模式。 | https://www.rfc-editor.org/info/rfc9267/ |
| RFC 9520 | Negative Caching of DNS Resolution Failures | DNS 失败负缓存。 | https://www.rfc-editor.org/info/rfc9520/ |

第一轮 DNS 建议只看：

- compression pointer；
- label/name length；
- parser termination；
- bailiwick/cache boundary 中的一个小方向。

## 6. 当前 CVE / Advisory seed

详细分析见 `docs/cve_seed_analysis.md`。这里列总览：

| Seed | 协议 | 实现 | 机制 | 可能方向 | JSON |
|---|---|---|---|---|---|
| ProtocolGuard ClientId | MQTT | Sol | CONNECT ClientId | 目的机制脱节 | `protocols/mqtt/cves/PG-MQTT-CLIENTID-TRUNCATION.json` |
| CVE-2023-0809 | MQTT | Mosquitto | 非 CONNECT 初始包 | 边界沉默 | `protocols/mqtt/cves/CVE-2023-0809.json` |
| CVE-2023-28366 | MQTT | Mosquitto | QoS 2 duplicate ID | 状态一致性 | `protocols/mqtt/cves/CVE-2023-28366.json` |
| CVE-2021-34431 | MQTT | Mosquitto | MQTT v5 CONNECT | 边界沉默 | `protocols/mqtt/cves/CVE-2021-34431.json` |
| CVE-2024-10525 | MQTT | libmosquitto | SUBACK reason codes | 字段数量一致性 | `protocols/mqtt/cves/CVE-2024-10525.json` |
| CVE-2025-34468 | CoAP | libcoap | proxy hostname | 边界沉默 | `protocols/coap/cves/CVE-2025-34468.json` |
| CVE-2026-29013 | CoAP | libcoap | OSCORE CBOR | 解析无歧义 | `protocols/coap/cves/CVE-2026-29013.json` |
| CVE-2025-40778 | DNS | BIND 9 | cache injection | 安全边界保持 | `protocols/dns/cves/CVE-2025-40778.json` |

## 7. 试点 1：MQTT

### 7.1 为什么选 MQTT

MQTT 是最适合第一轮跑通思路的协议：

- 消息结构相对简单；
- 实现容易找到；
- 输入容易构造；
- ProtocolGuard 的动机例子正好是 MQTT ClientId；
- ClientId、Remaining Length、QoS 2、SUBACK 都有明显隐式约束点。

MQTT 属于 OASIS/ISO 标准体系。若评估口径要求 IETF RFC 协议，MQTT 可作为动机案例和 baseline，正式试点可转向 CoAP。

### 7.2 关键隐式约束点

| 实体 | 可疑点 | 候选约束 |
|---|---|---|
| CONNECT.ClientId | 标准允许长 ClientId，存储/比较语义需要从身份目标反推。 | 接受长 ClientId 时应保持完整身份语义，避免静默截断导致身份坍缩。 |
| Initial Packet | 初始包异常时资源分配边界需要明确。 | 非 CONNECT 初始包应在协议阶段校验前完成拒绝或限界处理。 |
| QoS2.PacketIdentifier | 重复 ID / 未完成握手的状态生命周期。 | 重复或未完成 QoS 2 事务应保持有界状态和资源释放。 |
| SUBACK.reason_codes | 返回结果数量与订阅请求/回调访问之间的关系。 | callback 索引前必须验证 reason-code/result 数量。 |

### 7.3 当前 JSON

- `protocols/mqtt/protocol_profile.json`
- `protocols/mqtt/implementations/mosquitto.json`
- `protocols/mqtt/implementations/sol.json`
- `protocols/mqtt/constraints/MQTT-IC-0001.json` 到 `MQTT-IC-0004.json`

### 7.4 推荐实验路径

第一条 walkthrough 建议使用 ClientId：

```text
标准阅读：MQTT 3.1.3.1 Client Identifier
  -> 候选约束：MQTT-IC-0001
  -> 实现：Sol + Mosquitto
  -> 输入：两个前缀相同但后缀不同的长 ClientId
  -> 观察：是否静默截断、是否身份坍缩
```

## 8. 试点 2：CoAP

### 8.1 为什么选 CoAP

CoAP 是第一轮最合适的 RFC 协议：

- RFC 7252 标准完整；
- 消息格式不算太复杂；
- Token 和 Message ID 天然涉及状态一致性；
- Option 编码适合研究 parser/boundary；
- libcoap / FreeCoAP / microcoap / go-coap 可做 cross-impl。

### 8.2 关键隐式约束点

| 实体 | 可疑点 | 候选约束 |
|---|---|---|
| Token | 用于请求-响应匹配，但实现可能截断/复用/跨上下文混淆。 | Token 匹配必须保持完整 Token 和 endpoint/request 上下文。 |
| Message ID | ACK/RST 和去重依赖 Message ID。 | ACK/RST 应绑定对应 endpoint/context。 |
| Option delta/length | 压缩编码异常处理复杂。 | 异常 option 编码应进入明确错误处理。 |
| Proxy-Uri / Uri-Host | proxy hostname 长度边界。 | hostname 进入固定缓冲区前必须检查长度或拒绝。 |
| OSCORE / CBOR | 安全上下文解析边界。 | release build 中必须做运行时边界检查。 |

### 8.3 当前 JSON

- `protocols/coap/protocol_profile.json`
- `protocols/coap/implementations/libcoap.json`
- `protocols/coap/implementations/freecoap.json`
- `protocols/coap/constraints/COAP-IC-0001.json` 到 `COAP-IC-0003.json`

### 8.4 推荐实验路径

第一轮优先从 Token / Message ID / Option parser 开始：

```text
标准阅读：RFC 7252 Section 3, 4, 5.3.1, 5.4
  -> 候选约束：COAP-IC-0001
  -> 实现：libcoap + FreeCoAP
  -> 输入：构造 Token 边界和 ACK/RST 匹配场景
  -> 观察：是否完整匹配请求-响应上下文
```

## 9. 试点 3：DNS

### 9.1 为什么 DNS 只做备选

DNS 价值很高，但范围非常大。它的 parser、resolver、cache、DNSSEC 都可能形成研究点，但第一轮如果全做会失控。

建议只选一个小方向：

- DNS message parser；
- compression pointer；
- label/name length；
- bailiwick/cache boundary。

### 9.2 关键隐式约束点

| 实体 | 可疑点 | 候选约束 |
|---|---|---|
| compression pointer | 指针越界、循环、指向非法位置。 | pointer 应在包内解析、保持无环，并保证展开后长度合法。 |
| label/name length | 压缩前后长度约束一致性。 | label/name 长度检查必须在解压前后保持一致。 |
| Resolver cache | answer/additional 中的 RR 是否可信。 | cache 插入必须保持 bailiwick 和请求相关性。 |

### 9.3 当前 JSON

- `protocols/dns/protocol_profile.json`
- `protocols/dns/implementations/bind9.json`
- `protocols/dns/implementations/dnsmasq.json`
- `protocols/dns/implementations/miekg_dns.json`
- `protocols/dns/constraints/DNS-IC-0001.json`
- `protocols/dns/constraints/DNS-IC-0002.json`

### 9.4 推荐实验路径

先做 parser/compression：

```text
标准阅读：RFC 1035 Section 2.3.4, 4.1.4 + RFC 9267
  -> 候选约束：DNS-IC-0001
  -> 实现：Dnsmasq + miekg/dns
  -> 输入：构造 pointer 越界、循环、长度异常 packet
  -> 观察：是否拒绝、是否终止、是否解析一致
```

## 10. 后期目标协议

### TLS

TLS 1.3 标准和实现都很复杂，状态机、密码学材料、证书、密钥协商、扩展字段交织在一起。更适合作为后期高价值目标。

### QUIC / HTTP/2

QUIC 和 HTTP/2 都有研究价值，但状态复杂、实现多语言、测试输入构造难度高。建议等 MQTT/CoAP 流程跑通后再迁移。

## 11. 最终推荐

默认推荐：

| 排名 | 协议 | 角色 |
|---|---|---|
| 1 | MQTT | 第一主试点，用于讲清楚隐式约束前移生成的价值。 |
| 2 | CoAP | 第一 RFC 主试点，用于证明方法能迁移到 IETF RFC 协议。 |
| 3 | DNS | 高价值备选，只做小范围 parser/compression 或 cache-boundary。 |

RFC-only 推荐：

| 排名 | 协议 | 角色 |
|---|---|---|
| 1 | CoAP | 主试点。 |
| 2 | DNS parser/compression | 高价值子方向。 |
| 3 | FTP | 兜底试点。 |

## 12. 下一步

1. 优先复核 MQTT ClientId 和 CVE-2024-10525。
2. 补 MQTT / CoAP 标准条款摘录到 `protocols/*/notes/`。
3. 给 CoAP 的 OSCORE seed 补精确 RFC section，再纳入方向归纳。
4. DNS 优先围绕 compression pointer，后续再扩展到完整 resolver。
5. 方向归纳前统一更新每个 CVE JSON 的 `review_status`。
