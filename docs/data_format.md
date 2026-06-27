# 数据格式约定

本文件解释仓库里的 JSON 应该怎么写。为了后续脚本、统计和 LLM 处理方便，**JSON 字段名保留英文**；中文解释写在本文档中。

当前 `schema/*.schema.json` 是字段模板，不是严格 JSON Schema Draft。复制模板后填写即可。

## 1. 文件放置位置

| 数据类型 | 放置位置 | 示例 |
|---|---|---|
| 协议 profile | `protocols/<protocol>/protocol_profile.json` | `protocols/mqtt/protocol_profile.json` |
| 实现记录 | `protocols/<protocol>/implementations/<impl_id>.json` | `protocols/mqtt/implementations/mosquitto.json` |
| CVE/advisory 记录 | `protocols/<protocol>/cves/<cve_id>.json` | `protocols/mqtt/cves/CVE-2024-10525.json` |
| 候选约束 | `protocols/<protocol>/constraints/<constraint_id>.json` | `protocols/mqtt/constraints/MQTT-IC-0001.json` |
| 生成方向 | 当前为 `schema/directions.example.json` | T3 后可新增 `directions/directions.v0.json` |

## 2. `protocol_profile` 字段说明

协议 profile 描述为什么选择这个协议作为试点。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `protocol_id` | 协议短名。 | 与目录名一致，如 `mqtt`、`coap`、`dns`。 |
| `protocol_name` | 协议全称。 | 例如 `Constrained Application Protocol`。 |
| `standard_refs` | 标准/RFC/OASIS 文档列表。 | 每个条目写 title、type、url、notes。 |
| `candidate_status` | 试点状态。 | 如 `main_pilot`、`main_rfc_pilot`、`high_value_backup`。 |
| `reason_for_selection` | 选择理由。 | 用数组写 2-4 条，说明为什么适合 T1。 |
| `core_entities` | 核心字段/消息/状态。 | 例如 `CONNECT.ClientId`、`Name.compression_pointer`。 |
| `potential_implicit_constraint_points` | 潜在隐式约束点。 | 说明 entity、direction_hint、description。 |
| `notes` | 补充说明。 | 记录风险和范围控制。 |

后续需要补：

- 标准版本是否锁定；
- 是否下载本地副本；
- 试点是否最终保留；
- 进入 T2/T4 的优先级。

## 3. `implementation` 字段说明

实现记录服务于 T4/T5。

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
| `build_instructions` | 构建命令。 | T4 时补。 |
| `run_instructions` | 运行命令。 | T4 时补。 |
| `test_input_method` | 输入构造方式。 | raw packet、client tool、unit harness 等。 |
| `supported_versions` | 支持协议版本。 | 例如 MQTT 3.1.1、MQTT 5.0。 |
| `notes` | 补充说明。 | 记录限制、功能开关、依赖。 |

## 4. `cve_record` 字段说明

CVE 记录服务于 T2。它不是最终漏洞结论，而是“可复核的研究样本”。

| 字段 | 中文解释 | 填写建议 |
|---|---|---|
| `cve_id` | CVE 编号或稳定 advisory ID。 | 没有 CVE 时可用 `ADVISORY-...`。 |
| `protocol_id` | 协议 ID。 | 与目录一致。 |
| `implementation` | 受影响实现。 | 尽量对应 `implementations/` 里的 `impl_id`。 |
| `affected_versions` | 受影响版本。 | 只写公开来源能确认的版本。 |
| `summary` | 漏洞摘要。 | 用自己的话概括，不贴大段原文。 |
| `vulnerability_type` | 漏洞类型。 | DoS、OOB read、cache poisoning、state leak 等。 |
| `related_message_or_field` | 相关协议字段/消息/状态。 | 用数组，如 `SUBACK.reason_codes`。 |
| `related_standard_refs` | 相关标准条款。 | 写 standard、section、quote_or_summary。 |
| `root_cause_summary` | 根因摘要。 | T2 复核 patch 后继续补。 |
| `classification` | 分类结论。 | 是否协议相关、是否标准合规相关、显式/隐式/未知。 |
| `implicit_constraint_hypothesis` | 隐式约束假设。 | 写方向、标准缺口、候选约束、绑定目标。 |
| `evidence` | 证据链接。 | NVD、advisory、patch、PoC 链接。 |
| `review_status` | 复核状态。 | 初始通常是 `unreviewed`。 |
| `reviewer` | 复核人。 | 后续填。 |
| `notes` | 补充说明。 | 记录不确定点。 |

