# Derived Identity as Compression
## Section I.4 — Incidence Before Identity

**Status:** Proven | **Dependencies:** Identity No-Go Theorem, Standing Premise | **Scope:** Structural

---

## Preamble: Why Identity Must Be Reintroduced

Section I.3 established that **primitive identity is incompatible with non-collapse**. However:

> The absence of primitive identity does not imply the impossibility of identity tout court. It implies only that identity, if it appears, can only be structural, derivative, and earned.

This section shows that a restricted notion of identity is not only admissible but **unavoidable** once additional constraints already licensed by the standing premise are taken into account.

---

## Key Insight

Identity may arise only as a **compression of invariant relational behavior** that is:
- Stable under admissible extension
- Finite in distinguishability
- Contextual and revisable

---

## Definitions

### Admissible Extension

An **admissible extension** of a relational configuration is any finite composition of relations permitted by the admissibility constraints of the system.

**No temporal interpretation**: "Extension" refers only to further relational composition.

### Stability Under Extension

A relational pattern is **stable under admissible extension** if, for all admissible extensions, its observable relational behavior remains invariant under all admissible observational tests.

This invokes only:
- Constrained composition (already licensed)
- Internal observation (already licensed)
- Finite distinguishability (already licensed)

### Observational Compression

Two relational configurations **compress to the same normal form** if no admissible observer can distinguish them under any admissible extension.

**Critical**: Compression is not an operation performed by an observer. It is a **structural equivalence induced by finite indistinguishability**.

---

## Lemma: Compression is Forced by Finiteness

**Lemma I.4.1 (Compression Admits No Alternative Under Finiteness)**

In any finite relational system admitting admissible extension and internal observation, the space of distinguishable relational behaviors is finite.

**Proof**:
- By finite distinguishability, each observer resolves only finitely many distinctions
- By local finiteness and admissible composition, only finitely many relational configurations are testable
- Therefore, equivalence classes under indistinguishability must form

**Significance**: Compression is not optional. It is forced by the structure. ∎

---

## Definition: Derived Identity

**Definition I.4.3 (Derived Identity)**

A **derived identity** is a compression class of relational configurations that:

1. Are observationally indistinguishable under all admissible tests
2. Remain indistinguishable under all admissible extensions

**Properties of derived identity**:
- **Not global**: Defined only relative to admissible observer class and extension rules
- **Not primitive**: Arises from compression, not assumed
- **Not eternal**: May be revised if admissibility constraints change
- **Finite**: Only finitely many identities in any finite relational neighborhood

**Identity is therefore nothing more than conditional stability**.

---

## Properties: Derived Identity Avoids Collapse

### Lemma I.4.4 (Non-Triviality)

Derived identity does not trivialize relational structure.

**Proof**: Only configurations indistinguishable under all admissible tests are identified. Distinguishable configurations remain distinct. ∎

### Lemma I.4.5 (Compatibility with Composition)

Derived identity does not fragment admissible composition.

**Proof**: Identity is defined after admissible composition and only over its stable outcomes. No restriction on composition is required to preserve identity; identity tracks invariance rather than enforcing it. ∎

### Lemma I.4.6 (Observer Consistency)

Derived identity is consistent across all internal observers.

**Proof**: Identity is defined by agreement across all admissible observers. Any observer incapable of resolving a distinction agrees with the compression. Any observer capable of resolving a distinction prevents identification. Thus no inconsistency arises. ∎

---

## Corollary: Objects Are Not Primitive

**Corollary I.4.7**

Objects, insofar as they rely on persistent identity, **cannot be primitive**. They arise only as stabilized compression classes of relational behavior.

This corollary is **structural, not metaphysical**.

---

## What This Section Does NOT Introduce

For referee clarity:

| Potential Addition | Status |
|-------------------|--------|
| Time | ❌ No |
| Memory | ❌ No |
| Dynamics | ❌ No |
| Probability | ❌ No |
| Semantics | ❌ No |
| Agents | ❌ No |
| Truth conditions | ❌ No |

Identity emerges solely from:
- Constrained composition
- Finite distinguishability
- Stability under extension

---

## Limits of Derived Identity

Derived identity does **not** license:

- Unrestricted re-identification across arbitrary extensions
- Temporal persistence (no time assumed)
- Global or absolute identity
- Identity as equivalence relation (see Appendix)

Additional structure is required for persistence. This is addressed in **Survivors and Stabilizers**.

---

## Transition to Part II

At this point we have established:

1. ✅ Primitive identity is impossible without collapse
2. ✅ Derived identity is unavoidable under extension stability
3. ✅ Identity is a compression artifact, not a primitive

**Remaining questions** (scope, not foundations):
- What further structures depend on derived identity?
- Which familiar notions require it?
- Which do not?

These are addressed in **Protected Approximate Symmetry** (Part II).

---

## Appendix: Derived Identity Is Not an Equivalence Relation

This appendix clarifies a potential confusion. Derived identity may appear similar to an equivalence relation, but differs fundamentally:

| Feature | Equivalence Relation | Derived Identity |
|---------|---------------------|------------------|
| Presupposes identity | Yes | No |
| Defined globally | Yes | No |
| Stable under extension | Yes | Only conditionally |
| Licenses quotients | Yes | No |
| Primitive | Often | Never |

**Key distinction**: Equivalence relations organize pre-existing identity; derived identity **generates** a weak notion of sameness from structural constraints.

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No primitive identity | ✅ Pass |
| No time assumed | ✅ Pass |
| No objects presupposed | ✅ Pass |
| No semantics | ✅ Pass |
| Only licensed structures used | ✅ Pass |

**Audit Result:** ✅ Clean

---

## References

- Standing Premise: `core/standing_premise.md`
- Identity No-Go: `theorems/identity_no_go.md`
- PASS Theorem: `theorems/pass_theorem.md` (next)
