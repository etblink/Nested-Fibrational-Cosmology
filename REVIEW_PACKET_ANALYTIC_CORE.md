# MIG-048 — Independent Analytic Review Packet
# Γ Strip-Cyclicity / Continuity–Form-Core / RH-SCC Overlay Gates

**Class:** scaffold review packet; **not canon**. Assembled at accepted baseline `cbed4bb`
(MIG-047). **No repository file was created or modified in assembling this packet**; it is a
delivery artifact only (see §12, Path Authorization).

**Standing classification (verbatim in substance, load-bearing).** The certified rational-height
results M_H (H = 2 … 10) are finite restricted rational-height Weil tests, never RH
theorem-steps; they use no zero-location input and license no RH, SCC, or canonical-status
promotion. P0-WEIL-CORE is an internally verified form-core theorem about a declared domain;
the RH ⟺ {M_H ⪰ 0 ∀H} equivalence is conditional and symmetric, built on **imported** Weil and
Burnol criteria, and may not be described as evidence for RH (prohibitions 18–19). Per MIG-030,
the cyclicity and continuity arguments **have not undergone independent specialist review**, and
the equivalence may be described as a result only within the internal scaffold until such review
occurs. **This packet exists to obtain that review.**

**Why this review dominates the computational ladder.** The H-ladder (H = 2 … 10, all
certified, MIG-032 … MIG-047) is doing exactly what it should: producing increasingly strong
finite consistency checks *inside* the exact reformulation. But the reformulation itself rests
on the analytic chain reviewed here. A failure in this chain voids the meaning of every finite
success; a clean review makes the ladder meaningful as certified evidence inside a properly
audited infinite reformulation. That asymmetry is why height authorization is paused after H=10
in favor of this packet.

---

## 0. The three verdicts requested

| # | Review target | Where it lives | Current internal status |
|---|---|---|---|
| V1 | **Γ strip-cyclicity theorem** (T3 closure) | `RESEARCH_PACKET_RH_P0_WEIL_CORE.md` §2 (+ MIG-030 Laplace-primitive lemma) | Internally verified; never externally reviewed |
| V2 | **Continuity / form-core passage** (T1, moment-correction lemma, T2 Burnol import, and the composed equivalence RH ⟺ {M_H ⪰ 0}) | `RESEARCH_PACKET_RH_P0_W1.md` §§1–5; `RESEARCH_PACKET_RH_K0_WEIL.md` §§3–8; `RESEARCH_PACKET_RH_P0_WEIL_CORE.md` §4 | T1 proved internally; T2 closed via import; composition recorded |
| V3 | **RH/SCC overlay gates** (five canon claims + the K0/F4/D4 defect adjudication + disposition plan) | `NFC_SCC_Branch.tex` §"SCC-RH Kernel Positivity Equivalence"; `metadata/overlay.json`; `RESEARCH_PACKET_RH_K0.md` | Defects D1–D4 + F4 recorded internally (2026-07-03); claims gated `review_needed`; replacement route is V1+V2 |

Reviewer verdict forms are in §10. Falsification targets are in §8. Candidate weak points
identified during packet assembly (honest self-audit; not adjudicated) are in §9.

---

## 1. Architecture: how the three targets relate

The discovered failure order, layer by layer, each exposed *before* any theorem was attempted
against it:

```
S1 witness packet
  └─ F4 fired: canon probe space trivial (SCC-M3 + SCC-M4 ⟹ f = 0 a.e.)
       └─ P0 opened (probe repair)
            └─ K0 defect found one layer upstream: canon kernel criterion ill-posed (D1–D4)
                 └─ K0-6 anchor decision: re-anchor to the IMPORTED Weil criterion
                      (bespoke kernel route preserved as superseded intake, prohibition 13)
                      └─ K0-W1: exact imported Weil formulation (test class 𝒲, explicit
                         formula, symmetric zero summation, form 𝔔_W on 𝒲₀)
                           └─ P0-W1: weighted Sobolev form domain 𝓗¹_a, ½ < a < 1
                                ├─ T1 form continuity  — PROVED (internal)
                                ├─ T2 determining domain — CLOSED via Burnol import
                                └─ T3 constrained core — REDUCED (moment-correction lemma)
                                     └─ Γ strip-cyclicity — PROVED (internal, P0-WEIL-CORE)
                                          └─ RH ⟺ M_H ⪰ 0 for every H  (exact equivalence)
                                               └─ K0-W3 certified ladder H = 2 … 10
```

