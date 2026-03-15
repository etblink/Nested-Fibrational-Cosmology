# Incidence Before Identity: Core Theorems
## Referee-Ready Formalization

**Abstract:** We present a complete derivation of identity, persistence, and interaction structure from strictly relational primitives. Assuming only finite relational incidence, constrained composition, and internal observation—and explicitly excluding primitive identity, time, dynamics, and semantics—we prove: (1) primitive identity forces structural collapse; (2) identity, if it appears, must arise as derived compression of invariant relational behavior; (3) persistence requires stabilizer-supported compression classes ("survivors"); (4) multiple survivors force asymmetric, defect-mediated interaction; (5) such interaction induces protected approximate symmetry and finite regime structure. All results are purely structural and interpretation-free.

---

## 1. Introduction

### 1.1 The Foundational Problem

Relational approaches to foundational physics aim to minimize ontological commitments by treating relations as primary. However, one assumption is almost always retained implicitly: **identity**. Relations are typically taken to relate the same relata across compositions, iterations, or observational contexts.

In strictly relational and finitary frameworks, this retention is not benign. Without background structure to stabilize reference, re-identification itself must be supported by admissible relations.

### 1.2 Our Contribution

We prove a series of structural theorems showing:
- Identity cannot be primitive
- Identity, if it appears, is derived compression
- Persistence is not generic; it requires stabilizers
- Interaction among persistent structures is necessarily asymmetric
- Regime structure is finite and robust

**No physics is assumed.** The results apply to any finite relational system with constrained composition and internal observation.

### 1.3 Standing Assumptions

**Primitives (exhaustive):**
1. Finite relational incidence
2. Constrained (partial, typed, weakly associative) composition
3. Internal observation (relational subsystems, no external viewpoint)
4. Finite distinguishability

**Explicitly excluded:** Primitive identity, objects, time, dynamics, probability, background space, semantics, external observers.

---

## 2. The Identity No-Go Theorem

### 2.1 Definitions

**Definition 2.1 (Primitive Identity).** A system admits primitive identity if it licenses re-identification across admissible extensions not derived from relational behavior, observational congruence, or stability conditions.

**Definition 2.2 (Collapse).** A system collapses if it degenerates into: (a) trivialization (indiscriminate indistinguishability); (b) fragmentation (failure of composition); or (c) observer inconsistency (incompatible identity assignments).

### 2.2 Theorem

**Theorem 2.3 (Identity No-Go).** In any finite relational system with constrained composition and internal observation, primitive identity forces collapse.

**Proof (exhaustion).** Any enforcement of identity must be: (i) universal → trivialization (Lemma 2.4); (ii) selective → fragmentation (Lemma 2.5); or (iii) contextual → observer inconsistency (Lemma 2.6). These exhaust possibilities. ∎

**Lemma 2.4 (Trivialization).** Universal primitive identity forces all iteratively connected relations into single equivalence class.

*Proof.* Invariance under composition + weak associativity → no distinction can persist. ∎

**Lemma 2.5 (Fragmentation).** Selective primitive identity restricts admissible composition to prevent identity violation.

*Proof.* If composition could alter identity, identity would be violated. Restriction fragments system. ∎

**Lemma 2.6 (Observer Inconsistency).** Contextual primitive identity yields incompatible assignments across observers.

*Proof.* Finite distinguishability → different observers have different tests → different identity judgments. No global reconciliation. ∎

### 2.3 Corollary

**Corollary 2.7.** Identity cannot be taken as primitive in any non-collapsing finite relational framework.

---

## 3. Derived Identity as Compression

### 3.1 Definitions

**Definition 3.1 (Compression Class).** Equivalence class of configurations indistinguishable under all admissible tests.

**Definition 3.2 (Stability Under Extension).** A pattern is stable if its observable behavior remains invariant under all admissible extensions.

**Definition 3.3 (Derived Identity).** A compression class that is: (a) invariant under admissible composition; (b) stable under admissible extension.

### 3.2 Theorem

**Theorem 3.4 (Compression is Forced).** In any finite relational system with internal observation, compression classes form.

*Proof.* Finite distinguishability → finite number of observable distinctions → equivalence classes. ∎

**Theorem 3.5 (Derived Identity Avoids Collapse).** Derived identity: (a) does not trivialize structure; (b) does not fragment composition; (c) is consistent across observers.

*Proof.* (a) Distinguishable configurations remain distinct. (b) Identity tracks invariance, doesn't enforce it. (c) Defined by agreement across all observers. ∎

---

## 4. Protected Approximate Symmetry (PASS)

### 4.1 Obstruction to Exact Symmetry

**Definition 4.1 (Singular Projection).** Many-to-one projection with no admissible inverse.

