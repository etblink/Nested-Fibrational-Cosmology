# NFC Rewrite — Final Validation Report

**Scope validated:** the complete Phase 0–7 program on the isolated working copy (git history: 12 commits from baseline `d5d88c2` to final consistency pass).
**Gate definition:** `make validate` (labels / dangling refs / cycles / pinned census) + `scripts/compile_check.sh` (two-pass pdflatex, all 17 files, fatal = fail) + label-set and status-delta diff against the baseline commit.

---

## Acceptance criteria — verified one by one

**1. All 7 spine books and 10 branch books remain canonically intact.**
✅ All 17 `.tex` compile with exit 0 and 0 fatal errors (final full gate). Page counts stable except +1 page in SCC (30→31) and YM (81→82) from the added capsules — expected. No proof body, hypothesis list, theorem statement's mathematical content, or dependency reference was altered; the corpus-wide proof-citation graph re-extracts with 0 cycles.

**2. The beginning of each branch no longer misleads the reader about current status.**
✅ Every one of the 17 files now opens with a `[R]`-tagged Current Status Capsule (rendered, e.g., as "Remark 0.1" — verified present in the regenerated PDFs) that states the current posture verbatim from the branch's own status proposition and points to it by `\ref`. The six stale `%%` header status lines (BIO, CRYST, LING, SPEC, YM, SCC) were replaced with current one-liners, each retaining the original line immediately below as marked constitutional intake. The four "Prospective Derived Branch" title pages now render "Constituted Derived Branch" with the review-approved status-pointer subtitle (verified via `pdftotext` on the regenerated title pages).

**3. Historical intake material is preserved but clearly marked.**
✅ Zero intake sentences deleted. The "initial endpoint … deliberately modest" seeds, strategic-path remarks, UBLT constitution analyses, and the superseded `prop:spec-current-status` and `prop:SM-status` propositions are all still present, now explicitly marked "(constitutional intake)" / "Initial Constitution Status (superseded)" with forward pointers. Old header lines are quoted in place with `[retained as intake; superseded — MIG-nnn]`.

**4. The machine-readable corpus distinguishes all major frontier accountings.**
✅ `metadata/census.json` carries the four accountings as separate objects (I syntactic [O] = 5; II named `ob:` roster = 110; III reduced irreducible frontier = 4; IV per-branch postures) with an explicit `_warning` against summation; `metadata/views.json` carries the five status views. The dashboard renders them on separate panels.

**5. No theorem labels, obligation labels, or dependency references accidentally broken.**
✅ Machine-diffed against baseline: **1,972 baseline label keys → 1,989 current; removed = NONE; added = exactly the 17 intended `cap:*` capsule labels and nothing else.** Dangling references: **0** (baseline 0 → final 0). Duplicate labels: unchanged at the 12 known-benign keys, no new collisions.

**6. No generated artifact edited by hand.**
✅ All 17 PDFs were regenerated exclusively by two-pass `pdflatex` from the edited `.tex` (commit `caad9b0`). `metadata/*.json` and `dashboard/index.html` are produced only by `make metadata` / `make dashboard`. No PDF or JSON was patched directly at any point (verifiable from the git history: every PDF change co-commits with its regeneration step).

**7. Validation/build/regression tests pass.**
✅ Final `make validate`: 0 dangling, 0 cycles, census exactly matches the migration-updated pin (`D461 U211 C749 B9 O5 R366`). Final compile gate: all 17 files, exit 0, 0 fatal. **Status-tag delta from baseline is exactly the authorized set and nothing more: `R +17` (capsules), `U −1 / C +1` (the single review-authorized `prop:scc-status` `[U]→[C]` weakening). `[O]` count unchanged at 5 — no discharge was claimed and no status was promoted anywhere.**

**8. The GUI provides clear insight into branch status, stale labels, obligations, and review queues.**
✅ `dashboard/index.html` (self-contained, opens from disk, read-only by construction) renders 10 panels: branch overview with per-branch postures + tag counts, dual-census status counts with the F-3 reconciliation, the 5 open obligations, the four frontier accountings (CouplingTransfer correctly absent from the reduced frontier), historical/superseded/review queues, a 1,790-claim explorer, a dependency lookup over 1,094 proof-citation edges, release snapshot, generated-artifact map, and legend. Headless jsdom render test: 10 panels, 10 branch rows, 5 open rows, 0 runtime errors.

**9. A human can see exactly what changed, why, and what remains unresolved.**
✅ `migrations/MIGRATIONS.md` records 13 migration entries (MIG-001…MIG-013), each with location, classification, authority basis, labels touched (only ever the 17 new `cap:` keys), status touched (only the one authorized change), and gate result. The git history is 12 small commits in the plan's prescribed order. `PATCH_SUMMARY.md` and `UNRESOLVED_REVIEW_ITEMS.md` accompany this report.

---

## Final numbers at a glance

