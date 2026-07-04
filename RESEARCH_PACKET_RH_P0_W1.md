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

is a closed subspace of **codimension exactly 2**: the moment map L = (L₊,L₋) is surjective, since two distinct dilates give linearly independent moment vectors — L₊(H_q) = √π/2q, L₋(H_q) = √π, with det[[√π/2, √π],[√π/4, √π]] = π/4 ≠ 0 (verified). **This is the domain on which the Weil form will be posed.**

## 3. The generator and its rational dilates lie in 𝓗¹_a

The generator (image of f₀(x) = √x e^{−x} under the intertwiner) is

> H₀(t) = eᵗ e^{−eᵗ}.

- **Membership H₀ ∈ 𝓗¹_a for a < 1** (verified): as t → +∞ the double-exponential e^{−eᵗ} dominates every polynomial/exponential, so both weighted norms converge; as t → −∞, H₀(t) ∼ eᵗ and e^{a|t|}H₀ ∼ e^{(1−a)t} → 0 with a finite L² tail iff a < 1. H₀′(t) = (1 − eᵗ)H₀(t) has the same tails. So **H₀ ∈ 𝓗¹_a for a < 1**; the **joint program range** is ½ < a < 1, because moment continuity (§2) and prime summability (T1) impose the lower bound a > ½.
- **Rational dilates as weighted translates:** H_q(t) = q^{−1/2} H₀(t + log q), q ∈ ℚ₊. Translation moves the −∞ tail, so H_q ∈ 𝓗¹_a for the same a (the weight e^{a|t|} is translation-*quasi*-invariant: ‖H_q‖_{𝓗¹_a} ≤ e^{a|log q|}·const).
- **Moments of the generator (verified):** L₊(H₀) = Γ(3/2) = √π/2, L₋(H₀) = Γ(1/2) = √π — both nonzero, so H₀ ∉ 𝓗¹_{a,0}; the constrained combinations of §5 are needed.

## 4. Bilateral Laplace transform and the zero-free strip

> ∫_ℝ H₀(t) e^{zt} dt = Γ(1 + z)  (verified to 18 digits at z = 0.3 + 0.7i; it is the substitution u = eᵗ giving ∫₀^∞ u^z e^{−u} du).

Γ(1 + z) is **zero-free** and analytic in the strip |Re z| ≤ a < 1 (poles only at z = −1, −2, …). Consequently the Mellin/Laplace images {q^{−z}Γ(1+z) : q ∈ ℚ₊} share a common zero-free analytic factor — the structural fact behind the density candidate (§6), exactly parallel to Lemma K0.A but now in the form-domain topology.

## 5. Theorem targets

**T1 — Form continuity on 𝓗¹_{a,0} — PROVED (promoted from target, MIG-028).** Let w(t) = e^{a|t|} and Φ = H ∗ K̃ (K̃(t) = K(−t)‾). Weight **submultiplicativity** w(t) ≤ w(s)w(t−s) plus Cauchy–Schwarz give, directly,

> e^{a|t|}|Φ(t)| = |∫ w(t)H(s)K̃(t−s) ds| ≤ ∫ w(s)|H(s)|·w(t−s)|K̃(t−s)| ds ≤ ‖wH‖₂‖wK‖₂,

and differentiating under the integral onto either factor,

> e^{a|t|}|Φ′(t)| ≤ min(‖wH′‖₂‖wK‖₂, ‖wH‖₂‖wK′‖₂).

Hence |Φ(t)| + |Φ′(t)| ≤ C e^{−a|t|}‖H‖_{𝓗¹_a}‖K‖_{𝓗¹_a}. The **prime series** is then bounded by C‖H‖‖K‖ Σ_{n≥2} Λ(n)/n^{a+1/2}, which **converges because a + ½ > 1** (equivalently −ζ′/ζ(a+½) < ∞). For the **archimedean integral** the apparent singularity at t = 0 is removable — the numerator is O(t) by the C¹ bound while 1 − e^{−2t} = O(t) — and at infinity the same e^{−a|t|} estimate gives integrability. So the imported Weil functional 𝔔_W extends to a **continuous** Hermitian form on 𝓗¹_{a,0}. *(a > ½ pays off twice — moments AND prime sum.)* **Status: proved scaffold lemma.**

