# Supersession Readiness Report

**Schema version:** 0.43.0
**Current supersession level:** L2
**Recommended next level:** L2-generator-hardening
**L1 import-ready:** True
**L2 pilot-ready:** True
**Full corpus supersession-ready:** False
**Approved for full supersession:** False

## Readiness checks

| Check | Required for | Status | Evidence |
|---|---|---|---|
| `sup.audit.zero-errors` Governance audit has zero errors | L1+ | **pass** | errors=0, warnings=3 |
| `sup.import.packet` Canon-import appendix packet exists | L1+ | **pass** | status=generated |
| `sup.compile.packet` Standalone governance appendix compiles | L1+ | **pass** | status=passed, pages=7 |
| `sup.release.diff-basis` Release-diff changes carry basis notes | L1+ | **pass** | changes=5, missing_basis=0 |
| `sup.regression` Regression baseline passes | L1+ | **pass** | status=passed, failed_count=0 |
| `sup.gr.pilot` GR pilot locally infers current posture | L2+ | **pass** | computed_posture=domain-bounded-cert-close |
| `sup.ym.pilot` YM pilot locally infers current posture | L2+ | **pass** | computed_posture=conditional-cert-close |
| `sup.gr.successor-packet` GR generated branch-successor shell passes equivalence and compile checks | L2+ | **pass** | status=passed, computed_posture=domain-bounded-cert-close, pages=5 |
| `sup.full-claim-equivalence` Full current-corpus claim catalog equivalence | L5 | **not-started** | No full spine/branch claim equivalence audit has been run. |
| `sup.full-prose-migration` Full theorem/proof prose migrated into structured source | L5 | **not-started** | Human-authored theorem bodies remain outside the generated successor corpus. |
| `sup.full-pdf-corpus` All successor books compile as generated PDFs | L5 | **not-started** | Only the governance appendix compiles in v18. |
| `sup.human-release-approval` Formal supersession decision recorded | L5 | **not-started** | No decision log entry approves full corpus supersession. |

## Interpretation

v19 supports an L2 GR branch-successor pilot in addition to generated governance appendices. It does not authorize replacement of the current spine or branch books.

The next prudent milestone is L2 hardening: improve GR equivalence coverage, review migrated prose preservation, and only then consider a YM successor pilot.
