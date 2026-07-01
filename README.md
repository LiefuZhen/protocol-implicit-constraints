# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

仓库当前同时服务于 **T1 协议与 Implementation 调研** 和后续 **T6/T4 Docker 实验准备**。正式区保留可继续维护的仓库骨架、调研文档、字段模板、示例 JSON 和 implementation inventory；尚未复核、不能直接作为实验输入的 prompt、CVE candidate、candidate constraint 等材料统一放在 `draft/`。

## 1. 项目定位

本课题关注协议标准中“字里行间”的隐式约束。协议实现通常依据 RFC、OASIS、ISO 或其他公开 Specification 开发，标准中的约束可分为两类：

| 类型 | 含义 | 例子 |
|---|---|---|
| 显式约束 | 标准直接写出的规则。 | RFC 2119 关键词、字段长度、枚举取值、状态机顺序。 |
| 隐式约束 | 标准未直接写成单条强制规则，但可由协议目标、字段用途、上下文关系或多处条款一致性推出的要求。 | 接受长标识符时保持身份唯一性；解析压缩指针时保证有界终止；缓存数据保持信任边界。 |

当前重点不是声明完整 pipeline 已经可用，而是先建立可复核的实验对象基础：Implementation、Protocol、Specification、Section binding、仓库来源和 Docker execution recipe。

## 2. 当前正式交付

| 文件/目录 | 作用 | 当前状态 |
|---|---|---|
| `docs/protocol_implementation_survey.md` | T1 主文档。NDSS Table I 风格的 Implementation-centered 实验对象表。 | 正式维护。 |
| `docs/protocol_survey.md` | 旧版/补充协议调研。 | 可参考，后续以 implementation survey 为主。 |
| `docs/data_format.md` | JSON 字段含义和填写说明。 | 可参考。 |
| `docs/workflow.md` | 研究流程说明。 | 可参考，后续按任务分工更新。 |
| `docs/terminology.md` | 中英文术语表。 | 可参考。 |
| `protocols/*/protocol_profile.json` | 协议 profile。 | 保留为结构化 inventory。 |
| `protocols/*/implementations/*.json` | 实现记录。 | 保留，后续与 T1/T6 表格对齐。 |
| `schema/` | 字段模板。 | 保留，但不是严格 JSON Schema。 |
| `examples/` | 最小示例 JSON。 | 保留为格式示例，不代表正式样本。 |
| `scripts/validate_json.py` | JSON 语法检查脚本。 | 只检查 JSON parse，不检查字段语义。 |

## 3. Draft 材料

以下内容目前不能直接作为实验输入或正式结论，因此放在 `draft/`：

| 路径 | 说明 |
|---|---|
| `draft/prompts/` | prompt 草案。正式 prompt 需在 CVE seed 和 direction set 复核后冻结。 |
| `draft/protocols/*/cves/` | 早期 CVE/advisory candidate。尚未完成 T2 筛选和人工复核。 |
| `draft/protocols/*/constraints/` | 早期 candidate constraint。尚未被接受为 oracle。 |
| `draft/old_docs/cve_seed_analysis.md` | CVE seed 草案分析。 |
| `draft/old_docs/implicit_constraint_types.md` | 隐式约束方向草案。 |
| `draft/artifacts/` | 外部 artifact 和论文 PDF，仅作为调研来源。 |

## 4. 目录结构

```text
.
├── README.md
├── docs/
│   ├── protocol_implementation_survey.md  # T1 主交付：Implementation-centered dataset
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
└── draft/                                 # 未复核草案与 artifact
```

## 5. T1 / T6 衔接

T1 的目标是形成 Implementation-centered 调研表，确定哪些 Subject 可作为后续实验对象。T6/T4 的目标是在 Docker 中真正构建、运行和验证这些 Subject。

后续衔接关系：

1. T1：整理 Subject、Protocol、Specification、Section binding、Repo/Artifact source；
2. T6/T4：为 P0/P1 Subject 编写 Dockerfile，实测 build/run command；
3. T2：按 Implementation 收集 CVE/advisory，并映射到 Specification Section；
4. T3：从复核后的 CVE 中归纳 implicit constraint direction；
5. T7：做 cross-implementation comparison 和动态验证。

## 6. JSON 校验

```powershell
python scripts\validate_json.py
```

如果 Windows 环境没有把 Python 加入 PATH，可以改用已安装的 Python 解释器运行同一个脚本。

脚本会递归扫描 `.json` 文件，解析成功输出 `[OK] path`，解析失败输出 `[ERROR] path: error`。它只检查 JSON 语法，不检查字段完整性或研究结论正确性。

## 7. 公开仓库注意事项

当前仓库可以公开维护，因为正式区主要是调研文档、公开 Specification 链接、公开实现仓库和字段模板。后续如果加入未公开漏洞、PoC、复现脚本、敏感补丁分析或未披露结果，应改为 private 或迁移到受控仓库。
