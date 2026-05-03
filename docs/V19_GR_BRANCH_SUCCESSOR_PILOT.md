# v19 — GR Branch-Successor Pilot

v19 is the first L2 generated branch-pilot packet.

## Purpose

The goal is to test whether a branch book shell can be regenerated from structured governance records and human-authored prose fragments without claiming supersession of the live branch book.

## Generated artifacts

- `output/tex/gr_branch_successor.tex`
- `output/tex/gr_branch_successor_standalone.tex`
- `output/pdf/gr_branch_successor_standalone.pdf`
- `output/reports/gr_successor_equivalence_report.json`
- `output/tables/gr_successor_equivalence_report.md`

## Equivalence criteria

The pilot passes if:

1. all expected GR migrated records are present;
2. the computed GR posture is `domain-bounded-cert-close`;
3. `ob:GR.global-subcriticality` remains open;
4. there are no unexpected GR pilot records outside the declared order;
5. the standalone generated PDF compiles and renders.

## Supersession effect

None. This is an L2 generated packet only. The canonical GR Branch Book remains authoritative.
