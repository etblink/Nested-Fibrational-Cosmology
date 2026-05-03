# Book VII L4 Spine Equivalence Certificate

**NFC Governance Engine — Book VII Spine L4 Release Candidate**

**L4 gate:** ✅ PASSED (9/9 criteria)
**All governance theorems [U]:** True
**Session L+6 additions present:** True
**Governance rule mapping complete:** True
**Prose completeness:** 100.0%
**Supersession effect:** none

> The governance engine auditing its own canonical source: Book VII's theorems are implemented as governance_rules.yaml checks. This certificate verifies the correspondence between the canonical source and the executable implementation.

## L4 Criteria

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l4.vii.expected-claims` | ✅ | {'present': 19, 'missing': []} | All Book VII pilot claims present |
| `l4.vii.all-governance-unconditional` | ✅ | all [U] | All governance theorems must be [U] — conditional governance |
| `l4.vii.l6-additions-present` | ✅ | all present | Session L+6 additions (discharge-modes, declared-effective-a |
| `l4.vii.governance-rule-mapping` | ✅ | all rules mapped | Each governance_rules.yaml rule must map to a canonical Book |
| `l4.vii.prose-completeness` | ✅ | 100.0% (19/19) | >= 90% prose completeness |
| `l4.vii.xref-annotations` | ✅ | 19/19 | >= 17 xref annotations |
| `l4.vii.no-open-obligations` | ✅ | none | Book VII must have no open obligations — all governance rule |
| `l4.vii.governing-theorem` | ✅ | present=True, status=U | thm:VII.governing present and [U] |
| `l4.vii.governance-engine-implements-vii` | ✅ | Implemented: ['rule.claim.must-have-core-fields', 'rule.depe | >= 6 of 5 Book VII rules implemented in governance engine |

## Governance Rule to Book VII Theorem Mapping

| Governance Rule | Machine ID | Canonical Theorem |
|-----------------|------------|-------------------|
| `rule.claim.must-have-core-fields` | `sr:VII.declare-status` ✅ | `sr:declare-status` |
| `rule.dependencies.must-resolve` | `prop:VII.cite-declared-force` ✅ | `prop:cite-declared-force` |
| `rule.no-hidden-promotion` | `thm:VII.2.5` ✅ | `thm:promotion-requires-transfer` |
| `rule.scope-widening-requires-transfer` | `thm:VII.2.4` ✅ | `thm:scoped-cert-rule` |
| `rule.frontier-stability` | `thm:VII.4.3` ✅ | `thm:frontier-stability` |
| `rule.no-retired-alias-in-active-record` | `sr:VII.declare-status` ✅ | `sr:declare-status` |
| `rule.posture-must-match-claim-graph` | `rmk:VII.posture-vs-force` ✅ | `rmk:posture-vs-force` |
| `rule.non-retroactivity` | `thm:VII.non-retroactive` ✅ | `thm:non-retroactive` |

## Session L+6 Additions

| Machine ID | Name | Note |
|------------|------|------|
| `def:VII.discharge-modes` ✅ | Discharge Mode Taxonomy | Added Session L+6 |
| `def:VII.declared-effective-audit` ✅ | Declared/Effective/Audit Trichotomy | Added Session L+6 |
| `prop:VII.stale-label-correction` ✅ | Stale-Label Correction | Added Session L+6 |
| `rmk:VII.posture-vs-force` ✅ | Branch Posture vs. Claim-Force | Added Session L+6 |

## Structural Closure Note

Book VII is the one book in the corpus that cannot have a conditional theorem without undermining the governance framework itself. A conditional governance rule would leave branches uncertain whether the rule applies to them, violating the spine's role as the universal source of canonical force. All Book VII theorem-like objects are therefore [U] or [D] — never [C] or [O].
