
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims"
CANON_DIR = ROOT / "canon"
OUTPUT_DIR = ROOT / "output" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCHEMA_VERSION = "0.41.0"
SEVERITY_LEVELS = {"error", "warning", "info"}

REQUIRED_FIELDS = ("id", "declared_status", "scope")
THEOREMISH = {"theorem", "proposition", "corollary", "bridge", "obligation", "frontier"}
STATUSISH = {"status_note"}

def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def all_claim_paths() -> List[Path]:
    return sorted(CLAIMS_DIR.rglob("*.yaml"))

def load_claims() -> Dict[str, Dict[str, Any]]:
    claims = {}
    for path in all_claim_paths():
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            data["_path"] = str(path.relative_to(ROOT))
            claims[cid] = data
    return claims

def load_retired_aliases() -> Dict[str, str]:
    aliases = load_yaml(CANON_DIR / "aliases.yaml").get("aliases", [])
    retired = {}
    for entry in aliases:
        canonical = entry["canonical_id"]
        for name in entry.get("retired_labels", []):
            retired[name] = canonical
    return retired

def load_status_facts() -> Dict[str, Dict[str, Any]]:
    facts = load_yaml(CANON_DIR / "status_facts.yaml").get("status_facts", [])
    return {fact["target"]: fact for fact in facts}

def load_schema_version() -> Dict[str, Any]:
    path = CANON_DIR / "schema_version.yaml"
    return load_yaml(path).get("schema", {}) if path.exists() else {}

def load_claim_schema() -> Dict[str, Any]:
    path = CANON_DIR / "claim_schema.yaml"
    return load_yaml(path).get("claim_schema", {}) if path.exists() else {}

def load_allowed_statuses() -> tuple[set[str], set[str]]:
    statuses_raw = load_yaml(CANON_DIR / "statuses.yaml").get("claim_statuses", {})
    claim_statuses = set(statuses_raw.keys())
    postures_raw = load_yaml(CANON_DIR / "branch_postures.yaml").get("branch_postures", {})
    branch_postures = set(postures_raw.keys())
    return claim_statuses, branch_postures


def load_release_postures() -> Dict[str, str]:
    release = load_yaml(CANON_DIR / "releases" / "L_plus_4.yaml")
    return release.get("effective_branch_postures", {})


