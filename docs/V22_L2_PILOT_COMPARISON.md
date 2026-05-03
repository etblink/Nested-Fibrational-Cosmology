# v22 — L2 Pilot Comparison

Purpose: compare the GR and YM generated branch-successor pilots under a shared L2 standard.

This release does not migrate a new branch. It adds a side-by-side comparison layer that checks:

- both pilot equivalence reports pass;
- both standalone PDFs compile;
- GR remains domain-bounded rather than globally closed;
- YM remains conditionally closed rather than unconditionally Clay-grade closed;
- `ob:GR.global-subcriticality` remains open;
- `ob:YM.B3.A2` remains open;
- no generated pilot authorizes supersession of the canonical branch books.

The output is `output/reports/l2_pilot_comparison_report.json` and `output/tables/l2_pilot_comparison_report.md`.
