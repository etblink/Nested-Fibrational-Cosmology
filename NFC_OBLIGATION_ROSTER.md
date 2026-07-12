# NFC Obligation Roster — Authoritative Cross-Book Reconciliation

*Produced L+39 by the dedicated reconciliation pass registered at L+38
(Book VII rem:obligation-conventions). This roster is the single
authoritative partition of every `ob:`-labelled obligation in the
corpus. It is reconciled to the Canon Ledger, which remains the live
session-by-session record; this roster is a periodic snapshot and
carries its own date.*

**Snapshot basis:** corpus state as of L+39 (post VRP closure L+36, post
YM verification L+37, post cross-book integration L+38).
**Total `ob:`-labelled obligations corpus-wide (current, MIG-052):** 111 distinct `ob:` labels, of which 100 are `obligation`-environment labels (the generated accounting II basis) and 11 are carried by other environments (remark-tagged etc., a registered convention wrinkle, §4). *(Historical snapshot: 109 at L+39 / 110 distinct labels after the L+40 de-duplication of ob:cryst-EWALD; the L+56 split retained `ob:vrp-charge-quant` and MIG-052 registered `ob:NS-common-state-bridge`, bringing the current distinct-label total to 111.)*

---

## 1. The three accountings, reconciled

The L+38 note recorded that three frontier accountings coexist on
different bases. This roster reconciles them:

| Accounting | Basis | Count | What it measures |
|---|---|---|---|
| Syntactic `[O]`-tag census | environments tagged `\status{O}` | **6** *(MIG-052; snapshot value was 4, L+56 made it 5, MIG-052 adds `ob:NS-common-state-bridge`)* | obligations marked open-unproved by tag |
| Curated named-obligations (Book VII) | governance-significant not-fully-discharged items | "13" (pre-VRP snapshot) | the audit roster |
| Reduced irreducible frontier (Book VII) | genuinely open deep mathematics (internal canonical burdens only) | **5 distinct items** *(MIG-052 adds the internal NS common-state bridge; the external NS Stage-3 question is classified external and NOT counted)* | mathematical distance to completion |
| **This roster (objective partition)** | discharge-language + status tag, all 111 | **see §2** | complete, mechanical, auditable |

The three are not contradictory; they measure different things. This
roster supplies the objective substrate they each curate from.

---

## 2. Objective partition of all 111 obligations

Classification by the discharge-language in each obligation's own title
together with its status tag. This is mechanical and complete; it does
**not** by itself resolve the discharge status of "base declarations"
(§2.5), whose discharge is recorded in their branch status proposition,
not in the obligation's own title.

### 2.1 Genuinely OPEN — 6 (the syntactic `[O]` census; MIG-052 current)
- `ob:rh-s1-formal` (RH) — O-RH.S1 Arithmetic Witness Assembly, formal statement.
- `ob:cryst-PHASE` (CRYST) — O-CRYST.PHASE Phase Problem, formal statement.
- `ob:cryst-PHASE-progress` (CRYST) — O-CRYST.PHASE current status/remaining frontier.
- `ob:bio-BND-open` (BIO) — O-BIO.BND Boundary Self-Organization, reduced frontier.
- `ob:vrp-charge-quant` (Book III) — O_Charge.Quant-cont.b2, numeric isolation of Ω_B (remark-tagged `[O]`; added to this list by the L+56 split, see the L+56 addendum).
- `ob:NS-common-state-bridge` (NS) — Obstruction/Ledger Common-State Bridge (registered MIG-052; the single open NS obligation — see the MIG-052 addendum below).

### 2.2 CONDITIONALLY DISCHARGED at named scope (live residual) — 31
Includes the entire VRP dynamical-core arc (9 items, Book III) plus
branch conditional discharges. These are **not open** and **not fully
done**: each carries a named residual hypothesis or scope. VRP arc:
`ob:vrp-entropy-univ`, `ob:vrp-energy-transfer`, `ob:vrp-ham-domain`,
`ob:vrp-ham-time`, `ob:vrp-mass-sector`, `ob:vrp-time-encode`,
`ob:vrp-time-reversible`, `ob:vrp-phase-sync`, `ob:vrp-temp-equil`.
Branch conditional discharges: BIO (5), CRYST (3), LING (1), SCC (2),
SM (1), SPEC (3), YM (7 incl. Clay B1/B3 + SVC + WeakGlue-standalone +
B3-A2 + reserve).

### 2.3 BRIDGE-DISCHARGED `[B]` — 2
- `ob:spec-CI`, `ob:spec-CD` (SPEC) — continuum interfaces discharged at bridge force.

