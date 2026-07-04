# Research Packet — K0-W2: Certified Weil Matrix Entry Engine

**Class:** scaffold; **not canon**. Implements the computational track authorized alongside — never in place of — the P0-WEIL-CORE form-core theorem. Engine: `scripts/weil_engine.py` (Arb ball arithmetic via python-flint, 350-bit working precision). Result artifact: `metadata/weil_M3_result.json`.

**Standing classification (gate 8):** every number below is a **restricted finite Weil test** in the sense of K0-W1 §7. None constitutes, and none may be described as, progress toward RH absent P0-WEIL-CORE. The certified track uses **no zero-location assumption anywhere**.

---

## Gate 1 — Ambient form ☑
𝔅̂_W(g,h) := −ℰ(g∗h⋆) for g,h ∈ 𝒲 (whenever g∗h⋆ ∈ 𝒲), with 𝔅_W = 𝔅̂_W|_{𝒲₀×𝒲₀}. Recorded in the K0-W1 packet (§4, §7 corrected): the raw probes U_qf₀ ∉ 𝒲₀, so the unrestricted entries H_N(j,k) = 𝔅̂_W(U_{q_j}f₀, U_{q_k}f₀) live in the ambient form; V_N-compression restricts to the moment-zero subspace. Scaffold-definition repair only; no mathematical change.

## Gate 2 — Closed formulas, proved ☑
Verified symbolically (sympy, exact):
- **Cross-correlation:** (g_q∗g_r⋆)(x) = ∫₀^∞ √(qxy)e^{−qxy}·√(ry)e^{−ry} dy = **√(qrx)/(qx+r)²** =: f_{q,r}(x) ∈ 𝒲 (O(√x) at 0, O(x^{−3/2}) at ∞).
- **Mellin:** f̃_{q,r}(s) = q^{−s}r^{s−1}Γ(s+½)Γ(3/2−s) — sympy returns πr^{s−1}(1−2s)/(2qˢcos πs), identical by the reflection formula Γ(s+½)Γ(½−s) = π/cos πs with Γ(3/2−s) = (½−s)Γ(½−s). **Moments: f̃(0) = π/2r, f̃(1) = π/2q** (evaluated exactly).
- **Explicit-formula terms:** substituting f_{q,r} into ℰ gives exactly the packet's prime sum √(qr)ΣΛ(n)√n[1/(qn+r)² + 1/(q+rn)²], boundary √(qr)(log 4π+γ)/(q+r)², and archimedean J(q,r) — matching the review's displayed forms term-for-term.

## Gate 3 — Both evaluators implemented ☑
**Prime side (accelerated series):** T(q,r) = Σ_{2≤n≤N} Λ(n)√n/(qn+r)² + q^{−2}Σ_{m=0}^{M}(−1)^m(m+1)(r/q)^m S_m with S_m = −ζ′/ζ(m+3/2) − Σ_{n≤N}Λ(n)n^{−m−3/2}; the certified −ζ′/ζ values come from `arb_series([σ,1]).zeta()` (ball ζ and ζ′ simultaneously). N = 64, M = 48. Only real σ = m+3/2 > 1 occur — **no zero-location input**.
**Archimedean side (rational integral):** the substitution u = 1/t maps [1,∞) → [0,1] (no tail bound needed at all); the removable singularity at u = 1 is cancelled **exactly** by rational polynomial division (sympy `cancel` over ℚ, asserted nonvanishing denominator at u = 1); the resulting polynomial-quotient integrand is evaluated by Horner in complex balls and integrated by Arb's certified `acb_calc` over [0,1].

## Gate 4 — Explicit interval error bounds ☑
- Prime m-series truncation: |term_m| ≤ q^{−2}(m+1)(r/(qN))^m·N^{−1/2}(2 log N+4) via ∫_N^∞ log x·x^{−m−3/2}dx; the m > M remainder is bounded by the closed geometric-tail formula C·ρ^{M+1}[(M+2)−(M+1)ρ]/(1−ρ)², ρ = r/(qN), and the ball is **widened outward** by exactly this bound. With N = 64, M = 48, ρ ≤ 3/64: remainder < 10⁻⁶⁰.
- All other operations (head sums, ζ-series, Horner, acb_calc, constants π, γ, log 4π) are Arb balls: rounding is carried in the radius automatically. Final entry radii ≈ 10⁻²⁵; compressed-value radius ≈ 10⁻⁴⁷.

