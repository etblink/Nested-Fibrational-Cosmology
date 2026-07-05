# Research Packet — K0-W3: Certified Rational-Height Weil Evaluator

**Class:** scaffold; **not canon**. Implements the certified evaluator for the rational-height matrices M_H of the exact reformulation RH ⟺ (M_H ⪰ 0 for every H) established in P0-WEIL-CORE. Engine: `scripts/weil_engine.py` command `qh <H>`. Certificates: `metadata/weil_QH<H>_certificate.json`.

**Standing classification:** finite M_H positivity is a **restricted finite test**, never an RH theorem-step (P0-WEIL-CORE prohibition 18). The certified track uses no zero-location input.

---

## The eight implementation requirements (all satisfied)

1. **Exact rational conversion.** `_arb_from_fraction(fr) = arb(num)/arb(den)`; no `Fraction`-through-float path. sympy uses `Rational(num,den)`.
2. **Dynamic scale-ratio precision.** `MAX_SCALE_RATIO` is derived from the actual scale set as ⌈max/min⌉+1 = ⌈H²⌉+1 for Q_H (was hard-coded 12); this feeds the elevated S-table precision base+⌈M·log₂(ratio)⌉+64.
3. **Exact rational archimedean algebra.** `J_integrand_coeffs_rational` clears denominators over ℚ[u], cancels the removable u=1 singularity symbolically, and normalizes num/den by a **single common** lcm and gcd (preserving the rational-function value — see the bug note below).
4. **Primitive integer nullspace basis.** anchors q₁=1, q₂=2 fixed; b_k supported on (0,1,k); denominators cleared, divided by integer gcd, serialized as exact integer vectors; both moment identities asserted exactly at construction.
5. **Persistent nested ordering.** scales ordered as [anchors 1,2] then by (reduced height h(m/n)=max(m,n), value); V_H embeds canonically into V_{H+1}. (Q₂ = [1,2,½]; Q₃ = [1,2,½,⅓,⅔,3/2,3] — Q₂ is the prefix.)
6. **Certificate coverage.** every scale as [num,den]; exact integer basis vectors; profile (bits,N,M,max_scale_ratio); dyadic balls + decimal endpoints per pivot; LDL status; ordering rule string; full provenance.
7. **Validator extension.** `validate.py` check 8 now reconstructs each Q_H rational set, verifies reduction (gcd=1) and uniqueness, verifies **both** moment identities Σc=0 and Σc/q=0 exactly for every basis vector, and requires every PD pivot to have a strictly positive certified lower endpoint. Adversarially confirmed: breaking a moment identity is rejected.
8. **Classification** language retained verbatim in engine output and certificates.

## A real bug, found and fixed by the diagnostic targets

The first rational run gave M₂ = 2.32×10⁰, wildly off the reviewer's diagnostic target 2.9247568774451138314×10⁻¹⁶. Rather than accept it, component comparison against the verified integer engine localized the fault to the archimedean term: the rational coefficient normalizer divided numerator and denominator by **independent** gcds, corrupting the rational-function ratio (num scaled by 2, den by 9 → integrand off by 2/9). Fixed by normalizing both by a single common factor. After the fix:

> **M₂ ∈ [2.92475687744511383141046e-16, 2.92475687744511383141047e-16]** (certified enclosing interval, generated from certificate endpoints with **directed rounding** — lower endpoint ROUND_FLOOR, upper endpoint ROUND_CEILING — per MIG-033; the exact radius is ~1.31×10⁻⁵⁶). This matches the reviewer's zero-side diagnostic 2.924756877445113831410464909826×10⁻¹⁶ to all stated digits. Display-correction history: an earlier hand-written ±9.0×10⁻⁴² prose interval was **non-enclosing** (MIG-032); MIG-032's machine display then used round-to-nearest formatting and was **also non-enclosing** (its lower endpoint sat ~9.02×10⁻⁴² above the certified lower endpoint); MIG-033 fixes the display with directed rounding, a mandatory enclosure self-check in `display_interval_from_cert`, and validator check 8b proving every prose interval encloses its certified ball.

This is exactly why diagnostic targets accompany each authorized step: a 16-order error was caught before it entered a certificate.

## Certified results

**H = 2.** Q₂ = [1, 2, ½] (max/min = 4 = H²); primitive basis (3, −2, −1) (matches reviewer); compressed dimension 1.
> M₂ ∈ [2.92475687744511383141046e-16, 2.92475687744511383141047e-16], **PD** (enclosing interval from certificate endpoints, directed rounding per MIG-033).

