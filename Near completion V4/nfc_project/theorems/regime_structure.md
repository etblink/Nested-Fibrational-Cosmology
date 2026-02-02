# Regimes and Defect-Mediated Interaction
## NFC Corpus — Part IV

**Status:** Proven | **Dependencies:** Survivor-Stabilizer, PASS | **Scope:** Structural

---

## IV.1 The Multiple-Survivor Problem

At the conclusion of survivor-stabilizer analysis, the framework admits:
- One or more survivors may exist within a finite relational neighborhood
- Each survivor is individually invariant under all admissible extensions
- Survivor status is local, contextual, finite, and revisable

**Nothing yet constrains interactions among distinct survivors.**

### The Unresolved Question

> If more than one survivor exists in a finite relational system, under what conditions can those survivors coexist without inducing collapse under admissible extension?

This is a question of **internal consistency**, not interpretation.

---

## IV.2 Impossibility of Symmetric Survivor Coexistence

### IV.2.1 Exact Mutual Invariance

Suppose two distinct survivors $C_1$ and $C_2$ coexist. One might require **mutual invariance**: admissible extensions preserve both survivors jointly, and interactions do not introduce new observational distinctions.

### Theorem IV.2.1 (Symmetric Coexistence Collapse)

**Exact symmetric coexistence of distinct survivors is structurally impossible.**

**Proof**:

Survivors persist only by virtue of stabilizers. For two survivors to be symmetrically invariant:

**Case 1: Shared stabilizers**
- Shared stabilizers collapse $C_1$ and $C_2$ into single compression class
- Violates identity no-go (reintroduces identity-like sameness)

**Case 2: Distinct but commuting stabilizers**
- Commuting stabilizers preserve cross-survivor indistinguishability
- Again induces global sameness under extension
- Violates identity no-go

**Case 3: Stabilizers enforcing mutual invariance**
- Active enforcement of sameness across survivors
- Constitutes enforcement rather than permission
- Reintroduces collapse via trivialization or fragmentation

In all cases, exact symmetric coexistence forces re-identification or restriction of admissible extension. Both are forbidden. ∎

### Conclusion

Exact symmetry among survivors is **incompatible with non-collapse**.

---

## IV.3 Why Coexistence Is Not Forbidden

### Lemma IV.3.1 (Survivor Non-Uniqueness)

The framework does **not** force global uniqueness of survivors.

**Proof**: Survivors are defined locally relative to:
- Admissible observers
- Admissible extensions
- Stabilizer availability

Nothing forbids multiple distinct stabilizer-supported compression classes within same relational neighborhood. ∎

Thus: coexistence is possible in principle, but only if interaction avoids symmetric collapse modes.

---

## IV.4 Necessity of Asymmetric Interaction

### Theorem IV.4.1 (Forced Asymmetry)

If more than one survivor exists in a finite relational system, any admissible interaction among them must be **asymmetric**.

**Proof**:

Let $C_1$, $C_2$ be distinct survivors.

- **Complete isolation**: Renders coexistence vacuous (survivors indistinguishable from independent systems)
- **Symmetric interaction**: Collapses by Theorem IV.2.1

Therefore, if survivors coexist non-trivially, interaction must:
- Not enforce mutual invariance
- Not share stabilizers
- Not permit reciprocal refinement blocking

Such interaction must be **directional, non-reciprocal, or otherwise asymmetric**. ∎

**Asymmetry is not introduced as principle. It is the only remaining admissible form.**

---

## IV.5 Defects as the Only Admissible Interaction Currency

### IV.5.1 Why Direct Interaction Fails

Any relation that directly modifies stabilizers of a survivor:
- Alters conditions guaranteeing persistence
- Destabilizes survivor status
- Therefore collapses persistence itself

Admissible interaction must satisfy:
- ❌ No modification of stabilizer families
- ❌ No introduction of new invariant structure
- ❌ No backreaction into survivor-defining relations

### IV.5.2 Definition of Defect

**Definition IV.5.1 (Defect)**

A **defect** is a relational structure that:
1. Couples halo variation to backbone constraints
2. Does not itself belong to backbone
3. Cannot accumulate or propagate without bound

**Defects are defined negatively** by what they do not do, not by success in mediating coexistence.

