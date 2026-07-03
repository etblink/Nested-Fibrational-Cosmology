# NFC Rewrite — Unresolved / Deferred Human-Review Items

All seven blocking review items from the July 2 adjudication were resolved and applied. The following remain open by design (deferred, out of scope, or flagged during execution). None blocks acceptance.

## Deferred by explicit ruling
1. **`openobligation` environment rename.** 110 declarations, only 5 genuinely `[O]`; name is misleading but a rename was ruled out of Phase 7. The compatibility-alias migration path (neutral `obligation` env → alias → mechanical migration → zero-label-change + compile/diff gate) is documented in `metadata/SCHEMA_MIGRATION_PLAN.md` §7. The metadata layer already classifies by `\status` tag, so nothing downstream depends on the rename.

## Flagged during execution (conservative non-edits)
2. **SCC residual CERT-PROJ table cells.** Two obligation-ledger/dependency-table cells ("O-SCC.UC; CERT-PROJ upgrade"; "External scrutiny; CERT-PROJ posture" on the `thm:scc-frontier` row) and one transition sentence ("upgraded from CERT-PROJ toward CERT-CLOSE") were left unchanged: they read as per-obligation/stage descriptions rather than blanket current-status claims, and the C-2 ruling enumerated specific locations. If the reviewer wants these swept too, it is a three-cell edit + compile.
3. **`thm:scc-frontier` remains `[U]`** with items (ii)–(iv) still phrased as blocked/"must be discharged." Item (i) was reconciled to the conditional discharge; items (ii)–(iv) describe the WeakGlue→MCS→UC→TSI dependency ladder, which is still the correct statement of what *unconditional* closure requires, so they were preserved. A reviewer may prefer the same "conditionally discharged; residual = unconditional proof" phrasing applied to (ii)–(iv) for symmetry.
4. **NS dormant tail.** The corrected D-3 remark sits *after* `\end{document}` in `NFC_NS_Branch.tex` (it never renders). Corrected for source consistency, but the reviewer may want it moved above `\end{document}` (one-line move + compile) or deleted; moving/deleting was not authorized, so it was left in place.
5. **STATE_OF_CANON deeper refresh.** Only the count table + counting note were repaired (F-3 scope). The file's mid-section "Open Obligation Register (4 items, as of L+22)" header and other dated interior sections are still dated snapshots; full regeneration of that document from `metadata/` would make it GENERATED end-to-end. Recommended as the next maintenance task.
6. **Book VII "13 items" figure retained as dated.** Per ruling F-8 it now carries a snapshot qualifier + roster pointer rather than a live number. If a live number is ever wanted there, it should be injected from `metadata/` at build time, not hand-typed.

## Known-benign, monitored
7. **12 duplicate labels** (9 per-file `sec:*` + `thm:governing`/`cor:conditional-no-unconditional`/`def:transport-invariant` cross-book copies) — unchanged, allowlisted in `scripts/validate.py`; any *new* duplicate fails the gate.
8. **11 prose `\status` mentions** (GR narrative, NS sub-lemma list) — counted in the raw census, excluded from claim records; documented in `metadata/census.json.prose_mention_delta`.
9. **Extractor's statement-proof node count (835) vs. the corpus's historical "711".** Methodology for the historical figure was never documented; the scripted count is now the canonical one going forward (flagged in `AUDIT_BASELINE.md` §0.7).

## Suggested next maintenance tasks (non-blocking)
- Adopt `make check` as the pre-commit hook for any future canon edit.
- Regenerate STATE_OF_CANON fully from metadata (item 5).
- Schedule the `openobligation` deprecation commit (item 1).
- Add a dashboard "diff two snapshots" panel once a second release snapshot exists (the release_snapshot_view is already diff-ready).
