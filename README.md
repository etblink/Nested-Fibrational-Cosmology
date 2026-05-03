## v25 — Project Lead Pilot Portfolio

v25 adds a Project Lead intake layer for branch-pilot expansion. It does not migrate a new branch. Instead, it ranks the next candidate branches, checks candidate postures against computed governance state, and recommends the next L2 successor pilot by readiness, canon value, and risk.

New files:

- `canon/pilot_intake.yaml`
- `build/pilot_intake.py`
- `output/reports/pilot_intake_report.json`
- `output/tables/pilot_intake_report.md`

Run the full build with:

```bash
python build/build.py
```

Current recommended next pilot: `SCC`.


## v23 — L2 Pilot Standardization

v23 factors the GR/YM L2 pilot checks into a reusable pilot standard. The standard is configured in `canon/pilot_standard.yaml`, executed by `build/pilot_standard.py`, and gated by `gate.l2_pilot_standard`.

The generated outputs are:

- `output/reports/l2_pilot_standard_report.json`
- `output/tables/l2_pilot_standard_report.md`
- `output/tables/l2_pilot_standard_template.md`

Run the full build with:

```bash
python build/build.py
```

The current configured L2 pilots are GR and YM. Both must compile, pass equivalence, preserve their expected branch posture, preserve their active frontier, and avoid any supersession effect.


## v21 — YM Branch-Successor Pilot

v21 adds a generated YM L2 branch-successor pilot. The pilot compiles to PDF and is checked by an equivalence report plus a quality gate. It preserves `status:YM = conditional-cert-close` while keeping `ob:YM.B3.A2` active as the residual frontier. It does not supersede the canonical YM Branch Book.

Run:

```bash
python build/build.py
```

# NFC Governance Starter

A minimal governance-first starter pack for the NFC canon.

This repo skeleton is designed to make governance drift visible before any full TeX generation.
It includes:

- central status and posture vocabularies
- alias registry
- governance rules
- a few sample claim/frontier records
- human-authored body/proof text files
- a first-pass validator and audit report generator

## Quick start

```bash
python build/validate.py
```

This writes JSON audit reports into `output/reports/`.

## Current checks

- required core fields
- dependency resolution
- detection of retired aliases in active records
- basic promotion checks (`C -> U` needs transfer basis)
- explicit discharge edge requirement
- stale-label detection against a toy `status_facts.yaml`

## Notes

This is intentionally an MVP. It does not yet compute full effective status from theorem graphs.
Instead, it demonstrates the architecture and reporting shape needed to support that.

## Added pressure-test slice

This starter now includes:

- Book VII governance claims (`VII.2.4`, `VII.2.5`, `VII.4.3`, `VII.6.4`)
- GR, YM, NS, and SM posture records
- a posture reconciliation report against `canon/releases/L_plus_4.yaml`


## Added real-slice migration v3

This version extends the pressure-test slice with SPEC, SM, BIO, LING, CRYST, RH, and one additional GR frontier object, plus a richer L+4 release snapshot and branch-posture reconciliation basis.


## Added local inference v4

This version starts replacing hand-curated `status_facts.yaml` entries with local inference.

It now computes effective status for:
- `ob:GR.EFE1` from explicit discharge edges in the GR packet
- `status:GR` from the GR packet plus the surviving global frontier
- `status:YM` from the YM endpoint packet plus live B3-A2 burden
- `status:SM` from the SM intrinsic closure packet plus live `O-IDcont`
- `status:NS` from its active named frontier
- `status:SPEC` from its locally unconditional endpoint packet

The validator now writes `output/reports/computed_statuses.json` so you can inspect whether an effective status came from:
- declared metadata
- remaining manual status facts
- local discharge inference
- branch-packet inference


## v5 update: SCC local inference

This version adds a live-shaped SCC packet to the local inference layer.

New SCC records:
- `ob:SCC.MCS`
- `ob:SCC.UC`
- `ob:SCC.TSI`
- `thm:SCC.MCS`
- `thm:SCC.UC`
- `thm:SCC.TSI`

The branch posture rule now infers:

```text
status:SCC = conditional-cert-close
```

when the MCS, UC, and TSI packets are present at conditional or unconditional force.