### 2.4 FULLY DISCHARGED (title says "Discharged"/"Resolved", no residual) — 10
`ob:vrp-energy-form` (Book III, resolved by characterization),
`ob:ling-REC-open`, `ob:scc-weakglue`, `ob:scc-mcs`, `ob:spec-OP`,
`ob:spec-TR`, `ob:spec-NL`, `ob:spec-GC`, `ob:spec-END`,
`ob:B1-ClaySpec` (YM).

### 2.5 BASE DECLARATIONS (discharge recorded in branch status, not in title) — 62
Original obligation statements in branch endpoint/status tables. Their
discharge status is asserted by the branch's status proposition (e.g.
prop:YM-status confirms YM O-ID/RIG/ENC/GLOB/CLU discharged at [C]), not
in the obligation's own title. **This bucket is heterogeneous** and
splits into:
- *Branch-endpoint-discharged* (the BIO/CRYST/LING/SM/SPEC base
  realization/ledger/margin/no-channel/descent obligations, closed by
  their `-END` endpoint theorems and branch status propositions).
- *Live deep frontier* (the genuinely open mathematics; see §3).

**Completed L+41 — per-label discharge trace of the 62 base
declarations.** Each branch's endpoint theorem or status proposition
was read and the 62 base declarations partitioned exactly:

- **Live deep frontier (10)** — the genuinely open mathematics, matching
  the reduced irreducible frontier of §3:
  - RH orbit grammar (3): ob:rh-sf-logderiv-legality,
    ob:rh-sf-trace-pairing-law, ob:rh-sf-d2-audit.
  - RH packet-local synthesis (5): ob:rh-tloc-L3, L4, L5, L6, L7.
  - SM matter content (2): ob:SM-matter, ob:SM-IDcont-TV.
  (GR global curvature-subcriticality, the 4th reduced-frontier item,
  is tracked as def:curv-subcrit-global, outside the ob: namespace.)

- **Conditionally established / endpoint-discharged at named scope (52)**
  — discharge asserted by the branch endpoint theorem or status
  proposition, not the obligation's own title:
  - *Standard-branch endpoint-conditional* (18): each named in its
    branch endpoint theorem's conditional bracket and proved by its own
    theorem — BIO {REP, MET, FID, NC, BND, HER}; CRYST {PR, GAP, LAT,
    NC, SG, DOM, EWALD}; LING {CR, CL, CM, NC, GD}.
  - *Branch endpoint theorems* (2): ob:cryst-END, ob:ling-END
    (conditionally discharged "endpoint reached under stated conditions").
  - *Extension obligations at own scope* (11): BIO {EVO, MULTI,
    EVO-pop-bridge}; LING {REC, SEM, SEM-open, rec-infty,
    rec-infty-bridge, SEM-ref-open, ref-probe-nomination, ref-formal}.
  - *CERT-PROJ conditionally-established* (21): RH {RH4, RH5, RH6};
    SM {coupling-transfer, coupling-transfer-full, harmonization, higgs};
    SCC {rh-d1-full}; SPEC {frontier-min, a CERT-PROJ frontier marker
    awaiting YM/GR CERT-CLOSE}; YM {O-YM-SLC, O-YM-WeakGlue, O-ID, O-RIG,
    O-ENC, O-GLOB, O-CLU, O-ID-cont, B2, Planck-SI-calibration} — the
    closure stack confirmed at [C] by prop:YM-status (verified L+37).

**Verification:** the live-frontier subset of the base declarations
(10) accounts for the `ob:`-labelled part of the reduced irreducible
frontier that lives in the base-declaration bucket (RH×2 blocks + SM
matter). It is **not** the whole reduced frontier: the reduced
irreducible frontier (§3) has **5** items, of which GR is tracked
through a different convention (`def:curv-subcrit-global`, outside the
`ob:` namespace) and the NS common-state bridge
(`ob:NS-common-state-bridge`, MIG-052) is a genuinely-open `[O]`
obligation (§2.1), not a base declaration. The roster is fully
mechanical: every one of the 111 `ob:` labels has a determined
category, and the category counts sum to 111
($6+31+2+10+62$).

---

## 3. The reduced irreducible frontier (deep open mathematics) — verified

The reduced irreducible frontier (Book VII's original 4-item list,
extended to **5** by MIG-052; internal canonical burdens only),
verified against the live labels:
1. **RH arithmetic orbit grammar** (first hard block) — live labels
   `ob:rh-sf-logderiv-legality`, `ob:rh-sf-trace-pairing-law`,
   `ob:rh-sf-d2-audit`.
2. **RH packet-local synthesis** (second hard block) — live labels
   `ob:rh-tloc-L3`..`L7` (phase detectability, phase-spacing, Gram,
   leakage, compression).
