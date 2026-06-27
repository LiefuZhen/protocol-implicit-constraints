# 隐式约束类型与生成方向

本文件是 T1/T6 阶段的“种子版方向说明”。按照 `方案设计.md`，真正的方向集应该在 T3 中从已复核 CVE 中归纳出来；这里先给出可用于 T2/T7 的工作分类，帮助统一记录方式。

## 1. 为什么要定义方向

如果直接让 LLM “找隐式约束”，结果很容易随机、不可复现，也很难解释漏掉了什么。本项目希望把问题改成：

> 从历史 CVE 中归纳“标准哪里容易留空子”，再用这些方向去新标准中系统查找候选隐式约束。

所以方向不是漏洞类型，也不是 CWE，而是：

- 去标准的哪里找；
- 为什么那里可能有隐式约束；
- 如何从标准目的或上下文反推出候选约束；
- 这个方向有什么误报风险。

## 2. 方向总表

| Direction ID | 中文名 | 在标准中看哪里 | 反推问题 | 常见漏洞形态 | 误报风险 |
|---|---|---|---|---|---|
| `boundary_silence` | 边界沉默 / 欠定义 | 标准描述正常输入，但没说异常、越界、极值、畸形输入。 | 如果实现接受异常输入，会破坏哪个协议目标？ | oversized length、畸形首包、非法 option、指针越界。 | 有些标准故意把错误处理留给实现。 |
| `purpose_mechanism_gap` | 目的与机制脱节 | 标准说明字段/机制目的，但没说实现必须怎样维护目的。 | 为了维持这个目的，实现至少必须满足什么？ | ID 静默截断、请求响应错配、cache 污染。 | 目的可能是描述性文字，需要绑定明确协议目标。 |
| `cross_reference_conflict` | 前后矛盾 / 交叉引用不一致 | 同一字段/状态在不同章节被不同方式描述。 | 哪种解释更能保持安全或互操作？ | 一处允许、一处禁止；范围/长度定义不一致。 | 可能更适合作为标准歧义，而不是实现 bug。 |
| `ambiguous_capability_scope` | 能力/范围声明含糊 | 标准说 MAY allow/support，但没定义支持边界。 | 如果实现只支持一半，至少不能发生什么？ | 半支持、静默截断、扩展误解析。 | MAY 语言会削弱强制性。 |
| `state_consistency` | 状态一致性 | 多步交互、事务 ID、Token、session、重传、cache。 | 哪些状态关系必须跨消息保持？ | QoS 2 状态泄露、ACK/RST 错配、Token 复用。 | 需要动态上下文，单靠静态文本容易误判。 |
| `parser_unambiguity` | 解析无歧义 | 二进制编码、长度字段、压缩、嵌套编码、CBOR。 | 同一字节序列是否可能被解析成冲突含义？解析是否有界终止？ | DNS 指针循环、label/pointer 混淆、CBOR OOB。 | 可能退化成普通内存安全 bug，需要标准映射。 |
| `message_cardinality_consistency` | 字段数量一致性 | 请求/响应列表、reason code 数组、option 次数、count 字段。 | 返回项数量是否与请求项或声明 count 一致？ | SUBACK reason code 缺失导致越界。 | 必须找到精确标准条款。 |
| `security_boundary_preservation` | 安全边界保持 | cache、authority、bailiwick、origin、endpoint identity、OSCORE context。 | 哪些数据不能跨越信任边界？ | DNS cache injection、OSCORE context confusion。 | 常分散在多个 RFC/BCP，映射成本高。 |

## 3. 当前协议中的示例

| 协议 | 方向 | 候选约束 |
|---|---|---|
| MQTT | `purpose_mechanism_gap` | 服务端接受长 ClientId 时，不能静默截断导致身份坍缩。 |
| MQTT | `boundary_silence` | 非 CONNECT 初始包不能在协议阶段校验前触发大内存分配。 |
| MQTT | `message_cardinality_consistency` | SUBACK reason-code/result 列表必须在 callback 索引前验证数量。 |
| CoAP | `state_consistency` | Token 必须保持请求-响应关联，不能截断或跨 endpoint 错配。 |
| CoAP | `parser_unambiguity` | OSCORE/CBOR 解析必须在 release build 中做运行时边界检查。 |
| DNS | `parser_unambiguity` | compression pointer 必须在包内、不能循环、不能突破 name 长度限制。 |
| DNS | `security_boundary_preservation` | resolver cache 不能把伪造、越权、无关 RR 当作可信缓存。 |

## 4. L1/L2 强度判断

| 强度 | 判断标准 | 例子 |
|---|---|---|
| L1 | 违反后必然破坏明确协议目标。 | ClientId 静默截断破坏身份唯一性；DNS pointer 循环破坏解析终止性。 |
| L2 | 更像经验规则、鲁棒性建议或最佳实践。 | 某些错误码选择、日志行为、超时策略。 |

只有 L1 才适合进入“实现缺陷”判定；L2 更适合记为可疑点或未来工作。

## 5. 使用流程

1. 从 CVE 或标准条款定位相关字段/状态。
2. 判断命中哪个 direction。
3. 写出候选约束。
4. 明确绑定协议目标。
5. 标记 L1/L2。
6. 写入 `protocols/<protocol>/constraints/`。
7. 等待独立复核和实现验证。

## 6. 后续 T3 要做什么

当前方向只是 seed。T3 时需要：

- 从 T2 接受的隐式 CVE 中重新归纳方向；
- 看这些 seed 是否保留、合并、拆分或删除；
- 每条方向都要有 CVE 支撑；
- 报告方向之间的边界；
- 报告无法覆盖的 CVE 盲区。
