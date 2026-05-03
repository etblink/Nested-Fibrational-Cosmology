# YM Pilot Migration Report

This report is generated from YM branch records and computed governance status.

| ID | Kind | Declared | Computed | Scope | Source | Title |
|---|---|---|---|---|---|---|
| ob:YM.O-ID | obligation | C | C | branch-local | local-discharge-inference | Operator / Target-Side Identification Obligation |
| thm:YM.ID | theorem | C | C | branch-local | declared | YM Identification Discharge Packet |
| ob:YM.O-RIG | obligation | C | C | branch-local | local-discharge-inference | Operator Rigidity Obligation |
| thm:YM.RIG | theorem | C | C | branch-local | declared | YM Rigidity Discharge Packet |
| ob:YM.O-ENC | obligation | C | C | branch-local | local-discharge-inference | Encoding Compatibility Obligation |
| thm:YM.ENC | theorem | C | C | branch-local | declared | YM Encoding Compatibility Packet |
| ob:YM.O-GLOB | obligation | C | C | branch-local | local-discharge-inference | Global Coercivity Obligation |
| thm:YM.GLOB | theorem | C | C | branch-local | declared | YM Global Coercivity Packet |
| ob:YM.O-CLU | obligation | C | C | branch-local | local-discharge-inference | Cluster / Vacuum Uniqueness Obligation |
| thm:YM.CLU | theorem | C | C | branch-local | declared | YM Cluster and Vacuum Packet |
| thm:YM.7 | theorem | C | C | branch-wide | declared | Endpoint Mass-Gap and OS/Wightman Closure Packet |
| ob:YM.B1 | obligation | C | C | branch-local | local-discharge-inference | B1 Quantization Bridge Residual |
| thm:YM.B1.bridge | theorem | C | C | branch-local | declared | B1 Quantization Bridge Conditional Packet |
| ob:YM.B2 | obligation | C | C | branch-local | local-discharge-inference | B2 Domain Bridge Residual |
| thm:YM.B2.bridge | theorem | C | C | branch-local | declared | B2 Domain Bridge Conditional Packet |
| ob:YM.B3 | obligation | C | C | branch-local | local-discharge-inference | B3 Compact Simple SU(3) Bridge Residual |
| thm:YM.B3.bridge | theorem | C | C | branch-local | declared | B3 Compact Simple SU(3) Conditional Packet |
| ob:YM.B3.A2 | obligation | O | O | branch-local | declared | Simple A2 Gap Restriction Without SM Gauge Dependence |
| status:YM | status_note | conditional-cert-close | conditional-cert-close | branch-wide | branch-packet-inference | YM Branch Posture Record |

## Pilot verdict

- YM local posture is expected to compute as `conditional-cert-close`.
- The B1/B2/B3 bridge packets are represented as conditional/scoped packets, not unconditional Clay-grade closure.
- `ob:YM.B3.A2` is expected to remain `O` as the surviving residual frontier in this pilot slice.
- The pilot is successful when conditional closure is represented without promoting YM to unconditional `cert-close`.
