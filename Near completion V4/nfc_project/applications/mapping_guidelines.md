# Application-Layer Mapping Guidelines
## Explicitly Interpretive — Not Part of NFC Core

**Status:** Guidelines only | **Scope:** Suggested mappings, not derivations | **Authority:** Application-layer (user discretion)

---

## ⚠️ Critical Preamble

This document provides **suggested interpretive mappings** between NFC structural concepts and physical/phenomenological notions. These mappings are:

- **Not derived** from NFC primitives
- **Not necessary** for NFC consistency
- **Not unique** — alternative mappings may be equally valid
- **Explicitly interpretive** — marked throughout

**Using these mappings does not make them structural theorems.**

---

## Mapping Philosophy

NFC provides **structural constraints** on what any finite relational system can support. Physical theories that violate these constraints are (within the NFC framework) **structurally impossible**.

However, NFC does not **force** any particular physical instantiation. Multiple physical theories may be compatible with NFC structure.

The mappings below are **consistency checks**, not derivations.

---

## Suggested Mappings

### 1. Relations → Physical Degrees of Freedom

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Relation token | Local degree of freedom at incidence site | Interpretive |
| Finite relational incidence | Finite-dimensional local state space | Interpretive |
| Constrained composition | Locality / selection rules for interaction | Interpretive |

**Consistency check**: Physical systems with infinite local degrees of freedom (QFT on continuum) may require approximation or regularization to fit NFC finiteness.

---

### 2. Compression → Coarse-Graining / Effective Theory

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Compression class | Equivalence class under coarse-graining | Interpretive |
| Irreversible compression | Loss of fine-grained information | Interpretive |
| Compression frequency | Relative weight in effective ensemble | Interpretive |

**Consistency check**: NFC "probability" as compression frequency is **structural counting**, not quantum probability. The Born rule requires additional structure not derived in NFC.

**Critical gap**: NFC shows that *a* probability-like structure emerges. It does not show that *quantum* probability (with interference, amplitudes, etc.) is forced.

---

### 3. Witnesses → Observers / Measurement Contexts

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Witness family | Set of compatible measurements | Interpretive |
| Fine witness | Complete measurement (maximal information) | Interpretive |
| Coarse witness | Incomplete / coarse-grained measurement | Interpretive |
| Witness gap | Energy / resolution threshold | Interpretive |

**Consistency check**: NFC witnesses are **structural tests**, not conscious observers. The mapping to quantum measurement requires additional interpretive steps.

---

### 4. Defects → Interactions / Perturbations

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Defect | Localized perturbation / interaction | Interpretive |
| Sub-gap defect | Below detection threshold | Interpretive |
| Super-gap defect | Above detection threshold | Interpretive |
| Defect-mediated interaction | Force carrier / exchange | Interpretive |

**Consistency check**: NFC defects modify admissible continuations without altering stabilizers. Physical forces should respect this "no backreaction on protected sector" constraint.

---

### 5. Stabilizers → Conservation Laws / Symmetries

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Stabilizer | Conservation law / symmetry generator | Interpretive |
| Incidence neutrality | Noether-like property | Interpretive |
| Extension commutation | Compatibility with dynamics | Interpretive |

**Consistency check**: NFC stabilizers are **incidence-neutral**, not group-theoretic symmetries. The mapping to Noether's theorem requires additional structure.

---

### 6. Survivors → Particles / Stable States

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Survivor | Stable particle / bound state | Interpretive |
| Survivor-stabilizer pair | Particle with conserved quantum numbers | Interpretive |
| Finite survivors | Finite particle spectrum | Interpretive |

**Consistency check**: NFC survivors are **contextual and revisable**, not eternal. Physical particles should exhibit similar context-dependence (e.g., environment-dependent stability).

---

### 7. Regimes → Phases / Vacuum States

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Regime | Thermodynamic phase / vacuum state | Interpretive |
| Regime alphabet | Phase diagram / vacuum landscape | Interpretive |
| Finite regime alphabet | Finite phase structure | Interpretive |

**Consistency check**: NFC regimes are **jointly stable survivor configurations**, not energy eigenstates. The mapping requires thermodynamic or energetic interpretation.

