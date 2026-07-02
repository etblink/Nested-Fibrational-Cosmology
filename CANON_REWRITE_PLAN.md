# NFC Canon Rewrite Plan (File-by-File)

**Produced:** Phase 4 (plan only — **no edits applied**).
**Governs:** the Phase-7 incremental edit sequence.
**Every entry obeys** `REWRITE_POLICY.md`. No plan item strengthens a status, changes a `\status{}` value, or touches a theorem/obligation label. Every planned change is either (i) a comment-header edit, (ii) an added `[R]` Current Status Capsule that *points at* existing authority, (iii) a section-title rename preserving the label, or (iv) an intake marker. Scaffold edits are tracked separately.

**Risk legend:** LOW = comment-only or additive `[R]` capsule; MED = in-body prose relabel / section retitle in a branch; HIGH = spine-book in-body edit (feeds many branches) or touching a `\status`-tagged proposition (⇒ always REVIEW_NEEDED, never auto-applied).

**Required test after *every* file:** two-pass `pdflatex` (exit 0, page count stable); corpus-wide label/ref audit (0 dangling, 12 known dup labels, no new `cap:` collision).

---

## SPINE BOOKS

### NFC_Book_I.tex — Primitive Relational Foundations
- **Front-matter problem:** none of substance. Header is a clean status legend; F-4 applies (legend omits `[B]`).
- **Body/final-status state:** foundational `[U]/[D]` layer; stable. No branch-posture claims.
- **Stale labels to repair:** F-4 only — add `[B]` line to the `%%` status legend (comment-only).
- **Proposed capsule:** spine-book capsule `cap:book1-status` after `\section*{I.0 Purpose}`: "Foundational [U]/[D] layer; stable. Governs: Observational Quotient Theorem etc. See Book VII for governance rules."
- **Sections to rename:** none.
- **Preserve as intake:** I.0 Purpose (already purpose-framed; fine).
- **Labels/refs that must not change:** `thm:governing` (Book I copy — part of the known benign cross-book duplicate set; do **not** touch).
- **Risk:** LOW.

### NFC_Book_II … NFC_Book_VI (.tex)
- **Front-matter problem:** F-4 legend only.
- **Body/final-status state:** `[U]/[C]` stable. Book II has honest "remaining gap" language (CURRENT, leave). Book III has the VRP arc (all `[C]`/characterized — leave) and "deferred" technical scoping (CURRENT, leave).
- **Stale labels to repair:** F-4 legend line per file (comment-only).
- **Proposed capsule:** spine-book capsule per file (`cap:book2-status` … `cap:book6-status`) after each `X.0 Purpose`.
- **Sections to rename:** none.
- **Preserve as intake:** each `X.0 Purpose`.
- **Labels/refs that must not change:** `thm:governing` copies (II,III,IV,VI); `def:transport-invariant` (II,IV — benign dup); `cor:conditional-no-unconditional` (VI). Leave all.
- **Risk:** LOW (comment + additive capsule). Book III capsule MED-flagged only because III is heavily cross-referenced — compile-check carefully.

### NFC_Book_VII.tex — Governance
- **Front-matter problem:** F-4 legend.
- **Body/final-status state:** governance rules (high authority, CURRENT). But contains three data-staleness items: **F-6** (Branch Status Table SM row vs. `sec:obligation-vs-frontier` — internal contradiction), **F-8** ("currently 13 items"), **F-9** (Branch Status Table omits BIO/CRYST/LING/SPEC).
- **Stale labels to repair:**
  - F-8: add forward-pointer sentence to `NFC_OBLIGATION_ROSTER.md` beside "(currently 13 items)"; keep "13" as dated. **LOW.**
  - F-9: add BIO/CRYST/LING/SPEC rows to `sec:status-table`, each sourced verbatim from that branch's A1 posture. **HIGH** (spine in-body table edit) — stage carefully, compile after.
  - F-6: **REVIEW_NEEDED.** Do not edit the SM row until reviewer confirms whether "CouplingTransfer" belongs in the remaining-work column given `thm:SM-coupling-transfer-full`. Flagged, not applied.
- **Proposed capsule:** spine-book capsule `cap:book7-status`.
- **Sections to rename:** none.
- **Labels/refs that must not change:** `thm:governing` (VII), `cor:conditional-no-unconditional` (VII), `sec:status` (VII — dup with SCC/YM, benign), `def:open-obligation`, `def:toolkit-boundary-frontier`.
- **Risk:** LOW (capsule, F-8) / HIGH (F-9 table) / REVIEW_NEEDED (F-6).

