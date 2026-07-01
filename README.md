# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

仓库当前聚焦于公开协议标准、开源 Implementation、Specification Section binding、Docker 构建线索和结构化调研材料。正式区保留可继续维护的调研文档、字段模板、示例 JSON 和 implementation inventory；尚未复核、不能直接作为实验输入的 prompt、CVE candidate、candidate constraint 等材料统一放在 `draft/`。

## 1. 项目定位

本课题关注协议标准中“字里行间”的隐式约束。协议实现通常依据 RFC、OASIS、ISO 或其他公开 Specification 开发，标准中的约束可分为两类：

| 类型 | 含义 | 例子 |
|---|---|---|
| 显式约束 | 标准直接写出的规则。 | RFC 2119 关键词、字段长度、枚举取值、状态机顺序。 |
| 隐式约束 | 标准未直接写成单条强制规则，但可由协议目标、字段用途、上下文关系或多处条款一致性推出的要求。 | 接受长标识符时保持身份唯一性；解析压缩指针时保证有界终止；缓存数据保持信任边界。 |

当前仓库的主要作用是建立可复核的实验对象基础：Implementation、Protocol、Specification、Section binding、Repo / Artifact source、Docker execution recipe 和推荐 Pilot。

## 2. 文件说明

| 文件/目录 | 作用 | 当前状态 |
|---|---|---|
| `docs/protocol_implementation_survey.md` | 主调研文档。NDSS Table I 风格的 Implementation-centered 实验对象表，并包含推荐 Pilot。 | 正式维护。 |
| `docs/docker_execution_recipes.md` | 各 Subject 的 Docker 构建与运行线索。 | 全部标注为未实测，后续需要逐项验证。 |
| `docs/protocol_survey.md` | 旧版/补充协议调研。 | 可参考，后续以 implementation survey 为主。 |
| `docs/data_format.md` | JSON 字段含义和填写说明。 | 可参考。 |
| `docs/workflow.md` | 研究流程说明。 | 可参考，后续按实际流程更新。 |
| `docs/terminology.md` | 中英文术语表。 | 可参考。 |
| `protocols/*/protocol_profile.json` | 协议 profile。 | 保留为结构化 inventory。 |
| `protocols/*/implementations/*.json` | Implementation 记录。 | 保留，后续与调研表对齐。 |
| `schema/` | 字段模板。 | 保留，但不是严格 JSON Schema。 |
| `examples/` | 最小示例 JSON。 | 保留为格式示例，不代表正式样本。 |
| `scripts/validate_json.py` | JSON 语法检查脚本。 | 只检查 JSON parse，不检查字段语义。 |
| `draft/` | 未复核材料和外部 Artifact。 | 不作为正式结论。 |

## 3. Draft 材料

以下内容目前不能直接作为实验输入或正式结论，因此放在 `draft/`：

| 路径 | 说明 |
|---|---|
| `draft/prompts/` | prompt 草案。正式 prompt 需在 CVE seed 和 direction set 复核后冻结。 |
| `draft/protocols/*/cves/` | 早期 CVE/advisory candidate。尚未完成人工复核。 |
| `draft/protocols/*/constraints/` | 早期 candidate constraint。尚未被接受为 oracle。 |
| `draft/old_docs/cve_seed_analysis.md` | CVE seed 草案分析。 |
| `draft/old_docs/implicit_constraint_types.md` | 隐式约束方向草案。 |
| `draft/artifacts/` | 外部 Artifact 和论文 PDF，仅作为调研来源。 |

## 4. 目录结构

```text
.
├── README.md
├── docs/
│   ├── protocol_implementation_survey.md  # 主调研文档：Implementation-centered dataset 与推荐 Pilot
│   ├── docker_execution_recipes.md        # Docker 构建与运行线索，当前均未实测
│   ├── protocol_survey.md                 # 协议调研补充
│   ├── data_format.md                     # JSON 字段说明
│   ├── workflow.md                        # 工作流说明
│   └── terminology.md                     # 术语表
├── protocols/
│   ├── mqtt/
│   ├── coap/
│   └── dns/
│       ├── protocol_profile.json
│       ├── implementations/
│       ├── cves/                          # 当前仅保留目录，未复核内容在 draft/
│       └── constraints/                   # 当前仅保留目录，未复核内容在 draft/
├── schema/                                # JSON 字段模板，不是严格 JSON Schema
├── examples/                              # 最小格式示例
├── scripts/                               # 辅助脚本
├── review/                                # 会议/人工评审记录
└── draft/                                 # 未复核草案与 Artifact
```

## 5. 建议阅读顺序

1. 先阅读 `docs/protocol_implementation_survey.md`，了解候选 Protocol、Subject、Specification、Section binding 和推荐 Pilot。
2. 再阅读 `docs/docker_execution_recipes.md`，查看各 Subject 的未实测 Docker 构建线索。
3. 如需维护结构化数据，再查看 `protocols/`、`schema/` 和 `examples/`。
4. `draft/` 中内容只作为草稿或来源材料，引用前需要人工复核。

## 6. JSON 校验

```powershell
python scripts\validate_json.py
```

如果 Windows 环境没有把 Python 加入 PATH，可以改用已安装的 Python 解释器运行同一个脚本。

脚本会递归扫描 `.json` 文件，解析成功输出 `[OK] path`，解析失败输出 `[ERROR] path: error`。它只检查 JSON 语法，不检查字段完整性或研究结论正确性。

