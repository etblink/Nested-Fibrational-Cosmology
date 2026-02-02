# Physical Theory Compatibility Matrix
## Which Theories Satisfy NFC Constraints?

**Status:** Investigation | **Scope:** Comparative analysis | **Dependencies:** Full NFC corpus

---

## Preamble: Compatibility Criteria

A physical theory is **NFC-compatible** if it can be formulated (possibly after approximation) using only:
- P1: Finite relational incidence
- P2: Constrained composition
- P3: Internal observation
- P4: Finite distinguishability

**Note**: Compatibility does not mean "derived from NFC." It means "does not violate NFC structure."

---

## Part 1: Quantum Mechanics

### Standard Quantum Mechanics (Hilbert Space Formulation)

| NFC Constraint | QM Status | Compatibility |
|---------------|-----------|---------------|
| P1: Finite relational | ❌ Infinite-dimensional Hilbert spaces | ⚠️ Requires regularization |
| P2: Constrained composition | ✅ Tensor product structure | ✅ Compatible |
| P3: Internal observation | ⚠️ Measurement problem | ⚠️ Interpretation-dependent |
| P4: Finite distinguishability | ⚠️ Continuous spectra | ⚠️ Requires coarse-graining |

**Overall**: ⚠️ **Conditionally compatible** with regularization.

### Regularized QM (Finite-dimensional)

| Aspect | Status |
|--------|--------|
| Finite Hilbert spaces | ✅ Satisfies P1 |
| Tensor product composition | ✅ Satisfies P2 |
| POVM measurements | ✅ Satisfies P3, P4 |

**Overall**: ✅ **Compatible** (but is it still QM?)

### NFC Mapping Suggestions

| NFC Concept | QM Analogue | Confidence |
|-------------|-------------|------------|
| Relations | Local operators / states | Medium |
| Compression | Decoherence / coarse-graining | Medium |
| Witnesses | Measurement contexts | Medium |
| Defects | Environmental interactions | Low |
| Survivors | Pointer states | Medium |
| Regimes | Decoherent histories | Medium |

---

## Part 2: Quantum Field Theory

### Standard QFT (Continuous Spacetime)

| NFC Constraint | QFT Status | Compatibility |
|---------------|------------|---------------|
| P1: Finite relational | ❌ Infinite modes per point | ❌ Challenging |
| P2: Constrained composition | ✅ Locality | ✅ Compatible |
| P3: Internal observation | ⚠️ Measurement unclear | ⚠️ Open |
| P4: Finite distinguishability | ❌ Continuous fields | ❌ Challenging |

**Overall**: ❌ **Not directly compatible** — requires significant modification.

### Lattice QFT

| Aspect | Status |
|--------|--------|
| Finite sites | ✅ Satisfies P1 |
| Local interactions | ✅ Satisfies P2 |
| Finite field values | ⚠️ Still infinite per site |

**Overall**: ⚠️ **Partially compatible** — better than continuous, but not fully finite.

### NFC Mapping Suggestions

| NFC Concept | QFT Analogue | Confidence |
|-------------|--------------|------------|
| Relations | Field configurations | Low |
| Compression | RG flow / coarse-graining | Medium |
| Witnesses | Local observables | Medium |
| Defects | Topological defects? | Speculative |

---

## Part 3: General Relativity

### Classical GR (Continuous Manifold)

| NFC Constraint | GR Status | Compatibility |
|---------------|-----------|---------------|
| P1: Finite relational | ❌ Continuous manifold | ❌ Challenging |
| P2: Constrained composition | ⚠️ Diffeomorphism invariance | ⚠️ Complex |
| P3: Internal observation | ⚠️ Observer-dependence | ⚠️ Compatible |
| P4: Finite distinguishability | ❌ Continuous metric | ❌ Challenging |

**Overall**: ❌ **Not directly compatible** — requires discretization.

### Regge Calculus (Simplicial GR)

| Aspect | Status |
|--------|--------|
| Finite simplices | ✅ Satisfies P1 |
| Edge lengths as variables | ⚠️ Still continuous values |
| Local constraints | ✅ Satisfies P2 |

**Overall**: ⚠️ **Partially compatible** — closer than continuous GR.

### Causal Set Theory

| Aspect | Status |
|--------|--------|
| Discrete elements | ✅ Satisfies P1 |
| Order relation | ✅ Satisfies P2 (partial) |
| Finite intervals | ✅ Satisfies P4 |

**Overall**: ✅ **Highly compatible** — explicitly relational and discrete.

### NFC Mapping Suggestions

| NFC Concept | GR Analogue | Confidence |
|-------------|-------------|------------|
| Relations | Causal / metric relations | Medium |
| Compression | Coarse-graining of geometry | Medium |
| Witnesses | Geodesic observers | Low |
| 9th coordinate | Proper time / entropy? | Speculative |

