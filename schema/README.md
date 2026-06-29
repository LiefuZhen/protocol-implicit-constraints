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

如果要把正式数据补扎实，优先补这些资料：

| 数据类型 | 需要补的资料 | 可公开检索的来源 | 可能需要你提供的资料 |
|---|---|---|---|
| CVE/advisory | NVD/CVE 链接、厂商公告、patch commit、受影响版本、修复版本、漏洞根因位置。 | NVD、CVE.org、GitHub advisory、项目 release note、commit。 | 你想纳入论文样本的 CVE 清单、老师确认的取舍标准。 |
| 标准映射 | 相关 RFC/OASIS/ISO 版本、section、字段/消息名、原文摘要。 | RFC Editor、OASIS、ISO 公开页、协议官方文档。 | 如果标准不是公开全文，需要你提供可引用版本或摘录。 |
| 隐式违背判断 | 是否有直接严格规则、是否属于沉默/含糊/矛盾、为什么能反推约束。 | 标准文本、patch 差异、漏洞分析文章。 | 人工裁决口径：显式样本是否保留、L1/L2 强度如何判。 |
| 实现记录 | 仓库 URL、tag/commit、构建命令、运行命令、测试入口、支持协议版本。 | GitHub/GitLab、官方文档、README、release。 | 本地实验环境、你实际要跑的版本和平台。 |
| 候选约束 | 约束语句、触发条件、期望行为、违背模式、关联 CVE/实现、复核状态。 | 已确认的 CVE seed、标准映射和实现行为。 | 人工复核结论和最终是否进入论文实验。 |

因此，这个仓库现在已经可以查阅和继续写正式资料；只是不能把所有空字段都当成“应该马上填满”。最稳的做法是：先选定一批 CVE/advisory，再逐条补 `protocols/<protocol>/cves/`，最后由这些 seed 归纳方向和候选约束。