The five canon overlay gates (V3) are the *pre-K0* text: they remain in canon with intact
`[D]/[C]/[R]` tags but **gated usable force** (`review_needed` in `metadata/overlay.json`),
awaiting either repair or formal supersession-as-intake. The V1+V2 chain is the replacement
route. The three verdicts are therefore not independent: **V3 asks the reviewer to confirm the
internal defect adjudication and disposition plan; V1+V2 ask whether the replacement chain
actually holds.**

---

## 2. The analytic setting (exact statements under review)

All statements below are quoted in substance from the packets of record; the packets contain
the full text and the internal verification logs.

**The space.** Fix ½ < a < 1. 𝓗¹_a := { H : e^{a|t|}H ∈ L²(ℝ), e^{a|t|}H′ ∈ L²(ℝ) } with
‖H‖² = ‖e^{a|t|}H‖₂² + ‖e^{a|t|}H′‖₂². (Weighted Sobolev; Hilbert.)

**The moments.** L_±(H) = ∫ H(t) e^{±t/2} dt. Continuous on 𝓗¹_a **iff a > ½** (Cauchy–Schwarz
against ‖e^{±t/2−a|t|}‖₂). 𝓗¹_{a,0} := ker L₊ ∩ ker L₋, closed, codimension exactly 2
(surjectivity via two dilates: L₊(H_q) = √π/2q, L₋(H_q) = √π, det = π/4 ≠ 0).

**The generator and orbit.** H₀(t) = eᵗe^{−eᵗ} (image of f₀(x) = √x·e^{−x});
H_q(t) = q^{−1/2}H₀(t + log q), q ∈ ℚ₊. H₀ ∈ 𝓗¹_a **iff a < 1** (the −∞ tail e^{(1−a)t});
the weight is translation-quasi-invariant (‖H_q‖ ≤ e^{a|log q|}·const). Under the strip
transform, H₀ ↦ Γ(1+z), zero-free and analytic on |Re z| ≤ a < 1.

**The imported criterion (external; not re-proved).** Weil positivity in Bombieri's
normalization: RH ⟺ 𝔔_W ≥ 0 on the declared test class 𝒲₀ (two-sided moment-null), with the
zero side taken in the prescribed symmetric limit Σ*_ρ = lim_{T→∞} Σ_{|Im ρ|<T}. Import status
`[B]`/external-theorem; the research burden is **not** to reprove Weil's criterion but to show
the NFC probe family is a sufficient test core for it. Burnol's compact-support form
(arXiv:math/9810169) supplies the determining-domain direction (T2).

**The equivalence under review (P0-WEIL-CORE §4).** Q_H := {m/n > 0 : 1 ≤ m,n ≤ H,
gcd(m,n)=1}; ⋃_H Q_H = ℚ₊. M_H := the two-moment-nullspace compression of the ambient Weil
matrix on the Q_H dilate family. Claimed: **RH ⟺ M_H ⪰ 0 for every H**, with
*Forward* = imported Weil positivity restricted; *Converse* = positivity on 𝒟_ℚ (all finite
rational-scale moment-null combinations) + core density (T3) + form continuity (T1) extending
to 𝓗¹_{a,0}, then T2 (Burnol) giving RH.

---

## 3. V1 — the Γ strip-cyclicity proof, decomposed into reviewable steps

**Theorem (T3 core statement).** For ½ < a < 1:
closure_{𝓗¹_a} span{ H_q : q ∈ ℚ₊ } = 𝓗¹_a.

The proof (P0-WEIL-CORE §2, incorporating the MIG-030 repair) decomposes into eight steps.
Each is a separate review item; the internal verification log (packet §5) records the
symbolic/numeric checks performed.

- **S1 (orthogonality setup).** F ∈ X := 𝓗¹_a orthogonal to every H_q, q ∈ ℚ₊.
- **S2 (extension to all q > 0).** "Continuity in q extends this to every q > 0."
  *Review:* requires q ↦ H_q continuous in the 𝓗¹_a **norm** (the weight is only
  quasi-invariant under translation; see §9-W1).
- **S3 (Laplace identity).** With u = eᵗ, weight W(u) = u^{−2a} (u<1), u^{2a} (u>1):
  0 = q^{−1/2}⟨F,H_q⟩_X = ∫₀^∞ e^{−qu}[W(F+Ḟ) − qWuḞ] du. Internally verified numerically to
  13–24 digits at q ∈ {0.5, 1, 2.3} for a test F; symbolic derivation is a review item
  (§9-W2).
