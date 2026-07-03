# Research Packet — K0-W1: The Weil Specification (Imported Baseline)

**Class:** scaffold planning document; **not canon**. This packet records the authoritative K0-6 anchor decision in exact form: the **multiplicative Weil formulation** of the RH positivity criterion, imported from the literature with its precise test class, involution, explicit formula, summation prescription, and sign convention. It replaces the invalid bespoke kernel route (`def:rh-kernel` / `prop:rh-kernel-positivity`, defects D1–D4) as the criterion the RH branch will eventually stand on. **Canon remains untouched**; every eventual canon entry derived from this packet is individually migration-gated.

**Sources of record:** Bombieri's Clay Institute exposition of the Riemann Hypothesis (test class, explicit formula, positivity statement); Bombieri, *Remarks on Weil's quadratic functional in the theory of prime numbers, I* (the quadratic functional and its finite truncations); Bombieri–Lagarias (Li-coefficient connection to the Guinand–Weil framework). All computational identities below were independently re-verified (symbolically or by substitution) before recording.

---

## 1. Exact test class

𝒲 := the class of g : ℝ₊ → ℂ that are continuous and piecewise C¹, with only finitely many first-kind discontinuities in g or g′ (midpoint values taken there), satisfying, for some δ > 0,

> g(x) = O(x^δ) (x → 0⁺),  g(x) = O(x^{−1−δ}) (x → ∞).

Mellin convention: g̃(s) = ∫₀^∞ g(x) x^s dx/x, analytic in a strip containing 0 ≤ Re s ≤ 1.

**Moment-zero subclass** (the class the criterion quantifies over):

> 𝒲₀ := { g ∈ 𝒲 : g̃(0) = 0 and g̃(1) = 0 }, equivalently ∫₀^∞ g(x) dx/x = 0 and ∫₀^∞ g(x) dx = 0.

The two moment constraints are **essential parts of the Weil criterion**, not optional NFC filters.

## 2. Multiplicative involution and autocorrelation

> g⋆(x) := x^{−1} · g(1/x)‾  (involution);  (g∗h)(x) := ∫₀^∞ g(y) h(x/y) dy/y  (multiplicative convolution).

Then (verified by the substitution y = xu): (g∗g⋆)(x) = ∫₀^∞ g(xy) g(y)‾ dy. Set **f_g := g∗g⋆**. Its Mellin transform factorizes (verified: 𝓜g⋆(s) = g̃(1−s̄)‾ by x ↦ 1/x):

> f̃_g(s) = g̃(s) · g̃(1−s̄)‾.

On the critical line ρ = ½+iγ we have 1−ρ̄ = ρ, hence **f̃_g(ρ) = |g̃(ρ)|²**. This factorization is the correct replacement for the invalid pointwise-kernel argument (D1–D3).

## 3. Exact explicit-formula functional

For f ∈ 𝒲 define

> ℰ(f) := Σ_{n=1}^∞ Λ(n) [ f(n) + (1/n) f(1/n) ] + (log 4π + γ) f(1) + ∫₁^∞ [ f(x) + (1/x) f(1/x) − (2/x) f(1) ] dx/(x − x^{−1}),

where γ is Euler's constant and Λ is the von Mangoldt function. The **Weil explicit formula** is

> f̃(0) − Σ*_ρ f̃(ρ) + f̃(1) = ℰ(f),

