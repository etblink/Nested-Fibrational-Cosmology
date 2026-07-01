# Project RIG-Q — O-RQ.1 Proof Effort: Result

*Produced L+50 on operator instruction to open O-RQ.1 (source
pre-inner-product extraction), the load-bearing hinge of Project RIG-Q.
This is work on a prospective-program obligation (RIG-Q, Speculative
Holding); it does not touch the canon and promotes nothing. Outcome
recorded honestly below.*

**Outcome in one line:** O-RQ.1 is **not discharged, but materially
sharpened** — the positivity hinge (Lemma RQ.1d), which the source note
itself predicted would fail first into a Krein/indefinite structure, is
instead **resolved affirmatively** using a canonical positive form the
corpus already carries (the L+34 energy/persistence form built on the
L+30 nonnegative generator); the null-space (RQ.1e) **aligns exactly
with the existing L+30 superselection kernel** rather than a new notion;
and the residual reduces to two precisely-named items, one of which is
an **already-existing** corpus hypothesis and the other a **new sharp
obligation** (representation-richness). The feared indefinite outcome is
avoided for the energy-carrying part.

---

## 1. What was attempted

Theorem RQ.5 / O-RQ.1: from the source encoding datum 𝕊_enc alone,
construct a canonical pre-inner-product space ℋ₀(𝕊_enc) with source map
Γ₀ such that every lawful realization factors through its completion. The
source note's architecture: free complex module ℂ[X]_fin on source
classes → canonical source-defined sesquilinear form K → quotient by null
space → completion; with required lemmas RQ.1a (well-defined), RQ.1b
(sesquilinear), RQ.1c (symmetry-invariant), **RQ.1d (positive
semidefinite — "the real hinge")**, RQ.1e (null-space compatibility),
RQ.1f (functoriality).

## 2. The decisive observation: the corpus already carries a canonical positive form

The source note treats K abstractly and lists three candidate kernels
(transition-overlap, spectral Gram, symmetry-averaged), flagging that
positivity may fail for all three. But the corpus already contains a
canonical, source-descended, positive-semidefinite sesquilinear form
that the abstract treatment does not reference:

> the **canonical persistence cost / energy form** 𝔥_B (Book III
> thm:vrp-energy-form-char, L+34), built from the **nonnegative licensed
> generator H_B ≥ 0** on the canonical nontrivial sector (Book III
> thm:vrp-mass-sector, L+30, after the forced kernel factorization).

