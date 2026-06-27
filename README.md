# protocol-implicit-constraints

本仓库用于支持协议安全研究课题：

> **Security Between the Lines：基于 CVE 实证的协议隐式约束生成与协议合规缺陷检测**

它不是普通漏洞库，也不是 PoC 仓库，而是一个研究工作区。仓库的目标是把“协议标准里没有直接写出来、但实现必须遵守的隐式约束”系统化记录下来，并为后续的 CVE 筛选、方向归纳、候选约束生成、实现验证和论文实验服务。

## 1. 项目要解决什么问题

网络协议实现通常依据 RFC、OASIS、ISO 或其他公开标准开发。标准里有两类约束：

- **显式约束**：标准直接写出来的规则，例如 MUST、MUST NOT、字段长度、枚举值、状态机顺序。
- **隐式约束**：标准没有直接写成严格规则，但由协议目标、上下文、字段用途或多处条款共同推出的要求。

本课题重点研究第二类。典型例子是 MQTT ClientId：标准允许服务端支持超过 23 字节的 ClientId，但如果实现接受长 ClientId 后静默截断，就可能让两个不同 ClientId 变成同一个内部身份。这条“不能静默截断导致身份坍缩”的约束并不是简单的 MUST 句，而是由 ClientId 的身份/会话管理目的推出的隐式约束。

本仓库围绕这个思路组织资料：

1. 收集协议相关 CVE 和 advisory；
2. 判断漏洞是否与协议标准合规有关；
3. 分析漏洞背后违反的是显式约束还是隐式约束；
4. 从隐式 CVE 中归纳“约束生成方向”；
5. 用这些方向去 RFC/标准中生成候选隐式约束；
6. 后续再对实现做检测、cross-implementation 验证、人工裁决和 PoC walkthrough。

## 2. 当前任务范围：T1 + T6

根据 PPT 最后一张任务图，本仓库目前重点完成 **T1 调研协议** 和 **T6 建仓/格式**，但这两个任务必须能支撑后续 T2/T3/T7/T4/T5。

| 任务 | 当前仓库需要支撑什么 |
|---|---|
| T1 调研协议 | 列出可验证协议/RFC，筛选 2-3 个试点，整理标准下载地址、实现、CVE 种子、隐式约束切入点。 |
| T6 建仓/格式 | 建立仓库结构，约定候选约束、CVE、实现、协议 profile 的 JSON 数据格式，并给出示例记录。 |
| T2 筛 CVE | 可以直接从 `protocols/*/cves/` 开始复核 CVE，而不是重新找资料。 |
| T3 归纳方向 | 可以从 `docs/implicit_constraint_types.md` 和 CVE seed 中抽象方向。 |
| T7 试生成 | 可以从 `protocols/*/constraints/` 继续生成和人工点评候选约束。 |
| T4 找实现 | 可以从 `protocols/*/implementations/` 继续补版本、构建、运行方式。 |
| T5 检测闭环 | 可以沿着 “CVE -> candidate constraint -> implementation” 做一条 walkthrough。 |

## 3. 当前推荐试点

| 协议 | 角色 | 标准类型 | 推荐理由 | 风险 |
|---|---|---|---|---|
| MQTT | 第一主试点 | OASIS/ISO | 最容易跑通；与 ProtocolGuard ClientId 例子强相关；隐式约束很直观。 | 不是 IETF RFC，如果老师要求全 RFC，需要降为动机/对照案例。 |
| CoAP | RFC 主试点 | IETF RFC | IoT 场景，复杂度适中，有 Token、Message ID、Option、Observe、Block-wise 等隐式约束点。 | CVE 数量少于 DNS，部分漏洞可能偏内存安全。 |
| DNS | 高价值备选 | IETF RFC | CVE/advisory 多，解析歧义、压缩指针、缓存安全边界都很适合隐式约束研究。 | 范围很大，第一轮必须缩小到 parser/compression 或 cache-boundary 子方向。 |

如果必须全选 RFC 协议，建议组合改为：

1. CoAP；
2. DNS parser/compression 子方向；
3. FTP 作为兜底试点。

## 4. 仓库目录说明

