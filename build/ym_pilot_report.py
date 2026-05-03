from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "YM"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

YM_ORDER = [
    "ob:YM.O-ID",
    "thm:YM.ID",
    "ob:YM.O-RIG",
    "thm:YM.RIG",
    "ob:YM.O-ENC",
    "thm:YM.ENC",
    "ob:YM.O-GLOB",
    "thm:YM.GLOB",
    "ob:YM.O-CLU",
    "thm:YM.CLU",
    "thm:YM.7",
    "ob:YM.B1",
    "thm:YM.B1.bridge",
    "ob:YM.B2",
    "thm:YM.B2.bridge",
    "ob:YM.B3",
    "thm:YM.B3.bridge",
    "ob:YM.B3.A2",
    "status:YM",
]

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_claims() -> Dict[str, Dict[str, Any]]:
    claims = {}
    for path in CLAIMS_DIR.glob("*.yaml"):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            data["_path"] = str(path.relative_to(ROOT))
            claims[cid] = data
    return claims

def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    claims = load_claims()
    computed = load_json(REPORTS / "computed_statuses.json")
    rows = []
    for cid in YM_ORDER:
        claim = claims.get(cid)
        if not claim:
            continue
        info = computed.get(cid, {})
        rows.append({
            "id": cid,
            "kind": claim.get("kind", ""),
            "declared": claim.get("declared_status", ""),
            "computed": info.get("effective_status", ""),
            "scope": claim.get("scope", {}).get("certificate_scope", ""),
            "source": info.get("source", ""),
            "title": claim.get("title", ""),
        })

    lines = [
        "# YM Pilot Migration Report",
        "",
        "This report is generated from YM branch records and computed governance status.",
        "",
        "| ID | Kind | Declared | Computed | Scope | Source | Title |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row[k]).replace("|", "\\|") for k in ["id", "kind", "declared", "computed", "scope", "source", "title"]) + " |")

    lines += [
        "",
        "## Pilot verdict",
        "",
        "- YM local posture is expected to compute as `conditional-cert-close`.",
        "- The B1/B2/B3 bridge packets are represented as conditional/scoped packets, not unconditional Clay-grade closure.",
        "- `ob:YM.B3.A2` is expected to remain `O` as the surviving residual frontier in this pilot slice.",
        "- The pilot is successful when conditional closure is represented without promoting YM to unconditional `cert-close`.",
        "",
    ]
    (TABLES / "ym_pilot_report.md").write_text("\n".join(lines), encoding="utf-8")

    with (REPORTS / "ym_pilot_report.json").open("w", encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2)

    print(json.dumps({"ym_rows": len(rows)}, indent=2))

if __name__ == "__main__":
    main()
