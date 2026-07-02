# NFC Canon Authority Model

**Produced:** Phase 1 (planning only — no canon or scaffold file edited).
**Purpose:** Define an explicit, ordered authority hierarchy so that when
two places in the corpus disagree about a status, there is a
deterministic rule for *which text is treated as current* — and,
separately, a rule for *what may be done about the disagreement*
(flag-and-propose, never silent overwrite).

**Prime directive of this model:** Higher authority does **not** license
deleting or silently rewriting lower-authority text. When a
lower-authority passage conflicts with a higher-authority one, the
lower passage is either (a) confirmed as *constitutional intake /
historical* and clearly marked as such, or (b) flagged `SUPERSEDED`
with a migration entry pointing to the governing text, or (c) escalated
to `REVIEW_NEEDED`. **The canon's meaning, proof force, labels, and
scoped claims are preserved in every case** (per the core rule).

---

## 1. The Authority Hierarchy (highest → lowest)

The task specifies seven authority tiers. This model instantiates them
against the actual files, assigns each an explicit rank, and — crucially
— records *what each tier is actually authoritative about*. A tier is
not globally authoritative; it is authoritative **within its own
competence**. Mixing competences is the root cause of most findings in
`AUDIT_BASELINE.md`.

| Rank | Tier | Concrete instance(s) in this corpus | Authoritative **for** | NOT authoritative for |
|---|---|---|---|---|
| **A1** | Branch final status proposition (in-body, `\status`-tagged) | `prop:YM-status`, `prop:NS-status`, `prop:gr-status`, `prop:cryst-status`, `prop:SPEC-status`, `prop:RH-status`, `prop:scc-status`, `prop:SM-status`+`prop:SM-status-reconciliation`+`rem:sm-status-current`; for BIO/LING the `rem:*-two-status` + `-END` discharge theorems | **The current formal status of that one branch**, because it is *inside the canon*, carries a status tag, is proof-backed, and lives with the theorems it summarizes. This is the single most trustworthy statement of "where is this branch now." | Any *other* branch; corpus-wide counts; cross-branch frontier totals. |
| **A2** | Named failure frontier section (in-body, in the same branch) | `thm:*-frontier`, `def:toolkit-boundary-frontier` (Book VII), each branch's "Failure Frontier"/"Limits" section | **What remains genuinely open for that branch, at the declared scope.** Co-equal with A1 and cross-checks it: A1 says how far we got; A2 says what's left. If A1 and A2 (same branch) disagree, that is a *within-branch* defect → `REVIEW_NEEDED`. | Status of discharged items (that's A1's job). |
| **A3** | Updated closure ledger / updated obligation register (in-body) | Each branch's "Closure Ledger" / "Obligation Discharges" section; the `openobligation` environments themselves | **The per-obligation discharge basis and named conditions** for that branch. The authority that says *why* an item is `[C]` and under what hypotheses. | The rolled-up branch posture (A1) or corpus totals. |
| **B1** | Current live canon ledger — session record | `NFC_CANON_LEDGER.md` **PART 9 (Recent Promotions Log)** + `NFC_STATE_OF_CANON.md` session log (through L+63) | **The chronological truth of what happened and when**, corpus-wide. This is the live, append-only record and is authoritative for *sequence and provenance* ("O_ID^cont_TV discharged at L+20"). It is the tie-breaker across branches when in-body A1/A3 texts are silent about corpus-level context. | Superseding an in-body A1 status. A log entry is a *record that a change occurred in canon*; the canon text is the change. If the log and the canon body disagree, the **canon body wins for "what is true now"**, and the divergence is a `REVIEW_NEEDED` (the log may record a session whose file-write did not persist — the corpus itself warns of exactly this, STATE_OF_CANON "standing cautions" (3)). |
| **B2** | Latest reconciled obligation roster (dated snapshot) | `NFC_OBLIGATION_ROSTER.md` (Authoritative as of L+39 + L+56 addendum) | **The reconciled partition of all 110 `ob:` labels across the four frontier accountings.** The best existing single source for "how many obligations, in which accounting." Self-scoped and self-dated — a model citizen. | Anything after its snapshot date not covered by its addenda; per-theorem force (that's A3). |
| **B3** | Corpus-wide state snapshot — summary tables | `NFC_STATE_OF_CANON.md` top summary table + branch status summary table | **A convenient corpus-wide dashboard.** Authoritative *only* where it agrees with A1–A3/B1–B2; where it disagrees it is presumed stale (it is a periodic hand-maintained snapshot). Its branch-status *summary* table is currently the freshest single cross-branch view and is a good scaffolding source, but individual cells must be validated against each branch's A1. | Formal per-branch status when it conflicts with that branch's A1 (see F-3: its tag counts are stale vs. a direct census). |
| **C1** | Spine cross-branch governance tables (in-body, Book VII) | Book VII `sec:status-table` (Branch Status Table); `sec:obligation-vs-frontier` | **The governance *rules* for status (inflation ban, transfer law, frontier stratification).** These rules are top-tier authority (see §4). But Book VII's *data* tables (which branch is where, the "13 items" count) are **snapshots like any other** and are demonstrably stale (F-6, F-8, F-9). Rule content = high authority; data content = B3-level. | Per-branch current status data (defer to each branch's A1); it omits 4 branches entirely (F-9). |
| **D1** | Front block / constitutional intake (in-body, per file) | Each file's `%%`-comment header status line; `\author{… Prospective Derived Branch}`; "Purpose and Canonical Seed" / "Strategic path" sections | **The original constitution of the branch: its founding question, its seed obligations, its intended endpoint.** This is *historically* authoritative and must be **preserved** — it explains how the branch was constituted (Phase 3 Rule 4). It is **not** authoritative for current status. | Current status. Its "Prospective / pre-closure" language is intake, not a live posture (this is the crux of the primary problem). |
| **D2** | Purpose / motivation / strategic-path language (in-body) | `rem:*-strategic-path`, "motivation" prose | **Why the branch exists and what its ambition is.** Never load-bearing (`[R]`). Preserve as-is. | Any status claim whatsoever. |
| **E1** | Generated scaffold outputs | The 17 `.pdf` files; (future) JSON/CSV/dashboard exports | **Nothing, on their own.** A generated artifact's authority is exactly the authority of its source. It is *never* hand-edited (Phase 3 Rule 8; acceptance criterion 6). | Everything. Fix upstream, regenerate. |

