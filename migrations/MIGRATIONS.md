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
| MIG-008 | 5 stale-repair | NFC_SPEC_Branch.tex | prop:spec-current-status + its subsection title | SUPERSEDED (B-1) | review ruling B-1; A1 prop:SPEC-status | none (label + [C] preserved) | none | validate pass; compile pass |
| MIG-009 | 5 stale-repair | NFC_SCC_Branch.tex | front-block status, rmk:scc-status-vocab, prop:scc-status, boundary, dep-ledger R1+status rows | SUPERSEDED (C-2) | review ruling C-2; A3 thm:scc-mcs-full/uc/tsi | none (all labels preserved) | prop:scc-status [U]->[C] (weakening/correction, authorized) | validate pass; compile pass |
| MIG-010 | 5 stale-repair | NFC_SCC_Branch.tex | thm:scc-r1 Reserved/[C] contradiction; thm:scc-frontier item (i) | SUPERSEDED (C-2) | review ruling C-2 | none (thm:scc-r1 label + [C] preserved) | none (thm:scc-r1 already [C]; reconciled prose to its completed proof) | validate pass; compile pass |
| MIG-011 | 5 stale-repair | NFC_NS_Branch.tex | dormant post-\end{document} remark | SUPERSEDED (D-3) | review ruling D-3; A1 prop:NS-status | none | none | validate pass; compile pass. Note: this remark is after \end{document} (does not render); corrected for source consistency. In-body prop:NS-status already current. |
| MIG-012 | 6 spine-table | NFC_Book_VII.tex | sec:status-table SM row + 4 added branch rows; irreducible-frontier list | SUPERSEDED (F-6,F-9) | review ruling F-6; each branch A1 | none | none (table text, not \status) | validate pass; compile pass |
| MIG-013 | 6 spine-text | NFC_Book_VII.tex | "currently 13 items" -> dated + roster pointer | HISTORICAL (F-8) | review ruling F-8; NFC_OBLIGATION_ROSTER.md | none | none | validate pass; compile pass |
