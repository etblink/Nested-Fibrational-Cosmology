# NS Branch Successor Equivalence Report

**Status:** passed
**Pilot level:** L2
**Generated claim count:** 16
**Computed NS posture:** `domain-bounded-cert-close`
**Stale posture corrected from:** `frontier-blocked`
**Stale posture corrected:** True
**SB2 discharged:** True
**Stage-3 frontier preserved:** True
**Active frontiers:** `ob:NS.bridge-stage2`, `front:NS.main`

## Governance finding

> STALE-POSTURE CORRECTION: NS preamble says frontier-blocked but canonical NS branch book (prop:NS-status, thm:NS71, cor:NS-both-give-endpoint) establishes domain-bounded conditional CERT-CLOSE. Pilot corrects the governance repo posture and documents the NS preamble as requiring a canon maintenance update.

## Domain-bounded hypotheses

Phase-A, K_0=7, PASS, LS-2

## Checks

| Check | Status | Observed | Expected |
|---|---|---|---|
| ns.successor.expected-claim-list | pass | {'missing': []} | All NS_ORDER claims present. |
| ns.successor.posture-correction | pass | domain-bounded-cert-close | domain-bounded-cert-close (correcting stale frontier-blocked) |
| ns.successor.frontier-profile | pass | ['ob:NS.bridge-stage2', 'front:NS.main'] | ['front:NS.main'] |
| ns.successor.sb2-discharged | pass | {'declared': 'C'} | ob:NS.SB2 must be [C] — conditionally discharged via SCT.6b. |
| ns.successor.stage3-frontier-preserved | pass | {'declared': 'O'} | front:NS.main must remain [O] — Stage-3 global unconditional is external frontier. |
| ns.successor.no-unexpected-claims | warn | ['thm:VI.8.1'] | No NS records outside pilot order. |
| ns.successor.no-clay-prize-claim | pass | domain-bounded-cert-close | Must not claim unconditional global regularity or Clay Prize solution. |

## Supersession effect

None. This packet is a branch-successor pilot shell.

## Canon maintenance note

The NS branch preamble (front block) should be updated to reflect domain-bounded conditional CERT-CLOSE, correcting the stale ``frontier-blocked'' language. This is a canon editorial task separate from the governance pilot.