**T2 — Determining-domain theorem — CLOSED (no density theorem needed, MIG-028).** The equivalence follows directly from Burnol's compact-support form of Weil's criterion (arXiv:math/9810169), **without** proving 𝓗¹_{a,0} dense in 𝒲₀:
- *(⇒, under RH)* positivity extends to all of 𝓗¹_{a,0} by a compact-support moment-zero density argument: (1) C_c^∞(ℝ) is dense in 𝓗¹_a; (2) choose two compactly supported functions whose moment vectors span ℂ²; (3) correct cutoff/mollified approximants by those two so both moments vanish; (4) hence C_c^∞ ∩ 𝓗¹_{a,0} is dense in 𝓗¹_{a,0}; (5) T1 continuity extends Weil positivity from that dense compact-support subclass to the whole space. (Routine; introduces no new gate.)
- *(⇐)* positivity on 𝓗¹_{a,0} **includes** positivity on C_c^∞(0,∞) ∩ 𝒲₀ — and Burnol shows this compactly supported subclass already detects any off-critical zero (his non-RH-direction counterexample test function can be chosen with Mellin values zero at both 0 and 1, i.e. inside 𝒲₀ and, being smooth and compactly supported in log-coordinates, inside 𝓗¹_{a,0}).

So positivity on 𝓗¹_{a,0} ⟺ RH. The determining-domain implication is supplied by Burnol's direct construction; **T2 is closed** — there is no need for a density theorem here. **Status: closed by imported result** (Burnol criterion, recorded as external import alongside the Weil baseline).

**T3 — Constrained rational-scale core — REDUCED to one cyclicity theorem (MIG-028).**

> 𝒟_ℚ := span{ H_q : q ∈ ℚ₊ } ∩ ker L₊ ∩ ker L₋  dense in 𝓗¹_{a,0}.

**Finite-dimensional moment-correction lemma (proved).** Because L = (L₊,L₋) is surjective (codim exactly 2, above), 𝒟 = span{H_q} contains a two-element right inverse for L: pick dilates whose moment vectors span ℂ². Then **if D is dense in X = 𝓗¹_a, then D ∩ ker L is dense in ker L = 𝓗¹_{a,0}.** Proof: given F ∈ ker L and ε, take D ∋ G with ‖F − G‖ < ε; G has small but nonzero moments L(G) = (L(G−F)); subtract the right-inverse combination R·L(G) ∈ D (with ‖R·L(G)‖ ≤ ‖R‖‖L‖ε by continuity of L, T1-style); then G − R·L(G) ∈ D ∩ ker L and is within (1+‖R‖‖L‖)ε of F. ∎

So the **constrained** density T3 reduces to the **unconstrained** density of D in X — i.e. to a pure cyclicity statement with no moment side-conditions:

> **Γ strip-cyclicity theorem (the sole remaining analytic gate).**
> closure_{𝓗¹_a} span{ q^{−1/2} H₀(· + log q) : q ∈ ℚ₊ } = 𝓗¹_a.

Since log ℚ₊ is dense in ℝ and translation is continuous on 𝓗¹_a, this is equivalent to **cyclicity of H₀ under all real translations** in 𝓗¹_a.

## 6. The single remaining gate: cyclicity of Γ(1−iz) in the Hardy–Sobolev strip

After T1 (proved) and T2 (closed), and the moment-correction lemma reducing T3 to unconstrained cyclicity, the **entire** remaining analytic content is one question. Under the strip Fourier–Laplace transform, H₀ maps to **Γ(1−iz)**, analytic and zero-free on the strip |Im z| ≤ a < 1 (poles only at z = −i, −2i, …). The gate:

> **Is H₀ cyclic under real translations in 𝓗¹_a — equivalently, is Γ(1−iz) cyclic in the corresponding exponential-weight Hardy–Sobolev strip space?**

