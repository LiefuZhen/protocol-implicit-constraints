# Draft 材料说明

本目录存放早期生成、尚未复核、当前不能直接作为正式实验输入的材料。

这些文件保留是为了追溯已有尝试，不代表已经完成正式复核，也不代表可以直接用于 Docker 实验、CVE 分析或 implicit constraint 生成。

| 子目录 | 状态 |
|---|---|
| `prompts/` | prompt 草案，需在 CVE seed 和 direction set 复核后再冻结。 |
| `protocols/*/cves/` | 早期 CVE/advisory candidate，尚未完成正式筛选。 |
| `protocols/*/constraints/` | 早期 candidate constraint，尚未被接受为 oracle。 |
| `old_docs/` | 旧版 CVE seed 和方向说明等草案文档。 |
| `artifacts/` | 外部 artifact 或论文材料，仅用于调研参考。 |

说明：`schema/`、`examples/`、`scripts/`、`protocols/*/protocol_profile.json` 和 `protocols/*/implementations/` 已恢复到正式区，作为仓库骨架、字段模板、格式示例和 implementation inventory 使用。
