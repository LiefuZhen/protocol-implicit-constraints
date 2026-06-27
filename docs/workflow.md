# 项目工作流

本文件说明本仓库支持的研究任务路线，以及各阶段对应的资料位置。

## 1. 任务路线

| 任务 | 内容 | 交付物 | 依赖 |
|---|---|---|---|
| T1 调研协议 | 列出可验证 RFC/标准协议，筛选 2-3 个试点。 | 候选协议表、推荐试点、标准下载地址。 | - |
| T6 建仓与格式 | 建立仓库结构，约定候选约束数据格式。 | 仓库结构、schema、示例 JSON、README。 | - |
| T2 筛选 CVE | 收集 CVE/advisory，判断显式/隐式违背。 | CVE seed 清单、分类结果、复核记录。 | T1, T6 |
| T3 归纳方向 | 从隐式 CVE 中归纳约束生成方向。 | direction set v0、可行性说明。 | T2 |
| T7 试生成约束 | 将方向应用到标准文本并生成候选约束。 | prompt v0、candidate constraint、人工点评。 | T3, T6 |
| T4 准备实现 | 选择 2-3 份独立实现并记录构建运行方式。 | implementation 记录、构建笔记、输入构造方式。 | T1 |
| T5 验证闭环 | 对一条候选约束进行检测、cross-impl 验证和 walkthrough。 | 端到端验证记录。 | T4 |

## 2. 仓库资料对应关系

| 任务 | 当前资料 | 后续维护 |
|---|---|---|
| T1 | `docs/protocol_survey.md`、协议 profile、实现列表、标准链接。 | 补充标准摘录和最终试点确认。 |
| T6 | README、schema 模板、协议目录、示例 JSON、校验脚本。 | 增加严格字段校验和统计脚本。 |
| T2 | `docs/cve_seed_analysis.md`、`protocols/*/cves/*.json`。 | 补充 patch 阅读、标准条款引用、分类结论。 |
| T3 | `docs/implicit_constraint_types.md`、`schema/directions.example.json`。 | 形成正式 direction set v0。 |
| T7 | `protocols/*/constraints/*.json`、`prompts/constraint_generation_prompt.md`。 | 增加生成结果、人工点评和复核状态。 |
| T4 | `protocols/*/implementations/*.json`。 | 补充版本、commit、构建命令、运行命令。 |
| T5 | CVE -> constraint -> implementation 的关联字段。 | 形成 walkthrough 文档。 |

## 3. T1：协议调研

目标：筛选能够支撑实验闭环的协议。

当前推荐：

1. MQTT：第一主试点，适合解释 ProtocolGuard ClientId 隐式约束。
2. CoAP：第一 RFC 主试点，适合迁移验证。
3. DNS：高价值备选，第一轮聚焦 parser/compression 或 cache-boundary 子方向。

输出文件：

- `docs/protocol_survey.md`
- `protocols/mqtt/protocol_profile.json`
- `protocols/coap/protocol_profile.json`
- `protocols/dns/protocol_profile.json`

## 4. T6：建仓与格式

目标：为后续所有记录提供固定位置和字段约定。

当前格式：

- `schema/cve_record.schema.json`
- `schema/candidate_constraint.schema.json`
- `schema/implementation.schema.json`
- `schema/protocol_profile.schema.json`
- `schema/directions.example.json`

这些文件作为字段模板使用。后续可增加严格 JSON Schema 和字段完整性检查脚本。

## 5. T2：CVE 筛选

筛选流程：

1. 定位漏洞涉及的协议字段、消息、状态或 parser。
2. 找到相关标准条款。
3. 判断显式约束覆盖情况。
4. 分析边界沉默、目的机制脱节、交叉引用冲突、能力范围含糊等隐式违背可能性。
5. 更新 JSON 中的 `classification` 和 `review_status`。

输出建议：

- 每条 CVE 一个 JSON；
- 每条记录公开证据链接；
- 每条记录候选隐式约束假设；
- 证据不足时标记 `unknown` 或 `needs_more_evidence`。

## 6. T3：方向归纳

目标：从 T2 确认的隐式 CVE 中归纳“去哪找、怎么反推”的生成方向。

聚类维度：

- 标准缺陷形态；
- 可疑位置；
- 反推逻辑；
- 绑定的协议目标。

输出：

- direction set v0；
- 每条 direction 对应的 CVE 支撑；
- 每条 direction 的适用边界和误报风险。

## 7. T7：候选约束生成

目标：将方向转成提示词，分析 RFC/标准文本并生成候选约束。

每条约束至少包含：

- `direction`
- `spec_ref`
- `statement`
- `condition`
- `expected_behavior`
- `violation_pattern`
- `bound_goal`
- `strength`
- `review`

候选约束经独立复核和实现验证后进入 T5 或论文实验。

## 8. T4：实现准备

目标：每个试点准备 2-3 份独立实现。

实现记录维护项：

- 版本号或 commit；
- 构建命令；
- 运行命令；
- 输入构造方式；
- cross-implementation 对比适配性；
- 功能开关和依赖。

## 9. T5：检测闭环

建议第一条 walkthrough 使用 MQTT ClientId：

```text
ProtocolGuard ClientId seed
  -> MQTT-IC-0001 candidate constraint
  -> Sol / Mosquitto behavior comparison
  -> 人工裁决
  -> 安全 walkthrough
```

闭环结果分类：

- 约束导错；
- 标准歧义；
- 实现缺陷；
- 共享 bug；
- PoC 待补。

## 10. 工作原则

1. T1/T6 阶段采用保守记录。
2. CVE seed 需保留公开证据链接。
3. 候选约束需绑定协议目标。
4. 未公开漏洞 PoC 保存在受控环境。
5. 不确定项使用 `unknown`、`needs_more_evidence` 或 `ambiguous_spec`。
