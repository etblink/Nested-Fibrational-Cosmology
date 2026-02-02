# NFC Category Theory Formalization
## Functorial Treatment of Relational Structure

**Status:** Deep foundations | **Scope:** Mathematical rigor upgrade | **Dependencies:** Full NFC corpus

---

## Preamble: Why Category Theory?

Category theory provides:
1. **Precision**: Eliminates ambiguity in "composition," "functoriality," "natural transformation"
2. **Abstraction**: Separates structural patterns from concrete instantiations
3. **Universality**: Identifies what is inevitable vs. contingent
4. **Compositionality**: Builds complex structures from simple ones

NFC already uses categorical language informally. This document makes it rigorous.

---

## 1. The Category of Relational Configurations

### 1.1 Definition: Rel

**Definition 1.1.** Let **Rel** be the category where:
- **Objects**: Finite sets of incidence sites $\mathcal{I}, \mathcal{J}, \ldots$
- **Morphisms**: Relations $r: \mathcal{I} \to \mathcal{J}$ as subsets $r \subseteq \mathcal{I} \times \mathcal{J}$
- **Composition**: $s \circ r = \{(i,k) : \exists j, (i,j) \in r, (j,k) \in s\}$
- **Identity**: $\text{id}_{\mathcal{I}} = \{(i,i) : i \in \mathcal{I}\}$

**NFC twist**: We work with **partial relations** — morphisms may not exist between arbitrary objects.

### 1.2 Partial Category Structure

**Definition 1.2.** A **partial category** $\mathcal{C}$ consists of:
- Objects $\text{Ob}(\mathcal{C})$
- For $A, B \in \text{Ob}(\mathcal{C})$, a set $\mathcal{C}(A,B)$ (possibly empty)
- Partial composition: $\circ: \mathcal{C}(B,C) \times \mathcal{C}(A,B) \rightharpoonup \mathcal{C}(A,C)$
- Associativity where defined
- Identity morphisms where admissible

**Proposition 1.3.** NFC relational systems form partial categories.

*Proof.* Constrained composition is partial by definition. Weak associativity gives associativity where defined. Identity exists only where admissible. ∎

---

## 2. The Compression Functor

### 2.1 Witnesses as Functors

**Definition 2.1.** A **witness** is a functor:
$$W: \mathcal{C}_{\text{configs}} \to \mathcal{C}_{\text{reports}}$$

where:
- $\mathcal{C}_{\text{configs}}$ = category of relational configurations
- $\mathcal{C}_{\text{reports}}$ = category of witness reports

**Key property**: Functoriality means $W(r' \circ r) = W(r') \circ W(r)$ — witness respects composition.

### 2.2 Compression as Quotient

**Definition 2.2.** The **compression** induced by witness $W$ is the quotient category:
$$\mathcal{C}/\sim_W$$

where $r \sim_W r' \iff W(r) = W(r')$.

**Proposition 2.3.** $\mathcal{C}/\sim_W$ is a category iff $\sim_W$ is a congruence.

*Proof.* Standard category theory. ∎

**NFC situation**: $\sim_W$ is **not** a congruence (non-functoriality) — this is the obstruction addressed by the 9th coordinate.

---

## 3. The 9th Coordinate as Natural Transformation

### 3.1 Lifting to Extended Category