- **S4 (Laplace-primitive lemma — the MIG-030 repair).** The *earlier draft* integrated by
  parts and asserted vanishing boundary terms; for arbitrary F ∈ 𝓗¹_a, Ḟ is only L² and
  C(u) = WuḞ need not have a pointwise trace at u = 0 — a real proof-presentation gap,
  internally found and repaired. The repair: weighted Cauchy–Schwarz gives A := W(F+Ḟ) and C
  ∈ L¹(0,1) (tail integral 1/(2(1−a)) finite **iff a < 1**), integrable at ∞ after e^{−qu};
  define D(u) := ∫₀ᵘ A, then Fubini gives ℒ(D) = ℒ(A)/q = ℒ(C); **Laplace injectivity** gives
  C = D a.e., so C has an absolutely continuous representative with C(0) = 0 and C′ = A —
  boundary behavior *derived, not assumed*.
- **S5 (the ODE).** Back in t: (e^{2a|t|}F′)′ = e^{2a|t|}F distributionally. Note the weight's
  kink at t = 0 (u = 1) is interior to the u-domain (0,∞), so the equation holds across it.
- **S6 (root selection).** t < 0: roots a ± κ, κ = √(a²+1); X-membership keeps e^{(a+κ)t}
  only. t > 0: roots −a ± κ; X-membership keeps e^{(−a−κ)t} only.
- **S7 (junction conditions).** F ∈ H¹_loc ⟹ F continuous at 0 ⟹ C = D; no delta source in the
  distributional ODE ⟹ weighted flux e^{2a|t|}F′ continuous at 0, and the weight equals 1
  there ⟹ F′ continuous ⟹ (a+κ)C = −(a+κ)D. Together C = D = 0, F ≡ 0. ∎
- **S8 (non-applicability honesty).** Beurling–Domar fails for ω = e^{a|t|} (blocks only the
  generic Tauberian route; does **not** prove incompleteness). Borichev–Hedenmalm requires
  log ω = o(t) — exactly linear here, hence **inapplicable**; the earlier MIG-028 anchor to it
  is informative but non-load-bearing. The closure rests on S1–S7 alone.

**What V1 asks:** does S1–S7 constitute a correct, complete proof of the theorem as stated on
this exact space, for all ½ < a < 1?

---

## 4. V2(a) — T1 form continuity, decomposed

**Statement.** The imported Weil functional 𝔔_W extends to a continuous Hermitian form on
𝓗¹_{a,0} for ½ < a < 1.

- **C1 (convolution bound).** w(t) = e^{a|t|} is submultiplicative; for Φ = H ∗ K̃,
  e^{a|t|}|Φ(t)| ≤ ‖wH‖₂‖wK‖₂ and e^{a|t|}|Φ′(t)| ≤ min(‖wH′‖₂‖wK‖₂, ‖wH‖₂‖wK′‖₂)
  (differentiation under the integral — review item).
- **C2 (prime side).** The prime series is dominated by C‖H‖‖K‖ Σ_{n≥2} Λ(n)/n^{a+1/2},
  convergent because a + ½ > 1 (equivalently −ζ′/ζ(a+½) < ∞).
- **C3 (archimedean side).** The apparent t = 0 singularity is removable (numerator O(t) by
  the C¹ bound; 1 − e^{−2t} = O(t)); at ∞ the e^{−a|t|} decay gives integrability.
  *Review:* C3 must be checked against the **exact** archimedean term recorded in K0-W1
  (the ℰ normalization), not a paraphrase.

## 5. V2(b) — the moment-correction lemma and T2, decomposed

- **M1 (moment-correction lemma; proved internal).** L = (L₊,L₋) surjective with a
  two-element right inverse R inside 𝒟 = span{H_q}. If D is dense in X, then D ∩ ker L is
  dense in ker L: correct G by R·L(G), an O(ε) perturbation by continuity of L. This reduces
  the **constrained** core density (T3) to the **unconstrained** cyclicity of §3.
- **T2-forward (routine chain; each step a review item).** (1) C_c^∞ dense in 𝓗¹_a; (2) two
  compactly supported functions with moment vectors spanning ℂ²; (3) moment-correct mollified
  approximants; (4) hence C_c^∞ ∩ 𝓗¹_{a,0} dense in 𝓗¹_{a,0}; (5) T1 continuity extends Weil
  positivity from the compact-support subclass to the whole space.