---

## BRANCH BOOKS

### NFC_BIO_Branch.tex — Biology (the flagship primary-problem case)
- **Front-matter problem:** A-1 (header "pre-closure — all theorem shells carry open obligations" — SUPERSEDED), A-5/A-6 ("Prospective Derived Branch" — HISTORICAL), F-adjacent (initial endpoint / deferred — HISTORICAL, preserve).
- **Body/final-status state:** REP–END discharged `[C]`; `rem:bio-two-status` = replication–heredity endpoint reached; EVO/MULTI conditionally advanced; `ob:bio-BND-open` = the one syntactic `[O]` (toolkit-boundary residual).
- **Stale labels to repair:** rewrite `%%` header status line (mark old as intake, add current one-liner + pointer to `rem:bio-two-status`); mark `\author{…Prospective…}` per Rule 1; add "(constitutional intake)" marker to the Purpose seed's "initial endpoint … deferred" sentence (no wording change to the sentence itself).
- **Proposed capsule:** `cap:BIO-status` after `\maketitle`/before `sec:bio-purpose`. Posture line from `rem:bio-two-status`. Frontier line: "syntactic [O]: 1 (`ob:bio-BND-open`, toolkit-boundary); reduced frontier: none; posture: replication–heredity endpoint, EVO/MULTI extensions conditional."
- **Sections to rename:** none required (Two-Status Reading is fine).
- **Preserve as intake:** `sec:bio-purpose`, `rem:bio-strategic-path`, "initial endpoint" sentence.
- **Labels/refs that must not change:** all `ob:bio-*`, `def:bio-*`, `thm:bio-*`, `rem:bio-two-status`; `sec:arena` (dup, benign).
- **Risk:** LOW (header comment + additive capsule) / MED (in-body intake marker on Purpose sentence).

### NFC_CRYST_Branch.tex — Crystallography
- **Front-matter problem:** A-2 (header "pre-closure" — SUPERSEDED), A-5/A-6, E-1 ("pre-closure scope" in `rem:cryst-legitimacy` — HISTORICAL), F (initial endpoint — HISTORICAL).
- **Body/final-status state:** `prop:cryst-status` = Conditional CERT-CLOSE pending two ε-convergence conditions + phase frontier; `ob:cryst-PHASE`, `ob:cryst-PHASE-progress` = the two syntactic `[O]`.
- **Stale labels to repair:** header line (→ pointer to `prop:cryst-status`); mark `\author` intake; add "(at constitution)" parenthetical to the `rem:cryst-legitimacy` pre-closure sentence (E-1); "initial endpoint" left verbatim, oriented by capsule.
- **Proposed capsule:** `cap:CRYST-status`. Frontier line: "syntactic [O]: 2 (phase problem, toolkit-boundary); reduced frontier: none; posture: conditional CERT-CLOSE (diffraction-periodicity-symmetry)."
- **Sections to rename:** none.
- **Preserve as intake:** `Legitimacy Analysis and Branch Constitution`, UBLT pre-analysis.
- **Labels/refs that must not change:** all `ob:cryst-*` (incl. the de-duplicated `ob:cryst-EWALD` / `ob:cryst-EWALD-reduced` pair — leave exactly as is), `thm:cryst-*`, `prop:cryst-status`; `sec:*` dups.
- **Risk:** LOW/MED.

### NFC_LING_Branch.tex — Linguistics
- **Front-matter problem:** A-3 (header — SUPERSEDED), A-5/A-6, F (initial endpoint — HISTORICAL).
- **Body/final-status state:** contrast+recursion+context-response closed; reference semantics conditional at two scopes; `rem:ling-two-status`, `rem:ling-REC-full-status`; no syntactic `[O]` in the branch.
- **Stale labels to repair:** header line (→ `rem:ling-two-status`); mark `\author` intake; orient the Purpose seed via capsule.
- **Proposed capsule:** `cap:LING-status`. Frontier line: "syntactic [O]: 0; reduced frontier: none; posture: contrast+recursion+context-response closed, reference semantics conditional at two scopes." (One `[B]` bridge theorem `thm:ling-rec-infty-bridge` — capsule notes recursion-infinity carried at bridge force per Rule 7.)
- **Sections to rename:** none.
- **Preserve as intake:** `sec:ling-purpose`.
- **Labels/refs that must not change:** all `ob:ling-*`, `thm:ling-*` (incl. `thm:ling-rec-infty-bridge` `[B]`).
- **Risk:** LOW/MED.