3. **SM matter content** — `ob:SM-matter`, `ob:SM-IDcont-TV`,
   `ob:O-ID-cont` (continuum identification at full canonical force).
4. **GR global curvature-subcriticality** — tracked as
   `def:curv-subcrit-global` (GR), **not** an `ob:` label: GR uses a
   fourth tracking convention (definition-as-frontier-marker). Flagged.
5. **NS obstruction/ledger common-state bridge** *(internal; added
   MIG-052)* — `ob:NS-common-state-bridge`: a common temporal state
   carrying both the level-stock window obstruction and the
   contracting increment ledger, with a proved state-evolution law,
   a uniform same-functional contraction (or equivalent uniform
   product estimate), a two-sided same-state comparison (or direct
   closed contracting recurrence), and complete channel accounting.
   **External, deliberately not counted here:** NS unconditional
   global regularity (Stage-3, Clay) remains classified external and
   must never be silently merged into this internal count.

The reduced frontier is consistent with the current live labels. The
VRP closure (L+36) does **not** touch the reduced frontier: every VRP
obligation is conditionally discharged or characterized, none is a deep
open item. The VRP arc therefore adds 0 to the reduced frontier and 0
to the `[O]` census, while adding 9 conditionally-discharged items to
the governance roster.

---

## 4. Convention wrinkles and registered defects

1. **Four tracking conventions coexist:** `[O]`-tagged remarks (Book
   I–III), `[C]`-tagged `openobligation` environments (YM and most
   branches), bridge-tagged `[B]` (SPEC continuum), and
   definition-as-frontier-marker (GR `def:curv-subcrit-global`). The
   `[O]` census sees only the first.
2. **RESOLVED L+40 — duplicate label `ob:cryst-EWALD`:** was two
   distinct `\label{ob:cryst-EWALD}` in NFC_CRYST_Branch.tex (one
   "Ewald/Fourier Bridge" declaration, one "Conditionally Reduced"
   reduction). Verified to have **zero references** by any mechanism
   corpus-wide, so the fix was safe with no rewiring: the reduction was
   renamed `ob:cryst-EWALD-reduced`, the declaration keeps
   `ob:cryst-EWALD`. CRYST recompiles with zero multiply-defined
   warnings; corpus collision count 13 → 12. The remaining 12 are
   benign `sec:*` section-name recurrences (harmless across separate
   compiles) plus three cross-book theorem/def duplicates
   (cor:conditional-no-unconditional, def:transport-invariant,
   thm:governing) — a separate lower-priority class that does not
   corrupt this roster.

---

## 5. Reconciled headline

- **Genuinely open (`[O]`):** 6 *(MIG-052)* — RH, CRYST×2, BIO, Book III charge-quant (L+56), NS common-state bridge (MIG-052).
- **Deep open mathematics (reduced frontier, internal):** 5 *(MIG-052)* — RH×2, SM, GR, NS common-state bridge; the external NS Stage-3 question is classified external and not counted.
- **Conditionally discharged with live residual:** 31 (incl. full VRP arc).
- **Fully discharged / bridge-discharged:** 12.
- **Base declarations (62):** 52 conditionally established / endpoint-discharged at named scope; **10 are the `ob:`-labelled live deep frontier in this bucket** (RH orbit grammar ×3, RH packet synthesis ×5, SM matter ×2). These 10 are the base-declaration part of the reduced frontier; the full reduced irreducible frontier is **5 items** (§3), adding GR (tracked as `def:curv-subcrit-global`) and the NS common-state bridge (`ob:NS-common-state-bridge`, a genuinely-open `[O]` obligation in §2.1).
- The genuinely-open and deep-frontier sets barely overlap (RH only);
  the corpus's "what is open" depends on which question is asked, and
  this roster answers all of them on one page.

## 6. NFR cross-branch defect-localization (reference, not promotion; added L+44)

Nested Fibrational Realization (NFR; Speculative Holding register,
restricted bridge tool) provides a status-preserving cross-branch view
of part of this roster's live frontier. Per the L+44 NFR-integration
assessment (NFC_NFR_INTEGRATION_ASSESSMENT.md), NFR is **not promotable**
(fails branch legitimacy and the promotion law; self-disclaims both) but
is a legitimate admissible-import organizer. Its defect ledgers localize
roster obligations already tracked:

