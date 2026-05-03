from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

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


def add_result(results: List[Dict[str, Any]], test_id: str, status: str, message: str, observed: Any = None, expected: Any = None) -> None:
    results.append({
        "id": test_id,
        "status": status,
        "message": message,
        "observed": observed,
        "expected": expected,
    })


def main() -> int:
    baseline = load_yaml(CANON / "regression_baseline.yaml").get("regression_baseline", {})
    summary = load_json(REPORTS / "audit_summary.json")
    audit = load_json(REPORTS / "audit_report.json")
    computed = load_json(REPORTS / "computed_statuses.json")
    digest = load_json(REPORTS / "governance_digest.json")
    branch_report = load_json(REPORTS / "branch_posture_report.json")
    release_diff = load_json(REPORTS / "release_diff_report.json")

    results: List[Dict[str, Any]] = []
    expected_counts = baseline.get("expected_counts", {})

    checks = [
        ("schema_version", summary.get("schema_version"), baseline.get("schema_version")),
        ("claims", summary.get("claims_count"), expected_counts.get("claims")),
        ("computed_statuses", summary.get("computed_statuses"), expected_counts.get("computed_statuses")),
        ("errors", summary.get("errors"), expected_counts.get("errors")),
        ("release_diff_changes", release_diff.get("change_count"), expected_counts.get("release_diff_changes")),
        ("release_diff_missing_basis", release_diff.get("missing_basis_count"), expected_counts.get("release_diff_missing_basis")),
    ]
    for name, observed, expected in checks:
        add_result(
            results,
            f"regression.{name}",
            "pass" if observed == expected else "fail",
            f"{name} must match the active regression baseline.",
            observed,
            expected,
        )

    warnings = int(summary.get("warnings", 0) or 0)
    warnings_max = int(expected_counts.get("warnings_max", 0) or 0)
    add_result(
        results,
        "regression.warnings_max",
        "pass" if warnings <= warnings_max else "fail",
        "Warning count must not exceed the accepted baseline.",
        warnings,
        warnings_max,
    )

    warning_types = sorted({issue.get("type", "") for issue in audit.get("issues", []) if issue.get("severity") == "warning"})
    expected_warning_types = sorted(baseline.get("expected_warning_types", []))
    add_result(
        results,
        "regression.warning_types",
        "pass" if warning_types == expected_warning_types else "fail",
        "Warning classes must remain stable unless the baseline is intentionally updated.",
        warning_types,
        expected_warning_types,
    )

    active_items = sorted(digest.get("active_open_items", []))
    expected_active = sorted(baseline.get("expected_active_open_items", []))
    add_result(
        results,
        "regression.active_open_items",
        "pass" if active_items == expected_active else "fail",
        "Active open-item identity must remain stable unless canon coverage or release state changes.",
        active_items,
        expected_active,
    )

    computed_postures = {
        cid.split(":", 1)[1]: info.get("effective_status")
        for cid, info in computed.items()
        if cid.startswith("status:")
    }
    expected_postures = baseline.get("expected_branch_postures", {})
    posture_mismatches = {
        branch: {"observed": computed_postures.get(branch), "expected": expected}
        for branch, expected in sorted(expected_postures.items())
        if computed_postures.get(branch) != expected
    }
    add_result(
        results,
        "regression.branch_postures",
        "pass" if not posture_mismatches else "fail",
        "Computed branch postures must match the active regression baseline.",
        posture_mismatches or "all matched",
        expected_postures,
    )

    protected = baseline.get("protected_claim_statuses", {})
    protected_mismatches = {
        cid: {"observed": computed.get(cid, {}).get("effective_status"), "expected": expected}
        for cid, expected in sorted(protected.items())
        if computed.get(cid, {}).get("effective_status") != expected
    }
    add_result(
        results,
        "regression.protected_claim_statuses",
        "pass" if not protected_mismatches else "fail",
        "Protected pilot claims must retain their effective statuses.",
        protected_mismatches or "all matched",
        protected,
    )

    failed = [r for r in results if r["status"] != "pass"]
    report = {
        "status": "passed" if not failed else "failed",
        "test_count": len(results),
        "failed_count": len(failed),
        "results": results,
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    with (REPORTS / "regression_test_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# Regression Test Report",
        "",
        f"**Status:** {report['status']}",
        f"**Tests:** {report['test_count']}",
        f"**Failures:** {report['failed_count']}",
        "",
        "| Test | Status | Observed | Expected |",
        "|---|---:|---|---|",
    ]
    for r in results:
        observed = json.dumps(r.get("observed"), ensure_ascii=False)
        expected = json.dumps(r.get("expected"), ensure_ascii=False)
        lines.append(f"| `{r['id']}` | {r['status']} | `{observed}` | `{expected}` |")
    (TABLES / "regression_test_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": report["status"],
        "test_count": report["test_count"],
        "failed_count": report["failed_count"],
    }, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
