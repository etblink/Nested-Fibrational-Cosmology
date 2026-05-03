from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run supersession readiness.") from exc

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
PROJECT = ROOT / "project"
CANON = ROOT / "canon"


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def file_exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    policy = load_yaml(PROJECT / "supersession_policy.yaml").get("supersession_policy", {})
    audit_summary = load_json(REPORTS / "audit_summary.json")
    quality_gate = load_json(REPORTS / "quality_gate_report.json")
    regression = load_json(REPORTS / "regression_test_report.json")
    compile_check = load_json(REPORTS / "compile_check_report.json")
    import_manifest = load_json(REPORTS / "canon_import_manifest.json")
    release_diff = load_json(REPORTS / "release_diff_report.json")
    gr_pilot = load_json(REPORTS / "gr_pilot_report.json")
    ym_pilot = load_json(REPORTS / "ym_pilot_report.json")
    gr_successor = load_json(REPORTS / "gr_successor_equivalence_report.json")

    checks: List[Dict[str, Any]] = []

    def add_check(cid: str, label: str, status: str, evidence: Any, required_for: str) -> None:
        checks.append({
            "id": cid,
            "label": label,
            "status": status,
            "required_for": required_for,
            "evidence": evidence,
        })

    add_check(
        "sup.audit.zero-errors",
        "Governance audit has zero errors",
        "pass" if int(audit_summary.get("errors", 0) or 0) == 0 else "fail",
        {"errors": audit_summary.get("errors", 0), "warnings": audit_summary.get("warnings", 0)},
        "L1+",
    )
    add_check(
        "sup.import.packet",
        "Canon-import appendix packet exists",
        "pass" if file_exists("output/tex/canon_governance_appendix.tex") and file_exists("output/reports/canon_import_manifest.json") else "fail",
        import_manifest,
        "L1+",
    )
    add_check(
        "sup.compile.packet",
        "Standalone governance appendix compiles",
        "pass" if compile_check.get("status") == "passed" else "fail",
        {"status": compile_check.get("status"), "pages": compile_check.get("compile", {}).get("page_count")},
        "L1+",
    )
    add_check(
        "sup.release.diff-basis",
        "Release-diff changes carry basis notes",
        "pass" if int(release_diff.get("missing_basis_count", 0) or 0) == 0 else "fail",
        {"changes": release_diff.get("change_count", 0), "missing_basis": release_diff.get("missing_basis_count", 0)},
        "L1+",
    )
    add_check(
        "sup.regression",
        "Regression baseline passes",
        "pass" if regression.get("status") == "passed" else "fail",
        {"status": regression.get("status"), "failed_count": regression.get("failed_count")},
        "L1+",
    )

    computed = load_json(REPORTS / "computed_statuses.json")
    gr_status = gr_successor.get("posture") or computed.get("status:GR", {}).get("effective_status") or gr_pilot.get("computed_posture") or gr_pilot.get("posture")
    ym_status = computed.get("status:YM", {}).get("effective_status") or ym_pilot.get("computed_posture") or ym_pilot.get("posture")
    add_check(
        "sup.gr.pilot",
        "GR pilot locally infers current posture",
        "pass" if gr_status == "domain-bounded-cert-close" else "needs-work",
        {"computed_posture": gr_status},
        "L2+",
    )
    add_check(
        "sup.ym.pilot",
        "YM pilot locally infers current posture",
        "pass" if ym_status == "conditional-cert-close" else "needs-work",
        {"computed_posture": ym_status},
        "L2+",
    )

    gr_successor_compile = compile_check.get("targets", {}).get("gr_branch_successor", {})
    add_check(
        "sup.gr.successor-packet",
        "GR generated branch-successor shell passes equivalence and compile checks",
        "pass" if gr_successor.get("status") == "passed" and gr_successor_compile.get("status") == "passed" else "needs-work",
        {
            "status": gr_successor.get("status"),
            "computed_posture": gr_successor.get("posture"),
            "pages": gr_successor_compile.get("compile", {}).get("page_count"),
        },
        "L2+",
    )

    # Full replacement gates are deliberately not passed in v18.
    add_check(
        "sup.full-claim-equivalence",
        "Full current-corpus claim catalog equivalence",
        "not-started",
        "No full spine/branch claim equivalence audit has been run.",
        "L5",
    )
    add_check(
        "sup.full-prose-migration",
        "Full theorem/proof prose migrated into structured source",
        "not-started",
        "Human-authored theorem bodies remain outside the generated successor corpus.",
        "L5",
    )
    add_check(
        "sup.full-pdf-corpus",
        "All successor books compile as generated PDFs",
        "not-started",
        "Only the governance appendix compiles in v18.",
        "L5",
    )
    add_check(
        "sup.human-release-approval",
        "Formal supersession decision recorded",
        "not-started",
        "No decision log entry approves full corpus supersession.",
        "L5",
    )

    l1_checks = [c for c in checks if c["required_for"] == "L1+"]
    l2_checks = [c for c in checks if c["required_for"] in {"L1+", "L2+"}]
    l5_checks = checks

    l1_ready = all(c["status"] == "pass" for c in l1_checks)
    l2_ready = l1_ready and all(c["status"] == "pass" for c in l2_checks if c["required_for"] == "L2+")
    l3_report = load_json(REPORTS / "l3_readiness_report.json")
    l3_ready = l2_ready and len(l3_report.get("l3_ready_branches", [])) >= 2
    # L3 is satisfied when at least GR and YM pass the L3 gate
    l5_ready = all(c["status"] == "pass" for c in l5_checks)

    report = {
        "schema_version": load_yaml(CANON / "schema_version.yaml").get("schema", {}).get("version"),
        "policy_version": policy.get("version"),
        "current_level": policy.get("current_level"),
        "recommended_next_level": policy.get("recommended_next_level"),
        "approved_for_full_supersession": bool(policy.get("approved_for_full_supersession", False)) and l5_ready,
        "l1_import_ready": l1_ready,
        "l2_pilot_ready": l2_ready,
        "l5_full_supersession_ready": l5_ready,
        "checks": checks,
        "summary": {
            "pass": sum(1 for c in checks if c["status"] == "pass"),
            "needs_work": sum(1 for c in checks if c["status"] == "needs-work"),
            "not_started": sum(1 for c in checks if c["status"] == "not-started"),
            "fail": sum(1 for c in checks if c["status"] == "fail"),
        },
        "recommendation": "Harden the L2 GR branch-successor pilot and then decide whether to pilot YM. Do not supersede the full spine/branch corpus yet.",
    }

    with (REPORTS / "supersession_readiness_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# Supersession Readiness Report",
        "",
        f"**Schema version:** {report['schema_version']}",
        f"**Current supersession level:** {report['current_level']}",
        f"**Recommended next level:** {report['recommended_next_level']}",
        f"**L1 import-ready:** {report['l1_import_ready']}",
        f"**L2 pilot-ready:** {report['l2_pilot_ready']}",
        f"**Full corpus supersession-ready:** {report['l5_full_supersession_ready']}",
        f"**Approved for full supersession:** {report['approved_for_full_supersession']}",
        "",
        "## Readiness checks",
        "",
        "| Check | Required for | Status | Evidence |",
        "|---|---|---|---|",
    ]
    for c in checks:
        evidence = c["evidence"]
        if isinstance(evidence, dict):
            evidence_text = ", ".join(f"{k}={v}" for k, v in evidence.items() if k in {"status", "errors", "warnings", "changes", "missing_basis", "pages", "computed_posture", "failed_count"})
        else:
            evidence_text = str(evidence)
        lines.append(f"| `{c['id']}` {c['label']} | {c['required_for']} | **{c['status']}** | {evidence_text} |")

    lines += [
        "",
        "## Interpretation",
        "",
        "v19 supports an L2 GR branch-successor pilot in addition to generated governance appendices. It does not authorize replacement of the current spine or branch books.",
        "",
        "The next prudent milestone is L2 hardening: improve GR equivalence coverage, review migrated prose preservation, and only then consider a YM successor pilot.",
    ]

    (TABLES / "supersession_readiness_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "current_level": report["current_level"],
        "l1_import_ready": report["l1_import_ready"],
        "l2_pilot_ready": report["l2_pilot_ready"],
        "l5_full_supersession_ready": report["l5_full_supersession_ready"],
        "approved_for_full_supersession": report["approved_for_full_supersession"],
    }, indent=2))


if __name__ == "__main__":
    main()