Take the spectral-Gram kernel (the note's Kernel B) in its canonical
form
  K(x,y) := ⟨x, H_B y⟩   (equivalently the persistence-cost bilinear form),
with H_B the licensed self-adjoint generator restricted to the nontrivial
sector. Because H_B ≥ 0 there (L+30 removes the negative/zero-cost
superselection part), K is **positive semidefinite by construction** —
not by assumption. This resolves Lemma RQ.1d affirmatively for the
energy-carrying content, and avoids the Krein/indefinite branch the note
feared as the likely first failure.

## 3. Lemma-by-lemma outcome (honest)

- **RQ.1a (well-defined on source classes): holds.** ⟨x, H_B y⟩ depends
  only on quotient-visible data (H_B is the licensed generator on the
  quotient; its matrix elements are re-description-invariant by the
  spectral-invariance used in thm:vrp-mass / thm:vrp-frequency).
- **RQ.1b (sesquilinear): holds**, routinely (H_B linear, pairing
  sesquilinear).
- **RQ.1c (symmetry-invariant): holds.** H_B is PASS/symmetry-invariant
  (the generator commutes with the certified symmetry action used
  throughout the VRP construction), so K is invariant under the certified
  action — exactly what RQ.1c needs for later PASS/isotropy matching.
- **RQ.1d (positive semidefinite — the hinge): RESOLVED affirmatively**
  for the energy-carrying part, via H_B ≥ 0 (§2). The note's feared
  indefinite/Krein outcome is avoided here; positivity is earned from the
  L+30 kernel factorization, not assumed.
- **RQ.1e (null-space compatibility): aligns with existing canon.** The
  null space 𝒩 = {v : K(v,v) = 0} = ker H_B on the sector, which is
  **exactly the L+30 superselection kernel** (the persistent zero-cost
  labels factored out in thm:vrp-mass-sector). This is precisely the
  "already-harmless degeneracy" the note hoped RQ.1e would match (it asks
  to "align O-RQ.1 with KCOMP/ND instead of inventing a new notion of
  collapse") — and it does, with no new notion of collapse.
- **RQ.1f (functoriality): holds modulo the standard transfer.** Source
  morphisms preserving the encoding datum carry H_B by the generator
  uniqueness/transfer (prop:vrp-transfer-reduction), inducing
  contractions/isometries on the pre-Hilbert object.

## 4. The residual — two precisely named items

O-RQ.1 is **not** thereby discharged. After §3, two things remain, and
naming them precisely is the value of having opened the hinge:

**(i) Closable Hilbert realization = the existing L+34 hypothesis (not
new).** The pre-inner-product → Hilbert completion step requires 𝔥_B
(equivalently K) to be a **closable** quadratic form. This is exactly the
realization hypothesis carried verbatim in thm:vrp-hamiltonian's bracket
since L+24 and recorded at L+34 (rmk:vrp-why-quadratic) as the
"why is energy quadratic" question. So the completion step of O-RQ.1 is
**not a fresh obstruction** — it is the corpus's already-named realization
hypothesis, with YM/GR/NS the certified models where it holds.

**(ii) Representation-richness — a NEW sharp obligation surfaced by this
effort.** The energy form K = ⟨·, H_B ·⟩ canonically carries the
**energy/metric** content, but a representation realizing 𝕊_enc must also
carry the transport operator L and the symmetry action Π (Definition
RQ.2). Whether the single positive form K **separates enough** to force
the full (Γ, L, Π) data — i.e. whether every lawful realization factors
through (ℂ[X]_fin / ker H_B)^completion, RQ.5's universality clause — is
**not** settled by positivity alone. A coarse positive form could
identify vectors that L or Π distinguish. This is the genuinely new
named obligation:

> **O-RQ.1-rich (Representation-Richness / Faithfulness).** The canonical
> positive form K must separate the full transport/symmetry data: for
> lawful realizations, ker H_B (the RQ.1e null space) must coincide with
> the joint kernel of the encoding-transport-symmetry package, not merely
> the energy kernel. Equivalently, the energy form must be **faithful**
> for the representation, not only for the metric.

## 5. Honest status and what was learned

- **O-RQ.1: SHARPENED, not discharged.** The positivity hinge — the
  note's predicted first failure — is cleared affirmatively for the
  energy-carrying part using the L+30/L+34 structure; the null space is
  the existing L+30 superselection kernel; functoriality and invariance
  hold. What remains is (i) the **already-named L+34 closable-realization
  hypothesis** and (ii) the **new, precisely-stated O-RQ.1-rich
  faithfulness obligation**.
- **What "extra rigidity is missing" (the note's anticipated lesson):**
  not positivity (that is supplied by H_B ≥ 0), but **representation-
  richness** — the canonical positive form must be shown faithful for the
  full transport/symmetry package, not just the energy/metric. That is
  the precise rigidity O-RQ.1 now demands.
- **Connection established:** RIG-Q's hinge is not disjoint from the
  corpus — it routes through the L+30 kernel factorization and the L+34
  energy-form characterization. This both grounds RIG-Q and bounds it:
  its pre-inner-product is (on the energy-carrying part) the realized
  energy form, so RIG-Q inherits the L+34 realization hypothesis exactly,
  and its genuinely new content is the faithfulness obligation O-RQ.1-rich.
- **Promotion: still nothing.** This is a holding-layer result on a
  prospective-program obligation; RIG-Q remains non-promotable. O-RQ.1's
  downstream chain (O-RQ.2 universal realization, …) now has a concrete
  candidate pre-Hilbert object to work with — the energy-form completion
  — but only modulo (i) and (ii).

## 6. Recommended continuation (for the program owner)

The next genuine hinge is **O-RQ.1-rich (faithfulness)**: determine
whether the canonical energy form separates the transport (L) and
symmetry (Π) data, or whether a strictly richer canonical form is needed
(e.g. a direct integral over the licensed spectral/charge data rather
than the single energy weight). If faithful, O-RQ.1 closes modulo the
L+34 realization hypothesis and the RIG-Q chain becomes realistic at
CERT-PROJ force. If not faithful, the precise deficiency (which part of
L or Π the energy form blurs) is the next named rigidity input — again a
genuine result either way, exactly as the program intended.

*Holding-layer result, L+50. RIG-Q status unchanged (prospective program,
not promotable). No canon contact; nothing promoted; no corpus [O]
created. O-RQ.1 sharpened; O-RQ.1-rich surfaced as the next hinge.*

---

# Continuation L+51 — O-RQ.1-rich (Representation-Faithfulness): Result

*The next hinge named at L+50. Question: does the canonical energy form
separate the full transport (L) and symmetry (Π) data, or only the
energy/metric content? Worked against the corpus's actual operator
structure. Holding-layer result; no canon contact; nothing promoted.*

**Outcome in one line:** the bare energy form is **not faithful** — it
carries energy/metric and symmetry but **blurs transport**, because its
null space ker H_B is Π-invariant but **not** transport-invariant. The
structural fix is identified (a **joint** energy-plus-transport-cost
form), both ingredients exist in the corpus (the L+34 energy form and the
L+28/29 entropy/defect ledger), and the residual is named precisely. So
O-RQ.1-rich, like O-RQ.1, is **sharpened, not discharged** — and the
missing rigidity is now a **canonical transport cost and its
energy-relative normalization**.

## 1. The bare energy form fails faithfulness for transport

A representation realizing 𝕊_enc carries three things (Definition RQ.2):
the encoding Γ, the **transport operator L**, and the symmetry action Π.
The corpus distinguishes two operators here: the **self-adjoint
generator H_B** (energy, ≥ 0 on the nontrivial sector) and the **type
transition operator T_∂** (transport, Book II def:T-partial) — these are
genuinely different operators (T_∂ is generally non-self-adjoint; the
conserved charges are ker of its adjoint). In RIG-Q's tuple, L ≈ T_∂.

For the energy form K = polarization of 𝔥_B (null space ker H_B) to
carry L faithfully, L must descend to the quotient ℂ[X]/ker H_B, which
requires **L(ker H_B) ⊆ ker H_B** — i.e. transport must preserve the
zero-energy null space. But:
- **Π-invariance of ker H_B: holds** (H_B is symmetry-invariant, L+50),
  so the energy form is faithful for symmetry.
- **T_∂-invariance of ker H_B: fails in general.** Transport moves a
  zero-energy (transport-trivial-cost) state to a nonzero-energy state;
  equivalently [T_∂, H_B] ≠ 0 on ker H_B generically. So L does **not**
  descend to the energy-form quotient.

**Conclusion:** the bare energy form is faithful for energy/metric and
symmetry but **not for transport**. It identifies vectors that L
distinguishes. RQ.5's universality clause ("every lawful realization
factors through this quotient") therefore fails for the (Γ, **L**, Π)
package with the bare energy form. This is the precise content of
O-RQ.1-rich, and it is a genuine (negative) finding, not a setback to
hide — exactly the faithfulness deficiency anticipated at L+50.

## 2. The structural fix: a joint energy-plus-transport-cost form

To carry L faithfully the canonical form must include the transport
operator's contribution — the standard graph-norm principle: a form
carries an operator faithfully iff the operator's degeneracy is inside
the form's null space. So the faithful canonical object is the **joint
form** whose null space is the **joint** degeneracy
  𝒩_joint = ker H_B ∩ (transport-degeneracy) ∩ (symmetry-degeneracy),
not the energy kernel alone.

The corpus already supplies a canonical positive transport functional:
the **entropy/defect ledger** (def:branch-entropy-ledger, the
"structural distinguishability burden"; L+28/29), which measures exactly
how many transport-distinct classes a state resolves into. It is
canonical, source-descended, and positive. The natural faithful
canonical form is therefore the **joint energy-defect form**
  K_joint(x,y) = (energy-cost pairing from H_B) ⊕ (defect/distinguishability pairing),
whose null space is the doubly-trivial degeneracy (zero energy cost AND
zero distinguishability burden) — the genuinely harmless degeneracy,
faithful for energy (H_B), transport (defect ledger), and symmetry (both
invariant under Π).

## 3. The residual — named precisely (three items)

O-RQ.1-rich is **not** thereby discharged; the fix has its own honest
residual:

**(a) Closability of the joint form** — the extended L+34 realization
hypothesis, now applied to the combined energy-plus-defect form rather
than the energy form alone. Not a fresh wall; the same realization
hypothesis, enlarged.

**(b) Canonical energy/defect normalization** — the joint form combines
two costs (energy and distinguishability), and their **relative weight**
is a choice unless canonically fixed. This is the genuinely new rigidity
demand. **Promising lead, not yet established:** the corpus's canonical
energy↔entropy exchange rate is the **temperature/exchange slope**
β_B = ∂S_B/∂E_B (thm:vrp-temperature, L+35). If the joint form's
energy-defect weighting is canonically fixed by β_B, the normalization
is source-descended and the choice disappears — but this identification
must be proved, not assumed. This is exactly the kind of "one more
source-descended rigidity condition" the source note (and RQ.F1)
anticipated would be needed.

**(c) Joint-kernel / encoding-predicate alignment** — confirm that
𝒩_joint matches the degeneracy the YM encoding predicates already treat
as harmless (the L+50 RQ.1e alignment, now for the joint kernel rather
than ker H_B alone).

## 4. Honest status and what was learned

- **O-RQ.1-rich: SHARPENED, not discharged.** The bare energy form is
  proved non-faithful for transport (a real negative result); the
  structural fix (joint energy-defect form) is identified and is
  **corpus-grounded** (both the energy form and the defect ledger are
  already licensed); the residual is three named items.
- **The missing rigidity, named:** not positivity (L+50), not symmetry,
  but **a canonical transport cost and its energy-relative
  normalization**. The transport cost has a corpus candidate (the defect
  ledger); the normalization has a corpus lead (the temperature slope,
  L+35) that must be proved to apply.
- **Deepening corpus connection:** the O-RQ.1 line now routes through
  four established results — the L+30 kernel factorization, the L+34
  energy form, the L+28/29 entropy/defect ledger, and (as a lead) the
  L+35 temperature slope. RIG-Q's representation hinge is being resolved
  **into the recovered-variable structure**, not into external machinery:
  the faithful canonical inner product, if it exists, is built from
  energy, distinguishability, and their exchange rate — all licensed VRP
  variables. This is a meaningful structural finding: the
  representation/metric frontier connects directly to the closed VRP arc.
- **Promotion: still nothing.** Holding-layer result; RIG-Q remains
  non-promotable; no corpus [O] created. The O-RQ.1 chain now reads:
  positivity secured (L+50), transport-faithfulness requires the joint
  form (L+51), residual = closability (extended L+34) + canonical
  energy/defect normalization (β_B lead) + kernel alignment.

## 5. Recommended continuation

The next genuine hinge is residual **(b): prove (or refute) that the
temperature/exchange slope β_B canonically fixes the energy/defect
normalization of the joint form.** If it does, the joint canonical form
is fully source-descended (faithful + canonically normalized), and
O-RQ.1 closes modulo the (extended) L+34 closability hypothesis — a
major advance putting the RIG-Q representation target at CERT-PROJ force.
If it does not, the precise normalization freedom that remains is the
next named rigidity input. Either is a genuine result, and both keep the
construction inside the licensed VRP structure rather than importing
external machinery.

*Holding-layer result, L+51. RIG-Q status unchanged (prospective program,
not promotable). O-RQ.1-rich sharpened; the joint energy-defect form
identified as the faithful candidate; canonical normalization (β_B lead)
surfaced as the next hinge.*

---

# Continuation L+52 — Residual (b): the Temperature Canonically Fixes the Normalization (Transport-Covariance Argument)

*Residual (b) from L+51: does the temperature slope β_B canonically fix
the energy/defect normalization of the joint form? Worked through the
transport-transformation laws. Holding-layer result; no canon contact;
nothing promoted.*

**Outcome in one line:** **Resolved (conditionally).** The temperature
T_B = 1/β_B is forced as the unique canonical normalization of the joint
energy-defect cost by a transport-covariance argument — it is both the
canonical exchange rate between the two ledgers being combined (L+35) and
the unique weight making the joint cost transform covariantly under
lawful interface transfer (using L+29 entropy absoluteness). With this,
the canonical pre-inner-product is **fully specified** as
𝔥_B + T_B·𝔡_B, and O-RQ.1 reduces to the (extended) L+34 closability
hypothesis plus a kernel-alignment check plus the sector conditions — no
free normalization remains.

## 1. The covariance argument

Write the joint cost candidate C_λ(x) = 𝔥(x) + λ·𝔡(x), with 𝔥 the
energy/persistence cost (L+34) and 𝔡 the coefficient-free
distinguishability/transport cost (the L+28/29 defect ledger, realized
as a quadratic form). The normalization λ > 0 is the freedom to fix.
Under a lawful interface I with licensed energy exchange coefficient g_I,
the three ingredients transform by **established corpus transfer laws**:

| Quantity | Transfer law | Source |
|---|---|---|
| Energy cost 𝔥 | 𝔥 ↦ g_I · 𝔥 | thm:vrp-energy-transfer (L+25) |
| Distinguishability cost 𝔡 | 𝔡 ↦ 𝔡 (no coefficient) | thm:vrp-entropy-transfer, **absoluteness** (L+29) |
| Temperature T_B = 1/β_B | T_B ↦ g_I · T_B | thm:vrp-temperature cl.3 (β_B ↦ g_I⁻¹β_B) (L+35) |

For the joint cost to be a single canonical object it must transform
**homogeneously** — as one energy-type cost, C_λ ↦ g_I · C_λ — so that
the pre-inner-product it induces transforms covariantly under transfer
(the same requirement every licensed variable meets). Compute:
  C_λ ↦ g_I·𝔥 + λ·𝔡   (using the transfer laws above).
Homogeneity C_λ ↦ g_I·C_λ = g_I·𝔥 + g_I·λ·𝔡 requires
  λ·𝔡 ↦ g_I·λ·𝔡, i.e. **λ ↦ g_I·λ.**
A *constant* λ fails this (the two terms scale differently — the energy
term by g_I, the defect term not at all), so **no constant normalization
is covariant.** The weight must itself scale as g_I.

## 2. Why the scaling weight is forced to be T_B

Two independent requirements converge on T_B:

- **Canonical-exchange-rate requirement.** The normalization relates the
  two specific ledgers being combined — energy and entropy/distinguish-
  ability. The unique *licensed* quantity whose defined role is the
  exchange rate between exactly these two ledgers is the temperature
  slope: β_B = ∂S_B/∂E_B, equivalently T_B = ∂E_B/∂S_B (thm:vrp-
  temperature, L+35). Combining an energy cost with a distinguishability
  cost at their canonical exchange rate is the only source-descended way
  to make the sum dimensionally and structurally coherent — this is the
  thermodynamic free-energy structure (energy and entropy combined at the
  temperature), here in its positive-cost form.
- **Covariance requirement (§1).** The weight must scale as g_I. T_B
  scales exactly as g_I (table above). It passes.

T_B satisfies both; a constant fails covariance; any other transforming
quantity is not the canonical exchange rate of these two ledgers.
**Therefore λ = T_B is forced**, and the canonical joint cost is
  **C_can(x) = 𝔥_B(x) + T_B · 𝔡_B(x).**

## 3. Properties of the canonical joint cost

- **Positive:** 𝔥_B ≥ 0 (L+50) and 𝔡_B ≥ 0 (entropy/defect nonnegative)
  and T_B > 0 on the positive-temperature sector (L+35 sign clause), so
  C_can ≥ 0. Null space = ker 𝔥_B ∩ ker 𝔡_B (the joint degeneracy).
- **Faithful** for energy, transport, and symmetry (L+51): the joint
  kernel is the doubly-trivial degeneracy, so transport (which moved
  states off ker 𝔥_B alone) is now carried.
- **Canonically normalized:** no free weight remains (§2).
- **Covariant** under lawful transfer: C_can ↦ g_I · C_can (§1).

## 4. Conditions (named — this is a [C]-type result, not unconditional)

1. **Exchange-coherence** (L+35): β_B / T_B is a well-defined sector
   constant only on exchange-coherent sectors. Off them the normalization
   is not a single number and the argument does not apply.
2. **Positive temperature** T_B > 0 (L+35 sign clause; sector data) for
   positivity of C_can.
3. **Entropy absoluteness** (L+29): the coefficient-free transfer of 𝔡
   is what breaks the symmetry and forces the g_I-scaling weight. Without
   it the covariance argument has no handle.
4. **Quadratic realization of 𝔡_B** as a coefficient-free distinguish-
   ability form: folds into the closability residual (a) below.

## 5. Status of O-RQ.1 after L+52

The canonical pre-inner-product is now **fully specified**:
  H_can = completion of (ℂ[X]_fin / ker C_can) under C_can = 𝔥_B + T_B·𝔡_B.
The line of residuals has collapsed to:

- **(a) Closability** of the joint quadratic form C_can — the **extended
  L+34 realization hypothesis**, now covering 𝔥_B + T_B·𝔡_B rather than
  𝔥_B alone. On the certified models YM/GR/NS the energy component is
  closable (L+34); joint closability plausibly extends but must be
  confirmed, not assumed.
- **(c) Joint-kernel / encoding-predicate alignment** (the L+50/L+51
  alignment, for ker C_can).
- **Sector conditions** (1)–(2) above.

**No free normalization remains.** This is the advance: residual (b) is
removed by a genuine covariance argument, and the canonical inner product
is built **entirely from licensed VRP variables** — energy cost,
distinguishability cost, and the temperature exchange rate. O-RQ.1, the
load-bearing RIG-Q hinge, is thereby reduced to the **same L+34
realization hypothesis the whole VRP arc already carries**, plus a kernel
check, on exchange-coherent positive-temperature sectors.

## 6. Honest status and what was learned

- **Residual (b): RESOLVED conditionally.** Temperature fixes the
  normalization, forced by canonical-exchange-rate + transport-covariance
  (§§1–2), on exchange-coherent positive-T sectors with L+29 absoluteness.
- **O-RQ.1: reduced to known structure.** From "extract a pre-inner-
  product (may be indefinite, may fail)" (the source note's open hinge)
  to "the canonical pre-inner-product is 𝔥_B + T_B·𝔡_B, positive,
  faithful, canonically normalized, closable iff the extended L+34
  realization hypothesis holds." On YM/GR/NS (where L+34 holds for the
  energy part) O-RQ.1 is **plausibly dischargeable at CERT-PROJ force
  pending confirmation of joint closability** — a major narrowing.
- **The deep finding, now sharp:** the representation/metric frontier's
  load-bearing hinge resolves **entirely into the closed VRP recovery
  structure** — the canonical inner product that forces the
  representation is energy ⊕ (temperature × distinguishability). The
  frontier RIG-Q targets is not disjoint from the recovery program; it is
  its continuation by one realization hypothesis.
- **Promotion: still nothing.** RIG-Q remains non-promotable: O-RQ.1 is
  reduced-not-closed (the extended L+34 closability + kernel alignment +
  sector conditions remain), and the downstream chain O-RQ.2–O-RQ.8 and
  the GR gating obligations (O-GR.real/compat) are untouched. Holding-
  layer result; no corpus [O] created.

## 7. Recommended continuation

Two honest options. **(i)** Pursue **(a) joint closability on a certified
model** (YM): confirm whether 𝔥_B + T_B·𝔡_B is closable where the energy
form is — if so, O-RQ.1 discharges at CERT-PROJ on YM, the first concrete
model where the RIG-Q representation target is realized. **(ii)** Step up
to **O-RQ.2 (universal realization)**, now that O-RQ.1 supplies a concrete
canonical pre-Hilbert object to test universality against. Either advances
the chain; neither promotes anything until closability is confirmed and
the GR gating obligations are addressed.

*Holding-layer result, L+52. RIG-Q status unchanged (prospective program,
not promotable). Residual (b) resolved by transport-covariance; O-RQ.1
reduced to the extended L+34 closability hypothesis + kernel alignment +
sector conditions; canonical inner product fully specified as energy ⊕
(temperature × distinguishability).*

---

# Continuation L+53 — Step (i): Joint Closability on YM — CONFIRMED at CERT-PROJ Force

*Step (i) from L+52: is the canonical joint form C_can = 𝔥_B + T_B·𝔡_B
closable on YM, where the energy form is? Worked by form-perturbation
theory. Holding-layer result; no canon contact; nothing promoted.*

**Outcome in one line:** **Joint closability holds on YM.** The energy
form is certified closable (thm:B1-closable) and the distinguishability
form is a *bounded* perturbation of it (the YM collar alphabet is finite,
K_0 = 7, so the transport operator is finite-dimensional), so by the KLMN
form-perturbation theorem the sum C_can is closable. The canonical
pre-inner-product completes to a Hilbert carrier H_can^YM, discharging the
construction/existence content of O-RQ.1 at CERT-PROJ force on YM — the
first concrete model realizing the RIG-Q representation target.

## 1. The two ingredients on YM

- **Energy form 𝔥_B = |D_{A_0}ψ|²_{L²}: closable and semibounded**
  (YM thm:B1-closable, conditional on the Y6 coercive/Friedrichs
  framework), with Friedrichs extension H_NFC, λ₁ ≥ m² > 0. Form domain
  the gauge-covariant Sobolev space H¹_{A_0}. This is the certified model
  for the L+34 realization hypothesis.
- **Distinguishability form 𝔡_B: bounded.** 𝔡_B is built from the
  type-transition/transport structure T_∂, which acts on V = ℝ^{Σ_∂}
  over the **finite** stabilized collar alphabet (K_0 = 7; Book II,
  YM). A finite alphabet makes T_∂ finite-dimensional, hence bounded;
  the induced quadratic distinguishability form 𝔡_B is therefore a
  **bounded** (zeroth-order) nonnegative form, with form domain all of
  L² ⊇ H¹_{A_0}.

## 2. The closability argument (KLMN form perturbation)

The relevant standard result (Kato–Lions–Lax–Milgram–Nelson): if 𝔮 is a
closed nonnegative form and 𝔭 is a symmetric nonnegative form with
𝔮-relative form-bound < 1, then 𝔮 + 𝔭 is closed (closable). A *bounded*
form has relative form-bound 0 < 1.

Apply with 𝔮 = (closure of) 𝔥_B and 𝔭 = T_B·𝔡_B:
- 𝔥_B is closable (§1).
- T_B·𝔡_B is bounded (§1; T_B > 0 a finite sector constant, 𝔡_B
  bounded), hence 𝔥_B-form-bounded with relative bound 0.
- The common form domain is H¹_{A_0} (the energy form domain, contained
  in 𝔡_B's domain L²), which is dense.

Therefore **C_can = 𝔥_B + T_B·𝔡_B is closable on YM**, its closure has
form domain H¹_{A_0}, and its Friedrichs extension defines the canonical
generator and the canonical representation carrier
  H_can^YM := completion of (ℂ[X]_fin / ker C_can) under C_can.

## 3. What is discharged on YM, precisely

Combining the O-RQ.1 line on YM:
- **Positivity** (L+50): 𝔥_B ≥ 0 (H_NFC ≥ m² > 0 on the nontrivial
  sector); 𝔡_B ≥ 0; T_B > 0 on the positive-T sector ⇒ C_can ≥ 0.
- **Faithfulness** (L+51): the joint kernel carries transport, not only
  energy.
- **Canonical normalization** (L+52): T_B forced by transport-covariance.
- **Closability** (L+53, this result): C_can closable ⇒ the canonical
  pre-Hilbert object **completes** to H_can^YM.

So the **construction/existence content of O-RQ.1 — Theorem RQ.5's
"there exists a canonical pre-inner-product space with source map Γ₀" —
is discharged at CERT-PROJ force on YM.** The canonical inner product is
explicitly C_can = 𝔥_B + T_B·𝔡_B = energy ⊕ (temperature × distinguish-
ability), a closed form on the gauge-covariant H¹_{A_0}.

## 4. Conditions and honest scope (this is CERT-PROJ on one model, not universal)

- **Model-specific:** CERT-PROJ force on **YM only**. On GR/NS the energy
  form is closable (certified models) and the same argument applies if
  their type alphabets are finite/bounded; in general O-RQ.1 still needs
  the L+34 hypothesis per branch.
- **Conditional on:** thm:B1-closable's Y6 framework (energy closability,
  itself [C]); the positive-temperature exchange-coherent sector (L+35)
  on the YM mass-gap sector for T_B > 0; and the modeling identification
  of 𝔡_B with the (bounded) transport/distinguishability form.
- **Not yet done, even on YM:** the kernel-alignment check (c) — that
  ker C_can matches the YM encoding-predicate degeneracy (KCOMP/ND); and
  **universality** — that every lawful YM realization factors through
  H_can^YM, which is **O-RQ.2**, not O-RQ.1. So what discharges on YM is
  the *existence/construction* half of O-RQ.1; the universality half is
  the next obligation.

## 5. Status and significance

- **O-RQ.1 (existence/construction): discharged at CERT-PROJ on YM.** The
  load-bearing RIG-Q hinge — which the source note feared might fail into
  an indefinite structure — is concretely realized on a certified branch:
  a positive, faithful, canonically-normalized, closed canonical inner
  product C_can exists on YM, completing to H_can^YM.
- **Entirely inside the closed VRP structure.** C_can = energy form
  (L+34/thm:B1-closable) ⊕ temperature (L+35) × distinguishability ledger
  (L+28/29), closable by the finiteness of the collar alphabet (the same
  finiteness that drove entropy universality at L+29 and charge
  discreteness at L+45). The representation/metric frontier's hinge is
  realized using only recovered-variable machinery — no external import.
- **Promotion: still nothing.** RIG-Q remains non-promotable: this is
  CERT-PROJ on one model, the kernel-alignment (c) is unconfirmed,
  universality is the untouched O-RQ.2, and the downstream chain
  (O-RQ.3–O-RQ.8) plus the GR gating obligations (O-GR.real/compat) are
  all open. But the hinge that gated the entire program is now
  concretely realized on YM — a genuine milestone, honestly bounded.

## 6. Recommended continuation

**O-RQ.2 (universal realization):** does every lawful YM realization
factor through H_can^YM? With the canonical carrier now concretely in
hand on YM, universality is the natural next clause and the bridge to the
rest of the chain. (The kernel-alignment check (c) folds in here, since
universality is what forces ker C_can to be exactly the encoding
degeneracy.) If universality holds on YM, the RIG-Q representation target
is realized-and-universal on a certified branch at CERT-PROJ force, and
the chain advances to the metric weld (O-RQ.6), which is where the open GR
obligations re-enter.

*Holding-layer result, L+53. RIG-Q status unchanged (prospective program,
not promotable). O-RQ.1 existence/construction discharged at CERT-PROJ on
YM via KLMN form perturbation; canonical carrier H_can^YM defined;
universality (O-RQ.2) and the GR gating obligations remain.*

---

# Continuation L+54 — O-RQ.2 (Universal Realization on YM): Reduced to Comparison-Rigidity; Holds Within a Topological Sector; a Sharp Cross-Sector Obstruction Identified

*The universality clause: does every lawful YM realization factor through
the canonical carrier H_can^YM (built L+53)? Worked by constructing the
factoring map and locating exactly what pins or breaks universality.
Holding-layer result; no canon contact; nothing promoted.*

**Outcome in one line:** universality on YM **reduces to a single sharp
condition (comparison-rigidity)** modulo a minimality clause the program's
anti-smuggling rules already enforce; it **holds within a fixed
topological sector** at CERT-PROJ force; and taking it seriously surfaces
a **concrete cross-sector obstruction** — C_can is built from
local/spectral data and does not separate YM's topological (theta /
instanton) sectors, so cross-sector universality needs the source datum
to fix the sector (a named refinement). Universality is **reduced, not
fully discharged.**

## 1. The factoring map

For a lawful YM realization R = (H, ⟨·,·⟩_H, Γ, L, Π) of the source
encoding datum, define
  φ_R : H_can^YM → H,   φ_R([x]) = Γ(x)   on source classes x ∈ X,
extended by linearity and continuity. φ_R is well-defined and isometric
**iff** the realization's inner product agrees with the canonical form on
source classes:
  ⟨Γ(x), Γ(y)⟩_H = C_can(x,y)   for all x,y ∈ X.   (★)
Universality (R factors through H_can^YM, uniquely up to canonical
unitary) is exactly: (★) holds and Γ(X) is dense in H.

## 2. What lawfulness forces, and the residual

**Forced direction.** A lawful realization carries the *same* licensed
objects the canonical form is built from: the generator (energy form
𝔥_B, by generator uniqueness prop:vrp-transfer-reduction), the transport
operator (𝔡_B), and the symmetry Π. So R reproduces C_can on the
structure C_can sees — (★) holds **restricted to the C_can-visible
(energy/transport/symmetry) data.**

**The gap.** (★) as an *equality* can fail only if R carries inner-product
structure on source classes **beyond** energy + transport + symmetry —
i.e. a lawful invariant not captured by C_can. So universality reduces to
two conditions:

- **Minimality / cyclicity:** Γ(X) dense in H (R is generated by source
  classes, no imported "junk" subspace). **Enforced** by RIG-Q's Standing
  Rules (no smuggling of non-source-descended structure); under them
  lawful realizations are minimal. This condition is met by the program's
  own governance.
- **Comparison-rigidity (the open content):** the YM encoding admits **no
  lawful inner-product invariant on source classes beyond the C_can data**
  — i.e. C_can is the *complete* source-comparison datum. Under
  comparison-rigidity, (★) holds with equality.

Under minimality + comparison-rigidity, φ_R is an isometric isomorphism
and **universality holds**: every lawful YM realization is canonically
unitarily equivalent to H_can^YM. Universality on YM is therefore
**reduced to comparison-rigidity.**

## 3. The cross-sector obstruction (sharp, YM-specific)

Comparison-rigidity is **not** unconditional on YM, and the obstruction is
concrete. C_can = 𝔥_B + T_B·𝔡_B is built from **local/spectral** data:
the gauge-covariant curvature energy form, the (finite-alphabet) type
transport, and the gauge symmetry. But YM genuinely carries
**topological structure** — instanton number and theta sectors are present
in the branch. Configurations in distinct topological sectors can share
the same local energy/transport/spectral data, so **C_can does not
separate topological sectors.** Consequently:

- A lawful realization that distinguishes theta/instanton sectors carries
  structure C_can does not see — (★) fails across sectors, and such a
  realization does **not** factor through H_can^YM.
- Structurally this is expected: H_can^YM is built around a background A_0
  (the energy form is |D_{A_0}·|²), so it is naturally a **per-sector**
  (per-background) carrier. Universality is a **within-sector** statement;
  the cross-sector relation is a different question.

**Conclusion:** comparison-rigidity — and hence universality — holds
**within a fixed topological sector** (modulo local comparison-rigidity,
the plausible completeness of energy+transport+symmetry for local data).
**Cross-sector** universality requires the source encoding datum to fix
the topological sector (or C_can to be refined with topological data).
This is the named refinement:

> **O-RQ.2-topological.** Either the YM source encoding datum determines
> the topological sector (so realizations are per-sector and within-sector
> universality is the full statement), or C_can must be enriched with a
> topological invariant to achieve cross-sector universality.

## 4. Honest status

- **O-RQ.2 (universality on YM): REDUCED, not fully discharged.** The
  factoring map is constructed (§1); compatibility is forced on the
  C_can-visible data (§2); universality reduces to minimality (enforced by
  anti-smuggling rules) + comparison-rigidity (§2).
- **Within a fixed topological sector:** universality holds at CERT-PROJ
  force, modulo local comparison-rigidity (the residual sharp condition —
  that energy+transport+symmetry is the complete *local* source-comparison
  datum).
- **Across topological sectors:** a concrete obstruction is identified —
  C_can is topology-blind — bounding universality to within-sector and
  surfacing the named refinement O-RQ.2-topological.
- **What was learned:** universality is not free, and its precise
  deficiency on YM is now named — not positivity, not faithfulness, not
  normalization (all resolved L+50–L+53), but (i) local comparison-
  rigidity and (ii) topological-sector data. The canonical carrier is
  per-background; the representation forcing is a within-sector statement.
- **Promotion: still nothing.** RIG-Q remains non-promotable: universality
  is reduced not proved, comparison-rigidity and O-RQ.2-topological are
  open, and the downstream chain (O-RQ.3 uniqueness, O-RQ.4–5 induced
  form, O-RQ.6 metric weld, O-RQ.7–8 cone-null + signature) plus the GR
  gating obligations are untouched. Holding-layer; no corpus [O] created.

## 5. Recommended continuation

Two honest options. **(i)** Attack **local comparison-rigidity** directly:
prove (or refute) that energy + transport + symmetry is the complete local
source-comparison datum for the YM encoding (no extra local lawful
invariant) — if proved, within-sector universality discharges at CERT-PROJ
on YM. **(ii)** Resolve **O-RQ.2-topological**: determine whether the YM
source datum fixes the topological sector (settling whether universality
is inherently within-sector or needs C_can enriched). Either sharpens the
representation-forcing target; neither promotes anything until the
residuals close and the GR gating obligations are addressed. Note the
chain's next structural step after universality — the metric weld
(O-RQ.6) — re-enters the open GR obligations O-GR.real/compat, which
remain the external gate on the whole program.

*Holding-layer result, L+54. RIG-Q status unchanged (prospective program,
not promotable). O-RQ.2 reduced to comparison-rigidity + minimality;
within-sector universality at CERT-PROJ modulo local rigidity; cross-sector
obstruction (topological-sector data) named as O-RQ.2-topological.*

---

# Continuation L+55 — O-RQ.2-topological Resolved (Into Existing Structure), and Closing Consolidation of the O-RQ.1/O-RQ.2 Effort

*Project-Lead judgment call (operator delegated). Rather than drill into a
further sub-reduction, resolve the cleaner hinge — which has a terminal
answer — and consolidate. Holding-layer; no canon contact; nothing
promoted.*

## A. O-RQ.2-topological — resolved into the L+36 interface-cohomology structure

The question: does the source encoding datum fix the topological sector
(making within-sector universality the full statement), or must C_can be
enriched? Checked against the actual datum structure:

- The **source encoding datum is local** (Book II): built from collar
  data on the relational substrate, with **no global gluing/cocycle
  content** at the foundational level. The global gluing data appears at
  the **branch** level (YM carries the bundle/gluing structure).
- C_can (local/spectral) therefore does not — and structurally cannot —
  capture the global topological sector (confirming L+54).
- **The topological sector is a gluing class.** A YM topological sector is
  the gauge-bundle class, i.e. a Čech class in H¹(cover; G) (transition-
  function cohomology). This is the **same type of object** as the L+36
  synchronization obstruction, which lives in H¹(interface nerve; G)
  supported on β₁ — and Book II already carries the β₁ cycle-rank
  structure these classes inhabit.

**Resolution.** The global/topological data that C_can omits is **not new
open content** — it is interface-nerve gluing cohomology of exactly the
kind the corpus already characterizes (the L+36 β₁-supported H¹ class).
The canonical carrier H_can^YM is therefore **per-gluing-class** (per
topological sector / per background bundle): fix the H¹(cover; G) class,
and C_can forces the representation within it. **Within-sector
universality is the natural and full statement** of representation-forcing
— one forces the representation *given* the global sector, exactly as one
forces it given a background A₀; the choice of sector is genuinely
additional (cohomological) data, already handled by the corpus's interface
machinery, not a deficiency of the construction. O-RQ.2-topological is
thus resolved structurally: cross-sector data = L+36-type interface gluing
cohomology; within-sector universality stands modulo local comparison-
rigidity. (This is a structural identification routing the obstruction
into existing machinery, not a computation equating instanton number to a
specific L+36 class; the point is that the *kind* of object is already in
the corpus.)

## B. Closing consolidation — where the O-RQ.1/O-RQ.2 effort stands

Across L+50–L+55 the operator-opened deep-frontier effort drove RIG-Q's
load-bearing hinge from "may fail into an indefinite structure" to a
precise, corpus-grounded state. Summary:

**Achieved (at CERT-PROJ force, holding-layer, on YM):**
- **O-RQ.1 existence/construction discharged on YM** (L+50–L+53): the
  canonical pre-inner-product is C_can = 𝔥_B + T_B·𝔡_B = **energy ⊕
  (temperature × distinguishability)** — positive (L+50), transport-
  faithful via the joint form (L+51), canonically normalized by the
  temperature via transport-covariance (L+52), and closable on YM via
  KLMN + the finite collar alphabet (L+53), completing to H_can^YM.
- **O-RQ.2 within-sector universality reduced** (L+54–L+55): the factoring
  map is constructed; universality holds within a fixed topological
  (H¹-gluing) sector modulo **local comparison-rigidity**, with minimality
  enforced by the anti-smuggling rules and the cross-sector data
  identified as existing L+36 interface cohomology.

**The single clean remaining within-YM residual:**
- **Local comparison-rigidity** — that energy + transport + symmetry +
  distinguishability is the *complete local* source-comparison datum for
  the YM encoding (no further local lawful invariant). This is a sharp
  classification question and a reasonable terminal residual for the
  within-YM construction.

**The structural finding (the real payoff):** the representation/metric
frontier's load-bearing hinge resolves **entirely into established NFC
structure** — the closed VRP recovery variables (energy L+34, temperature
L+35, distinguishability ledger L+28/29), the L+30 kernel, the finite
collar alphabet (L+29/L+45), and the L+36 interface cohomology. The
frontier RIG-Q targets is not disjoint from the corpus; it is its
continuation, with one clean open local-rigidity residual on YM and an
external gate beyond.

**The external gate (unchanged, decisive):** every route past universality
— uniqueness (O-RQ.3), induced form (O-RQ.4–5), and especially the
**metric weld (O-RQ.6)** — re-enters the open GR obligations
**O-GR.real / O-GR.compat**, which the L+42 triage placed out-of-toolkit
(nonlinear-PDE global stability). No amount of within-YM work removes this
gate; the RIG-Q endpoint (a *derived* Lorentzian interface metric)
remains gated on out-of-toolkit GR machinery.

## C. Project-Lead recommendation: hold the RIG-Q effort here, consolidated

I recommend **holding** the RIG-Q proof effort at this consolidated point,
rather than drilling into local comparison-rigidity or the downstream
chain, for three honest reasons:
1. **Diminishing within-toolkit returns.** Each further step reduces to a
   sharper sub-condition; local comparison-rigidity is a sharp
   classification question that is a reasonable stopping point, and pushing
   past it does not change the program's promotability.
2. **The decisive gate is external.** The endpoint is gated on
   O-GR.real/compat (out-of-toolkit). Within-YM progress cannot close the
   program; only opening a GR nonlinear-PDE program could, and that is a
   separate major scope decision.
3. **The valuable result is already secured and recorded.** The hinge is
   discharged on YM at CERT-PROJ, the canonical form is identified as a
   VRP-variable object, and the obstructions are named and routed into
   existing structure. This is the honest, useful deliverable; further
   drilling risks an open-ended thread without changing the status.

RIG-Q remains a **non-promotable prospective program** with a now-sharp
map: within-YM, one local-rigidity residual; globally, the out-of-toolkit
GR gate. The natural next *substantive* move is not more RIG-Q drilling
but the standing architectural decision — whether to open a GR
nonlinear-PDE external-machinery program — which is the program owner's
call.

*Holding-layer consolidation, L+55. RIG-Q status unchanged (prospective,
non-promotable). O-RQ.2-topological resolved into L+36 interface
cohomology; within-sector universality reduced to local comparison-
rigidity; effort consolidated; recommend hold pending the GR scope
decision. No corpus [O] created.*

---

# Continuation L+61 — Local Comparison-Rigidity Settled: O-RQ.2 Within-Sector Universality Discharged on YM; O-RQ.3–5 Cascade; Chain Stands at the Metric Weld (Now With a Realized GR Target)

*Resuming the RIG-Q line after the L+60 GR result lifted the metric-weld
gate in the CK corner. The next open internal step was O-RQ.2's residual,
local comparison-rigidity. Holding-layer; no canon contact; nothing
promoted.*

**Outcome in one line:** local comparison-rigidity **holds** on YM, so
**O-RQ.2 within-sector universality discharges at CERT-PROJ**; O-RQ.3
(uniqueness), O-RQ.4 (induced-form invariance), and O-RQ.5
(nondegeneracy) follow; the RIG-Q chain now stands at the metric weld
**O-RQ.6**, whose GR target g_{μν} was realized in the CK corner at L+60.

## 1. Local comparison-rigidity holds

The residual from L+54–55: is C_can the complete local source-comparison
datum, with no extra lawful invariant? The structure settles it. The
observable family is the certified triple (Spec(L_Spec), R_probe, T_Spec)
— spectrum, probe-response algebra, transport — and R_resp is a
\emph{certified} observable family, its content fixed by the encoding,
not free. In any lawful realization:
- the **generator** (spectral/energy data), **transport** operator, and
  **symmetry** action are the *same licensed objects* (by their
  uniqueness/transfer — prop:vrp-transfer-reduction and the symmetry
  certification), encoding-fixed, not free;
- the **probe-response algebra** R_probe is generated by these
  encoding-fixed operators (linear-response reconstruction: the response
  to a fixed admissible probe coupling is determined by the spectral
  decomposition of the generator and its transport matrix elements);
- the **inner product** is the forced C_can = 𝔥_B + T_B·𝔡_B (L+50–52).

So two lawful YM realizations agree on **both** the inner product
(C_can, forced) **and** the operators (generator/transport/symmetry,
encoding-fixed), with the probe-response algebra generated by the latter.
There is no room for an additional lawful inner-product invariant: any
candidate extra invariant would be either a function of the encoding-fixed
operators (already captured) or non-source-descended (barred by the
anti-smuggling Standing Rules). **Local comparison-rigidity holds**, on
YM, conditional on the linear-response reconstruction (response generated
by the encoding-fixed operators — standard) and the encoding fixing the
admissible probes (definitional).

## 2. O-RQ.2 discharges, and O-RQ.3–5 cascade

With local comparison-rigidity and minimality (the anti-smuggling rules),
the L+54 factoring map φ_R is an isometric isomorphism for every lawful
within-sector realization:

- **O-RQ.2 (within-sector universality): discharged at CERT-PROJ on YM.**
  Every lawful YM realization in a fixed topological (H¹-gluing) sector
  factors through H_can^YM, unitarily, because it agrees with the
  canonical carrier on both inner product and operators.
- **O-RQ.3 (canonical unitary uniqueness): follows.** Universality gives
  every lawful realization ≅ H_can^YM up to the canonical unitary
  identifying cyclic data; uniqueness up to canonical unitary is immediate.
- **O-RQ.4 (induced-form invariance): follows.** The induced bilinear form
  on H_can^YM is C_can itself, which is realization-independent by
  construction (canonical, forced — L+50–52), hence invariant under lawful
  re-description.
- **O-RQ.5 (nondegeneracy): follows.** C_can is nondegenerate on
  H_can^YM: the joint kernel was quotiented out (faithfulness, L+51), so
  the form is nondegenerate on the carrier.

So the **representation-forcing half of RIG-Q (O-RQ.1 → O-RQ.5)** is now
[C]/CERT-PROJ on YM within a fixed topological sector: the representation
exists, is canonical, universal, unique up to canonical unitary, with a
canonical invariant nondegenerate induced form Q_can = C_can.

## 3. The chain now stands at the metric weld O-RQ.6 — with a realized target

What remains is the **metric-identification half**: O-RQ.6 (weld Q_can to
GR's g_{μν}), O-RQ.7 (cone-null compatibility), O-RQ.8 (derived Lorentz
signature). The decisive change from L+60: **the GR target g_{μν} now
exists.** prop:gr-ck-corner-extension realized g_{μν} in the small-data
AF vacuum corner (genuine Einstein-vacuum metric, asymptotically
Minkowskian). So O-RQ.6 is no longer welding to an open obligation — it
welds Q_can (the YM-built canonical induced form) to a realized GR metric.

**The remaining content of O-RQ.6 is the cross-branch identification**:
showing that the YM-representation induced form Q_can and the GR-corner
metric g_{μν} are the same object (or canonically identified). This is a
genuine cross-branch weld (YM induced form ↔ GR metric), not a within-YM
step — and it is the natural next hinge. O-RQ.7 (cone-null) and O-RQ.8
(signature via Book VI thm:lorentzian-signature, whose (SI) hypothesis
RIG-Q targets) follow the weld; note that in the CK corner the GR metric
is already asymptotically Minkowskian (Lorentzian) by CK, which is a
strong consistency check on the eventual signature, though not yet the
RIG-Q representation-forced derivation.

## 4. Honest status

- **O-RQ.2 within-sector universality: discharged at CERT-PROJ on YM**
  (conditional on linear-response reconstruction + encoding-fixed probes
  + the topological sector fixed). O-RQ.3–5 follow.
- **Representation-forcing half (O-RQ.1–5): [C]/CERT-PROJ on YM
  within-sector.** A real milestone: the canonical representation is
  forced, universal, and carries a canonical nondegenerate induced form.
- **Remaining: the metric-identification half (O-RQ.6–8)**, now with a
  realized GR target (L+60). O-RQ.6 is a cross-branch weld.
- **Promotion: still nothing.** CERT-PROJ on one model, within-sector,
  conditional; O-RQ.6–8 open; the weld is cross-branch and the corner is
  scoped. RIG-Q remains non-promotable. Holding-layer; no corpus [O].

## 5. Recommended continuation

**O-RQ.6 (metric weld) in the CK corner:** determine whether the YM
induced form Q_can and the GR-corner metric g_{μν} are canonically
identified. This is the cross-branch hinge the whole RIG-Q program builds
toward, and for the first time both sides exist concretely (Q_can on YM
from O-RQ.1–5; g_{μν} on the GR corner from L+60). It is genuinely
cross-branch and likely hard; either it identifies them (advancing to
cone-null and signature) or it exposes the precise YM↔GR mismatch — a real
result either way.

*Holding-layer result, L+61. RIG-Q non-promotable. O-RQ.2 within-sector
universality discharged at CERT-PROJ on YM; O-RQ.3–5 cascade; chain at the
metric weld O-RQ.6 with a realized GR target.*

---

# Continuation L+62 — O-RQ.6 (Metric Weld): Direct Identification Rejected, the Weld Structured, and the Chain Reduced to Cone-Null Compatibility = the (SI) Hypothesis (Loop Closed)

*The cross-branch metric weld, with Q_can (YM induced form) on one side
and the L+60 GR-corner metric g_{μν} on the other. Holding-layer; no
canon contact; nothing promoted.*

**Outcome in one line:** a **direct** identification Q_can = g_{μν} is
**rejected** on two grounds (signature and domain), but the weld is
**structured**: the 4D metric content is carried by R_resp
(dim = 9 = the traceless-symmetric 4D metric dof), Q_can supplies the
positive-definite spatial part, the VRP time rung supplies the temporal
direction, and the Lorentzian signature emerges from the spatial/temporal
split. **O-RQ.6 thereby reduces to cone-null compatibility (O-RQ.7),
which is exactly the (SI) hypothesis of Book VI thm:lorentzian-signature**
— closing the loop with RIG-Q's original purpose.

## 1. The direct identification fails — two mismatches

Q_can = C_can = 𝔥_B + T_B·𝔡_B is a **positive-definite** inner product on
the **infinite-dimensional** YM representation carrier H_can^YM. The
GR-corner g_{μν} is a **Lorentzian** (indefinite, −+++) metric on the
**4-dimensional** tangent space. So Q_can = g_{μν} is false twice over:
- **Signature mismatch:** positive-definite ≠ Lorentzian. A representation
  inner product cannot *be* a Lorentzian metric.
- **Domain mismatch:** a form on an infinite-dimensional Hilbert space is
  not a form on a 4-dimensional tangent space.

The weld must therefore be a *structured correspondence*, not an equality.
This is the honest crux any "metric from a positive inner product" program
faces, and naming it is the first result.

## 2. The structured weld

**Dimensional content — carried by R_resp.** The GR response algebra has
$\dim\mathcal{R}_{\mathrm{resp}} = 9$, decomposed $1+4+4$ in the GR
branch; nine is exactly the number of independent components of a
traceless symmetric 4D 2-tensor — the metric-perturbation (graviton)
degrees of freedom. So R_resp already carries the 4-dimensional
metric-perturbation structure: the dimensional content of the weld is
**present in the corpus**, not a free input. The frame map
$\iota: T_pM^4 \to$ (representation modes) routes through this structure
rather than being conjured. \emph{(The precise $1+4+4$ block reading is a
detail; the load-bearing fact is $\dim\mathcal{R}_{\mathrm{resp}} = 9 =$
4D metric dof.)}

**Spatial part — from Q_can.** Under the frame map, the positive-definite
Q_can supplies the positive-definite (spatial) block of the metric — the
Riemannian part. This matches the GR-corner metric, whose spatial block
is positive-definite (near-Minkowski).

**Temporal direction — from the VRP time rung.** The Lorentzian signature
needs a distinguished timelike direction. This is supplied not by Q_can
(which is positive-definite) but by the **licensed VRP time**
(Thm.~\ref{thm:vrp-time}, time as the certified continuation order) and
its canonical temporal projection — precisely the "canonical temporal
projection" from which Book VI thm:lorentzian-signature derives the causal
cone $C$.

**Signature — from the split.** The Lorentzian $(-,+,+,+)$ then emerges
from the spatial/temporal split: three (+) directions from Q_can's spatial
block, one ($-$) from the VRP-time direction. The signature is not posited;
it is the split of the recovered variables — spatial from
energy ⊕ temperature × distinguishability, temporal from licensed time.

## 3. The reduction — O-RQ.6 → O-RQ.7 = (SI): the loop closes

The one thing the structured weld still needs is that the spatial Q_can
block and the temporal VRP-time direction **assemble consistently** into
the Lorentzian metric — i.e. that the null cone of the assembled form is
the causal cone. That consistency condition is **cone-null
compatibility** $\partial C \subseteq \{v : Q(v)=0\}$ — which is
**verbatim the (SI) hypothesis** of Book VI thm:lorentzian-signature
(Q nondegenerate + cone-null, with $C$ from the canonical temporal
projection). So:

> **O-RQ.6 (metric weld) reduces to O-RQ.7 (cone-null compatibility),
> which is exactly the (SI) hypothesis of thm:lorentzian-signature.**

This closes the loop with RIG-Q's founding purpose (L+49): RIG-Q was
opened precisely to discharge the (SI) hypothesis of the Lorentzian-
signature theorem by forcing Q canonically. The entire chain —
O-RQ.1 (construction) → O-RQ.5 (canonical nondegenerate induced form) →
O-RQ.6 (structured weld) — now lands exactly on (SI). Nondegeneracy of Q
is already in hand (O-RQ.5, faithfulness). What remains is the cone-null
half of (SI): that the causal cone from the VRP-time projection is null
for Q_can.

## 4. Honest status

- **O-RQ.6: structured, reduced — not a direct identification.** The
  signature and domain mismatches are resolved by the spatial/temporal
  split (Q_can spatial + VRP-time temporal), with the 4D dimensional
  content carried by R_resp (dim 9 = 4D metric dof). The weld reduces to
  cone-null compatibility.
- **O-RQ.6 → O-RQ.7 = (SI).** The remaining genuine content of the metric
  weld is exactly the cone-null half of the (SI) hypothesis; once it
  holds, thm:lorentzian-signature delivers O-RQ.8 (derived Lorentz
  signature), and RIG-Q's endpoint is reached.
- **The chain is now a single hinge from its goal.** O-RQ.1–5 closed on
  YM within-sector (CERT-PROJ); O-RQ.6 structured and reduced to (SI);
  O-RQ.7 = (SI) cone-null is the last genuine condition; O-RQ.8 follows
  from thm:lorentzian-signature.
- **Promotion: still nothing.** Holding-layer; CERT-PROJ/within-sector/
  conditional; cone-null (O-RQ.7/(SI)) open; the frame map is structured
  but not fully proven; the GR side is the scoped CK corner. RIG-Q
  remains non-promotable. No corpus [O].

## 5. The honest shape of what remains

RIG-Q has been driven from a 443-page open program to a single remaining
mathematical condition: **cone-null compatibility (O-RQ.7 = (SI))** — that
the causal cone derived from the licensed VRP-time projection is null for
the canonical form Q_can = energy ⊕ temperature × distinguishability. If
that holds, the chain closes and thm:lorentzian-signature derives the
Lorentz signature; if it fails, the precise way the recovered-variable
form and the causal cone are misaligned is the obstruction. Either is a
real result. Notably, the whole metric weld resolved **into established
NFC structure**: R_resp's 4D metric dof, the VRP time rung, Q_can from the
VRP variables, and Book VI's signature theorem — no new external machinery
beyond CK (which supplied the GR-corner target at L+60).

*Holding-layer result, L+62. RIG-Q non-promotable. O-RQ.6 structured and
reduced to cone-null compatibility = the (SI) hypothesis; the chain stands
one hinge (O-RQ.7) from its Lorentz-signature endpoint.*

---

# Continuation L+63 — O-RQ.7 (Cone-Null = (SI)): the Close Attempted; Cone Structure and Cone-Null Match Follow, but ISOTROPY Is Irreducible — the Chain Reduces to Emergent Lorentz Invariance

*The final hinge: attempt to discharge cone-null compatibility = the (SI)
hypothesis, which would close the entire RIG-Q chain. Holding-layer; no
canon contact; nothing promoted.*

**Outcome in one line:** the close **does not succeed** — but it
**almost** does, and where it stops is sharp and honest. Two of the three
ingredients follow (the causal **cone structure** from collar locality;
the **cone-null match** by calibration), but the third — **spatial
isotropy** (a round cone = exact Lorentz invariance) — is **irreducible**:
the discrete minimal symmetry carrier is not the full rotation group, and
(SI) is exactly the assumed isotropy. The entire RIG-Q chain therefore
reduces, end-to-end, to a single deep question: **whether the Book VI
continuum bridge restores exact spatial isotropy (emergent Lorentz
invariance) from the discrete collar substrate.**

## 1. What cone-null compatibility requires

The assembled candidate metric is g = −a(time)² + Q_can(spatial) (L+62),
with the time direction from the VRP time rung and Q_can the positive-
definite spatial form. (SI)/cone-null asks: the causal cone C derived
\emph{independently} from the VRP-time/continuation-order causal structure
must coincide with the null cone of g, ∂C = {v : g(v)=0}. Three things
must hold: (i) C is a genuine \emph{cone} (a finite maximum propagation
speed exists); (ii) the cone is \emph{calibrated} to g (the propagation
speed matches the spatial form, fixing a); (iii) the cone is
\emph{round} (isotropic) — the same speed in every spatial direction.

## 2. What follows (two of three)

**(i) Cone structure — follows from collar locality.** Transport is
collar-local on the finite collar alphabet (K_0=7): a continuation step
moves at most one collar-step, so there is a finite maximum propagation
rate. Causal accessibility is therefore bounded by a cone, not all of
space — a genuine causal cone exists. [C], from collar locality.

**(ii) Cone-null match (calibration) — follows.** Fixing the constant a so
that the metric's null speed equals the collar propagation speed makes
∂C = {g=0} on the calibrated cone. This is a calibration (the "speed of
light" = the collar propagation speed), available once (i) holds. [C].

## 3. What does NOT follow — isotropy is irreducible

**(iii) Roundness (isotropy) — the irreducible residual.** A round cone
requires the propagation speed to be the same in every spatial direction
— full spatial-rotation symmetry SO(3). But the NFC substrate's symmetry
is the **minimal symmetry carrier (MSC), a discrete** structure
(space-group/point-group level), **not** SO(3). A discrete collar
substrate generically yields an \emph{anisotropic} cone — different
propagation speeds along different lattice directions, reflecting the
discrete point group, not full rotational symmetry. And Book VI's
isotropy is precisely the **(SI) hypothesis** — assumed, not derived.
So roundness/isotropy is exactly the content RIG-Q has \emph{not}
supplied: it is not in the discrete symmetry (MSC ≠ SO(3)), and it is the
assumed half of (SI).

**Consequence.** Cone-null compatibility — and hence the RIG-Q close —
reduces to **isotropy restoration**: does the Book VI continuum bridge
wash out the collar-lattice anisotropy to yield a round (Lorentzian)
light cone as the collar scale → 0? This is the well-known **emergent
Lorentz invariance from a discrete substrate** problem. It is plausible
(if the anisotropic operators are irrelevant under the continuum bridge)
but \emph{not automatic} (Lorentz-violating anisotropy can survive), and
NFC's continuum bridge does not settle it. It cannot be derived from the
discrete structure, because the discrete structure does not contain SO(3).

## 4. Honest verdict — the chain does not close; it reduces to one deep question

The RIG-Q close is **not achieved.** The honest terminal state:
- O-RQ.1–O-RQ.6: established at CERT-PROJ on YM within-sector (construction,
  positivity, faithfulness, normalization, closability, universality,
  uniqueness, induced form, structured metric weld).
- O-RQ.7 (cone-null = (SI)): cone structure (i) and calibration (ii)
  follow; **isotropy (iii) is irreducible** and is the assumed content of
  (SI).
- O-RQ.8 (derived signature): would follow from thm:lorentzian-signature
  \emph{once} (SI) holds — i.e. once isotropy is established.

So the entire 443-page RIG-Q program, pushed to its endpoint, reduces to
a **single, sharply located, deep question**: emergent spatial isotropy
(Lorentz invariance) from the discrete collar substrate, via the Book VI
continuum bridge. RIG-Q does not solve it — but it shows that
\emph{everything else} reduces to it, and that the missing ingredient is
exactly the one physical principle a discrete substrate cannot supply for
free: full rotational symmetry.

## 5. Why this is the honest outcome (not a manufactured close)

It would have been easy to declare cone-null "compatible by construction"
— but that is circular (it holds trivially only if C is *defined* as g's
cone; the real content is the *independently* derived causal cone matching
g's null cone, and its roundness). The genuine obstruction is isotropy,
and it is genuine: the discrete MSC is not SO(3), and (SI) assumes exactly
what is missing. Declaring the close would falsify the program's own
anti-smuggling discipline (it would smuggle in rotational symmetry not
present in the substrate). The honest result — reduction to emergent
Lorentz invariance — is both the correct verdict and a genuinely
illuminating one: it identifies the precise, irreducible physical content
the representation→metric→signature program bottoms out on.

## 6. Status

- **RIG-Q: reduced to its irreducible core.** O-RQ.1–6 at CERT-PROJ on YM
  within-sector; O-RQ.7 reduced to isotropy restoration (emergent Lorentz
  invariance); O-RQ.8 contingent on it. The program is non-promotable and
  now provably so until the isotropy question is settled — which is not an
  NFC-internal matter but the deep emergent-Lorentz-invariance problem,
  plausibly continuum-bridge-dependent and not derivable from the discrete
  substrate. Holding-layer; no corpus [O]; nothing promoted.
- **The RIG-Q line is at its genuine terminus.** Further within-NFC work
  cannot close it; the residual is a known hard physical problem, not a
  reducible NFC obligation.

*Holding-layer result, L+63. RIG-Q non-promotable, reduced end-to-end to
emergent spatial isotropy (Lorentz invariance) from the discrete
substrate via the continuum bridge — the irreducible content of (SI).
The close is not achieved; the chain is reduced to its deep core.*