### `classification` 建议取值

| 字段 | 推荐取值 | 说明 |
|---|---|---|
| `is_protocol_related` | `true` / `false` | 是否涉及协议消息、字段、状态、parser。 |
| `is_standard_compliance_related` | `yes` / `no` / `unknown` | 是否能映射到标准合规问题。 |
| `explicit_or_implicit` | `explicit` / `implicit` / `mixed` / `ambiguous` / `unknown` / `out_of_scope` | 不确定时不要硬写 implicit。 |

### `review_status` 建议取值

| 状态 | 含义 |
|---|---|
| `unreviewed` | 只收集了资料，还没有复核。 |
| `triaged` | 初步看过，适合作为 seed。 |
| `needs_more_evidence` | 缺 patch、标准映射或 advisory。 |
| `accepted_seed` | 确认可进入 T3 方向归纳。 |
| `rejected` | 不适合作为本项目样本。 |

## 5. `candidate_constraint` 字段说明

候选约束服务于 T7/T5。它记录的是“可能成立的协议约束”，不是已经确认的实现漏洞。

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
| `violation_pattern` | 违反模式。 | 不合规实现看起来是什么样。 |
| `bound_goal` | 绑定的协议目标。 | 例如身份唯一性、解析终止性、缓存完整性。 |
| `strength` | 强度。 | `L1` 或 `L2`。 |
| `status` | 当前状态。 | 初始是 `candidate`。 |
| `related_cves` | 相关 CVE。 | 用 CVE ID 数组。 |
| `related_implementations` | 相关实现。 | 用 impl_id 数组。 |
| `review` | 人工复核信息。 | review_status、reviewer、review_notes。 |

### `strength` 解释

| 强度 | 含义 | 能否直接支撑缺陷判定 |
|---|---|---|
| `L1` | 逻辑必然约束。违反后会破坏明确协议目标。 | 可以，但仍需复核和实现验证。 |
| `L2` | 经验/最佳实践/鲁棒性约束。 | 不建议单独作为实现缺陷。 |

### `status` 建议取值

| 状态 | 含义 |
|---|---|
| `candidate` | 候选，未复核。 |
| `under_review` | 正在复核标准和实现。 |
| `accepted` | 约束本身可作为标准侧 oracle。 |
| `validated` | 已有实现验证证据。 |
| `ambiguous_spec` | 更像标准歧义。 |
| `rejected` | 约束不成立或不适合本项目。 |

## 6. 生成方向数据

`schema/directions.example.json` 当前只是 seed examples，不是最终方向集。

后续 T3 生成正式方向集时，建议每条方向包含：

- `direction_id`
- `direction_name`
- 标准缺陷形态；
- 在标准中如何定位；
- 如何反推隐式约束；
- 支撑它的 CVE seed；
- 适用边界；
- 误报风险；
- 人工复核状态。

## 7. 新增记录流程

新增 CVE：

```powershell
Copy-Item schema\cve_record.schema.json protocols\mqtt\cves\CVE-XXXX-XXXX.json
notepad protocols\mqtt\cves\CVE-XXXX-XXXX.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

新增候选约束：

```powershell
Copy-Item schema\candidate_constraint.schema.json protocols\mqtt\constraints\MQTT-IC-0005.json
notepad protocols\mqtt\constraints\MQTT-IC-0005.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

新增实现：

```powershell
Copy-Item schema\implementation.schema.json protocols\mqtt\implementations\new_impl.json
notepad protocols\mqtt\implementations\new_impl.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```
