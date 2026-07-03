# Research Packet — RH-P0: Probe-Space Nontriviality and Separation Audit

> ## ⚠ GATE NOTICE (2026-07-03, second review): RH-K0 PRECEDES ANY P0 CANON MIGRATION
> A deeper defect sits one layer upstream: `prop:rh-kernel-positivity` and `def:rh-kernel`
> carry three independent problems (sign reversal in the displayed zero contribution;
> exact cancellation of functional-equation partners in the displayed sum; a
> difference-kernel vs. spectral-multiplier mismatch between `def:rh-kernel` and the
> quadratic form actually used). See **`RESEARCH_PACKET_RH_K0.md`**. P0's *research* items
> (P0-1…P0-4 analysis, the density candidate) may proceed, but **no P0 canon migration is
> authorized until K0 is resolved** — repairing the probe space against an ill-posed
> kernel criterion would build on sand. Both kernel claims are flagged `review_needed`.

**Class:** scaffold planning document; **not canon**. Nothing here alters any `\status` tag, label, or canon text. This packet is the mandated prerequisite to S1-ARC-0 (see the gate notice in `RESEARCH_PACKET_RH_S1.md`) and exists because the S1 packet's F4 falsification criterion fired against the canon's own probe-space definition. The canon repairs it motivates are `[D]`-level re-declarations plus one theorem repair, each individually migration-gated.

**Affected canon claims (flagged `review_needed` in metadata):** `def:scc-admissible-probes` (SCC Branch, SCC-M1–M4) and `thm:scc-rh-equivalence` `[C]`; `thm:rh-s1-conditional` and `ob:rh-s1-formal` carry inherited gate notes.

---

## 1. The scale-invariance collapse lemma (recorded; verified against canon text)

> **Lemma P0.1 (Probe-space triviality under SCC-M3 + SCC-M4).**
> Let f : ℝ₊ → ℂ satisfy SCC-M3 (f(qx) = f(x) for all q ∈ ℚ×) and SCC-M4 (f ∈ L²(ℝ₊, dx/x)). Then f = 0 almost everywhere; consequently the SCC-admissible probe space of `def:scc-admissible-probes` is {0}, and ψ ≡ 0 is its only Mellin transform.
>
> *Proof.* It suffices to use the single rational q = 2. Set g(t) := f(eᵗ). The substitution x = eᵗ gives ‖f‖²_{L²(dx/x)} = ∫_ℝ |g(t)|² dt, so g ∈ L²(ℝ). SCC-M3 at q = 2 gives f(2x) = f(x), i.e. g(t + log 2) = g(t) for a.e. t: g is (log 2)-periodic. For a periodic g, ∫_ℝ |g|² dt equals the sum over infinitely many periods of the constant period-integral ∫₀^{log 2} |g|² dt; finiteness forces that period-integral to be 0, hence g = 0 a.e., hence f = 0 a.e. ∎

**Immediate consequences (as the review states):** W_RH = {0}; Q[0] = 0 holds vacuously; every truncation W_RH^sf(N) inheriting SCC-M3/M4 is likewise trivial; positivity on this class cannot imply RH. The canon's own Gaussian-exclusion remark in `thm:scc-rh-equivalence` was a visible symptom: the definition excludes not just Gaussians but everything nonzero.

## 2. The separation gap in `thm:scc-rh-equivalence` (recorded)

Independently of Lemma P0.1, the theorem's proof establishes only:
RH ⟹ K positive-definite ⟹ Q[ψ] ≥ 0 for every SCC-admissible ψ.
The converse — that positivity **on the subclass** implies positive-definiteness of K, hence RH — requires the subclass to *detect every negative direction* of the quadratic form. Restriction of a universal quantifier does not preserve an equivalence; the missing ingredient is a **separation (or density) theorem**: if K is not positive-definite, some admissible ψ witnesses Q[ψ] < 0. No such theorem exists in the canon. Until it does, the honest reading of the equivalence is one-directional at the declared scope.

## 3. Program items (the mandate, in order)

**P0-1. Record the collapse lemma.** Done above (§1). Canonical destination when authorized: a `[U]` lemma adjacent to the re-declared probe definition, serving as the permanent record of *why* the definition was repaired (Phase-3 Rule 4: the failed intake is preserved and explained, not erased).

**P0-2. Repair SCC-M3: family-level covariance instead of pointwise invariance.** Proposed re-declaration: replace "f(qx) = f(x) for all q ∈ ℚ×" with a **quotient-visible action on the family**: with (U_q f)(x) := f(qx), require
> **SCC-M3′:** U_q W ⊆ W for every q ∈ ℚ₊ (the probe *family* is stable under the arithmetic scaling action),
so no individual member is required to be a fixed point. This preserves the original intent (ℚ×-quotient descent = the arithmetic scaling structure is visible to the family) while removing the fixed-point requirement that caused the collapse. Note U_q is the multiplicative translation on L²(dx/x); each U_q is exactly an isometry of L²(dx/x) (Haar invariance), so SCC-M3′ is compatible with SCC-M4 by construction.

