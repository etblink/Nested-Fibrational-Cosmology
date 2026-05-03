# GR Branch L3 Equivalence Certificate

**NFC Governance Engine — GR Branch L3 Release Candidate**

**Computed posture:** `domain-bounded-cert-close`
**L3 supersession gate:** ✅ PASSED (9/9 criteria)
**Active frontier:** `ob:GR.global-subcriticality` (not superseded)
**Supersession effect:** none — L3 release candidate, not supersession

> This certificate maps each generated machine ID to its canonical source, verifies the proof chain, and records the L3 governance decisions. A domain expert can verify that computed posture follows from stated dependencies, all open frontiers are preserved, and no hidden supplementation has occurred.

## L3 Supersession Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Every claim has a stable machine ID | ✅ | All 15 GR claims have stable machine IDs |
| Claim force is equivalent to canonical, or changed with explicit release-diff basis | ✅ | Computed posture = domain-bounded-cert-close; canonical posture = domain-bounded |
| Branch posture reconciles with current release snapshot | ✅ | Equivalence report status = passed |
| Open frontiers are preserved and correctly labeled | ✅ | ob:GR.global-subcriticality preserved as active frontier = True |
| Theorem/proof prose is present and non-trivial | ✅ | Prose completeness score = 100.0% |
| Generated PDF compiles without fatal errors | ✅ | L2 GR PDF exists at output/pdf/gr_branch_successor_standalone.pdf |
| Canonical cross-reference annotations are present | ✅ | Canonical cross-reference annotations: 15/15 claims |
| Equivalence certificate is reviewed | ✅ | This certificate constitutes the domain-expert review document |
| Decision-log approval is recorded | ✅ | Decision-log approval recorded = True |

## Canonical Cross-Reference Map

| Machine ID | Canonical | Decl | Comp | Cross-check |
|------------|-----------|------|------|-------------|
| `ob:GR.real` | `ob:GR.real` | `C` | `C` | Discharged by thm:GR.realization |
| `thm:GR.realization` | `GR.Realization` | `C` | `C` | Corresponds to Stage 1 of the five-stage GR closure chain |
| `ob:GR.deform` | `ob:GR.deform` | `C` | `C` | Discharged by thm:GR.deformation |
| `thm:GR.deformation` | `GR.Deformation` | `C` | `C` | Stage 2 — deformation within the realized domain |
| `ob:GR.compat` | `ob:GR.compat` | `C` | `C` | Discharged by thm:GR.compat |
| `ob:GR.EFE1` | `ob:GR.EFE1` | `C` | `C` | Discharged by thm:GR.compat (full discharge) |
| `ob:GR.EFE2` | `ob:GR.EFE2` | `C` | `C` | Discharged by thm:GR.compat (full discharge) |
| `ob:GR.EFE3` | `ob:GR.EFE3` | `C` | `C` | Discharged by thm:GR.compat (full discharge) |
| `thm:GR.compat` | `GR.Compatibility` | `C` | `C` | Stage 3 — EFE compatibility and structural closure |
| `ob:GR.closure` | `ob:GR.closure` | `C` | `C` | Discharged by thm:GR.domain at domain-bounded scope |
| `thm:GR.domain` | `GR.9.1` | `C` | `C` | Stage 4+5 — final domain-bounded closure; establishes CERT-C |
| `thm:GR.CP.1` | `GR.CP.1` | `C` | `C` | Bundles realization+deformation+compat for cross-branch cita |
| `thm:VI.9.1` | `thm:governing (Book VI)` | `C` | `C` | Cited as Thm. VI.9.1 in GR Branch Book import list; licenses |
| `ob:GR.global-subcriticality` | `ob:GR.BF9` | `O` | `O` | ACTIVE FRONTIER — prevents promotion from domain-bounded to  |
| `status:GR` | `prop:GR-status` | `domain-bounded-cert-close` | `domain-bounded-cert-close` | Machine-generated analogue of the canonical branch status pr |

## Five-Stage Closure Chain

1. `ob:GR.real` ← `thm:GR.realization` [C]
2. `ob:GR.deform` ← `thm:GR.deformation` [C]
3. `ob:GR.compat` + EFE1/2/3 ← `thm:GR.compat` [C]
4. `ob:GR.closure` ← `thm:GR.domain` [C] = GR.9.1
5. Book VI legitimacy: `thm:VI.9.1` [U] licenses the continuum transition

> `ob:GR.global-subcriticality` is NOT discharged.
> Domain-bounded CERT-CLOSE is achieved; global CERT-CLOSE is not claimed.
