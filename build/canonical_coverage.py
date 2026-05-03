"""
build/canonical_coverage.py — v33 Canonical Coverage Manifest

For GR and YM (the two most migration-mature branches), cross-reference
generated machine IDs against the canonical theorem lists from the
branch books. Produces a coverage manifest showing:
  - Which canonical theorems have corresponding generated machine IDs
  - Which generated claims have no canonical source reference
  - Coverage percentage
  - Prose stub completeness (non-empty body_file content)
  - Scope completeness (required scope fields populated)
  - Discharge mode completeness

This is the primary L3 hardening check: a branch is L3-ready when
its coverage manifest shows high canonical coverage, full prose stubs,
and complete scope and discharge records.

Output:
  output/reports/canonical_coverage_gr.json
  output/reports/canonical_coverage_ym.json
  output/tables/canonical_coverage.md
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

# Canonical theorem reference lists derived from reading the branch books.
# These are the NAMED theorem-like objects that should be represented
# in a complete L3 migration.

GR_CANONICAL_REFS = [
    {"canonical_id": "thm:GR.realization",   "canonical_label": "GR Realization Theorem",          "canonical_number": "GR.1"},
    {"canonical_id": "thm:GR.deformation",   "canonical_label": "GR Deformation Theorem",          "canonical_number": "GR.2"},
    {"canonical_id": "thm:GR.compat",        "canonical_label": "GR Compatibility Theorem",         "canonical_number": "GR.3"},
    {"canonical_id": "thm:GR.domain",        "canonical_label": "Domain-Bounded Gravity Closure",   "canonical_number": "GR.9.1"},
    {"canonical_id": "thm:GR.CP.1",          "canonical_label": "GR Realization+Coherence Packet", "canonical_number": "GR.CP.1"},
    {"canonical_id": "ob:GR.real",           "canonical_label": "GR Realization Obligation",        "canonical_number": "ob:GR.real"},
    {"canonical_id": "ob:GR.deform",         "canonical_label": "GR Deformation Obligation",        "canonical_number": "ob:GR.deform"},
    {"canonical_id": "ob:GR.compat",         "canonical_label": "GR Compatibility Obligation",      "canonical_number": "ob:GR.compat"},
    {"canonical_id": "ob:GR.closure",        "canonical_label": "GR Closure Obligation",            "canonical_number": "ob:GR.closure"},
    {"canonical_id": "ob:GR.EFE1",          "canonical_label": "EFE Structural Compatibility 1",   "canonical_number": "ob:GR.EFE1"},
    {"canonical_id": "ob:GR.EFE2",          "canonical_label": "EFE Structural Compatibility 2",   "canonical_number": "ob:GR.EFE2"},
    {"canonical_id": "ob:GR.EFE3",          "canonical_label": "EFE Structural Compatibility 3",   "canonical_number": "ob:GR.EFE3"},
    {"canonical_id": "ob:GR.global-subcriticality", "canonical_label": "Global Curvature-Subcriticality Frontier", "canonical_number": "ob:GR.BF9"},
    {"canonical_id": "status:GR",            "canonical_label": "GR Branch Status",                "canonical_number": "status:GR"},
]

YM_CANONICAL_REFS = [
    {"canonical_id": "thm:YM.ID",           "canonical_label": "YM Identity/Sourcing",             "canonical_number": "YM.ID"},
    {"canonical_id": "thm:YM.RIG",          "canonical_label": "YM Rigidity",                      "canonical_number": "YM.RIG"},
    {"canonical_id": "thm:YM.ENC",          "canonical_label": "YM Weyl Encoding",                 "canonical_number": "YM.ENC"},
    {"canonical_id": "thm:YM.GLOB",         "canonical_label": "YM Globalization",                 "canonical_number": "YM.GLOB"},
    {"canonical_id": "thm:YM.CLU",          "canonical_label": "YM Clustering",                    "canonical_number": "YM.CLU"},
    {"canonical_id": "thm:YM.7",            "canonical_label": "YM Endpoint (Mass-Gap+OS/Wightman)","canonical_number": "YM.7"},
    {"canonical_id": "thm:YM.B1.bridge",    "canonical_label": "YM B1 Post-Program Bridge",        "canonical_number": "YM.B1"},
    {"canonical_id": "thm:YM.B2.bridge",    "canonical_label": "YM B2 Post-Program Bridge",        "canonical_number": "YM.B2"},
    {"canonical_id": "thm:YM.B3.bridge",    "canonical_label": "YM B3 Post-Program Bridge",        "canonical_number": "YM.B3"},
    {"canonical_id": "ob:YM.O-ID",          "canonical_label": "YM Identity Obligation",           "canonical_number": "ob:YM.O-ID"},
    {"canonical_id": "ob:YM.O-RIG",         "canonical_label": "YM Rigidity Obligation",           "canonical_number": "ob:YM.O-RIG"},
    {"canonical_id": "ob:YM.O-ENC",         "canonical_label": "YM Encoding Obligation",           "canonical_number": "ob:YM.O-ENC"},
    {"canonical_id": "ob:YM.O-GLOB",        "canonical_label": "YM Globalization Obligation",      "canonical_number": "ob:YM.O-GLOB"},
    {"canonical_id": "ob:YM.O-CLU",         "canonical_label": "YM Clustering Obligation",         "canonical_number": "ob:YM.O-CLU"},
    {"canonical_id": "ob:YM.B1",            "canonical_label": "YM B1 Post-Program Obligation",    "canonical_number": "ob:YM.B1"},
    {"canonical_id": "ob:YM.B2",            "canonical_label": "YM B2 Post-Program Obligation",    "canonical_number": "ob:YM.B2"},
    {"canonical_id": "ob:YM.B3",            "canonical_label": "YM B3 Post-Program Obligation",    "canonical_number": "ob:YM.B3"},
    {"canonical_id": "ob:YM.B3.A2",         "canonical_label": "YM B3-A2 Residual Frontier",      "canonical_number": "ob:YM.B3.A2"},
    {"canonical_id": "status:YM",           "canonical_label": "YM Branch Status",                 "canonical_number": "status:YM"},
]

REQUIRED_SCOPE_FIELDS = ["regime", "domain", "certificate_scope", "promotion_ceiling"]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_branch_claims(branch: str) -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    branch_dir = ROOT / "claims" / "branches" / branch
    if not branch_dir.exists():
        return claims
    for path in sorted(branch_dir.glob("*.yaml")):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            claims[cid] = data
    return claims


def check_prose_stub(claim: Dict[str, Any]) -> Dict[str, Any]:
    """Check whether a claim has non-trivial prose stubs."""
    body_path = claim.get("body_file")
    proof_path = claim.get("proof_file")
    kind = claim.get("kind", "")

    body_ok = False
    body_length = 0
    if body_path:
        p = ROOT / body_path
        if p.exists():
            content = p.read_text(encoding="utf-8").strip()
            body_length = len(content)
            body_ok = body_length >= 50  # non-trivial stub

    proof_ok = False
    proof_length = 0
    if proof_path and kind not in ("obligation", "frontier", "status_note"):
        p = ROOT / proof_path
        if p.exists():
            content = p.read_text(encoding="utf-8").strip()
            proof_length = len(content)
            proof_ok = proof_length >= 30
    elif kind in ("obligation", "frontier", "status_note"):
        proof_ok = True  # not required for these kinds

    return {
        "body_present": bool(body_path),
        "body_non_trivial": body_ok,
        "body_length": body_length,
        "proof_present": bool(proof_path),
        "proof_non_trivial": proof_ok,
        "proof_length": proof_length,
    }


def check_scope_completeness(claim: Dict[str, Any]) -> Dict[str, Any]:
    """Check whether scope fields are fully populated."""
    scope = claim.get("scope", {}) or {}
    missing = [f for f in REQUIRED_SCOPE_FIELDS if not scope.get(f)]
    return {
        "complete": not missing,
        "missing_fields": missing,
        "present_fields": [f for f in REQUIRED_SCOPE_FIELDS if scope.get(f)],
    }


def check_discharge_completeness(claim: Dict[str, Any]) -> Dict[str, Any]:
    """Check whether discharge edges are fully specified."""
    discharges = claim.get("discharges", []) or []
    if not discharges:
        return {"has_discharges": False, "all_typed": True, "issues": []}

    issues = []
    for d in discharges:
        if not d.get("kind"):
            issues.append(f"discharge to {d.get('target','?')} has no kind")
        if not d.get("basis"):
            issues.append(f"discharge to {d.get('target','?')} has no basis")
        if not d.get("scope_relation"):
            issues.append(f"discharge to {d.get('target','?')} has no scope_relation")

    return {
        "has_discharges": True,
        "all_typed": not issues,
        "issues": issues,
    }


def generate_coverage_manifest(
    branch: str,
    canonical_refs: List[Dict[str, Any]],
    claims: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Generate a coverage manifest for one branch."""
    canonical_ids = {ref["canonical_id"] for ref in canonical_refs}
    generated_ids = set(claims.keys())

    # Coverage: which canonical IDs are in the generated set
    covered = sorted(canonical_ids & generated_ids)
    missing = sorted(canonical_ids - generated_ids)
    extra = sorted(generated_ids - canonical_ids)

    coverage_pct = round(100 * len(covered) / len(canonical_ids), 1) if canonical_ids else 0.0

    # Per-claim quality checks
    claim_quality: List[Dict[str, Any]] = []
    prose_issues = []
    scope_issues = []
    discharge_issues = []

    for cid in sorted(generated_ids):
        claim = claims[cid]
        prose = check_prose_stub(claim)
        scope = check_scope_completeness(claim)
        discharge = check_discharge_completeness(claim)

        quality_entry = {
            "id": cid,
            "kind": claim.get("kind", ""),
            "status": claim.get("declared_status", ""),
            "prose": prose,
            "scope": scope,
            "discharge": discharge,
        }
        claim_quality.append(quality_entry)

        if not prose["body_non_trivial"]:
            prose_issues.append(f"{cid}: body stub too short ({prose['body_length']} chars)")
        if not scope["complete"]:
            scope_issues.append(f"{cid}: missing scope fields: {scope['missing_fields']}")
        if not discharge["all_typed"]:
            discharge_issues.extend([f"{cid}: {iss}" for iss in discharge["issues"]])

    # Compute L3 readiness score
    prose_score = round(
        100 * sum(1 for q in claim_quality if q["prose"]["body_non_trivial"]) / len(claim_quality), 1
    ) if claim_quality else 0.0
    scope_score = round(
        100 * sum(1 for q in claim_quality if q["scope"]["complete"]) / len(claim_quality), 1
    ) if claim_quality else 0.0
    discharge_score = round(
        100 * sum(1 for q in claim_quality if q["discharge"]["all_typed"]) / len(claim_quality), 1
    ) if claim_quality else 0.0

    l3_ready = (
        coverage_pct >= 90
        and prose_score >= 80
        and scope_score >= 80
        and discharge_score >= 90
        and not missing
    )

    return {
        "branch": branch,
        "canonical_ref_count": len(canonical_ids),
        "generated_claim_count": len(generated_ids),
        "covered_count": len(covered),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "coverage_pct": coverage_pct,
        "prose_score": prose_score,
        "scope_score": scope_score,
        "discharge_score": discharge_score,
        "l3_ready": l3_ready,
        "covered": covered,
        "missing": missing,
        "extra": extra,
        "prose_issues": prose_issues,
        "scope_issues": scope_issues,
        "discharge_issues": discharge_issues,
        "claim_quality": claim_quality,
        "l3_gaps": (
            ([f"Coverage {coverage_pct}% < 90%"] if coverage_pct < 90 else [])
            + ([f"Prose score {prose_score}% < 80%"] if prose_score < 80 else [])
            + ([f"Scope score {scope_score}% < 80%"] if scope_score < 80 else [])
            + ([f"Discharge score {discharge_score}% < 90%"] if discharge_score < 90 else [])
            + ([f"Missing canonical items: {missing}"] if missing else [])
        ),
    }


