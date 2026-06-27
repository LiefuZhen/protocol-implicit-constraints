# 术语表

本文件用于统一仓库中的中英文术语。JSON 字段名为了脚本和后续自动化处理，仍保留英文；中文文档中尽量使用中文解释。

| 英文术语 | 中文术语 | 含义 | 在本项目中的作用 |
|---|---|---|---|
| protocol non-compliance bug | 协议合规缺陷 | 协议实现行为偏离标准要求或标准隐含目标导致的缺陷。常见表现包括互操作失败、安全边界破坏、解析歧义或 DoS。 | 本项目主要检测对象。 |
| explicit constraint | 显式约束 | 标准中直接写出的约束，例如 MUST、MUST NOT、SHALL、字段长度、枚举值、ABNF/位图格式。 | 作为 baseline，也用于和隐式约束对比。 |
| implicit constraint | 隐式约束 | 标准没有直接写成强制句，但由字段目的、协议目标、上下文、多章节一致性推出的要求。 | 本项目核心研究对象。 |
| constraint-generation direction | 约束生成方向 | 从 CVE 溯因中归纳出的“去标准哪里找、如何反推出隐式约束”的方向。 | 方向归纳的核心产物，用于生成候选约束。 |
| boundary silence | 边界沉默 / 欠定义 | 标准只描述正常输入或正常流程，对异常、越界、极值、畸形输入没有说明。 | 常见隐式约束来源。 |
| purpose-mechanism gap | 目的与机制脱节 | 标准说明了字段/机制的目的，但实现侧维护方式需要从目标中反推。 | 例如 ClientId 目的为身份/会话管理，因此接受长 ClientId 时应保持身份完整性。 |
| cross-reference conflict | 交叉引用冲突 / 前后矛盾 | 标准不同章节对同一字段、状态或行为存在不一致描述，导致实现解释分歧。 | 用于定位标准内部矛盾处。 |
| ambiguous capability scope | 能力/范围声明含糊 | 标准说实现 MAY support / MAY allow 某能力，但支持边界和失败处理需要进一步明确。 | 例如支持长字段时应保持语义完整性和可判定错误处理。 |
| state consistency | 状态一致性 | 协议多步交互、事务 ID、Token、session、cache 等状态必须保持一致。 | MQTT QoS 2、CoAP Token/Message ID、DNS cache 都可能涉及。 |
| parser unambiguity | 解析无歧义 | 一个字节序列或字段编码应具有单一可判定含义，解析过程有界并能终止。 | DNS compression pointer、CoAP option encoding、CBOR 等都属于这类。 |
| security boundary preservation | 安全边界保持 | 实现应保持标准或协议目标要求的信任边界。 | DNS bailiwick/cache、OSCORE context 等可能涉及。 |
| cross-implementation validation | 跨实现验证 | 用同一输入或同一候选约束观察多个独立实现的行为一致性或分歧。 | 本项目中用于验证候选。 |
| CandidateConstraint | 候选约束 | 记录一条显式或隐式候选约束的数据结构，包括方向、标准位置、约束语句、触发条件、期望行为、违反模式、绑定目标、强度和评审状态。 | 约束生成和验证闭环的主要输入。 |
| constraint-level precision | 约束层精确率 | 生成出的候选约束中，有多少确实能作为标准侧 oracle。 | 用来防止“约束导错导致假 bug”。 |
| L1 constraint | L1 逻辑必然约束 | 违反后必然破坏一个明确协议目标的约束。 | 可进入缺陷判定，但仍需复核和验证。 |
| L2 constraint | L2 经验/最佳实践约束 | 偏向健壮性或最佳实践的约束。 | 作为可疑点或辅助证据使用。 |
