# Explicit NFC Mapping to Loop Quantum Gravity
## Structural Correspondences and Derivations

**Status:** Physical application | **Scope:** Quantum gravity interface | **Dependencies:** Full NFC corpus

---

## Preamble: Why Loop Quantum Gravity?

Loop Quantum Gravity (LQG) is the most NFC-compatible quantum gravity approach:
- ✅ **Discrete**: Spin networks are finite graphs
- ✅ **Relational**: No background spacetime
- ✅ **Background-independent**: Geometry emerges from relations
- ✅ **Finite spectra**: Area and volume operators have discrete eigenvalues

This document establishes explicit structural mappings.

---

## 1. Spin Networks as Relational Configurations

### 1.1 LQG Structure

A **spin network** is:
- Graph $\Gamma$ with edges $e$ and vertices $v$
- Each edge labeled by irreducible representation $j_e \in \frac{1}{2}\mathbb{N}$ (spin)
- Each vertex labeled by intertwiner $i_v$

### 1.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Graph $\Gamma$ | Incidence sites $\mathcal{I}$ | Vertices = sites, edges = relations |
| Spin label $j_e$ | Relation type | Distinguishes relation "strength" |
| Intertwiner $i_v$ | Composition rule | How relations compose at vertex |
| Spin network state | Relational configuration | Full specification |

**Key insight**: Spin networks are **typed relational configurations** — exactly NFC's structure.

---

## 2. The Holonomy-Flux Algebra as Constrained Composition

### 2.1 LQG Structure

Holonomies $h_e \in SU(2)$ along edges, fluxes $E_f$ through faces.

**Algebra**:
$$[h_e, E_f] = i\hbar \delta_{e,f} h_e$$

Non-commutativity = quantum geometry uncertainty.

### 2.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Holonomy $h_e$ | Relation token | Group-valued relation |
| Flux $E_f$ | Witness | "Measurement" of geometry |
| Non-commutativity | Non-commuting witnesses | $(\omega_E)_F \neq (\omega_F)_E$ |
| [h, E] = iℏ | Witness gap | Finite distinguishability |

**Key insight**: The holonomy-flux algebra **is** NFC's witness non-commutativity, with ℏ as gap parameter.

---

## 3. Spin Foam Moves as Admissible Extension

### 3.1 LQG Structure

**Spin foams**: 2-complexes interpolating between spin networks.

**Pachner moves**: Local combinatorial changes to triangulation.

### 3.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Spin foam | Admissible extension | 2D history of 1D configurations |
| Pachner move | Admissible composition rule | Local, typed, partial |
| Foam amplitude | Compression weight | Contribution to path integral |

**Key insight**: Spin foam dynamics **is** NFC's admissible extension, with amplitudes as weighted compression frequencies.

---

## 4. Area and Volume Spectra as Finite Distinguishability

### 4.1 LQG Structure

**Area operator**:
$$\hat{A}(S) = 8\pi\gamma_{\text{Immirzi}} \ell_P^2 \sum_{e \cap S \neq \emptyset} \sqrt{j_e(j_e+1)}$$

**Spectrum**: Discrete, with minimum $A_0 \sim \ell_P^2$.

### 4.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Area spectrum | Finite distinguishability | Only finitely many area values |
| Minimum area $A_0$ | Gap threshold $\gamma$ | Smallest distinguishable unit |
| Immirzi parameter | Free parameter | Like NFC's $c$ in k_eff |
| Planck length $\ell_P$ | Fundamental scale | Where discreteness appears |

**Key insight**: LQG's discrete spectra **are** NFC's finite distinguishability, with ℏG/c³ setting the scale.

---

## 5. Coherent States as Survivor-Stabilizer Pairs

### 5.1 LQG Structure

**Coherent states** $|\psi_{g}\rangle$: Peaked on classical geometry $g$.

**Properties**:
- Minimum uncertainty
- Stable under Hamiltonian flow
- Form overcomplete basis

### 5.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Coherent state | Survivor | Stable under extension |
| Peak geometry $g$ | Compression class | What the state "is" |
| Uncertainty minimum | Stabilizer | Prevents refinement |
| Overcompleteness | Multiple stabilizers | Different paths to same class |

