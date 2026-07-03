# Maintenance Migration Report — `openobligation` Deprecation (v1.1, MIG-019)

**Scope:** the source-level deprecation documented in `metadata/SCHEMA_MIGRATION_PLAN.md` §7 and deferred out of the v1.0 rewrite by explicit ruling.

**What was done.**
1. A neutral environment `obligation` was introduced in every canon file that defines `openobligation`, sharing the **same counter** (`[theorem]`) and the **same display name** ("Open Obligation") — rendering is therefore identical by construction, including numbering.
2. All 99 `\begin{openobligation}`/`\end{openobligation}` pairs were migrated mechanically to `obligation` (BIO 15, CRYST 15, LING 16, RH 12, SCC 5, SM 7, SPEC 11, YM 18; GR defines the environment but has no uses — definition-only change).
3. `openobligation` **remains defined** in every preamble as a compatibility alias (marked DEPRECATED in a comment): any old source or external snippet still compiles unchanged.

**Gate results (all required to pass; all passed).**
- **Zero label changes:** git-diff label audit — added: [], removed: [].
- **Zero status changes:** raw census byte-identical (`D461/U211/C749/B9/O5/R366`).
- **Identical rendered theorem content:** `pdftotext` before/after diff on all 9 affected PDFs — identical in every file.
- `make check` passes in full (validation incl. checks 6–7; all 17 files compile twice, 0 fatal).
- Metadata layer unaffected by design: the extractor classifies by `\status{X}` tag, and `obligation` was already in its environment list since Phase 5 — claim count, `ob:` roster (110), and all four frontier accountings unchanged.

**Deliberately not done (future, individually-reviewed presentation decision):** changing the *displayed* heading from "Open Obligation" to "Obligation". That would alter rendered text and is excluded from this compatibility-preserving migration; the reader-facing status truth is already carried by each environment's `[C]`/`[B]`/`[O]` tag and the Current Status Capsules.
