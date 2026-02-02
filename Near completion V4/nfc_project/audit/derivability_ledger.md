# Derivability Ledger (Normative)
## NFC Dependency Graph and Audit Trail

**Status:** Living document | **Authority:** Binding for all NFC derivations | **Version:** 2.0

---

## Ledger Principle

> No structure may be used, named, or compressed into a normal form unless its generating conditions have been explicitly derived.

This ledger records, in globally auditable form, which structures are licensed at each stage. **Absence from derivation is not prohibition; it is non-licensing.**

---

## Primitive Inventory (Exhaustive)

The **only** primitives used across the full NFC corpus:

| # | Primitive | Meaning | First Licensed |
|---|-----------|---------|----------------|
| P1 | Finite relational incidence | Relations involve finitely many sites | Standing Premise |
| P2 | Constrained composition | Partial, typed, weakly associative | Standing Premise |
| P3 | Internal observation | Relational subsystems, no external viewpoint | Standing Premise |
| P4 | Finite distinguishability | Only finitely many distinctions per context | Standing Premise |

**Nothing else is primitive.**

---

## Derived Structure Dependency Graph

```
P1, P2, P3, P4 (Standing Premise)
│
├── IBI-1: Identity No-Go Theorem
│   └── Derived: Primitive identity causes collapse
│
├── IBI-2: Derived Identity as Compression
│   └── Requires: Finite distinguishability + stability under extension
│
├── PASS: Protected Approximate Symmetry
│   └── Requires: Singular projection + non-collapse requirement
│       └── Derived: Backbone-halo decomposition (one-way protection)
│
├── SURVIVOR: Survivor-Stabilizer Classification
│   └── Requires: Compression + admissible extension
│       └── Derived: Persistence requires stabilizers
│       └── Derived: Objects = survivor-stabilizer pairs
│       └── Derived: Finite number of survivors
│
├── REGIME: Regime Structure
│   └── Requires: Multiple survivors + defect-mediated interaction
│       └── Derived: Finite regime alphabet
│       └── Derived: Asymmetric interaction forced
│
├── PROB: Probability as Compression Frequency
│   └── Requires: Regimes + irreversible compression
│       └── ⚠️ Status: Existence demonstrated, quantitative behavior not derived
│
├── LAW: Law as Compression-Stable Transformer
│   └── Requires: Regimes + witness invariance
│       └── ⚠️ Status: Structural definition licensed, physical mapping interpretive
│
├── CLASSICAL: Classicality as Coarse Invariance
│   └── Requires: PASS + compression dominance
│       └── ⚠️ Status: Coarse fixed points proven, "classical physics" interpretive
│
└── GLOBAL: 9th Coordinate (Additive Lift)
    └── Requires: Non-functoriality + R1–R4 regularity
        └── ⚠️ Status: Lift proven given regularity; regularity assumed not derived
```

---

## Complete Dependency Table

### Part I: Incidence Before Identity

| Result | Depends On | Does NOT Depend On | Status |
|--------|------------|-------------------|--------|
| Identity No-Go (Thm I.3.1) | P1–P4 | PASS, survivors, time | ✅ Proven |
| Derived Identity (Def I.4.3) | No-Go + finite distinguishability | Dynamics, semantics | ✅ Proven |
| Compression forced (Lem I.4.1) | P1–P4 | Stability conditions | ✅ Proven |

### Part II: Protected Approximate Symmetry

| Result | Depends On | Does NOT Depend On | Status |
|--------|------------|-------------------|--------|
| PASS Theorem (Thm II.2.1) | Singular projection + non-collapse | Survivors, time, dynamics | ✅ Proven |
| Backbone-halo split (Thm II.3.2) | PASS | Objects, identity | ✅ Proven |
| One-way protection (Lem II.3.3) | PASS | Dynamics, causality | ✅ Proven |

### Part III: Survivors and Stabilizers

| Result | Depends On | Does NOT Depend On | Status |
|--------|------------|-------------------|--------|
| Stabilizer necessity (Thm III.2.1) | Compression + extension | PASS, time | ✅ Proven |
| Survivor definition (Def III.3.1) | Stabilizers + invariance | Identity, persistence | ✅ Proven |
| Finite survivors (Thm III.3.1) | Finiteness + stabilizers | Global finiteness | ✅ Proven |
| Object corollary (Cor III.3.2) | Survivor-stabilizer pairs | Object primitives | ✅ Proven |

### Part IV: Regimes and Interaction