**What is NOT a proof.** Zero-freeness of Γ(1−iz) on the strip is necessary but **must not be treated as sufficient** for cyclicity (prohibition 15, sharpened). The failure of Beurling–Domar for ω(t) = e^{a|t|} (Σ a·n/n² diverges, verified in MIG-027) blocks one standard *algebraic* route — but **it does not establish incompleteness**; it only removes the generic Wiener–Tauberian argument.

**Correct literature anchors (hypotheses to verify against this exact space, not invoked generically):**
- **Borichev–Hedenmalm, "Completeness of translates in weighted spaces on the half-line"** (Acta Math.): directly about completeness of translates in weighted spaces *including quasianalytic regimes* — the focused anchor for this problem, far more apposite than a generic weighted-Wiener invocation.
- **Dales–Hayman / Esterle** (Beurling-algebra Tauberian, Numdam AIF_1981__31_4_141_0): a genuine Tauberian source, but its applicability to *this* weighted Sobolev strip must be **demonstrated**, since the weight is quasianalytic here — not presumed.
- de Branges spaces remain a secondary route (structure function tied to Γ) if the translation-cyclicity framing stalls.

**Falsification criteria (updated).**
- **W1-F1:** a proof that {q^{−1/2}H₀(·+log q)} is *incomplete* in 𝓗¹_a settles the gate negatively — f₀/H₀ must be replaced or the family enlarged beyond pure dilates. (Note: incompleteness is exactly what Beurling–Domar failure does *not* prove.)
- **W1-F2:** if Borichev–Hedenmalm-type completeness provably cannot hold for ω(t) = e^{a|t|} at any ½ < a < 1, the weighted-Sobolev model is the wrong completion and the form-domain choice (K0-3) reopens.
- **W1-F3 is retired:** T2 is closed, so "positivity on 𝓗¹_{a,0} is strictly weaker than 𝒲₀ positivity" is no longer a live failure mode.

## 7. Prohibited paths (inherited + new)

All K0/K0-W1 prohibitions stand. Additionally: **(14)** no claim that 𝒟_ℚ is a core may rest on unweighted L²-density (Lemma K0.A alone) — the form norm and both moment constraints must be controlled; **(15)** no invocation of a "weighted Wiener–Tauberian theorem" without exhibiting the exact theorem and verifying its hypotheses against ω(t) = e^{a|t|} (which fails Beurling–Domar) — generic invocation is barred; **(16)** [DISCHARGED — T2 closed via Burnol] the determining-domain equivalence is now proved, not an open obligation; **(17)** zero-freeness of Γ(1−iz) on the strip may not be cited as cyclicity — a completeness theorem with verified hypotheses is required.

## 8. Status and exit criteria (updated, MIG-028)

- **T1 (form continuity): PROVED** (submultiplicativity + Cauchy–Schwarz; prime sum converges for a > ½).
- **T2 (determining domain): CLOSED** (Burnol compact-support Weil criterion; no density theorem needed).
- **T3 (constrained core): REDUCED** to the single Γ strip-cyclicity theorem via the proved finite-dimensional moment-correction lemma.

P0-W1 therefore closes when the **Γ strip-cyclicity theorem** is settled — the sole remaining analytic gate. It is no longer a diffuse "weighted form-core topology" problem but the sharply stated question of whether Γ(1−iz) is cyclic in the exponential-weight Hardy–Sobolev strip (½ < a < 1), to be attacked via Borichev–Hedenmalm completeness-of-translates with hypotheses verified against this weight. The certified finite tests M₃–M₁₂ (K0-W2) are retained as **evidence only** — finite-dimensional shadows consistent with the form's positivity, carrying no RH content until cyclicity closes T3 and P0-WEIL-CORE follows.

**Updated gate sequence:** MIG-026 ✓ → T1 ✓ / T2 ✓ / T3-reduction ✓ (MIG-028) → **Γ strip-cyclicity (sole active gate)** → P0-WEIL-CORE → all-N positivity.
