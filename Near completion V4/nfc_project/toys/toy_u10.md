# Toy Universe 𝕌₁₀: Witness Depth and Resolution Budget
## Extended Toy with Intermediate Witness Layer

**Status:** Existence proof extended | **Type:** Illustrative | **Dependencies:** 𝕌₈

---

## Preamble: What 𝕌₁₀ Adds to 𝕌₈

**𝕌₈ established:**
- Quantum-like multiplicity (W_f distinguishes h₀, h₁)
- Coherent pocket (sub-gap defects don't cause public branching)
- Classical fixed point (W_c collapses everything)

**𝕌₁₀ introduces:**
- **Intermediate witness W_m**: Creates refinement chain W_c ≺ W_m ≺ W_f
- **Witness depth k**: Minimal level to separate configurations
- **Resolution budget k_eff**: How defect accumulation degrades accessible depth
- **Explicit threshold crossing**: When 𝔇/γ² forces loss of refinement level

This makes the "quantum-to-classical transition" structurally explicit.

---

## A. Carry Over 𝕌₈ (Unchanged)

### Incidence Sites
$$\mathcal{I} = \{a, b, c, d\}$$

### Relation Tokens (8 total — same as 𝕌₈)

**Backbone (level 0):**
- $b_1 := (\{a\}, \{b\})$
- $b_2 := (\{b\}, \{c\})$
- $b_3 := (\{c\}, \{d\})$

**Halo (level 1):**
- $h_0 := (\{a\}, \{d\})$
- $h_1 := (\{a\}, \{d\})$ (distinct token)
- $\delta^{(1)} := (\{b\}, \{b\})$ (sub-gap)
- $\delta^{(2)} := (\{c\}, \{c\})$ (super-gap)
- $w := (\{d\}, \{d\})$ (witness context)

### Composition, Stratification, PASS Split

Identical to 𝕌₈. See `toys/toy_u8.md` Section B–D.

---

## B. New: Defect-Tainted Paths

### Path Classification

An **extension-path** from stabilized situation S is a finite admissible continuation where defect tokens may occur.

Define predicate on paths:
- **Clean**: Path contains no $\delta^{(2)}$
- **Tainted**: Path contains at least one $\delta^{(2)}$

**Structural license**: "Leakage events" = "defect registered by at least one witness."

---

## C. Three Witnesses: Refinement Chain W_c ≺ W_m ≺ W_f

### Coarse Witness W_c

**Output alphabet:** $\{C\}$

**Rule:** Reports only projected base pattern
$$W_c(h_0) = W_c(h_1) = C$$

Always identifies h₀ and h₁.

### Fine Witness W_f

**Output alphabet:** $\{0, 1\}$

**Rule:** Separates token-level distinctions
$$W_f(h_0, \text{any path}) = 0$$
$$W_f(h_1, \text{any path}) = 1$$

Always distinguishes h₀ from h₁.

### NEW: Medium Witness W_m

**Output alphabet:** $\{A, B\}$

**Rule (asymmetric as proposed):**
- $W_m(h_0, \text{clean}) = A$
- $W_m(h_1, \text{clean}) = A$ (cannot separate in clean pocket)
- $W_m(\_, \text{tainted}) = B$ (any taint collapses to "defect-marked")

**Key property:** W_m distinguishes "defect-tainted vs not" but does NOT fully resolve token identity like W_f.

---

## D. Refinement Chain Verification

Define "≺" (coarser than): $W' \prec W$ if $x \equiv_W y \Rightarrow x \equiv_{W'} y$

**Verify W_c ≺ W_m:**
- Under W_c: everything → C (single class)
- Under W_m: clean → A, tainted → B (two classes)
- If W_m identifies them (both A or both B), W_c certainly does
- ✅ W_c ≺ W_m

**Verify W_m ≺ W_f:**
- Under W_f: h₀ → 0, h₁ → 1 (always distinct)
- Under W_m: clean → both A (identified); tainted → both B (identified)
- If W_f identifies them, W_m does (but not conversely)
- ✅ W_m ≺ W_f

**Chain confirmed:** $W_c \prec W_m \prec W_f$

---

## E. Witness Depth k(h₀, h₁)

### Definition

Index witnesses by refinement level:
- Level 0: W_c
- Level 1: W_m
- Level 2: W_f