def schema_version_audit(schema_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues = []
    found = schema_info.get("version")
    if not found:
        issues.append({
            "severity": "error",
            "type": "schema-version-missing",
            "id": "canon:schema",
            "reason": "canon/schema_version.yaml is missing or does not define schema.version.",
        })
    elif str(found) != SCHEMA_VERSION:
        issues.append({
            "severity": "warning",
            "type": "schema-version-drift",
            "id": "canon:schema",
            "declared_version": found,
            "expected_version": SCHEMA_VERSION,
            "reason": "Schema version differs from validator target.",
        })
    return issues

def schema_shape_audit(
    claims: Dict[str, Dict[str, Any]],
    claim_schema: Dict[str, Any],
    claim_statuses: set[str],
    branch_postures: set[str],
) -> List[Dict[str, Any]]:
    """Strict-enough v9 schema checks. These catch malformed governance data before graph inference."""
    issues: List[Dict[str, Any]] = []
    allowed_kinds = set(claim_schema.get("allowed_kinds", [])) or (THEOREMISH | STATUSISH | {"definition", "standing_rule", "remark"})
    required_all = claim_schema.get("required_all", ["id", "book", "track", "kind", "title", "scope"])
    scope_required = claim_schema.get("scope_required", ["regime", "domain", "certificate_scope"])
    dep_sections = set(claim_schema.get("dependency_sections", ["requires", "optional", "excludes"]))
    discharge_required = claim_schema.get("discharge_required", ["target", "kind", "basis", "scope_relation"])
    discharge_kinds = set(claim_schema.get("discharge_kinds", ["full", "partial", "scoped", "superseding"]))
    scope_relations = set(claim_schema.get("scope_relations", ["preserved", "restricted", "widened"]))

    seen_ids = set()
    for cid, claim in claims.items():
        path = claim.get("_path")
        # Duplicate IDs are overwritten during load; load_claims records duplicates separately in v10. Guard basic self-consistency here.
        if claim.get("id") != cid:
            issues.append({"severity": "error", "type": "schema-id-mismatch", "id": cid, "path": path})

        missing = [field for field in required_all if field not in claim]
        if missing:
            issues.append({
                "severity": "error",
                "type": "schema-missing-core-field",
                "id": cid,
                "path": path,
                "missing": missing,
            })

        kind = claim.get("kind")
        if kind not in allowed_kinds:
            issues.append({
                "severity": "error",
                "type": "schema-invalid-kind",
                "id": cid,
                "path": path,
                "kind": kind,
                "allowed": sorted(allowed_kinds),
            })

        declared = claim.get("declared_status")
        if kind == "status_note":
            if declared not in branch_postures:
                issues.append({
                    "severity": "error",
                    "type": "schema-invalid-branch-posture",
                    "id": cid,
                    "path": path,
                    "declared_status": declared,
                    "allowed": sorted(branch_postures),
                })
        elif kind in THEOREMISH or kind in {"definition", "standing_rule", "remark"}:
            if declared not in claim_statuses:
                issues.append({
                    "severity": "error",
                    "type": "schema-invalid-claim-status",
                    "id": cid,
                    "path": path,
                    "declared_status": declared,
                    "allowed": sorted(claim_statuses),
                })

        scope = claim.get("scope")
        if not isinstance(scope, dict):
            issues.append({
                "severity": "error",
                "type": "schema-invalid-scope",
                "id": cid,
                "path": path,
                "reason": "scope must be a mapping.",
            })
        else:
            missing_scope = [field for field in scope_required if field not in scope]
            if missing_scope:
                issues.append({
                    "severity": "error",
                    "type": "schema-missing-scope-field",
                    "id": cid,
                    "path": path,
                    "missing": missing_scope,
                })

        deps = claim.get("dependencies", {"requires": [], "optional": [], "excludes": []})
        if not isinstance(deps, dict):
            issues.append({
                "severity": "error",
                "type": "schema-invalid-dependencies",
                "id": cid,
                "path": path,
                "reason": "dependencies must be a mapping with requires/optional/excludes lists.",
            })
        else:
            for section, values in deps.items():
                if section not in dep_sections:
                    issues.append({
                        "severity": "warning",
                        "type": "schema-unknown-dependency-section",
                        "id": cid,
                        "path": path,
                        "section": section,
                    })
                if not isinstance(values, list):
                    issues.append({
                        "severity": "error",
                        "type": "schema-invalid-dependency-list",
                        "id": cid,
                        "path": path,
                        "section": section,
                    })

        discharges = claim.get("discharges", [])
        if not isinstance(discharges, list):
            issues.append({
                "severity": "error",
                "type": "schema-invalid-discharges",
                "id": cid,
                "path": path,
                "reason": "discharges must be a list.",
            })
        else:
            for idx, discharge in enumerate(discharges):
                if not isinstance(discharge, dict):
                    issues.append({
                        "severity": "error",
                        "type": "schema-invalid-discharge-record",
                        "id": cid,
                        "path": path,
                        "index": idx,
                    })
                    continue
                missing_discharge = [field for field in discharge_required if field not in discharge]
                if missing_discharge:
                    issues.append({
                        "severity": "error",
                        "type": "schema-missing-discharge-field",
                        "id": cid,
                        "path": path,
                        "index": idx,
                        "missing": missing_discharge,
                    })
                if discharge.get("kind") and discharge.get("kind") not in discharge_kinds:
                    issues.append({
                        "severity": "error",
                        "type": "schema-invalid-discharge-kind",
                        "id": cid,
                        "path": path,
                        "kind": discharge.get("kind"),
                        "allowed": sorted(discharge_kinds),
                    })
                if discharge.get("scope_relation") and discharge.get("scope_relation") not in scope_relations:
                    issues.append({
                        "severity": "error",
                        "type": "schema-invalid-scope-relation",
                        "id": cid,
                        "path": path,
                        "scope_relation": discharge.get("scope_relation"),
                        "allowed": sorted(scope_relations),
                    })
                if "basis" in discharge and not isinstance(discharge.get("basis"), list):
                    issues.append({
                        "severity": "error",
                        "type": "schema-invalid-discharge-basis",
                        "id": cid,
                        "path": path,
                        "index": idx,
                    })
    return issues

def required_field_audit(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for claim in claims.values():
        if claim.get("kind") in THEOREMISH | STATUSISH:
            missing = [f for f in REQUIRED_FIELDS if f not in claim]
            if missing:
                issues.append({
                    "severity": "error",
                    "type": "missing-fields",
                    "id": claim.get("id"),
                    "path": claim.get("_path"),
                    "missing": missing,
                })
    return issues

def dependency_audit(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for claim in claims.values():
        deps = claim.get("dependencies", {}).get("requires", [])
        for dep in deps:
            if dep not in claims:
                issues.append({
                    "severity": "error",
                    "type": "unresolved-dependency",
                    "id": claim["id"],
                    "path": claim["_path"],
                    "dependency": dep,
                })
    return issues

def retired_alias_audit(claims: Dict[str, Dict[str, Any]], retired_aliases: Dict[str, str]) -> List[Dict[str, Any]]:
    issues = []
    for claim in claims.values():
        active_aliases = claim.get("aliases", [])
        for alias in active_aliases:
            if alias in retired_aliases:
                issues.append({
                    "severity": "warning",
                    "type": "retired-alias-detected",
                    "id": claim["id"],
                    "path": claim["_path"],
                    "alias": alias,
                    "canonical_target": retired_aliases[alias],
                })
    return issues

def promotion_audit(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for claim in claims.values():
        if claim.get("declared_status") == "U":
            deps = claim.get("dependencies", {}).get("requires", [])
            conditional_deps = [dep for dep in deps if claims.get(dep, {}).get("declared_status") == "C"]
            if conditional_deps:
                issues.append({
                    "severity": "error",
                    "type": "illegal-promotion",
                    "id": claim["id"],
                    "path": claim["_path"],
                    "conditional_dependencies": conditional_deps,
                })
    return issues

def discharge_audit(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for claim in claims.values():
        for discharge in claim.get("discharges", []):
            target = discharge.get("target")
            if target and target not in claims:
                issues.append({
                    "severity": "error",
                    "type": "discharge-target-missing",
                    "id": claim["id"],
                    "path": claim["_path"],
                    "target": target,
                })
    return issues

def status_fact_basis_audit(claims: Dict[str, Dict[str, Any]], facts: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for target, fact in facts.items():
        for basis in fact.get("basis", []):
            if basis not in claims:
                issues.append({
                    "severity": "error",
                    "type": "status-fact-basis-missing",
                    "target": target,
                    "basis": basis,
                })
    return issues

def compute_effective_statuses(claims: Dict[str, Dict[str, Any]], facts: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, str], Dict[str, Dict[str, Any]]]:
    effective = {}
    reasons = {}

    # Start from declared status
    for cid, claim in claims.items():
        effective[cid] = claim.get("declared_status")
        reasons[cid] = {
            "effective_status": effective[cid],
            "source": "declared",
            "reason": "No stronger inference applied.",
            "basis": [],
            "trace_steps": ["Declared status/posture used as the initial effective value."],
        }

    # Apply explicit facts for still-manual targets
    for cid, fact in facts.items():
        if cid in claims:
            effective[cid] = fact["effective_status"]
            reasons[cid] = {
                "effective_status": fact["effective_status"],
                "source": "status_facts",
                "reason": fact.get("reason", ""),
                "basis": fact.get("basis", []),
                "trace_steps": [
                    "Manual override/status fact applied.",
                    fact.get("reason", ""),
                ],
            }

    # Infer discharged obligations from local discharge edges
    for oid, claim in claims.items():
        if claim.get("kind") != "obligation":
            continue
        dischargers = []
        for src_id, src in claims.items():
            for discharge in src.get("discharges", []):
                if discharge.get("target") == oid and src.get("audit", {}).get("active", True):
                    dischargers.append((src_id, src))
        if dischargers:
            closing_dischargers = []
            partial_dischargers = []
            for src_id, src in dischargers:
                matching_edges = [d for d in src.get("discharges", []) if d.get("target") == oid]
                if any(edge.get("kind") == "partial" for edge in matching_edges):
                    partial_dischargers.append((src_id, src))
                if any(edge.get("kind") in {"full", "scoped", "superseding"} for edge in matching_edges):
                    closing_dischargers.append((src_id, src))

            if closing_dischargers:
                basis_ids = [cid for cid, _ in closing_dischargers]
                basis_statuses = [effective.get(cid, src.get("declared_status")) for cid, src in closing_dischargers]
                inferred = "U" if basis_statuses and all(s == "U" for s in basis_statuses) else "C"
                effective[oid] = inferred
                reasons[oid] = {
                    "effective_status": inferred,
                    "source": "local-discharge-inference",
                    "reason": f"Locally inferred from explicit closing discharge edges by {', '.join(basis_ids)}.",
                    "basis": basis_ids,
                    "trace_steps": [
                        "Located explicit closing discharge edge(s).",
                        "Accepted discharge kinds: full, scoped, superseding.",
                        f"Basis claim(s): {', '.join(basis_ids)}.",
                        f"Inferred obligation status: {inferred}.",
                    ],
                }
            elif partial_dischargers:
                basis_ids = [cid for cid, _ in partial_dischargers]
                reasons[oid]["trace_steps"].extend([
                    "Located partial discharge edge(s).",
                    f"Partial basis claim(s): {', '.join(basis_ids)}.",
                    "Partial discharge is recorded but does not close the obligation.",
                ])
                reasons[oid]["reason"] = "Partial discharge recorded; effective status remains declared unless a closing edge exists."

    # Infer selected branch postures from local branch packets
    def is_status(cid: str, expected: str) -> bool:
        return effective.get(cid) == expected

    def in_status(cid: str, allowed: set[str]) -> bool:
        return effective.get(cid) in allowed

    posture_rules = {
        "status:GR": (
            in_status("thm:GR.domain", {"C", "U"}) and is_status("ob:GR.global-subcriticality", "O"),
            "domain-bounded-cert-close",
            ["thm:GR.domain", "ob:GR.global-subcriticality"],
            "Local GR pilot packet supports domain-bounded closure while global curvature-subcriticality / BF-9 remains open."
        ),
        "status:YM": (
            in_status("thm:YM.7", {"C", "U"})
            and in_status("thm:YM.B1.bridge", {"C", "U"})
            and in_status("thm:YM.B2.bridge", {"C", "U"})
            and in_status("thm:YM.B3.bridge", {"C", "U"})
            and is_status("ob:YM.B3.A2", "O"),
            "conditional-cert-close",
            ["thm:YM.7", "thm:YM.B1.bridge", "thm:YM.B2.bridge", "thm:YM.B3.bridge", "ob:YM.B3.A2"],
            "Local YM pilot packet supports conditional closure through B1/B2/B3 bridge packets while B3-A2 remains the surviving residual frontier."
        ),
        "status:SM": (
            in_status("thm:SM.18.1", {"C", "U"}) and is_status("ob:SM.O-IDcont", "O"),
            "intrinsic-structural-close",
            ["thm:SM.18.1", "ob:SM.O-IDcont"],
            "Local SM packet supports intrinsic-structural closure while O-IDcont blocks unconditional force-upgrade."
        ),
        "status:NS": (
            in_status("thm:NS.7.1", {"C", "U"}) and in_status("thm:NS.6.1", {"C", "U"}) and is_status("front:NS.main", "O"),
            "domain-bounded-cert-close",
            ["thm:NS.7.1", "thm:NS.6.1", "front:NS.main"],
            "NS reaches domain-bounded conditional CERT-CLOSE via NS.6.1+NS.7.1 chain; Stage-3 global frontier remains active."
        ),
        "status:SPEC": (
            is_status("thm:SPEC.10.1", "U"),
            "cert-close",
            ["thm:SPEC.10.1"],
            "SPEC is inferred closed from a locally unconditional endpoint packet."
        ),
        "status:SCC": (
            in_status("thm:SCC.MCS", {"C", "U"}) and in_status("thm:SCC.UC", {"C", "U"}) and in_status("thm:SCC.TSI", {"C", "U"}),
            "conditional-cert-close",
            ["thm:SCC.MCS", "thm:SCC.UC", "thm:SCC.TSI"],
            "Local SCC packet supports conditional closure once MCS, UC, and TSI packets are present."
        ),
        "status:BIO": (
            in_status("thm:BIO.END", {"C", "U"}),
            "conditional-cert-close",
            ["thm:BIO.END"],
            "BIO posture is inferred from the nondegenerate endpoint packet."
        ),
        "status:LING": (
            in_status("thm:LING.END", {"C", "U"}) and is_status("ob:LING.REF-INVIS-RECOV", "O"),
            "conditional-cert-close",
            ["thm:LING.END", "ob:LING.REF-INVIS-RECOV"],
            "LING posture is inferred from endpoint closure plus the retained reference frontier."
        ),
        "status:CRYST": (
            in_status("thm:CRYST.END", {"C", "U"}) and is_status("ob:CRYST.phase-problem", "O"),
            "conditional-cert-close",
            ["thm:CRYST.END", "ob:CRYST.phase-problem"],
            "CRYST posture is inferred from endpoint closure plus the retained phase frontier."
        ),
                "status:RH": (
            in_status("thm:RH.3", {"C","U"}) and is_status("ob:RH.S1-ARC", "O"),
            "cert-proj",
            ["thm:RH.3", "ob:RH.S1-ARC"],
            "RH posture is cert-proj: RH1-RH3 constituted, S1-ARC irreducibly open."
        ),
    }
    for cid, (cond, posture, basis, reason) in posture_rules.items():
        if cid in claims and cond:
            effective[cid] = posture
            reasons[cid] = {
                "effective_status": posture,
                "source": "branch-packet-inference",
                "reason": reason,
                "basis": basis,
                "trace_steps": [
                    "Matched branch-packet inference rule.",
                    f"Basis item(s): {', '.join(basis)}.",
                    f"Computed branch posture: {posture}.",
                    reason,
                ],
            }

    return effective, reasons

def stale_status_audit(claims: Dict[str, Dict[str, Any]], effective: Dict[str, str], reasons: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    issues = []
    for cid, claim in claims.items():
        declared = claim.get("declared_status")
        inferred = effective.get(cid)
        if inferred is None:
            continue
        if declared != inferred:
            why = reasons.get(cid, {})
            issues.append({
                "severity": "warning",
                "type": "stale-label",
                "id": cid,
                "path": claim.get("_path"),
                "declared_status": declared,
                "effective_status": inferred,
                "reason": why.get("reason"),
                "basis": why.get("basis", []),
                "source": why.get("source"),
            })
    return issues

def branch_posture_audit(claims: Dict[str, Dict[str, Any]], release_postures: Dict[str, str], effective: Dict[str, str]) -> List[Dict[str, Any]]:
    issues = []
    for cid, claim in claims.items():
        if claim.get("kind") != "status_note" or not cid.startswith("status:"):
            continue
        branch = cid.split(":", 1)[1]
        declared = claim.get("declared_status")
        computed = effective.get(cid)
        release_value = release_postures.get(branch)
        if computed and declared != computed:
            issues.append({
                "severity": "warning",
                "type": "branch-posture-mismatch",
                "id": cid,
                "path": claim.get("_path"),
                "branch": branch,
                "declared_posture": declared,
                "computed_posture": computed,
            })
        if release_value and computed and computed != release_value:
            issues.append({
                "severity": "warning",
                "type": "release-vs-computed-posture-mismatch",
                "id": cid,
                "path": claim.get("_path"),
                "branch": branch,
                "computed_posture": computed,
                "release_posture": release_value,
            })
    return issues

def orphan_release_posture_audit(claims: Dict[str, Dict[str, Any]], release_postures: Dict[str, str]) -> List[Dict[str, Any]]:
    issues = []
    existing = set(claims)
    for branch, posture in release_postures.items():
        cid = f"status:{branch}"
        if cid not in existing:
            issues.append({
                "severity": "warning",
                "type": "release-posture-without-status-record",
                "branch": branch,
                "release_posture": posture,
            })
    return issues


def write_markdown_tables(claims: Dict[str, Dict[str, Any]], effective: Dict[str, str], reasons: Dict[str, Dict[str, Any]], issues: List[Dict[str, Any]]) -> None:
    """Emit lightweight human-readable tables for review in addition to JSON reports."""
    tables_dir = ROOT / "output" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    # Branch posture table
    rows = []
    for cid, claim in sorted(claims.items()):
        if claim.get("kind") == "status_note" and cid.startswith("status:"):
            branch = cid.split(":", 1)[1]
            rows.append([
                branch,
                claim.get("declared_status", ""),
                effective.get(cid, ""),
                reasons.get(cid, {}).get("source", ""),
                reasons.get(cid, {}).get("reason", ""),
            ])
    lines = ["# Branch Posture Reconciliation", "", "| Branch | Declared | Computed | Source | Reason |", "|---|---|---|---|---|"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |")
    (tables_dir / "branch_postures.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Active frontier / obligation table
    frontier_rows = []
    for cid, claim in sorted(claims.items()):
        if claim.get("kind") in {"obligation", "frontier"} and effective.get(cid) == "O":
            frontier_rows.append([
                cid,
                claim.get("book", ""),
                claim.get("title", ""),
                claim.get("scope", {}).get("certificate_scope", ""),
            ])
    lines = ["# Active Frontiers and Open Obligations", "", "| ID | Book | Title | Scope |", "|---|---|---|---|"]
    for row in frontier_rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |")
    (tables_dir / "active_frontiers.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Warning summary table
    warn_rows = [[i.get("type",""), i.get("id",""), i.get("severity",""), i.get("reason","")] for i in issues]
    lines = ["# Governance Audit Issues", "", "| Type | ID | Severity | Reason |", "|---|---|---|---|"]
    for row in warn_rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |")
    (tables_dir / "audit_issues.md").write_text("\n".join(lines) + "\n", encoding="utf-8")



def write_status_trace_tables(reasons: Dict[str, Dict[str, Any]]) -> None:
    tables_dir = ROOT / "output" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Why Status Trace", ""]
    for cid, info in sorted(reasons.items()):
        lines.append(f"## `{cid}`")
        lines.append("")
        lines.append(f"- **Effective status/posture:** `{info.get('effective_status', '')}`")
        lines.append(f"- **Source:** `{info.get('source', '')}`")
        basis = info.get("basis", [])
        if basis:
            lines.append("- **Basis:** " + ", ".join(f"`{b}`" for b in basis))
        else:
            lines.append("- **Basis:** _none_")
        steps = [step for step in info.get("trace_steps", []) if step]
        if steps:
            lines.append("- **Trace:**")
            for step in steps:
                lines.append(f"  - {step}")
        reason = info.get("reason")
        if reason and reason not in steps:
            lines.append(f"- **Reason:** {reason}")
        lines.append("")
    (tables_dir / "why_status.md").write_text("\n".join(lines), encoding="utf-8")

def write_warning_explanations(issues: List[Dict[str, Any]]) -> None:
    tables_dir = ROOT / "output" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for issue in issues:
        grouped.setdefault(issue.get("type", "unknown"), []).append(issue)

    explanations = {
        "branch-posture-mismatch": "The local branch posture record is stale relative to the computed branch-packet posture.",
        "retired-alias-detected": "A retired label appears in an active record. This is usually name-history drift rather than mathematical failure.",
        "stale-label": "The declared status/posture differs from the computed effective value.",
        "release-vs-computed-posture-mismatch": "The computed branch posture does not match the active release snapshot.",
        "schema-version-drift": "The schema file and validator target different schema versions.",
    }

    lines = ["# Current Warning Explanations", ""]
    if not grouped:
        lines.append("_No warnings or errors._")
    for issue_type, entries in sorted(grouped.items()):
        lines.append(f"## `{issue_type}`")
        lines.append("")
        lines.append(explanations.get(issue_type, "No specific explanation registered yet. Review the audit payload."))
        lines.append("")
        lines.append("| Severity | ID | Path | Detail |")
        lines.append("|---|---|---|---|")
        for issue in entries:
            if issue.get("severity") == "error":
                detail = issue.get("reason") or issue.get("dependency") or issue.get("target") or ""
            else:
                detail = issue.get("reason") or issue.get("alias") or issue.get("computed_posture") or issue.get("effective_status") or ""
            lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in [
                issue.get("severity", ""),
                issue.get("id", issue.get("target", "")),
                issue.get("path", ""),
                detail,
            ]) + " |")
        lines.append("")
    (tables_dir / "warning_explanations.md").write_text("\n".join(lines), encoding="utf-8")



def write_pilot_status_traces(reasons: Dict[str, Dict[str, Any]], effective: Dict[str, str]) -> None:
    """Emit focused GR/YM explainability traces for pilot review."""
    tables_dir = ROOT / "output" / "tables"
    reports_dir = ROOT / "output" / "reports"
    tables_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    pilots = {
        "GR": ["status:GR", "thm:GR.domain", "ob:GR.global-subcriticality", "ob:GR.EFE1", "ob:GR.EFE2", "ob:GR.EFE3"],
        "YM": ["status:YM", "thm:YM.7", "thm:YM.B1.bridge", "thm:YM.B2.bridge", "thm:YM.B3.bridge", "ob:YM.B3.A2"],
    }
    payload = {}
    lines = ["# Pilot Status Traces", ""]
    for branch, ids in pilots.items():
        lines.append(f"## {branch}")
        lines.append("")
        payload[branch] = []
        for cid in ids:
            info = reasons.get(cid, {})
            row = {
                "id": cid,
                "effective_status": effective.get(cid),
                "source": info.get("source"),
                "basis": info.get("basis", []),
                "reason": info.get("reason"),
                "trace_steps": info.get("trace_steps", []),
            }
            payload[branch].append(row)
            lines.append(f"### `{cid}`")
            lines.append(f"- **Effective:** `{row['effective_status']}`")
            lines.append(f"- **Source:** `{row['source']}`")
            if row["basis"]:
                lines.append("- **Basis:** " + ", ".join(f"`{b}`" for b in row["basis"]))
            else:
                lines.append("- **Basis:** _none_")
            if row["trace_steps"]:
                lines.append("- **Trace:**")
                for step in row["trace_steps"]:
                    lines.append(f"  - {step}")
            if row["reason"]:
                lines.append(f"- **Reason:** {row['reason']}")
            lines.append("")
    (tables_dir / "pilot_status_traces.md").write_text("\n".join(lines), encoding="utf-8")
    with (reports_dir / "pilot_status_traces.json").open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def summarize(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    errors = sum(1 for i in issues if i["severity"] == "error")
    warnings = sum(1 for i in issues if i["severity"] == "warning")
    return {
        "total_issues": len(issues),
        "errors": errors,
        "warnings": warnings,
    }

def main() -> None:
    claims = load_claims()
    retired_aliases = load_retired_aliases()
    facts = load_status_facts()
    release_postures = load_release_postures()
    schema_info = load_schema_version()
    claim_schema = load_claim_schema()
    claim_statuses, branch_postures = load_allowed_statuses()
    effective, reason_map = compute_effective_statuses(claims, facts)

    issues = []
    issues += schema_version_audit(schema_info)
    issues += schema_shape_audit(claims, claim_schema, claim_statuses, branch_postures)
    issues += required_field_audit(claims)
    issues += dependency_audit(claims)
    issues += retired_alias_audit(claims, retired_aliases)
    issues += promotion_audit(claims)
    issues += discharge_audit(claims)
    issues += status_fact_basis_audit(claims, facts)
    issues += stale_status_audit(claims, effective, reason_map)

    posture_issues = []
    posture_issues += branch_posture_audit(claims, release_postures, effective)
    posture_issues += orphan_release_posture_audit(claims, release_postures)
    issues += posture_issues

    audit_report = {
        "schema_version": SCHEMA_VERSION,
        "claims_count": len(claims),
        "issues": issues,
    }
    summary = summarize(issues)
    summary["schema_version"] = SCHEMA_VERSION
    summary["claims_count"] = len(claims)
    summary["computed_statuses"] = len(effective)

    with (OUTPUT_DIR / "audit_report.json").open("w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=2)
    with (OUTPUT_DIR / "audit_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (OUTPUT_DIR / "branch_posture_report.json").open("w", encoding="utf-8") as f:
        json.dump({"issues": posture_issues}, f, indent=2)
    with (OUTPUT_DIR / "computed_statuses.json").open("w", encoding="utf-8") as f:
        json.dump(reason_map, f, indent=2)

    write_markdown_tables(claims, effective, reason_map, issues)
    write_status_trace_tables(reason_map)
    write_pilot_status_traces(reason_map, effective)
    write_warning_explanations(issues)

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