This removes the earlier release-vs-computed SCC mismatch. The remaining SCC finding is now the more useful stale-posture warning:

```text
declared posture: cert-proj
computed posture: conditional-cert-close
```

That is the intended behavior for local stale-governance detection.


## v6 update

This version removes the remaining hand-entered effective-status facts for the migrated
sample slice. Effective status is now derived from:

1. declared claim records,
2. explicit discharge edges,
3. local branch-packet inference rules, and
4. the L+4 release snapshot for reconciliation checks.

New generated tables are written to `output/tables/`:

- `branch_postures.md`
- `active_frontiers.md`
- `audit_issues.md`

The `canon/status_facts.yaml` file remains available as a manual override layer, but is
intentionally empty in this version so the migrated slice demonstrates local inference
rather than restated reconciliation facts.

## v7 — Generated governance artifacts

This version adds a first rendering layer. The validator remains the source of truth for computed statuses, but `build/render.py` now turns the computed graph into importable governance artifacts.

Run:

```bash
python build/validate.py
python build/render.py
```

Generated outputs:

- `output/tex/branch_postures.tex`
- `output/tex/active_frontiers.tex`
- `output/tex/claim_catalog.tex`
- `output/tex/audit_issues.tex`
- `output/tex/governance_packet.tex`
- `output/tables/release_reconciliation.md`

The TeX files are intentionally table-only fragments. They are designed to be imported into canon appendices or status packets before the project migrates to full book rendering.

## v8: one-command build pipeline

Run the whole governance MVP with:

```bash
python build/build.py
```

This executes validation, renders Markdown/TeX governance artifacts, and writes a build manifest.

New v8 outputs:

- `output/build_manifest.json`
- `output/reports/governance_digest.json`
- `output/tables/governance_digest.md`
- refreshed TeX fragments in `output/tex/`

The build returns a nonzero exit code only if a script crashes or the audit contains errors.
Stale labels and posture mismatches remain warnings during the MVP phase so the repo can keep compiling while drift is being reviewed.


## v9 — Governance Core Stabilization

v9 intentionally does **not** expand canon coverage. It stabilizes the governance
core so later migration is safer.

New stabilization artifacts:

- `canon/schema_version.yaml`
- `canon/claim_schema.yaml`
- `canon/severity.yaml`

New/strengthened validation behavior:

- schema version check
- strict claim-shape validation
- strict scope-shape validation
- strict discharge-edge validation
- status vocabulary validation
- branch-posture vocabulary validation
- status/posture trace generation
- current warning explanations

New generated review files:

- `output/tables/why_status.md`
- `output/tables/warning_explanations.md`

Build entry point:

```bash
python build/build.py
```

v9 also rewrites `build/build.py` to run validation and rendering in-process rather
than by spawning subprocesses. The standalone scripts still work:

```bash
python build/validate.py
python build/render.py
```

Current v9 governance result:

- schema version: `0.9.0`
- claims: 40
- computed statuses: 40
- warnings: 15
- errors: 0

The remaining warnings are intentional MVP governance findings rather than malformed
schema errors. They are documented in `output/tables/warning_explanations.md`.

## v10 — Project Lead Controls

This version does not expand canon coverage. It adds operational controls around the v9 governance core:

- `PROJECT_LEAD_BRIEF.md`
- `ROADMAP.md`
- `MIGRATION_PLAN.md`
- `RISK_REGISTER.md`
- `DECISION_LOG.md`
- `canon/project_governance.yaml`
- `build/quality_gate.py`
- `output/reports/quality_gate_report.json`
- `output/tables/quality_gate_report.md`

Run the full controlled build with:

```bash
python build/build.py
```

The quality gate currently enforces:

- zero audit errors
- zero release-vs-computed mismatches
- warning count at or below the accepted v9 baseline
- every active open item in the digest appears in computed statuses

This turns the starter from a governance prototype into a project-managed MVP baseline.

## v11 — GR Pilot Migration

v11 migrates the GR sample into a more live-shaped branch packet. It adds the GR five-stage closure chain, EFE1–3 records, domain-bounded closure inference, and retains global curvature-subcriticality / BF-9 as the surviving frontier.