- **T2-converse (the Burnol import — the crux).** Positivity on 𝓗¹_{a,0} includes positivity
  on C_c^∞(0,∞) ∩ 𝒲₀, and Burnol's compact-support form of Weil's criterion shows this
  subclass already detects any off-critical zero — *provided* his counterexample test function
  can be chosen with both Mellin values zero (inside 𝒲₀) and, in log-coordinates, inside
  𝓗¹_{a,0}. **This provision is the single most important import-verification item in the
  entire packet** (§9-W6).
- **Composition.** Forward: imported Weil positivity ⟹ every M_H ⪰ 0 (compression). Converse:
  all M_H ⪰ 0 ⟹ positivity on 𝒟_ℚ ⟹ (T3 density + T1 continuity) positivity on 𝓗¹_{a,0} ⟹
  (T2) RH. *Review:* the compression step — that M_H ⪰ 0 is exactly positivity of the ambient
  form on span{H_q : q ∈ Q_H} ∩ ker L — is recorded in K0-W1 §7 (M_N = V_N* H_N V_N) and must
  be checked once against the engine's actual construction.

**What V2 asks:** do (a) and (b) hold as stated, and is the composed equivalence
RH ⟺ {M_H ⪰ 0 ∀H} therefore established **as a conditional equivalence built on the declared
imports** (never as an internal RH result)?

---

## 6. V3 — the five canon overlay gates (verbatim force, prior findings, disposition)

The five claims sit in `NFC_SCC_Branch.tex` §"SCC-RH Kernel Positivity Equivalence" (the
pre-K0 bespoke route). Verbatim canon text is reproduced in Annex A of this packet's source
section (the .tex lines 1872–2010). Their machine records:

| claim | tag | force | prior internal finding (2026-07-03 adjudication, `metadata/overlay.json`) |
|---|---|---|---|
| `def:rh-kernel` | D | definitional | **K0:** F declared as difference kernel K(t,u)=F(t−u) but used downstream as spectral multiplier; displayed zero-sum sign error; ρ ↔ 1−ρ̄ partners cancel exactly; "~" regularization undefined |
| `prop:rh-kernel-positivity` | C | conditional | **K0 D1–D3:** (D1) proof asserts "negative bump" for σ>½ but the leading minus makes it positive; (D2) functional-equation partners cancel exactly — the displayed sum is structurally blind to off-critical pairs regardless of RH; (D3) positive-definite functions may take negative values (cos t), so the pointwise-bump inference is invalid under the declared difference-kernel reading |
| `def:scc-admissible-probes` | D | definitional | **F4:** SCC-M3 (f(qx)=f(x) ∀q∈ℚ^×) + SCC-M4 (f ∈ L²(dx/x)) jointly force f = 0 a.e. — **the probe space is trivial as written** |
| `thm:scc-rh-equivalence` | C | conditional | inherits D1–D3; **D4 (Mellin–Plancherel domain error):** the Gaussian-exclusion argument is false — ψ_γ = e^{−(τ−γ)²} IS the Mellin transform of f_γ(x) = (1/(2√π))x^{−iγ}e^{−(log x)²/4} ∈ L²(dx/x) (verified); Gaussians fail only SCC-M3 as written; SCC-M2 undecidable until formalized; restriction-only converse gap |
| `rem:scc-rh-governance` | R | remark | repeats the unestablished "establishes" claim and the wrong Gaussian exclusion |

**Standing disposition (prohibition 13 / Phase-3 Rules 4–5):** the bespoke texts are preserved
— never deleted — and are to enter superseded-intake status only through individually
migration-gated canon edits, none yet authorized. The `[C]` tags remain formally intact as
conditional statements; what is gated is their **usable force**.

**What V3 asks:** (i) confirm or refute each recorded defect D1–D4 and the F4 triviality
finding against the exact canon text; (ii) rule on whether any bespoke repair is viable
(K0-5) or whether supersession-as-intake with the Weil re-anchor (K0-6, the current plan) is
the correct disposition; (iii) rule on whether the five claims' current tags + gating
correctly represent their epistemic status pending canon edit.

---

## 7. Relation to the computational ladder (what is and is not at stake)

