# v23 — L2 Pilot Standardization

v23 converts the GR/YM L2 pilot comparison into a reusable pilot standard.

## Purpose

The generated successor-pilot layer should not rely on custom one-off checks for each branch. A future branch pilot should declare its expected posture, preserved frontier, compile target, equivalence report, and no-supersession constraints in a single configuration file.

## New files

- `canon/pilot_standard.yaml`
- `build/pilot_standard.py`
- `output/reports/l2_pilot_standard_report.json`
- `output/tables/l2_pilot_standard_report.md`
- `output/tables/l2_pilot_standard_template.md`

## Standard checks

Each configured L2 pilot must pass:

1. equivalence report passed
2. compile target passed
3. expected posture preserved
4. expected frontier preserved
5. no supersession effect
6. active frontier remains open
7. successor TeX exists
8. successor PDF exists

GR also retains its L2 hardening report as a branch-specific additional check.

## Current configured pilots

- GR: `domain-bounded-cert-close`, preserving `ob:GR.global-subcriticality`
- YM: `conditional-cert-close`, preserving `ob:YM.B3.A2`

## Result

The v23 build passes with both configured L2 pilots satisfying the reusable standard.
