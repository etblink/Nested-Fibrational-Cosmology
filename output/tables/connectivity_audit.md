# NFC Governance Engine — Connectivity Audit
**Schema:** 0.43.0 | **Status:** ✅ PASSED

| Metric | Value |
|--------|-------|
| Total claims | 243 |
| Spine records | 135 |
| Branch records | 108 |
| Branch→Spine edges | 42 |
| Spine→Spine inter-book edges | 25 |
| Backward spine edges | 0 |
| Dangling deps | 0 |
| Status inheritance violations | 0 |
| Xref completeness | 100.0% |
| Errors | 0 |
| Warnings | 0 |

## Six Audit Passes
| Pass | Status | Observed | Expected |
|------|--------|----------|----------|
| `pass1.citation-coverage` | ✅ | 10/10 branches fully cited | All 10 branch status records must cite thm:V.UBLT and thm:VI |
| `pass2.reachability` | ✅ | 10/10 branches fully reach spine | Every branch must transitively reach Books I-II-III-IV-V-VII |
| `pass3.status-inheritance` | ✅ | 0 violations | No [U] claim may depend on a [C] or [O] claim |
| `pass4.dangling-deps` | ✅ | 0 dangling | All dep_ids must resolve to a known claim |
| `pass5.edge-direction` | ✅ | 0 backward | All spine→spine inter-book edges must go to an earlier book  |
| `pass6.xref-completeness` | ✅ | 100.0% (135/135 spine records) | >= 90% of spine records have canonical_xref annotations |

## Reachability Matrix (Pass 2)
| Branch | Books Reached | Expected | OK |
|--------|--------------|---------|-----|
| BIO | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| CRYST | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| GR | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | ✓ |
| LING | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| NS | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | ✓ |
| RH | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| SCC | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| SM | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | ✓ |
| SPEC | `['I', 'II', 'III', 'IV', 'V', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VII']` | ✓ |
| YM | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | `['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']` | ✓ |
