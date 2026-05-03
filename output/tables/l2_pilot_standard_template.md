# L2 Pilot Standard Template

A configured L2 branch-successor pilot must provide the following fields and pass the following checks.

## Required pilot fields

- `branch`
- `status_id`
- `generator`
- `tex_target`
- `pdf_target`
- `compile_target_id`
- `equivalence_report`
- `expected_posture`
- `expected_frontiers`
- `must_not_claim`
- `supersession_effect_allowed`

## Required checks

- `equivalence_report_passed`
- `compile_target_passed`
- `expected_posture_preserved`
- `expected_frontier_profile_preserved`
- `no_supersession_effect`
- `expected_active_frontiers_are_open`
- `successor_tex_present`
- `successor_pdf_present`

## Current configured pilots

- **GR**: posture `domain-bounded-cert-close`, frontiers `['ob:GR.global-subcriticality']`
- **YM**: posture `conditional-cert-close`, frontiers `['ob:YM.B3.A2']`
- **SPEC**: posture `cert-close`, frontiers `[]`
- **SCC**: posture `conditional-cert-close`, frontiers `[]`
- **CRYST**: posture `conditional-cert-close`, frontiers `['ob:CRYST.phase-problem']`
- **LING**: posture `conditional-cert-close`, frontiers `['ob:LING.REF-INVIS-RECOV']`
- **BIO**: posture `conditional-cert-close`, frontiers `['ob:BIO.BND-open']`
- **SM**: posture `intrinsic-structural-close`, frontiers `['ob:SM.O-IDcont']`
- **NS**: posture `domain-bounded-cert-close`, frontiers `['front:NS.main', 'ob:NS.bridge-stage2']`
- **RH**: posture `cert-proj`, frontiers `['ob:RH.S1-ARC', 'thm:RH.S1.formal']`