**H = 3.** Q₃ = [1, 2, ½, ⅓, ⅔, 3/2, 3] (7 scales, max/min = 9 = H²); 5 primitive basis vectors; compressed dimension 5; profile 350 bits / N=64 / M=48 (MAX_SCALE_RATIO=10).
> M₃ certified **PD** — the certification is the 5 rigorous LDL pivots (all strictly positive lower endpoints), NOT the eigenvalues. The individual **eigenvalues below are DIAGNOSTIC ONLY** (midpoint estimates, not certified enclosures): 4.395×10⁻³², 7.736×10⁻²⁷, 8.340×10⁻²⁶, 2.839×10⁻¹⁷, 1.219×10⁻¹⁵ — matching the reviewer's independent 50-ordinate diagnostics (4.3952…×10⁻³², 7.7364…×10⁻²⁷, 8.3399…×10⁻²⁶, 2.8395…×10⁻¹⁷, 1.2190…×10⁻¹⁵). (An earlier draft printed the smallest as 4.34×10⁻³², an over-rounded/unstable estimate; the stable value is 4.395×10⁻³².) The smallest eigenvalue confirms H=3 already needs substantially more precision than the H=2 scalar test. Rigorous eigenvalue enclosures require serialized compressed matrix-entry balls (deferred to the next step, MIG-032 req 7); until then PD rests on LDL pivots alone.

## Relation to the integer ladder and next steps
Q_H exhausts ℚ₊ (the integer sequence did not), so the M_H are the matrices of the exact reformulation. The certified integer results Q₃–Q₁₂ (K0-W2) are valid slices of the corresponding integer-scale subsystem. Natural next computational steps within this packet's authority: H=4,5 with the escalation profile ladder (the smallest eigenvalue's ~H⁻ᵏ decay sets the precision schedule); a certified eigenvalue-enclosure routine for M_H (rather than diagnostic midpoint eigenvalues). The two program-level tracks remain the certified Q_H computation and **independent specialist review** of the cyclicity and continuity arguments before any external claim.

---

# MIG-032 Addendum — Validator Hardening + Interval/Eigenvalue Corrections

Three scaffold defects from the MIG-031 review, all reproduced and fixed:

