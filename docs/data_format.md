# 数据格式约定

本文件解释仓库里的 JSON 记录方式。为了后续脚本、统计和 LLM 处理方便，**JSON 字段名保留英文**；中文解释写在本文档中。

当前 `schema/*.schema.json` 作为字段模板使用。正式数据放入 `protocols/<protocol>/` 下对应目录。

## 1. 文件放置位置

| 数据类型 | 放置位置 | 示例 |
|---|---|---|
| 协议 profile | `protocols/<protocol>/protocol_profile.json` | `protocols/mqtt/protocol_profile.json` |
| 实现记录 | `protocols/<protocol>/implementations/<impl_id>.json` | `protocols/mqtt/implementations/mosquitto.json` |
| CVE/advisory 记录 | `protocols/<protocol>/cves/<cve_id>.json` | `protocols/mqtt/cves/CVE-2024-10525.json` |
| 候选约束 | `protocols/<protocol>/constraints/<constraint_id>.json` | `protocols/mqtt/constraints/MQTT-IC-0001.json` |
| 生成方向示例 | `schema/directions.example.json` | 方向归纳完成后形成正式方向集 artifact |
| 蒸馏提示词草案 | `prompts/distilled_direction_prompt.v0.md` | 方向集确认后冻结正式版本 |

## 2. `protocol_profile` 字段说明

协议 profile 描述为什么选择这个协议作为试点。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `protocol_id` | 协议短名。 | 与目录名一致，如 `mqtt`、`coap`、`dns`。 |
| `protocol_name` | 协议全称。 | 例如 `Constrained Application Protocol`。 |
| `standard_refs` | 标准/RFC/OASIS 文档列表。 | 每个条目写 title、type、url、notes。 |
| `candidate_status` | 试点状态。 | 如 `main_pilot`、`main_rfc_pilot`、`high_value_backup`。 |
| `reason_for_selection` | 选择理由。 | 用数组写 2-4 条，说明为什么适合作为试点协议。 |
| `core_entities` | 核心字段/消息/状态。 | 例如 `CONNECT.ClientId`、`Name.compression_pointer`。 |
| `potential_implicit_constraint_points` | 潜在隐式约束点。 | 说明 entity、direction_hint、description。 |
| `notes` | 补充说明。 | 记录风险和范围控制。 |

后续需要补充：

- 标准版本锁定情况；
- 本地标准副本或引用快照；
- 试点最终保留结论；
- 进入 CVE 筛选和实现准备的优先级。

## 3. `cve_record` 字段说明

CVE 记录表示一条可复核的研究样本，重点保存证据、标准映射、三级筛选结论和隐式约束假设。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `cve_id` | CVE 编号或稳定 advisory ID。 | 没有 CVE 时可用 `ADVISORY-...`。 |
| `protocol_id` | 协议 ID。 | 与目录一致。 |
| `implementation` | 受影响实现。 | 尽量对应 `implementations/` 里的 `impl_id`。 |
| `affected_versions` | 受影响版本。 | 只写公开来源能确认的版本。 |
| `summary` | 漏洞摘要。 | 用简短转述概括。 |
| `vulnerability_type` | 漏洞类型。 | DoS、OOB read、cache poisoning、state leak 等。 |
| `related_message_or_field` | 相关协议字段/消息/状态。 | 用数组，如 `SUBACK.reason_codes`。 |
| `related_standard_refs` | 相关标准条款。 | 写 standard、section、quote_or_summary。 |
| `root_cause_summary` | 根因摘要。 | 复核 patch 后继续补。 |
| `screening` | 三级筛选记录。 | 见下表。 |
| `classification` | 分类结论。 | 是否协议相关、是否标准合规相关、显式/隐式/未知。 |
| `implicit_constraint_hypothesis` | 隐式约束假设。 | 写方向、标准缺口、候选约束、绑定目标。 |
| `evidence` | 证据链接。 | NVD、advisory、patch、PoC 链接。 |
| `review_status` | 复核状态。 | 初始通常是 `unreviewed`。 |
| `reviewer` | 复核人。 | 后续填。 |
| `notes` | 补充说明。 | 记录待补证据和复核事项。 |