Run:

```bash
python build/build.py
```

Generated GR pilot report:

- `output/tables/gr_pilot_report.md`
- `output/reports/gr_pilot_report.json`


## v12 — YM Pilot Migration

v12 migrates a more live-shaped YM packet. It adds the YM bridge stack
(O-ID/O-RIG/O-ENC/O-GLOB/O-CLU), B1/B2/B3 post-program bridge packets,
and preserves `ob:YM.B3.A2` as the surviving residual frontier.

Run:

```bash
python build/build.py
```

New report:

- `output/tables/ym_pilot_report.md`
- `output/reports/ym_pilot_report.json`
- `docs/YM_PILOT_MIGRATION.md`


## v13 — Release-diff governance

This version adds release-to-release comparison.

New command behavior:

```bash
python build/build.py
```

now also runs:

```bash
python build/release_diff.py
```

The release-diff layer compares the active release in `canon/project_governance.yaml`
against the configured comparison release.

Current config:

- active release: `L_plus_4`
- comparison release: `L_plus_5_draft`

Generated outputs:

- `output/reports/release_diff_report.json`
- `output/tables/release_diff_report.md`

Every detected release-diff event must be basis-supported in the target release's
`change_basis` block. This is enforced by `gate.release_diff_basis`.


## v14 — Regression Test Layer

v14 adds a conservative regression-test layer. The build now checks the expected
schema version, claim counts, active-open-item identity, warning classes, release-diff
basis coverage, selected protected claim statuses, and computed branch postures.

Run the full build:

```bash
python build/build.py
```

Primary new outputs:

- `output/reports/regression_test_report.json`
- `output/tables/regression_test_report.md`

The accepted baseline lives in `canon/regression_baseline.yaml`. Updating that file
should be treated as a governance decision, not a routine formatting change.


## v15 — GR/YM Pilot Hardening

v15 is a hardening release. It does not expand canon coverage. It tightens the governance model by:

- updating the schema to `0.15.0`;
- correcting SCC and SM local posture labels now that their branch-packet inferences are stable;
- treating `partial` discharge edges as progress records rather than closing edges;
- reducing the warning baseline from 10 to 2;
- adding focused GR/YM pilot status traces in `output/tables/pilot_status_traces.md`.

Run the full build with:

```bash
python build/build.py
```

The accepted v15 warnings are retired-alias detections only. Stale-label and branch-posture warnings should now be treated as regressions unless deliberately reintroduced with a decision-log entry.


## v16 — Canon Import Pilot

v16 adds a canon-import layer without migrating full book prose.

New generated artifacts:

- `output/tex/canon_governance_appendix.tex`
- `output/tex/canon_governance_appendix_standalone.tex`
- `output/reports/canon_import_manifest.json`
- `output/tables/canon_import_manifest.md`

The full build now runs:

```bash
python build/build.py
```

and includes a `gate.canon_import_packet` quality gate. The generated appendix is
intended to be imported into a canon status appendix or compiled via the standalone
wrapper for local review.


## v17 Compile Verification

v17 adds a compile-check step to the one-command build. After the canon-import packet is generated, the build compiles the standalone TeX wrapper to PDF and renders the PDF to page images.

Run:

```bash
python build/build.py
```

New outputs:

- `output/pdf/canon_governance_appendix_standalone.pdf`
- `output/pdf_render_check/page-1.png`
- `output/reports/compile_check_report.json`
- `output/tables/compile_check_report.md`

The quality gate `gate.compile_verification` fails if the PDF cannot be compiled or rendered.


## v18 — Supersession Roadmap

v18 clarifies the long-term direction: the generated corpus may eventually replace and supersede the current spine and branch books, but only by staged equivalence and release approval.

New artifacts:
- `project/supersession_policy.yaml`
- `build/supersession_readiness.py`
- `output/reports/supersession_readiness_report.json`
- `output/tables/supersession_readiness_report.md`
- `docs/V18_SUPERSESSION_ROADMAP.md`

Current policy:
- generated governance appendices are import-ready;
- GR/YM branch pilots are the next successor-corpus step;
- full corpus supersession is explicitly **not** approved in v18.


## v19 — GR Branch-Successor Pilot