**P0-3. Nontriviality of the repaired family (proposed lemma, with witness).**
> **Proposed Lemma P0.3 (target `[C]` pending audit of the aggregation rule).** The smallest family W containing f₀(x) := x^{1/2} e^{−x} and closed under {U_q : q ∈ ℚ₊}, Mellin weighting, and the licensed finite aggregation rule consists of L²(ℝ₊, dx/x) functions and is nontrivial.
> *Sketch:* ‖f₀‖²_{L²(dx/x)} = ∫₀^∞ |x^{1/2}e^{−x}|² dx/x = ∫₀^∞ e^{−2x} dx = **1/2** < ∞ (corrected per review — an earlier draft misstated 1/4, which would correspond to f₀(x)=xe^{−x}) and f₀ ≢ 0; each U_q is **exactly** an isometry of L²(dx/x): ‖U_q f‖² = ∫|f(qx)|² dx/x = ∫|f(y)|² dy/y by y = qx and Haar invariance; finite aggregation preserves membership. (The Mellin transform of f₀ is Γ(1/2 + iτ)-type — nonvanishing, giving a nonzero ψ.)
This discharges the reviewer's item 3 at proposal level; the canonical proof must additionally verify the branch-visibility/no-smuggling conditions of the RH descent discipline.

**P0-4. The exact separation condition (to be stated and proved before any converse is claimed).**
> **Required theorem shape (SEP):** Let W satisfy SCC-M1, M2, M3′, M4. Call W *separating for K* if: whenever K is not positive-definite on the full declared test class, there exists ψ ∈ W (equivalently, in the closed span of W under the licensed aggregation) with Q[ψ] < 0.
> Sufficient route to prove SEP: show the Mellin images of W are **dense** in the relevant weighted L² space on the critical line (density ⟹ any negative direction of the form is approximable ⟹ some member goes negative). The Γ-type images of the U_q-orbit of f₀ under Mellin weighting are a natural candidate total set; density must be proved, not assumed.
Only after SEP is proved may `thm:scc-rh-equivalence` be repaired to a genuine equivalence (a theorem-statement change: `[C]`, migration-gated, with the old statement preserved as superseded intake per Phase-3 Rule 5).

**P0-5. Only then: re-found the truncations.** Define W_RH^sf(N) over the repaired family: generator set = {U_q f₀ : q = a/b, a,b ≤ N} together with the declared Mellin weightings; admissible aggregation = the licensed finite rule; and the **finite quadratic-form matrix** Q_N := (Q[ψ_i, ψ_j])_{i,j} (the polarized form on the generator list). All of `def:rh-sf-probe-subfamily`'s closure clauses re-anchor to SCC-M3′.

**P0-6. Re-formulate S1-ARC-0.** New target (replacing the paused version): **positivity of the finite matrix Q_N ⪰ 0**, with the induction step N → N′ expressed as a **Gram-matrix extension / Schur-complement condition**: writing Q_{N′} = [[Q_N, B],[B*, D]], the step is D − B* Q_N⁺ B ⪰ 0 on the new generators. This makes the inductive program a sequence of concrete finite checks whose limit statement, *combined with SEP*, is exactly S1-ARC on the repaired space.

## 4. Prohibited paths (inherited + new)

All six prohibitions of the S1 packet remain. Additionally: **(7)** no repair of `def:scc-admissible-probes` may be applied to canon before P0-3 (nontriviality) is proved for the repaired form — replacing a trivial space with an unverified one repeats the failure; **(8)** no converse use of `thm:scc-rh-equivalence` in any argument until SEP (P0-4) is a proved theorem; **(9)** the collapse lemma may not be "resolved" by weakening SCC-M4 (dropping square-integrability would destroy the Hilbert-space frame the kernel positivity analysis needs) — the repair locus is M3, per the review.

## 5. Falsification criteria for P0 itself

- **P0-F1:** a proof that *every* ℚ₊-covariant family satisfying M1/M2/M4 fails density (SEP unprovable in principle) would falsify the P0 repair route and force a deeper re-design of the probe frame.
- **P0-F2:** failure of the licensed aggregation rule to preserve L²(dx/x) on the U_q-orbit of any admissible generator would falsify P0-3 as stated.
- **P0-F3:** a demonstration that the repaired W is separating but Q_N ⊁ 0 already at small N would be an F1-class event for the whole RH route (a certified negative direction).

## 6. Exit criteria (what re-opens S1-ARC-0)

S1-ARC-0 resumes when, and only when: P0-3 is proved (nontrivial repaired family), SEP is proved (P0-4), the re-declaration of `def:scc-admissible-probes` and the repaired `thm:scc-rh-equivalence` have entered canon through individually-reviewed migrations with the superseded texts preserved as intake, and `make check` passes with the two `review_needed` flags cleared by the reviewer.
