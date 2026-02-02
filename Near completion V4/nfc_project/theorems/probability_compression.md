# Probability as Compression Frequency
## Part V — Compression Limits (With Explicit Status Flags)

**Status:** ⚠️ Partial — Structural definition licensed, quantitative behavior not fully derived | **Dependencies:** Regimes, irreversible compression | **Scope:** Structural with interpretive boundary

---

## ⚠️ Critical Preamble: Status of This Result

This section derives a **structural analogue** of probability within NFC. It does **not** derive quantum probability, the Born rule, or physical stochastic behavior.

| Claim | Status | Clarification |
|-------|--------|---------------|
| "A probability-like structure emerges" | ✅ Licensed | Compression frequency is structurally forced |
| "This is quantum probability" | ❌ NOT proven | Would require additional structure |
| "Born rule is derived" | ❌ NOT proven | Requires interpretive mapping |
| "Randomness is explained" | ❌ NOT claimed | NFC uses counting, not chance |

**This is structural counting modulo indistinguishability, not physical probability theory.**

---

## V.1 Defect-Mediated Multiplicity of Continuations

### V.1.1 The Setting

Given a regime $R$, admissible extension does **not** determine a unique continuation. Instead:
- Multiple defect-mediated continuation paths may be admissible
- Distinct paths may collapse back into same regime under observational indistinguishability
- Observers cannot track path-level distinctions indefinitely

Thus: even with finite regime alphabet, space of admissible continuations is **combinatorially rich**.

### V.1.2 Observational Indistinguishability of Paths

**Lemma V.1.1 (Path Collapse)**

Distinct admissible continuation paths that terminate in same regime are observationally indistinguishable under all admissible witnesses.

**Proof**: Regimes are joint compression classes invariant under admissible extension. By definition, no admissible observer can distinguish configurations within same regime. Therefore path distinctions not altering terminal regime are observationally inaccessible. ∎

Observers must describe outcomes in terms of **regimes, not paths**.

---

## V.2 Compression Frequency: Definition

### V.2.1 Structural Definition

**Definition V.2.1 (Compression Frequency)**

Let $R_i$ be a regime. The **compression frequency** of $R_i$ is:

> The proportion of admissible, observationally indistinguishable continuation paths that terminate in $R_i$, relative to total number of admissible paths indistinguishable under all witnesses.

**Key features**:
- ❌ No randomness assumed
- ❌ No probability measure introduced
- ✅ Only finite counting of admissible continuations

Compression frequency is **structural ratio**, not chance assignment.

---

## V.3 Probability Emergence Theorem

### Theorem V.3.1 (Probability Without Randomness)

Any internal observer who:
- Tracks regimes under admissible extension
- Cannot resolve path-level distinctions
- Observes repeated admissible continuations

**must** describe outcomes using compression frequencies.

**Proof**:

Observers have access only to regime-level reports. When multiple indistinguishable paths collapse into same regime, relative frequencies of regime appearance are **only invariant descriptors** of outcome distribution available.

No further structure is accessible. ∎

### Corollary V.3.2 (Public Character)

Compression frequencies are **invariant across all admissible observers**.

**Proof**: All admissible observers subject to same finite distinguishability and witness constraints. Indistinguishability classes are public. Counting admissible paths modulo indistinguishability yields observer-independent ratios. ∎

---

## V.4 What Has Been Derived (And What Has Not)

### ✅ What IS Derived

| Result | Status |
|--------|--------|
| Compression frequency is structurally forced | ✅ Proven |
| Compression frequency is observer-invariant | ✅ Proven |
| Compression frequency uses only counting | ✅ Proven |

### ⚠️ What Is NOT Derived

| Claim | Status | Gap |
|-------|--------|-----|
| Compression frequencies sum to 1 | ⚠️ Requires normalization convention | Application-layer |
| Compression frequencies satisfy Kolmogorov axioms | ⚠️ Requires measure structure | Not in NFC |
| Compression frequencies match quantum probabilities | ❌ NOT proven | Would require Hilbert space |
| Interference patterns emerge | ⚠️ Partial (non-commutativity) | Toy examples only |

---

## V.5 The Gap to Physical Probability

### Structural vs. Physical Probability

| Aspect | NFC Compression Frequency | Physical Probability |
|--------|---------------------------|---------------------|
| Foundation | Finite counting | Measure theory |
| Randomness | None assumed | Usually assumed |
| Normalization | Conventional | Required (sums to 1) |
| Interference | Non-commutativity hint | Complex amplitudes |
| Prediction | Structural tendency | Quantitative forecasts |

### What Would Bridge the Gap

To derive physical probability from NFC would require:
1. **Quantitative measure**: Assigning consistent weights to paths (not just counting)
2. **Interference structure**: Showing non-commutativity yields amplitude-like behavior
3. **Born rule**: Deriving $|\psi|^2$ from compression structure
4. **Empirical validation**: Matching observed frequencies

These are **open problems**, not solved in NFC.

---

## V.6 Honest Assessment

### What NFC Achieves

NFC shows that **any finite relational system with regimes and compression** must admit a probability-like description based on counting indistinguishable paths. This is:
- **Structural**: Follows from primitives
- **Universal**: Applies to all such systems
- **Interpretation-free**: No physics assumed

### What NFC Does Not Achieve

NFC does **not** show that:
- Physical systems are finite relational systems
- Quantum mechanics is the only NFC-compatible theory
- The Born rule is structurally necessary
- Probability is "explained" in full physical sense

---

## V.7 Forward License

This section licenses:
- Using compression frequency as structural analogue of probability
- Investigating quantitative behavior in toy examples
- Exploring mappings to physical probability theories

This section does **not** license:
- Claiming quantum probability is derived
- Asserting Born rule follows from NFC
- Using probability claims to test NFC empirically (without additional structure)

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No probability primitive | ✅ Pass |
| Only counting used | ✅ Pass |
| Randomness not assumed | ✅ Pass |
| Structural definition explicit | ✅ Pass |
| Physical claims flagged | ✅ Pass |

**Audit Result:** ✅ Clean (with explicit limitation flags)

---

## References

- Regime Structure: `theorems/regime_structure.md`
- Law as Compression-Stable Transformer: `theorems/law_transformer.md` (next)
- Application Mapping: `applications/mapping_guidelines.md`
