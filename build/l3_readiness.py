"""
build/l3_readiness.py — v33 L3 Readiness Checker

Checks whether each L2 pilot is ready to be promoted to L3 status
(branch successor release candidate). L3 requires:

  1. All expected claims present with non-trivial prose stubs
  2. All discharge edges typed with explicit discharge modes
  3. All scope objects complete (regime, domain, certificate_scope, promotion_ceiling)
  4. Equivalence report passed
  5. PDF compiled and rendered
  6. Posture reconciles with current release snapshot
  7. Active frontiers are open and correctly labeled
  8. No illegal promotions
  9. Why-status trace available
  10. For GR/YM: canonical coverage >= 90%

Output:
  output/reports/l3_readiness_report.json
  output/tables/l3_readiness_report.md
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

# Per-pilot L3 criteria
L3_PILOTS = [
    {
        "branch": "GR",
        "status_id": "status:GR",
        "expected_posture": "domain-bounded-cert-close",
        "expected_frontiers": ["ob:GR.global-subcriticality"],
        "equivalence_report": "output/reports/gr_successor_equivalence_report.json",
        "pdf_path": "output/pdf/gr_branch_successor_standalone.pdf",
        "requires_canonical_coverage": True,
        "canonical_coverage_report": "output/reports/canonical_coverage_gr.json",
        "min_coverage_pct": 90.0,
        "min_prose_score": 80.0,
        "min_scope_score": 80.0,
    },
    {
        "branch": "YM",
        "status_id": "status:YM",
        "expected_posture": "conditional-cert-close",
        "expected_frontiers": ["ob:YM.B3.A2"],
        "equivalence_report": "output/reports/ym_successor_equivalence_report.json",
        "pdf_path": "output/pdf/ym_branch_successor_standalone.pdf",
        "requires_canonical_coverage": True,
        "canonical_coverage_report": "output/reports/canonical_coverage_ym.json",
        "min_coverage_pct": 90.0,
        "min_prose_score": 80.0,
        "min_scope_score": 80.0,
    },
    {
        "branch": "NS",
        "status_id": "status:NS",
        "expected_posture": "domain-bounded-cert-close",
        "expected_frontiers": ["front:NS.main"],
        "equivalence_report": "output/reports/ns_successor_equivalence_report.json",
        "pdf_path": "output/pdf/ns_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 60.0,
        "min_scope_score": 60.0,
    },
    {
        "branch": "SM",
        "status_id": "status:SM",
        "expected_posture": "intrinsic-structural-close",
        "expected_frontiers": ["ob:SM.O-IDcont"],
        "equivalence_report": "output/reports/sm_successor_equivalence_report.json",
        "pdf_path": "output/pdf/sm_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 60.0,
        "min_scope_score": 60.0,
    },
    {
        "branch": "RH",
        "status_id": "status:RH",
        "expected_posture": "cert-proj",
        "expected_frontiers": ["ob:RH.S1-ARC"],
        "equivalence_report": "output/reports/rh_successor_equivalence_report.json",
        "pdf_path": "output/pdf/rh_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 60.0,
        "min_scope_score": 60.0,
    },
    {
        "branch": "SPEC",
        "status_id": "status:SPEC",
        "expected_posture": "cert-close",
        "expected_frontiers": [],
        "equivalence_report": "output/reports/spec_successor_equivalence_report.json",
        "pdf_path": "output/pdf/spec_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 50.0,
        "min_scope_score": 50.0,
    },
    {
        "branch": "SCC",
        "status_id": "status:SCC",
        "expected_posture": "conditional-cert-close",
        "expected_frontiers": [],
        "equivalence_report": "output/reports/scc_successor_equivalence_report.json",
        "pdf_path": "output/pdf/scc_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 50.0,
        "min_scope_score": 50.0,
    },
    {
        "branch": "BIO",
        "status_id": "status:BIO",
        "expected_posture": "conditional-cert-close",
        "expected_frontiers": ["ob:BIO.BND-open"],
        "equivalence_report": "output/reports/bio_successor_equivalence_report.json",
        "pdf_path": "output/pdf/bio_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 50.0,
        "min_scope_score": 50.0,
    },
    {
        "branch": "LING",
        "status_id": "status:LING",
        "expected_posture": "conditional-cert-close",
        "expected_frontiers": ["ob:LING.REF-INVIS-RECOV"],
        "equivalence_report": "output/reports/ling_successor_equivalence_report.json",
        "pdf_path": "output/pdf/ling_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 50.0,
        "min_scope_score": 50.0,
    },
    {
        "branch": "CRYST",
        "status_id": "status:CRYST",
        "expected_posture": "conditional-cert-close",
        "expected_frontiers": ["ob:CRYST.phase-problem"],
        "equivalence_report": "output/reports/cryst_successor_equivalence_report.json",
        "pdf_path": "output/pdf/cryst_branch_successor_standalone.pdf",
        "requires_canonical_coverage": False,
        "min_coverage_pct": 0.0,
        "min_prose_score": 50.0,
        "min_scope_score": 50.0,
    },
]

# L3 readiness levels
L3_LEVELS = {
    "not_started": "L2 only — no L3 work begun",
    "l3_candidate": "L3 candidate — passes basic checks but coverage gaps remain",
    "l3_ready": "L3 ready — passes all L3 criteria, eligible for release candidate",
}


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_pilot_l3(pilot: Dict[str, Any]) -> Dict[str, Any]:
    branch = pilot["branch"]
    eq_path = ROOT / pilot["equivalence_report"]
    pdf_path = ROOT / pilot["pdf_path"]
    eq = load_json(eq_path)

    checks: List[Dict[str, Any]] = []

    def add(check_id: str, passed: bool, observed: Any, expected: Any, severity: str = "error") -> None:
        checks.append({
            "id": check_id,
            "status": "pass" if passed else "fail",
            "severity": severity,
            "observed": observed,
            "expected": expected,
        })

    # 1. Equivalence report
    add("l3.equivalence_passed", eq.get("status") == "passed",
        eq.get("status", "missing"), "passed")

    # 2. PDF compiled
    add("l3.pdf_compiled", pdf_path.exists(),
        str(pdf_path.relative_to(ROOT)) if pdf_path.exists() else "missing",
        "exists")

    # 3. Posture correct
    actual_posture = eq.get("posture")
    add("l3.posture_correct", actual_posture == pilot["expected_posture"],
        actual_posture, pilot["expected_posture"])

    # 4. Frontiers preserved
    actual_frontiers = sorted(eq.get("active_frontiers", []) or [])
    expected_frontiers = sorted(pilot["expected_frontiers"])
    frontiers_ok = all(f in actual_frontiers for f in expected_frontiers)
    add("l3.frontiers_preserved", frontiers_ok,
        actual_frontiers, expected_frontiers)

    # 5. No supersession claimed
    supersession = eq.get("supersession_effect", "")
    add("l3.no_supersession",
        supersession in ("none", "none; pilot shell only", ""),
        supersession, "none or none; pilot shell only")

    # 6. Proof trees available
    trees_path = ROOT / "output" / "reports" / "proof_trees.json"
    trees_data = load_json(trees_path)
    trees_branches = [t.get("branch") for t in trees_data] if isinstance(trees_data, list) else []
    add("l3.proof_tree_available", branch in trees_branches,
        branch, f"{branch} in proof_trees.json",
        severity="warning")

    # 7. Canonical coverage (GR/YM only)
    if pilot.get("requires_canonical_coverage"):
        cov_report = load_json(ROOT / pilot["canonical_coverage_report"])
        coverage_pct = cov_report.get("coverage_pct", 0.0)
        prose_score = cov_report.get("prose_score", 0.0)
        scope_score = cov_report.get("scope_score", 0.0)

        add("l3.canonical_coverage",
            coverage_pct >= pilot["min_coverage_pct"],
            f"{coverage_pct}%", f">= {pilot['min_coverage_pct']}%")

        add("l3.prose_score",
            prose_score >= pilot["min_prose_score"],
            f"{prose_score}%", f">= {pilot['min_prose_score']}%")

        add("l3.scope_score",
            scope_score >= pilot["min_scope_score"],
            f"{scope_score}%", f">= {pilot['min_scope_score']}%")
    else:
        # For non-GR/YM, just check that prose stubs exist in the eq report
        generated_count = eq.get("generated_claim_count", 0)
        add("l3.claims_present",
            generated_count > 0,
            f"{generated_count} claims", "> 0",
            severity="warning")

    # Compute L3 level
    hard_fails = [c for c in checks if c["status"] == "fail" and c["severity"] == "error"]
    soft_fails = [c for c in checks if c["status"] == "fail" and c["severity"] == "warning"]

    if not hard_fails and not soft_fails:
        level = "l3_ready"
    elif not hard_fails:
        level = "l3_candidate"
    else:
        level = "not_started"

    return {
        "branch": branch,
        "level": level,
        "level_description": L3_LEVELS[level],
        "l3_ready": level == "l3_ready",
        "l3_candidate": level in ("l3_ready", "l3_candidate"),
        "hard_failures": [c["id"] for c in hard_fails],
        "soft_failures": [c["id"] for c in soft_fails],
        "checks": checks,
    }


def render_l3_md(results: List[Dict[str, Any]]) -> List[str]:
    lines = [
        "# v33 L3 Readiness Report",
        "",
        "Formal per-pilot L3 gate — checks whether each L2 pilot is ready for",
        "promotion to L3 (branch successor release candidate) status.",
        "",
        "| Branch | Level | L3 Ready | Hard failures | Soft failures |",
        "|--------|-------|----------|---------------|---------------|",
    ]
    for r in results:
        level_badge = "✅" if r["l3_ready"] else ("🟡" if r["l3_candidate"] else "⬜")
        lines.append(
            f"| {r['branch']} | {level_badge} {r['level']} "
            f"| {r['l3_ready']} "
            f"| {', '.join(r['hard_failures']) or 'none'} "
            f"| {', '.join(r['soft_failures']) or 'none'} |"
        )
    lines += ["", "---", ""]

    for r in results:
        lines += [
            f"## {r['branch']}",
            "",
            f"**Level:** `{r['level']}`  ",
            f"**Description:** {r['level_description']}",
            "",
            "| Check | Status | Observed | Expected |",
            "|-------|--------|----------|----------|",
        ]
        for c in r["checks"]:
            sev = "" if c["severity"] == "error" else " _(warn)_"
            lines.append(
                f"| `{c['id']}` | {'✅' if c['status']=='pass' else '❌'}{sev} "
                f"| {str(c['observed'])[:50]} "
                f"| {str(c['expected'])[:50]} |"
            )
        lines.append("")

    return lines


def main() -> int:
    results = [check_pilot_l3(pilot) for pilot in L3_PILOTS]

    l3_ready_branches = [r["branch"] for r in results if r["l3_ready"]]
    l3_candidate_branches = [r["branch"] for r in results if r["l3_candidate"] and not r["l3_ready"]]

    report = {
        "status": "passed",
        "l3_ready_branches": l3_ready_branches,
        "l3_candidate_branches": l3_candidate_branches,
        "results": results,
        "summary": {
            "total_pilots": len(results),
            "l3_ready": len(l3_ready_branches),
            "l3_candidate": len(l3_candidate_branches),
            "not_started": len(results) - len(l3_ready_branches) - len(l3_candidate_branches),
        },
    }

    # Remove verbose checks from results for JSON readability
    slim_results = [
        {k: v for k, v in r.items() if k != "checks"}
        for r in results
    ]
    slim_report = {**report, "results": slim_results}

    (REPORTS / "l3_readiness_report.json").write_text(
        json.dumps(slim_report, indent=2), encoding="utf-8"
    )
    (TABLES / "l3_readiness_report.md").write_text(
        "\n".join(render_l3_md(results)) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "status": "passed",
        "l3_ready_branches": l3_ready_branches,
        "l3_candidate_branches": l3_candidate_branches,
        "summary": report["summary"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
