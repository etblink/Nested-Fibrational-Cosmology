from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def status(value: bool) -> str:
    return "pass" if value else "fail"


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    computed = load_json(REPORTS / "computed_statuses.json")
    compile_report = load_json(REPORTS / "compile_check_report.json")
    gr = load_json(REPORTS / "gr_successor_equivalence_report.json")
    ym = load_json(REPORTS / "ym_successor_equivalence_report.json")
    gr_l2 = load_json(REPORTS / "gr_l2_hardening_report.json")

    compile_targets = compile_report.get("targets", {}) or {}

    pilots = {
        "GR": {
            "expected_posture": "domain-bounded-cert-close",
            "expected_frontier": "ob:GR.global-subcriticality",
            "equivalence_report": gr,
            "compile_target": "gr_branch_successor",
            "hardening_report": gr_l2,
            "must_not_claim": "global-cert-close",
        },
        "YM": {
            "expected_posture": "conditional-cert-close",
            "expected_frontier": "ob:YM.B3.A2",
            "equivalence_report": ym,
            "compile_target": "ym_branch_successor",
            "hardening_report": None,
            "must_not_claim": "unconditional-clay-cert-close",
        },
    }

    checks: List[Dict[str, Any]] = []
    pilot_rows: List[Dict[str, Any]] = []

    for name, cfg in pilots.items():
        eq = cfg["equivalence_report"] or {}
        compile_target = compile_targets.get(cfg["compile_target"], {}) or {}
        posture = eq.get("posture")
        frontiers = eq.get("active_frontiers") or []
        expected_frontier = cfg["expected_frontier"]
        expected_posture = cfg["expected_posture"]
        hardening = cfg.get("hardening_report")

        row = {
            "pilot": name,
            "equivalence_status": eq.get("status"),
            "compile_status": compile_target.get("status"),
            "posture": posture,
            "expected_posture": expected_posture,
            "frontier_preserved": expected_frontier in frontiers,
            "expected_frontier": expected_frontier,
            "supersession_effect": eq.get("supersession_effect"),
            "hardening_status": (hardening or {}).get("status") if hardening is not None else "not-required-in-v22",
        }
        pilot_rows.append(row)

        checks.extend([
            {
                "id": f"{name}.equivalence_passed",
                "status": status(eq.get("status") == "passed"),
                "observed": eq.get("status"),
                "expected": "passed",
            },
            {
                "id": f"{name}.compiled",
                "status": status(compile_target.get("status") == "passed"),
                "observed": compile_target.get("status"),
                "expected": "passed",
            },
            {
                "id": f"{name}.posture_preserved",
                "status": status(posture == expected_posture),
                "observed": posture,
                "expected": expected_posture,
            },
            {
                "id": f"{name}.frontier_preserved",
                "status": status(expected_frontier in frontiers),
                "observed": frontiers,
                "expected": expected_frontier,
            },
            {
                "id": f"{name}.no_supersession",
                "status": status(str(eq.get("supersession_effect", "")).startswith("none")),
                "observed": eq.get("supersession_effect"),
                "expected": "none; pilot shell only",
            },
        ])

        if hardening is not None:
            checks.append({
                "id": f"{name}.l2_hardening_passed",
                "status": status(hardening.get("status") == "passed" and int(hardening.get("failed_count", 1) or 0) == 0),
                "observed": {"status": hardening.get("status"), "failed_count": hardening.get("failed_count")},
                "expected": {"status": "passed", "failed_count": 0},
            })

    # Cross-pilot invariants: the two generated pilots exercise different closure regimes.
    gr_posture = pilots["GR"]["equivalence_report"].get("posture")
    ym_posture = pilots["YM"]["equivalence_report"].get("posture")
    checks.append({
        "id": "cross_pilot.distinct_closure_regimes",
        "status": status(gr_posture != ym_posture),
        "observed": {"GR": gr_posture, "YM": ym_posture},
        "expected": "GR and YM postures remain distinct",
    })

    checks.append({
        "id": "cross_pilot.both_frontiers_in_computed_graph",
        "status": status("ob:GR.global-subcriticality" in computed and "ob:YM.B3.A2" in computed),
        "observed": {
            "ob:GR.global-subcriticality": "ob:GR.global-subcriticality" in computed,
            "ob:YM.B3.A2": "ob:YM.B3.A2" in computed,
        },
        "expected": "both active frontier IDs exist in computed status graph",
    })

    failed = [c for c in checks if c["status"] != "pass"]
    report = {
        "status": "passed" if not failed else "failed",
        "failed_count": len(failed),
        "pilots": pilot_rows,
        "checks": checks,
        "summary": {
            "pilot_count": len(pilot_rows),
            "checked_pilots": sorted(pilots.keys()),
            "distinct_closure_regimes": gr_posture != ym_posture,
            "full_supersession_effect": "none",
        },
    }

    with (REPORTS / "l2_pilot_comparison_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# L2 Pilot Comparison Report",
        "",
        f"**Status:** {report['status']}",
        f"**Failed checks:** {report['failed_count']}",
        "",
        "## Pilot matrix",
        "",
        "| Pilot | Equivalence | Compile | Posture | Frontier preserved | Supersession effect | Hardening |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in pilot_rows:
        lines.append(
            f"| {row['pilot']} | {row['equivalence_status']} | {row['compile_status']} | "
            f"`{row['posture']}` | {row['frontier_preserved']} (`{row['expected_frontier']}`) | "
            f"{row['supersession_effect']} | {row['hardening_status']} |"
        )

    lines += [
        "",
        "## Checks",
        "",
        "| Check | Status | Observed | Expected |",
        "|---|---|---|---|",
    ]
    for check in checks:
        lines.append(
            f"| `{check['id']}` | **{check['status']}** | `{check.get('observed')}` | `{check.get('expected')}` |"
        )

    lines += [
        "",
        "## Governance conclusion",
        "",
        "GR and YM now constitute two L2 branch-successor pilots under a shared comparison standard. "
        "The comparison explicitly preserves their different closure regimes and keeps both terminal frontiers open. "
        "No supersession of the canonical branch books is authorized by this report.",
        "",
    ]
    (TABLES / "l2_pilot_comparison_report.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"status": report["status"], "failed_count": report["failed_count"]}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
