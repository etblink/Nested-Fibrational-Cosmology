# Book V L4 Equivalence Certificate

**L4 gate:** ✅ PASSED (10/10 criteria)
**UBLT (Thm. V.8.1):** `[U]` | **Branch projection (Prop. V.3.1):** `[U]`
**All primary [U]:** True | **Open branch = lawful:** True

> Closes the machine-readable dependency gap between the spine and the branch books. Branch books cite thm:V.UBLT (= Thm. V.8.1) and prop:V.branch-projection (= Prop. V.3.1). With Book V machine records, the governance engine can now trace the full branch-to-spine dependency chain.

## L4 Criteria
| Check | Status | Observed |
|-------|--------|----------|
| `l4.v.UBLT-present-and-U` | ✅ | thm:V.UBLT status = U |
| `l4.v.branch-projection-U` | ✅ | prop:V.branch-projection (Prop. V.3.1) status = U |
| `l4.v.primary-results-unconditional` | ✅ | all [U] |
| `l4.v.open-branch-canonical-U` | ✅ | cor:V.open-branch-still-canonical status = U |
| `l4.v.standing-rules-present` | ✅ | all present |
| `l4.v.screened-sector-conditional` | ✅ | status = C, constraints = ['PASS', 'LS-2', 'Phase-A', 'K0-7'] |
| `l4.v.mandatory-declarations` | ✅ | present |
| `l4.v.branch-spine-linkage` | ✅ | thm:VII.6.4 canonical cross-reference documents the Book V dependency |
| `l4.v.prose-completeness` | ✅ | 100.0% (19/19) |
| `l4.v.xref-annotations` | ✅ | 19/19 |

## Branch-Spine Dependency Linkage

Branches citing thm:V.UBLT: `GR`, `YM`, `NS`, `SM`, `BIO`, `LING`, `CRYST`, `SCC`, `SPEC`, `RH`

Dependency chain example: `thm:GR.domain → thm:VII.6.4 → thm:V.UBLT → def:V.branch-candidate → ...`