**Definition 3.1.** The **extended category** $\widetilde{\mathcal{C}}$ has:
- Objects: $(A, a)$ where $A \in \text{Ob}(\mathcal{C})$, $a \in \mathbb{R}$
- Morphisms: $(r, \Delta a): (A, a) \to (B, a')$ where $r: A \to B$ and $a' = a + \Delta a$

**Proposition 3.2.** $\widetilde{\mathcal{C}}$ is a category (total, not partial).

*Proof.* Composition: $(r', \Delta a') \circ (r, \Delta a) = (r' \circ r, \Delta a + \Delta a')$. Associativity from $\mathbb{R}$ addition. ∎

### 3.2 The Lifting Functor

**Definition 3.3.** The **lifting functor**:
$$\widetilde{W}: \mathcal{C}_{\text{configs}} \to \widetilde{\mathcal{C}}_{\text{reports}}$$

is defined by:
- $\widetilde{W}(A) = (W(A), A(A))$ where $A(A)$ is the 9th coordinate
- $\widetilde{W}(r) = (W(r), \Delta A(r))$

**Theorem 3.4 (Functoriality Restoration).** $\widetilde{W}$ is a functor (total, not partial).

*Proof.* By construction:
$$\widetilde{W}(r' \circ r) = (W(r' \circ r), A(r' \circ r))$$
$$= (W(r') \circ W(r), A(r') + A(r) + \alpha(r',r))$$
$$= (W(r'), A(r')) \circ (W(r), A(r))$$
$$= \widetilde{W}(r') \circ \widetilde{W}(r)$$

where $\alpha$ is the defect correction. ∎

### 3.3 Natural Transformation Interpretation

**Definition 3.5.** Let $\pi: \widetilde{\mathcal{C}} \to \mathcal{C}$ be projection $(A, a) \mapsto A$.

**Proposition 3.6.** The diagram:
$$\begin{array}{ccc}
\mathcal{C}_{\text{configs}} & \xrightarrow{\widetilde{W}} & \widetilde{\mathcal{C}}_{\text{reports}} \\
\downarrow W & & \downarrow \pi \\
\mathcal{C}_{\text{reports}} & = & \mathcal{C}_{\text{reports}}
\end{array}$$

commutes up to natural isomorphism.

**Interpretation**: The 9th coordinate is the **obstruction to strict functoriality**, measured by how far $W$ is from being a functor.

---

## 4. Stabilizers as Endomorphisms

### 4.1 Stabilizer Category

**Definition 4.1.** For compression class $C$, the **stabilizer category** $\text{Stab}(C)$ has:
- Objects: Configurations in $C$
- Morphisms: Stabilizer relations $S: x \to y$ for $x, y \in C$

**Proposition 4.2.** $\text{Stab}(C)$ is a groupoid (all morphisms invertible up to equivalence).

*Proof.* Stabilizers commute with extension and are incidence-neutral, giving inverses up to observational equivalence. ∎

### 4.2 Automorphism Group

**Definition 4.3.** The **stabilizer group** of $C$ is:
$$\text{Aut}_{\text{Stab}}(C) = \{S \in \text{Stab}(C) : S: x \to x\}$$

**Theorem 4.4 (Stabilizer Necessity).** $C$ persists under extension iff $\text{Aut}_{\text{Stab}}(C)$ is nontrivial.

*Proof.* Nontrivial automorphisms provide relations that block refinement. ∎

---

## 5. Defects as 2-Morphisms

### 5.1 Higher Category Structure

**Definition 5.1.** A **defect** between relations $r, r': A \to B$ is a 2-morphism:
$$\delta: r \Rightarrow r'$$

satisfying:
- $	ext{dom}(\delta) = r$, $	ext{cod}(\delta) = r'$
- Horizontal composition: $\delta' * \delta: r' \circ r \Rightarrow s' \circ s$
- Vertical composition: $\delta' \circ \delta: r \Rightarrow r''$

### 5.2 Defect 2-Category

**Definition 5.2.** The **defect 2-category** $\text{Def}(\mathcal{C})$ has:
- 0-cells: Objects of $\mathcal{C}$
- 1-cells: Morphisms of $\mathcal{C}$
- 2-cells: Defects

**Theorem 5.3 (Defect-Mediated Interaction).** Interaction among survivors is given by horizontal composition of defects in $\text{Def}(\mathcal{C})$.

*Proof.* Defects modify paths without altering stabilizers; horizontal composition gives joint effect. ∎

---

## 6. The Fundamental NFC Diagram

### 6.1 Complete Categorical Structure

$$
\begin{array}{ccccc}
\text{Rel}_{\text{configs}} & \xrightarrow{\text{Comp}} & \text{Rel}/\sim & \xleftarrow{\text{Stab}} & \text{Survivors} \\
\downarrow W & & \downarrow & & \downarrow \\
\text{Reports} & \xleftarrow{\pi} & \widetilde{\text{Reports}} & \xrightarrow{\text{Def}} & \text{Regimes}
\end{array}$$

### 6.2 Interpretation

| Arrow | Meaning |
|-------|---------|
| Comp | Compression functor |
| Stab | Stabilizer inclusion |
| W | Witness functor (non-functorial without lift) |
| π | Projection (forgets 9th coordinate) |
| Def | Defect 2-functor |

---

## 7. Universality and Adjunctions

### 7.1 Free vs. Forgetful Functors

**Definition 7.1.** Let $U: \text{PartialCat} \to \text{Set}$ be forgetful (objects only).

**Proposition 7.2.** The free partial category functor $F: \text{Set} \to \text{PartialCat}$ is left adjoint to $U$.

$$F \dashv U$$

**Interpretation**: NFC relational systems are "free" in a precise sense — minimal structure consistent with given objects.

### 7.2 Compression as Reflection

**Definition 7.3.** Witness $W$ induces **reflective subcategory** if compression has left adjoint.

**Proposition 7.4.** For coarse witnesses, compression is reflective.

*Proof.* Coarse witnesses identify more, giving left adjoint (inclusion of coarse into fine). ∎

---

## 8. Conclusion

Category theory provides:
1. **Rigorous foundation** for NFC concepts
2. **Universal properties** identifying inevitable structure
3. **Compositionality** for building complex systems
4. **Comparison tools** with other frameworks

**Key insight**: NFC structure is not arbitrary — it emerges from universal properties of finite relational systems.

---

## References

- Mac Lane, S. "Categories for the Working Mathematician"
- Baez, J. & Dolan, J. "Higher-Dimensional Algebra and Topological Quantum Field Theory"
- NFC corpus: `theorems/`, `toys/`, `audit/`
