# CVE / Advisory 种子分析

本文件把试点协议中的 CVE/advisory 种子展开成可继续复核的材料。当前结论统一按 **seed / candidate** 管理。

## 1. 证据来源

| 来源 | 用途 |
|---|---|
| NVD CVE 页面 | 获取公开漏洞描述、影响版本、参考链接、CWE/CVSS 等。 |
| RFC Editor / IETF Datatracker | 获取 RFC 标准文本和稳定下载地址。 |
| OASIS MQTT 标准 | 获取 MQTT 3.1.1 / 5.0 标准文本。 |
| 本地 ProtocolGuard 论文 PDF | 获取 ClientId 动机例子和 ProtocolGuard 方法基线。 |

## 2. 种子总表

| Seed | 协议 | 实现 | 公开来源 | 相关机制 | 可能方向 | 当前状态 |
|---|---|---|---|---|---|---|
| ProtocolGuard ClientId example | MQTT | Sol | https://dx.doi.org/10.14722/ndss.2026.240521 | CONNECT ClientId | `purpose_mechanism_gap`, `ambiguous_capability_scope` | 强 seed |
| CVE-2023-0809 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2023-0809 | 非 CONNECT 初始包 / Remaining Length | `boundary_silence` | 候选 |
| CVE-2023-28366 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2023-28366 | QoS 2 duplicate message ID | `state_consistency` | 候选 |
| CVE-2021-34431 | MQTT | Mosquitto | https://nvd.nist.gov/vuln/detail/CVE-2021-34431 | MQTT v5 crafted CONNECT | `boundary_silence`, `parser_unambiguity` | 候选 |
| CVE-2024-10525 | MQTT | libmosquitto | https://nvd.nist.gov/vuln/detail/CVE-2024-10525 | SUBACK reason codes | `message_cardinality_consistency` | 强 seed |
| CVE-2025-34468 | CoAP | libcoap | https://nvd.nist.gov/vuln/detail/CVE-2025-34468 | proxy hostname/address resolution | `boundary_silence` | 弱/中 seed |
| CVE-2026-29013 | CoAP | libcoap | https://nvd.nist.gov/vuln/detail/CVE-2026-29013 | OSCORE CBOR unwrap | `parser_unambiguity` | 需补证据 |
| CVE-2025-40778 | DNS | BIND 9 | https://nvd.nist.gov/vuln/detail/CVE-2025-40778 | cache injection / answer acceptance | `security_boundary_preservation` | 强 seed 但复杂 |
| RFC 9267 examples | DNS | 多实现 | https://www.rfc-editor.org/rfc/rfc9267.txt | RR processing / compression / label length | `parser_unambiguity`, `boundary_silence` | 方向 seed |

## 3. MQTT 种子分析

### 3.1 ProtocolGuard ClientId 静默截断

ProtocolGuard 论文中的动机例子来自 Sol MQTT 实现：实现把超长 ClientId 拷贝到固定大小内部缓冲区，导致静默截断。两个不同的长 ClientId 只要前缀相同，就可能映射为同一个内部身份。

| 项 | 分析 |
|---|---|
| 标准位置 | MQTT 3.1.1 Section 3.1.3.1 Client Identifier |
| 显式文本摘要 | Server 必须允许 1-23 UTF-8 字节的 ClientId，也可以允许更长 ClientId。 |
| 隐式约束 | 服务端接受超长 ClientId 时，应完整保留或显式拒绝，避免静默截断导致身份坍缩。 |
| 绑定目标 | 客户端身份唯一性、会话管理、消息路由。 |
| 隐式来源 | 标准允许更长 ClientId；完整保留要求由 ClientId 的用途推出。 |
| 复核动作 | 复核 MQTT 标准原文和 Sol 代码，写安全 walkthrough。 |

对应 JSON：

- `protocols/mqtt/cves/PG-MQTT-CLIENTID-TRUNCATION.json`
- `protocols/mqtt/constraints/MQTT-IC-0001.json`

### 3.2 CVE-2023-0809：Mosquitto 初始非 CONNECT 包导致资源分配

NVD 描述：Mosquitto 2.0.16 之前，恶意初始包在 CONNECT 合法性校验不足时可能造成过量内存分配，从而导致远程 DoS。

