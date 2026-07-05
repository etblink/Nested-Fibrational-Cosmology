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

---

# MIG-038 Addendum — H=6 Certified Rational-Height Weil Test

The H=6 certificate (`metadata/weil_QH6_certificate.json`) is complete under the hardened
MIG-036/MIG-037 residual-certificate format. Q₆ contains exactly 23 ordered reduced rational
scales with Q₅ verified as its exact ordered prefix; the compressed two-moment nullspace has
dimension 21 (exact rational rank 21, every basis vector verified against both moment
identities exactly); the full 21×21 Hermitian dyadic-ball matrix is serialized with
nonnegative radii and exact Hermitian pairing. The base profile (350 bits, N=64, M=48) was
INDETERMINATE; the certificate was produced at the existing escalation profile (500 bits,
N=192, M=112) — no engine change was required. Twenty-one residual witnesses (each 21 dyadic
coordinates) yield exact-rationally recomputable Rayleigh centers and residual inequalities;
the 21 residual intervals are pairwise disjoint and strictly ordered, exhausting the midpoint
spectrum, and each is widened outward by the independently recomputed nonnegative ‖R‖∞. Every
widened interval has a strictly positive lower endpoint (λ_min lower bound
≈ 7.53×10⁻⁷⁰), the serialized enclosures outward-contain the widened intervals, the interval-LDL
pivots are retained only as a redundant cross-check, and the inertia record is consistently
21-positive. A permanent H=6 payload-binding adversarial test (tamper 15) is added.

**Classification (unchanged, load-bearing).** H=6 is one additional finite restricted
rational-height Weil test. It is not an RH theorem-step, does not establish progress from
finitely many positive matrices toward the universal positivity statement, and licenses no
SCC/RH status promotion. No zero-location data enters the certified generation path, and this
result remains procedurally and logically separate from the independent Weil-core /
SCC specialist-review track.


---

# MIG-039 → MIG-040 — H=7 Certified After the Active-Precision Boundary-Constant Repair

MIG-039 delivered H=7 as a numerical-certification obstruction: the constants EULER and
LOG4PI were evaluated once at module import (350-bit default), freezing a ≈4.4×10⁻¹⁰⁷ radius
into every matrix entry through the boundary term (log 4π + γ)/(q+r)², a floor invariant under
all precision profiles. MIG-040 removes that floor with a narrowly targeted engine repair — no
mathematical change: the boundary constant is now evaluated at the active profile precision
(`boundary_constant()`, cached by exact precision, built once per profile, with no fallback to
the frozen constants). The term remains exactly (log 4π + γ)/(q+r)².

Constant-radius diagnostics confirm the floor is gone — the boundary radius now contracts with
precision instead of staying fixed: ≈2.0×10⁻¹⁰⁶ at 350 bits, ≈1.4×10⁻¹⁵¹ at 500, ≈8.7×10⁻²¹²
at 700, ≈5.4×10⁻²⁷² at 900 (previously identical ≈4.4×10⁻¹⁰⁷ at 900 and 1600).

The H=7 ladder was rerun from the base rung: (350, 64, 48) LDL INDETERMINATE; (500, 192, 112)
LDL INDETERMINATE; **(700, 384, 160) certified** — 33×33 matrix LDL positive-definite, all 33
eigenvalues residual-certified, pairwise disjoint, Weyl-widened, strictly positive, with

    λ_min ≥ 4.101947712306630724476060955915436794880175738319424571 × 10⁻⁹².

All 23 required certificate properties hold, including exact rational rank 33, exact Q₆ prefix
nesting, the full 1,089-ball Hermitian grid, and provenance recording the boundary-constant
mode as active-profile. A permanent H=7 matrix-to-residual binding adversarial test (tamper 16)
is added and rejected downstream from the residual certificate.

**Classification (unchanged, load-bearing).** H=7 is one additional finite restricted
rational-height Weil test. It is not an RH theorem-step, provides no logical or probabilistic
promotion toward universal Weil positivity, and licenses no RH/SCC/canonical-status change. The
flint-free validator verifies the serialized matrix and proof objects; the analytic production
link remains generation provenance. Certified heights are now H = 2, 3, 4, 5, 6, 7. H=8+ remains
unauthorized. The independent Weil-core / SCC specialist review continues in parallel, logically
separate.


