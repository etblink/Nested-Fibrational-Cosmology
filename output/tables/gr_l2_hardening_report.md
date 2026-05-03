# GR L2 Hardening Report

**Status:** passed
**Pilot level:** L2-hardened
**Claims checked:** 15
**Prose files cataloged:** 20
**Failed checks:** 0
**Supersession effect:** none; pilot shell only

## Checks

| Check | Status | Observed | Expected |
|---|---:|---|---|
| `gr.l2.equivalence-report-passed` | **pass** | passed | passed |
| `gr.l2.compile-passed` | **pass** | passed | passed |
| `gr.l2.posture-preserved` | **pass** | domain-bounded-cert-close | domain-bounded-cert-close |
| `gr.l2.frontier-preserved` | **pass** | ['ob:GR.global-subcriticality'] | ['ob:GR.global-subcriticality'] |
| `gr.l2.no-supersession` | **pass** | none; pilot shell only | none; pilot shell only |
| `gr.l2.prose-files-present` | **pass** | 0 | 0 |
| `gr.render.contains.thm:VI.9.1` | **pass** | True | True |
| `gr.render.contains.thm:GR.CP.1` | **pass** | True | True |
| `gr.render.contains.ob:GR.real` | **pass** | True | True |
| `gr.render.contains.thm:GR.realization` | **pass** | True | True |
| `gr.render.contains.ob:GR.deform` | **pass** | True | True |
| `gr.render.contains.thm:GR.deformation` | **pass** | True | True |
| `gr.render.contains.ob:GR.compat` | **pass** | True | True |
| `gr.render.contains.thm:GR.compat` | **pass** | True | True |
| `gr.render.contains.ob:GR.EFE1` | **pass** | True | True |
| `gr.render.contains.ob:GR.EFE2` | **pass** | True | True |
| `gr.render.contains.ob:GR.EFE3` | **pass** | True | True |
| `gr.render.contains.ob:GR.closure` | **pass** | True | True |
| `gr.render.contains.thm:GR.domain` | **pass** | True | True |
| `gr.render.contains.ob:GR.global-subcriticality` | **pass** | True | True |
| `gr.render.contains.status:GR` | **pass** | True | True |
| `gr.scope.thm:GR.CP.1` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.real` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.thm:GR.realization` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.deform` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.thm:GR.deformation` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.compat` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.thm:GR.compat` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.EFE1` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.EFE2` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.EFE3` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.ob:GR.closure` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.thm:GR.domain` | **pass** | domain-bounded | domain-bounded or explicitly global for the terminal frontier |
| `gr.scope.global-frontier-remains-global-open` | **pass** | {'certificate_scope': 'global', 'declared_status': 'O'} | {'certificate_scope': 'global', 'declared_status': 'O'} |

## Prose Preservation Manifest

| Claim | Field | Path | Size | SHA-256 |
|---|---|---|---:|---|
| `thm:VI.9.1` | body_file | `text/spine/VI/thm_VI_governing.md` | 787 | `33f338ff08795df9609e5b1bafecd9b213eec563b0d7ec15179abdbe93853b49` |
| `thm:GR.CP.1` | body_file | `text/branches/GR/thm_GR_CP_1.md` | 179 | `b65f3de8fa47c93e0065800298c9dbe1dc7a15f65736c9029c1ece655756c7b8` |
| `thm:GR.CP.1` | proof_file | `text/branches/GR/proof_thm_GR_CP_1.md` | 19 | `a05edc24405f3dbb52a25ad7223b3df1a67bb88d366ca501384b943d78d54feb` |
| `ob:GR.real` | body_file | `text/branches/GR/ob_GR_real.md` | 168 | `b7dee143bf8ebbdcf5da38f6a9b86403f0948189e2c041a9715649cc10d5a853` |
| `thm:GR.realization` | body_file | `text/branches/GR/thm_GR_realization.md` | 179 | `1235ca3428fd259500dcec61634f3085e457efc0f2b51f6518e5ef7b636c61d3` |
| `thm:GR.realization` | proof_file | `text/branches/GR/proof_thm_GR_realization.md` | 187 | `e851b2690e09c48a608bf9f42180ef504f07da15de8ba1b6a1ece85a01efdb58` |
| `ob:GR.deform` | body_file | `text/branches/GR/ob_GR_deform.md` | 160 | `ebfc8c6f08f1a171819a367c899c2bad95726d65430f0218b40bebb47af91d56` |
| `thm:GR.deformation` | body_file | `text/branches/GR/thm_GR_deformation.md` | 162 | `53f665cf022faac325cb4f941bda1668fbaafd2e726ef24bc0bee57a44c6f474` |
| `thm:GR.deformation` | proof_file | `text/branches/GR/proof_thm_GR_deformation.md` | 170 | `4ceba9ce85037390b9eab2484f64bbd8f6e25e19fa40d0b0fbd11b33d6c57ed9` |
| `ob:GR.compat` | body_file | `text/branches/GR/ob_GR_compat.md` | 189 | `b3e906a8c10036e9a0294958c0f4f8fcd6b5ed8f68dae338a863897d19966967` |
| `thm:GR.compat` | body_file | `text/branches/GR/thm_GR_compat.md` | 192 | `541e63579665db5f735a2a9c04ff1dc7803fc51157b079e332842b712409e0de` |
| `thm:GR.compat` | proof_file | `text/branches/GR/proof_thm_GR_compat.md` | 200 | `9d5e8fcfd2e462f079ebc2dbf19dc23096fb415d9ebc6c3f507a79f266196909` |
| `ob:GR.EFE1` | body_file | `text/branches/GR/ob_GR_EFE1.md` | 72 | `973ba4fe9284397d3ae74650116a71f5fcbf37149adac761bfb346840929c5e4` |
| `ob:GR.EFE2` | body_file | `text/branches/GR/ob_GR_EFE2.md` | 178 | `cbad970ffd5e6b2d32e5aa785134e242b4426674d00ae8f15628f4c2a7e6bbcd` |
| `ob:GR.EFE3` | body_file | `text/branches/GR/ob_GR_EFE3.md` | 185 | `7a7b5c26c4d0f9d2f0faa6dcac5ddffe5c5201dd2e1b15e4f5c9fd180b277d77` |
| `ob:GR.closure` | body_file | `text/branches/GR/ob_GR_closure.md` | 167 | `de64fb4e2ef6ad86156cb172a39a2081e83664500768419982de23400e2e2be5` |
| `thm:GR.domain` | body_file | `text/branches/GR/thm_GR_domain.md` | 170 | `7640f968799cd2faa28bce706100948d2ade788b1e69c88e3c425d1031537f8a` |
| `thm:GR.domain` | proof_file | `text/branches/GR/proof_thm_GR_domain.md` | 178 | `dda0d916a05b89f1d8c0847b9ea8ca219323461695ae678a7113df62fb6e392d` |
| `ob:GR.global-subcriticality` | body_file | `text/branches/GR/ob_GR_global.md` | 87 | `97a335ce9847a84ecfafa92b3e4008d24d17d1fdaff33438bef79a59162fdd48` |
| `status:GR` | body_file | `text/branches/GR/status_GR.md` | 128 | `98d5868680322415154b8b808eec261699b14b93fccaba2b5efd8adad36ff12b` |
