# Research Packet — P0-W1: The Weil Form Domain (weighted Sobolev model)

**Class:** scaffold planning document; **not canon**. Establishes the functional-analytic setting in which P0-WEIL-CORE will be posed, per the reviewer's mandate. Pauses further Q_N expansion: the computational pipeline (K0-W2, certified through Q₁₂) is demonstrated; the bottleneck is now the **form-core topology**, which no finite matrix can settle.

**Gate sequence:** MIG-026 certificate closure ✓ → **P0-W1 form domain (this packet)** → P0-WEIL-CORE → all-N positivity program.

All analytic claims below were checked (symbolically or to ≥15 digits) before recording; the one genuine obstacle — the weight fails Beurling–Domar — is flagged as an explicit open sub-problem, not smoothed over.

---

## 1. Logarithmic coordinates and the weighted Sobolev space

Put t = log x and H(t) = e^{t/2} g(eᵗ) (the unitary L²(dx/x) → L²(ℝ, dt) intertwiner composed with the e^{t/2} twist that symmetrizes the functional equation about Re s = ½). Fix once **½ < a < 1** and define

> 𝓗¹_a := { H : e^{a|t|}H ∈ L²(ℝ) and e^{a|t|}H′ ∈ L²(ℝ) },  ‖H‖²_{𝓗¹_a} := ‖e^{a|t|}H‖²₂ + ‖e^{a|t|}H′‖²₂.

This is a Hilbert space (weighted Sobolev). The lower bound a > ½ is what makes the two Weil moments **continuous** (§2); the upper bound a < 1 is what keeps the generator inside the space and the prime side summable (§3–4).

## 2. The two Weil moments are continuous functionals

In these coordinates the moment functionals are

> L_±(H) = ∫_ℝ H(t) e^{±t/2} dt.

**Continuity (a > ½).** |L_±(H)| ≤ ∫ |H(t)| e^{±t/2} dt = ∫ (e^{a|t|}|H(t)|)·(e^{±t/2−a|t|}) dt ≤ ‖e^{a|t|}H‖₂ · ‖e^{±t/2−a|t|}‖₂ by Cauchy–Schwarz, and the second factor is finite iff the exponent ±t/2 − a|t| → −∞ fast enough on both tails, i.e. iff a > ½ (for t → ±∞, ±t/2 − a|t| = (±½ ∓ a)|t| ... the binding tail gives (½ − a)|t|, square-integrable iff a > ½). Hence L_± ∈ (𝓗¹_a)* and

> 𝓗¹_{a,0} := ker L₊ ∩ ker L₋

is a closed subspace of codimension ≤ 2. **This is the domain on which the Weil form will be posed.**

## 3. The generator and its rational dilates lie in 𝓗¹_a

The generator (image of f₀(x) = √x e^{−x} under the intertwiner) is

> H₀(t) = eᵗ e^{−eᵗ}.

- **Membership H₀ ∈ 𝓗¹_a for a < 1** (verified): as t → +∞ the double-exponential e^{−eᵗ} dominates every polynomial/exponential, so both weighted norms converge; as t → −∞, H₀(t) ∼ eᵗ and e^{a|t|}H₀ ∼ e^{(1−a)t} → 0 with a finite L² tail iff a < 1. H₀′(t) = (1 − eᵗ)H₀(t) has the same tails. So H₀ ∈ 𝓗¹_a exactly on ½ < a < 1.
- **Rational dilates as weighted translates:** H_q(t) = q^{−1/2} H₀(t + log q), q ∈ ℚ₊. Translation moves the −∞ tail, so H_q ∈ 𝓗¹_a for the same a (the weight e^{a|t|} is translation-*quasi*-invariant: ‖H_q‖_{𝓗¹_a} ≤ e^{a|log q|}·const).
- **Moments of the generator (verified):** L₊(H₀) = Γ(3/2) = √π/2, L₋(H₀) = Γ(1/2) = √π — both nonzero, so H₀ ∉ 𝓗¹_{a,0}; the constrained combinations of §5 are needed.

## 4. Bilateral Laplace transform and the zero-free strip

> ∫_ℝ H₀(t) e^{zt} dt = Γ(1 + z)  (verified to 18 digits at z = 0.3 + 0.7i; it is the substitution u = eᵗ giving ∫₀^∞ u^z e^{−u} du).

Γ(1 + z) is **zero-free** and analytic in the strip |Re z| ≤ a < 1 (poles only at z = −1, −2, …). Consequently the Mellin/Laplace images {q^{−z}Γ(1+z) : q ∈ ℚ₊} share a common zero-free analytic factor — the structural fact behind the density candidate (§6), exactly parallel to Lemma K0.A but now in the form-domain topology.

## 5. Theorem targets

**T1 — Form continuity on 𝓗¹_{a,0}.** For Φ = H ∗ K̃ (multiplicative autocorrelation in log-coordinates, K̃(t) = K(−t)‾), establish

> |Φ(t)| + |Φ′(t)| ≤ C e^{−a|t|} ‖H‖_{𝓗¹_a} ‖K‖_{𝓗¹_a}.

