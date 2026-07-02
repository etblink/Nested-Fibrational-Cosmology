# NFC Stale-Label Audit

**Produced:** Phase 2 (audit/classification only — **no canon file edited**). Uses the classification vocabulary and authority tiers defined in `CANON_AUTHORITY_MODEL.md`.

**Classifications:**
- **CURRENT** — still accurate; leave alone.
- **HISTORICAL** — accurate as intake/constitution/record, but not current status; preserve and mark/contextualize.
- **SUPERSEDED** — contradicted by a higher-or-equal authority text that is current; propose a migration-tracked repair (scaffold) or a capsule (canon).
- **AMBIGUOUS** — requires human review; do not resolve mechanically.
- **GENERATED** — do not hand-edit; fix upstream source, regenerate.

**Method:** each candidate phrase from the task list was grepped corpus-wide; every hit was read *in context* (surrounding environment, whether it is a defined technical term, whether an A-tier status proposition in the same file contradicts it). Counts are from the Phase-0 census. **The single most important methodological result: a large fraction of raw phrase-hits are CURRENT technical vocabulary or correctly-scoped honest language, NOT stale.** Mechanical search-and-replace would corrupt the canon. Only the genuinely misleading hits are marked SUPERSEDED / HISTORICAL-needs-marking.

---

## A. Front-matter status lines and titles (the primary problem — highest priority)

D1-tier constitutional-intake locations whose language mismatches the branch's own A1 status proposition.

| # | File | Section / line | Exact phrase | Class | Reason | Proposed treatment |
|---|---|---|---|---|---|---|
| A-1 | NFC_BIO_Branch.tex | `%%` header, l.3 | "Status: Architecturally constituted; pre-closure — all theorem shells carry open obligations" | **SUPERSEDED** | Body discharges REP–END as `[C]` theorems; `rem:bio-two-status` declares replication–heredity endpoint reached; only BND-residual + EVO/MULTI extensions remain. "All theorem shells carry open obligations" is false now. | Rewrite `%%` status line to a current one-liner AND add pointer to `rem:bio-two-status`. Preserve original as a dated "(intake status, as constituted)" comment line directly below. Comment-only region → low compile risk. |
| A-2 | NFC_CRYST_Branch.tex | `%%` header, l.3 | "Status: Architecturally constituted; pre-closure." | **SUPERSEDED** | `prop:cryst-status` declares "Conditional CERT-CLOSE pending two convergence conditions + phase frontier." | As A-1, pointing to `prop:cryst-status`. |
| A-3 | NFC_LING_Branch.tex | `%%` header, l.3 | "…pre-closure — all theorem shells carry open obligations" | **SUPERSEDED** | Body: contrast+recursion+context-response closed; `rem:ling-two-status`. | As A-1, pointing to `rem:ling-two-status`. |
| A-4 | NFC_SPEC_Branch.tex | `%%` header, l.3 | "…pre-closure — all theorem shells carry open obligations" | **SUPERSEDED** | `prop:SPEC-status`: "CERT-CLOSE on the gauge-response spectroscopy regime." | As A-1, pointing to `prop:SPEC-status`. |
| A-5 | BIO/CRYST/LING/SPEC | `\author{… Prospective Derived Branch}` (BIO l.54, CRYST l.56, LING l.53, SPEC l.55) | "Prospective Derived Branch" | **HISTORICAL** | "Prospective" was accurate at constitution; now misleading on the title page, but it is constitutional language and the branch *was* constituted prospectively. | Do not delete. Per Phase-3 Rule 1, keep the line; the Current Status Capsule (added at top of body) carries the live posture. Optionally change subtitle to "Derived Branch (constituted prospectively; see Current Status Capsule)". Recompile + visual check. **Flag: exact wording → confirm with reviewer.** |
| A-6 | BIO/CRYST/LING/SPEC | `%%` comment l.2 "(Prospective)" | "(Prospective)" | **HISTORICAL** | Comment-level; harmless but stale. | Update comment to current posture; retain "(constituted prospectively)" note. Comment-only. |
| A-7 | NFC_YM_Branch.tex | `%%` header, l.3 | "Status: CERT-PROJ direction; not yet CERT-CLOSE" | **SUPERSEDED** | `prop:YM-status` + following `[R]` explicitly state the "CERT-PROJ. Not CERT-CLOSE" language "reflected the pre-MSC-normalization state" and is superseded → now "Conditional CERT-CLOSE at MSC-normalized scope." The canon body already contains the supersession statement; only the header lags. | Rewrite header status line to "Conditional CERT-CLOSE (MSC-normalized NFC scope); B1/B2/B3 post-program — see prop:YM-status". Preserve old as intake note. |
| A-8 | NFC_SCC_Branch.tex | `%%` header, l.3 | "Status: CERT-PROJ at most; MCS is the main frontier" | **SUPERSEDED** | `prop:scc-status` [U] + STATE_OF_CANON list SCC at conditional CERT-CLOSE (MCS/UC/TSI discharged). | Rewrite header; pointer to `prop:scc-status`. |
| A-9 | NFC_RH_Branch.tex | `%%` header, l.2–3 | "Initial Canonical Draft" | **HISTORICAL** | RH genuinely at CERT-PROJ (A1 agrees) — no status contradiction — but "Initial … Draft" is intake framing. | Low priority. Add Current Status Capsule → `prop:RH-status`; keep "Initial Canonical Draft" as a dated provenance line. |
| A-10 | NFC_SM_Branch.tex | `%%` header, l.2–3 | "Initial Canonical Draft" | **HISTORICAL** | SM body advanced to "conditionally intrinsic-structural closed" (`prop:SM-status-reconciliation`); "Initial Draft" is stale framing but not a false status claim in the header. | Add Current Status Capsule → reconciliation prop + `rem:sm-status-current`. |
| A-11 | NFC_GR_Branch.tex | `%%` header, l.3 | "Domain-bounded CERT-CLOSE conditional; global closure open" | **CURRENT** | Matches `prop:gr-status` / `thm:gr-domain-bounded`. CK-corner extension refines, does not contradict (global frontier still open). | Leave as-is. Optionally add a capsule noting CK-corner partial extension. Header not misleading. |
| A-12 | NFC_NS_Branch.tex | `%%` header, l.2–3 | "Canonical Descendant Draft" (no status line) | **CURRENT** (absence, not error) | No status claim in header; `prop:NS-status` carries "domain-bounded conditional CERT-CLOSE." | Add a Current Status Capsule for uniformity (Phase 3 Rule 2); nothing to correct. |

