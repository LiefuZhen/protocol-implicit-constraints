# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

仓库统一管理协议标准、CVE/advisory 证据、约束生成方向、候选隐式约束、实现记录和验证材料，为后续研究流程提供可复核的数据基础。

## 1. 项目定位

本课题关注协议标准中“字里行间”的隐式约束。协议实现通常依据 RFC、OASIS、ISO 等公开标准开发，标准中的约束可分为两类：

| 类型 | 含义 | 例子 |
|---|---|---|
| 显式约束 | 标准直接写出的规则。 | RFC 2119 关键词、字段长度、枚举取值、状态机顺序。 |
| 隐式约束 | 标准未直接写成单条强制规则，但可由协议目标、字段用途、上下文关系或多处条款一致性推出的要求。 | 接受长标识符时保持身份唯一性；解析压缩指针时保证有界终止；缓存数据保持信任边界。 |

阶段 I 的目标是从真实 CVE/advisory 中归纳“约束生成方向”，并最终蒸馏为一份可复用的 **隐式约束生成方向提示词**。仓库的基础资料包括试点协议、标准链接、CVE seed、候选约束、实现候选和统一 JSON 格式。

## 2. 研究资料范围

| 模块 | 内容 | 当前产物 | 后续衔接 |
|---|---|---|---|
| 协议与标准 | 列出可验证的公开协议/RFC/OASIS/ISO 标准，筛选 2-3 个试点。 | `docs/protocol_survey.md`、协议 profile、实现候选记录。 | 支撑 CVE 采集、标准映射和实现准备。 |
| 数据格式 | 约定 CVE、方向、候选约束和实现记录格式。 | `schema/`、`examples/`、`scripts/validate_json.py`。 | 支撑筛选、聚类、约束生成和验证记录。 |
| 提示词与方向 | 保存 CVE 溯因、方向归纳、约束生成和蒸馏提示词草案。 | `prompts/`、`schema/directions.example.json`。 | 支撑方向集冻结和阶段 II 约束生成。 |

仓库会保留少量 CVE seed、候选方向和候选约束示例，用于说明格式和验证研究路线。正式样本筛选、聚类、方向冻结和实现验证在后续研究步骤中继续补充。

## 3. 目录结构

仓库目录不是为了“摆结构”，而是把后续研究链条拆成可复核的资料位置：模板放在 `schema/`，格式示例放在 `examples/`，正式研究数据放在 `protocols/`，研究说明和人工裁决放在 `docs/`、`review/`。

```text
.
├── README.md
├── docs/
│   ├── protocol_survey.md              # 试点协议调研、标准来源、选择理由
│   ├── workflow.md                     # 阶段 I 到验证闭环的工作流
│   ├── data_format.md                  # JSON 字段含义和填写规则
│   ├── cve_seed_analysis.md            # CVE/advisory seed 分析记录
│   ├── implicit_constraint_types.md    # 隐式约束方向和类型说明
│   └── terminology.md                  # 中英文术语表
├── schema/
│   ├── *.schema.json                   # 字段模板，不是已经完成的研究数据
│   ├── directions.example.json         # 方向集示例，正式方向集后续冻结
│   └── README.md                       # 模板用途说明
├── examples/
│   └── *.json                          # 最小填写示例，用于查字段怎么写
├── protocols/
│   └── <protocol>/                     # 当前包括 mqtt、coap、dns
│       ├── protocol_profile.json       # 协议 profile：标准、选择理由、核心对象
│       ├── cves/                       # CVE/advisory seed 记录
│       ├── constraints/                # 候选隐式约束记录
│       └── implementations/            # 实现、库、工具或服务记录
├── prompts/
│   ├── cve_abduction_prompt.md         # 从 CVE 反推隐式约束假设
│   ├── direction_generation_prompt.md  # 从 seed 归纳方向
│   ├── constraint_generation_prompt.md # 从方向生成候选约束
│   └── distilled_direction_prompt.v0.md # 阶段 II 使用的蒸馏提示词草案
├── scripts/
│   └── validate_json.py                # 当前只检查 JSON 语法是否可解析
├── review/
│   └── meeting_notes.md                # 会议、人工复核和取舍记录
├── .agents/                            # 工具/代理运行上下文，通常不用手动维护

```

