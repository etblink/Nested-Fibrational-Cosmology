# Research Packet — RH-K0: Kernel-Criterion Audit

**Class:** scaffold planning document; **not canon**. This gate sits **upstream of RH-P0**: the probe-space repair (P0) presupposes a well-posed kernel positivity criterion, and the second review has shown — verified line-by-line against the canon text — that the criterion as written is ill-posed in three independent ways. No P0 canon migration may be authorized until K0 resolves. The failure order discovered by the falsification machinery is: S1 packet → F4 fired (probe space trivial) → P0 opened → K0 defect found one layer upstream (kernel criterion ill-posed). Each layer was exposed *before* any theorem was attempted against it.

**Affected canon claims (all flagged in metadata):** `def:rh-kernel` and `prop:rh-kernel-positivity` (SCC Branch — newly `review_needed`); `thm:scc-rh-equivalence` (note strengthened: inherits all three defects in addition to F4); `thm:rh-s1-conditional`, `ob:rh-s1-formal` (inherited notes; gate order K0 → P0 → S1-ARC-0).

---

## 1. The three verified defects (recorded against the exact canon text)

**D1 — Sign reversal.** `def:rh-kernel` displays
F(τ) ~ −Re(ζ′/ζ(½+iτ)) = **−**Σ_ρ Re[(½−σ_ρ) / ((½−σ_ρ)² + (τ−γ_ρ)²)].
For σ > ½ the inner numerator (½−σ) is negative, so with the leading minus the displayed contribution to F near τ = γ is **positive**. The proof of `prop:rh-kernel-positivity` asserts the opposite ("numerator is negative, contributing a negative bump to F") — it analyzes the summand and forgets the definition's leading sign.

**D2 — Functional-equation cancellation.** If ρ = σ+iγ is a nontrivial zero, so is 1−σ+iγ. Their displayed terms share the denominator ((½−σ)² = (σ−½)², same γ) and carry opposite numerators (½−σ) and (σ−½): they **cancel exactly**. The displayed real-part sum is therefore structurally blind to off-critical pairs — equivalently, Re(ξ′/ξ) vanishes on the critical line away from zeros **by the functional equation alone, irrespective of RH**. The criterion, as displayed, cannot distinguish RH from its negation.

**D3 — Kernel/multiplier mismatch.** `def:rh-kernel` declares the **difference kernel** K(t,u) = F(t−u), whose quadratic form is Q_K[φ] = ∬F(t−u)φ(t)φ̄(u) dt du = (1/2π)∫F̂(ξ)|φ̂(ξ)|² dξ — positivity governed by **F̂ ≥ 0** (Bochner), not by pointwise signs of F. The canon's `thm:scc-rh-equivalence` instead uses ∫F(τ)|ψ(τ)|² dτ — the form of a **spectral multiplier with symbol F**, whose positivity is governed by **F ≥ 0 pointwise**. These are different criteria for different objects; no Fourier-domain identification is supplied. And even under the difference-kernel reading, a local negative bump in F would not by itself disprove positive-definiteness (cos t is positive-definite and takes negative values), so the proof's central inference fails under either reading.

**D4 — Mellin–Plancherel domain error (added MIG-022).** The proof of `thm:scc-rh-equivalence` asserts that ψ_γ(τ) = e^{−(τ−γ)²} "is not a Mellin transform of any f ∈ L²(ℝ₊, dx/x)" and therefore fails SCC-M4. **False.** With t = log x the canon's Mellin convention becomes ordinary Fourier transformation of g(t) = f(eᵗ); Plancherel then makes 𝓜 a unitary between L²(dx/x) and L²(dτ), so **every** L² probe is a Mellin transform of an L²(dx/x) function. Explicitly, f_γ(x) = (1/(2√π)) x^{−iγ} exp(−(log x)²/4) has 𝓜f_γ(τ) = e^{−(τ−γ)²} exactly, with ‖f_γ‖²_{L²(dx/x)} = √2/(4√π) < ∞ (both verified symbolically). Gaussians satisfy SCC-M4 and fail only SCC-M3 as written; SCC-M2 is undecidable until "stable under x ↦ x/n" is formalized. The theorem's claimed exclusion of standard localized probes rests on a domain confusion, and `rem:scc-rh-governance` — which repeats both the exclusion and "the equivalence is genuine" — is flagged `review_needed` (the fifth queue item).

