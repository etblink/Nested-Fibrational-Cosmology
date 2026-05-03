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


SCORE = {
    "very-high": 5,
    "high": 4,
    "medium-high": 3.5,
    "medium": 3,
    "medium-low": 2,
    "low-medium": 2,
    "low": 1,
}
RISK_PENALTY = {
    "low": 0,
    "medium": 1,
    "medium-high": 1.5,
    "high": 2.5,
    "very-high": 4,
}


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def readiness_score(candidate: Dict[str, Any]) -> float:
    value = SCORE.get(candidate.get("canon_value"), 0)
    readiness = SCORE.get(candidate.get("migration_readiness"), 0)
    risk = RISK_PENALTY.get(candidate.get("risk_band"), 0)
    order_bonus = max(0, 8 - int(candidate.get("recommended_order", 99))) * 0.1
    return round(value + readiness - risk + order_bonus, 2)


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    intake = load_yaml(CANON / "pilot_intake.yaml")
    computed = load_json(REPORTS / "computed_statuses.json")
    quality = load_json(REPORTS / "quality_gate_report.json")

    candidates: List[Dict[str, Any]] = []
    for c in intake.get("candidates", []):
        branch = c.get("branch")
        status_id = f"status:{branch}"
        computed_posture = computed.get(status_id, {}).get("effective_status")
        posture_matches = computed_posture == c.get("current_posture")
        row = dict(c)
        row["status_id"] = status_id
        row["computed_posture"] = computed_posture
        row["posture_matches_computed"] = posture_matches
        row["score"] = readiness_score(c)
        row["blocked"] = bool(not posture_matches)
        candidates.append(row)

    ranked = sorted(candidates, key=lambda x: (-float(x.get("score", 0)), int(x.get("recommended_order", 99)), x.get("branch", "")))
    recommended = next((c for c in ranked if not c.get("blocked")), None)

    gate_status = quality.get("status")
    report = {
        "schema_version": intake.get("schema_version"),
        "status": "passed" if recommended else "failed",
        "current_l2_pilots": intake.get("current_l2_pilots", []),
        "candidate_count": len(candidates),
        "recommended_next_pilot": recommended.get("branch") if recommended else None,
        "recommended_rationale": recommended.get("rationale") if recommended else None,
        "ranked_candidates": ranked,
        "quality_gate_status_observed": gate_status,
        "policy": intake.get("selection_policy", {}),
    }

    with (REPORTS / "pilot_intake_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# L2 Pilot Intake Report",
        "",
        f"**Status:** {report['status']}",
        f"**Schema version:** {report['schema_version']}",
        f"**Current L2 pilots:** {', '.join(report['current_l2_pilots'])}",
        f"**Recommended next pilot:** `{report['recommended_next_pilot']}`",
        "",
        "## Recommendation rationale",
        "",
        report.get("recommended_rationale") or "_No recommendation available._",
        "",
        "## Ranked candidates",
        "",
        "| Rank | Branch | Score | Current posture | Computed posture | Canon value | Readiness | Risk | Blocked |",
        "|---:|---|---:|---|---|---|---|---|---|",
    ]
    for idx, c in enumerate(ranked, start=1):
        lines.append(
            f"| {idx} | `{c.get('branch')}` | {c.get('score')} | `{c.get('current_posture')}` | "
            f"`{c.get('computed_posture')}` | {c.get('canon_value')} | {c.get('migration_readiness')} | "
            f"{c.get('risk_band')} | {c.get('blocked')} |"
        )

    lines += [
        "",
        "## Required successor checks for recommended branch",
        "",
    ]
    if recommended:
        for check in recommended.get("required_successor_checks", []):
            lines.append(f"- {check}")
    else:
        lines.append("_None._")

    lines += [
        "",
        "## Project Lead policy notes",
        "",
    ]
    policy = report.get("policy", {})
    for key, value in policy.items():
        if isinstance(value, list):
            lines.append(f"- **{key}:** {', '.join(value)}")
        else:
            lines.append(f"- **{key}:** {value}")

    (TABLES / "pilot_intake_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": report["status"],
        "recommended_next_pilot": report["recommended_next_pilot"],
        "candidate_count": report["candidate_count"],
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
