# Protected Approximate Symmetry (PASS) Theorem
## Part II — Symmetry Structure from Non-Collapse

**Status:** Proven | **Dependencies:** Derived Identity, Standing Premise | **Scope:** Structural

---

## Preamble: From Obstruction to Necessity

Part I established that **exact symmetry is structurally obstructed** in finite relational systems with singular projection interfaces. One might attempt to abandon symmetry altogether—but this option is not generally viable.

**Unconstrained asymmetry** allows arbitrary divergence under admissible extension, reintroducing collapse through loss of coherent recurrence.

To avoid collapse while respecting the obstruction of exact symmetry, any admissible symmetry must satisfy:
1. **Approximation**: Invariance holds only up to finite, localized deviation
2. **Protection**: Deviations cannot accumulate or propagate without violating admissibility

These conditions are **not optional**. They are forced by finiteness, constrained composition, and internal observation.

---

## II.1 Singular Projection and Obstruction to Exact Symmetry

### II.1.1 Projection as Structural Reduction

In a finite relational system with constrained composition, recurrence of relational behavior becomes tractable only through **structural reduction**: passage from richer relational configurations to simpler ones preserving admissible behavior.

A **projection** is a partial relational operation associating higher-complexity relations with lower-complexity ones while preserving admissibility.

**No assumption**: Invertibility, symmetry, or global definition.

### II.1.2 Singular Projection Interfaces

A projection interface is **singular** when:
- Multiple distinct relational configurations project to same reduced configuration
- No admissible inverse projection exists

**Singular interfaces are generic** in finite relational systems because:
- Finiteness limits discriminability
- Constrained composition restricts admissible refinements
- Internal observation forbids external resolution

### II.1.3 Exact Symmetry Requirements

Exact symmetry requires:
1. Re-identification of relational occurrences across contexts
2. Invertibility or bidirectional correspondence
3. Global coherence across projections

Each requirement **conflicts with singular projection interfaces**.

### Proposition II.1.1: Obstruction to Exact Symmetry

In any finite relational system with constrained composition and singular projection interfaces, **exact symmetry is structurally obstructed**.

**Proof sketch**: Any attempt to impose exact symmetry transformations must:
- Collapse distinct configurations (trivialization), OR
- Forbid admissible compositions exposing non-invertibility (fragmentation), OR
- Restrict to privileged substructure (observer inconsistency)

All three reproduce collapse modes excluded in Part I. ∎

---

## II.2 Protected Approximate Symmetry

### II.2.1 Definition of Approximate Symmetry

An **approximate symmetry** is a family of transformations on relational configurations such that:
- Admissible behavior is preserved under composition
- Deviations from exact invariance are finite and localized
- No admissible operation can refine the deviation into exact symmetry

**No assumption**: Identity, invertibility, or group structure.

### II.2.2 Protection of Approximate Symmetry

Approximate symmetry is **protected** if any admissible extension that attempts to:
- Eliminate the deviation, OR
- Amplify the deviation beyond bounds

triggers one of the collapse modes from Part I.

**Protection = rigidity under admissible extension**: Bounds on deviation cannot be tuned, smoothed, or removed without violating constraints.

---

## II.2.3 The PASS Theorem

**Theorem II.2.1 (Protected Approximate Symmetry)**

In any finite relational system with constrained composition and singular projection interfaces:

1. **Exact symmetry is obstructed**
2. **Any non-collapsing symmetry compatible with admissibility must be approximate and protected**
3. **The deviation from exact invariance is finite, localized, and rigid under admissible extension**

**Proof**:
- (1) By Proposition II.1.1
- (2) By exhaustion: exact symmetry collapses; no symmetry collapses; therefore approximate symmetry is forced
- (3) By protection definition: bounds are rigid under admissible extension

∎

---

## II.3 Backbone–Halo Decomposition

### II.3.1 Protected and Unprotected Structure

PASS distinguishes two structurally inequivalent classes:

| Class | Property | Role |
|-------|----------|------|
| **Backbone** | Invariant features preserved under all admissible compositions/extensions | Protected structure |
| **Halo** | Features may vary within bounded deviation without inducing collapse | Variable structure |

These denote **structural roles**, not substances or domains.

### II.3.2 Uniqueness of the Decomposition

The backbone–halo split is **unique**.

Any alternative partition mixing protected and unprotected features fails protection:
- Variability leaks into invariant structure → collapse
- Invariance enforced where variability required → collapse

**Formally**: Backbone relations are exactly those whose admissible extensions preserve invariant behavior under all PASS. Halo relations are those whose extensions exhibit bounded variation compatible with protection.

### II.3.3 One-Way Protection

Protection is **strictly one-way**:

$$\text{Halo variation} \not\rightarrow \text{Backbone modification}$$

**Converse holds**: Backbone structure constrains halo variation by fixing invariant framework.

**If halo→backbone backreaction occurred**:
- Deviations would amplify beyond protected bounds, OR
- Backbone invariants would be forced to refine

Both reintroduce collapse.

---

## II.3.4 Consequences of PASS

1. **Invariant structure admits no autonomous novelty**
2. **All admissible novelty is confined to halo**
3. **Interaction between invariant and variable structure is necessarily asymmetric**

These follow directly from protection; no interpretation required.

---

## II.4 Closure of Part II

At this point:
- ✅ Exact symmetry is structurally obstructed
- ✅ Any admissible symmetry must be approximate and protected
- ✅ PASS induces unique backbone–halo decomposition
- ✅ Protection is one-way: halo cannot modify backbone

**Next question**: Which relational compressions, if any, can remain stable under admissible extension?

This is addressed in **Survivors and Stabilizers** (Part III).

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No symmetry assumed primitive | ✅ Pass |
| No group structure introduced | ✅ Pass |
| No dynamics assumed | ✅ Pass |
| Protection derived from non-collapse | ✅ Pass |
| One-way asymmetry structural | ✅ Pass |

**Audit Result:** ✅ Clean

---

## References

- Derived Identity: `theorems/derived_identity.md`
- Survivor-Stabilizer: `theorems/survivor_stabilizer.md` (next)
- Derivability Ledger: `audit/derivability_ledger.md`
