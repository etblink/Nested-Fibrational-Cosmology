# Research Packet — P0-WEIL-CORE: Closure via Direct Γ Strip-Cyclicity

**Class:** scaffold planning document; **not canon**. Records the closure of P0-WEIL-CORE. **Every step below was independently verified** (symbolically and/or numerically to ≥15 digits) before recording; the verification log is reproduced in §5. **This closes a form-core theorem, NOT the Riemann Hypothesis**: it establishes an exact *conditional equivalence* (RH ⟺ positivity of every rational-height compressed Weil matrix), turning the infinite matrix program into a non-vacuous exact system. No finite calculation is RH evidence in the theorem-proving sense.

**Import status:** the Γ strip-cyclicity proof is elementary (Riesz representation → Laplace injectivity → constant-coefficient Sturm–Liouville ODE) and is recorded here in full; the Weil criterion and Burnol compact-support criterion remain external imports.

---

## 1. Status of the three P0-W1 targets (all closed)

- **T1 — form continuity: PROVED** (MIG-028; submultiplicativity + Cauchy–Schwarz; prime sum converges for a > ½).
- **T2 — determining domain: CLOSED** (Burnol compact-support Weil criterion; forward implication completed by the compact-support moment-zero density argument now recorded in P0-W1 §5).
- **T3 — constrained rational-scale core: PROVED** (this packet; direct cyclicity, below). Combined with the finite-dimensional moment-correction lemma (P0-W1), 𝒟_ℚ is dense in 𝓗¹_{a,0}.

Therefore **P0-WEIL-CORE is CLOSED**: 𝒟_ℚ is a core for 𝔔_W on the declared Weil form domain 𝓗¹_{a,0}.

## 2. The Γ strip-cyclicity theorem (direct proof — Riesz / Laplace / Sturm–Liouville)

**Theorem.** For ½ < a < 1, closure_{𝓗¹_a} span{ H_q : q ∈ ℚ₊ } = 𝓗¹_a, where H_q(t) = q^{−1/2}H₀(t + log q) = √q · eᵗ e^{−q eᵗ}.

**Proof (verified).** Let X = 𝓗¹_a with ⟨F,G⟩_X = ∫_ℝ e^{2a|t|}(F Ḡ + F′ Ḡ′) dt. Suppose F ∈ X is orthogonal to every H_q, q ∈ ℚ₊; continuity in q extends this to every q > 0. With u = eᵗ and the weight W(u) = u^{−2a} (0<u<1), u^{2a} (u>1):

> 0 = q^{−1/2}⟨F,H_q⟩_X = ∫₀^∞ e^{−qu}[ W(F + Ḟ) − q W u Ḟ ] du.   (identity verified to 24 digits, §5.i)

Setting A(u) = W(F + Ḟ), C(u) = W u Ḟ: the second term integrates by parts to ℒ(C′)(q) with **boundary terms vanishing** at u = 0 and u = ∞ — this is exactly where **a < 1** is used (endpoint cutoffs; verified, §5.ii). So ℒ(A)(q) = ℒ(C′)(q) for all q > 0, and **Laplace injectivity** gives C′ = A distributionally, i.e. back in t:

> **(e^{2a|t|}F′)′ = e^{2a|t|}F.**   (a constant-coefficient Sturm–Liouville equation on each half-line)

- On t < 0 (weight e^{−2at}): F″ − 2aF′ − F = 0, roots a ± κ with κ = √(a²+1); X-membership (decay as t → −∞) keeps only **F = C e^{(a+κ)t}** (verified: the a−κ root blows up in X-norm).
- On t > 0 (weight e^{2at}): F″ + 2aF′ − F = 0, roots −a ± κ; X-membership keeps only **F = D e^{(−a−κ)t}**.

Two junction conditions from H¹ regularity of the distributional ODE: **F continuous at 0** ⟹ C = D; **the weighted flux e^{2a|t|}F′ continuous at 0** (no delta source) — and since the weight is 1 at t = 0, this is F′ continuity — ⟹ (a+κ)C = −(a+κ)D. Together **C = D = 0**, so F ≡ 0. The orthogonal complement of the rational-scale orbit is trivial; the span is dense. ∎ (All four algebraic steps verified, §5.iii.)

