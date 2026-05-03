# L2 Pilot Standard Report

**Status:** passed
**Standard version:** 1.4
**Pilots checked:** 10
**Failed checks:** 0

| Branch | Status | Expected posture | Computed posture | Preserved frontiers | Frontier statuses | Compile | Equivalence | Supersession | Failed checks |
|---|---|---|---|---|---|---|---|---|---:|
| GR | **passed** | `domain-bounded-cert-close` | `domain-bounded-cert-close` | `['ob:GR.global-subcriticality']` | `{'ob:GR.global-subcriticality': 'O'}` | passed | passed | none; pilot shell only | 0 |
| YM | **passed** | `conditional-cert-close` | `conditional-cert-close` | `['ob:YM.B3.A2']` | `{'ob:YM.B3.A2': 'O'}` | passed | passed | none; pilot shell only | 0 |
| SPEC | **passed** | `cert-close` | `cert-close` | `[]` | `{}` | passed | passed | none; pilot shell only | 0 |
| SCC | **passed** | `conditional-cert-close` | `conditional-cert-close` | `[]` | `{}` | passed | passed | none; pilot shell only | 0 |
| CRYST | **passed** | `conditional-cert-close` | `conditional-cert-close` | `['ob:CRYST.phase-problem']` | `{'ob:CRYST.phase-problem': 'O'}` | passed | passed | none; pilot shell only | 0 |
| LING | **passed** | `conditional-cert-close` | `conditional-cert-close` | `['ob:LING.REF-INVIS-RECOV']` | `{'ob:LING.REF-INVIS-RECOV': 'O'}` | passed | passed | none; pilot shell only | 0 |
| BIO | **passed** | `conditional-cert-close` | `conditional-cert-close` | `['ob:BIO.BND-open']` | `{'ob:BIO.BND-open': 'O'}` | passed | passed | none; pilot shell only | 0 |
| SM | **passed** | `intrinsic-structural-close` | `intrinsic-structural-close` | `['ob:SM.O-IDcont']` | `{'ob:SM.O-IDcont': 'O'}` | passed | passed | none; pilot shell only | 0 |
| NS | **passed** | `domain-bounded-cert-close` | `domain-bounded-cert-close` | `['front:NS.main', 'ob:NS.bridge-stage2']` | `{'front:NS.main': 'O', 'ob:NS.bridge-stage2': 'O'}` | passed | passed | none; pilot shell only | 0 |
| RH | **passed** | `cert-proj` | `cert-proj` | `['ob:RH.S1-ARC', 'thm:RH.S1.formal']` | `{'ob:RH.S1-ARC': 'O', 'thm:RH.S1.formal': 'O'}` | None | passed | none; pilot shell only | 0 |

## Check details