def render_manifest_md(manifest: Dict[str, Any]) -> List[str]:
    branch = manifest["branch"]
    lines = [
        f"## {branch} Canonical Coverage Manifest",
        "",
        f"| Metric | Value |",
        "|--------|-------|",
        f"| Canonical refs | {manifest['canonical_ref_count']} |",
        f"| Generated claims | {manifest['generated_claim_count']} |",
        f"| Covered | {manifest['covered_count']} ({manifest['coverage_pct']}%) |",
        f"| Missing | {manifest['missing_count']} |",
        f"| Extra | {manifest['extra_count']} |",
        f"| Prose score | {manifest['prose_score']}% |",
        f"| Scope score | {manifest['scope_score']}% |",
        f"| Discharge score | {manifest['discharge_score']}% |",
        f"| **L3 ready** | {'✅ YES' if manifest['l3_ready'] else '❌ NO'} |",
        "",
    ]
    if manifest["missing"]:
        lines.append("**Missing from generated set:**")
        for m in manifest["missing"]:
            lines.append(f"- `{m}`")
        lines.append("")
    if manifest["l3_gaps"]:
        lines.append("**L3 gaps to address:**")
        for gap in manifest["l3_gaps"]:
            lines.append(f"- {gap}")
        lines.append("")
    if manifest["prose_issues"]:
        lines.append(f"**Prose issues ({len(manifest['prose_issues'])}):**")
        for iss in manifest["prose_issues"][:10]:
            lines.append(f"- {iss}")
        if len(manifest["prose_issues"]) > 10:
            lines.append(f"- _(and {len(manifest['prose_issues'])-10} more)_")
        lines.append("")
    if manifest["scope_issues"]:
        lines.append(f"**Scope completeness issues ({len(manifest['scope_issues'])}):**")
        for iss in manifest["scope_issues"][:10]:
            lines.append(f"- {iss}")
        lines.append("")
    return lines