**Range:** the proof works throughout the joint program range ½ < a < 1.

## 3. Why no weighted Tauberian theorem is needed — and why Borichev–Hedenmalm does not apply

The failure of Beurling–Domar (MIG-027) blocked only the generic algebraic route; it never implied incompleteness. The direct Riesz/Laplace/Sturm–Liouville argument bypasses Tauberian machinery entirely. Moreover **Borichev–Hedenmalm's completeness-of-translates theorem does not cover this space**: their main theorem assumes a **subexponential weight** with log ω(t) = o(t), whereas here log ω(t) = a|t| is exactly linear, not o(t) (verified). The earlier MIG-028 anchor to Borichev–Hedenmalm is therefore *informative but inapplicable*; the closure rests on the self-contained proof above, not on that reference.

## 4. Consequence: the exact RH-equivalent rational-height matrix program

With P0-WEIL-CORE closed, the finite program acquires an **exact, non-vacuous equivalence** (previously the finite slices were merely suggestive):

**Rational-height exhaustion.** Q_H := { m/n > 0 : 1 ≤ m,n ≤ H, gcd(m,n) = 1 }; then ⋃_{H≥1} Q_H = ℚ₊ (whereas the old integer sequence Q_N = {1,…,N} does **not** exhaust ℚ₊, so integer-scale positivity alone would not reach the core). For each H compress the ambient Weil matrix to the two-moment nullspace as before (nested basis, V_H-compression), giving M_H.

> **RH ⟺ M_H ⪰ 0 for every H.**

*Forward:* Weil positivity (imported) gives every M_H ⪰ 0. *Converse:* positivity of every M_H gives positivity on every finite rational-scale combination, hence on 𝒟_ℚ; core density (P0-WEIL-CORE) + T1 continuity extend it to 𝓗¹_{a,0}; T2 gives RH.

**This does not make any finite M_H an RH proof-step.** It places the infinite program on an exact equivalence rather than a suggestive slice. The certified integer-scale results Q₃–Q₁₂ (K0-W2, all PD) remain **valid first slices** of this larger directed system — evidence, not proof.

## 5. Independent verification log (this session, before recording)

- **(i)** The Laplace identity q^{−1/2}⟨F,H_q⟩_X = ∫₀^∞ e^{−qu}[W(F+Ḟ) − qWuḞ]du: confirmed for a test F = e^{−t²} at q = 0.5, 1, 2.3 to 13–24 digits.
- **(ii)** Integration-by-parts qℒ(C) = ℒ(C′) with boundary terms e^{−qu}C(u) → 0 at both ends (a = 0.7): boundary values ~10^{−225} (u→0) and ~10^{−36} (u→∞); identity matched to 30 digits.
- **(iii)** ODE root selection and junction algebra: t<0 roots a±κ, t>0 roots −a±κ (sympy); X-membership selects the decaying root each side; C=D from continuity; (a+κ)C = −(a+κ)D from flux continuity ⟹ C=D=0.
- **(iv)** Borichev–Hedenmalm hypothesis log ω(t) = o(t) fails for ω(t)=e^{a|t|} (log ω = a|t|): confirmed inapplicable.
- **(v)** Moment values L₊(H_q)=√π/2q, L₋(H_q)=√π and moment-vector independence (det = π/4): confirmed (P0-W1).

## 6. Prohibited paths (inherited + new) and standing classification

All prior prohibitions stand. **(18)** No statement may describe P0-WEIL-CORE's closure, or the RH ⟺ {M_H ⪰ 0} equivalence, as evidence *for* RH: the equivalence is conditional and symmetric; a finite positive M_H is a consistency check, not a theorem-step. **(19)** The RH-equivalence may enter canon only as a structure built on the **imported** Weil + Burnol criteria (external), never as an NFC-internal proof of RH. **Classification:** the certified M₃–M₁₂ remain restricted finite Weil tests; P0-WEIL-CORE is a proved form-core theorem about the declared domain; RH itself remains open and is claimed nowhere.
