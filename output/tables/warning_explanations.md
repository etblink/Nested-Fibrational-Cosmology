# Current Warning Explanations

## `release-vs-computed-posture-mismatch`

The computed branch posture does not match the active release snapshot.

| Severity | ID | Path | Detail |
|---|---|---|---|
| warning | status:NS | claims/branches/NS/status_NS.yaml | domain-bounded-cert-close |

## `retired-alias-detected`

A retired label appears in an active record. This is usually name-history drift rather than mathematical failure.

| Severity | ID | Path | Detail |
|---|---|---|---|
| warning | ob:GR.EFE1 | claims/branches/GR/ob_GR_EFE1.yaml | O-GR.EFE1-old |
| warning | thm:NS.6.1 | claims/branches/NS/thm_NS_6_1.yaml | KPO3 |
