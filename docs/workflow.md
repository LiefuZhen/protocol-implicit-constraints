# 项目工作流

本文件把仓库内容和 PPT 最后一张“任务清单”对齐。当前仓库虽然只要求完成 T1 和 T6，但 T1/T6 是后续 T2/T3/T7/T4/T5 的上游，所以这里必须提前约定资料组织方式。

## 1. PPT 任务依赖

| 任务 | 一句话做什么 | 交付物 | 估时 | 依赖 |
|---|---|---|---|---|
| T1 调研协议 | 列可验证 RFC/标准协议，挑 2-3 个试点。 | 候选协议表 + 推荐试点。 | 2.0d | 无 |
| T6 建仓/格式 | 建仓库，约定候选约束数据格式。 | 仓库 + 示例 JSON + README。 | 0.5d | 无 |
| T2 筛 CVE | 拉 CVE，露出隐式违背，复核与判据。 | 漏斗数 + 隐式 CVE 清单 + 一致性统计。 | 2.0d | T1, T6 |
| T3 归纳方向 | 把隐式 CVE 归纳成几条生成方向。 | 方向集 v0 + 可行性结论。 | 1.5d | T2 |
| T7 试生成 | 方向写成提示词，喂 RFC 试生成约束。 | 提示词 v0 + 候选约束 + 人工点评。 | 1.0d | T3, T6 |
| T4 找实现 | 找 2-3 份独立实现，能编译并跟踪一个输入。 | 可跑实现 + 怎么跑笔记。 | 2.0d | T1 |
| T5 检测闭环 | 拿一条已知 CVE 手工跑检测、cross-impl、PoC。 | 一条端到端 walkthrough。 | 1.5d | T4 |

## 2. 当前仓库对每个任务的支持

| 任务 | 当前已有内容 | 后续要补 |
|---|---|---|
| T1 | `docs/protocol_survey.md`、协议 profile、实现列表、RFC/OASIS 链接。 | 继续补人工阅读后的标准摘录和最终试点确认。 |
| T6 | README、schema 模板、协议目录、示例 JSON、校验脚本。 | 后续可升级为严格 JSON Schema 和统计脚本。 |
| T2 | `docs/cve_seed_analysis.md`、`protocols/*/cves/*.json`。 | 逐条补 patch 阅读、标准条款引用、分类结论。 |
| T3 | `docs/implicit_constraint_types.md`、`schema/directions.example.json`。 | 用 T2 结果归纳真正的 direction set v0。 |
| T7 | `protocols/*/constraints/*.json`、`prompts/constraint_generation_prompt.md`。 | 试跑 RFC 生成约束并人工点评。 |
| T4 | `protocols/*/implementations/*.json`。 | 补版本 pin、构建命令、运行命令、测试输入构造方法。 |
| T5 | CVE -> constraint -> implementation 的链接关系。 | 选择一条 MQTT 或 CoAP 样例写完整 walkthrough。 |

## 3. T1：调研协议

目标：找出可以支撑实验闭环的协议，而不是泛泛列协议。

当前推荐：

1. MQTT：第一主试点，适合解释 ProtocolGuard ClientId 隐式约束。
2. CoAP：第一 RFC 主试点，适合正式迁移验证。
3. DNS：高价值备选，第一轮只做 parser/compression 或 cache-boundary 子方向。

输出文件：

- `docs/protocol_survey.md`
- `protocols/mqtt/protocol_profile.json`
- `protocols/coap/protocol_profile.json`
- `protocols/dns/protocol_profile.json`

## 4. T6：建仓与格式

目标：让后续所有记录都有固定位置和固定字段，避免 T2/T3/T7 时资料散掉。

当前格式包括：

- `schema/cve_record.schema.json`
- `schema/candidate_constraint.schema.json`
- `schema/implementation.schema.json`
- `schema/protocol_profile.schema.json`
- `schema/directions.example.json`

注意：这些文件目前是字段模板，不是严格 JSON Schema Draft。

## 5. T2：CVE 筛选

筛选流程：

1. 定位漏洞涉及的协议字段、消息、状态或 parser。
2. 找到相关标准条款。
3. 判断是否有清楚的显式约束直接覆盖该行为。
4. 如果没有，分析是否属于边界沉默、目的机制脱节、交叉引用冲突、能力范围含糊等隐式违背。
5. 更新 JSON 中的 `classification` 和 `review_status`。

输出建议：

- 每条 CVE 一个 JSON；
- 每条有 NVD/advisory/patch 链接；
- 每条都写“为什么可能是隐式约束”；
- 不确定就保留 `unknown` 或 `needs_more_evidence`。

## 6. T3：方向归纳

目标：从 T2 确认的隐式 CVE 中归纳“去哪找、怎么反推”的生成方向。

不要按“漏洞危害”聚类，而要按：

- 标准缺陷形态；
- 可疑位置；
- 反推逻辑；
- 绑定的协议目标。

输出：

- direction set v0；
- 每条 direction 对应的 CVE 支撑；
- 每条 direction 的适用边界和误报风险。

## 7. T7：候选约束生成

目标：把方向写成 prompt，喂给 RFC/标准，生成候选约束。

每条约束至少要包含：

- `direction`
- `spec_ref`
- `statement`
- `condition`
- `expected_behavior`
- `violation_pattern`
- `bound_goal`
- `strength`
- `review`

候选约束不是 bug。只有经过独立复核和实现验证后，才能进入 T5 或论文实验。

## 8. T4：实现准备

目标：每个试点至少准备 2-3 份独立实现。

实现记录要补：

- 版本号或 commit；
- 构建命令；
- 运行命令；
- 如何构造输入；
- 是否适合 cross-implementation 对比；
- 哪些功能需要开启。

## 9. T5：检测闭环

建议第一条 walkthrough 用 MQTT：

```text
ProtocolGuard ClientId seed
  -> MQTT-IC-0001 candidate constraint
  -> Sol / Mosquitto behavior comparison
  -> 人工裁决
  -> 安全的非武器化 walkthrough
```

闭环里要区分：

- 约束导错；
- 标准歧义；
- 实现缺陷；
- 共享 bug；
- PoC 还没补。

## 10. 工作原则

1. T1/T6 阶段保守记录，不急着下最终结论。
2. 所有 CVE seed 都要能追溯到公开链接。
3. 所有候选约束都要绑定协议目标。
4. 不上传未公开漏洞 PoC。
5. 对不确定项明确写 `unknown`、`needs_more_evidence` 或 `ambiguous_spec`。