### 3.1 顶层目录职责

| 路径 | 当前作用 | 是否需要继续补内容 | 维护重点 |
|---|---|---|---|
| `docs/` | 解释研究路线、字段设计、术语和协议调研。 | 需要。 | 补充筛选统计、方向集版本、人工复核结论和最终实验叙述。 |
| `schema/` | 保存字段模板和方向示例。 | 需要，但不是填真实样本的地方。 | 后续可升级为严格 JSON Schema，增加必填字段、枚举值和字段完整性检查。 |
| `examples/` | 展示最小 JSON 写法。 | 少量即可。 | 保持简洁，帮助理解字段；正式数据不要堆在这里。 |
| `protocols/` | 保存正式研究数据。 | 最需要补。 | 每个协议下持续补 CVE、标准条款、实现信息、候选约束和验证结果。 |
| `prompts/` | 保存各阶段提示词草案。 | 需要。 | 随着 seed 增多，冻结方向集并蒸馏正式提示词。 |
| `scripts/` | 保存校验、统计、导出等工具。 | 后续需要扩展。 | 当前只校验 JSON 语法，之后可检查必填字段和状态流转。 |
| `review/` | 保存人工判断和会议记录。 | 需要。 | 记录为什么保留/剔除某个 CVE、方向或约束。 |

### 3.2 `protocols/` 内部结构

每个协议目录都按同一套结构维护，便于横向比较：

| 子路径 | 记录内容 | 示例 |
|---|---|---|
| `protocol_profile.json` | 协议标准来源、试点角色、核心字段/消息、潜在隐式约束点。 | `protocols/mqtt/protocol_profile.json` |
| `cves/` | CVE/advisory seed，包括漏洞摘要、受影响实现、标准映射、patch 证据和筛选结论。 | `protocols/mqtt/cves/CVE-2024-10525.json` |
| `constraints/` | 候选隐式约束，包括适用条件、期望行为、违背模式、强度和关联 CVE。 | `protocols/mqtt/constraints/MQTT-IC-0001.json` |
| `implementations/` | 实现记录，包括仓库地址、语言、协议版本、构建状态、运行方式和测试输入方式。 | `protocols/mqtt/implementations/mosquitto.json` |

### 3.3 哪些文件是正式资料

| 位置 | 性质 | 现在怎么看 |
|---|---|---|
| `schema/*.schema.json` | 字段模板。里面有很多空字符串和空数组是正常的，用于复制后填写。 | 看字段结构，不把它当成研究结论。 |
| `examples/*.json` | 最小示例。部分字段空着是为了说明“可以这样填”。 | 看写法，不统计进正式样本。 |
| `protocols/*/*.json` | 正式研究数据或候选数据。 | 这里才是后续论文、实验和复核主要引用的资料。 |
| `prompts/*.md` | 提示词草案。 | 阶段 I 完成后需要冻结版本。 |
| `docs/*.md` | 方法、字段和调研说明。 | 随研究推进补结论和取舍依据。 |

## 4. JSON 模板与资料补充说明


| 类型 | 用途| 后续 |
|---|---|---|
| 模板字段 | `schema/*.schema.json` 用来规定字段长什么样，空值是占位符。 | 不需要填真实内容；后续复制到 `protocols/` 后再填。 |
| 示例字段 | `examples/*.json` 只演示最小结构。 | 可以保持简略，不必写满。 |
| 正式数据待复核字段 | `protocols/*/cves/`、`constraints/`、`implementations/` 中有些字段确实还缺证据。 | 可以继续补，但要基于公开资料、patch、标准条款或人工复核。 |


## 5. 阶段 I 路线

