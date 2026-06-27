# 项目工作流

本文件说明仓库当前工作与完整研究路线之间的关系。当前重点是 **T1 协议调研** 与 **T6 建仓/格式约定**，同时为阶段 I 的 CVE 语料构建、方向归纳和提示词蒸馏打好数据基础。

## 1. 阶段 I 总目标

阶段 I 的核心产物是一份冻结版本的 **隐式约束生成方向提示词**。它来自真实 CVE/advisory 的实证归纳，用于阶段 II 在目标标准中定位模糊、欠定义、前后矛盾和目的未落地的位置，并生成具体隐式约束。

阶段 I 的链条如下：

```text
CVE/advisory 采集
  -> 标准协议筛选
  -> 隐式违背筛选
  -> LLM 溯因
  -> 聚类与方向归纳
  -> 方向集冻结
  -> 蒸馏为生成方向提示词
```

当前 T1/T6 的工作位于这条链条的前端：确定协议范围、建立数据格式、保存 seed 示例和复核入口。

## 2. 任务路线

| 任务 | 当前定位 | 交付物 | 依赖 |
|---|---|---|---|
| T1 调研协议 | 列出可验证 RFC/标准协议，筛选 2-3 个试点。 | 候选协议表、推荐试点、标准下载地址、协议 profile。 | - |
| T6 建仓与格式 | 建立仓库结构，约定 CVE、方向、候选约束和实现记录格式。 | README、schema、示例 JSON、校验脚本、提示词草案。 | - |
| T2 筛选 CVE | 执行三级筛选，形成可复核 CVE seed。 | CVE seed 清单、分类结果、复核记录、留存率统计。 | T1, T6 |
| T3 归纳方向 | 从隐式 CVE 中归纳“去哪找、怎么反推”的生成方向。 | direction set v0、聚类说明、人工核实记录。 | T2 |
| T7 试生成约束 | 将方向应用到标准文本并生成候选约束。 | distilled prompt、candidate constraint、人工点评。 | T3, T6 |
| T4 准备实现 | 选择 2-3 份独立实现并记录构建运行方式。 | implementation 记录、构建笔记、输入构造方式。 | T1 |
| T5 验证闭环 | 对候选约束进行检测、cross-impl 验证和 walkthrough。 | 端到端验证记录。 | T4, T7 |

## 3. 仓库资料对应关系

| 任务 | 当前资料 | 后续维护 |
|---|---|---|
| T1 | `docs/protocol_survey.md`、协议 profile、实现列表、标准链接。 | 补充标准摘录、最终试点确认和范围控制。 |
| T6 | README、schema 模板、协议目录、示例 JSON、校验脚本、提示词草案。 | 增加严格字段校验、统计脚本和正式 artifact 目录。 |
| T2 | `docs/cve_seed_analysis.md`、`protocols/*/cves/*.json`。 | 补充 patch 阅读、标准条款引用、三级筛选结论。 |
| T3 | `docs/implicit_constraint_types.md`、`schema/directions.example.json`、`prompts/direction_generation_prompt.md`。 | 形成正式 `direction set v0` 和聚类稳定性记录。 |
| T7 | `prompts/distilled_direction_prompt.v0.md`、`protocols/*/constraints/*.json`。 | 用冻结提示词生成候选约束并记录人工点评。 |
| T4 | `protocols/*/implementations/*.json`。 | 补充版本、commit、构建命令、运行命令。 |
| T5 | CVE -> direction -> constraint -> implementation 的关联字段。 | 形成 walkthrough 文档和验证裁决记录。 |

## 4. T1：协议调研

目标：筛选能够支撑实验闭环的协议，并保证每个试点具有公开标准、可获取实现和可追溯漏洞资料。

当前推荐：

| 协议 | 角色 | 调研重点 |
|---|---|---|
| MQTT | 第一主试点 | ClientId、会话状态、SUBACK 数量一致性、CONNECT 初始包。 |
| CoAP | RFC 主试点 | Token、Message ID、Option 顺序、OSCORE/CBOR 边界。 |
| DNS | 高价值备选 | 压缩指针、解析终止性、缓存边界、bailiwick 规则。 |

输出文件：