v19 advances the project from L1 importable governance appendices to an L2 branch-pilot generated packet.

New generated artifacts:
- `output/tex/gr_branch_successor.tex`
- `output/tex/gr_branch_successor_standalone.tex`
- `output/pdf/gr_branch_successor_standalone.pdf`
- `output/reports/gr_successor_equivalence_report.json`
- `output/tables/gr_successor_equivalence_report.md`

The GR successor pilot is a generated governance shell over migrated GR claim records and human-authored prose stubs. It is not a replacement for the canonical GR Branch Book. It verifies that the migrated GR packet preserves the current computed branch posture, keeps `ob:GR.global-subcriticality` open, compiles to PDF, and passes the L2 equivalence check.

Run:

```bash
python build/build.py
```


## v20 — L2 Hardening

v20 hardens the L2 GR branch-successor pilot without expanding canon coverage.

New outputs:
- `output/reports/gr_l2_hardening_report.json`
- `output/tables/gr_l2_hardening_report.md`
- `output/reports/gr_prose_preservation_manifest.json`

New guarantees:
- generated GR claim IDs are present in the TeX shell
- every GR pilot claim has non-empty body prose
- declared proof files are present and non-empty
- the GR global-subcriticality frontier remains open at global scope
- the GR successor pilot still has no supersession effect

Run:
```bash
python build/build.py
```

If the full build is slow in a constrained environment, the v20 hardening step can be run directly:
```bash
python build/gr_l2_hardening.py
```


## v22 — L2 Pilot Comparison

Run `python build/build.py` to validate, render, compile, and compare the GR/YM L2 pilots. The new comparison report is written to `output/tables/l2_pilot_comparison_report.md` and `output/reports/l2_pilot_comparison_report.json`.


## v24 — SPEC Branch-Successor Pilot

v24 adds the first zero-frontier L2 branch-successor pilot.

SPEC is intentionally different from GR and YM:
- GR preserves a domain-bounded close with a live global frontier.
- YM preserves conditional closure with a live residual Clay-grade frontier.
- SPEC preserves `cert-close` on the declared gauge-response spectroscopy regime with no SPEC-local active frontier in the pilot.

New outputs:
- `output/tex/spec_branch_successor.tex`
- `output/tex/spec_branch_successor_standalone.tex`
- `output/pdf/spec_branch_successor_standalone.pdf`
- `output/reports/spec_successor_equivalence_report.json`
- `output/tables/spec_successor_equivalence_report.md`

Run:
```bash
python build/build.py
```

The reusable L2 pilot standard now supports both frontier-preserving and zero-frontier branch pilots.


## v26 — SCC Branch-Successor Pilot

v26 adds the fourth L2 branch-successor pilot: SCC.

Run:

```bash
python build/build.py
```

Generated SCC artifacts:

- `output/tex/scc_branch_successor.tex`
- `output/tex/scc_branch_successor_standalone.tex`
- `output/pdf/scc_branch_successor_standalone.pdf`
- `output/reports/scc_successor_equivalence_report.json`
- `output/tables/scc_successor_equivalence_report.md`

The SCC pilot preserves `status:SCC = conditional-cert-close` through the MCS+UC+TSI structural packet. It explicitly does not assert phenomenological, conscious, or experiential content.

## v27 — CRYST Branch-Successor Pilot

v27 adds CRYST as the fifth reusable L2 branch-successor pilot. The generated packet preserves `status:CRYST = conditional-cert-close` and keeps `ob:CRYST.phase-problem` active. It does not claim a solution of the crystallographic phase problem and does not promote the branch to unconditional crystallography closure.

New files:
- `build/cryst_branch_successor.py`
- `output/tex/cryst_branch_successor.tex`
- `output/tex/cryst_branch_successor_standalone.tex`
- `output/reports/cryst_successor_equivalence_report.json`
- `output/tables/cryst_successor_equivalence_report.md`

Run the full build with:

```bash
python build/build.py
```


## v28 — LING Branch-Successor Pilot

Adds the generated LING L2 successor pilot under the reusable pilot standard. The pilot preserves `status:LING = conditional-cert-close` and keeps `ob:LING.REF-INVIS-RECOV` open.