## Gate 5 — Nested rational basis ☑
b_k supported on coordinates (1,2,k): (b_k)₁ = q₁(q₂−q_k), (b_k)₂ = q₂(q_k−q₁), (b_k)_k = q_k(q₁−q₂). Both moment identities Σ(b_k)_j = 0, Σ(b_k)_j/q_j = 0 hold identically (asserted exactly in integer/Fraction arithmetic at runtime), the columns are independent (each owns coordinate k), and V_{N+1} = [V_N | b_{N+1}] nests — so M_N is the leading principal block of M_{N+1} and the Schur induction is canonical. For a possibly singular M_N the extension criterion is the generalized Schur condition u ∈ ran M_N, α − u*M_N†u ≥ 0 (recorded; not yet exercised, since M₃ is 1×1).

## Gate 6 — M₃ reproduced with a rigorous positive interval ☑
Q₃ = {1,2,3}, V₃ = (−1, 4, −3)ᵀ (engine assertion matches the review exactly). Certified unrestricted entries (ball radii ~10⁻²⁵), each equal to −(π/2)(1/q+1/r) plus a residual of order 10⁻¹⁷–10⁻¹⁸ — confirming that the moment compression cancels the rank-two boundary component exactly, as the review predicted:

| entry | certified ball |
|---|---|
| H(1,1) | −3.141592653589793229249401 ± 3.4e−25 |
| H(1,2) | −2.356194490192344934914554 ± 9.9e−26 |
| H(1,3) | −2.094395102393195497542346 ± 1.2e−25 |
| H(2,2) | −1.570796326794896614624701 ± 3.3e−25 |
| H(2,3) | −1.308996938995747179490208 ± 1.9e−25 |
| H(3,3) | −1.047197551196597743083134 ± 2.2e−25 |

> **M₃ = [5.08345272853045093738616917619×10⁻¹⁷ ± 1.43×10⁻⁴⁷] > 0 — RIGOROUSLY POSITIVE.**
> Rayleigh value M₃/‖b₃‖² = [1.955174126357865745148527×10⁻¹⁸ ± 4e−43] (‖b₃‖² = 26).

Both agree with the review's non-interval diagnostics (5.08345272853045094×10⁻¹⁷; 1.95517412635786575×10⁻¹⁸) to every stated digit. The review's precision warning is validated quantitatively: the signal sits 17 orders below the raw entries, so double precision (~10⁻¹⁶ relative) could never determine the sign; the certified track resolves it with ~30 digits to spare.

