# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

仓库面向协议标准、CVE 证据、候选隐式约束和实现验证资料的统一管理，服务于后续调研、实验复现、论文写作和项目交付。

## 1. 项目概述

协议实现通常依据 RFC、OASIS、ISO 等公开标准开发。标准中的约束可分为两类：

- **显式约束**：标准直接写出的规则，例如 MUST、MUST NOT、字段长度、枚举值、状态机顺序。
- **隐式约束**：标准未直接写成单条强制规则，但可由协议目标、字段用途、上下文关系或多处条款一致性推出的要求。

本项目关注隐式约束的系统化生成与验证。典型例子是 MQTT ClientId：标准允许服务端支持超过 23 字节的 ClientId；当服务端接受长 ClientId 时，应保持客户端身份唯一性和会话管理语义，避免静默截断造成身份坍缩。

## 2. 研究流程

| 阶段 | 内容 | 主要产物 |
|---|---|---|
| T1 协议调研 | 筛选可验证协议/RFC，确定 2-3 个试点。 | 协议调研文档、protocol profile。 |
| T6 仓库与格式 | 建立资料结构，约定 JSON 数据格式。 | README、schema、示例 JSON、校验脚本。 |
| T2 CVE 筛选 | 收集 CVE/advisory，判断显式/隐式违背。 | CVE seed JSON、筛选说明。 |
| T3 方向归纳 | 从隐式 CVE 中归纳约束生成方向。 | direction set v0。 |
| T7 约束生成 | 用方向分析标准文本并生成候选约束。 | candidate constraint JSON、人工点评。 |
| T4 实现准备 | 选择并记录 2-3 份独立实现。 | implementation JSON、构建/运行笔记。 |
| T5 验证闭环 | 对候选约束进行实现验证和 walkthrough。 | 验证记录、裁决结果。 |

## 3. 当前试点协议

| 协议 | 角色 | 标准类型 | 选择理由 | 范围控制 |
|---|---|---|---|---|
| MQTT | 第一主试点 | OASIS/ISO | 与 ProtocolGuard ClientId 案例相关，消息结构清晰，适合说明隐式约束。 | 用作第一条 walkthrough 和方法动机案例。 |
| CoAP | RFC 主试点 | IETF RFC | IoT 协议，复杂度适中，Token、Message ID、Option 等机制适合约束生成。 | 优先分析 RFC 7252 核心机制。 |
| DNS | 高价值备选 | IETF RFC | CVE/advisory 丰富，解析歧义和缓存边界适合隐式约束研究。 | 第一轮聚焦 parser/compression 或 cache-boundary 子方向。 |

## 4. 目录结构

| 路径 | 内容 | 后续维护重点 |
|---|---|---|
| `docs/` | 研究说明文档，包括协议调研、CVE seed 分析、数据格式、术语和工作流。 | 补充 T2/T3 统计、方向集版本、人工复核结论。 |
| `schema/` | JSON 字段模板。 | 可升级为严格 JSON Schema，并增加字段完整性检查。 |
| `prompts/` | CVE 溯因、方向归纳、候选约束生成的提示词草稿。 | 根据 T3/T7 实验效果迭代版本。 |
| `protocols/` | 按协议组织的标准、CVE、实现、候选约束和笔记。 | 持续补充标准摘录、patch 阅读、实现运行记录。 |
| `examples/` | 最小示例 JSON。 | 保留作格式示例；正式研究数据放入 `protocols/`。 |
| `scripts/` | 工具脚本。 | 增加字段校验、统计、表格导出脚本。 |
| `review/` | 会议与人工评审记录。 | 记录试点选择、CVE 取舍、约束裁决和下一步任务。 |

## 5. 关键文档

| 文件 | 说明 |
|---|---|
| `docs/protocol_survey.md` | T1 协议调研，包含标准下载地址、试点推荐和实验路径。 |
| `docs/cve_seed_analysis.md` | CVE/advisory 种子分析，包含标准映射和隐式约束假设。 |
| `docs/implicit_constraint_types.md` | 隐式约束类型和生成方向说明。 |
| `docs/data_format.md` | JSON 字段含义、状态流转和新增记录方式。 |
| `docs/workflow.md` | 项目研究任务路线。 |
| `docs/terminology.md` | 中英文术语表。 |

## 6. 数据记录概览

| 协议 | Profile | CVE/Seed | Candidate Constraints | Implementations |
|---|---|---|---|---|
| MQTT | `protocols/mqtt/protocol_profile.json` | `protocols/mqtt/cves/` | `protocols/mqtt/constraints/` | `protocols/mqtt/implementations/` |
| CoAP | `protocols/coap/protocol_profile.json` | `protocols/coap/cves/` | `protocols/coap/constraints/` | `protocols/coap/implementations/` |
| DNS | `protocols/dns/protocol_profile.json` | `protocols/dns/cves/` | `protocols/dns/constraints/` | `protocols/dns/implementations/` |

## 7. 数据状态

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

## 8. 安全与可见性

建议 GitHub 仓库保持 **private**。仓库适合保存公开 CVE/NVD/advisory 链接、标准条款摘要、候选约束、实现记录和安全的人工分析笔记。未公开漏洞复现材料、可直接利用的 PoC、真实目标信息、密钥和私密沟通材料应保存在受控环境中。

## 9. JSON 校验

系统 Python 可用时：

```powershell
python scripts\validate_json.py
```

使用本地运行时 Python：

```powershell
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

脚本会递归扫描 `.json` 文件，解析成功输出 `[OK] path`，解析失败输出 `[ERROR] path: error`。

## 10. 新增记录

新增 CVE 记录：

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

新增实现记录：

```powershell
Copy-Item schema\implementation.schema.json protocols\mqtt\implementations\new_impl.json
notepad protocols\mqtt\implementations\new_impl.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

## 11. GitHub private 仓库

在 GitHub 创建 private 仓库 `protocol-implicit-constraints` 后关联远端：

```powershell
git remote add origin https://github.com/<你的用户名>/protocol-implicit-constraints.git
git push -u origin main
```

已设置 remote 时：

```powershell
git push origin main
```
