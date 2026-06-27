# 隐式约束类型与生成方向

本文件提供 T1/T6 阶段的种子版方向说明。正式方向集将在 T3 阶段基于已复核 CVE 归纳形成。

## 1. 方向定义

本项目将开放式隐式约束发现转化为可追溯的方向化生成：

> 从历史 CVE 中归纳“标准哪里容易留空子”，再用这些方向在新标准中系统查找候选隐式约束。

方向描述的是：

- 在标准中查看哪些位置；
- 为什么这些位置可能隐藏隐式约束；
- 如何从协议目标或上下文反推出候选约束；
- 该方向的误报风险和适用边界。

## 2. 方向总表

| Direction ID | 中文名 | 在标准中看哪里 | 反推问题 | 常见漏洞形态 | 复核重点 |
|---|---|---|---|---|---|
| `boundary_silence` | 边界沉默 / 欠定义 | 标准描述正常输入，异常、越界、极值、畸形输入处理较少。 | 接受异常输入会影响哪个协议目标？ | oversized length、畸形首包、非法 option、指针越界。 | 错误处理是否属于标准合规范围。 |
| `purpose_mechanism_gap` | 目的与机制脱节 | 标准说明字段/机制目的，实现维护方式需要反推。 | 为维持该目的，实现至少满足什么行为？ | ID 静默截断、请求响应错配、cache 污染。 | 目的是否能绑定明确协议目标。 |
| `cross_reference_conflict` | 前后矛盾 / 交叉引用不一致 | 同一字段/状态在不同章节存在不一致描述。 | 哪种解释更能保持安全或互操作？ | 一处允许、一处禁止；范围/长度定义不一致。 | 是否应归入标准歧义。 |
| `ambiguous_capability_scope` | 能力/范围声明含糊 | 标准说 MAY allow/support，但支持边界未量化。 | 部分支持时仍需保持哪些协议目标？ | 半支持、静默截断、扩展误解析。 | MAY 语言下的强制性边界。 |
| `state_consistency` | 状态一致性 | 多步交互、事务 ID、Token、session、重传、cache。 | 哪些状态关系必须跨消息保持？ | QoS 2 状态泄露、ACK/RST 错配、Token 复用。 | 动态上下文和实现路径。 |
| `parser_unambiguity` | 解析无歧义 | 二进制编码、长度字段、压缩、嵌套编码、CBOR。 | 字节序列是否具有单一可判定含义？解析是否有界终止？ | DNS 指针循环、label/pointer 混淆、CBOR OOB。 | 标准映射和内存安全边界。 |
| `message_cardinality_consistency` | 字段数量一致性 | 请求/响应列表、reason code 数组、option 次数、count 字段。 | 返回项数量是否与请求项或声明 count 一致？ | SUBACK reason code 缺失导致越界。 | 精确标准条款和 patch 证据。 |
| `security_boundary_preservation` | 安全边界保持 | cache、authority、bailiwick、origin、endpoint identity、OSCORE context。 | 哪些数据需要保持在信任边界内？ | DNS cache injection、OSCORE context confusion。 | 多 RFC/BCP 的共同约束。 |

## 3. 当前协议示例

| 协议 | 方向 | 候选约束 |
|---|---|---|
| MQTT | `purpose_mechanism_gap` | 服务端接受长 ClientId 时，应保持身份完整性，避免静默截断导致身份坍缩。 |
| MQTT | `boundary_silence` | 非 CONNECT 初始包应在协议阶段校验前完成拒绝或限界处理。 |
| MQTT | `message_cardinality_consistency` | SUBACK reason-code/result 列表应在 callback 索引前验证数量。 |
| CoAP | `state_consistency` | Token 应保持请求-响应关联，避免截断或跨 endpoint 错配。 |
| CoAP | `parser_unambiguity` | OSCORE/CBOR 解析应在 release build 中执行运行时边界检查。 |
| DNS | `parser_unambiguity` | compression pointer 应在包内解析、保持无环，并保证 name 长度合法。 |
| DNS | `security_boundary_preservation` | resolver cache 应隔离伪造、越权、无关 RR。 |

## 4. L1/L2 强度

| 强度 | 判断标准 | 例子 |
|---|---|---|
| L1 | 违反后会破坏明确协议目标。 | ClientId 静默截断破坏身份唯一性；DNS pointer 循环破坏解析终止性。 |
| L2 | 偏向经验规则、鲁棒性建议或最佳实践。 | 错误码选择、日志行为、超时策略。 |

L1 可进入实现缺陷判定流程；L2 更适合作为可疑点或辅助证据。

## 5. 使用流程

1. 从 CVE 或标准条款定位相关字段/状态。
2. 判断命中哪个 direction。
3. 写出候选约束。
4. 明确绑定协议目标。
5. 标记 L1/L2。
6. 写入 `protocols/<protocol>/constraints/`。
7. 进入独立复核和实现验证。

## 6. T3 方向归纳要求

T3 阶段需要：

- 从 T2 接受的隐式 CVE 中重新归纳方向；
- 判断 seed 方向的保留、合并、拆分或删除；
- 为每条方向绑定 CVE 支撑；
- 报告方向之间的边界；
- 报告现有方向无法覆盖的 CVE 盲区。