## Gate 7 — Zero-side cross-check (diagnostic only; certifies nothing) ☑
The symmetric zero-side value 2Σ_{γ>0}(πγ/sinh πγ)|Σ_j c_j q_j^{−1/2}e^{−iγ log q_j}|² over the first 10 zeros (mpmath, 60 dps) gives 5.083452728530450937386169176191424…×10⁻¹⁷ — agreeing with the certified prime-side value to ~30 digits (tail beyond zero #10 is O(γ₁₁e^{−πγ₁₁}) ~ 10⁻⁷⁰). This is a **convention-consistency check only**: it presumes computed zero locations and therefore certifies nothing (and is labeled so in the engine output).

## Gate 8 — Classification discipline ☑
The engine's console and JSON outputs carry the restricted-finite-Weil-test classification and the no-RH-progress disclaimer verbatim; the certified track's independence from zero locations is stated in the output itself.

---

## What M₃ > 0 does and does not mean
It means: the Weil quadratic form is rigorously positive on the **one-dimensional** moment-constrained slice spanned by −g₁ + 4g₂ − 3g₃ at scales {1,2,3}. It does not mean anything about RH (that requires positivity on all of 𝒲₀, i.e., P0-WEIL-CORE plus positivity on the full core), and per gate 8 no such language may be attached to it. Its genuine value is engineering: the pipeline — exact formulas → certified balls → moment compression → sign determination at the 10⁻¹⁷ scale — is now proven end-to-end and extends mechanically to larger N.

## Next computational steps (within this packet's authority)
1. Extend to Q_N for N = 4…12 (entries are pairwise; cost is O(N²) certified entries + exact compression); report certified eigenvalue-sign profiles of M_N via interval Cholesky/Gershgorin.
2. Exercise the generalized Schur extension criterion on the first genuinely 2×2 step (Q₄).
3. Profile how the certified radius scales with N to fix precision policy before larger runs.
The form-core theorem (P0-WEIL-CORE) remains the sole route by which any of this could ever acquire RH relevance.

---

# MIG-025 Addendum — Hardened Certificates, Certified Q₄ Schur Step, Certified Ladder to Q₁₂

## A. Certificate hardening (the float-serialization defect, fixed rigorously)
The MIG-024 JSON stored `float(mid)`/`float(rad)`: the double-rounded midpoint sat ~3.4×10⁻³³ from the true center while the stored radius was 6.3×10⁻⁶³ — the JSON interval **did not contain the certified value** (the review's catch). Certificates now serialize via **exact dyadic extraction**: `arb.man_exp()` yields exact (mantissa, exponent) for midpoint and radius → exact `Fraction` endpoints L = mid−rad, U = mid+rad → decimal strings with **directed rounding** (lower: ROUND_FLOOR; upper and radius: ROUND_CEILING). The float value is retained under `diagnostic_float`, explicitly non-certifying. Every certificate carries full provenance: precision bits, N, M, Python/python-flint versions (FLINT/Arb versions are not exposed by python-flint 0.8 — recorded as bundled-with-wheel), script SHA-256, git commit, scale set, exact basis, the prime-tail bound formula, and the archimedean method. `scripts/validate.py` check 8 now parses the decimal endpoints of every certificate and fails unless 0 < lower ≤ upper for every positivity claim. The hardened M₃ endpoints (width ~1.3×10⁻⁶⁰) contain the review's 100-digit value.

## B. Certified Q₄ (first Schur extension) — all diagnostic targets matched
Basis b₃ = (−1,4,−3,0), b₄ = (−2,6,0,−4) (moment identities asserted exactly at runtime). Certified results (balls):
M�� = [[5.0834527285304509374e−17, 1.6774809068366707783e−16],[·, 5.8495137548902276628e−16]]; LDL pivots M₃ and **Schur complement [3.140197844072025462229732×10⁻¹⁷ ± 1.1×10⁻⁴²]**; eigenvalue enclosures **[2.520752530345813039×10⁻¹⁸ ± 2.4×10⁻⁴³]** and **[6.332651502439814626×10⁻¹⁶ ± 1.3×10⁻⁴¹]** — every value matching the review's diagnostics to all stated digits, both eigenvalues rigorously positive. The zero-side matrix diagnostic, with the **corrected off-diagonal convention 2·Re(a_iā_j)** over positive ordinates, reproduces the certified matrix to 15 digits (diagnostic only).

## C. A second precision defect found and fixed by the escalation policy itself
The first Q₉ attempt returned an indeterminate 7th pivot, and escalation initially made radii **worse** (pivot-6 radius 4.7×10⁻³⁹ → 7.1×10⁻³⁰). Instrumentation isolated the cause: **S_m carries an *absolute* ball-radius floor ~2^(−prec)** (it is a difference of O(2^(−m))-scale quantities), and the downstream factor (r/q)^m — up to 12^m — amplifies that floor catastrophically as M grows (at m = 111 a single term contributed 1.1×10⁻¹⁴ of radius). Fix: the S-table is computed once per profile at **elevated internal precision** prec_S = base + ⌈M·log₂(max r/q)⌉ + 64, then the context is restored; term arithmetic stays at base precision (midpoints are small). This is exactly the kind of failure the review's auto-escalation directive was designed to surface, and it is now documented in the engine itself.

## D. Certified ladder Q₃ → Q₁₂: all positive-definite
With the fix, the escalation ladder certifies **every truncation**: Q₃–Q₈ at profile (350 bits, N=64, M=48); Q₉–Q₁₂ at profile (450 bits, N=192, M=112). Full certified pivot sequence at Q₁₂ (10 pivots, Sylvester ⟹ all eigenvalues of every M_N rigorously positive):

| k | pivot (certified ball) |
|---|---|
| 1 | 5.08345272853×10⁻¹⁷ |
| 2 | 3.14019784407×10⁻¹⁷ |
| 3 | 4.90702749193×10⁻²⁵ |
| 4 | 8.91994112684×10⁻²⁶ |
| 5 | 1.13226803457×10⁻³¹ |
| 6 | 9.00002691081×10⁻³¹ |
| 7 | 1.43254395580×10⁻³⁷ ± 2.8×10⁻⁴⁹ |
| 8 | 2.47512632682×10⁻³⁸ ± 8×10⁻⁵⁴ |
| 9 | 6.23133164444×10⁻⁴¹ ± 1.7×10⁻⁵³ |
| 10 | 2.21402513702×10⁻⁴² ± 1.6×10⁻⁵⁴ |

The pivot decay (25 orders of magnitude over 10 pivots) matches the expected spectral structure: the compressed matrix is a rapidly-weighted sum of rank-2 contributions per zero ordinate (weights ~2πγe^(−πγ)), so each new pivot pair descends to the next zero's scale — Q₁₂'s smallest pivots live at the γ₅/γ₆ weight scale. This quantifies the conditioning wall: each +2 dimensions costs ~7–9 more digits of certified entry precision, a scaling law now measured, not guessed.

**Classification (standing, gate 8):** all of the above are restricted finite Weil tests (K0-W1 §7). Positivity of M₃…M₁₂ says the Weil form is rigorously positive on specific finite moment-constrained slices; it carries no RH content absent P0-WEIL-CORE, and none may be described otherwise.