---

# MIG-041 → MIG-042 — H=8: Applicability Guard Added; Residual-Isolation Obstruction Remains

MIG-041 delivered H=8 as a profile-applicability obstruction: the base profile (350, 64, 48)
is structurally inapplicable because its prime-head N=64 does not exceed the maximum ordered
scale ratio 64 (the geometric-tail precondition N > r/q). MIG-042 adds the authorized exact
structural-applicability guard: before matrix construction, `run_rational_height_certified`
computes max_ratio = max(Q_H)/min(Q_H) as an exact `Fraction` and records any profile with
N ≤ max_ratio as STRUCTURALLY INAPPLICABLE, skipping it (the backstop assertion inside
`T_certified_rational` is retained; no broad exception-catching; no hardcoded 64 or H²). Guard
regressions verified: H=7 @ (350,64,48) applicable (64 > 49); H=8 @ (350,64,48) inapplicable
(64 ≤ 64); H=8 @ (500,192,112) applicable (192 > 64); predicate derived from the actual scale
set; QH2–QH7 unchanged.

With the guard, the H=8 ladder now reaches the applicable profiles. Complete profile history:

    (350,  64, 48)  STRUCTURALLY INAPPLICABLE (N=64 ≤ max_ratio 64; skipped, no matrix built)
    (500, 192,112)  LDL INDETERMINATE
    (700, 384,160)  LDL PD, residual-certificate isolation FAILED (no disjoint ordered intervals)
    (900, 512,224)  LDL PD, residual-certificate isolation FAILED
    (1200,768,320)  LDL PD, residual-certificate isolation FAILED
    (1600,1024,448) LDL PD, residual-certificate isolation FAILED

**H=8 is NOT certified.** The obstruction is new and distinct from both MIG-039 (radius floor)
and MIG-041 (applicability). At profiles 3–6 the interval LDL certifies positive-definiteness
rigorously (every pivot has a positive lower endpoint), so the compressed matrix is very likely
PD; but the *required primary proof object* — the exact-rational residual certificate — cannot
isolate the dense 41-dimensional midpoint spectrum into 41 pairwise-disjoint ordered intervals,
even with eigenvector working precision escalated to 32,000 bits (base 1600 × mult 20). As the
dimension grows the eigenvalues cluster, and the residual method needs each interval half-width
ρᵢ below half the local spectral gap; for at least one near-degenerate pair the achievable ρᵢ at
the authorized precisions exceeds the gap.

This is a residual-isolation obstruction, **not** a positivity failure in either direction: the
rigorous interval-LDL result points to PD, and nothing contradicts it. Per the MIG-042 failure
condition it is delivered as an obstruction, not converted into positivity by LDL alone,
heuristic eigenvalues, floating-point ordering, or widened tolerances.

**Diagnostic recommended before the next authorization.** Measure the minimum midpoint spectral
gap of the H=8 compressed matrix. If the gap is nonzero but small (isolable at higher precision),
the resolution is an authorized profile-only extension (higher monotone bits) that raises the
eigenvector precision past the gap. If the gap reflects genuine near-degeneracy at dim 41, the
resolution is an algorithmic enhancement to the residual certificate (a cluster-aware /
Kato–Temple subspace enclosure that certifies a tight *interval containing k eigenvalues*
without isolating them individually) — which is beyond the profile-only and guard permissions and
would require its own authorization. Determining which was not attempted here, as it needs either
a profile extension or an algorithmic change, both outside MIG-042's authorized scope.

**Classification (unchanged, load-bearing).** No H=8 result exists in either direction. Certified
heights remain exactly H = 2, 3, 4, 5, 6, 7 — finite restricted rational-height Weil tests, not
RH theorem-steps, no RH/SCC/canonical-status implication. Permanent tamper 17 (H=8
matrix-to-residual binding) is deferred until an H=8 certificate exists. H=9+ remains unauthorized.
