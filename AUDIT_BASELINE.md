# NFC Corpus — Phase 0 Audit Baseline

**Produced:** Pre-edit audit, isolated working copy.
**Scope:** Full corpus as delivered — 7 spine books, 10 branch books, 11
scaffold/governance markdown files, 17 compiled PDFs.
**Rule observed:** No canon file has been edited to produce this
document. This is a read-only inventory and measurement pass.

---

## 0.1 Working copy and isolation

- Working copy created at an isolated path, independent of the
  original project files.
- Git repository initialized in the working copy (`main` branch =
  baseline snapshot commit; work proceeds on `audit/phase0-inventory`).
- Baseline commit hash and per-file SHA-256 hashes recorded in
  §6 (Generated Report Hashes / Baseline Hashes) for future diffing.
- **No canon or scaffold file has been modified.** This audit was
  produced entirely by read-only inspection (`view`, `grep`, a
  custom Python label/citation-graph script, and a two-pass `pdflatex`
  compile check run against copies of the files).

---

## 0.2 File Inventory and Classification

| File | Type | Class | Notes |
|---|---|---|---|
| NFC_Book_I.tex … NFC_Book_VII.tex | .tex | **CANON** | 7-book spine. Source of truth for the program's foundational layer. |
| NFC_BIO_Branch.tex, NFC_CRYST_Branch.tex, NFC_GR_Branch.tex, NFC_LING_Branch.tex, NFC_NS_Branch.tex, NFC_RH_Branch.tex, NFC_SCC_Branch.tex, NFC_SM_Branch.tex, NFC_SPEC_Branch.tex, NFC_YM_Branch.tex | .tex | **CANON** | 10 branch books. |
| NFC_Book_*.pdf, NFC_*_Branch.pdf (17 files) | .pdf | **GENERATED** | Compiled output of the corresponding `.tex` file. Source of truth = the `.tex` file of the same base name. These must never be hand-edited; regenerate via `pdflatex`. |
| NFC_CANON_LEDGER.md | .md | **SCAFFOLD** (hand-maintained working ledger) | Internal bookkeeping / synthesis-note-intake log. Structurally mixed: PART 0–2 (orientation/architecture) and PART 3–5 (detailed per-book/per-branch ledger) are **written-once, not continuously refreshed**; PART 9 (Recent Promotions Log, ~6,100 lines) is a **continuously-appended chronological log** and is the most current material in the file. See Finding F-1/F-2 below — PART 3/4 contain severely stale branch descriptions. |
| NFC_STATE_OF_CANON.md | .md | **SCAFFOLD** (hand-maintained periodic snapshot) | Corpus-wide counts + branch status summary table + session log. Internally two-tier: top summary table is fresher than the "Open Obligation Register" mid-section, which is explicitly dated "as of L+22" while the rest of the file has moved to L+63. See Finding F-3. |
| NFC_OBLIGATION_ROSTER.md | .md | **SCAFFOLD** (hand-maintained, dated snapshot, explicitly self-scoped) | The single most rigorous and self-aware reconciliation document in the corpus. Explicitly labeled "Authoritative as of L+39" with a dated L+56 addendum; explicitly states "the Canon Ledger is the live record between snapshots." Recommended as the primary model for the Phase 1 authority hierarchy. |
| NFC_FRONTIER_FEASIBILITY.md | .md | **SCAFFOLD** (dated assessment note, L+42) | Explicitly self-labeled "an assessment, not a discharge." |
| NFC_NFR_INTEGRATION_ASSESSMENT.md | .md | **SCAFFOLD** (dated assessment note, L+44) | Explicitly self-labeled non-promotable / assessment-only. |
| NFC_RIGQ_INTEGRATION_ASSESSMENT.md | .md | **SCAFFOLD** (dated assessment note, L+49) | Assessment-only. |
| NFC_RIGQ_ORQ1_RESULT.md | .md | **SCAFFOLD** (dated working note, L+50) | Explicitly self-labeled as not touching canon. |
| NFC_SPECULATIVE_HOLDING.md | .md | **SCAFFOLD** (living pre-canonical holding document) | Explicitly named companion to the Canon Ledger; holds material that has NOT been promoted to canon. Not canon by its own declaration. |
| NFC_VARIABLE_RECOVERY_PROGRAM.md | .md | **SCAFFOLD** (speculative program packet) | Self-labeled "Speculative canon-facing program packet." Canonized portions live in Book III; this file is the pre-canonical working draft. |
| NFC_VARIABLE_RECOVERY_PROGRAM_LEDGER.md | .md | **SCAFFOLD** (speculative working ledger) | Self-labeled "speculative canon-facing working ledger." |
| NFC_VRP_COMPLETION_CAPSTONE.md | .md | **SCAFFOLD** (governance summary note, L+47) | Explicitly self-labeled "not a new canonical claim." |