def main() -> int:
    gr_claims = load_branch_claims("GR")
    ym_claims = load_branch_claims("YM")

    gr_manifest = generate_coverage_manifest("GR", GR_CANONICAL_REFS, gr_claims)
    ym_manifest = generate_coverage_manifest("YM", YM_CANONICAL_REFS, ym_claims)

    # Write per-branch JSONs (without large claim_quality array for readability)
    for manifest, name in [(gr_manifest, "gr"), (ym_manifest, "ym")]:
        slim = {k: v for k, v in manifest.items() if k != "claim_quality"}
        (REPORTS / f"canonical_coverage_{name}.json").write_text(
            json.dumps(slim, indent=2), encoding="utf-8"
        )

    # Write combined Markdown
    lines = [
        "# v33 Canonical Coverage Manifests",
        "",
        "Cross-reference of generated machine IDs against canonical theorem lists.",
        "Generated by `build/canonical_coverage.py`.",
        "",
    ]
    lines.extend(render_manifest_md(gr_manifest))
    lines.append("")
    lines.extend(render_manifest_md(ym_manifest))

    (TABLES / "canonical_coverage.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    result = {
        "status": "passed",
        "GR": {
            "coverage_pct": gr_manifest["coverage_pct"],
            "prose_score": gr_manifest["prose_score"],
            "scope_score": gr_manifest["scope_score"],
            "discharge_score": gr_manifest["discharge_score"],
            "l3_ready": gr_manifest["l3_ready"],
            "l3_gaps": gr_manifest["l3_gaps"],
        },
        "YM": {
            "coverage_pct": ym_manifest["coverage_pct"],
            "prose_score": ym_manifest["prose_score"],
            "scope_score": ym_manifest["scope_score"],
            "discharge_score": ym_manifest["discharge_score"],
            "l3_ready": ym_manifest["l3_ready"],
            "l3_gaps": ym_manifest["l3_gaps"],
        },
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