### NFC_SPEC_Branch.tex — Spectroscopy (contains an internal supersession — highest-care branch)
- **Front-matter problem:** A-4 (header — SUPERSEDED), A-5/A-6, F.
- **Body/final-status state:** **two status propositions.** `prop:spec-current-status` (earlier, "prospective … no certified transition theorem") is contradicted by `prop:SPEC-status` (later, "CERT-CLOSE on gauge-response regime; O-SPEC.PR–END discharged"). B-1/M-1.
- **Stale labels to repair:**
  - header line (→ `prop:SPEC-status`); mark `\author` intake.
  - **B-1/M-1 — REVIEW_NEEDED:** relabel `sec:spec-current-status` title to "Constitutional Intake Status (superseded by `prop:SPEC-status`)" and add a one-line supersession pointer *inside* the proposition, **without deleting** the `\status`-tagged `prop:spec-current-status`. Because this touches the presentation of a `\status`-tagged proposition, it is **not auto-applied** — reviewer confirms the relabel is acceptable.
- **Proposed capsule:** `cap:SPEC-status`. Per Rule 7: "CERT-CLOSE on the gauge-response regime; continuum interfaces licensed at bridge `[B]` (`ob:spec-CI`, `ob:spec-CD`); matter-rich regime open, gated on SM. syntactic [O]: 0; reduced frontier: none (SM-gated MAT is downstream)."
- **Sections to rename:** `sec:spec-current-status` (title only; label preserved) — REVIEW_NEEDED.
- **Preserve as intake:** `sec:spec-purpose`, `prop:spec-current-status` (retained, marked superseded).
- **Labels/refs that must not change:** all `ob:spec-*` (incl. `ob:spec-CI`/`ob:spec-CD` `[B]`), `thm:spec-*`, both status propositions' labels.
- **Risk:** MED / REVIEW_NEEDED (B-1).