**No SCRIPT, REPORT (in the machine-generated sense), or true UNKNOWN
files exist in the corpus as delivered.** There is currently no build
script, no test harness, no CI configuration, and no machine-readable
metadata layer (no JSON/YAML/DB of claims). Everything in the corpus,
including files that function as "reports," is hand-authored prose.
This is itself a Phase 5/6 gap, not a defect — it's the reason those
phases exist.

**Source of truth for every generated artifact:** each `NFC_*.pdf` ⟶
its identically-named `.tex` file. No other generated artifacts exist
yet (dashboards, JSON exports, etc. are to be built in Phase 5–6).

---

## 0.3 Build / Test Commands

**None existed at intake.** No Makefile, shell script, CI config, or
test harness was found anywhere in the delivered corpus
(`find . -iname "*.sh" -o -iname "makefile*" -o -iname "*.py" -o
-iname "*.yml" -o -iname "*.json"` returned nothing).

To establish a baseline anyway, this audit constructed and ran an
ad-hoc validation pass (methodology recorded here so it is
reproducible and becomes the seed for the Phase 5/6 real test suite):

1. **Compile check.** Each of the 17 `.tex` files was copied into an
   isolated directory and compiled twice with
   `pdflatex -interaction=nonstopmode -halt-on-error`.
   - **Result: 0 fatal errors, exit code 0, on all 17 files.** This
     matches the corpus's own claim ("All 17 files clean").
   - Each file does show `LaTeX Warning: Reference ... undefined`
     lines when compiled **standalone**. Spot-checking (Book III)
     confirms these are exclusively references to labels defined in
     *other* spine/branch files (e.g. `thm:ICDC`, `def:structural-entropy`
     from earlier books) — expected when compiling one chapter of a
     multi-file work in isolation, not a real defect. The corpus-wide
     label/reference audit below (§0.6) is the correct check for real
     dangling references, and it returns zero.
2. **Label / cross-reference graph audit** (custom Python/regex
   script over all 17 `.tex` files, treating the label namespace as
   global across the whole corpus — the correct model for a
   multi-file cross-referencing work).
3. **Approximate proof-citation cycle check** (custom Python script:
   for each `theorem`/`proposition`/`corollary`/`lemma` environment
   with a label, capture its immediately-following `proof` block and
   extract the labels it cites; build a directed graph; run cycle
   detection).

These three checks are read-only, non-destructive, and were run
against copies, not the working files. **Recommendation for Phase 5:**
promote this ad-hoc script into a checked-in `scripts/validate.py` (or
similar) plus a `Makefile`/`justfile` target, so "run the validation
suite" becomes a real, repeatable command rather than a manual
audit step.

---

## 0.4 Baseline Counts — Status Tags (Direct Syntactic Census)

Computed by `grep -o '\status{X}'` across all 17 `.tex` files (source
of truth: the macro `\newcommand{\status}[1]{\textup{[#1]}}`, defined
identically in every canon file). This is a **direct, reproducible,
current-as-of-this-audit census** — not copied from any prior summary.

