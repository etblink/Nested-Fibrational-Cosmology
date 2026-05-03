# v30 — SM Branch-Successor Pilot

## Summary

v30 implements the SM (Standard Model) branch-successor pilot, the eighth
L2 generated branch-pilot in the NFC governance engine, and the first to
exercise the `intrinsic-structural-close` posture.

## What changed

- Schema bumped to **0.30.0**
- Added 11 new SM claim records:
  - Obligation records: `ob:SM.harmonization`, `ob:SM.matter`,
    `ob:SM.higgs`, `ob:SM.coupling-transfer`
  - Theorem records: `thm:SM.gauge-chain`, `thm:SM.three-gen` [U],
    `thm:SM.harmonization-partial`, `thm:SM.coupling-transfer-full`,
    `thm:SM.higgs-source-descended`
  - Proposition records: `prop:SM.intrinsic-closure`,
    `prop:SM.status-reconciliation`
  - (Existing: `thm:SM.18.1`, `ob:SM.O-IDcont`, `status:SM` — updated)
- Updated `canon/inference_rules.yaml` for SM
- Added `build/sm_branch_successor.py`
- Added SM to all governance configs
- Fixed latent validator issue: `thm:SM.three-gen` [U] cannot depend
  on a [C] theorem; removed the conditional dependency — the three-generation
  count is genuinely unconditional from the NFC-3Gen structural argument

## Build result

| Metric | Value |
|--------|-------|
| Schema version | 0.30.0 |
| Claims | 91 (+11 new SM records) |
| Errors | 0 |
| Warnings | 2 (intentional retired-alias detections) |
| Quality gate | **passed** |
| Regression tests | **passed** |
| SM successor equivalence | **passed** |
| SM successor compile | **passed** (9 PDFs total, all rendered) |

## What makes SM different from all prior pilots

### The new posture: intrinsic-structural-close

Every prior pilot used one of: `cert-close` (SPEC), `conditional-cert-close`
(YM, SCC, CRYST, LING, BIO), or `domain-bounded-cert-close` (GR).

`intrinsic-structural-close` is a new posture meaning:
- The four SM-internal obligations (harmonization, matter, Higgs, coupling
  transfer) are **conditionally discharged at structural level**
- The SM branch is **strictly stronger than CERT-PROJ** (the old posture)
- But it is **strictly weaker than conditional-cert-close** because:
  - Inherited YM/GR scope limitations propagate to SM
  - O-IDcont force upgrade is still required for unconditional closure

### The status inequality

The governing constraint, now machine-checked:

```
Status(SM) ≤ Status(YM) ∧ Status(GR) ∧ Status(SM_intrinsic)
```

Current values: SM = `intrinsic-structural-close`,
YM = `conditional-cert-close`, GR = `domain-bounded-cert-close`.
The inequality holds.

### The discharge mode exercise

The SM pilot exercises `partial` and `scoped` discharge modes
(from the Discharge Mode Taxonomy added in Session L+6):
- `thm:SM.harmonization-partial` issues a **partial** discharge of
  `ob:SM.harmonization` — the KPO functor exists but the matter
  extension is pending
- `thm:SM.higgs-source-descended` and `thm:SM.coupling-transfer-full`
  issue **scoped** discharges — valid on their declared sub-regimes
  but not at full class force

## Governance invariants preserved

| Check | Result |
|-------|--------|
| Posture | `intrinsic-structural-close` ✓ |
| ob:SM.O-IDcont open | true ✓ |
| Status inequality | SM ≤ YM ∧ GR ✓ |
| No cert-close claimed | ✓ |
| No measured masses/CKM/PMNS | ✓ |
| No RG-running derivation | ✓ |
| No full empirical SM | ✓ |
| No gauge-gravity unification | ✓ |

## Updated L2 pilot portfolio

| Branch | Posture | Active frontier |
|--------|---------|----------------|
| GR | domain-bounded-cert-close | ob:GR.global-subcriticality |
| YM | conditional-cert-close | ob:YM.B3.A2 |
| SPEC | cert-close | — |
| SCC | conditional-cert-close | — |
| CRYST | conditional-cert-close | ob:CRYST.phase-problem |
| LING | conditional-cert-close | ob:LING.REF-INVIS-RECOV |
| BIO | conditional-cert-close | ob:BIO.BND-open |
| **SM** | **intrinsic-structural-close** | **ob:SM.O-IDcont** |

All five posture types in the branch posture vocabulary are now exercised:
cert-close (SPEC), conditional-cert-close (YM/SCC/CRYST/LING/BIO),
domain-bounded-cert-close (GR), intrinsic-structural-close (SM).
Remaining: frontier-blocked (NS) and cert-proj (RH).

## Recommended next milestone

**v31 — NS Branch-Successor Pilot**

NS is next in the intake queue. It exercises the `frontier-blocked` posture
and the partial-discharge semantics at the deepest level: `front:NS.main`
and `ob:NS.SB2` must remain active, and the pilot must represent
the NS branch as genuinely blocked rather than conditionally approaching
closure. Risk band remains high, but the partial-discharge machinery
(exercised in SM v30) is now better proven.