### Theorem IV.5.2 (Defect Mediation Necessity)

Any stable interaction among survivors must be **defect-mediated**.

**Proof**:

Let $r$ mediate interaction between survivors.

- If $r$ modifies stabilizers → survivor persistence collapses
- If $r$ introduces new invariant structure → identity-like sameness reintroduced
- If $r$ enforces reciprocity → symmetric coexistence collapse

Only remaining admissible relations:
- Modify admissible paths without stabilizer alteration
- Introduce bounded, non-amplifying deviation
- Commute asymmetrically with admissible extension

These are exactly **defects**. ∎

---

## IV.6 PASS as Consequence of Survivor Coexistence

### Theorem IV.6.1 (PASS from Coexistence)

Once multiple survivors coexist via defect-mediated asymmetric interaction:
- Exact symmetry is obstructed
- Bounded approximate symmetry is **unavoidable and protected**

**Proof**:

Defect-mediated interaction necessarily introduces deviation from exact invariance. However:
- Stabilizers forbid defect accumulation
- Admissible extension bounds defect influence
- Asymmetric mediation prevents reciprocal amplification

Therefore:
- Symmetry cannot be exact
- Deviation cannot grow unbounded
- Approximate invariance persists structurally

This is precisely **protected approximate symmetry**. ∎

**Significance**: PASS is **not an independent postulate**. It is the only stable residue of symmetry once multiple survivors coexist.

---

## IV.7 Regimes as Joint Survivor Fixed Points

### IV.7.1 Joint Extension Behavior

Once survivors interact defect-mediatedly, admissible extensions act on **configurations of survivors**, not individuals.

**New question**: Under admissible extension, which joint survivor configurations remain observationally indistinguishable?

### IV.7.2 Definition of Regime

**Definition IV.7.1 (Regime)**

A **regime** is a joint configuration of survivors such that:

1. **Joint extension invariance**: For every admissible extension $E$, all configurations reachable via $E$ remain observationally indistinguishable

2. **Defect tolerance**: Defect-mediated interactions may occur but do not refine joint configuration into distinguishable alternatives

3. **No admissible refinement**: No admissible extension splits joint configuration into two observationally distinguishable joint survivor configurations

**No appeal to**: Time, persistence through repetition, equilibrium, or semantic interpretation.

### IV.7.3 Regimes Are Not Assumed

**Critical**: Regimes are:
- ❌ Not postulated
- ❌ Not automatic from survivor existence
- ❌ Not guaranteed

A system may admit survivors yet admit **no regimes**, if joint configurations are extension-sensitive.

Regimes exist **if and only if** certain joint stability conditions are met.

---

## IV.8 Finite Regime Alphabet Theorem

### Theorem IV.8.1 (Finite Regime Alphabet)

In any finite relational system admitting survivor coexistence via defect-mediated interaction, the number of regimes is **finite**.

**Proof**:
1. Finitely many survivors (Theorem III.4.3)
2. Finitely many admissible joint survivor configurations
3. Defect mediation introduces only bounded, finite variation
4. Finite observers induce finite compression classes over joint configurations
5. Only compression classes invariant under all admissible extensions qualify as regimes

Therefore: finite number of regimes. ∎

This blocks:
- Infinite regime landscapes
- Continuous phase spaces
- Unbounded novelty at collective level

---

## IV.9 Closure of Part IV

At this point:
- ✅ Symmetric coexistence is impossible
- ✅ Coexistence requires asymmetric, defect-mediated interaction
- ✅ PASS is rederived as consequence, not assumption
- ✅ Regimes are joint stable configurations (conditionally)
- ✅ Regime alphabet is finite

**Next**: Probability, law, and classicality as compression limits (Part V).

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No symmetric interaction assumed | ✅ Pass |
| Defects defined structurally | ✅ Pass |
| PASS rederived, not assumed | ✅ Pass |
| Regimes conditional, not automatic | ✅ Pass |
| Finiteness preserved | ✅ Pass |

**Audit Result:** ✅ Clean

---

## References

- Survivor-Stabilizer: `theorems/survivor_stabilizer.md`
- Probability as Compression: `theorems/probability_compression.md` (next)
- Derivability Ledger: `audit/derivability_ledger.md`
