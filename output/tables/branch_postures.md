# Branch Posture Reconciliation

| Branch | Declared | Computed | Source | Reason |
|---|---|---|---|---|
| BIO | conditional-cert-close | conditional-cert-close | branch-packet-inference | BIO posture is inferred from the nondegenerate endpoint packet. |
| CRYST | conditional-cert-close | conditional-cert-close | branch-packet-inference | CRYST posture is inferred from endpoint closure plus the retained phase frontier. |
| GR | domain-bounded-cert-close | domain-bounded-cert-close | branch-packet-inference | Local GR pilot packet supports domain-bounded closure while global curvature-subcriticality / BF-9 remains open. |
| LING | conditional-cert-close | conditional-cert-close | branch-packet-inference | LING posture is inferred from endpoint closure plus the retained reference frontier. |
| NS | domain-bounded-cert-close | domain-bounded-cert-close | branch-packet-inference | NS reaches domain-bounded conditional CERT-CLOSE via NS.6.1+NS.7.1 chain; Stage-3 global frontier remains active. |
| RH | cert-proj | cert-proj | branch-packet-inference | RH posture is cert-proj: RH1-RH3 constituted, S1-ARC irreducibly open. |
| SCC | conditional-cert-close | conditional-cert-close | branch-packet-inference | Local SCC packet supports conditional closure once MCS, UC, and TSI packets are present. |
| SM | intrinsic-structural-close | intrinsic-structural-close | branch-packet-inference | Local SM packet supports intrinsic-structural closure while O-IDcont blocks unconditional force-upgrade. |
| SPEC | cert-close | cert-close | branch-packet-inference | SPEC is inferred closed from a locally unconditional endpoint packet. |
| YM | conditional-cert-close | conditional-cert-close | branch-packet-inference | Local YM pilot packet supports conditional closure through B1/B2/B3 bridge packets while B3-A2 remains the surviving residual frontier. |