1. **Validator did not reconstruct Q_H** (a counterfeit H=3 certificate carrying H=2 data under the H:3 name passed). The validator now computes the deterministic expected ordered Q_height(H) and requires exact equality; additionally checks dim = |Q_H|−2, basis vector count/length, exact rank (over 𝔽_p) equal to the nullspace dimension (so the basis **spans** the full two-moment nullspace, not merely lies in it), recorded max/min ratio agreement, and filename-height ↔ JSON-H ↔ scale-set consistency. The counterfeit substitution is now **rejected** and is a permanent adversarial test.
2. **Hand-rounded prose intervals were non-enclosing.** The displayed M₂ center 2.924…465×10⁻¹⁶ differs from the exact midpoint by ~9.02×10⁻⁴², so the hand-written ±9.0×10⁻⁴² did not contain the certified value (exact radius ~1.31×10⁻⁵⁶). MIG-032's repair generated displays from certificate endpoints but formatted them with **round-to-nearest**, which is not directionally safe: the H=2 displayed lower endpoint rounded UP past the certified lower endpoint by the same ~9.02×10⁻⁴², so the MIG-032 display was **still non-enclosing** (found in independent verification). MIG-033 completes the repair: `display_interval_from_cert` now applies ROUND_FLOOR to the lower endpoint and ROUND_CEILING to the upper, refuses (raises) if the formatted interval fails an exact-arithmetic enclosure check against the dyadic ball, and validator check 8b independently proves (i) the canonical directed display of every certified ball encloses its exact dyadic ball and (ii) every interval printed in prose reports encloses the certified ball it displays. The machine certificate was always valid; only the presentation layer was wrong, twice.
3. **H=3 "certified-matrix eigenvalues" was ambiguous** — PD is certified by the LDL pivots, but the individual eigenvalues are diagnostic midpoints. Relabeled **DIAGNOSTIC ONLY** in both packet and certificate; the smallest value is corrected from an unstable 4.34×10⁻³² to the stable **4.395240991×10⁻³²** (verified at 600-bit entry precision / 60 dps, matching the reviewer's 50-ordinate 4.3952409913…×10⁻³² to 10 digits). Rigorous eigenvalue enclosures require serialized compressed matrix-entry balls, deferred to the H=4/H=5 step; until then PD rests on LDL pivots alone.

**Permanent adversarial suite** (`scripts/adversarial_test.sh`, wired into `make check`): counterfeit H=3, broken moment identity, nonpositive PD pivot endpoint, reordered scales, tampered dim — all five must be (and are) rejected.

With this hardening, H=4 and H=5 are the correct next computational targets, with rigorous eigenvalue-enclosure serialization added at that step. Independent specialist review of the continuity and cyclicity arguments remains the parallel mathematical track.

---

# MIG-035 Addendum — H=4 and H=5 Certified Rational-Height Matrices

The H=4/H=5 step promised above is now complete. Both certificates
(`metadata/weil_QH4_certificate.json`, `metadata/weil_QH5_certificate.json`) were
generated by `run_rational_height_certified` and are independently re-checked by
`scripts/validate.py`.

**What is certified.** For each height H ∈ {4,5}: the deterministic ordered scale set
Q_H is reconstructed and its nesting against Q_{H−1} is verified (Q_{H−1} is the exact
ordered prefix of Q_H, so the primitive basis embeds canonically); the exact primitive
integer nullspace basis is serialized and every vector is verified to satisfy both moment
equations Σⱼ cⱼ = 0 and Σⱼ cⱼ/qⱼ = 0 exactly; the complete compressed Hermitian
(real-symmetric) matrix M_H is serialized as exact dyadic entry balls; positive-definiteness
is certified through interval LDLᵀ with every pivot carrying a strictly positive lower
endpoint; and rigorous eigenvalue enclosures are produced.

**Eigenvalue method (explicit, machine-checkable).** The near-singular H≥5 spectrum is not
isolable as an interval matrix, so eigenvalues use the midpoint-plus-Weyl construction:
A = A₀ + E with A₀ the exact dyadic midpoint matrix and |Eⱼₖ| ≤ Rⱼₖ the serialized ball
radii; ‖A − A₀‖₂ ≤ ‖R‖∞ (max absolute row sum, valid for Hermitian E); the point matrix A₀
isolates cleanly under Arb's Rump-verified eigensolver, and each sorted enclosure is widened
outward by ‖R‖∞ (Weyl). Because ‖R‖∞ (≈10⁻¹⁰³ at H=4, ≈10⁻⁹⁶ at H=5) is dozens of orders
below the smallest eigenvalue (λ_min ≈ 8.4×10⁻⁴³ at H=4, ≈ 6.5×10⁻⁶⁴ at H=5), the widening
preserves strict positivity of every enclosure. The validator independently re-derives ‖R‖∞
from the serialized radii, confirms the recorded bound is valid, and confirms trace = Σλ,
det = Πpivots = Πλ, Hermitian pairing Mⱼₖ = M_kⱼ, nondecreasing eigenvalue order, dim = |Q_H|−2,
and LDL/eigenvalue inertia agreement (both report all-positive).

Dimensions and profiles: M₄ is 9×9, M₅ is 17×17; both certified at the (500-bit, N=192, M=112)
escalation profile. Four permanent adversarial tests are added and all rejected: a broken
off-diagonal Hermitian pair, an eigenvalue lower endpoint pushed below zero under an
all-positive claim, a matrix-entry ball narrowed below its exact dyadic, and a basis vector
that is no longer a moment nullvector.

**Classification (unchanged and load-bearing).** H=4 and H=5 are rigorously positive
restricted rational-height Weil tests. They are finite consistency results inside an exact
infinite reformulation, **not** theorem-steps toward RH. Independent specialist review of the
continuity and cyclicity arguments remains the separate mathematical track before any external
claim.

---

# MIG-036 Note — Self-Verifying Eigenvalue and PD Certificates

An independent review of MIG-035 found that the eigenvalue certificate, while numerically
correct, was not *independently* machine-verifiable: the validator bound the spectrum to the
matrix only through positivity, trace overlap, determinant-product overlap, and Weyl width.
Those are necessary but not sufficient — a counterfeit that alters three eigenvalues while
preserving their sum and product passed validation.

MIG-036 closes this. The eigenvalue certificate now carries, for each eigenvalue, a dyadic
witness vector v and a dyadic bound ρ. The validator reconstructs the exact dyadic midpoint
matrix A₀ from the serialized entries and recomputes, in exact rational arithmetic,
θ = vᵀA₀v / vᵀv and the residual, verifying ‖A₀v − θv‖₂ ≤ ρ‖v‖₂. The Hermitian residual
theorem then places an eigenvalue of A₀ in [θ − ρ, θ + ρ]; the n intervals are proved
pairwise disjoint and ordered by exact rational comparison, so they exhaust the n-point
spectrum, and each is widened by the recomputed ‖R‖∞ to enclose the true spectrum. This
residual certificate is now the **primary** positive-definiteness proof (the LDL pivots are
retained as a redundant generator cross-check). The sum/product-preserving counterfeit is a
permanent adversarial test and is rejected because its intervals do not contain the
residual-certified eigenvalues of A₀. Eigenvalue ordering no longer uses floating point
(exact rational comparison of pᵢ/sᵢ), and the adversarial runner now distinguishes a genuine
validation rejection from an environment crash. The H=4/H=5 numerical values are unchanged.