Define:
$$k(h_0, h_1) := \min\{\ell : h_0 \not\equiv_{W_\ell} h_1\}$$

### Compute k in Different Regimes

**Coherent pocket (no taint):**
- Under W_c: both → C, so $h_0 \equiv_{W_c} h_1$
- Under W_m: both clean → A, so $h_0 \equiv_{W_m} h_1$
- Under W_f: 0 vs 1, so $h_0 \not\equiv_{W_f} h_1$
- **k(h₀, h₁) = 2** (needs finest layer)

**After super-gap defect activity (tainted paths):**
- Under W_c: everything → C (still identified)
- Under W_m: tainted → B for both (still identified at token level)
- But: W_m can no longer distinguish clean vs tainted for each token separately
- **Effective separation is degraded**

**Key insight:** k can "jump" or become effectively inaccessible depending on defect budget.

---

## F. Link to Gap/Defect Control: Resolution Budget k_eff

### Defect Functional (from canon)

$$\mathfrak{D} = \frac{\kappa^2}{\gamma} \int_0^T \delta(t)^2 dt$$

**Toy interpretation:** "Extension depth" T = number of admissible extension steps.

### Saturating Heuristic for k_eff

Define **effective available refinement depth**:
$$k_{\text{eff}}(\mathfrak{D}) = k_{\max} \cdot \max\left(0, \ 1 - c \cdot \frac{\mathfrak{D}}{\gamma^2}\right)$$

Where:
- $k_{\max} = 2$ (maximum witness depth in this toy)
- $c$ = saturation constant (application-layer parameter)
- $\gamma = 2$ (gap threshold)

### Behavior

| Regime | 𝔇/γ² | k_eff | Interpretation |
|--------|------|-------|----------------|
| Clean pocket | ≪ 1 | ≈ 2 | Fine distinctions accessible ("quantum-like") |
| Threshold crossing | ≈ 1/c | ≈ 1 | Medium witness dominates |
| High defect budget | ≫ 1/c | ≈ 0 | Only coarse invariants remain ("classical") |

**This gives a soft "action-like" scale**: "How much defect budget buys one lost refinement level?"

---

## G. What 𝕌₁₀ Demonstrates

| Feature | Mechanism | Status |
|---------|-----------|--------|
| Refinement chain W_c ≺ W_m ≺ W_f | Explicit witness rules | ✅ Existence |
| Witness depth k(h₀, h₁) = 2 in clean pocket | Definition + computation | ✅ Existence |
| k can jump with defect budget | Taint predicate | ✅ Existence |
| Resolution budget k_eff(𝔇) | Saturating heuristic | ⚠️ Application-layer |
| Classical fixed point under W_c | Same as 𝕌₈ | ✅ Existence |

---

## H. Explicit Limitations

### What 𝕌₁₀ Does NOT Prove

| Claim | Status | Why |
|-------|--------|-----|
| "k_eff formula is forced" | ❌ FALSE | Saturating form is heuristic choice |
| "c = 1 is necessary" | ❌ FALSE | Application-layer parameter |
| "All NFC systems have 3 witness levels" | ❌ FALSE | This toy has 3; others may differ |
| "γ = 2 is physical" | ❌ FALSE | Illustrative parameter |

### What Would Strengthen 𝕌₁₀

1. **Derive k_eff form** from primitive constraints (not heuristic)
2. **Prove threshold behavior** is generic across witness families
3. **Multiple taint grades** for finer degradation
4. **Formal connection** to decoherence timescales in physical systems

---

## I. Forward License to 𝕌₁₂

𝕌₁₀ licenses adding:
- **Defect composition rules**: $\delta^{(2)} \circ \delta^{(1)}$ admissible
- **Quadratic drift**: Weighted defect functional
- **Threshold lemma**: "When 𝔇 > Θ, k_eff drops by at least 1"

This makes the "economics" of resolution loss sharp.

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No time primitive | ✅ Pass (extension depth only) |
| No dynamics | ✅ Pass |
| k_eff heuristic explicit | ✅ Pass (flagged as application-layer) |
| Witness chain structural | ✅ Pass |
| PASS respected | ✅ Pass |

**Audit Result:** ✅ Clean (with explicit heuristic flag)

---

## References

- 𝕌₈: `toys/toy_u8.md`
- 𝕌₁₂ (next): `toys/toy_u12.md`
- Global Flow: `theorems/global_flow_completion.md`
