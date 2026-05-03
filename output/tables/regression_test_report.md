# Regression Test Report

**Status:** passed
**Tests:** 11
**Failures:** 0

| Test | Status | Observed | Expected |
|---|---:|---|---|
| `regression.schema_version` | pass | `"0.43.0"` | `"0.43.0"` |
| `regression.claims` | pass | `243` | `243` |
| `regression.computed_statuses` | pass | `243` | `243` |
| `regression.errors` | pass | `0` | `0` |
| `regression.release_diff_changes` | pass | `5` | `5` |
| `regression.release_diff_missing_basis` | pass | `0` | `0` |
| `regression.warnings_max` | pass | `3` | `3` |
| `regression.warning_types` | pass | `["release-vs-computed-posture-mismatch", "retired-alias-detected"]` | `["release-vs-computed-posture-mismatch", "retired-alias-detected"]` |
| `regression.active_open_items` | pass | `["front:NS.main", "ob:BIO.BND-open", "ob:CRYST.phase-problem", "ob:GR.global-subcriticality", "ob:LING.REF-INVIS-RECOV", "ob:NS.bridge-stage2", "ob:RH.S1-ARC", "ob:SM.O-IDcont", "ob:YM.B3.A2", "thm:RH.S1.formal"]` | `["front:NS.main", "ob:BIO.BND-open", "ob:CRYST.phase-problem", "ob:GR.global-subcriticality", "ob:LING.REF-INVIS-RECOV", "ob:NS.bridge-stage2", "ob:RH.S1-ARC", "ob:SM.O-IDcont", "ob:YM.B3.A2", "thm:RH.S1.formal"]` |
| `regression.branch_postures` | pass | `"all matched"` | `{"BIO": "conditional-cert-close", "CRYST": "conditional-cert-close", "GR": "domain-bounded-cert-close", "LING": "conditional-cert-close", "NS": "domain-bounded-cert-close", "RH": "cert-proj", "SCC": "conditional-cert-close", "SM": "intrinsic-structural-close", "SPEC": "cert-close", "YM": "conditional-cert-close"}` |
| `regression.protected_claim_statuses` | pass | `"all matched"` | `{"front:NS.main": "O", "ob:GR.global-subcriticality": "O", "ob:RH.S1-ARC": "O", "ob:SM.O-IDcont": "O", "ob:YM.B3.A2": "O", "prop:NS.status": "C", "prop:SM.intrinsic-closure": "C", "status:RH": "cert-proj", "thm:GR.domain": "C", "thm:NS.7.1": "C", "thm:RH.S1.formal": "O", "thm:SCC.MCS": "C", "thm:SCC.TSI": "C", "thm:SCC.UC": "C", "thm:YM.7": "C"}` |
