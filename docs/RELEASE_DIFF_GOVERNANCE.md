# v13 Release-Diff Governance

v13 adds a conservative release-diff layer.

The purpose is not to invent a new canon session. The included `L_plus_5_draft`
snapshot is a draft governance fixture used to test whether release-to-release
changes are explicit, classified, and basis-supported.

## New files

- `canon/releases/L_plus_5_draft.yaml`
- `build/release_diff.py`
- `output/reports/release_diff_report.json`
- `output/tables/release_diff_report.md`

## Rule

Every detected release-diff event must have an explicit `change_basis` entry in
the target release snapshot.

A change basis records:

- `change_id`
- `change_type`
- `basis`
- `scope_relation`
- `note`

## Current draft changes

The L+5 draft intentionally demonstrates three supported release-diff events:

1. legacy RH active-obligation label removed
2. canonical RH S1 frontier label added
3. NS main frontier surfaced explicitly

All three are basis-supported and scope-preserving. They are governance-label
or frontier-explicitness changes, not mathematical status promotions.

## Quality gate

`gate.release_diff_basis` fails if any release-diff event lacks a basis note.
