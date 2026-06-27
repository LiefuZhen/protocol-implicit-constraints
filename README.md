# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

当前仓库重点服务 **T1 协议调研** 与 **T6 建仓/格式约定**，并为阶段 I 的 CVE 语料构建、方向归纳和提示词蒸馏预留统一的数据结构。

## 1. 项目定位

本课题关注协议标准中“字里行间”的隐式约束。协议实现通常依据 RFC、OASIS、ISO 等公开标准开发，标准中的约束可分为两类：

| 类型 | 含义 | 例子 |
|---|---|---|
| 显式约束 | 标准直接写出的规则。 | RFC 2119 关键词、字段长度、枚举取值、状态机顺序。 |
| 隐式约束 | 标准未直接写成单条强制规则，但可由协议目标、字段用途、上下文关系或多处条款一致性推出的要求。 | 接受长标识符时保持身份唯一性；解析压缩指针时保证有界终止；缓存数据保持信任边界。 |

阶段 I 的目标是从真实 CVE/advisory 中归纳“约束生成方向”，并最终蒸馏为一份可复用的 **隐式约束生成方向提示词**。本仓库当前工作属于阶段 I 的基础建设：确定试点协议、统一资料位置、约定 CVE 与候选约束的数据格式。

## 2. 当前负责范围

| 任务 | 当前目标 | 当前产物 | 后续衔接 |
|---|---|---|---|
| T1 协议调研 | 列出可验证的公开协议/RFC，筛选 2-3 个试点。 | `docs/protocol_survey.md`、协议 profile、实现候选记录。 | 为 T2 CVE 采集、T4 实现准备提供协议范围。 |
| T6 建仓与格式 | 建立仓库结构，约定 CVE、方向、候选约束和实现记录格式。 | `README.md`、`schema/`、`examples/`、`scripts/validate_json.py`。 | 为 T2/T3/T7/T5 保持可复核的数据入口。 |

T1/T6 阶段会保留少量 CVE seed、候选方向和候选约束示例，用于说明格式和验证研究路线。正式样本筛选、聚类、方向冻结和实现验证由后续任务继续完成。

## 3. 阶段 I 路线

| 步骤 | 说明 | 仓库位置 |
|---|---|---|
| CVE 采集 | 从 NVD/CVE、厂商公告、实现 issue/commit/security advisory 收集合规类漏洞。 | `protocols/<protocol>/cves/` |
| 标准协议筛选 | 保留能映射到公开标准条款或协议目标的漏洞。 | `schema/cve_record.schema.json` 中的 `screening.standard_protocol_filter` |
| 隐式违背筛选 | 通过“定位漏洞、对齐文档、检查清楚严格限制语句”三步判断显式/隐式违背。 | `screening.implicit_violation_filter` |
| LLM 溯因 | 记录标准缺陷形态：沉默、含糊、矛盾、目的未落地。 | `implicit_constraint_hypothesis`、`prompts/cve_abduction_prompt.md` |
| 聚类与方向归纳 | 按“规范缺陷形态 + 反推思路”归纳方向。 | `schema/directions.example.json`、`prompts/direction_generation_prompt.md` |
| 提示词蒸馏 | 将冻结方向集压缩成阶段 II 使用的方向提示词。 | `prompts/distilled_direction_prompt.v0.md` |

## 4. 当前试点协议

| 协议 | 角色 | 标准类型 | 选择理由 | 当前边界 |
|---|---|---|---|---|
| MQTT | 第一主试点 | OASIS / ISO | 与 ClientId 身份唯一性案例相关，消息结构清晰，适合说明目的与机制脱节型隐式约束。 | 用作第一条 walkthrough 和方法动机案例。 |
| CoAP | RFC 主试点 | IETF RFC | IoT 协议，复杂度适中，Token、Message ID、Option 等机制适合约束生成。 | 优先分析 RFC 7252 核心机制。 |
| DNS | 高价值备选 | IETF RFC | CVE/advisory 丰富，解析歧义、压缩指针和缓存边界适合隐式约束研究。 | 第一轮聚焦 parser/compression 或 cache-boundary 子方向。 |