| 项 | 分析 |
|---|---|
| 相关机制 | MQTT 初始连接阶段、CONNECT、Fixed Header Remaining Length。 |
| 可能隐式约束 | broker 在为新连接分配大量状态前，应先验证初始包是合法 CONNECT，并且 Remaining Length 在该阶段可接受。 |
| 绑定目标 | 连接状态一致性、DoS 防护。 |
| 待复核点 | 需要区分协议阶段校验问题与通用资源限制问题。 |
| 复核动作 | 阅读 Mosquitto patch/release notes，确认根因是否与协议阶段合规有关。 |

对应 JSON：

- `protocols/mqtt/cves/CVE-2023-0809.json`
- `protocols/mqtt/constraints/MQTT-IC-0002.json`

### 3.3 CVE-2023-28366：Mosquitto QoS 2 重复 message ID 状态泄露

NVD 描述：客户端发送大量 QoS 2 消息并使用重复 message ID，同时不响应 PUBREC，可导致 broker 内存泄露。公开描述中还提到 EAGAIN 处理，因此需要谨慎分类。

| 项 | 分析 |
|---|---|
| 相关机制 | QoS 2 Packet Identifier、PUBREC/PUBREL/PUBCOMP 状态机。 |
| 可能隐式约束 | 重复 Packet Identifier 和未完成握手应保持有界状态和资源释放。 |
| 绑定目标 | exactly-once 语义、事务状态生命周期。 |
| 待复核点 | 需要区分协议状态不变量与通用 send/error handling bug。 |
| 复核动作 | 读 patch，把协议状态不变量和内存管理根因拆开。 |

对应 JSON：

- `protocols/mqtt/cves/CVE-2023-28366.json`
- `protocols/mqtt/constraints/MQTT-IC-0003.json`

### 3.4 CVE-2021-34431：MQTT v5 crafted CONNECT 内存泄露

NVD 描述：Mosquitto 1.6 到 2.0.10 中，认证 MQTT v5 客户端发送 crafted CONNECT 会造成内存泄露。

| 项 | 分析 |
|---|---|
| 相关机制 | MQTT v5 CONNECT、properties、session lifecycle。 |
| 可能隐式约束 | 畸形 CONNECT / property 输入应在错误路径释放解析和会话状态。 |
| 绑定目标 | 会话生命周期一致性、DoS 防护。 |
| 待复核点 | 当前公开摘要需要结合 patch 才能确认具体字段。 |
| 复核动作 | 查 Eclipse bug/patch，确定 malformed 字段。 |

对应 JSON：

- `protocols/mqtt/cves/CVE-2021-34431.json`

### 3.5 CVE-2024-10525：libmosquitto SUBACK reason code 数量不一致

NVD 描述：恶意 broker 发送没有 reason codes 的 crafted SUBACK，可导致 libmosquitto 客户端在 `on_subscribe` callback 中越界访问。

| 项 | 分析 |
|---|---|
| 相关机制 | SUBACK reason codes / return codes。 |
| 可能隐式约束 | 客户端在 callback 或索引前应验证 SUBACK result/reason-code 列表是否存在且数量一致。 |
| 绑定目标 | 请求-响应字段对应关系、安全解析。 |
| 价值 | 字段数量一致性清晰，可从内存安全 CVE 反推出协议结构约束。 |
| 复核动作 | 对比 MQTT 3.1.1 与 MQTT 5.0 SUBACK payload，确认 count/cardinality 关系。 |

对应 JSON：

- `protocols/mqtt/cves/CVE-2024-10525.json`
- `protocols/mqtt/constraints/MQTT-IC-0004.json`

## 4. CoAP 种子分析

### 4.1 CVE-2025-34468：libcoap proxy hostname 栈缓冲区溢出

NVD 描述：libcoap proxy 功能开启时，攻击者控制的 hostname 会进入固定大小栈缓冲区，导致溢出。

