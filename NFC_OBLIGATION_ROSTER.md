# NFC Obligation Roster — Authoritative Cross-Book Reconciliation

*Produced L+39 by the dedicated reconciliation pass registered at L+38
(Book VII rem:obligation-conventions). This roster is the single
authoritative partition of every `ob:`-labelled obligation in the
corpus. It is reconciled to the Canon Ledger, which remains the live
session-by-session record; this roster is a periodic snapshot and
carries its own date.*

**Snapshot basis:** corpus state as of L+39 (post VRP closure L+36, post
YM verification L+37, post cross-book integration L+38).
**Total `ob:`-labelled obligations corpus-wide:** 109 (110 distinct labels after the L+40 de-duplication of ob:cryst-EWALD).

---

## 1. The three accountings, reconciled

The L+38 note recorded that three frontier accountings coexist on
different bases. This roster reconciles them:

| Accounting | Basis | Count | What it measures |
|---|---|---|---|
| Syntactic `[O]`-tag census | environments tagged `\status{O}` | **4** | obligations marked open-unproved by tag |
| Curated named-obligations (Book VII) | governance-significant not-fully-discharged items | "13" (pre-VRP snapshot) | the audit roster |
| Reduced irreducible frontier (Book VII) | genuinely open deep mathematics | **4 distinct items** | mathematical distance to completion |
| **This roster (objective partition)** | discharge-language + status tag, all 109 | **see §2** | complete, mechanical, auditable |

The three are not contradictory; they measure different things. This
roster supplies the objective substrate they each curate from.

---

## 2. Objective partition of all 109 obligations

Classification by the discharge-language in each obligation's own title
together with its status tag. This is mechanical and complete; it does
**not** by itself resolve the discharge status of "base declarations"
(§2.5), whose discharge is recorded in their branch status proposition,
not in the obligation's own title.

### 2.1 Genuinely OPEN — 4 (the syntactic `[O]` census)
- `ob:rh-s1-formal` (RH) — O-RH.S1 Arithmetic Witness Assembly, formal statement.
- `ob:cryst-PHASE` (CRYST) — O-CRYST.PHASE Phase Problem, formal statement.
- `ob:cryst-PHASE-progress` (CRYST) — O-CRYST.PHASE current status/remaining frontier.
- `ob:bio-BND-open` (BIO) — O-BIO.BND Boundary Self-Organization, reduced frontier.

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
(10) is exactly the reduced irreducible frontier (RH×2 blocks + SM
matter), confirming §3 against the branch-level evidence. The roster is
now fully mechanical: every one of the 109 ob: labels has a determined
category.

---

## 3. The reduced irreducible frontier (deep open mathematics) — verified

Book VII's 4-item reduced frontier, verified L+39 against the live
labels:
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

- **Genuinely open (`[O]`):** 4 — all toolkit-boundary (RH, CRYST×2, BIO).
- **Deep open mathematics (reduced frontier):** 4 — RH×2, SM, GR.
- **Conditionally discharged with live residual:** 31 (incl. full VRP arc).
- **Fully discharged / bridge-discharged:** 12.
- **Base declarations (62):** 52 conditionally established / endpoint-discharged at named scope; **10 are the live deep frontier** (RH orbit grammar ×3, RH packet synthesis ×5, SM matter ×2) — exactly the reduced irreducible frontier.
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