### 3.1 三级筛选记录

`screening` 用于把阶段 I 的筛选过程写入 artifact，使样本来源和淘汰原因可复核。

| 子字段 | 中文解释 | 填写建议 |
|---|---|---|
| `collection` | 采集信息。 | 记录来源类型、是否有描述、参考链接、补丁、PoC。 |
| `standard_protocol_filter` | 标准协议筛选。 | 判断漏洞是否能映射到公开标准条款或协议目标。 |
| `implicit_violation_filter` | 隐式违背筛选。 | 记录根因位置、文档对齐和严格限制语句检查。 |
| `retention_decision` | 留存结论。 | 如 `keep_for_abduction`、`explicit_reference_only`、`drop_out_of_scope`。 |

`implicit_violation_filter.direct_rule_check.result` 建议取值：

| 取值 | 含义 |
|---|---|
| `explicit_violation` | 存在清楚、无歧义、直接管住该行为的严格限制语句。 |
| `implicit_silence` | 标准对边界、异常、越界或极值处理沉默/欠定义。 |
| `implicit_ambiguous_or_conflict` | 存在严格语句，但彼此矛盾、范围含糊或无法判定边界。 |
| `out_of_scope` | 与公开标准条款或协议目标关系弱。 |
| `unknown` | 证据仍需补充。 |

### 3.2 `classification` 建议取值

| 字段 | 推荐取值 | 说明 |
|---|---|---|
| `is_protocol_related` | `true` / `false` | 是否涉及协议消息、字段、状态、parser。 |
| `is_standard_compliance_related` | `yes` / `no` / `unknown` | 是否能映射到标准合规问题。 |
| `explicit_or_implicit` | `explicit` / `implicit` / `mixed` / `ambiguous` / `unknown` / `out_of_scope` | 根据三级筛选结论填写。 |

### 3.3 `review_status` 建议取值

| 状态 | 含义 |
|---|---|
| `unreviewed` | 只收集了资料，还没有复核。 |
| `triaged` | 初步看过，适合作为 seed。 |
| `needs_more_evidence` | 缺 patch、标准映射或 advisory。 |
| `accepted_seed` | 确认可进入方向归纳。 |
| `rejected` | 已从样本集中剔除。 |

## 4. `implementation` 字段说明

实现记录服务于实现准备和验证闭环。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `impl_id` | 实现 ID。 | 用小写短名，如 `mosquitto`、`libcoap`。 |
| `protocol_id` | 所属协议。 | 必须和协议目录一致。 |
| `name` | 实现名称。 | 项目正式名称。 |
| `language` | 编程语言。 | C、Go、Rust 等。 |
| `repo_url` | 仓库或官网地址。 | 优先 GitHub/GitLab；没有则官网。 |
| `implementation_type` | 实现类型。 | broker、client_library、resolver 等。 |
| `independence_note` | 独立性说明。 | 说明它是否适合 cross-implementation。 |
| `build_status` | 构建状态。 | `unknown`、`builds`、`failed`、`not_tried`。 |
| `build_instructions` | 构建命令。 | 实现准备阶段补充。 |
| `run_instructions` | 运行命令。 | 实现准备阶段补充。 |
| `test_input_method` | 输入构造方式。 | raw packet、client tool、unit harness 等。 |
| `supported_versions` | 支持协议版本。 | 例如 MQTT 3.1.1、MQTT 5.0。 |
| `notes` | 补充说明。 | 记录限制、功能开关、依赖。 |

## 5. `candidate_constraint` 字段说明