| Measure | Baseline | Final | Delta | Authorized by |
|---|---|---|---|---|
| Files compiling clean | 17/17 | 17/17 | — | — |
| Dangling references | 0 | 0 | — | — |
| Proof-citation cycles | 0 | 0 | — | — |
| Unique labels | 1,972 | 1,989 | +17 (`cap:` only) | MIG-007 |
| `[D]` | 461 | 461 | 0 | — |
| `[U]` | 212 | 211 | −1 | MIG-009 (SCC correction) |
| `[C]` | 748 | 749 | +1 | MIG-009 |
| `[B]` | 9 | 9 | 0 | — |
| `[O]` | 5 | 5 | 0 | — |
| `[R]` | 349 | 366 | +17 (capsules) | MIG-007 |
| Duplicate labels | 12 benign | 12 benign | 0 | — |

**Verdict: all nine acceptance criteria pass.** The one deliberate status change is a *weakening/correction* (`[U]→[C]`), explicitly review-authorized; every other status, label, and dependency is byte-preserved or additive-`[R]` only.

---

## Addendum — Final semantic-consistency commit (reviewer-directed)

Commit `486455c` (MIG-014…017), applied after the acceptance review, reconciles every remaining live rendered status surface:

**NS (MIG-014):** all 11 dependency-ledger display cells corrected to their referenced environments' declared tags (nine `[O]→[C]`, NS.7.1 `[B]→[C]`, status prop `[U]→[C]`); `rem:NS-chain-status` and `rem:NS7-now-accessible` rewritten as current summaries with dated transition snapshots retained inside them; `cor:NS-claims` now claims domain-bounded conditional CERT-CLOSE while explicitly withholding unconditional global regularity; Scholium `sch:NS-final` identifies the external unconditional Stage-3 frontier instead of UH.3/SB2; the dormant remark was moved above `\end{document}`, retitled "(Note on the pre-canonical record.)", explicitly differentiated from the scholium, and given the label `rem:NS-precanonical-completeness`.

**SCC (MIG-015):** `thm:scc-frontier` keeps `[U]` with the symmetric residual wording for all four items (each "conditionally discharged; residual = …"); its proof now states the four labels are the stable governance ledger for the residual-to-unconditional program; closure-ledger MCS/UC/TSI cells `[O]→[C]`; "CERT-PROJ upgrade" → "residual to unconditional CERT-CLOSE"; the stale remark below the table now records all links conditionally discharged (including MCS existence, carried inside the stated conditions); the "upgraded from CERT-PROJ toward" prose → "has reached conditional CERT-CLOSE; the listed verifications remain necessary for unconditional closure"; the dependency-ledger scrutiny cell → "residual-to-unconditional-closure audit"; the front-block "Four open obligations" list and bridge-stack MCS item corrected under the original C-2 open-declaration clause.

**Validator (MIG-017):** two new rules per the review — check 6 fails on non-comment content after `\end{document}`; check 7 compares every ledger display-status cell against the in-file declared `\status` of its referenced label (per-file resolution, avoiding duplicate-label false positives). **Check 7 immediately caught five further mismatches in Book I, Book III, GR, and YM** (MIG-016), all corrected to their declarations — including one cell that *understated* a `[U]` corollary as `[C]`. Both checks pass on the final corpus.

**Integrity after this commit:** census unchanged (`D461/U211/C749/B9/O5/R366` — every edit was table-cell or `[R]`/prose text); label delta = +1 authorized (`rem:NS-precanonical-completeness`), 0 removed; 0 dangling; 0 cycles; all touched files compile clean; all six affected PDFs regenerated from source; metadata and dashboard rebuilt. Every rendered contradiction enumerated in the acceptance review is verified absent from the regenerated PDFs (`pdftotext` checks: no "[O]" ledger rows against `[C]` declarations, no "blocked by two small… UH.3 and SB2," no "must be discharged / Blocked by / currently unresolved" in SCC).

---

## Addendum 2 — MIG-018 and the definitive release tag

Final rulings on items 10–11 applied (commit tagged as the definitive completed rewrite):
- **Item 10:** the SCC legitimacy-proof intake-survival sentence now timestamps its embedded status report ("at constitution, the ORA–CTM–TIN rungs were proposed or partial, and MCS was the main open burden"), pointing to the conditional-discharge chain (§`sec:ledger`, `prop:scc-status`). This was a **narrowly scoped, individually authorized** proof-body annotation — the only proof-body edit in the entire program — changing no hypothesis, inference, status, label, or proof force.
- **Item 11:** the `%%` MCS glossary line updated to the reviewer's wording; the source now contains no knowingly stale present-tense status language, rendered or not.

**Closure verification:** census delta zero (`D461/U211/C749/B9/O5/R366`), label delta zero, `make check` passes in full (validation incl. checks 6–7; all 17 files compile twice with 0 fatal errors), SCC PDF regenerated (31→32 pp from the added annotation), metadata and dashboard rebuilt. Per the reviewer: **the program is fully accepted with no remaining semantic-consistency exception inside the edited scope.**
