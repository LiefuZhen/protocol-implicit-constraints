# schema 目录说明

本目录里的 JSON 文件是**字段模板**，用于复制后填写并保持字段一致。目前的 `scripts/validate_json.py` 检查 JSON 解析状态；字段完整性检查可在后续脚本中扩展。

| 文件 | 用途 | 后续应放在哪里 |
|---|---|---|
| `cve_record.schema.json` | CVE/advisory seed 记录模板，包含采集、标准协议筛选、隐式违背筛选字段。 | 复制到 `protocols/<protocol>/cves/`。 |
| `candidate_constraint.schema.json` | 候选约束记录模板。 | 复制到 `protocols/<protocol>/constraints/`。 |
| `implementation.schema.json` | 实现/库/工具记录模板。 | 复制到 `protocols/<protocol>/implementations/`。 |
| `protocol_profile.schema.json` | 协议试点 profile 模板。 | 复制到 `protocols/<protocol>/protocol_profile.json`。 |
| `directions.example.json` | 约束生成方向 seed 示例，描述“在标准哪里找、如何反推”。 | 方向归纳后形成正式 direction set。 |

字段含义和状态流转见：

- `docs/data_format.md`
- `docs/implicit_constraint_types.md`

后续任务维护重点：

- CVE 筛选：补齐 `cve_record` 的三级筛选结论和留存/淘汰原因；
- 方向归纳：基于已接受 seed 形成正式方向集 artifact；
- 约束生成：将正式方向集蒸馏为提示词，并对齐候选约束字段；
- 工具扩展：新增字段完整性检查、枚举值检查和表格导出脚本。