**Consequence.** `prop:rh-kernel-positivity`'s claimed equivalence "K positive-definite ⟺ RH" is unestablished as written, and everything downstream that consumes it (`thm:scc-rh-equivalence`, `thm:rh-s1-conditional`, the S1 route) inherits the gap. The `[C]` tags remain formally intact as conditional statements; their **usable force** is what is gated.

## 2. The audit mandate (the six determinations)

**K0-1. Object type.** Determine whether F is intended as (a) a difference kernel on ℝ² (positivity = Bochner: F̂ ≥ 0), (b) a spectral multiplier (positivity = F ≥ 0 pointwise), or (c) a distribution/measure requiring pairing against a declared test class. The two displays in canon currently commit to (a) in the definition and (b) in use; K0 must pick one and re-derive the other or discard it.

**K0-2. Exact regularized definition.** The canon's "~" in F ~ −Re(ζ′/ζ) is undefined. K0 must supply the precise regularization — and should work with the **completed ξ** rather than ζ, since the completed ξ admits a genus-one Hadamard product whose logarithmic derivative takes the form ξ′/ξ(s) = B + Σ_ρ [1/(s−ρ) + 1/ρ] (or an equivalent symmetrically-ordered/regularized zero sum — the bare sum Σ 1/(s−ρ) is not absolutely convergent and needs exactly the prescription K0-2 demands), which removes the Γ-factor and pole bookkeeping that ζ′/ζ drags in. The explicit-formula route (Weil) enters here: the zero side must be paired with the prime side under a declared test class, not truncated to a bare real-part sum.

**K0-3. Correct quadratic form and form domain.** State Q with its Hilbert-space domain and prove it is densely defined and continuous or closed there. Without a declared domain, "positive-definite" is not a proposition.

**K0-4. Functional-equation symmetry.** Decide how the ρ ↔ 1−ρ̄ pairing is handled. The necessary condition: the repaired criterion must remain **sensitive after functional-equation pairing** — demonstrably responsive to |σ−½| > 0 with a rigorous global sign or positivity mechanism (which is exactly what the first-order real-part sum lacks, by D2). Even or quadratic dependence on the off-axis displacement (e.g. Σ_ρ Re[1/ρ(1−ρ)]-type quantities, or Weil's pairing where off-critical zeros contribute through (σ−½)² > 0) is one natural **sufficient** design — but not mandatory: literature-standard global positivity criteria such as Weil's or Li's may realize the sensitivity **nonlocally** (Li's λ_n = Σ_ρ [1−(1−1/ρ)ⁿ] are nonlinear in the zero positions, valid under the prescribed symmetric zero summation, not per-zero quadratic terms).

**K0-5. Provability audit.** Determine whether a genuine RH-equivalent positivity theorem is provable for the chosen object within the canon's toolkit and no-smuggling rules — or whether the equivalence must enter as a **cited external criterion** with declared import status.

**K0-6. Anchor decision (resolved by review, MIG-022): Weil positivity is the primary K0 anchor; Li coefficients serve as an independent scalar cross-check.** Weil's explicit-formula positivity (RH ⟺ W(f∗f̃) ≥ 0 for the declared test class) is naturally formulated through a quadratic form on a declared test class — exactly the shape NFC's S1 machinery already has (test functions, probe admissibility, density, separation) — so re-anchoring to Weil preserves the existing probe-family ladder. The Li criterion (RH ⟺ λ_n ≥ 0 for all n, with λ_n = Σ_ρ [1−(1−1/ρ)ⁿ] under the prescribed symmetric zero summation) is a sequence-positivity formulation, nonlinear in the zero positions; it would require more substantial reorganization if primary, but Bombieri–Lagarias relate its positivity mechanism to the broader Weil-type framework, making it the natural independent cross-check. The bespoke kernel route remains available only if K0-5 finds it provable; otherwise both `def:rh-kernel` texts are preserved as superseded intake per prohibition (13).

