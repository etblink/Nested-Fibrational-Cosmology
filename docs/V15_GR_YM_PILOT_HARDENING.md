# v15 — GR/YM Pilot Hardening

v15 is a controlled hardening release for the governance MVP.

## Changes

- Schema version advanced to `0.15.0`.
- SCC obligation labels and SCC/SM branch posture labels were corrected to match locally inferred effective status.
- Partial discharge semantics were made conservative: a `partial` discharge edge is recorded in the trace but does not close an obligation.
- The accepted warning baseline was reduced from 10 to 2.
- Focused pilot traces were added for GR and YM.

## Governance result

The build now treats the following as regressions unless deliberately approved:

- stale local posture after branch-packet inference is stable;
- stale obligation label where closing discharge evidence exists;
- branch-posture mismatch against the computed local packet.

The remaining accepted warning type is `retired-alias-detected`, preserving visibility into legacy-name drift.
