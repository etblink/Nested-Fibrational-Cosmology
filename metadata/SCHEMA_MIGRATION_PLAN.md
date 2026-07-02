# NFC Machine-Readable Metadata — Schema & Migration Plan (Phase 5)

**Produced:** Phase 5. Scaffold only (no canon edited).
**Status:** implemented and running. `make metadata` regenerates the corpus below from the 17 canon `.tex` files; `make validate` checks it.

---

## 1. Why this exists

Before Phase 5 there was **no** machine-readable layer: every count, obligation list, and status table was hand-maintained prose, which is exactly why the corpus drifted (F-1…F-9). This schema makes the `.tex` sources the single source of truth and makes every count a *regenerated artifact* rather than a hand-typed one. In particular it **permanently resolves F-3**: the State-of-Canon count table becomes a generated view, not a number someone must remember to update.

**Core design ruling (from the review):** the *authoritative status classifier is the `\status{X}` tag, not the environment name.* The `openobligation` environment holds 110 obligation declarations of which only 5 are `[O]`; the schema classifies by tag and treats the environment name as a separate, non-authoritative field. This is what lets `openobligation` be deprecated later (compatibility-alias migration) without any status meaning depending on it.

---

## 2. Record schema (one record per status-tagged environment)

All 18 required fields are present. Fields split into **extracted** (derived mechanically from the `.tex`, overwritten on every run) and **overlay** (human judgment, stored in `metadata/overlay.json`, merged by `claim_id`, and never clobbered by re-extraction).

| Field | Source | Meaning |
|---|---|---|
| `claim_id` | extracted | the `\label{}` key (or a positional id if unlabeled). Primary key. |
| `source_file` | extracted | canon `.tex` filename. |
| `source_section` | extracted | nearest enclosing `\section`/`\subsection` title. |
| `claim_type` | extracted | theorem / proposition / corollary / lemma / definition / remark / obligation / standing_rule / hypothesis. |
| `environment` | extracted | raw LaTeX env name (`openobligation` vs `obligation`, `scholium` vs `remark`) — kept distinct from `claim_type` so the env rename can be tracked later. |
| `status_tag` | extracted | D / U / C / B / O / R — **the authoritative classifier.** |
| `status_force` | extracted | human-readable force descriptor derived from the tag. |
| `branch` | extracted | SPINE or branch code (YM, NS, …). |
| `dependencies` | extracted | for statements: labels cited in the following `proof` block; else all refs in the body. |
| `discharge_basis` | overlay | why/at-what-scope an obligation is (conditionally) discharged. |
| `supersedes` / `superseded_by` | overlay | supersession links (e.g. `prop:SM-status-reconciliation` supersedes `prop:SM-status`). |
| `historical` | overlay | true = constitutional-intake / superseded record, not current status. |
| `authority_level` | overlay (heuristic default) | A1 / A2 / A3 / B / C / D tier from `CANON_AUTHORITY_MODEL.md`. |
| `frontier_accounting` | extracted | which of the four accountings this claim belongs to (never a single merged number). |
| `generated_from` | extracted | null for canon (authored); set for generated artifacts. |
| `last_reviewed` | overlay | date a human last signed off. |
| `reviewer_note` | overlay | free-text ruling / caution. |
| `review_needed` | overlay | true = in the human-review queue. |

**Idempotence:** stable sort + `sort_keys`, so re-running on unchanged sources yields byte-identical files (clean diffs). **Separation of concerns:** mechanical facts are never hand-edited; human judgments never get overwritten.

---

## 3. The five status views (`metadata/views.json`)

Generated simultaneously, each answering a different question:

1. **formal_tag_view** — D/U/C/B/O/R environment census.
2. **branch_posture_view** — each branch's A1 posture (verbatim, review-approved).
3. **obligation_roster_view** — all `ob:` labels partitioned by tag.
4. **reduced_frontier_view** — the 4 deep-frontier items with their live labels.
5. **release_snapshot_view** — census + `census_commit` + timestamp, for snapshot diffing.

## 4. The four frontier accountings (`metadata/census.json`) — never summed

Carried as four separate objects with an explicit `_warning` that they measure different things: **I** syntactic `[O]` census (5), **II** named-obligation roster (110 `ob:` labels), **III** reduced irreducible frontier (4 items), **IV** branch posture (per-branch). The extractor refuses to produce a single "open count."

---

## 5. F-3 reconciliation, baked in

`census.json` reports **both**:
- `raw_grep_census` = every `\status{X}` occurrence = **D461/U212/C748/B9/O5/R349** (the review-endorsed F-3 numbers), and
- `environment_census` = status-tagged *declarations* = D461/U211/C739/B8/O5/R349 (1,773 claim records),

with `prose_mention_delta` (U+1, C+9, B+1 = 11) explaining the difference as inline prose status-mentions (GR narrative "is `[C]`", NS inline sub-lemma tags) that are not standalone declarations. Both are correct for their own question; neither is "the" number in isolation. The stale State-of-Canon table (443/209/685) is superseded by regenerating from this file.

---

## 6. Sample records

**A preserved superseded baseline (SM):**
```json
{
  "claim_id": "prop:SM-status", "source_file": "NFC_SM_Branch.tex",
  "claim_type": "proposition", "status_tag": "C", "branch": "SM",
  "superseded_by": "prop:SM-status-reconciliation", "historical": true,
  "authority_level": "A1_branch_status_proposition",
  "reviewer_note": "PRESERVE as baseline referenced by prop:SM-status-reconciliation (SM-Old). Do not edit or delete.",
  "last_reviewed": "2026-07-02", "review_needed": false
}
```

**A genuinely-open obligation (BIO), in two accountings:**
```json
{
  "claim_id": "ob:bio-BND-open", "environment": "openobligation",
  "status_tag": "O", "branch": "BIO",
  "frontier_accounting": ["I_syntactic_O", "II_named_roster"],
  "discharge_basis": "toolkit-boundary residual; BND forced except trivial-core."
}
```

---

## 7. Migration path for the `openobligation` deprecation (deferred, per ruling)

Not done in Phase 7. When scheduled as a dedicated maintenance commit:
1. Introduce a neutral `obligation` environment (identical rendering).
2. Keep `openobligation` as a `\let`/`\newenvironment` **compatibility alias** so existing sources compile unchanged.
3. Migrate occurrences mechanically, **zero** label/reference changes.
4. Gate on full compile + census stability + `make validate` (0 dangling, 0 new dups) + PDF-diff review.

Because this schema already classifies by `status_tag` (not env name), **no count, view, or dashboard element depends on the rename** — the deprecation is purely cosmetic to the metadata layer.

---

## 8. How to run

```
make metadata   # regenerate claims/edges/views/census from canon .tex
make validate   # structural checks (labels, refs, cycles, census stability)
make compile    # compile gate (all 17 files, fatal=fail)
make check      # validate + compile  (the Phase-7 edit gate)
make dashboard  # rebuild read-only dashboard from current metadata
```