The e^{−a|t|} decay is what makes both sides of the explicit formula converge on 𝓗¹_{a,0}: the **prime side** Σ_n Λ(n) n^{−1/2}[Φ(log n) + Φ(−log n)] is dominated by C‖H‖‖K‖ Σ_n Λ(n) n^{−1/2−a}, finite because Σ Λ(n) n^{−1/2−a} = −ζ′/ζ(½ + a) < ∞ for a > ½ (the very lower bound already forced by moment continuity); the **archimedean side** ∫₁^∞[…] dx/(x − x^{−1}) converges by the same pointwise bound. So the imported Weil functional 𝔔_W extends to a continuous Hermitian form on 𝓗¹_{a,0}. *(This is where a > ½ pays off twice — moments AND prime sum.)*

**T2 — Determining-domain theorem.** Positivity of 𝔔_W on 𝓗¹_{a,0} must be **equivalent** to the imported Weil criterion (positivity on all of 𝒲₀), not merely positivity on a smaller harmless subspace. Route: show 𝒲₀ ∩ (image of 𝓗¹_{a,0}) is dense in 𝒲₀ in the Weil-form topology, so no negative direction of the full criterion is invisible to 𝓗¹_{a,0}. Until T2 is proved, positivity on 𝓗¹_{a,0} is **not** known to imply RH — this is the determining-domain obligation and must not be elided.

**T3 — Constrained rational-scale core.**

> 𝒟_ℚ := span{ H_q : q ∈ ℚ₊ } ∩ ker L₊ ∩ ker L₋

is dense in 𝓗¹_{a,0} in the form topology. (In log-coordinates the §6 K0-W1 constraints Σc_j = 0, Σc_j/q_j = 0 become the two moment kernels; minimum three distinct rational scales for a nonzero member.)

## 6. The density obstacle — stated precisely as an open sub-problem (reviewer's caution, confirmed)

T3 needs a **weighted** density theorem; ordinary unweighted L²-density (Lemma K0.A) is insufficient because the two moment constraints and the form norm ‖·‖_{𝓗¹_a} must both be controlled. The natural tool is a weighted Wiener–Tauberian / Beurling-algebra theorem for the weight ω(t) = e^{a|t|}. **But this weight fails the standard admissibility hypothesis, and that failure is real:**

> **Obstacle (verified).** The Beurling–Domar non-quasianalyticity condition Σ_{n≥1} log ω(n)/n² < ∞ **fails** for ω(t) = e^{a|t|}: log ω(n) = a·n, so Σ a·n/n² = a·Σ 1/n **diverges** for every a > 0.

Therefore the classical weighted-Wiener–Tauberian route (Beurling–Domar; cf. Esterle's proof for Beurling algebras, Numdam 10.5802/aif.852) is **not applicable to this weight as stated**. This is a genuine gap, flagged here as an explicit open sub-problem rather than invoked generically. Candidate substitutes, each to be identified precisely (with its exact hypotheses checked against ω) before use:

- **(C1) Beurling strip / quasianalytic-boundary theorems** exploiting that H₀'s transform Γ(1+z) is analytic and zero-free in |Re z| ≤ a — density may follow from a *completeness* argument on the zero-free analytic factor rather than a Tauberian one (the quasianalyticity that defeats Beurling–Domar can itself force completeness of the dilate system, à la Beurling–Malliavin territory).
- **(C2) Weighted Bernstein / Beurling–Malliavin** completeness for exponential systems {q^{−iτ}} against the multiplier Γ(½ + iτ): the density radius is governed by log ℚ₊ being dense, and the admissible-majorant machinery may supply the form-norm control the Tauberian route cannot.
- **(C3) de Branges spaces:** the twisted transform lands in a de Branges space with structure function tied to Γ; density of 𝒟_ℚ becomes a reproducing-kernel completeness question there.

**Falsification criteria for P0-W1.**
- **W1-F1:** if every ℚ₊-dilate system of a single 𝓗¹_a generator is provably *incomplete* in 𝓗¹_{a,0} (form norm), T3 fails for this generator and f₀/H₀ must be replaced or the family enlarged beyond pure dilates.
- **W1-F2:** if no weighted-completeness theorem applies to ω(t) = e^{a|t|} (all of C1–C3 obstructed), the weighted-Sobolev model itself is the wrong domain and the form-core must be sought in a different completion (reopening the K0-3 form-domain choice).
- **W1-F3:** if T2 fails — 𝓗¹_{a,0} positivity is strictly weaker than 𝒲₀ positivity — then even a proven core would not reach RH, and the determining-domain step must be redesigned.

## 7. Prohibited paths (inherited + new)

All K0/K0-W1 prohibitions stand. Additionally: **(14)** no claim that 𝒟_ℚ is a core may rest on unweighted L²-density (Lemma K0.A alone) — the form norm and both moment constraints must be controlled; **(15)** no invocation of a "weighted Wiener–Tauberian theorem" without exhibiting the exact theorem and verifying its hypotheses against ω(t) = e^{a|t|} (which fails Beurling–Domar) — generic invocation is barred; **(16)** T2 (determining domain) may not be skipped: positivity on 𝓗¹_{a,0} carries no RH content until equivalence to the full Weil criterion is proved.

## 8. Exit criteria

P0-W1 closes when T1 (form continuity) and T2 (determining domain) are proved, and T3 (constrained core) is either proved via a precisely-identified weighted-completeness theorem (one of C1–C3 with hypotheses verified) or explicitly reduced to a named, literature-anchored open problem. Only then does P0-WEIL-CORE — now a *theorem about this concrete domain* rather than a schematic burden — become the active target, with the certified finite tests M_N ⪰ 0 (K0-W2) as its already-established finite-dimensional shadows.