- `docs/protocol_survey.md`
- `protocols/mqtt/protocol_profile.json`
- `protocols/coap/protocol_profile.json`
- `protocols/dns/protocol_profile.json`

## 5. T6：建仓与格式

目标：为后续所有任务提供固定位置和字段约定，使每条资料都能追溯到协议、标准条款、CVE 证据、方向、候选约束和验证结果。

当前格式：

- `schema/cve_record.schema.json`
- `schema/candidate_constraint.schema.json`
- `schema/implementation.schema.json`
- `schema/protocol_profile.schema.json`
- `schema/directions.example.json`

提示词草案：

- `prompts/cve_abduction_prompt.md`
- `prompts/direction_generation_prompt.md`
- `prompts/constraint_generation_prompt.md`
- `prompts/distilled_direction_prompt.v0.md`

## 6. T2：CVE 三级筛选

T2 基于 T1/T6 的协议范围和数据格式执行三级筛选。

| 级别 | 操作 | 记录位置 |
|---|---|---|
| 采集 | 保存描述、参考链接、补丁、受影响实现和版本。 | `evidence`、`summary`、`affected_versions` |
| 标准协议筛选 | 判断漏洞是否能映射到公开标准条款或协议目标。 | `screening.standard_protocol_filter` |
| 隐式违背筛选 | 定位漏洞、对齐文档、检查是否存在清楚严格限制语句。 | `screening.implicit_violation_filter` |

隐式违背判定结果建议保留以下分支：

| 判定 | 含义 | 后续处理 |
|---|---|---|
| `explicit_violation` | 清楚严格限制语句直接约束该行为。 | 可记录为对照样本，通常不进入方向归纳。 |
| `implicit_silence` | 标准对边界、异常或极值处理沉默/欠定义。 | 进入 LLM 溯因候选。 |
| `implicit_ambiguous_or_conflict` | 标准存在限制语句，但含糊、冲突或边界不清。 | 进入 LLM 溯因候选。 |
| `out_of_scope` | 纯内存安全、配置错误或与标准目标关系弱。 | 记录淘汰原因。 |

## 7. T3：方向归纳

目标：从 T2 确认的隐式 CVE 中归纳“标准哪里有缺口、如何反推出约束”的生成方向。

聚类维度：

- 规范缺陷形态：沉默、含糊、欠定义、前后矛盾、目的未落地；
- 在标准中如何定位这种位置；
- 从该位置如何反推隐式约束；
- 绑定的协议目标；
- 误报风险和适用边界。

T3 输出的方向集应作为冻结 artifact 保存，供 T7 和阶段 II 复用。

## 8. T7：提示词蒸馏与候选约束生成

目标：将 T3 的方向集蒸馏为高度凝练的提示词，再用该提示词分析目标标准。

每条候选约束至少包含：

- `direction`
- `spec_ref`
- `statement`
- `condition`
- `expected_behavior`
- `violation_pattern`
- `bound_goal`
- `strength`
- `review`

候选约束经独立复核和实现验证后进入 T5 或论文实验。

## 9. T4/T5：实现准备与验证闭环

T4 为每个试点准备 2-3 份独立实现，并记录版本、构建、运行和输入构造方式。

T5 使用以下链条形成端到端记录：

```text
CVE seed
  -> 生成方向
  -> 候选隐式约束
  -> 实现定位
  -> cross-impl 验证
  -> 人工裁决
  -> walkthrough
```

闭环结果分类：

| 结果 | 含义 |
|---|---|
| 实现缺陷 | 约束成立，至少一个实现违反。 |
| 共享缺陷 | 多份实现一致违反，经人工裁决确认。 |
| 规范歧义 | 标准自身边界或优先级不清。 |
| 约束导错 | 候选约束与标准目标不一致。 |
| 证据待补 | 需要补充 PoC、patch 或实现路径。 |

## 10. 工作原则

1. T1/T6 阶段保持格式、证据和范围清晰。
2. CVE seed 保留公开证据链接、标准条款映射和筛选结论。
3. 候选方向说明“去哪找、怎么反推”，候选约束说明“什么条件下应有什么行为”。
4. L1 隐式约束需绑定明确协议目标。
5. 未公开漏洞、复现细节和敏感 PoC 线索进入受控材料区。