| Check | Status | Observed | Expected |
|---|---|---|---|
| `GR.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `GR.compile_target_passed` | **pass** | `passed` | `passed` |
| `GR.expected_posture_preserved` | **pass** | `{'equivalence': 'domain-bounded-cert-close', 'computed': 'domain-bounded-cert-close'}` | `domain-bounded-cert-close` |
| `GR.expected_frontier_profile_preserved` | **pass** | `['ob:GR.global-subcriticality']` | `['ob:GR.global-subcriticality']` |
| `GR.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `GR.expected_active_frontiers_are_open` | **pass** | `{'ob:GR.global-subcriticality': 'O'}` | `all expected frontiers have effective status O` |
| `GR.successor_tex_present` | **pass** | `output/tex/gr_branch_successor_standalone.tex` | `exists` |
| `GR.successor_pdf_present` | **pass** | `output/pdf/gr_branch_successor_standalone.pdf` | `exists` |
| `GR.hardening_passed` | **pass** | `passed` | `passed` |
| `YM.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `YM.compile_target_passed` | **pass** | `passed` | `passed` |
| `YM.expected_posture_preserved` | **pass** | `{'equivalence': 'conditional-cert-close', 'computed': 'conditional-cert-close'}` | `conditional-cert-close` |
| `YM.expected_frontier_profile_preserved` | **pass** | `['ob:YM.B3.A2']` | `['ob:YM.B3.A2']` |
| `YM.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `YM.expected_active_frontiers_are_open` | **pass** | `{'ob:YM.B3.A2': 'O'}` | `all expected frontiers have effective status O` |
| `YM.successor_tex_present` | **pass** | `output/tex/ym_branch_successor_standalone.tex` | `exists` |
| `YM.successor_pdf_present` | **pass** | `output/pdf/ym_branch_successor_standalone.pdf` | `exists` |
| `SPEC.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `SPEC.compile_target_passed` | **pass** | `passed` | `passed` |
| `SPEC.expected_posture_preserved` | **pass** | `{'equivalence': 'cert-close', 'computed': 'cert-close'}` | `cert-close` |
| `SPEC.expected_frontier_profile_preserved` | **pass** | `[]` | `[]` |
| `SPEC.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `SPEC.expected_active_frontiers_are_open` | **pass** | `{}` | `all expected frontiers have effective status O` |
| `SPEC.successor_tex_present` | **pass** | `output/tex/spec_branch_successor_standalone.tex` | `exists` |
| `SPEC.successor_pdf_present` | **pass** | `output/pdf/spec_branch_successor_standalone.pdf` | `exists` |
| `SCC.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `SCC.compile_target_passed` | **pass** | `passed` | `passed` |
| `SCC.expected_posture_preserved` | **pass** | `{'equivalence': 'conditional-cert-close', 'computed': 'conditional-cert-close'}` | `conditional-cert-close` |
| `SCC.expected_frontier_profile_preserved` | **pass** | `[]` | `[]` |
| `SCC.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `SCC.expected_active_frontiers_are_open` | **pass** | `{}` | `all expected frontiers have effective status O` |
| `SCC.successor_tex_present` | **pass** | `output/tex/scc_branch_successor_standalone.tex` | `exists` |
| `SCC.successor_pdf_present` | **pass** | `output/pdf/scc_branch_successor_standalone.pdf` | `exists` |
| `CRYST.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `CRYST.compile_target_passed` | **pass** | `passed` | `passed` |
| `CRYST.expected_posture_preserved` | **pass** | `{'equivalence': 'conditional-cert-close', 'computed': 'conditional-cert-close'}` | `conditional-cert-close` |
| `CRYST.expected_frontier_profile_preserved` | **pass** | `['ob:CRYST.phase-problem']` | `['ob:CRYST.phase-problem']` |
| `CRYST.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `CRYST.expected_active_frontiers_are_open` | **pass** | `{'ob:CRYST.phase-problem': 'O'}` | `all expected frontiers have effective status O` |
| `CRYST.successor_tex_present` | **pass** | `output/tex/cryst_branch_successor_standalone.tex` | `exists` |
| `CRYST.successor_pdf_present` | **pass** | `output/pdf/cryst_branch_successor_standalone.pdf` | `exists` |
| `LING.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `LING.compile_target_passed` | **pass** | `passed` | `passed` |
| `LING.expected_posture_preserved` | **pass** | `{'equivalence': 'conditional-cert-close', 'computed': 'conditional-cert-close'}` | `conditional-cert-close` |
| `LING.expected_frontier_profile_preserved` | **pass** | `['ob:LING.REF-INVIS-RECOV']` | `['ob:LING.REF-INVIS-RECOV']` |
| `LING.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `LING.expected_active_frontiers_are_open` | **pass** | `{'ob:LING.REF-INVIS-RECOV': 'O'}` | `all expected frontiers have effective status O` |
| `LING.successor_tex_present` | **pass** | `output/tex/ling_branch_successor_standalone.tex` | `exists` |
| `LING.successor_pdf_present` | **pass** | `output/pdf/ling_branch_successor_standalone.pdf` | `exists` |
| `BIO.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `BIO.compile_target_passed` | **pass** | `passed` | `passed` |
| `BIO.expected_posture_preserved` | **pass** | `{'equivalence': 'conditional-cert-close', 'computed': 'conditional-cert-close'}` | `conditional-cert-close` |
| `BIO.expected_frontier_profile_preserved` | **pass** | `['ob:BIO.BND-open']` | `['ob:BIO.BND-open']` |
| `BIO.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `BIO.expected_active_frontiers_are_open` | **pass** | `{'ob:BIO.BND-open': 'O'}` | `all expected frontiers have effective status O` |
| `BIO.successor_tex_present` | **pass** | `output/tex/bio_branch_successor_standalone.tex` | `exists` |
| `BIO.successor_pdf_present` | **pass** | `output/pdf/bio_branch_successor_standalone.pdf` | `exists` |
| `SM.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `SM.compile_target_passed` | **pass** | `passed` | `passed` |
| `SM.expected_posture_preserved` | **pass** | `{'equivalence': 'intrinsic-structural-close', 'computed': 'intrinsic-structural-close'}` | `intrinsic-structural-close` |
| `SM.expected_frontier_profile_preserved` | **pass** | `['ob:SM.O-IDcont']` | `['ob:SM.O-IDcont']` |
| `SM.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `SM.expected_active_frontiers_are_open` | **pass** | `{'ob:SM.O-IDcont': 'O'}` | `all expected frontiers have effective status O` |
| `SM.successor_tex_present` | **pass** | `output/tex/sm_branch_successor_standalone.tex` | `exists` |
| `SM.successor_pdf_present` | **pass** | `output/pdf/sm_branch_successor_standalone.pdf` | `exists` |
| `NS.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `NS.compile_target_passed` | **pass** | `passed` | `passed` |
| `NS.expected_posture_preserved` | **pass** | `{'equivalence': 'domain-bounded-cert-close', 'computed': 'domain-bounded-cert-close'}` | `domain-bounded-cert-close` |
| `NS.expected_frontier_profile_preserved` | **pass** | `['ob:NS.bridge-stage2', 'front:NS.main']` | `['front:NS.main', 'ob:NS.bridge-stage2']` |
| `NS.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `NS.expected_active_frontiers_are_open` | **pass** | `{'front:NS.main': 'O', 'ob:NS.bridge-stage2': 'O'}` | `all expected frontiers have effective status O` |
| `NS.successor_tex_present` | **pass** | `output/tex/ns_branch_successor_standalone.tex` | `exists` |
| `NS.successor_pdf_present` | **pass** | `output/pdf/ns_branch_successor_standalone.pdf` | `exists` |
| `RH.equivalence_report_passed` | **pass** | `passed` | `passed` |
| `RH.compile_target_passed` | **pass** | `pdf_exists` | `passed` |
| `RH.expected_posture_preserved` | **pass** | `{'equivalence': 'cert-proj', 'computed': 'cert-proj'}` | `cert-proj` |
| `RH.expected_frontier_profile_preserved` | **pass** | `['ob:RH.S1-ARC', 'thm:RH.S1.formal']` | `['ob:RH.S1-ARC', 'thm:RH.S1.formal']` |
| `RH.no_supersession_effect` | **pass** | `none; pilot shell only` | `['none', 'none; pilot shell only']` |
| `RH.expected_active_frontiers_are_open` | **pass** | `{'ob:RH.S1-ARC': 'O', 'thm:RH.S1.formal': 'O'}` | `all expected frontiers have effective status O` |
| `RH.successor_tex_present` | **pass** | `output/tex/rh_branch_successor_standalone.tex` | `exists` |
| `RH.successor_pdf_present` | **pass** | `output/pdf/rh_branch_successor_standalone.pdf` | `exists` |