## 5. 目录结构

| 路径 | 内容 | 后续维护重点 |
|---|---|---|
| `docs/` | 研究说明文档，包括协议调研、CVE seed 分析、数据格式、方向说明和工作流。 | T2/T3 补充筛选统计、方向集版本、人工复核结论。 |
| `schema/` | JSON 字段模板和方向示例。 | T6 后续可升级严格 JSON Schema，并增加字段完整性检查。 |
| `prompts/` | CVE 溯因、方向归纳、候选约束生成、蒸馏提示词草案。 | T3 完成后冻结正式方向提示词。 |
| `protocols/` | 按协议组织的标准、CVE、实现、候选约束和笔记。 | T2/T4/T5 持续补充 patch 阅读、实现运行记录、验证结果。 |
| `examples/` | 最小示例 JSON。 | 作为格式参考；正式研究数据进入 `protocols/`。 |
| `scripts/` | 工具脚本。 | 后续增加字段校验、统计、表格导出脚本。 |
| `review/` | 会议与人工评审记录。 | 记录试点选择、CVE 取舍、方向裁决和复核结果。 |

## 6. 关键文档

| 文件 | 说明 |
|---|---|
| `docs/protocol_survey.md` | T1 协议调研，包含标准下载地址、试点推荐和实验路径。 |
| `docs/workflow.md` | 阶段 I 与 T1/T6/T2/T3/T7/T4/T5 的衔接关系。 |
| `docs/data_format.md` | JSON 字段含义、三级筛选记录方式和状态流转。 |
| `docs/cve_seed_analysis.md` | CVE/advisory 种子分析，包含标准映射和隐式约束假设。 |
| `docs/implicit_constraint_types.md` | 种子方向说明，正式方向集由 T3 基于 CVE 聚类形成。 |
| `docs/terminology.md` | 中英文术语表。 |

## 7. 数据记录概览

| 协议 | Profile | CVE/Seed | Candidate Constraints | Implementations |
|---|---|---|---|---|
| MQTT | `protocols/mqtt/protocol_profile.json` | `protocols/mqtt/cves/` | `protocols/mqtt/constraints/` | `protocols/mqtt/implementations/` |
| CoAP | `protocols/coap/protocol_profile.json` | `protocols/coap/cves/` | `protocols/coap/constraints/` | `protocols/coap/implementations/` |
| DNS | `protocols/dns/protocol_profile.json` | `protocols/dns/cves/` | `protocols/dns/constraints/` | `protocols/dns/implementations/` |

## 8. 数据状态

| 状态 | 含义 |
|---|---|
| `unreviewed` | 初步收集，等待标准和 patch 复核。 |
| `triaged` | 已初步评估，可作为 seed 跟进。 |
| `needs_more_evidence` | 需要补充 RFC section、patch、advisory 或实现细节。 |
| `accepted_seed` | 可进入方向归纳。 |
| `candidate` | 候选约束已生成，等待复核。 |
| `accepted` | 约束可作为规范侧 oracle。 |
| `validated` | 已有实现验证证据。 |
| `ambiguous_spec` | 标准歧义产物。 |
| `rejected` | 记录已剔除。 |

## 9. 质量与安全原则

| 原则 | 说明 |
|---|---|
| 证据可追溯 | CVE/advisory 记录保留公开来源、补丁链接、标准条款映射和筛选结论。 |
| 判据可复用 | 隐式违背筛选采用定位漏洞、对齐文档、检查严格限制语句的三步流程。 |
| 方向可冻结 | T3 形成的方向集和蒸馏提示词作为 artifact 固定版本，供阶段 II 使用。 |
| 材料可控 | 候选漏洞、复现笔记、PoC 线索和敏感验证材料保存在受控访问环境。 |

## 10. JSON 校验

```powershell
python scripts\validate_json.py
```

脚本会递归扫描 `.json` 文件，解析成功输出 `[OK] path`，解析失败输出 `[ERROR] path: error`。