---

## B. "prospective" (body occurrences beyond front matter)

| # | File | Section | Exact phrase | Class | Reason | Proposed treatment |
|---|---|---|---|---|---|---|
| B-1 | NFC_SPEC_Branch.tex | `prop:spec-current-status` (l.798) | "The spectroscopy branch is a **prospective** lawful descendant program … without canonical closure … does not yet possess a certified transition theorem …" | **SUPERSEDED (content); AMBIGUOUS (mechanism)** | Contradicted by later `prop:SPEC-status` (same file), which certifies O-SPEC.PR–END discharged and declares gauge-response CERT-CLOSE. Two A1-tier propositions in one file; the later explicitly supersedes. | Recommended: relabel this section "Constitutional Intake Status (superseded by `prop:SPEC-status`)" and add a one-line supersession pointer inside it, WITHOUT deleting it (it records the branch's constitution). Do not silently delete a `\status`-tagged proposition — **REVIEW_NEEDED** for reviewer sign-off. |
| B-2 | Canon Ledger PART 4 (scaffold) | SM entry | "Prospective. No SM Branch book exists yet." | **SUPERSEDED** | = Finding F-1. Contradicted by the existing 2,219-line SM branch. | Scaffold edit + migration entry (Authority Model §5, F-1). |

---

## C. "CERT-PROJ" / "CERT-CLOSE"

Most hits are **CURRENT** — the corpus's precise status vocabulary, used correctly inside status propositions and ledgers. Only header/front-matter uses that contradict a branch's own A1 (captured in §A) are problematic.

| # | File | Section | Phrase | Class | Reason |
|---|---|---|---|---|---|
| C-1 | NFC_YM_Branch.tex (30× CLOSE, 11× PROJ) | body status props, referee table, ledger | both | **CURRENT** | Used correctly in `prop:YM-status` + supersession remark. Body right; only header (A-7) lagged. |
| C-2 | NFC_SCC_Branch.tex (12× PROJ, 6× CLOSE) | body | both | **MIXED → line-by-line REVIEW** | `prop:scc-status` [U] asserts conditional CERT-CLOSE. Any CERT-PROJ line describing SCC's *current* posture is SUPERSEDED; any describing a *past* stage is HISTORICAL. Itemize in Phase 4; **flag SCC CERT-PROJ occurrences for line-by-line review.** |
| C-3 | NFC_GR_Branch.tex (23× CLOSE, 3× PROJ) | two-status | both | **CURRENT** | GR's careful two-status reading uses both correctly and honestly. |
| C-4 | NFC_Book_VII.tex (10× CLOSE, 3× PROJ) | governance defs + Branch Status Table | both | **CURRENT (rules) / SUPERSEDED-data (table)** | Definitions CURRENT. The Branch Status Table SM="CERT-PROJ" cell is in tension with `prop:SM-status-reconciliation` → SUPERSEDED, but see F-6: reconcile only after review. |
| C-5 | NFC_SM_Branch.tex (7× PROJ, 9× CLOSE) | `prop:SM-status` vs `prop:SM-status-reconciliation` | both | **HISTORICAL (the CERT-PROJ of `prop:SM-status`)** | Reconciliation explicitly declares SM-New supersedes SM-Old on the internal ledger only → "conditionally intrinsic-structural closed." Supersession already in canon; only the front-matter capsule (A-10) and scaffold summaries need pointers. Do not alter `prop:SM-status` (deliberately preserved as the superseded baseline). |

---

## D. "frontier-blocked"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| D-1 | NFC_Book_IV.tex l.1140 | closure discussion | "NS regularity remains frontier-blocked by the named obligation of the NS branch book." | **CURRENT** | NS *unconditional* global regularity (Stage-3 Clay) is genuinely still the external frontier per `prop:NS-status`. | Leave. |
| D-2 | NFC_NS_Branch.tex l.1888 | mid-body | "no longer entirely frontier-blocked at SB2." | **CURRENT** | Honest incremental statement, consistent with domain-bounded CERT-CLOSE. | Leave. |
| D-3 | NFC_NS_Branch.tex l.2622 | remark | "the NS branch will advance from frontier-blocked to Cond(K₀=7)-closed" (future conditional) | **AMBIGUOUS** | `prop:NS-status` now says domain-bounded CERT-CLOSE is reached. Is this remark a still-future step or stale? | **REVIEW_NEEDED.** Ask whether the described advance has occurred; if yes → HISTORICAL/relocate; if no → CURRENT. |

---

## E. "pre-closure" (body, beyond front matter)

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| E-1 | NFC_CRYST_Branch.tex l.98 | `rem:cryst-legitimacy` | "All five UBLT conditions can be satisfied at the declared **pre-closure** scope." | **HISTORICAL** | Describes the legitimacy analysis as originally performed at constitution; branch has since advanced. | Preserve (constitution argument); capsule clarifies intake-era. Consider parenthetical "(at constitution; see Current Status Capsule)". Low priority. |

---

## F. "initial endpoint"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| F-1 | BIO l.102, CRYST l.287, LING l.92, SPEC l.84 | "Purpose and Canonical Seed" | "The **initial endpoint** is deliberately modest: certified [replication/Bragg/contrast/resonance] …" | **HISTORICAL (CURRENT as intake)** | Exactly the constitutional-intake language to **preserve**. Describes the founding target; not a current-status claim. | **Preserve verbatim.** Only fix is orientational: the Current Status Capsule tells the reader "the initial endpoint below has largely been reached; see [status prop]." No edit to this sentence. |

---

## G. "deferred"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| G-1 | NFC_Book_III.tex l.1289, 2035 | transport/encoding | "Continuum encoding: **deferred** — no continuum …" | **CURRENT** | Technical scoping; continuum encoding legitimately out of scope there, licensed later by Book VI. | Leave. |
| G-2 | NFC_Book_III.tex l.1707, 3485 | proof prose | "deferred", "deferred and proved nothing here" | **CURRENT** | Ordinary proof-organization language. | Leave. |
| G-3 | BIO/CRYST/LING/SPEC "Purpose" seed | | "…are **deferred** as named open obligations." | **HISTORICAL** | Intake: names obligations deferred at constitution; some (e.g. BIO EVO) since conditionally advanced. | Preserve as intake; capsule provides current view. Do not edit the seed sentence. |

---

## H. "remaining gap"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| H-1 | NFC_Book_II.tex l.2004, 2092 | P4-grade discussion | "the only **remaining gap** before a fully unconditional P4-grade reading" | **CURRENT** | Precise description of a genuine conditional residual in Book II. | Leave. |
| H-2 | NFC_SM_Branch.tex l.1688 | extspec intro | "identifies the minimal **remaining gaps**" | **CURRENT** | Accurately introduces `prop:SM-extspec-status` (SM-MAT/SM-HIGGS residuals). | Leave. |
| H-3 | NFC_GR_Branch.tex (1), NFC_RH_Branch.tex (1), NFC_SCC_Branch.tex (1), NFC_SPEC_Branch.tex (1), NFC_YM_Branch.tex (1) | various | "remaining gap" | **CURRENT** (verify per-line in Phase 4) | Honest residual language expected. | Verify line-reads in Phase 4; expected CURRENT. |

---

## I. "Clay gap(s)"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| I-1 | NFC_YM_Branch.tex l.1342, l.5136 | B1/B2/B3 section | "The three **Clay gaps** B1/B2/B3 remain open post-program obligations." | **CURRENT** | Correct, load-bearing honesty: deliberately open, post-program. `prop:YM-status` item (6) matches. | Leave. Do NOT "resolve" — honest permanent frontier markers (governance rule: frontier non-dissolution). |
| I-2 | NFC_Book_VII.tex l.1419 | `rem:obligation-conventions` | "Clay gaps ob:YM-B1/B2/B3, conditionally discharged at NFC scope" | **CURRENT** | Correct two-scope honesty (discharged at NFC scope, open at Clay scope). | Leave. |

---

## J. "not yet discharged"

| # | File | Section | Phrase | Class | Reason | Treatment |
|---|---|---|---|---|---|---|
| J-1 | NFC_Book_VII.tex l.123 | `def:open-obligation` | "a named burden **not yet discharged** by theorem or certified bridge" | **CURRENT** | This is the *definition* of an open obligation. Definitional, timeless. | Leave — editing would damage a governance definition. |

---

## K. "open obligation" (99 hits corpus-wide)

**Overwhelmingly CURRENT / definitional.** The phrase is the corpus's core governance term (`def:open-obligation`, Book VII) and appears in every branch's obligation section. The phrase itself is never the problem. The problem (F-5) is the *environment name* `openobligation` being applied to items now `[C]` — a structural naming issue, already routed to REVIEW_NEEDED in the Authority Model, not a search-replace target here. No treatment in this audit; see F-5.

---

## L. "branch candidate" (32 hits)

| Class | **CURRENT (all)** |
|---|---|
| Reason | `licensed branch candidate` is a **defined technical term** from Book V's UBLT (Book V §"Branch Candidates and Descent Structure"). Every branch legitimately declares itself "a lawful branch candidate" as step 1 of UBLT compliance. Not stale status. |
| Treatment | **Leave all.** A mechanical sweep would have corrupted core legitimacy vocabulary — this entry records that the phrase was checked and cleared. |

---

## M. "current status" (16 hits)

Section-title / proposition-title uses. **CURRENT** as titles, though several sit above content that has moved on:

| # | File | Phrase | Class | Treatment |
|---|---|---|---|---|
| M-1 | NFC_SPEC_Branch.tex `sec:spec-current-status` | "Current Status Proposition" titling `prop:spec-current-status` | **SUPERSEDED** (content — see B-1) | Title promises current status but content is the superseded prospective one. Retitle "Constitutional Intake Status (superseded)" per B-1; REVIEW_NEEDED. |
| M-2 | NFC_CRYST_Branch.tex `Updated Phase Problem Status` | title | **CURRENT** | Genuinely updated. Leave. |
| M-3 | GR, NS, RH, SM, SCC, YM | "current status" in prose/titles | **CURRENT** | Used correctly. Phase 3 standardizes capsule naming, which subsumes these. |

---

## N. Scaffold (`.md`) stale content — hand-maintained upstream

Not canon; may be repaired more freely (with migration notes). Several are the *upstream* whose staleness the canon must not inherit.

| # | File | Item | Class | Treatment |
|---|---|---|---|---|
| N-1 | NFC_CANON_LEDGER.md PART 4 | SM "Prospective, no book exists"; YM "5 obligations [O] in canon" | **SUPERSEDED** (F-1, F-2) | Repair PART 4 SM + YM entries to current; add dated migration notes; keep old text quoted in a "superseded description (as of session X)" block so history stays legible. |
| N-2 | NFC_STATE_OF_CANON.md | "Open Obligation Register (4 items, as of L+22)" header while file runs to L+63; tag counts 443/209/685 vs. census 461/212/748 | **AMBIGUOUS / SUPERSEDED** (F-3) | Do not overwrite counts by guess. Regenerate from Phase-5 metadata once it exists → tables become GENERATED (source = metadata DB), resolving F-3 permanently. Until then, add "⚠ counts pending regeneration; see census in AUDIT_BASELINE.md". |
| N-3 | NFC_Book_VII.tex "(currently 13 items)" | in-canon spine text | **HISTORICAL** (F-8) | This is *canon*, not scaffold. Add forward-pointer to `NFC_OBLIGATION_ROSTER.md`; keep "13" as a dated figure. Low risk. |
| N-4 | NFC_OBLIGATION_ROSTER.md | — | **CURRENT** | The exemplar. No change; use as template for Phase-5 schema and dashboard obligation view. |

---

## O. Summary of classifications

| Class | Distinct findings | Notable members |
|---|---|---|
| **SUPERSEDED** | 12 | A-1..A-4, A-7, A-8; B-1(content), B-2; C-4(table cell), M-1; N-1 |
| **HISTORICAL** (preserve + mark/capsule) | 11 | A-5, A-6, A-9, A-10, C-5, E-1, §F, G-3, I-adjacent, N-3 |
| **CURRENT** (leave) | large majority | D-1/2, G-1/2, H, I, J, K, L, M-2/3, A-11, A-12 |
| **AMBIGUOUS → REVIEW_NEEDED** | 5 (+2 inherited) | A-5 (wording), B-1/M-1 (deleting a `\status` prop), C-2 (SCC per-line), D-3 (NS future-tense); inherited F-3, F-6 |
| **GENERATED** (fix upstream) | 2 clusters | N-2 (STATE_OF_CANON tables → regenerate), all 17 `.pdf` |

**Headline for Phase 3/4:** the corpus-level fix is small and surgical, not a rewrite. Genuinely misleading text is concentrated in ~10 front-matter/header locations (§A) plus 2 scaffold ledger entries (N-1) plus one internally-superseded SPEC proposition (B-1). Everything else that *pattern-matched* the stale-phrase list is either correct technical vocabulary or honest, correctly-scoped status language that must be left intact. The primary-problem repair is therefore: **(i)** add a uniform Current Status Capsule to each branch/book; **(ii)** relabel the ~10 front-matter locations as constitutional intake with current-status pointers; **(iii)** repair 2 scaffold ledger entries with migration notes; **(iv)** route the 5 REVIEW_NEEDED items to the human queue. No theorem, proof, label, or scoped claim is altered.
