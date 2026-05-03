# GR Branch Successor Equivalence Report

**Status:** passed
**Pilot level:** L2
**Generated claim count:** 15
**Computed GR posture:** `domain-bounded-cert-close`
**Active frontiers:** `ob:GR.global-subcriticality`

## Checks

| Check | Status | Observed | Expected |
|---|---|---|---|
| gr.successor.expected-claim-list | pass | {'missing': []} | All GR_ORDER claims are present. |
| gr.successor.posture | pass | domain-bounded-cert-close | domain-bounded-cert-close |
| gr.successor.frontier-preservation | pass | ['ob:GR.global-subcriticality'] | ['ob:GR.global-subcriticality'] |
| gr.successor.no-unexpected-claims | pass | [] | No branch-local GR records outside the pilot order. |

## Supersession effect

None. This packet is a branch-successor pilot shell, not a replacement for the canonical GR Branch Book.