Certified: integer-scale Q₃–Q₁₂ (K0-W2) and rational-height H = 2 … 10 (K0-W3, MIG-032 …
MIG-047), each a flint-free exact-rational residual/Weyl certificate with adversarial
self-verification (20 permanent tampers) and full provenance binding. These are **valid
finite slices regardless of this review's outcome** — but their *meaning* as slices of an
exact equivalence stands or falls with V1+V2:

- V1 or V2 **fails** ⟹ the equivalence claim reverts to "suggestive finite slices"; the
  packets' §4 consequence sections and prohibition-18 language must be rewritten; no canon
  change (the equivalence never entered canon).
- V1+V2 **pass** ⟹ the equivalence may be described as an externally reviewed scaffold result
  (still conditional, still built on imports, still not RH evidence — prohibition 18 is
  permanent); canon entry remains separately migration-gated.
- V3 rulings determine the canon disposition of the five gated claims either way.

---

## 8. Falsification targets (consolidated)

Inherited, still live:
- **W1-F1.** A proof that {q^{−1/2}H₀(·+log q)} is *incomplete* in 𝓗¹_a settles V1 negatively
  (f₀ must be replaced or the family enlarged). Note: Beurling–Domar failure does **not**
  supply this.
- **W1-F2.** If completeness provably cannot hold for ω = e^{a|t|} at any ½ < a < 1, the
  weighted-Sobolev model is the wrong completion and the form-domain choice reopens (K0-3).
- **K0-F3.** If the Γ-span density input (|Γ(½+iτ)| ≍ e^{−π|τ|/2} decay) fails for the
  actually chosen weighting, Lemma K0.A's applicability voids.

New, specific to this packet:
- **F-S2.** Exhibit F ∈ 𝓗¹_a and q_n → q with ⟨F,H_{q_n}⟩ = 0 but ⟨F,H_q⟩ ≠ 0 — i.e. break
  the S2 extension — or prove q ↦ H_q is *not* norm-continuous.
