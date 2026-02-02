# Survivors and Stabilizers
## Part III — Persistence Without Time

**Status:** Proven | **Dependencies:** PASS, Derived Identity | **Scope:** Structural

---

## III.1 Compression Classes and Generic Instability

### III.1.1 Compression as Consequence of Finite Distinguishability

Finite distinguishability **forces compression**. When observers cannot resolve all relational differences, indistinguishable configurations are necessarily grouped.

**Definition III.1.1 (Compression Class)**

A compression class is a set of relational configurations that are observationally indistinguishable under all admissible tests available to internal observers.

Compression is **induced structurally**, not performed by observers.

### III.1.2 Compression Does Not Imply Persistence

**Critical distinction**: Compression classes are defined relative to fixed observational context. Nothing guarantees stability under further admissible extension.

**Lemma III.1.2 (Compression Is Context-Bound)**

A compression class defined relative to given admissible context may dissolve under admissible extension.

**Proof sketch**: Admissible extension introduces new relational contexts, enabling new observational tests. Finite distinguishability forces refinement whenever new distinctions become observable. ∎

### III.1.3 Generic Instability

**Lemma III.1.3 (Generic Refinement)**

Most compression classes are extension-sensitive. "Most" means: all but structurally constrained subset (characterized in Section III.2).

**Proof sketch**: Admissible extensions introduce new contexts → new tests → refinement of previously collapsed distinctions. ∎

**Corollary III.1.4**: Persistence is **not generic**. It requires additional structure beyond compression alone.

---

## III.2 Stabilizers

### III.2.1 Motivation

If persistence is to occur, there must exist structural features that **prevent refinement without enforcing sameness as primitive**.

The key observation: Refinement arises when admissible extension introduces new observable distinctions. Persistence requires relations whose participation **does not generate new distinguishability**.

These relations are **incidence-neutral**.

### III.2.2 Definition of Stabilizer

**Definition III.2.1 (Stabilizer)**

Let $C$ be a compression class. A relation (or finite family of relations) $S$ is a **stabilizer** of $C$ if for every configuration $x \in C$:

1. **Incidence neutrality**: Composing $S$ with $x$ does not introduce new incidence sites or relation types capable of generating additional observational tests

2. **Observational invariance**: For every admissible observer $W$:
   $$W(x) = W(S \circ x)$$
   up to indistinguishability

3. **Extension commutation**: For every admissible extension $E$:
   $$E(S \circ x) \sim S \circ E(x)$$
   (up to admissible reordering of composition)

**No assumption**: Identity element, inverse, symmetry group, or algebraic structure.

### III.2.3 What Stabilizers Are Not

| Misinterpretation | Why Incorrect |
|-------------------|---------------|
| Identity relations | Would violate IBI no-go |
| Symmetries | Would smuggle group structure |
| Conserved quantities | Would assume dynamics |
| Invariants imposed externally | Would violate internal constraint |

Stabilizers **do not enforce sameness**. They **permit sameness to persist** by failing to introduce new distinctions.

### III.2.4 Existence Is Not Assumed

**Critical**: Nothing guarantees stabilizers exist. Indeed, most relational systems admit none.

Stabilizers are **selective, not universal**: they explain why some compression classes persist, not why compression always yields persistence.

---

## III.3 The Stabilizer Theorem

### Lemma III.3.1 (Refinement Blocking)

Let $C$ be a compression class and $S$ a stabilizer of $C$. Then no admissible extension can refine $C$.

**Proof**:
Assume contradiction: there exists admissible extension $E$ and configurations $x, y \in C$ such that:
$$W(E(x)) \neq W(E(y))$$

By extension commutation:
$$E(S \circ x) \sim S \circ E(x), \quad E(S \circ y) \sim S \circ E(y)$$

By observational invariance:
$$W(S \circ E(x)) = W(E(x)), \quad W(S \circ E(y)) = W(E(y))$$

Thus $W$ distinguishes $S \circ x$ and $S \circ y$, contradicting incidence neutrality.

Therefore no such extension exists. ∎

### Lemma III.3.2 (No Persistence Without Stabilizers)

If a compression class admits no stabilizer, it is extension-sensitive.

**Proof (structural exhaustion)**:

Assume $C$ admits no stabilizer. Then for every relation $r$ incident on configurations in $C$, at least one stabilizer condition fails:
- $r$ introduces new incidence structure, OR
- $r$ enables new observational tests, OR
- $r$ fails to commute with admissible extension