### NFC_YM_Branch.tex — Yang–Mills
- **Front-matter problem:** A-7 (header "CERT-PROJ; not yet CERT-CLOSE" — SUPERSEDED; the body's own `[R]` already states this is superseded).
- **Body/final-status state:** `prop:YM-status` = Conditional CERT-CLOSE at MSC-normalized NFC scope; B1/B2/B3 post-program `[O]`-at-Clay-scope but `[C]`-at-NFC-scope; the "Clay gaps" language is CURRENT and honest.
- **Stale labels to repair:** header line only (→ `prop:YM-status`; preserve old as intake note). Everything else CURRENT.
- **Proposed capsule:** `cap:YM-status`. "Conditional CERT-CLOSE (MSC-normalized NFC scope); B1/B2/B3 post-program (Clay-scope open, NFC-scope conditionally discharged). syntactic [O]: 0; reduced frontier: none directly (SM matter is downstream of YM); posture per `prop:YM-status`."
- **Sections to rename:** none.
- **Preserve as intake:** the `[R]` remark explaining the superseded CERT-PROJ language (already perfect — it *is* the model for how supersession should read).
- **Labels/refs that must not change:** all `ob:*` incl. `ob:YM-B1/B2/B3`, `ob:O-ID/RIG/ENC/GLOB/CLU`, `ob:O-ID-cont`; `sec:arena/descent/frontier/governance/imports/status/transfer` (dups, benign); `prop:YM-status`.
- **Risk:** LOW.

### NFC_SCC_Branch.tex — Structural-Capacity Cognition
- **Front-matter problem:** A-8 (header "CERT-PROJ at most" — SUPERSEDED).
- **Body/final-status state:** `prop:scc-status` `[U]`; STATE_OF_CANON = conditional CERT-CLOSE (MCS/UC/TSI). **C-2: mixed CERT-PROJ/CERT-CLOSE usage in body → line-by-line REVIEW_NEEDED** to separate historical-stage uses from current-posture uses.
- **Stale labels to repair:** header line (→ `prop:scc-status`). C-2 body occurrences: **REVIEW_NEEDED**, itemize during the edit pass; do not mass-edit.
- **Proposed capsule:** `cap:SCC-status`, posture from `prop:scc-status`. "syntactic [O]: 0; reduced frontier: none; posture: conditional CERT-CLOSE (MCS+UC+TSI)."
- **Sections to rename:** none.
- **Preserve as intake:** Front Block.
- **Labels/refs that must not change:** all `ob:scc-*`, `thm:scc-*`, `prop:scc-status`; `sec:*` dups; `sec:rh-screening` (dup with RH, benign), `ob:rh-d1-full` (lives in SCC).
- **Risk:** LOW (header+capsule) / REVIEW_NEEDED (C-2).

### NFC_GR_Branch.tex — Gravity
- **Front-matter problem:** **none** — A-11: header is CURRENT and matches `prop:gr-status`.
- **Body/final-status state:** domain-bounded conditional CERT-CLOSE; CK-corner extension `prop:gr-ck-corner-extension` `[C]`; global curvature-subcriticality open (`def:curv-subcrit-global`); two-status reading exemplary.
- **Stale labels to repair:** none. ("remaining gap" H-3, "current status" M-3, CERT-* C-3 all CURRENT.)
- **Proposed capsule:** `cap:GR-status` (for uniformity), posture from `prop:gr-status`, noting the CK-corner partial extension. "syntactic [O]: 0 (`def:curv-subcrit-global` is the reduced-frontier item, tracked as a definition-marker, not an `[O]` tag — the branch's fourth-convention frontier); reduced frontier: 1 (GR global curvature-subcriticality); posture: domain-bounded CERT-CLOSE + CK-corner extension."
- **Sections to rename:** none.
- **Preserve as intake:** Front Block.
- **Labels/refs that must not change:** all `ob:*`, `def:curv-subcrit-global`, `rmk:ck-gr-stability-bridge` `[B]`, `prop:gr-ck-corner-extension`, `thm:gr-domain-bounded`, `thm:gr-global`, `hyp:KPO3`; `sec:*` dups.
- **Risk:** LOW.

### NFC_NS_Branch.tex — Navier–Stokes
- **Front-matter problem:** A-12: header has no status line (not an error); add capsule for uniformity.
- **Body/final-status state:** `prop:NS-status` = domain-bounded conditional CERT-CLOSE; Stage-3 Clay external frontier; **D-3: the future-tense "will advance from frontier-blocked to Cond(K₀=7)-closed" remark (l.2622) → REVIEW_NEEDED** (is that advance now realized?).
- **Stale labels to repair:** D-3 REVIEW_NEEDED (do not edit). D-1/D-2 frontier-blocked uses are CURRENT.
- **Proposed capsule:** `cap:NS-status`, posture from `prop:NS-status`. "syntactic [O]: 0; reduced frontier: none (Stage-3 is external Clay, tracked as `thm:NS61` frontier); posture: domain-bounded conditional CERT-CLOSE."
- **Sections to rename:** none.
- **Preserve as intake:** Front Block; pre-canonical achievements remark.
- **Labels/refs that must not change:** `thm:NS61`, all `thm:NS*`, `prop:NS-status`, `cor:NS-*`; `sec:arena` dup.
- **Risk:** LOW / REVIEW_NEEDED (D-3).

### NFC_RH_Branch.tex — Riemann Hypothesis
- **Front-matter problem:** A-9 (header "Initial Canonical Draft" — HISTORICAL framing, no false status).
- **Body/final-status state:** `prop:RH-status` = CERT-PROJ; RH4–6 + S1 arithmetic frontier; transport-localization chain L1–L7. Contributes **2 of the 4 reduced-frontier items** (RH orbit grammar, RH packet synthesis) + `ob:rh-s1-formal` = one syntactic `[O]`.
- **Stale labels to repair:** header framing (add capsule; keep "Initial Canonical Draft" as dated provenance).
- **Proposed capsule:** `cap:RH-status`, posture from `prop:RH-status`. "syntactic [O]: 1 (`ob:rh-s1-formal`); reduced frontier: 2 (RH arithmetic orbit grammar; RH packet-local synthesis); posture: CERT-PROJ."
- **Sections to rename:** none.
- **Preserve as intake:** Branch Architecture and Governance.
- **Labels/refs that must not change:** all `ob:rh-*` (incl. `ob:rh-sf-*`, `ob:rh-tloc-L3..L7`, `ob:rh-s1-formal`), `prop:RH-status`; `sec:rh-screening` dup.
- **Risk:** LOW.

### NFC_SM_Branch.tex — Standard Model super-branch (most internally layered)
- **Front-matter problem:** A-10 (header "Initial Canonical Draft" — HISTORICAL).
- **Body/final-status state:** **three-layer status.** `prop:SM-status` (CERT-PROJ, baseline) → `prop:SM-status-reconciliation` (supersedes on internal ledger only → "conditionally intrinsic-structural closed, inherited-scope open") → `rem:sm-status-current`. `prop:SM-extspec-status` details SM-MAT/SM-HIGGS blocked at `[U]` by O_ID^cont. Contributes **1 reduced-frontier item** (SM matter via O_ID^cont). C-5: the CERT-PROJ of `prop:SM-status` is HISTORICAL (supersession already in-canon).
- **Stale labels to repair:** header (add capsule → reconciliation prop). Do **not** alter `prop:SM-status` (it is the preserved superseded baseline the reconciliation refers to — deleting/editing it would break `prop:SM-status-reconciliation`'s reference to "SM-Old").
- **Proposed capsule:** `cap:SM-status`, posture verbatim from `prop:SM-status-reconciliation`: "conditionally intrinsic-structural closed, inherited-scope open." Per Rule 7: explicitly note "inherits all open YM/GR obligations; SM-MAT/SM-HIGGS at structural `[C]`, blocked at `[U]` by O_ID^cont; no unconditional or empirical SM claim." "reduced frontier: 1 (SM matter content); syntactic [O]: 0."
- **Sections to rename:** none.
- **Preserve as intake:** Super-Branch Governance Preamble; `prop:SM-status` (the superseded baseline).
- **Labels/refs that must not change:** all `ob:SM-*`, `prop:SM-status`, `prop:SM-status-reconciliation`, `prop:SM-extspec-status`, `thm:SM-*`; scaffold F-1/F-2 repairs are in the Ledger, not here.
- **Risk:** LOW (header+capsule). Any touch to `prop:SM-status` = HIGH/REVIEW_NEEDED (and is not planned).

---

## Scaffold edits (tracked separately; not canon)

| File | Item | Change | Risk |
|---|---|---|---|
| NFC_CANON_LEDGER.md PART 4 | SM entry (F-1), YM entry (F-2) | Repair to current; quote old text in a dated "superseded description" block; add migration entries | LOW (scaffold) |
| NFC_STATE_OF_CANON.md | Register header "as of L+22" (F-3 context); tag-count table | Add "⚠ counts pending regeneration (see AUDIT_BASELINE census)"; do **not** guess new counts. Regenerate from Phase-5 metadata when available. | LOW / GENERATED-later |
| (new) MIGRATIONS.md | — | Create; append one entry per applied edit | LOW |

---

## Consolidated REVIEW_NEEDED queue (must be resolved by a human before or during Phase 7)

1. **F-3** — STATE_OF_CANON tag counts (443/209/685) vs. direct census (461/212/748): stale, or narrower convention? (Blocks regenerating that table.)
2. **F-6** — Book VII Branch Status Table SM row lists "CouplingTransfer" as remaining vs. `sec:obligation-vs-frontier` treating it as proved. Same-file contradiction.
3. **B-1 / M-1** — relabeling/superseding `prop:spec-current-status` (a `\status`-tagged proposition). Confirm the relabel-in-place approach.
4. **C-2** — SCC body CERT-PROJ occurrences: which are current vs. historical (line-by-line).
5. **D-3** — NS "will advance from frontier-blocked to Cond(K₀=7)-closed": realized yet?
6. **A-5 wording** — exact replacement subtitle for "Prospective Derived Branch" on the four title pages.
7. **F-5** — whether to ever rename the `openobligation` environment (deferred; not in this rewrite).

---

## Execution order for Phase 7 (per policy Part IV.5, lowest-risk first)

1. Scaffold: create `MIGRATIONS.md`; repair Ledger PART 4 (F-1/F-2); annotate STATE_OF_CANON (F-3 note).
2. Comment-only canon edits: `[B]` legend line in all 17 files (F-4); header status-line relabels (A-1..A-4, A-7, A-8) marking old as intake.
3. Additive `[R]` Current Status Capsules, branches first (BIO, CRYST, LING, SPEC, YM, SCC, GR, NS, RH, SM), then spine books.
4. In-body intake markers (Purpose-seed parentheticals; `\author` line notes).
5. Section-title renames (SPEC `sec:spec-current-status`) — **only after B-1 review**.
6. Spine-book table completion (Book VII F-9) — **HIGH**, compile-verify immediately.
7. Final consistency pass: full compile of all 17; corpus-wide label/ref audit; regenerate PDFs; regenerate any GENERATED count tables from Phase-5 metadata; produce final validation report + patch summary + unresolved-review list.

**Nothing in steps 1–7 is applied until this plan is approved.** Items 5, 6, and the entire REVIEW_NEEDED queue additionally require explicit human sign-off even after plan approval.