| 步骤 | 说明 | 仓库位置 |
|---|---|---|
| CVE 采集 | 从 NVD/CVE、厂商公告、实现 issue/commit/security advisory 收集合规类漏洞。 | `protocols/<protocol>/cves/` |
| 标准协议筛选 | 保留能映射到公开标准条款或协议目标的漏洞。 | `schema/cve_record.schema.json` 中的 `screening.standard_protocol_filter` |
| 隐式违背筛选 | 通过“定位漏洞、对齐文档、检查清楚严格限制语句”三步判断显式/隐式违背。 | `screening.implicit_violation_filter` |
| LLM 溯因 | 记录标准缺陷形态：沉默、含糊、矛盾、目的未落地。 | `implicit_constraint_hypothesis`、`prompts/cve_abduction_prompt.md` |
| 聚类与方向归纳 | 按“规范缺陷形态 + 反推思路”归纳方向。 | `schema/directions.example.json`、`prompts/direction_generation_prompt.md` |
| 提示词蒸馏 | 将冻结方向集压缩成阶段 II 使用的方向提示词。 | `prompts/distilled_direction_prompt.v0.md` |

## 6. 当前试点协议

| 协议 | 角色 | 标准类型 | 选择理由 | 当前边界 |
|---|---|---|---|---|
| MQTT | 第一主试点 | OASIS / ISO | 与 ClientId 身份唯一性案例相关，消息结构清晰，适合说明目的与机制脱节型隐式约束。 | 用作第一条 walkthrough 和方法动机案例。 |
| CoAP | RFC 主试点 | IETF RFC | IoT 协议，复杂度适中，Token、Message ID、Option 等机制适合约束生成。 | 优先分析 RFC 7252 核心机制。 |
| DNS | 高价值备选 | IETF RFC | CVE/advisory 丰富，解析歧义、压缩指针和缓存边界适合隐式约束研究。 | 第一轮聚焦 parser/compression 或 cache-boundary 子方向。 |

## 7. 关键文档

| 文件 | 说明 |
|---|---|
| `docs/protocol_survey.md` | 试点协议调研，包含标准下载地址、试点推荐和实验路径。 |
| `docs/workflow.md` | 阶段 I 资料流、方向归纳、候选约束生成和验证闭环的衔接关系。 |
| `docs/data_format.md` | JSON 字段含义、三级筛选记录方式和状态流转。 |
| `docs/cve_seed_analysis.md` | CVE/advisory 种子分析，包含标准映射和隐式约束假设。 |
| `docs/implicit_constraint_types.md` | 种子方向说明，正式方向集由 CVE 聚类形成。 |
| `docs/terminology.md` | 中英文术语表。 |

## 8. 数据记录概览

| 协议 | Profile | CVE/Seed | Candidate Constraints | Implementations |
|---|---|---|---|---|
| MQTT | `protocols/mqtt/protocol_profile.json` | `protocols/mqtt/cves/` | `protocols/mqtt/constraints/` | `protocols/mqtt/implementations/` |
| CoAP | `protocols/coap/protocol_profile.json` | `protocols/coap/cves/` | `protocols/coap/constraints/` | `protocols/coap/implementations/` |
| DNS | `protocols/dns/protocol_profile.json` | `protocols/dns/cves/` | `protocols/dns/constraints/` | `protocols/dns/implementations/` |

## 9. 数据状态

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

## 10. 质量与安全原则

| 原则 | 说明 |
|---|---|
| 证据可追溯 | CVE/advisory 记录保留公开来源、补丁链接、标准条款映射和筛选结论。 |
| 判据可复用 | 隐式违背筛选采用定位漏洞、对齐文档、检查严格限制语句的三步流程。 |
| 方向可冻结 | 方向集和蒸馏提示词作为 artifact 固定版本，供阶段 II 使用。 |
| 材料可控 | 候选漏洞、复现笔记、PoC 线索和敏感验证材料保存在受控访问环境。 |

## 11. JSON 校验

```powershell
python scripts\validate_json.py
```

如果 Windows 环境没有把 Python 加入 PATH，可以改用已安装的 Python 解释器运行同一个脚本。

脚本会递归扫描 `.json` 文件，解析成功输出 `[OK] path`，解析失败输出 `[ERROR] path: error`。