Because admissible extensions are finite but nontrivial, some extension must activate such failure, introducing new distinguishability. Hence $C$ is extension-sensitive. ∎

### Theorem III.3.3 (Stabilizer Necessity and Sufficiency)

A compression class persists under all admissible extensions **if and only if** it admits at least one stabilizer family.

**Proof**:
- ($\Rightarrow$) By Lemma III.3.1
- ($\Leftarrow$) By Lemma III.3.2

∎

---

## III.4 Survivors

### III.4.1 Definition

**Definition III.4.1 (Survivor)**

Let $C$ be a compression class. $C$ is a **survivor** if and only if:

1. **Extension invariance**: For every admissible extension $E$, all configurations in $E(C)$ remain observationally indistinguishable

2. **Stabilizer support**: There exists at least one stabilizer family $S$ such that $S$ stabilizes $C$

3. **No admissible refinement**: There exists no admissible extension under which $C$ can be strictly refined into two observationally distinguishable compression classes

**No appeal to**: Persistence through time, re-identification, or global equivalence.

A survivor is **not something that endures**; it is something that **cannot be split by admissible structure**.

### III.4.2 Survivors Are Not Assumed to Exist

**Critical emphasis**: Survivors are **not guaranteed**.

A relational system may admit:
- Compression classes
- Stabilizers

Yet still have **no survivors**, if stabilizers fail to cover all admissible extensions.

This is not a failure of the framework. It is a statement about the **rarity of persistence**.

### III.4.3 Fixed-Point Characterization

**Lemma III.4.2**: A compression class $C$ is a survivor if and only if it is a fixed point of the admissible extension operator up to observational indistinguishability.

**Proof**: Immediate from definition. ∎

### III.4.4 Finite Survivor Theorem

**Theorem III.4.3 (Finite Survivors)**

In any finite relational neighborhood with constrained composition and internal observation, the number of survivors is **finite**.

**Proof**:
- Total compression classes: finite (by finite incidence + distinguishability)
- Most compression classes: extension-sensitive (Lemma III.1.3)
- Only stabilizer-supported classes: can persist (Theorem III.3.3)
- Stabilizer families: finite in number (finite incidence + admissibility)

Therefore only finitely many compression classes satisfy survivor criteria. ∎

This blocks:
- Infinite object proliferation
- Landscape-style persistence
- Unbounded identity emergence

---

## III.5 Objects as Survivor-Stabilizer Pairs

### III.5.1 Derived Objecthood

**Corollary III.5.1 (Objecthood)**

An **object**, insofar as the notion is admissible at all, is nothing more than:
> A survivor compression class together with its stabilizer family.

Objects are:
- ❌ Not primitive
- ❌ Not carriers
- ❌ Not substrates
- ❌ Not assumed

They are **structural fixed points of relational extension**.

### III.5.2 No-Object Consistency

**Lemma III.5.2**: A relational system may be fully consistent and non-collapsing even if it admits no survivors and therefore no objects.

**Proof**: Consistency depends only on finiteness, constrained composition, internal observation. Survivors are required for persistence, not for existence. ∎

This blocks the inference: "If objects don't exist, the system collapses." That inference is **false**.

---

## III.6 Closure of Part III

At this point:
- ✅ Compression alone does not yield persistence
- ✅ Stabilizers are necessary and sufficient for survivor status
- ✅ Survivors are finite, contextual, and revisable
- ✅ Objects are survivor-stabilizer pairs
- ✅ No identity, time, or dynamics assumed

**Next question**: If multiple survivors exist, how can they coexist without inducing collapse?

This is addressed in **Regimes and Defect-Mediated Interaction** (Part IV / NFC Corpus).

---

## Collapse-Gate Audit

| Check | Status |
|-------|--------|
| No identity assumed | ✅ Pass |
| No time introduced | ✅ Pass |
| Stabilizers not symmetries | ✅ Pass |
| Survivors not guaranteed | ✅ Pass |
| Objects derived, not primitive | ✅ Pass |

**Audit Result:** ✅ Clean

---

## References

- PASS Theorem: `theorems/pass_theorem.md`
- Regime Structure: `theorems/regime_structure.md` (next)
- Toy 𝕌₈: `toys/toy_u8.md`
