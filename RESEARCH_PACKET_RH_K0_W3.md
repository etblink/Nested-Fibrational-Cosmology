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

> **M₂ = [2.924756877445113831410465×10⁻¹⁶ ± 9.0×10⁻⁴²] — certified, matching the reviewer's zero-side diagnostic to every stated digit.**

This is exactly why diagnostic targets accompany each authorized step: a 16-order error was caught before it entered a certificate.

## Certified results

**H = 2.** Q₂ = [1, 2, ½] (max/min = 4 = H²); primitive basis (3, −2, −1) (matches reviewer); compressed dimension 1.
> M₂ = [2.92475687744511383×10⁻¹⁶ ± 1.4×10⁻³⁴], **PD**.

**H = 3.** Q₃ = [1, 2, ½, ⅓, ⅔, 3/2, 3] (7 scales, max/min = 9 = H²); 5 primitive basis vectors; compressed dimension 5; profile 350 bits / N=64 / M=48 (MAX_SCALE_RATIO=10).
> M₃ certified **PD** (all 5 LDL pivots strictly positive). Certified-matrix eigenvalues:
> 4.34×10⁻³², 7.74×10⁻²⁷, 8.34×10⁻²⁶, 2.84×10⁻¹⁷, 1.22×10⁻¹⁵ — matching the reviewer's 30-zero diagnostic targets (4.40×10⁻³², 7.74×10⁻²⁷, 8.34×10⁻²⁶, 2.84×10⁻¹⁷, 1.22×10⁻¹⁵) to their stated precision; the smallest eigenvalue confirms H=3 already needs substantially more precision than the H=2 scalar test, as the reviewer anticipated.

## Relation to the integer ladder and next steps
Q_H exhausts ℚ₊ (the integer sequence did not), so the M_H are the matrices of the exact reformulation. The certified integer results Q₃–Q₁₂ (K0-W2) are valid slices of the corresponding integer-scale subsystem. Natural next computational steps within this packet's authority: H=4,5 with the escalation profile ladder (the smallest eigenvalue's ~H⁻ᵏ decay sets the precision schedule); a certified eigenvalue-enclosure routine for M_H (rather than diagnostic midpoint eigenvalues). The two program-level tracks remain the certified Q_H computation and **independent specialist review** of the cyclicity and continuity arguments before any external claim.
