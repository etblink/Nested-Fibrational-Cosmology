# Standing Premise (Canonical Form)
## NFC Core Document — Version 2.0

**Status:** Frozen (no modifications without version bump)  
**Scope:** Binding for all NFC derivations  
**Dependencies:** None (foundational)

---

## Statement

> A purely relational system avoids collapse only through constrained composition. Typed composability, weak associativity, and iterative closure permit potential invariance but do not guarantee the emergence of identity-like structure. For persistence to be recognizable rather than merely extant, additional observational constraints are required: behavioral congruence and—within any framework admitting finitary distinguishability—finite distinguishability under admissible relational tests.

---

## Explication of Terms

### 1. Purely Relational System

A system consisting exclusively of:
- **Relations**: Primitive tokens without internal structure, labels, or intrinsic properties
- **Incidence**: Primitive compositional adjacency (when relations can compose)

No objects, carriers, states, or background spaces are assumed.

### 2. Constrained Composition

Composition is a **partial operation**:
$$\circ : \mathcal{R} \times \mathcal{R} \rightharpoonup \mathcal{R}$$

**Typed composability**: Whether $r' \circ r$ is defined depends only on structural roles internal to the system, not on assumed identity of relata.

**Weak associativity**: Associativity holds locally where both parenthesizations are admissible, but is not globally enforced.

**Iterative closure**: When composition is admissible, its output is eligible for further admissible composition.

### 3. Collapse (Structural)

A relational system collapses if it degenerates into:
1. **Trivialization**: Indiscriminate composability or indiscriminate indistinguishability
2. **Vacuity**: Failure of nontrivial admissible composition
3. **Unresolvable refinement**: Continual refinement preventing stable compression classes

### 4. Finite Distinguishability

Within any admissible observational context, only finitely many observationally distinct behavioral congruence classes exist.

Equivalently: No admissible observer can resolve infinitely many distinct outcomes in a single finite context.

### 5. Behavioral Congruence

Two relational configurations are behaviorally congruent (relative to specified admissible observational context) if no admissible observation distinguishes them.

**Critical distinction**: Congruence $\neq$ identity. Congruence records indistinguishability; identity would require re-identification across contexts.

---

## What the Standing Premise Licenses

From this premise alone, we may speak of:

1. Relations and their finite multiplicity
2. Composition and its constraints
3. Observers as internal relational processes
4. Indistinguishability under finite tests

---

## What the Standing Premise Does NOT License

The following are **explicitly not contained** in the standing premise:

- Identity relations or equality predicates
- Object carriers or substrates
- Global state spaces
- Time or persistence
- Probability or measures
- Truth values or semantics
- External viewpoints

If any of these appear later, their derivation must be shown explicitly.

---

## Minimal Ontology (Exhaustive)

The only admissible ontological commitments:

1. **Relations** (as primitive tokens)
2. **Constrained composition** (partial, typed, weakly associative)
3. **Internal observation** (relational subsystems subject to same constraints)

---

## Explicit Prohibitions (Binding)

No argument, definition, or theorem may rely—explicitly or implicitly—on:

| Prohibition | Rationale |
|-------------|-----------|
| Primitive objects or relata | Would smuggle identity |
| Primitive identity or re-identification | Violates IBI no-go |
| Temporal ordering or dynamics | Not primitive; must be derived |
| Background space, geometry, topology | Would assume structure |
| Probability, randomness, measures | Must emerge as compression frequency |
| Semantic interpretation, truth, meaning | Outside structural scope |
| Agency, intention, external observers | Would violate internal constraint |

---

## Derivability Condition

> No structure may be used, named, or compressed into a normal form unless its generating conditions have been explicitly derived.

This condition is **normative** for all subsequent sections.

---

## Version History

- **v1.0**: Initial statement (IBI paper)
- **v2.0**: Refined for NFC corpus; added explicit prohibitions and minimal ontology

---

## Audit Checkpoint

This document collapses if:
- Any primitive beyond (relations, constrained composition, internal observation) is smuggled
- Finiteness is assumed globally rather than locally
- "Admissible" is given semantic content beyond structural permission

**Status:** ✅ Audit passed