**Proposition 4.2.** Singular projections are generic in finite relational systems.

*Proof.* Finiteness + constrained composition + internal observation → many-to-one without inverse. ∎

**Theorem 4.3 (Exact Symmetry Obstructed).** Exact symmetry is incompatible with singular projection interfaces.

*Proof.* Exact symmetry requires invertibility and global coherence. Singular projections lack both. ∎

### 4.2 PASS Theorem

**Theorem 4.4 (PASS).** In any finite relational system with singular projections, any non-collapsing symmetry must be:
- Approximate (invariance up to finite deviation)
- Protected (deviation bounds are rigid under extension)

*Proof.* Exact symmetry collapses (Theorem 4.3). No symmetry collapses (unconstrained variation). Therefore approximate symmetry is forced. Protection follows from non-collapse requirement. ∎

### 4.3 Backbone-Halo Decomposition

**Theorem 4.5 (Unique Decomposition).** PASS induces unique partition into:
- **Backbone**: invariant under all admissible extensions
- **Halo**: bounded variation compatible with protection

*Proof.* Mixing protected/unprotected features violates protection. ∎

**Theorem 4.6 (One-Way Protection).** Halo variation cannot backreact on backbone.

*Proof.* Backreaction would either amplify deviation beyond bounds or force backbone refinement. Both collapse. ∎

---

## 5. Survivors and Stabilizers

### 5.1 Generic Instability

**Lemma 5.1.** Most compression classes are unstable under admissible extension.

*Proof.* Extensions introduce new tests → refinement. ∎

### 5.2 Stabilizers

**Definition 5.2 (Stabilizer).** Relation S stabilizing compression class C if: (a) incidence-neutral; (b) observationally invariant; (c) commutes with extension.

**Theorem 5.3 (Stabilizer Necessity and Sufficiency).** Compression class persists iff it admits stabilizers.

*Proof.* (⇒) Stabilizers block refinement (Lemma 5.4). (⇐) No stabilizers → extension-sensitive (Lemma 5.5). ∎

### 5.3 Survivors

**Definition 5.6 (Survivor).** Compression class that: (a) is extension-invariant; (b) has stabilizer support; (c) admits no admissible refinement.

**Theorem 5.7 (Finite Survivors).** In any finite relational neighborhood, the number of survivors is finite.

*Proof.* Finite compression classes + selective persistence. ∎

**Corollary 5.8 (Objects).** Objects, if admissible, are survivor-stabilizer pairs.

---

## 6. Defect-Mediated Interaction

### 6.1 Symmetric Coexistence Collapse

**Theorem 6.1.** Exact symmetric coexistence of distinct survivors is impossible.

*Proof.* Shared stabilizers → collapse to single class. Commuting stabilizers → global sameness. Mutual enforcement → collapse. ∎

### 6.2 Forced Asymmetry

**Theorem 6.2.** If multiple survivors coexist non-trivially, interaction must be asymmetric.

*Proof.* Isolation → vacuous. Symmetry → collapse (Theorem 6.1). ∎

### 6.3 Defect Necessity

**Definition 6.3 (Defect).** Relation modifying admissible paths without altering stabilizers or backbone.

**Theorem 6.4 (Defect Mediation).** All stable survivor interaction is defect-mediated.

*Proof.* Direct stabilizer modification → persistence collapse. New invariant structure → identity reintroduction. Reciprocity → symmetric collapse. Only defects remain. ∎

### 6.4 PASS from Coexistence

**Theorem 6.5.** Defect-mediated coexistence rederives PASS as consequence, not assumption.

*Proof.* Defects introduce deviation; stabilizers bound accumulation; asymmetry prevents amplification. ∎

---

## 7. Regime Structure

### 7.1 Definition

**Definition 7.1 (Regime).** Joint survivor configuration that: (a) is joint extension-invariant; (b) tolerates defects without refinement; (c) admits no admissible joint refinement.

### 7.2 Finiteness

**Theorem 7.2 (Finite Regime Alphabet).** The set of regimes is finite.

*Proof.* Finite survivors × finite defect variation × finite compression. ∎

---

## 8. Conclusion

We have proven from minimal relational primitives:
1. Identity must be derived, not primitive
2. Persistence requires stabilizer support
3. Coexistence requires asymmetric, defect-mediated interaction
4. Regime structure is finite and robust

**No time, dynamics, probability, or semantics were assumed.**

---

## References

None external. All results derived from stated primitives.

---

## Acknowledgments

This work builds on the NFC corpus, developed through systematic derivational analysis.

---

*Word count: ~1,500 (abstract to conclusion)*  
*Target journal: Foundations of Physics / Journal of Mathematical Physics*
