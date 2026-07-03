# NFC Canon-Preserving Rewrite — Release Notes v1.0

**Tag:** `v1.0-canon-rewrite` · **Commit:** `716e6fae585251185ffd15775dd923132f16c88e` (immutable) · **History:** 16 commits from baseline `d5d88c2`.
**Verification at release:** independently verified by reviewer; `make check` passes; program fully accepted with no remaining semantic-consistency exception inside the edited scope.

## What changed
- **Reader orientation repaired corpus-wide.** All 17 canon files gained a `[R]`-tagged Current Status Capsule (`cap:*`) pointing at each file's own authoritative status proposition. Six stale `%%` header status lines replaced (originals retained in place as marked constitutional intake). Four "Prospective Derived Branch" title pages → "Constituted Derived Branch" with a status-pointer subtitle.
- **Scaffold ledgers reconciled.** Canon Ledger PART 4 SM entry (branch "does not exist" → current three-layer status) and YM obligation block ("[O] in canon" → actual `[C]` tags); STATE_OF_CANON count table regenerated to the direct census.
- **In-canon supersessions made legible.** SPEC's early proposition retitled "Initial Constitution Status (superseded)" (label + `[C]` preserved); SCC corrected throughout to conditional CERT-CLOSE including the one authorized status change (`prop:scc-status` `[U]→[C]`, a weakening) and the `thm:scc-r1` Reserved/proof contradiction; NS swept to backward-looking conditional-closure language (11 ledger cells, two remarks, claims corollary, final scholium, dormant tail moved and differentiated); Book VII Branch Status Table completed (4 missing branches added, SM row per ruling F-6, CouplingTransfer removed from the irreducible frontier, "13 items" dated with roster pointer); 5 further ledger display cells in Books I/III, GR, YM corrected to their declarations; one individually-authorized proof-body annotation (SCC intake-survival, timestamped); `[B]` added to every file's status-legend comment.
- **Scaffold built from scratch.** Metadata extractor (1,790 claim records, 18 fields, human-judgment overlay), validation suite (7 checks incl. post-`\end{document}` guard and ledger-cell-vs-declaration consistency), compile gate, Makefile, read-only self-contained dashboard (10 panels), 18-entry migration log.

## What did NOT change
- **No `[O]` was discharged; no status promoted.** The census delta from baseline is exactly `R +17` (capsules) and `U −1 / C +1` (the authorized SCC correction); `[O]` unchanged at 5.
- **No theorem/obligation label renamed or removed.** Label delta: +18, all additive (`cap:*` ×17 + `rem:NS-precanonical-completeness`), 0 removed.
- **No proof mathematics touched.** One proof-body sentence annotated (timestamped) under individual authorization; no hypothesis, inference, or proof force altered anywhere.
- **No generated artifact hand-edited.** All 17 PDFs regenerated from source only.
- **Honest frontier language preserved byte-identical:** Clay gaps B1/B2/B3, Book II's "remaining gap", GR's two-status reading, UBLT "branch candidate" vocabulary, `prop:SM-status` (the preserved superseded baseline).

## Exact acceptance results
All nine acceptance criteria pass (see `FINAL_VALIDATION_REPORT_v1.0.md`): 17/17 files compile twice with 0 fatal errors; 0 dangling references; 0 citation cycles; 1,990 unique labels (12 known-benign duplicates, no new); census `D461/U211/C749/B9/O5/R366`; four frontier accountings kept separate (I: 5 syntactic `[O]`; II: 110 `ob:` labels; III: 4 reduced-frontier items; IV: 10 branch postures); reviewer-rendered NS pp. 35–36 and SCC pp. 27–29 confirmed reconciled.

## Archive manifests (SHA-256)
```
91178938a03ea11954750ea4cfbc5df2ac99765eac3ca4e2789b2752d3fc89c0  NFC_rewritten_corpus.zip
ead789d546b14bb717d106260aec261763627164edb6ba7d5f9f40de1d537353  NFC_rewrite_complete.zip
```
Per-file corpus manifest: `release/CORPUS_MANIFEST_v1.0.sha256` (45 files).

## Deferred (tracked, non-blocking)
`openobligation` deprecation (documented migration path; scheduled for v1.1); full regeneration of `NFC_STATE_OF_CANON.md` from metadata (first post-release task); 12 known-benign duplicate labels (allowlisted, monitored); 11 prose `\status` mentions (documented in `prose_mention_delta`).
