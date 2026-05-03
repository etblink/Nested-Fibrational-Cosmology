# v33 — L3 Hardening

## Summary

v33 is the first L3 hardening release, closing the L2 pilot portfolio and
adding the governance machinery that makes outputs *auditable* rather than
just present. No new claim records. Schema: 0.33.0.

## What changed

### New governance engines

**`build/proof_tree.py` — Proof Tree Engine**

Generates structured dependency chains from posture to leaf claims for all
10 branches. Output: `output/reports/proof_trees.json` and
`output/tables/proof_trees.md`. Each branch gets a recursive tree showing:
- Posture and narrative
- Basis claims with status badges (🟢/🟡/🔴/✅/🔵)
- Dependency chains to depth 4
- Discharge edges with typed modes
- Scope annotations
- Active frontier highlighting

This is the primary L3 deliverable: a domain expert can now read the proof
tree for GR or YM and verify that the inferred posture follows from the
stated dependencies, without having to trace the graph manually.

**`build/canonical_coverage.py` — Canonical Coverage Manifests**

For GR and YM, cross-references generated machine IDs against canonical
theorem lists derived from reading the branch books. Produces:
- Coverage percentage (canonical IDs found in generated set)
- Prose stub score (non-trivial body content)
- Scope completeness score (required scope fields populated)
- Discharge completeness score (all discharge edges typed)
- Missing/extra claim identification

**`build/l3_readiness.py` — L3 Readiness Checker**

Formal per-pilot L3 gate. A branch is L3-ready when:
1. Equivalence report passed
2. PDF compiled
3. Posture correct
4. Frontiers preserved
5. No supersession claimed
6. Proof trees available
7. (GR/YM) Canonical coverage ≥ 90%

## Build result

| Metric | Value |
|--------|-------|
| Schema | 0.33.0 |
| Claims | 112 (unchanged) |
| Errors | 0 |
| Warnings | 3 (unchanged intentional set) |
| Quality gate | **passed** |
| Regression | **passed** |
| Proof trees | 10 branches traced |
| GR canonical coverage | **100%** |
| YM canonical coverage | **100%** |

## L3 readiness results

All 10 branches pass the L3 gate:

| Branch | Posture | L3 status | Coverage |
|--------|---------|-----------|---------|
| GR | domain-bounded-cert-close | ✅ L3-ready | 100% / prose 93% |
| YM | conditional-cert-close | ✅ L3-ready | 100% / prose 100% |
| NS | domain-bounded-cert-close | ✅ L3-ready | — |
| SM | intrinsic-structural-close | ✅ L3-ready | — |
| RH | cert-proj | ✅ L3-ready | — |
| SPEC | cert-close | ✅ L3-ready | — |
| SCC | conditional-cert-close | ✅ L3-ready | — |
| BIO | conditional-cert-close | ✅ L3-ready | — |
| LING | conditional-cert-close | ✅ L3-ready | — |
| CRYST | conditional-cert-close | ✅ L3-ready | — |

## GR proof tree (excerpt)

```
status:GR = domain-bounded-cert-close
narrative: GR closure chain reaches the declared domain endpoint;
           global curvature-subcriticality remains the only surviving frontier.

Active frontiers:
  🔴 ob:GR.global-subcriticality — Global Curvature-Subcriticality Frontier

Proof tree (basis items → dependencies):
  - ✅ thm:GR.domain [C] domain-bounded-cert-close
    ↳ Domain-Bounded Gravity Closure Theorem
    📐 regime=declared-GR-target, cert=domain-bounded, ceiling=C
    ⚡ discharges ob:GR.closure via full discharge ✓
    - 🟡 thm:GR.compat [C] conditional
      - 🟡 thm:GR.deformation [C]
        - 🟡 thm:GR.realization [C] (leaf)
  - 🔴 ob:GR.global-subcriticality [O] open
    ↳ Global Curvature-Subcriticality / BF-9 Extension Frontier
    (leaf — no dependencies)
```

## YM proof tree (excerpt)

```
status:YM = conditional-cert-close
narrative: YM bridge stack establishes conditional closure at MSC-normalized
           scope; B3-A2 is the surviving residual obligation.

Active frontiers:
  🔴 ob:YM.B3.A2 — Simple A2 Gap Restriction

Proof tree (basis items → dependencies):
  - 🟡 thm:YM.7 [C] conditional — Endpoint Mass-Gap and OS/Wightman Closure
    📐 regime=ym-msc-normalized, cert=branch-wide, ceiling=C
    - 🟡 thm:YM.ID [C] → thm:YM.RIG [C] → thm:YM.ENC [C] → ...
  - 🟡 thm:YM.B1.bridge [C] — YM B1 Post-Program Bridge
  - 🟡 thm:YM.B2.bridge [C] — YM B2 Post-Program Bridge  
  - 🟡 thm:YM.B3.bridge [C] — YM B3 Post-Program Bridge
  - 🔴 ob:YM.B3.A2 [O] — ACTIVE FRONTIER
```

## RH proof tree (excerpt)

```
status:RH = cert-proj
narrative: Architecture constituted through RH1-RH3; S1-TRACE/DESCENT/COMP
           conditionally discharged; S1-ARC is the irreducible arithmetic frontier.

Active frontiers:
  🔴 ob:RH.S1-ARC — IRREDUCIBLE: Q[psi]>=0 from arithmetic structure of Xi

Proof tree:
  - 🟡 thm:RH.3 [C] — Admissible Probe Space
  - 🔴 ob:RH.S1-ARC [O] — S1-ARC IRREDUCIBLE FRONTIER (leaf)
    THIS PILOT DOES NOT PROVE THE RIEMANN HYPOTHESIS
```

## Recommended next milestone

**v34 — L3 GR Branch Successor Release Candidate**

GR has achieved 100% canonical coverage, 93% prose score, and passes all L3
criteria. The next step is to produce a formal GR L3 release candidate:

1. Enrich the GR proof stubs to reach 100% prose completeness
2. Add canonical cross-reference annotations linking machine IDs to
   numbered theorems in the canonical GR Branch Book
3. Produce an equivalence certificate that a GR domain expert could review
4. Generate a decision-log entry for the L3 supersession approval
5. Compile the v34 GR L3 release candidate PDF

YM would be the v35 L3 release candidate, following the same process.
