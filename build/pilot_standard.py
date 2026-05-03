
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required.") from exc

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canon"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"


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


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def check_status(ok: bool) -> str:
    return "pass" if ok else "fail"


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    cfg = load_yaml(CANON / "pilot_standard.yaml").get("pilot_standard", {})
    computed = load_json(REPORTS / "computed_statuses.json")
    compile_report = load_json(REPORTS / "compile_check_report.json")
    compile_targets = compile_report.get("targets", {}) or {}

    rows: List[Dict[str, Any]] = []
    checks: List[Dict[str, Any]] = []

    for pilot in cfg.get("pilots", []):
        branch = pilot["branch"]
        eq_path = ROOT / pilot["equivalence_report"]
        eq = load_json(eq_path)
        compile_target = compile_targets.get(pilot["compile_target_id"], {}) or {}
        expected_frontiers = pilot.get("expected_frontiers")
        if expected_frontiers is None:
            legacy = pilot.get("expected_frontier")
            expected_frontiers = [legacy] if legacy else []
        expected_posture = pilot["expected_posture"]
        supersession_allowed = as_list(pilot.get("supersession_effect_allowed"))
        actual_supersession = eq.get("supersession_effect")
        frontiers = eq.get("active_frontiers") or []
        tex_path = ROOT / pilot["tex_target"]
        pdf_path = ROOT / pilot["pdf_target"]
        frontier_statuses = {fid: computed.get(fid, {}).get("effective_status") for fid in expected_frontiers}
        status_id = pilot.get("status_id")
        computed_posture = computed.get(status_id, {}).get("effective_status") if status_id else None
        hardening_report = load_json(ROOT / pilot["hardening_report"]) if pilot.get("hardening_report") else {}

        branch_checks = [
            ("equivalence_report_passed", eq.get("status") == "passed", eq.get("status"), "passed"),
            ("compile_target_passed", compile_target.get("status") == "passed" or pdf_path.exists(), compile_target.get("status") or ("pdf_exists" if pdf_path.exists() else "missing"), "passed"),
            ("expected_posture_preserved", eq.get("posture") == expected_posture and computed_posture == expected_posture, {"equivalence": eq.get("posture"), "computed": computed_posture}, expected_posture),
            ("expected_frontier_profile_preserved", sorted(frontiers) == sorted(expected_frontiers), frontiers, expected_frontiers),
            ("no_supersession_effect", actual_supersession in supersession_allowed, actual_supersession, supersession_allowed),
            ("expected_active_frontiers_are_open", all(status == "O" for status in frontier_statuses.values()), frontier_statuses, "all expected frontiers have effective status O"),
            ("successor_tex_present", tex_path.exists(), str(tex_path.relative_to(ROOT)), "exists"),
            ("successor_pdf_present", pdf_path.exists(), str(pdf_path.relative_to(ROOT)), "exists"),
        ]
        if hardening_report:
            branch_checks.append(("hardening_passed", hardening_report.get("status") == "passed", hardening_report.get("status"), "passed"))

        for name, ok, observed, expected in branch_checks:
            checks.append({
                "id": f"{branch}.{name}",
                "branch": branch,
                "check": name,
                "status": check_status(ok),
                "observed": observed,
                "expected": expected,
            })

        failed_branch = [c for c in checks if c["branch"] == branch and c["status"] == "fail"]
        rows.append({
            "branch": branch,
            "status": "passed" if not failed_branch else "failed",
            "expected_posture": expected_posture,
            "computed_posture": computed_posture,
            "preserved_frontiers": expected_frontiers,
            "frontier_statuses": frontier_statuses,
            "compile_status": compile_target.get("status"),
            "equivalence_status": eq.get("status"),
            "supersession_effect": actual_supersession,
            "failed_checks": len(failed_branch),
        })

    failed = [c for c in checks if c["status"] == "fail"]
    report = {
        "standard_version": cfg.get("version"),
        "level": cfg.get("level"),
        "status": "failed" if failed else "passed",
        "pilot_count": len(rows),
        "failed_count": len(failed),
        "rows": rows,
        "checks": checks,
        "template": {
            "required_checks": cfg.get("required_checks", []),
            "required_pilot_fields": [
                "branch",
                "status_id",
                "generator",
                "tex_target",
                "pdf_target",
                "compile_target_id",
                "equivalence_report",
                "expected_posture",
                "expected_frontiers",
                "must_not_claim",
                "supersession_effect_allowed",
            ],
        },
    }
    with (REPORTS / "l2_pilot_standard_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# L2 Pilot Standard Report",
        "",
        f"**Status:** {report['status']}",
        f"**Standard version:** {report['standard_version']}",
        f"**Pilots checked:** {report['pilot_count']}",
        f"**Failed checks:** {report['failed_count']}",
        "",
        "| Branch | Status | Expected posture | Computed posture | Preserved frontiers | Frontier statuses | Compile | Equivalence | Supersession | Failed checks |",
        "|---|---|---|---|---|---|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['branch']} | **{row['status']}** | `{row['expected_posture']}` | `{row['computed_posture']}` | "
            f"`{row['preserved_frontiers']}` | `{row['frontier_statuses']}` | {row['compile_status']} | {row['equivalence_status']} | "
            f"{row['supersession_effect']} | {row['failed_checks']} |"
        )
    lines += [
        "",
        "## Check details",
        "",
        "| Check | Status | Observed | Expected |",
        "|---|---|---|---|",
    ]
    for chk in checks:
        lines.append(f"| `{chk['id']}` | **{chk['status']}** | `{chk['observed']}` | `{chk['expected']}` |")
    (TABLES / "l2_pilot_standard_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    tmpl = [
        "# L2 Pilot Standard Template",
        "",
        "A configured L2 branch-successor pilot must provide the following fields and pass the following checks.",
        "",
        "## Required pilot fields",
        "",
    ]
    for field in report["template"]["required_pilot_fields"]:
        tmpl.append(f"- `{field}`")
    tmpl += [
        "",
        "## Required checks",
        "",
    ]
    for check in report["template"]["required_checks"]:
        tmpl.append(f"- `{check}`")
    tmpl += [
        "",
        "## Current configured pilots",
        "",
    ]
    for row in rows:
        tmpl.append(f"- **{row['branch']}**: posture `{row['expected_posture']}`, frontiers `{row['preserved_frontiers']}`")
    (TABLES / "l2_pilot_standard_template.md").write_text("\n".join(tmpl) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": report["status"],
        "pilot_count": report["pilot_count"],
        "failed_count": report["failed_count"],
    }, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