---

## Part 4: Quantum Gravity Approaches

### String Theory

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ❌ Infinite tower of modes |
| P2: Constrained composition | ⚠️ Worldsheet / spacetime |
| P3: Internal observation | ❓ Unclear |
| P4: Finite distinguishability | ❌ Continuous moduli |

**Overall**: ❌ **Not directly compatible** — requires compactification/regularization.

### Loop Quantum Gravity

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ✅ Spin networks are finite |
| P2: Constrained composition | ⚠️ Spin foam moves |
| P3: Internal observation | ❓ Unclear |
| P4: Finite distinguishability | ✅ Discrete spectra |

**Overall**: ✅ **Highly compatible** — explicitly relational and discrete.

### Causal Dynamical Triangulations

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ✅ Simplicial complex |
| P2: Constrained composition | ✅ Gluing rules |
| P3: Internal observation | ⚠️ Emergent |
| P4: Finite distinguishability | ✅ Finite structure |

**Overall**: ✅ **Highly compatible** — explicitly discrete and relational.

### Asymptotic Safety

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ⚠️ Continuous but UV fixed |
| P2: Constrained composition | ✅ RG structure |
| P3: Internal observation | ❓ Unclear |
| P4: Finite distinguishability | ⚠️ Scale-dependent |

**Overall**: ⚠️ **Partially compatible** — less discrete than others.

---

## Part 5: Classical Physics

### Classical Mechanics (Phase Space)

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ❌ Continuous phase space |
| P2: Constrained composition | ✅ Hamiltonian flow |
| P3: Internal observation | ⚠️ Idealized |
| P4: Finite distinguishability | ❌ Continuous |

**Overall**: ❌ **Not compatible** — classicality is emergent in NFC, not fundamental.

### Statistical Mechanics

| NFC Constraint | Status |
|---------------|--------|
| P1: Finite relational | ⚠️ Thermodynamic limit |
| P2: Constrained composition | ✅ Microscopic dynamics |
| P3: Internal observation | ✅ Measurement |
| P4: Finite distinguishability | ⚠️ Coarse-graining |

**Overall**: ⚠️ **Partially compatible** — NFC "probability" resembles statistical mechanics.

---

## Part 6: Compatibility Summary Matrix

| Theory | P1 | P2 | P3 | P4 | Overall |
|--------|----|----|----|----|---------|
| QM (Hilbert space) | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| QM (finite-dim) | ✅ | ✅ | ✅ | ✅ | ✅ |
| QFT (continuous) | ❌ | ✅ | ⚠️ | ❌ | ❌ |
| Lattice QFT | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| GR (continuous) | ❌ | ⚠️ | ⚠️ | ❌ | ❌ |
| Regge calculus | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| Causal sets | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| String theory | ❌ | ⚠️ | ❓ | ❌ | ❌ |
| Loop QG | ✅ | ⚠️ | ❓ | ✅ | ✅ |
| CDT | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Asymptotic safety | ⚠️ | ✅ | ❓ | ⚠️ | ⚠️ |
| Classical mechanics | ❌ | ✅ | ⚠️ | ❌ | ❌ |
| Statistical mechanics | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ |

**Legend**: ✅ Compatible | ⚠️ Partial/conditional | ❌ Not compatible | ❓ Unclear

---

## Part 7: Key Insights

### Insight 1: Discreteness is Critical

Theories with **fundamental discreteness** (causal sets, loop QG, CDT) are most NFC-compatible. Continuous theories require regularization.

### Insight 2: Relationalism Varies

NFC is **strongly relational** (no background). Theories with background structures (string theory on fixed spacetime) are less compatible.

### Insight 3: Emergence is Central

NFC treats **classicality and continuity as emergent**, not fundamental. This aligns with quantum gravity approaches.

### Insight 4: Measurement is Challenging

The **internal observation** constraint (P3) is subtle. Many theories don't have a clear measurement theory.

---

## Part 8: Recommendations

### For NFC

1. **Develop explicit mappings**: How exactly do NFC concepts map to LQG, CDT, etc.?
2. **Study approximation**: How do continuous theories emerge from NFC structure?
3. **Collaborate**: Work with practitioners of compatible approaches.

### For Physical Theories

1. **Test NFC constraints**: Do your theory's structures satisfy P1–P4?
2. **Explore NFC language**: Does it offer new insights?
3. **Identify violations**: Where does your theory exceed NFC?

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| Honest assessment of compatibility | ✅ Pass |
| Distinguishes fundamental from emergent | ✅ Pass |
| Acknowledges uncertainty | ✅ Pass |
| No favoritism to NFC | ✅ Pass |

**Audit Result:** ✅ Clean

---

## References

- Application Mappings: `applications/mapping_guidelines.md`
- Falsifiability Analysis: `analysis/falsifiability.md`
- Individual theory references: Standard textbooks and review articles