**One-line statement of the hierarchy for status of a given branch:**
> A1 (that branch's status proposition) governs current status, cross-checked by A2/A3 of the same branch; B-tier snapshots and C1 tables are reconciled *to* it, not over it; D-tier front matter is preserved as constitutional intake; E-tier is regenerated, never edited.

---

## 2. Conflict-resolution procedure (the only permitted procedure)

For any detected conflict between two passages P_hi (higher rank) and
P_lo (lower rank):

1. **Never auto-overwrite.** Do not edit P_lo to match P_hi as a
   reflex.
2. **Classify P_lo** using the Phase 2 vocabulary
   (CURRENT / HISTORICAL / SUPERSEDED / AMBIGUOUS / GENERATED).
3. **If P_lo is D-tier (front block / purpose / intake):** default
   classification is **HISTORICAL**. Treatment = *preserve verbatim*,
   add a neighboring Current Status Capsule (Phase 3 Rule 2) and/or an
   "(constitutional intake)" marker (Phase 3 Rule 1). The intake text
   is not wrong; it is being read out of its temporal context.
4. **If P_lo is a B/C-tier snapshot or table:** classification is
   **SUPERSEDED** *only if* a specific A-tier text in the relevant
   branch contradicts it. Treatment = propose a minimal edit to the
   snapshot **plus** a migration entry; the underlying canon is
   untouched.
5. **If the conflict is between two A-tier texts of the *same branch*,
   or between two sections of the *same spine book* (e.g. F-6):**
   classification is **AMBIGUOUS → REVIEW_NEEDED**. Do **not** pick a
   winner mechanically; a same-tier in-canon contradiction is a
   semantic question requiring human sign-off (core rule: no semantic
   alteration without explicit review).
6. **If P_hi is B1 (session log) and P_lo is an A-tier canon body:**
   invert the usual direction — the **canon body is treated as current**
   and the log entry is flagged `REVIEW_NEEDED` as a possible
   non-persisted write (the corpus's own standing caution 3). The log
   is authoritative for *history*, not for *overriding present canon*.
7. **Record every conflict** in `STALE_LABEL_AUDIT.md` (file, section,
   phrase, classification, reason, proposed treatment). Nothing is
   resolved silently.

---

## 3. The four frontier accountings — kept permanently separate

Per the task's hard requirement ("Never collapse these into a single
number"), the model defines four *distinct* accountings, each with its
own authoritative source, its own current value, and an explicit
statement of what it does and does not measure. **No arithmetic
relationship among these four is asserted or implied.** They are four
different questions.

| # | Accounting | Definition | Authoritative source (tier) | Current value (this audit) | Measures | Does **not** measure |
|---|---|---|---|---|---|---|
| **I** | **Syntactic `[O]` census** | Count of environments literally tagged `\status{O}` | Direct grep over `.tex` (mechanical); mirrored by B2 roster §2.1 | **5** (`ob:vrp-charge-quant`/b2, `ob:bio-BND-open`, `ob:cryst-PHASE`, `ob:cryst-PHASE-progress`, `ob:rh-s1-formal`) | What is *syntactically flagged* open right now | Whether an untagged item is secretly open; depth/importance |
| **II** | **Curated named-obligation roster** | Governance-significant obligations with labels, scopes, discharge criteria | C1 Book VII `sec:obligation-vs-frontier`; B2 roster (the reconciled partition of all 110 `ob:` labels) | Book VII text says **"13"** (flagged HISTORICAL/pre-VRP by B2); B2's own mechanical partition covers **110** labels sorted into 5 buckets | The audit surface — every named burden, discharged or not | "How open" the program is (most of the 110 are `[C]`) |
| **III** | **Reduced irreducible frontier** | Smallest set of genuinely open *deep mathematics* after all reductions | C1 Book VII `sec:obligation-vs-frontier` + B2 roster §3 | **4** (RH orbit grammar; RH packet-local synthesis; SM matter content via O_ID^cont; GR global curvature-subcriticality) | Genuine mathematical distance to completion | Bookkeeping/governance items; anything conditionally discharged |
| **IV** | **Branch posture / closure status** | Per-branch closure level (CERT-PROJ / domain-bounded CERT-CLOSE / conditional CERT-CLOSE / CERT-CLOSE) | A1 status proposition of each branch | 10 branch postures — see §5 table | Where each branch sits on the closure ladder | A corpus-wide scalar (there is none) |

**Interlocks that are *stated*, never *summed*:**
- Accounting I (5) and Accounting III (4) **barely overlap** (RH only).
  Neither is a subset of the other. The corpus's own roster (B2 §5)
  makes exactly this point.
- Accounting II ⊇ Accounting III as *sets of concerns* (the reduced
  frontier is drawn from the named obligations), but the *counts*
  ("13" vs "4", or "110" vs "4") are not comparable because they
  partition on different bases.
- Accounting IV is orthogonal: a branch can be at "conditional
  CERT-CLOSE" (posture) while still contributing an item to Accounting
  III (e.g. GR).

---

## 4. Governance rules that sit *above* the data hierarchy

Certain Book VII contents are **rules**, not **snapshots**, and bind at
the top regardless of tier. These are never "reconciled away":

- **Status-inflation ban:** no result cited beyond declared scope.
- **Transfer law:** `[C]` → `[U]` only via a Transfer Theorem;
  a scoped certificate cannot self-promote (⇒ Phase 3 Rule 6).
- **Bridge-stack limit:** no branch may claim stronger closure than its
  declared bridge stack permits (⇒ Phase 3 Rule 7). E.g. SPEC's
  continuum interfaces are `[B]`; SPEC may not claim `[U]`-level
  continuum closure.
- **Frontier non-dissolution:** a named `[O]` frontier is not
  discharged by rephrasing.
- **No-smuggling:** no undeclared imports.

Any proposed rewrite that would violate one of these is rejected at
plan time, before it becomes a patch.

---

## 5. Applying the model to the known conflicts (F-1 … F-9)

This section *classifies* each Phase-0 finding under the hierarchy and
states the **proposed** treatment. It resolves nothing in the canon;
it routes each item.

| Finding | Conflict (P_hi vs P_lo) | Tiers | Classification | Proposed treatment (Phase 4/7) |
|---|---|---|---|---|
| **F-1** | SM branch body says "conditionally intrinsic-structural closed" (A1) vs. Canon Ledger PART 4 says SM "Prospective — no SM branch book exists yet" (B-tier descriptive text) | A1 > B(descriptive) | **SUPERSEDED** (B-text by A1-text) | Edit *scaffold* (`NFC_CANON_LEDGER.md` PART 4 SM entry) to current status + migration note pointing to `prop:SM-status-reconciliation`. Canon `.tex` untouched. |
| **F-2** | YM five obligations are `\status{C}` in the body (A3) vs. Canon Ledger PART 4 says they are "`[O]` in the canonical YM branch book as written" (B-descriptive) | A3 > B(descriptive) | **SUPERSEDED** | Edit scaffold Ledger PART 4 YM entry; migration note. Canon untouched. |
| **F-3** | Direct tag census D/U/C = 461/212/748 vs. STATE_OF_CANON top table 443/209/685 | mechanical vs. B3 | **AMBIGUOUS → REVIEW_NEEDED** | Do **not** overwrite the table. Ask reviewer whether the table uses a narrower convention; if "just stale," regenerate it from the Phase-5 metadata (then it becomes E-tier generated). |
| **F-4** | Per-file `%%` legend lists 5 codes, omits `[B]` vs. Canon Ledger PART 1 lists 6 | D1 (front block) vs. B2/rule | **SUPERSEDED** (the per-file legend is incomplete) | Add `[B]` line to each file's comment legend. This is a *comment*, not a semantic claim — low risk, but still logged with a migration entry. |
| **F-5** | Environment named `openobligation` for 105 items that are actually `[C]`/`[B]` | structural | **HISTORICAL (naming) → REVIEW_NEEDED** | Do **not** mass-rename the environment (labels/refs are load-bearing; high risk). Instead: (i) surface true status via the Current Status Capsule + the Phase-5 metadata `status_tag` field; (ii) optionally propose a *rendering-only* change (e.g. the environment prints "Obligation [C: discharged at scope]") in a later, separately-reviewed pass. Flag for human decision. |
| **F-6** | Book VII `sec:status-table` lists SM "CouplingTransfer" as remaining vs. Book VII `sec:obligation-vs-frontier` says it's proved (`thm:SM-coupling-transfer-full`) | A-tier vs A-tier, **same file** | **AMBIGUOUS → REVIEW_NEEDED** | Same-tier in-canon contradiction. Propose reconciling the status-table row to match the frontier section **only after reviewer confirms** which is intended current. No mechanical pick. |
| **F-7** | Branch front-matter "Prospective/pre-closure" (D1) vs. branch bodies at CERT-CLOSE-level (A1) — BIO, CRYST, LING, SPEC worst | A1 > D1 | **HISTORICAL** (front matter is intake) | The canonical treatment: **preserve** front matter, relabel it "(constitutional intake)", and insert a Current Status Capsule pointing to A1. This is the core fix for the primary problem. Detailed per-file in Phase 4. |
| **F-8** | Book VII "13 named obligations" vs. current 5-item `[O]` census / 110-label roster | C1-data vs I/II | **HISTORICAL** (already self-flagged by B2 roster) | Add a forward-pointer in Book VII text to `NFC_OBLIGATION_ROSTER.md`; keep "13" as a dated historical figure. Low risk. |
| **F-9** | Book VII Branch Status Table omits BIO/CRYST/LING/SPEC | C1-data | **SUPERSEDED (incomplete)** | Propose adding the 4 missing branches to the table, sourced from their A1 propositions. Medium risk (in-canon spine edit) → stage carefully in Phase 7, run compile after. |

**Branch posture reference (Accounting IV), sourced from each branch's
A1 — the authoritative current postures:**

| Branch | Authoritative current posture (A1 source) |
|---|---|
| YM | Conditional CERT-CLOSE at MSC-normalized NFC scope (`prop:YM-status`); B1/B2/B3 post-program |
| NS | Domain-bounded conditional CERT-CLOSE (`prop:NS-status`); Stage-3 Clay external |
| SCC | Conditional CERT-CLOSE (`prop:scc-status`) |
| GR | Domain-bounded conditional CERT-CLOSE, with CK-corner extension (`prop:gr-status`, `prop:gr-ck-corner-extension`); global curvature-subcriticality open |
| SM | Conditionally intrinsic-structural closed, inherited-scope open (`prop:SM-status-reconciliation`, `rem:sm-status-current`) — **stronger than the raw "CERT-PROJ" of `prop:SM-status`, which the reconciliation explicitly supersedes on the internal ledger only** |
| BIO | Replication–heredity endpoint discharged (REP–END); EVO/MULTI conditionally advanced; BND residual toolkit-boundary (`rem:bio-two-status` + `-END` theorems) |
| LING | Contrast+recursion+context-response closed; reference semantics conditional at two scopes (`rem:ling-two-status`, `-END`) |
| CRYST | Conditional CERT-CLOSE (diffraction-periodicity-symmetry); phase problem modulo certified invariance group open (`prop:cryst-status`) |
| SPEC | CERT-CLOSE on gauge-response regime; matter-rich regime open, gated on SM (`prop:SPEC-status` — supersedes the earlier `prop:spec-current-status` "prospective" language, which is intake) |
| RH | CERT-PROJ (`prop:RH-status`); S1 arithmetic + RH4–6 frontier |

---

## 6. What this model deliberately leaves open

- It does **not** decide F-3 or F-6; those are `REVIEW_NEEDED` by
  design (same-tier or convention-ambiguous conflicts are not for
  mechanical resolution).
- It does **not** authorize renaming the `openobligation` environment
  (F-5) — flagged for a separate, human-approved decision because the
  labels are load-bearing.
- It ranks Book VII's *rules* above its *data*; if a reviewer regards
  the Branch Status Table as itself rule-like/binding, that raises F-6
  and F-9 in severity and must be settled before Phase 7.

**Output of Phase 1:** every known conflict now has a tier assignment,
a classification, and a routed treatment (scaffold-edit vs.
capsule-insertion vs. REVIEW_NEEDED). Phase 2 turns the "primary
problem" surface into an exhaustive, phrase-level audit using exactly
these classifications.