with the zero sum taken in the **prescribed symmetric limit** Σ*_ρ := lim_{T→∞} Σ_{|Im ρ| < T}. These prime-power, archimedean, and zero terms are recorded **exactly**; no "~", no informal truncation, and no bare unregularized zero sum is permitted anywhere downstream (this discharges K0-2's prescription demand for the imported route).

## 4. The Weil quadratic form and the imported equivalence

Define first the **ambient form** on the full test class (domain correction, MIG-024):

> 𝔅̂_W(g,h) := −ℰ(g∗h⋆) for g, h ∈ 𝒲, whenever g∗h⋆ ∈ 𝒲,

and then the Weil form proper as its restriction:

> 𝔅_W := 𝔅̂_W |_{𝒲₀×𝒲₀},  𝔔_W(g) := 𝔅_W(g,g) = −ℰ(g∗g⋆).

The distinction matters because the finite-truncation matrices (§7) are built from **raw** probes U_qf₀ ∉ 𝒲₀: their unrestricted entries live in the ambient form, and only the V_N-compression lands in 𝒲₀.

Because both moments vanish on 𝒲₀, the explicit formula gives

> 𝔔_W(g) = Σ*_ρ g̃(ρ) · g̃(1−ρ̄)‾,  and under RH  𝔔_W(g) = Σ*_ρ |g̃(ρ)|² ≥ 0.

**Imported equivalence (the K0 criterion):**

> **RH ⟺ 𝔔_W(g) ≥ 0 for every g ∈ 𝒲₀.**

**Sign convention, fixed once:** 𝔔_W = −ℰ. This matches Bombieri's statement that the explicit-formula right-hand side is **nonpositive** on autocorrelations exactly when RH holds; the minus sign turns it into NFC-style positive semidefiniteness. No other sign convention may be introduced downstream.

## 5. Import status (binding)

This equivalence is **not** presented as internally derived by NFC. It enters, when canon migration is eventually authorized, as:

> **Imported Weil Criterion — `[B]` or declared external theorem:** the equivalence between RH and positivity of 𝔔_W on 𝒲₀ is imported with its exact hypotheses, test class, summation prescription, and explicit-formula normalization, attributed to Weil (with Bombieri's exposition as the normalization of record).

**The research burden is therefore NOT to reprove Weil's criterion.** It is to show that the repaired NFC probe family forms a **sufficient test core** for the imported criterion (§8).

## 6. The rational-scale family and the moment constraints

With f₀(x) = x^{1/2} e^{−x} (which lies in 𝒲: O(x^{1/2}) at 0, exponential decay at ∞) and (U_q f₀)(x) = f₀(qx):

> 𝓜(U_q f₀)(s) = q^{−s} Γ(s + ½)  (verified symbolically).

**The raw probes U_q f₀ are NOT in 𝒲₀:** each has moments g̃(0) = Γ(½) = √π ≠ 0 and g̃(1) = Γ(3/2)/q = √π/(2q) ≠ 0. For a combination g_c = Σ_{j=1}^m c_j U_{q_j} f₀, the two Weil moments vanish **exactly when**

> Σ_j c_j = 0  and  Σ_j c_j / q_j = 0.

Define the **candidate NFC probe core** (moment-constrained rational-scale family):

> 𝒟_ℚ := { Σ_{j=1}^m c_j U_{q_j} f₀ : q_j ∈ ℚ₊ distinct, Σ c_j = 0, Σ c_j q_j^{−1} = 0 }.

At least **three** distinct rational scales are needed for a generic nonzero constrained probe (two independent linear constraints; for m = 2 with q₁ ≠ q₂ the constraint matrix has trivial kernel). **𝒟_ℚ is a candidate probe core only — it is not yet called a form core** (that is P0-WEIL-CORE's burden, §8).

## 7. Finite truncations (the re-founded S1-ARC-0)

For a finite ordered scale set Q_N = {q₁, …, q_N} let

> A_N = [ 1 ⋯ 1 ; q₁^{−1} ⋯ q_N^{−1} ]  (2×N),  V_N = a chosen matrix whose columns form a basis of ker A_N.

Form the unrestricted Hermitian matrix **H_N(j,k) := 𝔅̂_W(U_{q_j} f₀, U_{q_k} f₀)** (the *ambient* form — the raw probes are not in 𝒲₀, so 𝔅_W itself is undefined on them; MIG-024 correction), then compress to the moment-null subspace:

> M_N := V_N* H_N V_N.  **The finite Weil test is M_N ⪰ 0.**

This is the correct re-founded form of S1-ARC-0. **It is a restricted finite positivity statement only.** It cannot discharge, weaken, or partially certify RH unless P0-WEIL-CORE (§8) is separately proved — and no finite positivity result may be described as "progress toward RH" without it. For nested scale sets Q_N ⊂ Q_{N+1}, the induction step may be expressed through principal extensions and Schur complements **only after** basis compatibility between ker A_N and ker A_{N+1} is explicitly fixed (the compression bases do not nest automatically).

## 8. The P0 theorem burden

> **P0-WEIL-CORE.** The constrained rational-scale space 𝒟_ℚ is a **core** for 𝔔_W on the declared Weil form domain.

The statement must specify what "core" means, per the form-theoretic dichotomy:
- if 𝔔_W extends to a **bounded** form on a Hilbert completion, density of 𝒟_ℚ in that Hilbert norm suffices;
- if it is **closed and unbounded**, 𝒟_ℚ must be dense in the form domain under the **form norm**.

**Density of the unconstrained Γ-span in plain L² (Lemma K0.A) does not by itself prove either claim:** the two moment conditions and the explicit-formula topology must also be controlled. Lemma K0.A is an ingredient, not the theorem.

## 9. Li cross-check (secondary, standing)

For every accepted normalization, independently compute the corresponding Li coefficients (or finite approximants) and verify consistency of signs and conventions; Bombieri–Lagarias connect Li positivity to the Guinand–Weil explicit formula and Weil's criterion. This remains a **cross-check, not the primary proof architecture**.

---

## K0-W1 acceptance gates (all must pass before this packet closes)

1. ☑ The exact class 𝒲₀ is stated (§1).
2. ☑ The involution, convolution, and Mellin factorization are proved (§2; verified by substitution).
3. ☑ The explicit formula is reproduced with the symmetric zero-sum prescription (§3).
4. ☑ The sign convention 𝔔_W = −ℰ is fixed once (§4).
5. ☑ The Weil equivalence is marked as an external import (§5).
6. ☑ The raw rational-scale probes are **not** claimed to satisfy the moment conditions (§6: they demonstrably do not; constraints derived and verified).
7. ☑ The constrained core 𝒟_ℚ is defined (§6).
8. ☑ Finite matrices are compressed to the moment-null subspace (§7: M_N = V_N* H_N V_N).
9. ☑ No finite positivity result is described as progress toward RH without P0-WEIL-CORE (§7, §8).
10. ☑ The stale quadratic exit criterion in the K0 packet is removed (MIG-023; K0 §6 now requires pairing-survival + off-critical sensitivity + a rigorous global positivity mechanism).

**Gate order (unchanged):** K0-W1 (this specification) → P0-WEIL-CORE (probe repair / form core) → S1-ARC-0 (finite Weil tests M_N ⪰ 0).
