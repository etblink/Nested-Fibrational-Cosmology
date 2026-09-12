# Nested Fibrational Cosmology — Repository Provenance and Canon Routing

This document records the repository-level relationship between the lightweight publication surface on `main` and the frozen theorem-bearing NFC scientific corpus.

It is a provenance/navigation document only. It does not alter, reinterpret, promote, demote, or supersede any scientific claim.

## Canonical theorem-source rule

For analysis of the frozen NFC scientific canon, use this exact source identity:

```text
REF = archive/nfc-canonical-ed3047c2
TAG = nfc-canonical-ed3047c2
COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78
TREE = 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973
```

The theorem-bearing TeX/PDF corpus, governance material, metadata, release artifacts, and validation machinery live on that frozen lineage. The default `main` branch is a publication/landing surface and is not the controlling theorem source.

Two explicit repository anchors now resolve to the same frozen canon commit:

```text
archive/nfc-canonical-ed3047c2
    -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78

refs/tags/nfc-canonical-ed3047c2
    -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78
```

A redundant branch also preserves reachability/discoverability:

```text
anchor/frozen-canon-ed3047c2
    -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78
```

The tag supplies a stable named release/canon pointer. Repository tag-protection/ruleset enforcement may be added as optional administrative tamper-resistance, but is not required for source identification at this recorded state.

## Why `main` and the canon have disconnected Git histories

Repository-native evidence establishes the following mechanical sequence.

### Publication-history side

```text
0f23c285191ab20bf468868940f385068e7e8717
    theorem-bearing pre-strip main
        |
        | direct child commit `remove`
        | zero additions / 53,368 deletions
        v
b8587ce3409e34c0dd4e56c61ee585c07798b0e5
    lightweight publication main baseline
```

### Canon-development side

```text
0f23c285191ab20bf468868940f385068e7e8717
    theorem-bearing pre-strip corpus
        |
        | content carried into an isolated working-copy baseline
        | (new Git root; not a Git parent/child edge)
        v
d5d88c2e7672b36c9ef7231aa657d967e9feef6b
    `Baseline snapshot: isolated working copy of NFC corpus as received`
        |
        | 74 further canon/audit/migration commits
        v
ed3047c2cbc0abc34d2549dd27754e4d3d05af78
    frozen scientific canon
```

Because `d5d88c2...` is a parentless root, GitHub correctly reports no common ancestor between the publication-history lineage and frozen canon `ed3047c2...`. This is Git-history discontinuity, not evidence that the scientific corpus is unrelated.

## Exact representative content continuity

Exact Git blob identities establish byte-for-byte continuity across the re-root boundary for representative theorem-bearing files spanning spine and branch material:

```text
NFC_Book_I.tex
  d5d88c2... blob = 12c4fd2fbaf0f0aa34a20756810fe467afb85368
  0f23c285... blob = 12c4fd2fbaf0f0aa34a20756810fe467afb85368

NFC_Book_II.tex
  d5d88c2... blob = 97493131943f5462726a484461d3cceb930fb214
  0f23c285... blob = 97493131943f5462726a484461d3cceb930fb214

NFC_NS_Branch.tex
  d5d88c2... blob = 81892c764f6f8b15eea2aa01a708037b229638c0
  0f23c285... blob = 81892c764f6f8b15eea2aa01a708037b229638c0
```

This proves representative content continuity. It is not presented as a complete historical file-by-file manifest comparison.

## Human intent is not reconstructed from Git mechanics

The repository establishes what happened mechanically. It does not contain sufficient explicit evidence to establish the human policy reason for the July 8 `remove` operation.

Accordingly:

```text
MECHANICAL_PROVENANCE_SEQUENCE = ESTABLISHED
REPRESENTATIVE_CONTENT_CONTINUITY = ESTABLISHED
HUMAN_POLICY_INTENT = UNRESOLVED
```

The publication-facing nature of `main` is the repository's current routing policy; it should not be retroactively treated as proof of the original motive for the historical split.

## Release-anchor status

The frozen canon release metadata declares:

```text
DECLARED_TAG = v1.0-canon-rewrite
DECLARED_COMMIT = 716e6fae585251185ffd15775dd923132f16c88e
```

That declared tag has now been restored exactly:

```text
refs/tags/v1.0-canon-rewrite
    -> 716e6fae585251185ffd15775dd923132f16c88e
```

The historical release pointer is therefore reconciled at the repository provenance/routing scope.

A redundant reachability branch remains:

```text
anchor/v1.0-canon-rewrite-716e6fa
    -> 716e6fae585251185ffd15775dd923132f16c88e
```

The frozen canon itself was not modified by this repair.

## Current source-selection guidance

Use the following identities for different purposes:

| Purpose | Repository source |
|---|---|
| Frozen theorem-bearing NFC canon | `archive/nfc-canonical-ed3047c2@ed3047c2cbc0abc34d2549dd27754e4d3d05af78` |
| Frozen canon tag | `nfc-canonical-ed3047c2 -> ed3047c2cbc0abc34d2549dd27754e4d3d05af78` |
| Exact frozen canon tree | `00ef55ff36d5e9663ca1ef2c9566e2bc1396f973` |
| Publication / citation landing surface | `main` |
| Historical v1 canon-rewrite release | `v1.0-canon-rewrite -> 716e6fae585251185ffd15775dd923132f16c88e` |
| Redundant frozen-canon reachability ref | `anchor/frozen-canon-ed3047c2` |
| Redundant v1-release reachability ref | `anchor/v1.0-canon-rewrite-716e6fa` |

Do not use default-branch presence as a proxy for scientific authority.

## Provenance-hardening closure

The provenance/routing repair is complete at its audited scope:

```text
H1_DURABLE_CANONICAL_ANCHOR = COMPLETE_AT_ROUTING_SCOPE
H2_V1_RELEASE_ANCHOR_RECONCILIATION = COMPLETE
H3_DEFAULT_MAIN_ROUTING = COMPLETE
H4_REPOSITORY_NATIVE_PROVENANCE_CROSSWALK = COMPLETE

FROZEN_CANON_COMMIT_UNCHANGED = YES
FROZEN_CANON_TREE_UNCHANGED = YES
THEOREM_CONTENT_CHANGED = NO
SCIENTIFIC_STATUS_CHANGED = NO
```

Optional future administration may protect the canonical tag/branch from deletion or force-update. Such protection changes repository enforcement only and must preserve the exact identities above.