# v14 Regression Test Layer

This layer protects the governance MVP against accidental drift.

It verifies:

- schema version identity
- audit error/warning baseline
- warning-class identity
- active open-item identity
- branch posture inference
- protected pilot claim statuses
- release-diff basis coverage

The regression baseline is stored in `canon/regression_baseline.yaml`.

A baseline update should only happen when the project deliberately changes canon
coverage, release state, or accepted warning policy.
