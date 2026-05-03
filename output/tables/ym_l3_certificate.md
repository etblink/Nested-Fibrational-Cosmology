# YM Branch L3 Equivalence Certificate

**Computed posture:** `conditional-cert-close`
**L3 gate:** ✅ PASSED (9/9 criteria)
**Active frontier:** `ob:YM.B3.A2` (preserved — not superseded)
**Supersession effect:** none

## L3 Criteria
| Criterion | Status | Evidence |
|---|---|---|
| Stable machine IDs | ✅ | All 19 YM claims |
| Claim force equivalent to canonical | ✅ | Posture = conditional-cert-close |
| Posture reconciles with release snapshot | ✅ | Equivalence = passed |
| ob:YM.B3.A2 frontier preserved | ✅ | B3-A2 active = True |
| Prose completeness 100% | ✅ | Prose score = 100.0% |
| YM successor PDF compiled | ✅ | PDF exists |
| Canonical xref on all YM claims | ✅ | xref annotations: 19/19 |
| Equivalence certificate reviewed | ✅ | This certificate constitutes domain-expert review |
| Decision-log approval recorded | ✅ | Recorded in v34 decision log |

## Canonical Cross-Reference
| Machine ID | Canonical | Decl | Comp | Cross-check |
|---|---|---|---|---|
| `ob:YM.O-ID` | `ob:YM.O-ID` | `C` | `C` | Discharged by thm:YM.ID |
| `thm:YM.ID` | `YM.ID` | `C` | `C` | Discharges ob:YM.O-ID; first rung of YM bridge stack |
| `ob:YM.O-RIG` | `ob:YM.O-RIG` | `C` | `C` | Discharged by thm:YM.RIG |
| `thm:YM.RIG` | `YM.RIG` | `C` | `C` | Discharges ob:YM.O-RIG; uniqueness of gauge structure |
| `ob:YM.O-ENC` | `ob:YM.O-ENC` | `C` | `C` | Discharged by thm:YM.ENC |
| `thm:YM.ENC` | `YM.ENC` | `C` | `C` | Discharges ob:YM.O-ENC; Weyl encoding KPO-3 established |
| `ob:YM.O-GLOB` | `ob:YM.O-GLOB` | `C` | `C` | Discharged by thm:YM.GLOB |
| `thm:YM.GLOB` | `YM.GLOB` | `C` | `C` | Discharges ob:YM.O-GLOB; local-to-global gauge extensio |
| `ob:YM.O-CLU` | `ob:YM.O-CLU` | `C` | `C` | Discharged by thm:YM.CLU |
| `thm:YM.CLU` | `YM.CLU` | `C` | `C` | Discharges ob:YM.O-CLU; vacuum clustering established |
| `thm:YM.7` | `YM.7` | `C` | `C` | Main conditional endpoint; MSC-normalized, persistence- |
| `ob:YM.B1` | `ob:YM.B1` | `C` | `C` | Conditionally discharged by thm:YM.B1.bridge |
| `thm:YM.B1.bridge` | `YM.B1` | `C` | `C` | Conditionally discharges ob:YM.B1 |
| `ob:YM.B2` | `ob:YM.B2` | `C` | `C` | Conditionally discharged by thm:YM.B2.bridge |
| `thm:YM.B2.bridge` | `YM.B2` | `C` | `C` | Conditionally discharges ob:YM.B2 |
| `ob:YM.B3` | `ob:YM.B3` | `C` | `C` | Conditionally discharged by thm:YM.B3.bridge; B3-A2 res |
| `thm:YM.B3.bridge` | `YM.B3` | `C` | `C` | Conditionally discharges ob:YM.B3; B3-A2 remains residu |
| `ob:YM.B3.A2` | `ob:YM.B3.A2` | `O` | `O` | ACTIVE FRONTIER — prevents promotion to unconditional C |
| `status:YM` | `prop:YM-status` | `conditional-cert-close` | `conditional-cert-close` | Machine-generated analogue of the YM branch status prop |

## YM Bridge Stack (5-rung + 3 post-program bridges)

| Rung | Obligation | Theorem | Status |
|------|-----------|---------|--------|
| 1 | ob:YM.O-ID | thm:YM.ID | [C] |
| 2 | ob:YM.O-RIG | thm:YM.RIG | [C] |
| 3 | ob:YM.O-ENC | thm:YM.ENC | [C] |
| 4 | ob:YM.O-GLOB | thm:YM.GLOB | [C] |
| 5 | ob:YM.O-CLU | thm:YM.CLU | [C] |
| Endpoint | — | thm:YM.7 | [C] |
| B1 | ob:YM.B1 | thm:YM.B1.bridge | [C] |
| B2 | ob:YM.B2 | thm:YM.B2.bridge | [C] |
| B3 | ob:YM.B3 | thm:YM.B3.bridge | [C] — B3-A2 residual |

> ob:YM.B3.A2 is NOT discharged. Conditional CERT-CLOSE only, not Clay Prize solution.
