# GR Pilot Migration Report

This report is generated from GR branch records and computed governance status.

| ID | Kind | Declared | Computed | Scope | Source | Title |
|---|---|---|---|---|---|---|
| ob:GR.real | obligation | C | C | domain-bounded | local-discharge-inference | Controlled Causal-Geometric Realization |
| thm:GR.realization | theorem | C | C | domain-bounded | declared | Controlled Causal-Geometric Realization Theorem |
| ob:GR.deform | obligation | C | C | domain-bounded | local-discharge-inference | Causal-Deformation Response Law |
| thm:GR.deformation | theorem | C | C | domain-bounded | declared | Causal-Deformation Law Theorem |
| ob:GR.compat | obligation | C | C | domain-bounded | local-discharge-inference | Metric/Connection and Einstein-Type Structural Compatibility |
| thm:GR.compat | theorem | C | C | domain-bounded | declared | Metric/Connection Compatible Structural Compatibility Packet |
| ob:GR.EFE1 | obligation | C | C | domain-bounded | local-discharge-inference | EFE Curvature Encoding Obligation |
| ob:GR.EFE2 | obligation | C | C | domain-bounded | local-discharge-inference | EFE Coupling Constants Obligation |
| ob:GR.EFE3 | obligation | C | C | domain-bounded | local-discharge-inference | EFE Diffeomorphism Invariance Obligation |
| ob:GR.closure | obligation | C | C | domain-bounded | local-discharge-inference | Domain-Bounded Gravity Closure Package |
| thm:GR.domain | theorem | C | C | domain-bounded | declared | Domain-Bounded Gravity Closure Theorem |
| ob:GR.global-subcriticality | obligation | O | O | global | declared | Global Curvature-Subcriticality / BF-9 Extension Frontier |
| status:GR | status_note | domain-bounded-cert-close | domain-bounded-cert-close | branch-wide | branch-packet-inference | GR Branch Posture Record |

## Pilot verdict

- GR local posture is expected to compute as `domain-bounded-cert-close`.
- `ob:GR.global-subcriticality` is expected to remain `O` at global scope.
- The pilot is successful when the GR posture is no longer stale while global closure remains blocked.
