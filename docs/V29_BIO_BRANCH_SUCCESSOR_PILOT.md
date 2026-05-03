# v29 — BIO Branch-Successor Pilot

## Summary

v29 implements the BIO (Biology) branch-successor pilot, the seventh L2
generated branch-pilot in the NFC governance engine.

## What changed

- Schema bumped to **0.29.0**
- Added 14 new BIO claim records across the full discharge chain:
  - Obligation records: `ob:BIO.REP`, `ob:BIO.MET`, `ob:BIO.FID`, `ob:BIO.NC`,
    `ob:BIO.HER`, `ob:BIO.BND`
  - Theorem records: `thm:BIO.REP`, `thm:BIO.MET`, `thm:BIO.FID`, `thm:BIO.NC`,
    `thm:BIO.HER`, `thm:BIO.BND`, `thm:BIO.END` (expanded), `thm:BIO.MULTI.twocell`
  - Frontier record: `ob:BIO.BND-open` (BND for the full replicator class — ACTIVE, OPEN)
- Added `build/bio_branch_successor.py`
- Added BIO to `canon/pilot_standard.yaml` and `canon/pilot_intake.yaml`
- Updated `canon/inference_rules.yaml` to require `ob:BIO.BND-open == O` for
  BIO conditional-cert-close inference
- Added `gate.bio_successor_pilot` to `build/quality_gate.py`
- Added BIO compile target to `build/compile_check.py`
- Added `build/build.py` step for bio_branch_successor

## Build result

| Metric | Value |
|--------|-------|
| Schema version | 0.29.0 |
| Claims | 80 |
| Computed statuses | 80 |
| Warnings | 2 (intentional retired-alias detections) |
| Errors | 0 |
| BIO successor equivalence | passed |
| BIO successor compile | passed |
| Quality gate | passed |

## BIO pilot result

The generated BIO packet preserves all required governance invariants:

| Check | Result |
|-------|--------|
| Posture | `conditional-cert-close` ✓ |
| Endpoint scope | `nondegenerate-bio` (C_Bio^nd only) ✓ |
| Active frontier | `ob:BIO.BND-open` preserved ✓ |
| BND frontier preserved | true ✓ |
| No evolutionary cert-close claimed | ✓ |
| No full-class biology cert-close claimed | ✓ |
| No biological primitives smuggled | ✓ |

## Governance boundary conditions

### What BIO conditional-cert-close means here

BIO reaches its endpoint on the **nondegenerate certified biological class**
`C_Bio^nd`. The obligations REP, MET, FID, NC, HER are conditionally discharged
at this scope. BND is conditionally discharged on the nondegenerate regime only.

### What it does NOT mean

- Evolutionary closure (`ob:BIO.EVO`) is **not** claimed
- Full multicellular organization (`ob:BIO.MULTI`) is **not** claimed
- Full-class BND is **not** claimed — `ob:BIO.BND-open` is the live frontier

### The no-smuggling invariant

The following primitives are **not** imported in this pilot:
- genes, cells, fitness functions
- thermodynamic entropy as a primitive
- membrane biophysics
- Lipschitz geometry
- any biological vocabulary not derivable from role carriers and
  NFC source-descendant structure

All structure derives from: SCC role-carrier machinery (thm:SCC.MCS),
Book II capacity law (imported via thm:VII.6.4), and Book V
branch-legitimacy.

### The two-unit assembly

`thm:BIO.MULTI.twocell` declares the minimal two-unit assembly
`A₂ = {X₁, X₂}` as a coordination structure. This is the BIO analogue
of the caesium calibration nomination in SPEC: it specifies the
minimal coordination carrier rather than claiming full multicellular biology.

### The BND frontier

`ob:BIO.BND-open` is the principal structural frontier of the BIO branch.
Whether boundary self-organization extends from the nondegenerate regime
to the full replicator class is a genuine force question that may require
either a new ingredient or a Book VI Transfer Theorem. The pilot preserves
this frontier as active and open.

## Updated L2 pilot portfolio

| Branch | Posture | Frontier profile |
|--------|---------|-----------------|
| GR | domain-bounded-cert-close | ob:GR.global-subcriticality |
| YM | conditional-cert-close | ob:YM.B3.A2 |
| SPEC | cert-close | none |
| SCC | conditional-cert-close | none |
| CRYST | conditional-cert-close | ob:CRYST.phase-problem |
| LING | conditional-cert-close | ob:LING.REF-INVIS-RECOV |
| **BIO** | **conditional-cert-close** | **ob:BIO.BND-open** |

## Recommended next milestone

**v30 — SM Branch-Successor Pilot** (or v30 — L2 Pilot Portfolio Hardening)

SM is the next candidate in the intake queue. It stresses a different
part of the governance system: intrinsic-structural-close posture,
inherited YM/GR scope limitations, and the O-IDcont frontier.

Risk band: high. Recommend a brief hardening pass on the v29 BIO pilot
before SM migration, ensuring the no-smuggling and scoped-endpoint
machinery is fully trusted before the more inheritance-sensitive SM branch.