| 路径 | 当前作用 | 后续需要补什么 |
|---|---|---|
| `docs/` | 人读的研究说明文档，包括调研、术语、工作流、CVE seed 分析、数据格式说明。 | T2/T3 完成后补筛选统计、方向集版本、人工标注一致性结果。 |
| `schema/` | JSON 字段模板。注意不是严格 JSON Schema Draft，而是字段约定模板。 | 如果后续要自动校验字段类型，可升级为真正 JSON Schema。 |
| `prompts/` | 给 LLM 用的提示词草稿，包括 CVE 溯因、方向归纳、候选约束生成。 | T3/T7 后根据实际效果迭代 prompt v1/v2。 |
| `protocols/` | 每个协议的工作区：标准、CVE、实现、候选约束、笔记。 | 后续重点补 `rfc/` 中的标准下载副本或索引、`notes/` 中的人工阅读笔记。 |
| `protocols/<protocol>/cves/` | CVE/advisory seed JSON。 | T2 逐条复核，更新 `review_status` 和分类结论。 |
| `protocols/<protocol>/constraints/` | 候选隐式约束 JSON。 | T7 继续生成、人工点评、标记 accepted/rejected/ambiguous_spec。 |
| `protocols/<protocol>/implementations/` | 实现记录，包括 repo、语言、构建状态、测试输入方式。 | T4 补版本号、commit、构建命令、运行命令。 |
| `protocols/<protocol>/rfc/` | 预留标准文本目录。 | 后续可放下载后的 RFC txt/pdf 或人工摘录，不建议放版权/敏感材料。 |
| `protocols/<protocol>/notes/` | 协议阅读笔记和实验笔记。 | T2/T4/T5 时补标准条款阅读、patch 阅读、walkthrough。 |
| `examples/` | 最小示例 JSON。 | 保留作模板演示，真实研究数据优先放 `protocols/`。 |
| `scripts/` | 工具脚本，目前有 JSON 解析校验。 | 后续可加字段完整性检查、统计脚本、候选约束导出脚本。 |
| `review/` | 会议记录和人工评审记录。 | 每次和老师讨论后补决策、否决项、下一步。 |

## 5. 关键文档索引

| 文件 | 内容 |
|---|---|
| `docs/protocol_survey.md` | T1 协议调研：协议筛选标准、RFC/OASIS 下载地址、试点推荐、实验思路。 |
| `docs/cve_seed_analysis.md` | CVE/advisory 种子详细分析：每条 CVE 的机制、标准映射、隐式约束假设、T2 风险。 |
| `docs/implicit_constraint_types.md` | 隐式约束类型和生成方向：边界沉默、目的机制脱节、状态一致性、解析无歧义等。 |
| `docs/data_format.md` | JSON 数据格式说明：每个字段怎么填、状态怎么流转、L1/L2 强度怎么理解。 |
| `docs/workflow.md` | 与 PPT 任务图对齐的 T1/T6/T2/T3/T7/T4/T5 工作流。 |
| `docs/terminology.md` | 中英文术语表。 |

## 6. 已建立的数据记录

### MQTT

| 类型 | 文件 |
|---|---|
| 协议 profile | `protocols/mqtt/protocol_profile.json` |
| CVE/seed | `PG-MQTT-CLIENTID-TRUNCATION.json`, `CVE-2023-0809.json`, `CVE-2023-28366.json`, `CVE-2021-34431.json`, `CVE-2024-10525.json` |
| 候选约束 | `MQTT-IC-0001.json` 到 `MQTT-IC-0004.json` |
| 实现 | `mosquitto.json`, `sol.json` |

### CoAP

| 类型 | 文件 |
|---|---|
| 协议 profile | `protocols/coap/protocol_profile.json` |
| CVE/seed | `CVE-2025-34468.json`, `CVE-2026-29013.json` |
| 候选约束 | `COAP-IC-0001.json` 到 `COAP-IC-0003.json` |
| 实现 | `libcoap.json`, `freecoap.json` |

### DNS

| 类型 | 文件 |
|---|---|
| 协议 profile | `protocols/dns/protocol_profile.json` |
| CVE/seed | `CVE-2025-40778.json` |
| 候选约束 | `DNS-IC-0001.json`, `DNS-IC-0002.json` |
| 实现 | `bind9.json`, `dnsmasq.json`, `miekg_dns.json` |

