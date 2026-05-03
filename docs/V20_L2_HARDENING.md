# v20 — L2 Hardening

v20 strengthens the GR L2 branch-successor pilot.

## Purpose

The v19 GR successor pilot proved that a generated branch shell can be produced and compiled. v20 adds a stricter hardening layer so the shell is not merely generated, but auditable as a prose-preserving, frontier-preserving, non-superseding pilot.

## New checks

- base GR successor equivalence report passed
- GR successor PDF compiled and rendered
- `status:GR` remains `domain-bounded-cert-close`
- `ob:GR.global-subcriticality` remains the active frontier
- supersession effect remains `none; pilot shell only`
- every generated claim ID appears in the TeX shell
- every generated claim has non-empty body prose
- declared proof files are present and non-empty
- every generated prose fragment is hashed in a preservation manifest

## Outputs

- `output/reports/gr_l2_hardening_report.json`
- `output/tables/gr_l2_hardening_report.md`
- `output/reports/gr_prose_preservation_manifest.json`

## Non-claim

v20 does not supersede the canonical GR Branch Book. It only strengthens the generated L2 pilot.
