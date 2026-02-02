# NFC and Quantum Information: A Resource Theory Framework
## Connecting Structural Constraints to Quantum Resources

**Status:** Phase 2 Development | **Priority:** High | **Collaboration Target:** QI Researchers

---

## Executive Summary for QI Collaborators

NFC's structure maps naturally to quantum information resource theories. This document establishes the correspondence and identifies new resource-theoretic insights from NFC.

**Key Insight**: NFC's compression classes = quantum states; NFC's witnesses = measurements; NFC's defects = noise.

---

## 1. The Resource Theory Framework

### 1.1 Standard QI Resource Theory

A resource theory consists of:
- **Free states**: States that are "easy" to prepare
- **Free operations**: Operations that are "easy" to perform
- **Resources**: States/operations that are valuable

**Examples**: Entanglement, coherence, athermality, magic.

### 1.2 NFC as Resource Theory

| QI Resource Theory | NFC Analogue |
|-------------------|--------------|
| Free states | Coarse compression classes |
| Free operations | Admissible extensions |
| Resources | Fine compression classes (survivors) |
| Resource measure | Witness depth k |

---

## 2. Entanglement as Survivor Coexistence

### 2.1 The NFC View

In NFC, **multiple survivors** are required for non-trivial interaction. This is structurally analogous to entanglement:

| Entanglement | NFC |
|-------------|-----|
| Two (or more) subsystems | Two (or more) survivors |
| Cannot be described separately | Cannot persist separately |
| Joint state is fundamental | Joint regime is fundamental |

### 2.2 Defect-Mediated Interaction = Entangling Operations

**NFC claim**: Defects that couple survivors are the **only** admissible interaction.

**QI mapping**: Defects = entangling gates.

**Key difference**: NFC defects are **structurally forced** (asymmetric, bounded), not postulated.

---

## 3. Coherence as Witness Depth

### 3.1 Standard Coherence Theory

**Coherent superposition**: Quantum state with off-diagonal elements in preferred basis.

**Incoherent states**: Diagonal in preferred basis.

### 3.2 NFC Mapping

| Coherence | NFC |
|-----------|-----|
| Coherent superposition | Multiple incompressible extension classes |
| Incoherent state | Single compression class |
| Preferred basis | Witness eigenbasis |
| Coherence measure | Witness depth k |

**Theorem (NFC Coherence)**: Coherence = ability to resolve multiple extension classes.

### 3.3 Decoherence as k_eff Degradation

**Standard view**: Decoherence = loss of off-diagonal elements.

**NFC view**: Decoherence = defect budget increases → k_eff decreases → fewer resolvable classes.

**Quantitative**: From U12 analysis:
$$k_{\text{eff}}(t) = k_{\max} \left(1 - \frac{\mathfrak{D}(t)}{\gamma^2}\right)$$

---

## 4. Quantum Channels from NFC Structure

### 4.1 Completely Positive Trace-Preserving Maps

Standard quantum channel: $\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger$

### 4.2 NFC Channel Construction

**NFC channel**: Map induced by admissible extension with defect accumulation.

**Kraus operators**: Correspond to different defect-mediated paths.

**Theorem (NFC Channel)**: NFC channels are:
- CPTP (by construction)
- Unital (if defects are symmetric)
- Non-unital (if defects are asymmetric)

### 4.3 Defect-Induced Depolarization

**Model**: Defects cause random transitions between compression classes.

**Result**: Effective channel:
$$\mathcal{E}_{\text{defect}}(\rho) = (1-p) \rho + p \frac{I}{d}$$

where $p \sim \mathfrak{D}/\gamma^2$.

---

## 5. Resource Measures from NFC

### 5.1 Witness Depth as Coherence Measure

**Definition**: $C_{\text{NFC}}(\rho) = k_{\text{eff}}(\rho)$

**Properties**:
- $C_{\text{NFC}} = 0$ for incoherent states
- $C_{\text{NFC}} = k_{\max}$ for maximally coherent states
- Monotonic under free operations (admissible extensions)

### 5.2 Defect Budget as Noise Measure

**Definition**: $N_{\text{NFC}}(\rho) = \mathfrak{D}(\rho)$

**Properties**:
- $N_{\text{NFC}} = 0$ for noiseless states
- Increases under defect accumulation
- Related to entanglement degradation

### 5.3 Trade-off Relation