| Status | Meaning (per Canon Ledger PART 1 — see Finding F-4) | Count |
|---|---|---|
| `[D]` | Definition / standing rule / declared posture | **461** |
| `[U]` | Unconditional | **212** |
| `[C]` | Conditional | **748** |
| `[B]` | Bridge theorem | **9** |
| `[O]` | Open obligation | **5** |
| `[R]` | Remark / scholium | **349** |
| **Total status-tagged environments** | | **1,784** |

Per-file breakdown (D/U/C/B/O/R/total):

| File | D | U | C | B | O | R | Total |
|---|---|---|---|---|---|---|---|
| NFC_Book_I.tex | 33 | 19 | 0 | 0 | 0 | 18 | 70 |
| NFC_Book_II.tex | 34 | 19 | 73 | 0 | 0 | 31 | 157 |
| NFC_Book_III.tex | 38 | 25 | 47 | 0 | 1 | 30 | 141 |
| NFC_Book_IV.tex | 18 | 25 | 1 | 0 | 0 | 13 | 57 |
| NFC_Book_V.tex | 19 | 14 | 5 | 0 | 0 | 8 | 46 |
| NFC_Book_VI.tex | 16 | 12 | 20 | 0 | 0 | 8 | 56 |
| NFC_Book_VII.tex | 27 | 39 | 0 | 0 | 0 | 20 | 86 |
| NFC_BIO_Branch.tex | 42 | 0 | 51 | 0 | 1 | 22 | 116 |
| NFC_CRYST_Branch.tex | 31 | 3 | 45 | 0 | 2 | 24 | 105 |
| NFC_GR_Branch.tex | 11 | 10 | 33 | 2 | 0 | 14 | 70 |
| NFC_LING_Branch.tex | 37 | 0 | 46 | 1 | 0 | 20 | 104 |
| NFC_NS_Branch.tex | 20 | 17 | 44 | 0 | 0 | 35 | 116 |
| NFC_RH_Branch.tex | 26 | 0 | 86 | 0 | 1 | 16 | 129 |
| NFC_SCC_Branch.tex | 15 | 9 | 39 | 0 | 0 | 18 | 81 |
| NFC_SM_Branch.tex | 6 | 1 | 42 | 0 | 0 | 18 | 67 |
| NFC_SPEC_Branch.tex | 41 | 0 | 31 | 6 | 0 | 9 | 87 |
| NFC_YM_Branch.tex | 47 | 19 | 185 | 0 | 0 | 45 | 296 |
| **TOTAL** | **461** | **212** | **748** | **9** | **5** | **349** | **1,784** |

**Discrepancy vs. NFC_STATE_OF_CANON.md's own top summary table**
(which reports [U]=209, [C]=685, [D]=443, [O]=5, and does not report
[B] or [R] at all): this audit's direct census is higher on D/U/C by
+18/+3/+63 respectively, and the top table omits [B] (9) and [R] (349)
as categories entirely. **[O]=5 matches exactly.** This is flagged as
**Finding F-3 / AMBIGUOUS→REVIEW_NEEDED**, not silently corrected: it
is not yet known whether STATE_OF_CANON's table is simply stale (most
likely — the file's own session log runs to L+63 while the table is
captioned "post L+56" and its methodology note is dated L+12) or
whether it is using a narrower counting convention (e.g. excluding
some environment types) that this audit's grep does not replicate.
**Phase 1 must adjudicate this, not Phase 0.**

---

## 0.5 Baseline Counts — Obligations (Multiple Accountings, Kept Separate)

Per the task's explicit instruction, the following are **not
collapsed**:

### (a) Syntactic `[O]` census — 5 items (verified, matches STATE_OF_CANON's headline number)
1. `ob:vrp-charge-quant` (NFC_Book_III.tex) — scoped to residual
   "b2" (numeric isolation of Ω_B ⊆ ℝ); a `remark` environment.
