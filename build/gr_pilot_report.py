from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "GR"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

GR_ORDER = [
    "ob:GR.real",
    "thm:GR.realization",
    "ob:GR.deform",
    "thm:GR.deformation",
    "ob:GR.compat",
    "thm:GR.compat",
    "ob:GR.EFE1",
    "ob:GR.EFE2",
    "ob:GR.EFE3",
    "ob:GR.closure",
    "thm:GR.domain",
    "ob:GR.global-subcriticality",
    "status:GR",
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
    for cid in GR_ORDER:
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
        "# GR Pilot Migration Report",
        "",
        "This report is generated from GR branch records and computed governance status.",
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
        "- GR local posture is expected to compute as `domain-bounded-cert-close`.",
        "- `ob:GR.global-subcriticality` is expected to remain `O` at global scope.",
        "- The pilot is successful when the GR posture is no longer stale while global closure remains blocked.",
        "",
    ]
    (TABLES / "gr_pilot_report.md").write_text("\n".join(lines), encoding="utf-8")

    with (REPORTS / "gr_pilot_report.json").open("w", encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2)

    print(json.dumps({"gr_rows": len(rows)}, indent=2))

if __name__ == "__main__":
    main()