**Conjecture (NFC Uncertainty)**:
$$C_{\text{NFC}}(\rho) \cdot N_{\text{NFC}}(\rho) \leq \text{constant}$$

**Interpretation**: More coherence requires less noise, and vice versa.

---

## 6. Quantum Error Correction from Stabilizers

### 6.1 Standard QEC

**Stabilizer code**: Subspace preserved by commuting stabilizer operators.

### 6.2 NFC Stabilizers = QEC Stabilizers

| QEC | NFC |
|-----|-----|
| Stabilizer operators | Stabilizer relations |
| Code space | Survivor compression class |
| Errors | Defects |
| Error correction | Refinement blocking |

**Theorem (NFC-QEC)**: NFC stabilizers define quantum error-correcting codes.

### 6.3 Defect Threshold

**Standard QEC**: Errors below threshold are correctable.

**NFC**: Defects below $\gamma$ are "sub-gap" and don't cause public branching.

**Result**: NFC gap threshold $\gamma$ = QEC threshold.

---

## 7. Circuit Model from NFC

### 7.1 Standard Quantum Circuit

- Qubits in states
- Gates as unitary operations
- Measurements at end

### 7.2 NFC Circuit Model

| Circuit Element | NFC Analogue |
|----------------|--------------|
| Qubit | Survivor |
| State | Compression class |
| Gate | Admissible extension |
| Entangling gate | Defect-mediated interaction |
| Measurement | Witness activation |
| Noise | Defect accumulation |

### 7.3 Circuit Depth and k_eff

**Standard**: Circuit depth = number of gates.

**NFC**: Effective depth = $k_{\text{eff}}$ after defect accumulation.

**Result**: Deep circuits (many gates) have degraded $k_{\text{eff}}$ → classical behavior.

---

## 8. Quantum Advantage from NFC Structure

### 8.1 What is Quantum Advantage?

Quantum computers can solve certain problems faster than classical computers.

### 8.2 NFC Interpretation

**Quantum advantage** = ability to maintain $k_{\text{eff}} > 0$ throughout computation.

**Classical simulation** = $k_{\text{eff}} = 0$ (coarse witness dominates).

### 8.3 Conditions for Quantum Advantage

From NFC:
1. **Sufficient survivors**: Multiple incompressible classes
2. **Low defect budget**: $\mathfrak{D} \ll \gamma^2$
3. **Fine witnesses**: Can resolve quantum structure

**NFC prediction**: Quantum advantage is fragile — requires careful control of defects.

---

## 9. Collaboration Opportunities

### 9.1 For QI Theorists

**Questions NFC raises**:
- Can resource theories be derived from first principles?
- Is coherence fundamentally about compression?
- What is the minimal structure for quantum advantage?

**NFC contribution**: Structural derivation of resource-theoretic concepts.

### 9.2 For Experimental QI

**NFC predictions**:
- Decoherence rates scale with "defect budget"
- Quantum advantage has fundamental limits
- Error correction thresholds are structural

**Experiments to design**:
- Measure $k_{\text{eff}}$ degradation in real systems
- Test if noise models match NFC structure

### 9.3 For Quantum Computing

**NFC insights**:
- Circuit depth limited by defect accumulation
- Stabilizer codes are structurally natural
- Quantum advantage requires maintaining fine witnesses

**Applications**:
- Optimal circuit design
- Noise mitigation strategies
- Error correction code selection

---

## 10. Open Problems

| Problem | Status | NFC Approach |
|---------|--------|--------------|
| Derive Born rule | Open | Compression frequency + ? |
| Quantum supremacy bounds | Open | k_eff analysis |
| Fault-tolerance thresholds | Partial | γ as threshold |
| Quantum gravity + QI | Open | NFC as bridge |

---

## 11. Conclusion

NFC provides a **structural foundation** for quantum information:

- ✅ Coherence = witness depth
- ✅ Decoherence = k_eff degradation
- ✅ Entanglement = survivor coexistence
- ✅ QEC = stabilizer structure
- ✅ Quantum advantage = maintaining k_eff > 0

**Status**: Framework ready for QI collaboration.

---

## References

- Chitambar, E. & Gour, G. (2019). Quantum resource theories.
- Brandão, F.G.S.L. & Gour, G. (2015). Reversible framework for quantum resource theories.
- NFC corpus: `theorems/`, `toys/`, `foundations/`