- **F-S4.** Exhibit F ∈ 𝓗¹_a with A ∉ L¹(0,1) or with the Fubini interchange failing at some
  q > 0 (would break the Laplace-primitive lemma's hypotheses).
- **F-T2.** Show Burnol's detecting test functions cannot simultaneously satisfy the two
  moment conditions and 𝓗¹_{a,0} membership for any ½ < a < 1 (would break the converse and
  revive a determining-domain gap — old W1-F3, currently retired).
- **F-C3.** Show the exact K0-W1 archimedean term ℰ has a non-removable singularity or
  insufficient decay against the C¹ bound (would break T1 as applied to the imported form).

---

## 9. Candidate weak points (assembler's self-audit — flagged, not adjudicated)

Identified while assembling this packet; each is a concrete question for the reviewer, in
rough order of concern:

- **W6 (T2-converse import).** The claim that Burnol's off-critical-detecting test function
  can be chosen inside 𝒲₀ **and** inside 𝓗¹_{a,0} is asserted with a parenthetical
  ("can be chosen with Mellin values zero at both 0 and 1 … and, being smooth and compactly
  supported in log-coordinates, inside 𝓗¹_{a,0}"). Smooth compact support in log-coordinates
  does give 𝓗¹_a membership trivially; the load-bearing part is the **moment-zero choice
  within Burnol's construction while preserving detection** — this must be verified against
  the actual paper, not the paraphrase.
- **W1 (S2 extension).** Norm-continuity of q ↦ H_q in 𝓗¹_a is used but not proved in the
  packet. Expected to hold (translation continuity plus quasi-invariance, dominated
  convergence on both weighted norms), but it is a missing lemma, not a triviality — the
  weight's quasi-invariance constant e^{a|log q|} blows up as q → 0, ∞, and continuity *at
  each fixed q* is what is needed.
- **W2 (S3 symbolic derivation).** The Laplace identity was verified numerically (13–24
  digits, three q values, one test F). The symbolic derivation — including why no boundary
  terms arise in the t → u change of variables for general F ∈ 𝓗¹_a — is exactly the kind of
  step the MIG-030 repair already caught a gap in once. It deserves a line-by-line check.
- **W3 (S5/S7 distributional bookkeeping).** The ODE is derived in u on (0,∞) and translated
  back to t; the junction conditions at t = 0 (u = 1) come from "no delta source." The
  reviewer should confirm the derivation yields the ODE distributionally **across** u = 1
  (the weight kink), so that the no-delta claim is a consequence, not an assumption.
- **W4 (K0-W1 §7 compression fidelity).** The equivalence's finite side assumes M_H as
  serialized equals the compressed ambient form exactly (basis, ordering, both moment
  constraints). The engine asserts and the validator checks the moment identities; the
  *formal* identification (M_N = V_N* H_N V_N as forms) should be reviewed once against the
  engine's construction.
- **W5 (a-range bookkeeping).** Three different constraints pin ½ < a < 1 (moment
  continuity, prime summability, H₀ membership / tail integral). The proofs use both
  endpoints in different places; the reviewer should confirm no step silently requires a
  closed endpoint.
- **W7 (prop:rh-kernel-positivity's "standard" proof).** For V3: beyond D1–D3, the
  displayed zero sum in `def:rh-kernel` is not absolutely convergent and no summation order
  is declared — even the *statement* needs the K0-2 regularization before any repair
  discussion is meaningful. (Consistent with the recorded adjudication; listed for
  completeness.)

None of these is asserted as a defect; W1–W5 look repairable-or-fine on their face. They are
where an adversarial reviewer should push first.

---

## 10. Reviewer verdict forms

For each verdict, the requested ruling vocabulary is: **CONFIRMED** (holds as stated) /
**CONFIRMED-WITH-REPAIRS** (holds after specified, bounded repairs — list them) /
**REFUTED** (a specified step fails; give the counterexample or gap) /
**NOT-DECIDABLE-AS-POSED** (statement or domain must be re-declared first — say what is
missing).

**V1 — Γ strip-cyclicity.**
```
Verdict: ______
Steps checked (S1–S8, each: pass/fail/repair): ______
If repairs: exact statements to add/change: ______
If refuted: failing step + witness: ______
a-range confirmed (½,1) open: yes/no: ______
Reviewer, date, method (line-by-line / independent reproof / counterexample search): ______
```

**V2 — Continuity / form-core passage and the composed equivalence.**
```
Verdict T1 (C1–C3): ______        Verdict M1: ______
Verdict T2-forward (steps 1–5): ______
Verdict T2-converse (Burnol import; W6 explicitly addressed): ______
Verdict composition (incl. W4 compression fidelity): ______
Overall V2: ______
Notes / required repairs / witnesses: ______
Reviewer, date, method: ______
```

**V3 — RH/SCC overlay gates.**
```
D1 confirmed/refuted: ______   D2: ______   D3: ______   D4: ______   F4 (trivial probe space): ______
Disposition ruling: bespoke repair viable (K0-5) / supersede-as-intake with Weil re-anchor (K0-6) / other: ______
Tag+gating adequacy for the five claims as they stand: adequate / must change (specify): ______
Reviewer, date, method: ______
```

---

## 11. Scope, prohibitions, and what this packet is NOT

- No new Q_H generation; no H=11 work (authorized but deferred by the MIG-047 verifier's
  recommendation).
- No canon `.tex`, census, or status change; no canon-status promotion of any kind.
- No RH claim in any direction; prohibitions 18–19 and the finite-test classification are
  restated above verbatim in substance and remain load-bearing.
- No merger with, or pre-emption of, the independent Weil-core/SCC specialist track — this
  packet is the *input* to that track.
- The packet asserts no new mathematics: every technical statement above is quoted or
  faithfully condensed from the documents of record (`RESEARCH_PACKET_RH_K0.md`,
  `_K0_WEIL.md`, `_K0_W2.md`, `_K0_W3.md`, `_P0.md`, `_P0_W1.md`, `_P0_WEIL_CORE.md`,
  `NFC_SCC_Branch.tex`, `metadata/overlay.json`), with §9 clearly marked as the assembler's
  non-adjudicated flags.

## 12. Path authorization note (governance)

The MIG-047 verification recommended this packet but did not enumerate authorized repository
paths (unlike every prior migration). Per the MIG-044 precedent (an unauthorized ninth path
was a formal defect), **no repository file was created or modified**: baseline `cbed4bb`
remains clean, and this packet is delivered outside the repo. If the packet is accepted as
MIG-048, the natural authorized-path set would be:

1. `REVIEW_PACKET_ANALYTIC_CORE.md` (this document, committed) — new;
2. `migrations/MIGRATIONS.md` — MIG-048 record;
3. `UNRESOLVED_REVIEW_ITEMS.md` — mark the specialist-review task as "packet assembled,
   review pending" with the three verdict IDs;
4. `metadata/overlay.json` — optionally add `review_packet: MIG-048` back-references on the
   five gated claims (no status change);
5. `release/TRACKED_TEXT_MANIFEST.txt` — only if (1) is committed.

Alternatively the packet can remain delivery-only. That decision is the verifier's.

**Resolution (MIG-048 authorization, 2026-07-09):** the packet was assembled and delivered
strictly outside the repository at clean baseline `cbed4bb` (as recorded above), then accepted
and explicitly authorized for commit under this five-path set. This file is that commit; the
delivery-only assembly provenance stands as the record of how it was produced. The commit
changes no canon text, no status or proof force, no certificate, and no engine/validator/
harness file, and asserts no external review of V1, V2, or V3 — those verdicts remain the
next work.

---
*Assembled at baseline `cbed4bb` (60 commits, tag `716e6fa` intact, tree clean). Certified
heights at assembly: H = 2 … 10. Generator hash unchanged since MIG-044:
`cbacd87aca74a5ee92ab03d58796943df1d392c6ec7806b903d782224ba43752`.*

---

## Annex A — verbatim canon text of the five overlay gates
(`NFC_SCC_Branch.tex`, §"SCC-RH Kernel Positivity Equivalence", lines 1872–2010 at `cbed4bb`;
reproduced unmodified for reviewer convenience)

```latex
\section{SCC-RH Kernel Positivity Equivalence}
\label{sec:scc-rh-kernel}
%% ---------------------------------------------------------------

This section formalizes the most structurally original NFC
contribution to the Riemann Hypothesis program: the equivalence
$\mathrm{RH} \Longleftrightarrow$ kernel positivity under
SCC-admissible probes. Source: NFC-RH 496pp §RH-Q14--Q19.

\begin{definition}[\status{D}]\label{def:rh-kernel}
\textup{(RH Kernel $K(t,u)$.)}
Define the \emph{RH kernel} by $K(t,u) := F(t-u)$ where
\[
 F(\tau) \;\sim\; -\mathrm{Re}\!\left(\frac{\zeta'}{\zeta}
 \!\left(\tfrac{1}{2}+i\tau\right)\right)
 \;=\; -\sum_\rho \mathrm{Re}\!\left(
 \frac{\tfrac{1}{2}-\sigma_\rho}{(\tfrac{1}{2}-\sigma_\rho)^2
 + (\tau-\gamma_\rho)^2}\right),
\]
where the sum is over nontrivial zeros $\rho = \sigma_\rho +
i\gamma_\rho$ of $\zeta$.
\end{definition}

\begin{proposition}[\status{C}]\label{prop:rh-kernel-positivity}
\textup{(RH Kernel Positivity Analysis.)}
Each nontrivial zero $\rho = \sigma + i\gamma$ contributes to
$F(\tau)$ near $\tau = \gamma$ as follows:
\begin{itemize}
 \item $\sigma = \tfrac{1}{2}$: contribution $= 0$ (critical-line
 zeros have no effect on kernel positivity);
 \item $\sigma \neq \tfrac{1}{2}$: localized positive/negative bump
 (negative near $\tau = \gamma$ if $\sigma > \tfrac{1}{2}$).
\end{itemize}
Therefore: $K(t,u)$ is positive-definite if and only if all
nontrivial zeros of $\zeta$ lie on the critical line.
\end{proposition}

\begin{proof}
Standard: the term $(\tfrac{1}{2}-\sigma)/[(\tfrac{1}{2}-\sigma)^2
+ (\tau-\gamma)^2]$ has the sign of $\tfrac{1}{2}-\sigma$.
For $\sigma = \tfrac{1}{2}$: numerator vanishes.
For $\sigma > \tfrac{1}{2}$: numerator is negative, contributing
a negative bump to $F(\tau)$ near $\tau = \gamma$, which
destroys positive-definiteness.
Hence positive-definiteness of $K$ is equivalent to $\sigma_\rho
= \tfrac{1}{2}$ for all $\rho$, i.e., RH. \qed
\end{proof}

\begin{definition}[\status{D}]\label{def:scc-admissible-probes}
\textup{(SCC-Admissible Probe Space; SCC-M1 through SCC-M4.)}
A probe function $\psi : \mathbb{R} \to \mathbb{C}$ is
\emph{SCC-admissible} if it is of the form
\[
 \psi(\tau) \;=\; \int_0^\infty f(x)\, x^{i\tau}\, \frac{dx}{x}
\]
(a Mellin transform) where $f : \mathbb{R}_+ \to \mathbb{C}$
satisfies all four conditions:
\begin{enumerate}[label=\textup{(SCC-M\arabic*)}]
 \item $\psi$ arises as a Mellin transform of a declared $f$
 (arithmetic scaling structure);
 \item $f$ is compatible with multiplicative convolution:
 stable under $x \mapsto x/n$ for $n \in \mathbb{N}$
 (analogous to SCC transport stability);
 \item $f$ descends to the $\mathbb{Q}^\times$-quotient:
 $f(qx) = f(x)$ for all $q \in \mathbb{Q}^\times$
 (arithmetic admissibility);
 \item $f \in L^2(\mathbb{R}_+, dx/x)$ (square-integrability
 with respect to the Haar measure on $\mathbb{R}_+^\times$).
\end{enumerate}
\end{definition}

\begin{theorem}[\status{C}]\label{thm:scc-rh-equivalence}
\textup{(SCC-RH Admissibility Theorem.)}
\textup{[Conditional on the SCC-admissible probe definition and the
RH kernel positivity analysis.]}
Under SCC-admissible probes (Def.~\ref{def:scc-admissible-probes}):
\[
 \mathrm{RH}
 \;\Longleftrightarrow\;
 K(t,u) \text{ is positive-definite}
 \;\Longleftrightarrow\;
 \forall\,\text{SCC-admissible } \psi:\;
 Q[\psi] \;:=\; \int F(\tau)|\psi(\tau)|^2\,d\tau \;\geq\; 0.
\]
Furthermore, Gaussian probes $\psi(\tau) = e^{-(\tau-\gamma)^2}$
are \emph{not} SCC-admissible (they fail SCC-M2, SCC-M3, and
SCC-M4), so the standard localize-near-a-zero approach is
excluded from the probe space.
\end{theorem}

\begin{proof}
The first equivalence is Proposition~\ref{prop:rh-kernel-positivity}:
positive-definiteness of $K$ is equivalent to RH.

The second equivalence follows from the definition of
positive-definiteness as $Q[\psi] \geq 0$ for all test functions
$\psi$ in the declared probe class; restricting to
SCC-admissible probes gives the stated form.

Gaussian exclusion: $\psi(\tau) = e^{-(\tau-\gamma)^2}$ is not
a Mellin transform of any $f \in L^2(\mathbb{R}_+, dx/x)$ (it
fails SCC-M4 since $\int |e^{-(\tau-\gamma)^2}|^2 d\tau$ requires
a frequency-domain representation not compatible with the Haar
measure structure). It also fails SCC-M2 (no multiplicative
convolution stability for Gaussians) and SCC-M3 (Gaussians are
not $\mathbb{Q}^\times$-invariant). \qed
\end{proof}

\begin{remark}[\status{R}]\label{rem:scc-rh-governance}
\textbf{Governance note: admissibility constraint vs.\ proof of RH.}
Theorem~\ref{thm:scc-rh-equivalence} establishes that RH is
equivalent to non-negativity of $Q[\psi]$ for all SCC-admissible
probes. This is an \emph{admissibility constraint}, not a
proof of RH. The SCC machinery establishes:
\begin{itemize}
 \item What would count as a counterexample to RH: a
 SCC-admissible probe with $Q[\psi] < 0$;
 \item What the witness assembly obligation (S1) must produce:
 a SCC-admissible probe family $\mathcal{W}_{\mathrm{RH}}$
 that certifies positivity or detects failure.
\end{itemize}
The NFC-specific contribution is the SCC-admissibility constraint
(SCC-M1 through SCC-M4), which restricts the probe space to
arithmetically structured functions and excludes artificial
localization probes. Attribution: the reformulation RH
$\Leftrightarrow$ kernel positivity is related to Li's criterion
(Li~1997), de Bruijn--Newman, and related work; the SCC-M1
through SCC-M4 restriction is the NFC contribution.

\textbf{RH-Q20 resolution (canonical):} SCC yields an
admissibility constraint, not a proof. Using SCC to force
RH would require proving that no SCC-admissible probe gives
$Q[\psi] < 0$ --- which is equivalent to RH itself.
The equivalence is genuine; the proof of RH within NFC would
consist of constructing such a witness family (S1) and
verifying $Q[\psi] \geq 0$ for all members.
\end{remark}

\section{Named Failure Frontier}
```