候选约束服务于约束生成和验证闭环。它记录可能成立的协议约束。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `id` | 约束 ID。 | 建议格式：`MQTT-IC-0001`、`DNS-IC-0001`。 |
| `protocol_id` | 协议 ID。 | 与目录一致。 |
| `source_type` | 来源类型。 | `implicit`、`explicit`、`mixed`。 |
| `direction` | 生成方向。 | 包含 `direction_id`、`direction_name`、`description`。 |
| `spec_ref` | 标准引用。 | 包含 standard、section、entity、quote_or_summary。 |
| `statement` | 约束语句。 | 一句话说明必须满足什么。 |
| `condition` | 生效条件。 | 什么输入/状态下触发。 |
| `expected_behavior` | 期望行为。 | 合规实现应该怎么做。 |
| `violation_pattern` | 违反模式。 | 记录实现偏离候选约束时的表现。 |
| `bound_goal` | 绑定的协议目标。 | 例如身份唯一性、解析终止性、缓存完整性。 |
| `strength` | 强度。 | `L1` 或 `L2`。 |
| `status` | 当前状态。 | 初始是 `candidate`。 |
| `related_cves` | 相关 CVE。 | 用 CVE ID 数组。 |
| `related_implementations` | 相关实现。 | 用 impl_id 数组。 |
| `review` | 人工复核信息。 | review_status、reviewer、review_notes。 |

### `strength` 解释

| 强度 | 含义 | 能否直接支撑缺陷判定 |
|---|---|---|
| `L1` | 逻辑必然约束。违反后会破坏明确协议目标。 | 可以进入缺陷判定，但仍需复核和实现验证。 |
| `L2` | 经验/最佳实践/鲁棒性约束。 | 作为可疑点或辅助证据使用。 |

### `status` 建议取值

| 状态 | 含义 |
|---|---|
| `candidate` | 候选，未复核。 |
| `under_review` | 正在复核标准和实现。 |
| `accepted` | 约束本身可作为标准侧 oracle。 |
| `validated` | 已有实现验证证据。 |
| `ambiguous_spec` | 更像标准歧义。 |
| `rejected` | 已从候选集中剔除。 |

## 6. 生成方向数据

`schema/directions.example.json` 当前用于保存种子方向示例。正式方向集在方向归纳完成后形成，并应记录为冻结 artifact。

每条方向建议包含：

| 字段 | 中文解释 |
|---|---|
| `direction_id` | 方向 ID。 |
| `direction_name` | 方向名称。 |
| `spec_defect_form` | 标准缺陷形态，如沉默、含糊、矛盾、目的未落地。 |
| `where_to_look` | 在标准中如何定位。 |
| `reverse_inference_rule` | 如何从该位置反推隐式约束。 |
| `supporting_cve_seeds` | 支撑该方向的 CVE seed。 |
| `applicability_boundary` | 适用边界。 |
| `false_positive_risk` | 误报风险。 |
| `review_status` | 人工核实状态。 |

## 7. 蒸馏提示词

阶段 I 最终产物是由方向集蒸馏出的提示词。它面向阶段 II，输入目标标准文本，输出可疑标准位置和候选隐式约束。

提示词版本建议记录：

| 字段/位置 | 中文解释 |
|---|---|
| 文件名 | 如 `prompts/distilled_direction_prompt.v0.md`。 |
| 来源方向集 | 指明对应的 direction set 版本。 |
| 使用范围 | 指明适用协议范围和阶段。 |
| 输出格式 | 对齐 `candidate_constraint` 字段。 |
| 复核要求 | 说明独立复核、L1/L2 分级和绑定协议目标。 |

## 8. 新增记录流程

新增资料时建议遵循：

1. 选择对应协议目录；
2. 从 `schema/` 复制字段模板；
3. 填写公开证据、标准条款和复核状态；
4. 运行 JSON 解析校验；
5. 在相关文档中补充统计或分析结论。

校验命令：

```powershell
python scripts\validate_json.py
```