| NFR ledger | Roster obligations it localizes | Roster category |
|---|---|---|
| d_scp^YM,C (d_ID,d_RIG,d_ENC,d_GLOB,d_CLU) | YM O-ID/RIG/ENC/GLOB/CLU | §2.5 CERT-PROJ conditionally-established |
| d_scp^GR,B (real,deform,compat,closure,extension) | GR bridge-stack; def:curv-subcrit-global | reduced frontier Item 4 |
| d_intf^C (type,functor,compat,regime) | YM/GR interface defect | (cross-branch, not a single ob:) |
| d_mat^K4 | SM matter content (ob:SM-matter, ob:SM-IDcont-TV) | §3 reduced frontier Item 3 |

This is a tracking cross-reference under import discipline; it changes no
status and promotes nothing. The NFR K4 structural datum
(M_SM^K4,struct → T_NFR^dist) remains a firewalled structural-only
observation, outside the obligation namespace.

---

*Authoritative as of L+39. Update only at a dedicated reconciliation
pass; the Canon Ledger is the live record between snapshots.*

---

### L+56 update — O_Charge.Quant-cont split (in-toolkit obligation sharpened)

`ob:vrp-charge-quant` (O_Charge.Quant-cont) is sharpened into three sub-items (Book III):
- **O_Charge.Quant-cont.a** — charge finite-carrier continuum survival: **[C] discharged** by `thm:vrp-charge-continuum-survival` (finite charge set stays isolated under a faithful Book VI bridge; def:continuum-bridge / thm:continuum-bridge-schema).
- **O_Charge.Quant-cont.b1** — abstract frequency-lattice survival: **[C] discharged** by `cor:vrp-frequency-lattice-survival` (Ω_B ≅ ℤ^r survives qua character lattice, from phase-frequency Pontryagin duality).
- **O_Charge.Quant-cont.b2** — numeric isolation of Ω_B as a subset of ℝ: **[O] retained** (`ob:vrp-charge-quant`, now scoped to b2). A f.g. subgroup of ℝ of rank ≥ 2 with rationally-independent generators is dense; isolation needs a commensurability/rank-one/uniform-separation hypothesis not licensed by source data and barred from import by anti-smuggling.

Net: [O] count unchanged at 5 (b2 remains the open tag); the obligation is now properly split, with the charge and abstract-frequency halves conditionally discharged. Corrects the L+46 over-coarse conflation of charge and frequency continuum survival as "the identical deferral."


---

### MIG-052 update — NS common-state bridge registered (corrected delivery)

**New obligation:** `ob:NS-common-state-bridge` (NS branch, `[O]`) — the
obstruction/ledger common-state bridge. Its burden (canon text is
authoritative): a common temporal state carrying both the window
obstruction and the contracting/coercive quantity; a proved
state-evolution law (including an interface-burden evolution law with a
genuine boundary-loss channel); a **uniform** same-functional
contraction V(T_nX) ≤ λV(X), λ<1, uniformly on the late tail with
controlled remainder, or an equivalent uniform product/joint
contraction estimate (individual per-step spectral-radius statements
for time-dependent T_n are insufficient); a genuine two-sided
same-state comparison a𝔇_k ≤ 𝒪_NS(W_k) ≤ b𝔇_k + ρ_k on the declared
threshold regime, or a direct closed contracting recurrence for 𝒪_NS;
and explicit accounting of every channel (level stock, transported
survivor, transported loss (1−Θ_n)C_n, interior/boundary defect
increments, renewal inflow, redistribution, remainder). The
state-vector and discounted-memory frames are research directions
only; neither is assumed; the discounted comparison I_n ≍ 𝔅̂^(ρ)_n
alone is insufficient.

**Context:** `hyp:NS-alpha` withdrawn as ill-typed as a canonical
identity and unsupported by current canon (level stock vs. step
increment; equation and label retained as historical intake only);
`hyp:NS-IDC-i/ii` re-scoped subsidiary and insufficient (Ψ^int occurs
inside the IDC-i hypothesis itself but has no independent preceding
definition, no projection/decomposition theorem from the canonical Ψ,
and no bridge to the Book III interior increment E_n).

**Branch posture:** NS = **CERT-PROJ / open-common-state-frontier**;
the former domain-bounded conditional CERT-CLOSE wording is
superseded; no NS closure claim may be cited at CERT-CLOSE force while
the bridge is open; no endpoint-regularity claim.

**The four accounting bases (kept separate; never summed):**
1. Syntactic `[O]` census: **6**.
2. Named-obligation accountings: **111** distinct `ob:` labels
   corpus-wide (all environments); **100** on the
   obligation-environment basis used by the generated accounting II.
3. Reduced irreducible frontier (internal): **5**, now including the
   NS common-state bridge; the external NS Stage-3 question stays
   classified external and uncounted.
4. Branch posture: per-branch A1 status proposition (NS: CERT-PROJ,
   open common-state frontier).
