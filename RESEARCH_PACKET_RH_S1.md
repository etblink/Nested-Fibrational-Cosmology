# Research Packet — RH Witness Assembly S1 (S1-ARC residual)

> ## ⚠ GATE NOTICE (2026-07-03): S1-ARC-0 IS PAUSED — F4 HAS FIRED
> This packet's own falsification criterion **F4 (probe-space degeneracy)** was triggered by
> independent review and verified against the canon text: `def:scc-admissible-probes`
> (SCC Branch) makes the admissible probe space **trivial** — SCC-M3's pointwise
> ℚ×-invariance plus SCC-M4's L²(dx/x) membership force f = 0 a.e. Additionally,
> the converse direction of `thm:scc-rh-equivalence` rests on an unproved separation
> assumption. **Do not attempt S1-ARC-0 (§6) under the current definitions**: every
> truncation W_RH^sf(N) inheriting SCC-M3/M4 is trivial, and positivity on it is vacuous.
> The prerequisite program is **`RESEARCH_PACKET_RH_P0.md`** (probe-space nontriviality
> and separation audit). Both affected canon claims are flagged `review_needed` in the
> metadata/dashboard. This is a pre-existing canon issue reached *through* this packet's
> discipline — the falsification machinery worked as designed. No canon edit has been
> made; re-declaration of the probe space is a [D]-level, migration-gated change pending
> the P0 results.

**Class:** scaffold planning document. **This packet is not canon and asserts no new mathematics.** It assembles the canon's own authoritative statements about the S1 frontier so that research can begin without contaminating any branch status. Every promotion out of this packet must pass the standing edit gate (`make check`) and the governance rules quoted in §5.

**Why this frontier first (selection rationale):** S1 is already isolated by the canon itself as a sharply named arithmetic residual — `rem:rh-s1-reduction` compresses the four-predicate Witness Assembly bundle to a single predicate, S1-ARC — and it sits in exactly one branch (RH), one syntactic `[O]` (`ob:rh-s1-formal`), and one reduced-frontier item, so work here cannot silently alter YM/GR/SM/NS/SCC postures.

---

## 1. Authoritative current proposition

The governing texts, in authority order (Canon Authority Model tiers):

- **A1 —** `prop:RH-status` (branch posture: **CERT-PROJ**; S1 arithmetic + RH4–6 frontier).
- **A2/A3 —** `ob:rh-s1-formal` `[O]` (the live obligation, quoted verbatim below) and `rem:rh-s1-reduction` `[R]` (the reduction).
- **Conditional target theorem —** `thm:rh-s1-conditional` `[C]`: *if* the S1 predicate (`def:rh-s1-predicate`) holds for a declared arithmetic witness package, and given the SCC–RH equivalence (`thm:scc-rh-equivalence`), then Q[ψ] ≥ 0 for all admissible ψ, "and therefore the Riemann Hypothesis holds conditionally on the declared SCC-admissible scope."

**The obligation, verbatim reduction (from `ob:rh-s1-formal`):** the four S1 sub-predicates are S1-ARC, S1-TRACE, S1-DESCENT, S1-COMP; S1-TRACE is conditionally realized via the scaling-flow candidate (`ob:rh-sf-trace-pairing-law` `[C]`), S1-DESCENT via the transport-localization chain L1–L7 (conditional), S1-COMP via SCC-MCS (conditionally discharged, `thm:scc-mcs`). **"Therefore the irreducible arithmetic content reduces to S1-ARC alone: proving Q[ψ] ≥ 0 from the arithmetic structure of Ξ."** This is the canon's sharpest statement of the residual, and it is deliberately outside the NFC collar-algebra toolkit ("pure arithmetic").

## 2. Exact remaining hypotheses

**The single open predicate:**
> **S1-ARC.** Q[ψ] ≥ 0 for all ψ ∈ W_RH (the declared SCC-admissible probe space), proved **from the arithmetic structure of Ξ**, without assuming RH.