2. `ob:bio-BND-open` (NFC_BIO_Branch.tex) — `openobligation` environment.
3. `ob:cryst-PHASE` (NFC_CRYST_Branch.tex) — `openobligation` environment.
4. `ob:cryst-PHASE-progress` (NFC_CRYST_Branch.tex) — `openobligation` environment (progress tracker for #3).
5. `ob:rh-s1-formal` (NFC_RH_Branch.tex) — `openobligation` environment.

### (b) Total `ob:`-labeled obligation environments corpus-wide — 110 unique labels
Matches NFC_OBLIGATION_ROSTER.md's own reconciled count exactly
("109 [pre-dedup] … 110 distinct labels after the L+40
de-duplication"). Of these 110, only the 5 above are tagged `[O]`;
the remainder are tagged `[C]` (conditionally discharged at a named
scope) or `[B]` (bridge-discharged, 2 items: `ob:spec-CI`,
`ob:spec-CD`). **This is Finding F-5**: the LaTeX environment is
named `openobligation` for all 110, regardless of current status —
so a naive `grep -c "begin{openobligation}"` (110) wildly overstates
what is actually still open (5), and this naming choice is itself a
corpus-wide, structural instance of the "primary problem" the task
describes. See §7.

### (c) Curated named-obligation roster (Book VII's own count) — "13 items"
Book VII §sec:obligation-vs-frontier states "every named obligation
in the canonical files (currently 13 items)." **This number is
itself stale**: the STATE_OF_CANON session log shows the `[O]` count
fluctuating session-by-session from an early high down through 10 → 7
→ 6 → 4 → 9 → 5 (L+12 through L+63), and NFC_OBLIGATION_ROSTER.md
(§1) explicitly annotates Book VII's "13" as a "pre-VRP snapshot" —
i.e., the corpus has *already*, on its own, flagged this figure as
historical. Treated here as **HISTORICAL**, not silently updated.

### (d) Reduced irreducible frontier — 4 items, but two non-identical published versions
Both Book VII (§sec:obligation-vs-frontier) and
NFC_OBLIGATION_ROSTER.md (§3) claim to state "the" 4-item reduced
irreducible frontier, and mostly agree:
1. RH arithmetic orbit grammar (3 sub-labels)
2. RH packet-local synthesis (5 sub-labels)
3. SM matter content
4. GR global curvature-subcriticality (`def:curv-subcrit-global`,
   not an `ob:` label — its own fourth tracking convention)

**But Book VII's separate, earlier "Branch Status Table"
(§sec:status-table, same file) lists a conflicting fifth-ish item —
"SM … CouplingTransfer" — as still-remaining**, which the very next
section in the same file (§sec:obligation-vs-frontier) and the
Obligation Roster both treat as **already conditionally discharged**
(`thm:SM-coupling-transfer-full`, [C]). **This is Finding F-6: an
internal contradiction inside Book VII itself, between two adjacent
sections**, not merely a cross-file drift. Flagged
`AMBIGUOUS`/`REVIEW_NEEDED` for Phase 1/2, not resolved here.

### (e) Branch posture / closure status — see §0.6.

---

## 0.6 Branch Posture List (as currently *declared*, multiple sources — not yet reconciled)

| Branch | STATE_OF_CANON.md (top table, most recent) | Book VII "Branch Status Table" (§sec:status-table) | Branch's own front-matter comment line | Branch's own in-body Status Proposition |
|---|---|---|---|---|
| YM | Conditional CERT-CLOSE; branch [O]=0 | Cond. CERT-CLOSE | "CERT-PROJ direction; not yet CERT-CLOSE" | `prop:YM-status` [C] |
| NS | Domain-bounded conditional CERT-CLOSE | Cond. CERT-CLOSE | "Canonical Descendant Draft" (no status claim) | `prop:NS-status` [U]: "frontier-blocked" |
| SCC | Conditional CERT-CLOSE (MCS+UC+TSI) | Cond. CERT-CLOSE | "CERT-PROJ at most; MCS is the main frontier" | `prop:scc-status` [U] |
| GR | Domain-extended conditional CERT-CLOSE | Cond. CERT-CLOSE | "Domain-bounded CERT-CLOSE conditional; global closure open" | `prop:gr-status` [C] |
| SM | Conditionally intrinsic-structural closed; branch [O]=0 | CERT-PROJ | "Initial Canonical Draft" (no status claim) | `prop:SM-status` [C] (superseded in part by `prop:SM-status-reconciliation` [C] and `rem:sm-status-current` [R], all later in the same file) |
| BIO | Full endpoint on C_Bio^nd; BND forced except trivial-core | *(not listed — branch absent from this table)* | "(Prospective) … pre-closure — all theorem shells carry open obligations" | via `rem:bio-two-status` [R] |
| LING | Contrast+recursion+context-response closed | *(not listed)* | "(Prospective) … pre-closure — all theorem shells carry open obligations" | via `rem:ling-two-status` [R] |
| CRYST | Conditional CERT-CLOSE (diffraction-periodicity-symmetry) | *(not listed)* | "(Prospective) … pre-closure" | `prop:cryst-status` [C] |
| SPEC | CERT-CLOSE (gauge-response); branch [O]=0 | *(not listed)* | "(Prospective) … pre-closure — all theorem shells carry open obligations" | `prop:SPEC-status` [C], `prop:spec-current-status` [C] |
| RH | CERT-PROJ | CERT-PROJ | "Initial Canonical Draft" | `prop:RH-status` [C] ("Updated") |

**Observations (not yet adjudicated — Phase 1 material):**
- Book VII's own "Branch Status Table" is missing 4 of the 10 branch
  books entirely (BIO, CRYST, LING, SPEC never appear in it). This is
  strong evidence the table was authored before those branches were
  constituted and never revisited.
- **Every one of the 10 branch front-matter comment lines
  understates or mismatches the branch's own currently-declared
  status** to some degree — from mild (RH, NS — a framing/title
  issue) to severe (BIO, CRYST, LING, SPEC — front matter says
  "pre-closure, all theorem shells carry open obligations" for
  branches whose own bodies show 0–2 syntactically-open items and a
  declared CERT-CLOSE-level or near-CERT-CLOSE-level status). This is
  the corpus-wide pattern the task calls "the primary problem." Full
  per-file detail is deferred to `STALE_LABEL_AUDIT.md` (Phase 2) and
  `CANON_REWRITE_PLAN.md` (Phase 4); it is only catalogued, not
  treated, here.
- Naming of the "current status" section is inconsistent across
  branches: "Final Status Proposition" (NS, SCC, YM), "\_\_\_ Branch
  Status Proposition" (RH, SM, SPEC), "Two-Status Reading" as a
  sub-section only (BIO, LING), no title at all in some cases. This
  supports Phase 3 Rule 2 (a uniformly-named, uniformly-located
  Current Status Capsule).

---

## 0.7 Dangling References and Citation/Dependency Cycles

**Dangling references: 0.** Independently verified via a corpus-wide
label/reference audit (Python, `\label{}` vs. `\ref|\eqref|\cref|\Cref{}`,
treating all 17 files as one label namespace, which is the correct
model for a cross-referencing multi-file work):
- Total `\label{}` occurrences: 1,995
- Unique label keys: 1,972
- Total `\ref`/`\eqref`/`\cref`/`\Cref` occurrences: 3,133 (1,019 unique targets)
- **Dangling references (ref to a label never defined anywhere): 0**

This matches the corpus's own claim exactly ("0 dangling refs
corpus-wide").

**Duplicate label definitions: 12** (a key defined more than once).
Also matches the corpus's own claim exactly ("12 benign collisions").
Detail:
- 9 `sec:*` section-name recurrences across independently-compiled
  branch files (benign — each file compiles alone):
  `sec:arena`, `sec:descent`, `sec:frontier`, `sec:governance`,
  `sec:imports`, `sec:ledger`, `sec:rh-screening`, `sec:status`,
  `sec:transfer`.
- 3 cross-book theorem/definition duplicates (flagged by the corpus
  itself as a "standing caution," never to be cited cross-corpus by
  `\ref`): `thm:governing` (appears in Books I, II, III, IV, VI, VII),
  `cor:conditional-no-unconditional` (Books VI, VII),
  `def:transport-invariant` (Books II, IV).

**Citation/proof-dependency cycles: 0** (independently verified via
an approximate proof-citation graph — for every `theorem` /
`proposition` / `corollary` / `lemma` environment with a label,
capture its immediately-following `proof` block and extract cited
labels; 475 statement-environments-with-proofs found, 1,083 citation
edges, 835-node graph, **0 cycles** by `networkx.simple_cycles`).
This qualitatively confirms the corpus's own claim ("0 citation
cycles"), though the exact node count (835 vs. the corpus's own
claimed 711 "statement-proof nodes") differs — expected, since this
audit's graph-construction heuristic (proof must immediately follow
the environment) is an approximation and the corpus's own
methodology for producing "711" is not documented anywhere found in
this audit. **Flagged AMBIGUOUS** — Phase 5 should specify one
canonical, scripted method for this count so it stops being
re-derived by hand each time.

