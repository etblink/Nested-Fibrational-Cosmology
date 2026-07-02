# NFC Canon Migration Log

Every canon-facing change in Phase 7 is recorded here: what changed, where, why, the authority that licenses it, whether any label/status was touched, and the edit-gate result. Scaffold-only changes are noted but the canon `.tex` changes are the load-bearing entries.

**Invariants enforced on every entry:**
- No new discharge claim; no status promotion unsupported by an existing proposition.
- Labels preserved (any label touch is listed explicitly and was pre-authorized).
- PDFs regenerated only from edited `.tex`.
- Edit gate = `make validate` (labels/refs/cycles/census) + compile; any failure blocks the entry.

Authority tiers refer to `CANON_AUTHORITY_MODEL.md`. Ruling IDs refer to the July 2 2026 review adjudication.

| ID | phase-step | file | location (label) | class | authority basis | labels touched | status touched | gate |
|---|---|---|---|---|---|---|---|---|
| MIG-001 | 1 scaffold | NFC_CANON_LEDGER.md | PART 4 SM entry | SUPERSEDED (F-1) | A1 `prop:SM-status-reconciliation` | none (scaffold .md) | none | validate pass; no canon .tex touched |
| MIG-002 | 1 scaffold | NFC_CANON_LEDGER.md | PART 4 YM obligation block | SUPERSEDED (F-2) | A3 branch body tags + `prop:YM-status` | none (scaffold .md) | none | validate pass; no canon .tex touched |
| MIG-003 | 1 scaffold | NFC_STATE_OF_CANON.md | corpus overview count table + counting note | SUPERSEDED (F-3) | review ruling F-3 + `metadata/census.json` | none (scaffold .md) | none | validate pass; census unchanged |
| MIG-004 | 2 canon-comment | all 17 NFC_*.tex | `%%` status legend block | SUPERSEDED (F-4) | Canon Ledger PART 1 6-code vocabulary | none | none (comment only) | validate pass; census unchanged; compile pass (spot-checked Book I, SPEC) |
| MIG-005 | 4 canon front-matter | BIO,CRYST,LING,SPEC,YM,SCC .tex | `%%` header status line | SUPERSEDED (A-1..A-4,A-7,A-8) | each branch's A1 status prop | none | none (comment header; old text retained as intake) | validate pass; compile pass |
| MIG-006 | 4 canon front-matter | BIO,CRYST,LING,SPEC .tex | `\author{...Prospective Derived Branch}` + `%%` l.2 | HISTORICAL (A-5,A-6) | review ruling "Constituted Derived Branch" | none | none | validate pass; compile pass; PDF title renders "Constituted Derived Branch" |
| MIG-007 | 3 canon capsules | all 17 NFC_*.tex | new `cap:<file>-status` [R] remark after \tableofcontents | ADD (Phase 3 Rule 2) | branch A1 status props / spine governance; pointers verified present | +17 new `cap:` labels (unique, verified) | +17 [R] only (349->366); no D/U/C/B/O change; no existing status touched | validate pass (0 dangling, 0 cycles); compile pass all 17; census baseline updated |