---

### 8. 9th Coordinate → Cosmological Time / Entropy

| NFC Concept | Suggested Physical Mapping | Status |
|-------------|---------------------------|--------|
| Additive coordinate $A(h)$ | Accumulated entropy / cosmological time | Interpretive |
| Monotone compression order | Thermodynamic arrow of time | Interpretive |
| Pure gauge character | Unobservable absolute time | Interpretive |

**Consistency check**: NFC "emergent time" is **monotone compression bookkeeping**, not physical duration. The mapping to cosmological time requires metric/geometry assumptions.

**Critical gap**: NFC does not derive the metric signature, dimensionality, or specific dynamics of spacetime.

---

## Mapping Validation Criteria

A proposed mapping is **structurally consistent** if:

1. **No primitive violation**: Mapped physical concept does not require prohibited primitives
2. **Dependency respect**: Mapped concept's dependencies match NFC dependencies
3. **Collapse avoidance**: Mapping does not reintroduce collapse modes
4. **Finiteness preservation**: Physical instantiation respects finite distinguishability

A mapping is **structurally forced** only if physical theory violates NFC constraints without it.

---

## Example: Quantum Mechanics Mapping

### What NFC Can Say (Structural)

- Multiple incompressible extension classes can persist under finite distinguishability
- Coarse witnesses can force compression to single public class
- Non-commutativity of witness order yields interference-like structure

### What NFC Cannot Say (Without Interpretation)

- Hilbert space structure is forced
- Complex amplitudes are necessary
- Born rule is derived
- Unitary evolution is required

### Suggested Minimal Mapping

| Quantum Concept | NFC Structure | Confidence |
|-----------------|---------------|------------|
| Superposition | Multiple incompressible extension classes | Medium |
| Measurement | Witness expansion forcing compression | Medium |
| Decoherence | Defect accumulation degrading witness depth | Medium |
| Classicality | Coarse witness fixed point dominance | Medium |
| Born rule | ⚠️ Not derived — requires additional structure | Low |

---

## Example: Classical Physics Mapping

### What NFC Can Say (Structural)

- Coarse witnesses can have stable fixed points
- PASS-bounded defects prevent arbitrary amplification
- Compression dominance selects stable public reports

### What NFC Cannot Say (Without Interpretation)

- Deterministic equations of motion are forced
- Phase space structure is derived
- Hamiltonian/Lagrangian formalism is necessary

### Suggested Minimal Mapping

| Classical Concept | NFC Structure | Confidence |
|-------------------|---------------|------------|
| Determinism | Single extension class under coarse witness | Medium |
| Phase space | Regime alphabet structure | Low |
| Conservation laws | Stabilizer-supported invariants | Medium |
| Arrow of time | Monotone compression order | Medium |

---

## Anti-Patterns: Mappings to Avoid

| Anti-Pattern | Why Problematic |
|--------------|-----------------|
| "NFC proves quantum mechanics" | NFC provides structural analogue, not derivation |
| "The 9th coordinate IS time" | It's pure gauge bookkeeping; physical time requires metric |
| "Defects ARE forces" | Defects are structural; forces are physical |
| "Survivors ARE particles" | Survivors are contextual; particles are (usually) not |
| "Compression frequency IS probability" | Structural counting ≠ quantum probability |

---

## Recommended Usage

1. **Use NFC as constraint**: Physical theories should respect NFC structure
2. **Use NFC as inspiration**: NFC suggests new ways to think about emergence
3. **Do not use NFC as derivation**: Physical claims require physical argument

---

## Forward Work

1. Develop explicit toy models with physical parameters
2. Explore quantitative predictions for specific physical systems
3. Investigate which physical theories are NFC-compatible
4. Identify physical phenomena that would falsify NFC structure

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| Mappings explicitly marked interpretive | ✅ Pass |
| No structural claims based on mappings | ✅ Pass |
| Alternative mappings acknowledged | ✅ Pass |
| Physical derivation distinguished | ✅ Pass |

**Audit Result:** ✅ Clean (as guidelines document)

---

*"Interpretation is not derivation. NFC constrains what can be; it does not determine what is."*
