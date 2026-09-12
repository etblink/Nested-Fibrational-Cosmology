# NFC Provenance Hardening — Preregistration v0.1

Status: `PREREGISTERED`

## 1. Authorization and controlling finding

This is a bounded source-project provenance/navigation repair authorized by the Project Lead after accepted Project Observatory result `OBS-U009`.

Accepted Observatory endpoint:

```text
OBS_U009_ACCEPTANCE = 928f5d79c39b15657b9d4f36a096bcac1807dab8
ACCEPTED_OUTCOME = C__CONTENT_CONTINUITY_AND_MECHANISM_ESTABLISHED__HUMAN_INTENT_UNRESOLVED__HARDENING_REQUIRED
```

This operation does not reopen or reinterpret that result.

## 2. Frozen source identities

```text
PUBLICATION_MAIN_BASE = b8587ce3409e34c0dd4e56c61ee585c07798b0e5
PUBLICATION_MAIN_TREE = f5d2112d6346b659127d596f1f62a2c7069cdc60
PRE_STRIP_MAIN = 0f23c285191ab20bf468868940f385068e7e8717

FROZEN_CANON_REF = archive/nfc-canonical-ed3047c2
FROZEN_CANON_COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78
FROZEN_CANON_TREE = 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973
ISOLATED_CANON_ROOT = d5d88c2e7672b36c9ef7231aa657d967e9feef6b

DECLARED_V1_RELEASE_COMMIT = 716e6fae585251185ffd15775dd923132f16c88e
DECLARED_V1_RELEASE_TAG = v1.0-canon-rewrite
```

The scientific canon commit/tree are immutable inputs to this repair. No theorem-bearing file on the frozen-canon lineage may be edited.

## 3. Repair requirements

The accepted minimum package is:

```text
H1 = durable canonical anchor for ed3047c2... / tree 00ef55ff...
H2 = reconcile stale declared v1.0-canon-rewrite release anchor
H3 = make default main explicitly route theorem-source readers to frozen canon
H4 = record the re-root/import provenance boundary in repository-native documentation
```

## 4. Connector capability boundary

The active GitHub connection can create/update branches, commits, and files. It does not expose tag creation or branch-protection/ruleset mutation.

Therefore this operation separates:

```text
AUTOMATABLE_NOW:
- H3 default-main routing repair
- H4 repository-native provenance crosswalk
- redundant explicit branch anchors for the frozen canon and v1 release commit
- exact validation and publication of those documentation changes

REQUIRES_MANUAL_GITHUB_REF_ADMINISTRATION:
- creation/restoration of immutable tags and/or protection/rulesets sufficient to fully satisfy H1/H2 durability semantics
```

An ordinary branch must not be described as immutable or protected merely because it is named as an anchor.

## 5. Planned refs

If absent, create exact redundant reachability refs:

```text
anchor/frozen-canon-ed3047c2 -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78
anchor/v1.0-canon-rewrite-716e6fa -> 716e6fae585251185ffd15775dd923132f16c88e
```

These are redundancy/discoverability anchors only until separately protected or replaced/supplemented by immutable tags.

## 6. Publication-surface edits

On `maintenance/nfc-provenance-hardening-v0.1` only:

1. Replace the false present-tense statement that default `main` hosts the TeX/PDF corpus.
2. State that `main` is the publication/landing surface.
3. Name the controlling frozen theorem source exactly by ref, commit, and tree.
4. Link/readers to a new `PROVENANCE.md` crosswalk.
5. Preserve existing author, license, DOI, citation, and attribution information unless a minimal wording adjustment is required for routing accuracy.

`PROVENANCE.md` must record:

```text
0f23c285...  theorem-bearing pre-strip main
    -> d5d88c2... isolated content baseline / new Git root
    -> 74 commits
    -> ed3047c2... frozen scientific canon

0f23c285...
    -> b8587ce... deletion-only publication-surface strip
    -> default main
```

It must state that repository evidence establishes the mechanical sequence and representative content continuity, but does not establish the human policy motive for the split.

## 7. Validation gates

The automated candidate may publish to `main` only if all pass:

1. `main` base identity was exactly `b8587ce...` when the maintenance branch opened.
2. frozen canon still resolves exactly to `ed3047c2...` / tree `00ef55ff...`.
3. declared v1 release commit `716e6fa...` remains an ancestor of the frozen canon.
4. maintenance diff is limited to provenance/governance/publication routing files.
5. no theorem-bearing source, PDF, metadata claim graph, migration ledger, or scientific-status file is changed.
6. README no longer claims the default tree contains files absent from it.
7. README identifies the frozen theorem source exactly.
8. `PROVENANCE.md` records the disconnected-history/re-root boundary without inventing human intent.
9. redundant anchor branches, if created, resolve to the exact intended commits.
10. tag/protection limitations are disclosed rather than misrepresented as complete.

## 8. Publication rule

If gates 1–10 pass, integrate the documentation repair into `main` without importing the frozen canon tree into publication main.

The final report must classify H1/H2 as either fully satisfied or `PARTIAL__MANUAL_IMMUTABILITY_STEP_REQUIRED`, based on actual GitHub ref state after automation.

## 9. Scientific firewall

```text
THEOREM_CONTENT_CHANGE = FORBIDDEN
CANON_COMMIT_MOVE = FORBIDDEN
CANON_TREE_CHANGE = FORBIDDEN
DEFAULT_BRANCH_REPLACEMENT_WITH_CANON = NOT_REQUIRED
HUMAN_INTENT_INFERENCE = FORBIDDEN
```
