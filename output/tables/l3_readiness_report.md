# v33 L3 Readiness Report

Formal per-pilot L3 gate — checks whether each L2 pilot is ready for
promotion to L3 (branch successor release candidate) status.

| Branch | Level | L3 Ready | Hard failures | Soft failures |
|--------|-------|----------|---------------|---------------|
| GR | ✅ l3_ready | True | none | none |
| YM | ✅ l3_ready | True | none | none |
| NS | ✅ l3_ready | True | none | none |
| SM | ✅ l3_ready | True | none | none |
| RH | ✅ l3_ready | True | none | none |
| SPEC | ✅ l3_ready | True | none | none |
| SCC | ✅ l3_ready | True | none | none |
| BIO | ✅ l3_ready | True | none | none |
| LING | ✅ l3_ready | True | none | none |
| CRYST | ✅ l3_ready | True | none | none |

---

## GR

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/gr_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | domain-bounded-cert-close | domain-bounded-cert-close |
| `l3.frontiers_preserved` | ✅ | ['ob:GR.global-subcriticality'] | ['ob:GR.global-subcriticality'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | GR | GR in proof_trees.json |
| `l3.canonical_coverage` | ✅ | 100.0% | >= 90.0% |
| `l3.prose_score` | ✅ | 100.0% | >= 80.0% |
| `l3.scope_score` | ✅ | 100.0% | >= 80.0% |

## YM

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/ym_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | conditional-cert-close | conditional-cert-close |
| `l3.frontiers_preserved` | ✅ | ['ob:YM.B3.A2'] | ['ob:YM.B3.A2'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | YM | YM in proof_trees.json |
| `l3.canonical_coverage` | ✅ | 100.0% | >= 90.0% |
| `l3.prose_score` | ✅ | 100.0% | >= 80.0% |
| `l3.scope_score` | ✅ | 100.0% | >= 80.0% |

## NS

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/ns_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | domain-bounded-cert-close | domain-bounded-cert-close |
| `l3.frontiers_preserved` | ✅ | ['front:NS.main', 'ob:NS.bridge-stage2'] | ['front:NS.main'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | NS | NS in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 16 claims | > 0 |

## SM

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/sm_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | intrinsic-structural-close | intrinsic-structural-close |
| `l3.frontiers_preserved` | ✅ | ['ob:SM.O-IDcont'] | ['ob:SM.O-IDcont'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | SM | SM in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 14 claims | > 0 |

## RH

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/rh_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | cert-proj | cert-proj |
| `l3.frontiers_preserved` | ✅ | ['ob:RH.S1-ARC', 'thm:RH.S1.formal'] | ['ob:RH.S1-ARC'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | RH | RH in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 12 claims | > 0 |

## SPEC

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/spec_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | cert-close | cert-close |
| `l3.frontiers_preserved` | ✅ | [] | [] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | SPEC | SPEC in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 2 claims | > 0 |

## SCC

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/scc_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | conditional-cert-close | conditional-cert-close |
| `l3.frontiers_preserved` | ✅ | [] | [] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | SCC | SCC in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 7 claims | > 0 |

## BIO

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/bio_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | conditional-cert-close | conditional-cert-close |
| `l3.frontiers_preserved` | ✅ | ['ob:BIO.BND-open'] | ['ob:BIO.BND-open'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | BIO | BIO in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 16 claims | > 0 |

## LING

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/ling_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | conditional-cert-close | conditional-cert-close |
| `l3.frontiers_preserved` | ✅ | ['ob:LING.REF-INVIS-RECOV'] | ['ob:LING.REF-INVIS-RECOV'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | LING | LING in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 3 claims | > 0 |

## CRYST

**Level:** `l3_ready`  
**Description:** L3 ready — passes all L3 criteria, eligible for release candidate

| Check | Status | Observed | Expected |
|-------|--------|----------|----------|
| `l3.equivalence_passed` | ✅ | passed | passed |
| `l3.pdf_compiled` | ✅ | output/pdf/cryst_branch_successor_standalone.pdf | exists |
| `l3.posture_correct` | ✅ | conditional-cert-close | conditional-cert-close |
| `l3.frontiers_preserved` | ✅ | ['ob:CRYST.phase-problem'] | ['ob:CRYST.phase-problem'] |
| `l3.no_supersession` | ✅ | none; pilot shell only | none or none; pilot shell only |
| `l3.proof_tree_available` | ✅ _(warn)_ | CRYST | CRYST in proof_trees.json |
| `l3.claims_present` | ✅ _(warn)_ | 3 claims | > 0 |

