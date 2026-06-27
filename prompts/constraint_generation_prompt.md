# 候选隐式约束生成提示词

用途：把已经归纳出的方向应用到某个目标 RFC/标准，生成候选隐式约束。

候选约束属于待复核研究记录，需要经过人工复核和实现验证。

## 输入

- 目标协议标准片段；
- 协议实体索引：字段、消息、状态、option、ID、cache 等；
- 约束生成方向；
- 已知协议目标；
- 相关 CVE seed，如果有。

## 生成步骤

1. 在标准中定位可疑位置：
   - 边界沉默；
   - 目的与机制脱节；
   - 交叉引用冲突；
   - 能力/范围声明含糊；
   - 状态一致性；
   - 解析无歧义；
   - 安全边界保持。
2. 判断命中哪条 direction。
3. 写出候选约束 statement。
4. 写出生效条件 condition。
5. 写出合规实现 expected_behavior。
6. 写出违反模式 violation_pattern。
7. 绑定协议目标 bound_goal。
8. 判断强度：
   - `L1`：逻辑必然，违反后破坏明确协议目标；
   - `L2`：经验/最佳实践，作为辅助证据或可疑点。

## 输出格式

尽量输出可填入 `candidate_constraint.schema.json` 的字段：

```json
{
  "id": "",
  "protocol_id": "",
  "source_type": "implicit",
  "direction": {},
  "spec_ref": {},
  "statement": "",
  "condition": "",
  "expected_behavior": "",
  "violation_pattern": "",
  "bound_goal": "",
  "strength": "L1",
  "status": "candidate",
  "related_cves": [],
  "related_implementations": [],
  "review": {}
}
```

## 输出要求

- 候选约束状态保持为 `candidate`；
- 输出聚焦标准语义和验证条件；
- RFC section 需来自输入材料；
- 标准映射不足时标记 `needs_more_evidence`。
