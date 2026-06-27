# Schema Folder

The files in this folder are **JSON field templates**, not strict JSON Schema Draft validators.

| File | Used for |
|---|---|
| `cve_record.schema.json` | CVE/advisory seed records in `protocols/<protocol>/cves/`. |
| `candidate_constraint.schema.json` | Candidate implicit or explicit constraints in `protocols/<protocol>/constraints/`. |
| `implementation.schema.json` | Implementation/build target records in `protocols/<protocol>/implementations/`. |
| `protocol_profile.schema.json` | Per-protocol standard and selection profile. |
| `directions.example.json` | Seed direction examples, not the final T3 direction set. |

For field meaning and status rules, read `docs/data_format.md`.
