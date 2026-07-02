# NFC Canon Dashboard (read-only, local-first)

A single self-contained HTML file for inspecting the state of the canon: branch postures, status counts, open obligations, the four frontier accountings, stale/review queue, a claim explorer, a dependency lookup, release-snapshot data, and the generated-artifact map.

## Run it

**Option A — just open it (no server needed).** The dashboard has all data inlined; it opens directly from disk:

```
# macOS
open dashboard/index.html
# Linux
xdg-open dashboard/index.html
# Windows
start dashboard/index.html
```

**Option B — serve it (optional).**

```
python3 -m http.server 8000
# then visit http://localhost:8000/dashboard/
```

## Rebuild it after any metadata change

```
make metadata     # re-extract claim corpus from canon .tex
make dashboard    # rebuild dashboard/index.html from the fresh metadata
```

## Panels

- **Branch overview** — every branch's current posture (verbatim A1 status proposition) + per-branch status-tag counts.
- **Status counts** — the F-3-resolved dual census (raw `\status` vs. environment declarations) with the prose-mention delta explained.
- **Open obligations** — Accounting I: the 5 syntactically `[O]` items with their residuals.
- **Frontier accountings** — all four, side by side, with the explicit "never sum these" warning; the reduced-frontier table (CouplingTransfer correctly excluded per ruling F-6).
- **Stale / review queue** — machine-flagged `review_needed`, `historical`, and `superseded` claims.
- **Claim explorer** — search/filter all 1,773 status-tagged claims by label, branch, status, section, note.
- **Dependency graph** — per-label "depends on / depended on by" lookup over the 1,093 proof-citation edges (0 cycles, validated).
- **Release snapshot** — census + commit + timestamp, for diffing releases.
- **Generated reports** — the 17 PDFs mapped to their `.tex` source of truth.
- **Legend** — status tags and claim-state colour key.

## Read-only guarantee

There is **no write path** from this page back to any canon `.tex` or metadata file. It is a viewer. Editing is out of scope until a safe review workflow is added (a later phase); the current build cannot mutate the corpus. Data is a static snapshot inlined at build time.

## Distinctions the dashboard makes visible

`current` · `historical/intake` · `superseded` · `generated artifact` · `human-review-required` — each rendered with a distinct colour pill so a reader can tell at a glance which claims are live, which are constitutional history, and which need a human.
