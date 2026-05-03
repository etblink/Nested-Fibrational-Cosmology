# L2 Pilot Comparison Report

**Status:** passed
**Failed checks:** 0

## Pilot matrix

| Pilot | Equivalence | Compile | Posture | Frontier preserved | Supersession effect | Hardening |
|---|---|---|---|---|---|---|
| GR | passed | passed | `domain-bounded-cert-close` | True (`ob:GR.global-subcriticality`) | none; pilot shell only | passed |
| YM | passed | passed | `conditional-cert-close` | True (`ob:YM.B3.A2`) | none; pilot shell only | not-required-in-v22 |

## Checks

| Check | Status | Observed | Expected |
|---|---|---|---|
| `GR.equivalence_passed` | **pass** | `passed` | `passed` |
| `GR.compiled` | **pass** | `passed` | `passed` |
| `GR.posture_preserved` | **pass** | `domain-bounded-cert-close` | `domain-bounded-cert-close` |
| `GR.frontier_preserved` | **pass** | `['ob:GR.global-subcriticality']` | `ob:GR.global-subcriticality` |
| `GR.no_supersession` | **pass** | `none; pilot shell only` | `none; pilot shell only` |
| `GR.l2_hardening_passed` | **pass** | `{'status': 'passed', 'failed_count': 0}` | `{'status': 'passed', 'failed_count': 0}` |
| `YM.equivalence_passed` | **pass** | `passed` | `passed` |
| `YM.compiled` | **pass** | `passed` | `passed` |
| `YM.posture_preserved` | **pass** | `conditional-cert-close` | `conditional-cert-close` |
| `YM.frontier_preserved` | **pass** | `['ob:YM.B3.A2']` | `ob:YM.B3.A2` |
| `YM.no_supersession` | **pass** | `none; pilot shell only` | `none; pilot shell only` |
| `cross_pilot.distinct_closure_regimes` | **pass** | `{'GR': 'domain-bounded-cert-close', 'YM': 'conditional-cert-close'}` | `GR and YM postures remain distinct` |
| `cross_pilot.both_frontiers_in_computed_graph` | **pass** | `{'ob:GR.global-subcriticality': True, 'ob:YM.B3.A2': True}` | `both active frontier IDs exist in computed status graph` |

## Governance conclusion

GR and YM now constitute two L2 branch-successor pilots under a shared comparison standard. The comparison explicitly preserves their different closure regimes and keeps both terminal frontiers open. No supersession of the canonical branch books is authorized by this report.