| Result | Depends On | Does NOT Depend On | Status |
|--------|------------|-------------------|--------|
| Symmetric coexistence collapse (Thm IV.1.1) | IBI + survivors | PASS (used for proof, not assumed) | ✅ Proven |
| Defect necessity (Thm IV.2.1) | Survivors + admissibility | Dynamics, forces | ✅ Proven |
| Finite regime alphabet (Thm IV.3.1) | Finiteness + defects | Probability, time | ✅ Proven |
| PASS from coexistence (Thm IV.4.1) | Defects + survivors | Prior PASS assumption | ✅ Proven |

### Part V: Probability, Law, Classicality

| Result | Depends On | Does NOT Depend On | Status | Note |
|--------|------------|-------------------|--------|------|
| Compression frequency (Def V.1.2) | Regimes + defects | Randomness, measures | ✅ Licensed | Structural definition |
| Probability emergence (Thm V.1.3) | Compression frequency | Stochastic postulates | ⚠️ Partial | Existence, not uniqueness |
| Law definition (Def V.2.1) | Regimes + compression | Dynamics, equations | ✅ Licensed | Structural definition |
| Finite laws (Thm V.2.3) | Finite regimes | Tuning, selection | ✅ Proven | Structural result |
| Classical sector (Def V.3.2) | Regimes + witnesses | Measurement, time | ✅ Licensed | Structural definition |
| Classicality theorem (Thm V.3.4) | PASS + compression | Macroscopic realism | ⚠️ Partial | Coarse fixed points, not physics |

### Global Flow (9th Coordinate)

| Result | Depends On | Does NOT Depend On | Status | Note |
|--------|------------|-------------------|--------|------|
| Non-functoriality obstruction (Thm X.Y.1) | NF condition | Time, dynamics | ✅ Proven | Structural |
| Defect monoid (Def X.Y.3) | Non-closure | Physics content | ✅ Proven | Construction |
| Scalarization (Thm X.Y.9) | R1–R4 regularity | Physical necessity | ⚠️ Conditional | Given regularity |
| Minimal lift (Thm X.Y.10) | Scalarization | Extra dimensions | ✅ Proven | Given scalarization |
| Gauge freedom (Prop X.Y.8) | Additivity | Dynamics | ✅ Proven | Structural |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Structurally complete (proof valid, dependencies clean) |
| ⚠️ | Partial (existence or definition licensed, full derivation incomplete) |
| ❓ | Open (question remains, further work needed) |

---

## Non-Circularity Guarantee

No result in NFC depends on:
- ❌ Probability to derive regimes
- ❌ Regimes to derive survivor coexistence
- ❌ Laws to derive probability
- ❌ Classicality to derive regimes
- ❌ PASS as assumption for PASS rederivation

All dependencies flow **strictly forward**.

---

## How to Disagree With NFC

Any coherent objection must take one of these forms:

| Form | Example |
|------|---------|
| 1. Reject finiteness | "Infinite relations are physically necessary" |
| 2. Reject constrained admissibility | "All compositions should be allowed" |
| 3. Reject internal observation | "External observers are fundamental" |
| 4. Reject stabilizer-supported persistence | "Persistence requires no mechanism" |
| 5. Accept collapse | "The system should collapse" |

No other disagreement is structurally coherent within the framework.

---

## Application-Layer Boundary

The following are **explicitly interpretive** and marked as such:

| Mapping | Status |
|---------|--------|
| NFC "probability" → Physical probability (Born rule) | Interpretive |
| NFC "law" → Physical laws (equations of motion) | Interpretive |
| NFC "classicality" → Classical physics emergence | Interpretive |
| NFC "9th coordinate" → Cosmological time | Interpretive |
| NFC "defects" → Physical forces/interactions | Interpretive |

**Structural theorems do not require these mappings to hold.**

---

## Collapse-Gate Audit Summary

| Potential Smuggle | Status |
|-------------------|--------|
| Identity assumed primitive | ❌ No (proven impossible) |
| Time introduced | ❌ No (derived as monotone parameter only) |
| Objects presupposed | ❌ No (derived as survivor-stabilizer) |
| Probability primitive | ❌ No (derived as compression frequency) |
| Dynamics assumed | ❌ No (bookkeeping of compression order) |
| Semantics used | ❌ No (structural throughout) |
| External observers | ❌ No (internal only) |

**Overall Audit:** ✅ Clean (with explicit flags where claims exceed demonstration)

---

## Version History

- **v1.0**: Initial ledger (IBI paper)
- **v2.0**: Expanded for NFC corpus; added status flags and application-layer boundary

---

## Forward Work

1. Strengthen ⚠️ results to ✅ where possible
2. Clarify quantitative predictions for probability emergence
3. Develop explicit physical mapping guidelines
4. Explore alternative regularity conditions for 9th coordinate

---

*"The ledger does not introduce new assumptions; it enforces dependency discipline."*
