# NFC Provenance Hardening — Execution v0.1

Status: `QUALIFIED_FOR_PUBLICATION__IMMUTABILITY_ADMIN_STEP_REMAINS`

Preregistration commit:

```text
4eaf60d7ca6750c648dbc0b186977d20229bb1c4
```

## 1. Frozen identities revalidated

```text
PUBLICATION_MAIN_BASE = b8587ce3409e34c0dd4e56c61ee585c07798b0e5
FROZEN_CANON_REF = archive/nfc-canonical-ed3047c2
FROZEN_CANON_COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78
FROZEN_CANON_TREE = 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973
DECLARED_V1_RELEASE_COMMIT = 716e6fae585251185ffd15775dd923132f16c88e
```

The original canon ref still resolves exactly to `ed3047c2...`. The declared v1 release commit remains an ancestor of frozen canon by 59 commits.

## 2. Redundant anchor refs created

```text
anchor/frozen-canon-ed3047c2
  -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78

anchor/v1.0-canon-rewrite-716e6fa
  -> 716e6fae585251185ffd15775dd923132f16c88e
```

These refs improve explicit discoverability and reachability. They are ordinary branches and are not represented as immutable/protected anchors.

## 3. Publication-routing repair

`README.md` is repaired so it now states:

- default `main` is a lightweight publication/citation/provenance landing surface;
- `main` is not the controlling theorem-bearing source tree;
- frozen theorem source is exactly `archive/nfc-canonical-ed3047c2@ed3047c2...`, tree `00ef55ff...`;
- the TeX/PDF corpus listing describes the archive lineage, not the default tree;
- `PROVENANCE.md` is the repository-native routing/crosswalk document.

Author, DOI, license, citation, and attribution information are retained.

## 4. Provenance crosswalk

New `PROVENANCE.md` records the exact mechanical split:

```text
0f23c285... theorem-bearing pre-strip main
    -> content re-rooted at parentless d5d88c2...
    -> +74 commits
    -> ed3047c2... frozen scientific canon

0f23c285...
    -> b8587ce... direct deletion-only child
    -> publication main
```

It also records exact representative blob continuity for Book I, Book II, and the NS branch, and expressly keeps human policy intent unresolved.

## 5. Candidate diff validation

Relative to exact base `b8587ce...`, the maintenance candidate before this execution record was three commits ahead and zero behind, modifying only:

```text
README.md
governance/NFC_PROVENANCE_HARDENING_PREREGISTRATION_V0_1.md
PROVENANCE.md
```

This execution record is the only additional path.

No theorem-bearing `.tex`, generated PDF, metadata claim graph, migration ledger, branch book, spine book, or frozen-canon file is modified by the publication-surface candidate.

## 6. Preregistered gate results

```text
G1 exact main base identity                     PASS
G2 frozen canon exact identity/tree             PASS
G3 v1 release commit ancestor of frozen canon   PASS
G4 maintenance diff provenance/routing only     PASS
G5 no theorem/scientific-status file changed    PASS
G6 README no longer misdescribes default tree   PASS
G7 README names exact frozen theorem source      PASS
G8 PROVENANCE crosswalk/no intent invention      PASS
G9 redundant anchor refs exact                   PASS
G10 connector tag/protection limitation disclosed PASS
```

## 7. H1–H4 disposition

```text
H1 durable canonical anchor
   = PARTIAL__REDUNDANT_EXACT_REF_CREATED__IMMUTABILITY_OR_PROTECTION_PENDING

H2 reconcile stale v1.0-canon-rewrite release anchor
   = PARTIAL__EXACT_RELEASE_COMMIT_REANCHORED__DECLARED_TAG_RECREATION_PENDING

H3 default-main theorem-source routing
   = SATISFIED_BY_CANDIDATE

H4 repository-native re-root/import provenance crosswalk
   = SATISFIED_BY_CANDIDATE
```

The active connector does not expose tag creation or branch-protection/ruleset mutation. Therefore H1/H2 cannot honestly be classified as fully complete from this execution alone.

## 8. Minimum remaining administrative step

To complete H1/H2 durability semantics without changing scientific content:

```text
1. Create immutable tag for frozen canon, recommended:
   nfc-canonical-ed3047c2
   -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78

2. Restore declared release tag:
   v1.0-canon-rewrite
   -> 716e6fae585251185ffd15775dd923132f16c88e

3. Optionally protect archive/nfc-canonical-ed3047c2 and/or
   anchor/frozen-canon-ed3047c2 with a ruleset preventing force-push/deletion.
```

Tag names and target SHAs must be exact. Do not retarget the tags to later descendants.

## 9. Publication authorization result

All preregistered automated validation gates pass. The documentation/provenance candidate is qualified to fast-forward into `main` provided `main` still equals `b8587ce...` immediately before publication.

```text
THEOREM_CONTENT_CHANGED = NO
FROZEN_CANON_COMMIT_MOVED = NO
FROZEN_CANON_TREE_CHANGED = NO
DEFAULT_BRANCH_REPLACED_WITH_CANON = NO
```
