# Terminology

| Term | Chinese | Meaning | Role in this project |
|---|---|---|---|
| protocol non-compliance bug | 协议合规缺陷 | A bug where implementation behavior deviates from a protocol standard or from a protocol goal implied by that standard. | Main target of detection and validation. |
| explicit constraint | 显式约束 | A requirement directly stated by a standard, often through RFC 2119 keywords such as MUST, MUST NOT, SHALL, SHOULD, or by explicit numeric/format rules. | Baseline constraints that can be extracted with keyword and structure-based methods. |
| implicit constraint | 隐式约束 | A requirement not directly written as a strict rule, but logically implied by the standard's goals, entities, state relations, or cross-references. | Core research target. |
| constraint-generation direction | 约束生成方向 | A reusable direction abstracted from CVE abduction that tells the analyst where to look in a standard and how to infer a candidate implicit constraint. | Main artifact of the CVE-driven stage. |
| boundary silence | 边界沉默 | A standard describes normal behavior but is silent about boundary, malformed, extreme, or exceptional cases. | One seed direction for implicit constraint generation. |
| purpose-mechanism gap | 目的与机制脱节 | A standard states a purpose, such as identity uniqueness or replay prevention, but does not fully specify the implementation behavior needed to preserve it. | Useful for deriving L1 constraints tied to protocol goals. |
| cross-reference conflict | 交叉引用冲突 | Different sections describe the same entity, field, or behavior inconsistently or with conflicting scopes. | A source of ambiguity and implementation divergence. |
| ambiguous capability scope | 含糊能力范围声明 | A standard says an implementation may support or allow a capability, but does not clearly define the extent of support. | Helps detect partial support, silent truncation, or inconsistent acceptance. |
| cross-implementation validation | 跨实现验证 | Running the same candidate behavior or input against multiple independent implementations to see whether behavior diverges. | Used to validate candidates, not as the only detection oracle. |
| CandidateConstraint | 候选约束 | A structured record for a generated constraint, including source direction, standard reference, expected behavior, violation pattern, bound goal, strength, and review state. | Input to implementation analysis and validation. |