---

## 0.8 Generated Report Hashes / Baseline Hashes

No pre-existing generated-report hashes were found (no prior
automation exists). This audit establishes the **first baseline**:
SHA-256 was computed for all 45 files (17 `.tex` + 17 `.pdf` + 11
`.md`) in the isolated working copy immediately after intake, before
any inspection artifacts were written. This baseline is committed to
the git history of the working branch (commit "Baseline snapshot:
isolated working copy of NFC corpus as received") and the full hash
manifest is available for any future diffing task. Representative
entries:

```
2306fe6b128aa6ca464860abbd4b81623db4d45795466d263b67ec6471a2cb3b  NFC_Book_I.tex
0f9f612d8dd3666a04a3b0cde34c34dfd6d64aa4c268c047b4996b3512ea340e  NFC_Book_I.pdf
11eaa42291d4556cd3d8b59293a3e25275a1c459519bb6aabf5ec307e34e6129  NFC_BIO_Branch.tex
e12811d1a226c8f5a79ace292db4425a74b9cec94e74a6e79dc5e33e3d4e3eaf  NFC_BIO_Branch.pdf
```//full manifest retained in working-branch history, not reproduced in full here for length.

---

## 0.9 Headline Findings Carried Forward to Phase 1 / Phase 2

These are **observations, not fixes**. Nothing has been changed.
Each is a candidate for classification in `STALE_LABEL_AUDIT.md` and
adjudication in `CANON_AUTHORITY_MODEL.md`.

- **F-1 (severe / SUPERSEDED-candidate).** NFC_CANON_LEDGER.md PART 4
  describes the SM Branch as *"(Prospective). No SM Branch book
  exists yet… The SM branch remains prospective pending canonical
  import."* `NFC_SM_Branch.tex` exists, runs 2,219 lines, contains 42
  `[C]`-status theorems, and contains its own later in-body
  supersession chain (`prop:SM-status` → `prop:SM-status-reconciliation`
  → `rem:sm-status-current`) concluding "conditionally
  intrinsic-structural closed." This Ledger entry appears to predate
  the SM branch's actual authorship and was never revisited.
- **F-2 (severe / SUPERSEDED-candidate).** The same Ledger PART 4
  entry for the YM Branch asserts that five obligations (O-ID, O-RIG,
  O-ENC, O-GLOB, O-CLU) "are marked `[O]` in the *canonical* YM
  branch book as written." Direct inspection of `NFC_YM_Branch.tex`
  shows all five are currently tagged `\status{C}`, not `[O]`.
- **F-3 (moderate / internally stale).** NFC_STATE_OF_CANON.md's own
  "Open Obligation Register" section header reads "(4 items, as of
  L+22 — census-verified)" while the same file's top summary table
  and session log reflect state through L+63, and the corpus-wide
  `[O]` count has been 5 (not 4) since at least L+45. Internal,
  same-file staleness.
