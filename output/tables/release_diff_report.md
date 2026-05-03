# Release Diff Report

**Source release:** `L+4`
**Target release:** `L+5-draft`
**Target status:** `draft-for-governance-testing`
**Detected changes:** 5
**Changes missing basis:** 0

| Change ID | Category | Item | Before | After | Basis? | Type | Scope | Note |
|---|---|---|---|---|---|---|---|---|
| branch-posture:update:NS | branch-posture | NS | frontier-blocked | domain-bounded-cert-close | yes | stale-posture-correction | restricted | NS posture corrected from frontier-blocked to domain-bounded-cert-close. Canonical NS branch book contains prop:NS-status [C], thm:NS71 [C], and cor:NS-both-give-endpoint [C] establishing domain-bounded conditional CERT-CLOSE. The NS preamble was stale. Correction surfaced by v31 pilot. |
| active-obligation:remove:ob:NS.SB2 | active-obligation | ob:NS.SB2 | active | absent | yes | obligation-discharge | preserved | ob:NS.SB2 conditionally discharged via SCT.6b coercive-transport mechanism (thm:NS.SB2-discharged). Full discharge conditional on Phase-A/K_0=7/PASS/SCT.6b. |
| active-obligation:remove:ob:rh-s1-formal | active-obligation | ob:rh-s1-formal | active | absent | yes | alias-normalization | preserved | Retired/legacy RH active-obligation label is replaced by the local canonical S1 frontier record. No mathematical force changes. |
| active-obligation:add:front:NS.main | active-obligation | front:NS.main | absent | active | yes | frontier-explicitness | preserved | The NS main frontier is listed explicitly while preserving the underlying SB2 obligation. |
| active-obligation:add:thm:RH.S1.formal | active-obligation | thm:RH.S1.formal | absent | active | yes | alias-normalization | preserved | Canonical local RH S1 record is surfaced in the active-obligation list. |