## 7. 数据状态说明

当前大多数 JSON 记录仍是 **candidate / unreviewed / needs_more_evidence**。这不是问题，而是 T1/T6 阶段应有的保守状态。

后续 T2/T7 应按下面方式更新：

| 状态 | 含义 |
|---|---|
| `unreviewed` | 只做了初步收集，还没有对照标准和 patch。 |
| `triaged` | 已初步看过，适合作为 seed，但还不是最终结论。 |
| `needs_more_evidence` | 缺 RFC section、patch、advisory 或实现细节。 |
| `accepted_seed` | 可进入 T3 方向归纳。 |
| `candidate` | 候选约束已生成，但未独立复核。 |
| `accepted` | 约束可作为规范侧 oracle。 |
| `validated` | 已经有实现层验证证据。 |
| `ambiguous_spec` | 更像标准歧义，不应直接报实现 bug。 |
| `rejected` | 约束或 CVE 分类不成立。 |

## 8. 安全与仓库可见性

GitHub 仓库建议保持 **private**。

不要上传：

- 未公开漏洞的可利用 PoC；
- 可直接攻击真实服务的 exploit；
- 厂商未修复漏洞的复现细节；
- 私密邮件、未公开报告、敏感截图；
- 包含 token、密钥、真实目标地址的实验材料。

可以上传：

- 公开 CVE/NVD/advisory 链接；
- 标准条款引用或摘要；
- 非武器化的候选约束描述；
- 实现 repo 链接；
- 安全的人工分析笔记。

## 9. 如何校验 JSON

如果系统 `python` 可用：

```powershell
python scripts\validate_json.py
```

如果当前机器没有把 Python 加到 PATH，可以使用 Codex 自带 Python：

```powershell
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

脚本会递归扫描仓库下所有 `.json` 文件：

- 成功解析：输出 `[OK] path`
- 解析失败：输出 `[ERROR] path: error`
- 有错误时退出码为 `1`

## 10. 如何新增一条 CVE 记录

以 MQTT 为例：

```powershell
Copy-Item schema\cve_record.schema.json protocols\mqtt\cves\CVE-XXXX-XXXX.json
notepad protocols\mqtt\cves\CVE-XXXX-XXXX.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

填写时优先补：

1. `cve_id`
2. `protocol_id`
3. `implementation`
4. `summary`
5. `related_message_or_field`
6. `related_standard_refs`
7. `classification`
8. `implicit_constraint_hypothesis`
9. `evidence`

不要一开始就把 `explicit_or_implicit` 写死为 `implicit`，除非已经对照了标准原文、patch 和根因。

## 11. 如何新增一条候选约束

以 MQTT 为例：

```powershell
Copy-Item schema\candidate_constraint.schema.json protocols\mqtt\constraints\MQTT-IC-0005.json
notepad protocols\mqtt\constraints\MQTT-IC-0005.json
C:\Users\jzh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\validate_json.py
```

候选约束至少要能回答：

- 这个约束来自哪条生成方向？
- 标准里对应哪个 section/entity？
- 什么条件下生效？
- 期望行为是什么？
- 违反模式是什么？
- 绑定哪个协议目标？
- 是 L1 逻辑必然，还是 L2 经验/最佳实践？

## 12. 如何推送到 GitHub private 仓库

在 GitHub 上创建 private 仓库 `protocol-implicit-constraints`，不要勾选自动生成 README。然后：

```powershell
git remote add origin https://github.com/<你的用户名>/protocol-implicit-constraints.git
git push -u origin main
```

如果已经设置过 remote，则只需要：

```powershell
git push origin main
```

## 13. 下一步建议

1. T2 先复核 MQTT 的 `PG-MQTT-CLIENTID-TRUNCATION` 和 `CVE-2024-10525`，这两条最适合写清楚隐式约束。
2. CoAP 先补 RFC 7252 的 Token、Message ID、Option 相关条款摘录。
3. DNS 暂时只做 compression pointer / label length，不要马上进入完整 resolver/cache 复杂语义。
4. 给每条 CVE seed 增加 patch 阅读笔记，放到对应 `protocols/<protocol>/notes/`。
5. T3 前不要急着冻结方向集，先把 CVE seed 的分类做扎实。