- **F-4 (structural / SUPERSEDED-candidate).** The `%% Status legend`
  comment block, identical in all 17 canon files, lists only 5 codes
  (D, U, C, R, O) and omits `[B]` (Bridge Theorem), which is used 9
  times across GR, LING, and SPEC. NFC_CANON_LEDGER.md PART 1 ("STATUS
  VOCABULARY") is the accurate, 6-code source. No per-file legend was
  ever updated after `[B]` was introduced.
- **F-5 (structural / naming).** All 110 `ob:`-labeled obligation
  declarations use the LaTeX environment name `openobligation`
  regardless of current status; 105 of 110 are currently `[C]` or
  `[B]`, not `[O]`. The environment name itself misleads a naive
  reader/grep. See §7 rationale.
- **F-6 (internal contradiction, single file).** Book VII's "Branch
  Status Table" (§sec:status-table) lists SM's remaining work as
  "O-SM.Matter, CouplingTransfer," while the immediately following
  section, "Named Obligations vs. Reduced Irreducible Frontier"
  (§sec:obligation-vs-frontier), states CouplingTransfer is already
  proved (`thm:SM-coupling-transfer-full`) and lists only SM matter
  content (via O_ID^cont) as the live SM item in the reduced
  frontier. Same file, two adjacent sections, in tension.
- **F-7 (corpus-wide pattern).** Every one of the 10 branch books'
  front-matter title/status comment lines understates the branch's
  actual current status relative to the branch's own body content and
  relative to NFC_STATE_OF_CANON.md's most recent branch table. BIO,
  CRYST, LING, and SPEC are the most severe cases (front matter says
  "Prospective… pre-closure… all theorem shells carry open
  obligations" for branches with 0–2 syntactically open items and
  declared CERT-CLOSE-level status). This is direct, corroborated
  evidence for the task's stated "primary problem."
- **F-8 (already partially self-corrected — HISTORICAL, not a new
  defect).** Book VII's "13 named obligations" figure is stale
  relative to the current 5-item syntactic census, but
  NFC_OBLIGATION_ROSTER.md already explicitly flags this ("13
  (pre-VRP snapshot)") — the corpus's own governance has partially
  caught this; only the Book VII source text itself was never edited
  to point forward to the roster.
- **F-9 (missing coverage).** Book VII's "Branch Status Table" omits
  BIO, CRYST, LING, and SPEC entirely, evidence the table predates
  those branches' constitution.

None of F-1 through F-9 have been corrected in this pass. They are
inputs to Phase 1 (authority adjudication) and Phase 2 (formal
stale-label classification with proposed treatment).

---

## 0.10 What Phase 0 Deliberately Does Not Do

- Does not decide which document "wins" when two sources disagree
  (that is Phase 1).
- Does not classify every stale phrase in the corpus (that is Phase
  2's exhaustive pass; this document surfaces the load-bearing
  examples found incidentally while building the baseline).
- Does not touch any canon or scaffold file.
- Does not yet build any tooling beyond the throwaway audit scripts
  described in §0.3 (Phase 5/6 will formalize this).

**Recommendation:** proceed to Phase 1 (`CANON_AUTHORITY_MODEL.md`)
using this baseline, F-1…F-9, and the multi-accounting tables in
§0.5–0.6 as direct inputs, unless review of this baseline surfaces
corrections first.
