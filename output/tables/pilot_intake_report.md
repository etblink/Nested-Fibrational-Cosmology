# L2 Pilot Intake Report

**Status:** passed
**Schema version:** 0.28.0
**Current L2 pilots:** GR, YM, SPEC, SCC, CRYST, LING, BIO, SM, NS, RH
**Recommended next pilot:** `BIO`

## Recommendation rationale

BIO L2 pilot completed in v29; retained for portfolio history.

## Ranked candidates

| Rank | Branch | Score | Current posture | Computed posture | Canon value | Readiness | Risk | Blocked |
|---:|---|---:|---|---|---|---|---|---|
| 1 | `BIO` | 5.0 | `conditional-cert-close` | `conditional-cert-close` | medium-high | medium | medium-high | False |
| 2 | `NS` | 4.5 | `frontier-blocked` | `domain-bounded-cert-close` | very-high | low-medium | high | True |
| 3 | `SM` | 4.5 | `intrinsic-structural-close` | `intrinsic-structural-close` | very-high | medium-low | high | False |
| 4 | `CRYST` | 2.5 | `conditional-cert-close` | `conditional-cert-close` | medium-high | complete | medium | False |
| 5 | `LING` | 2.5 | `conditional-cert-close` | `conditional-cert-close` | medium-high | complete | medium | False |
| 6 | `RH` | 2.0 | `cert-proj` | `cert-proj` | very-high | low | very-high | False |

## Required successor checks for recommended branch

- preserve C_Bio^nd scope
- preserve BND/full-class limitation
- avoid primitive genes/cells/fitness import

## Project Lead policy notes

- **avoid_next_pilot_if:** requires full proof-prose migration before value is visible, would imply global supersession, depends on unsettled branch posture vocabulary
- **do_not_expand_if_quality_gate_fails:** True
- **prefer_next_pilot_with:** high canonical leverage, manageable frontier profile, available local records, limited supersession risk
