# schema 目录说明

本目录里的 JSON 文件是**字段模板**，用于复制后填写并保持字段一致。目前的 `scripts/validate_json.py` 检查 JSON 解析状态；字段完整性检查可在后续脚本中扩展。

| 文件 | 用途 | 后续应放在哪里 |
|---|---|---|
| `cve_record.schema.json` | CVE/advisory seed 记录模板。 | 复制到 `protocols/<protocol>/cves/`。 |
| `candidate_constraint.schema.json` | 候选约束记录模板。 | 复制到 `protocols/<protocol>/constraints/`。 |
| `implementation.schema.json` | 实现/库/工具记录模板。 | 复制到 `protocols/<protocol>/implementations/`。 |
| `protocol_profile.schema.json` | 协议试点 profile 模板。 | 复制到 `protocols/<protocol>/protocol_profile.json`。 |
| `directions.example.json` | 约束生成方向 seed 示例。 | T3 后形成正式 direction set。 |

字段含义和状态流转见：

- `docs/data_format.md`
- `docs/implicit_constraint_types.md`

后续如果要做更严格的自动化，可以新增：

- `schema/*.draft.schema.json`：真正 JSON Schema；
- `scripts/validate_records.py`：检查必填字段、枚举值、ID 命名；
- `scripts/export_tables.py`：把 JSON 汇总成论文表格。