**Key insight**: LQG coherent states **are** NFC survivors, with quantum geometry fluctuations as halo.

---

## 6. The Hamiltonian Constraint as Defect

### 6.1 LQG Structure

**Hamiltonian constraint**:
$$\hat{H}|\psi\rangle = 0$$

Generates dynamics, but: anomaly-free definition is difficult.

### 6.2 NFC Mapping

| LQG Concept | NFC Concept | Mapping |
|-------------|-------------|---------|
| Hamiltonian constraint | Defect | Modifies admissible paths |
| Constraint algebra | Defect monoid | How defects compose |
| Anomaly | Non-closure | Failure of constraint algebra |
| Master constraint | Defect functional | Accumulated constraint violation |

**Key insight**: The Hamiltonian constraint **is** NFC's defect, with anomalies as non-closure requiring 9th coordinate.

---

## 7. The 9th Coordinate in LQG

### 7.1 What Could It Be?

Candidate interpretations:

| Candidate | Evidence | Assessment |
|-----------|----------|------------|
| Proper time | Parameterizes evolution | Natural but gauge-dependent |
| Immirzi parameter | Free parameter | Matches gauge freedom |
| Barbero-Immirzi time | Related to time gauge | Promising |
| Thermal time | From KMS condition | Matches monotone order |
| Entropy | From black hole thermodynamics | Matches compression |

### 7.2 Proposed Mapping

**Hypothesis**: The 9th coordinate in LQG is **entropic time** — accumulated information loss under coarse-graining.

**Evidence**:
- Black hole entropy $S = A/4G\hbar$ is geometric
- Entropy increases monotonically (R1)
- Entropy is additive (R2)
- Different entropies comparable (R3)
- No infinitesimal entropy (R4 — at Planck scale)

---

## 8. Derivation: Why LQG Satisfies NFC Constraints

### 8.1 P1: Finite Relational Incidence

**LQG**: Spin networks have finite graphs.

**Verification**: ✅ Each spin network involves finitely many edges and vertices.

### 8.2 P2: Constrained Composition

**LQG**: Spin foam moves are local and typed.

**Verification**: ✅ Pachner moves apply only at specific configurations; not all compositions are admissible.

### 8.3 P3: Internal Observation

**LQG**: Observers are quantum systems on spin networks.

**Verification**: ✅ No external classical observer assumed.

### 8.4 P4: Finite Distinguishability

**LQG**: Area and volume spectra are discrete.

**Verification**: ✅ Only finitely many distinguishable geometric configurations at any scale.

---

## 9. Predictions: What NFC Suggests for LQG

### 9.1 Finite Regime Alphabet

**NFC prediction**: LQG should have finitely many "phases" or vacuum states.

**LQG status**: Open. Different spin network graphs may represent different regimes.

### 9.2 Defect-Mediated Dynamics

**NFC prediction**: Hamiltonian constraint should be defect-like, not fundamental.

**LQG status**: Consistent with master constraint approach and group field theory.

### 9.3 Classicality as Coarse Fixed Point

**NFC prediction**: Classical GR emerges from coarse witness (coarse-grained spin networks).

**LQG status**: Semiclassical limit is active research area; NFC suggests specific mechanism.

---

## 10. Open Questions

| Question | Status |
|----------|--------|
| What is the explicit witness hierarchy in LQG? | Open |
| Can k_eff be computed from LQG parameters? | Open |
| What are the stabilizers (conserved quantities)? | Partial — known for specific models |
| How does the 9th coordinate relate to physical time? | Open |

---

## Conclusion

LQG is **highly NFC-compatible**. The mappings are natural and mutually illuminating:
- Spin networks = relational configurations
- Holonomy-flux algebra = witness non-commutativity
- Spin foams = admissible extensions
- Coherent states = survivors
- Hamiltonian constraint = defect

**Key insight**: NFC provides a **structural meta-language** for understanding what LQG achieves and what remains open.

---

## References

- Rovelli, C. "Quantum Gravity"
- Ashtekar, A. & Lewandowski, J. "Background Independent Quantum Gravity"
- Thiemann, T. "Modern Canonical Quantum General Relativity"
- NFC corpus: `theorems/`, `toys/`, `foundations/`