| 项 | 分析 |
|---|---|
| 相关机制 | Proxy-Uri、Uri-Host、地址解析。 |
| 可能隐式约束 | 从 CoAP 请求接受的 proxy hostname 应在进入固定缓冲区前做长度检查或拒绝。 |
| 绑定目标 | proxy 请求安全处理、host/authority 解析边界。 |
| 待复核点 | 需要确认它与 CoAP proxy option 语义的关系。 |
| 复核动作 | 确认 hostname 是否来自 CoAP option，查 RFC 7252 对 Proxy-Uri/Uri-Host 的长度和错误处理要求。 |

对应 JSON：

- `protocols/coap/cves/CVE-2025-34468.json`
- `protocols/coap/constraints/COAP-IC-0002.json`

### 4.2 CVE-2026-29013：libcoap OSCORE CBOR unwrap 边界检查

NVD 描述：libcoap OSCORE Appendix B.2 CBOR unwrap 中使用 `assert()` 做边界检查，release build 去掉 assert 后可能出现越界读取。

| 项 | 分析 |
|---|---|
| 相关机制 | OSCORE、CBOR unwrap、安全上下文协商。 |
| 可能隐式约束 | OSCORE/CBOR 解析应在 release build 中执行运行时边界检查，并覆盖 debug assert 之外的生产路径。 |
| 绑定目标 | 安全上下文协商、解析终止性、安全解析。 |
| 待复核点 | 需要补 OSCORE 对应 RFC section。 |
| 复核动作 | 查 OSCORE RFC 与 patch `b7847c4...`，补精确标准映射。 |

对应 JSON：

- `protocols/coap/cves/CVE-2026-29013.json`
- `protocols/coap/constraints/COAP-IC-0003.json`

## 5. DNS 种子分析

### 5.1 RFC 9267：DNS RR 处理反模式

RFC 9267 对 DNS RR 处理反模式做了标准化总结，很适合帮助建立 DNS parser 方向。

| 项 | 分析 |
|---|---|
| 标准基础 | RFC 1035 Section 2.3.4、Section 4.1.4。 |
| 相关机制 | label length、domain name length、compression pointer。 |
| 可能隐式约束 | compression pointer 应在包内解析、保持无环，并保证展开后满足 label/name 长度限制。 |
| 绑定目标 | DNS 解析终止性、解析无歧义、DoS/RCE 防护。 |
| 复核动作 | 选择一个具体实现和一个具体畸形包类型，形成可控 parser 子任务。 |

对应 JSON：

- `protocols/dns/constraints/DNS-IC-0001.json`

### 5.2 CVE-2025-40778：BIND 9 forged data cache injection

NVD 描述：BIND 9 answer processing 过于宽松，特定情况下可让伪造数据进入 cache。

| 项 | 分析 |
|---|---|
| 相关机制 | answer/additional section、resolver cache、bailiwick。 |
| 可能隐式约束 | resolver cache 插入应保持 bailiwick 和请求相关性；伪造、未请求或越权 RR 应进入拒绝或隔离处理。 |
| 绑定目标 | cache integrity、防缓存投毒。 |
| 待复核点 | 精确 oracle 可能分散在 RFC、BCP、ISC advisory 中。 |
| 复核动作 | 阅读 ISC advisory，补 resolver 信任边界的标准/BCP 映射。 |

对应 JSON：

- `protocols/dns/cves/CVE-2025-40778.json`
- `protocols/dns/constraints/DNS-IC-0002.json`

## 6. 复核优先级

建议优先顺序：

1. **ProtocolGuard ClientId seed**：最能讲清楚隐式约束方法动机。
2. **CVE-2024-10525**：字段数量一致性强，适合从 CVE 反推约束。
3. **CVE-2023-0809**：适合验证边界沉默，同时需要区分资源限制与协议合规边界。
4. **CoAP Token / COAP-IC-0001**：适合约束生成试验。
5. **DNS-IC-0001**：适合 parser 子方向，完整 DNS resolver 语义可作为后续扩展。

## 7. 复核原则

- 内存安全 CVE 需要进一步确认协议字段、状态或 parser 语义关系。
- 标准中出现 MUST 时仍需检查多处条款是否存在冲突或歧义。
- MAY support 相关候选约束需要绑定明确协议目标。
- PoC 和攻击细节应保存在受控环境。
- 证据不足的记录使用 `unknown`。