**Inherited conditional hypotheses that any *unconditional* S1 discharge must eventually clear** (these do not block S1-ARC work but bound what any result may claim):
1. The scaling-flow trace pairing conditions of `ob:rh-sf-trace-pairing-law` `[C]` (S1-TRACE's discharge basis).
2. The log-derivative legality + D2 audit conditions of `ob:rh-sf-logderiv-legality` and `ob:rh-sf-d2-audit` `[C]` — per `rem:rh-sf-remaining-burden`, exactly the two-item burden left on the orbit-grammar side (branch-visible/no-smuggling manipulations; correct prime-power pairing).
3. The transport-localization chain conditions L3–L7 (`ob:rh-tloc-L3` … `ob:rh-tloc-L7`, all `[C]`) underlying S1-DESCENT.
4. The SCC-MCS conditional scope (UCTI / depth-sum / threshold-stability, SCC branch) underlying S1-COMP.

## 3. Dependency subgraph

Machine-extracted from `metadata/edges.json`. **Selection rule:** all distinct directed proof-citation edges with at least one endpoint whose label contains `rh-s1`, `rh-sf`, `rh-tloc`, or `rh-L3` (the L3-observable family is part of the S1-DESCENT neighborhood). Under this rule there are **87 distinct edges** (81 without the `rh-L3` family); the full list is reproduced in Appendix A (also queryable live in the dashboard's dependency panel). Structure at a glance: the two "hard-block-cleared" corollaries sit at the top (`cor:rh-sf-first-hard-block-cleared` over the orbit-grammar package; `cor:rh-second-hard-block-cleared` over the L1–L7 chain); the sf-lemma layer (`lem:rh-sf-*`) feeds the pairing/determinant propositions (`prop:rh-sf-*`); `thm:rh-s1-conditional` consumes the whole assembly via `def:rh-s1-predicate` and `thm:scc-rh-equivalence`. **S1-ARC has no incoming discharge edge — that absence is the frontier.**

## 4. Prohibited promotion paths (binding, from Book VII governance + rewrite policy)

1. **No `[C]`→`[U]` without a Transfer Theorem.** In particular `thm:rh-s1-conditional` cannot be promoted by restatement, and no result conditional on the sf/tloc stacks may shed those conditions by citation alone.
2. **No frontier dissolution by rephrasing.** `ob:rh-s1-formal` stays `[O]` until a theorem or certified bridge discharges S1-ARC itself; reformulating Q, W_RH, or the predicate does not count.
3. **No circular route through RH.** Any argument assuming RH (or zero-location data equivalent to it) to establish Q[ψ] ≥ 0 is inadmissible — S1-ARC's statement explicitly excludes it.
4. **No scope inflation from SCC.** S1-COMP inherits SCC-MCS *at its conditional scope only*; no S1 result may claim more SCC force than `thm:scc-mcs-full`'s stated conditions permit (bridge-stack limit).
5. **No hidden arithmetic import.** Any new probe construction must pass the S1-DESCENT no-hidden-import discipline and, if it touches the log-derivative route, the `ob:rh-sf-d2-audit` conditions.
6. **No status change outside a migration entry.** Any tag or ledger consequence of new work enters canon only through the standing gate (`make check` + migration log), per the release-frozen rewrite policy.

## 5. Falsification criteria (what would refute the packet's premises)

- **F1 (direct).** A certified ψ ∈ W_RH with Q[ψ] < 0, constructed under the declared admissibility rules, falsifies S1-ARC as stated — and, via `thm:scc-rh-equivalence`, would contradict RH at the declared scope; such a finding would trigger an immediate corpus-level review of the equivalence's hypotheses before any status action.
- **F2 (trace layer).** An h ∈ W_RH for which the certified pairing Tr_{G_sf}(h) = Σ_{p,m} (log p) p^{−m/2} h(m log p) fails would void the conditional discharge of S1-TRACE (`ob:rh-sf-trace-pairing-law` reverts toward `[O]` by migration).
- **F3 (descent layer).** A demonstrated hidden arithmetic import in the Mellin/Dirichlet descent (an L1–L7 audit failure) voids S1-DESCENT's conditional discharge.
- **F4 (probe-space degeneracy).** A proof that W_RH^sf (the scaling-flow probe subfamily, `def:rh-sf-probe-subfamily`) fails to be separating for the positivity question would show the declared probe space is too small to carry S1-ARC, forcing a re-declaration (a `[D]`-level change, migration-gated).

## 6. Smallest admissible next theorem (proposed, non-canonical until proved and gated)

> **Proposed Lemma (target tag `[C]`; working name S1-ARC-0).**
> *Restricted positivity on the scaling-flow probe subfamily at finite truncation.* For every ψ in the finitely-generated truncation W_RH^sf(N) of the scaling-flow probe subfamily (`def:rh-sf-probe-subfamily`, generators up to admissible scaling index N), Q[ψ] ≥ 0, proved from the certified prime-power pairing (`prop:rh-sf-primepower-pairing`) and the half-density damping law (`lem:rh-sf-half-density-weight`), **conditional on** the sf-stack conditions of §2.1–2.2 and **without assuming RH**.

Why this is the smallest admissible step: it quantifies over a finite, canon-declared subfamily rather than all of W_RH; it consumes only already-certified `[C]` machinery; it is falsifiable in the strongest sense (a single truncated counterexample kills it — and would already be an F1-class event); and it **cannot** discharge or weaken `ob:rh-s1-formal` (path 2 of §4 applies — the packet states this explicitly so no future reader mistakes S1-ARC-0 for S1-ARC). Its role is to convert the frontier from "prove positivity everywhere" into an inductive program over the scaling index with a certified base, which is the canon's own compression direction per `rem:rh-sf-remaining-burden`.

**Admission path:** prove S1-ARC-0 → add as `[C]` lemma in the RH branch sf-section with explicit condition list → `make check` → migration entry → regenerate. No other file, status, or accounting changes.

---

## Appendix A — Family dependency edges (machine-extracted)

| From | | To |
|---|---|---|
| `cor:rh-second-hard-block-cleared` | → | `def:rh-tloc-template` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L1` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L2` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L4-structural` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L4-uniform` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L5-structural` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L5-uniform` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L6-structural` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L6-uniform` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L7-structural` |
| `cor:rh-second-hard-block-cleared` | → | `prop:rh-tloc-L7-uniform` |
| `cor:rh-sf-first-hard-block-cleared` | → | `thm:rh-og-5` |
| `cor:rh-sf-first-hard-block-cleared` | → | `thm:rh-sf-local-d2-checks` |
| `cor:rh-sf-logroute-ready` | → | `lem:rh-d2-reduction` |
| `cor:rh-sf-logroute-ready` | → | `prop:rh-sf-logderiv-d2-ready` |
| `cor:rh-sf-logroute-ready` | → | `thm:rh-sf-local-d2-checks` |
| `lem:rh-sf-half-density-weight` | → | `prop:rh-sf-period-law` |
| `lem:rh-sf-logdiff-amplitude` | → | `def:rh-logdiff-channel` |
| `lem:rh-sf-logdiff-amplitude` | → | `prop:rh-sf-determinant-origin` |
| `lem:rh-sf-primepower-logderiv` | → | `prop:rh-sf-det-euler` |
| `lem:rh-sf-trace-uniformity` | → | `def:rh-logderiv-trace-pairing` |
| `lem:rh-sf-trace-uniformity` | → | `def:rh-trace-test-subfamily` |
| `prop:rh-L3-observable-existence` | → | `prop:rh-tloc-L1` |
| `prop:rh-L3-observable-existence` | → | `prop:rh-tloc-L2` |
| `prop:rh-L3-observable-existence` | → | `prop:rh-wc1am` |
| `prop:rh-L3-template-clean` | → | `def:rh-tloc-template` |
| `prop:rh-L3-template-clean` | → | `prop:rh-L3-observable-existence` |
| `prop:rh-L3-template-clean` | → | `prop:rh-L3-threshold` |
| `prop:rh-L3-template-clean` | → | `prop:rh-L3-uniformity` |
| `prop:rh-L3-threshold` | → | `prop:rh-tloc-L2` |
| `prop:rh-L3-uniformity` | → | `prop:rh-L3-observable-existence` |
| `prop:rh-L3-uniformity` | → | `prop:rh-tloc-L1` |
| `prop:rh-L3-uniformity` | → | `prop:rh-tloc-L2` |
| `prop:rh-L3-uniformity` | → | `thm:rh-d1-8` |
| `prop:rh-sf-determinant-origin` | → | `def:rh-det-channel-local` |
| `prop:rh-sf-determinant-origin` | → | `prop:rh-sf-operator-origin` |
| `prop:rh-sf-logderiv-d2-ready` | → | `lem:rh-d2-reduction` |
| `prop:rh-sf-operator-origin` | → | `def:rh-sf-aggregation-channel` |
| `prop:rh-sf-operator-origin` | → | `def:rh-sf-probe-subfamily` |
| `prop:rh-sf-package-landing` | → | `def:rh-primepower-package` |
| `prop:rh-sf-package-landing` | → | `prop:rh-sf-primepower-pairing` |
| `prop:rh-sf-period-law` | → | `def:rh-og-scaling-candidate` |
| `prop:rh-sf-primepower-pairing` | → | `def:rh-logderiv-trace-pairing` |
| `prop:rh-sf-primepower-pairing` | → | `lem:rh-sf-half-density-weight` |
| `prop:rh-sf-primepower-pairing` | → | `lem:rh-sf-logdiff-amplitude` |
| `prop:rh-sf-primepower-pairing` | → | `lem:rh-sf-trace-uniformity` |
| `prop:rh-sf-primepower-pairing` | → | `prop:rh-sf-period-law` |
| `prop:rh-sf-trace-test-origin` | → | `def:rh-trace-test-subfamily` |
| `prop:rh-sf-trace-test-origin` | → | `lem:rh-sf-logdiff-amplitude` |
| `prop:rh-sf-trace-test-origin` | → | `prop:rh-sf-determinant-origin` |
| `prop:rh-sf-trace-test-origin` | → | `prop:rh-sf-operator-origin` |
| `prop:rh-tloc-L1` | → | `def:rh-tloc-template` |
| `prop:rh-tloc-L1` | → | `lem:rh-wc1al` |
| `prop:rh-tloc-L1` | → | `thm:rh-d1-8` |
| `prop:rh-tloc-L2` | → | `prop:rh-tloc-L1` |
| `prop:rh-tloc-L2` | → | `prop:rh-wc1am` |
| `prop:rh-tloc-L4-structural` | → | `lem:rh-wc1al` |
| `prop:rh-tloc-L4-structural` | → | `prop:rh-wc1am` |
| `prop:rh-tloc-L4-uniform` | → | `prop:rh-tloc-L1` |
| `prop:rh-tloc-L4-uniform` | → | `prop:rh-tloc-L2` |
| `prop:rh-tloc-L4-uniform` | → | `prop:rh-tloc-L4-structural` |
| `prop:rh-tloc-L5-structural` | → | `prop:rh-wc1ba` |
| `prop:rh-tloc-L5-uniform` | → | `def:rh-gram-matrix` |
| `prop:rh-tloc-L5-uniform` | → | `prop:rh-tloc-L4-uniform` |
| `prop:rh-tloc-L5-uniform` | → | `thm:rh-d1-8` |
| `prop:rh-tloc-L6-structural` | → | `prop:rh-tloc-L5-structural` |
| `prop:rh-tloc-L6-uniform` | → | `prop:rh-tloc-L5-uniform` |
| `prop:rh-tloc-L7-structural` | → | `prop:rh-tloc-L6-structural` |
| `prop:rh-tloc-L7-uniform` | → | `def:rh-phase-threshold` |
| `prop:rh-tloc-L7-uniform` | → | `prop:rh-L3-threshold` |
| `prop:rh-tloc-L7-uniform` | → | `prop:rh-L3-uniformity` |
| `prop:rh-tloc-L7-uniform` | → | `prop:rh-tloc-L2` |
| `prop:rh-wc1bb-L12-partial` | → | `def:rh-tloc-template` |
| `prop:rh-wc1bb-L12-partial` | → | `prop:rh-tloc-L1` |
| `prop:rh-wc1bb-L12-partial` | → | `prop:rh-tloc-L2` |
| `thm:rh-og-5` | → | `lem:rh-sf-half-density-weight` |
| `thm:rh-og-5` | → | `prop:rh-sf-det-euler` |
| `thm:rh-og-5` | → | `prop:rh-sf-period-law` |
| `thm:rh-s1-conditional` | → | `thm:scc-rh-equivalence` |
| `thm:rh-sf-local-d2-checks` | → | `lem:rh-d2-reduction` |
| `thm:rh-sf-local-d2-checks` | → | `lem:rh-sf-trace-uniformity` |
| `thm:rh-sf-local-d2-checks` | → | `prop:rh-sf-determinant-origin` |
| `thm:rh-sf-local-d2-checks` | → | `prop:rh-sf-operator-origin` |
| `thm:rh-sf-local-d2-checks` | → | `prop:rh-sf-package-landing` |
| `thm:rh-sf-local-d2-checks` | → | `prop:rh-sf-trace-test-origin` |
| `thm:rh-sf-local-d2-checks` | → | `rem:rh-logdiff-attribution-discipline` |
| `thm:rh-sf-local-d2-checks` | → | `rem:rh-logdiff-interface-lawfulness` |