## 3. Recorded positive result (reviewer-supplied; independently verified): rational-scale Γ-span density

> **Lemma K0.A (density of the rational-scale family).** With f₀(x) = x^{1/2}e^{−x}, the Mellin transform gives 𝓜f₀(τ) = Γ(½+iτ) (verified symbolically), and 𝓜(U_q f₀)(τ) = q^{−iτ}Γ(½+iτ). Then
> span{ q^{−iτ}Γ(½+iτ) : q ∈ ℚ₊ } is **dense in L²(ℝ, dτ)**.
> *Proof (recorded).* Suppose h ∈ L² is orthogonal to every member. Then g(τ) := h(τ)·Γ(½+iτ)̄ ∈ L¹(ℝ) (Cauchy–Schwarz: h ∈ L² and Γ(½+iτ) ∈ L² by the exponential decay |Γ(½+iτ)| ≍ e^{−π|τ|/2}). Orthogonality says the Fourier transform ĝ vanishes at every point of log ℚ₊, which is dense in ℝ; ĝ is continuous (g ∈ L¹), hence ĝ ≡ 0; Fourier uniqueness gives g = 0 a.e.; Γ(½+iτ) never vanishes, so h = 0 a.e. ∎

**Role and limit of this result:** it supplies the natural candidate for **P0-4's density requirement** (totality of the repaired probe family). It yields separation only after K0 fixes the quadratic form, and the transfer condition is form-theoretic: if the form is **bounded/continuous on L²**, ordinary L²-density of the Γ-span suffices; if the form is **unbounded but closed**, L²-density is NOT enough — the rational-scale span must additionally be proved a **form core**, i.e. dense in the form domain under the form norm. Hence the gate order:

> **K0 (Weil specification) → P0 (probe repair + form core) → S1-ARC-0**

## 4. Prohibited paths (inherited + new)

All prior prohibitions stand. Additionally: **(10)** no canon repair of `def:rh-kernel` may commit to object type (a) or (b) without the K0-1 determination recorded in the migration entry; **(11)** no repaired positivity claim may rest on pointwise signs of F under the difference-kernel reading (Bochner governs); **(12)** no first-order real-part zero sum may be used as an RH detector (D2 cancellation is structural); **(13)** if K0-6 re-anchors to Weil/Li, the bespoke kernel texts are preserved as superseded intake (Phase-3 Rules 4–5), never deleted.

## 5. Falsification criteria for K0 itself

- **K0-F1:** a proof that no quadratic-in-(σ−½) functional expressible in the canon's declared arithmetic data can be both computable from ζ-side data and sign-definite would falsify the bespoke-repair route and force K0-6's re-anchoring branch.
- **K0-F2:** failure of the chosen form to be closable on any domain containing the (repaired) probe family falsifies the K0-3 choice and reopens K0-1.
- **K0-F3:** discovery that the Γ-span density lemma's decay input fails for the actually-chosen weighting (e.g., a different critical-line measure) voids Lemma K0.A's applicability to P0-4 and requires a new total set.

## 6. Exit criteria

K0 closes when: the object type is fixed (K0-1) with regularized definition (K0-2) and a proved form-domain statement (K0-3); the off-critical contribution is sign-definite quadratic in (σ−½) (K0-4); and either a provable bespoke equivalence is exhibited (K0-5) or the branch is re-anchored to Weil/Li (K0-6) — each entering canon only through individually-reviewed, migration-gated edits with all superseded texts preserved as intake. Then P0 canon migration unlocks; then S1-ARC-0.
