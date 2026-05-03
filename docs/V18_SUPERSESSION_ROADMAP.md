# v18 — Supersession Roadmap

v18 records the strategic end goal: the governance engine can eventually become the source system for generated successor versions of the NFC spine and branch books.

This is not an immediate replacement. The correct migration is staged.

## Supersession ladder

| Level | Name | Meaning |
|---|---|---|
| L0 | Audit-only | The system audits existing governance metadata. |
| L1 | Importable governance appendix | Generated tables may be imported into current books. |
| L2 | Branch-pilot generated packet | One branch gets a generated shell with preserved human prose and equivalence checks. |
| L3 | Branch successor release candidate | A generated branch book compiles and matches the current canon packet. |
| L4 | Spine successor release candidate | A generated spine book compiles and passes claim/dependency equivalence. |
| L5 | Full corpus supersession | All spine and branch books are generated from structured source. |

## Current v18 state

The project is at **L1**.

The generated governance appendix compiles, and GR/YM have live-shaped pilot governance packets. Full book generation remains future work.

## No-silent-supersession rule

A generated book may supersede an existing book only if:

1. every claim has a stable ID;
2. claim-level force is equivalent or intentionally changed with release-diff basis;
3. branch posture is reconciled;
4. open frontiers are preserved or lawfully discharged;
5. theorem/proof prose is preserved or intentionally revised;
6. generated PDF compiles;
7. equivalence report is reviewed;
8. decision-log approval records the supersession.

## Next recommended milestone

v19 should be an **L2 branch-successor pilot**.

Recommended target: GR, because the GR pilot already has a domain-bounded closure chain and surviving global frontier. The goal should be a generated GR governance shell, not a rewritten GR branch book.
