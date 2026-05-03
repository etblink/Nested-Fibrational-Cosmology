
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "GR"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"
REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

GR_ORDER = [
    "thm:VI.9.1",
    "thm:GR.CP.1",
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

EXPECTED_POSTURE = "domain-bounded-cert-close"
EXPECTED_FRONTIERS = ["ob:GR.global-subcriticality"]
EXPECTED_NO_SUPERSESSION = "none; pilot shell only"


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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def load_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(CLAIMS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            data["_path"] = str(path.relative_to(ROOT))
            claims[cid] = data
    # include the Book VI stub housed in GR for pilot purposes
    stub = CLAIMS_DIR / "thm_VI_9_1_stub.yaml"
    if stub.exists():
        data = load_yaml(stub)
        if data.get("id"):
            data["_path"] = str(stub.relative_to(ROOT))
            claims[data["id"]] = data
    return claims


def body_path_for(claim: Dict[str, Any], key: str) -> Path | None:
    rel = claim.get(key)
    if not rel:
        return None
    return ROOT / rel


def prose_manifest(claims: Dict[str, Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    entries: List[Dict[str, Any]] = []
    issues: List[Dict[str, Any]] = []
    for cid in GR_ORDER:
        claim = claims.get(cid)
        if not claim:
            issues.append({"id": cid, "severity": "error", "type": "missing-claim", "reason": "Expected GR pilot claim is absent."})
            continue
        for field in ("body_file", "proof_file"):
            path = body_path_for(claim, field)
            required = field == "body_file" or bool(claim.get(field))
            if path is None:
                if required and field == "body_file":
                    issues.append({"id": cid, "severity": "error", "type": "missing-body-file-field", "reason": "Claim has no body_file field."})
                continue
            exists = path.exists()
            size = path.stat().st_size if exists else 0
            sha = sha256_file(path) if exists else None
            if required and not exists:
                issues.append({"id": cid, "severity": "error", "type": "missing-prose-file", "reason": f"{field} path does not exist.", "path": str(path.relative_to(ROOT))})
            elif required and size == 0:
                issues.append({"id": cid, "severity": "error", "type": "empty-prose-file", "reason": f"{field} is empty.", "path": str(path.relative_to(ROOT))})
            entries.append({
                "claim_id": cid,
                "field": field,
                "path": str(path.relative_to(ROOT)),
                "exists": exists,
                "size_bytes": size,
                "sha256": sha,
            })
    return entries, issues


def rendered_presence_checks(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    tex_path = TEX / "gr_branch_successor.tex"
    text = tex_path.read_text(encoding="utf-8", errors="replace") if tex_path.exists() else ""
    checks: List[Dict[str, Any]] = []
    for cid in GR_ORDER:
        present = cid in text
        checks.append({
            "id": f"gr.render.contains.{cid}",
            "status": "pass" if present else "fail",
            "observed": present,
            "expected": True,
            "message": "Generated GR successor TeX should contain every pilot machine ID.",
        })
    return checks


def dependency_scope_checks(claims: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    for cid in GR_ORDER:
        claim = claims.get(cid, {})
        if not claim:
            continue
        scope = claim.get("scope", {}) or {}
        if cid == "ob:GR.global-subcriticality":
            ok = scope.get("certificate_scope") == "global" and claim.get("declared_status") == "O"
            checks.append({
                "id": "gr.scope.global-frontier-remains-global-open",
                "status": "pass" if ok else "fail",
                "observed": {"certificate_scope": scope.get("certificate_scope"), "declared_status": claim.get("declared_status")},
                "expected": {"certificate_scope": "global", "declared_status": "O"},
                "message": "The GR global frontier must remain open at global scope.",
            })
        elif cid.startswith("thm:GR") or cid.startswith("ob:GR"):
            if cid != "status:GR":
                ok = scope.get("certificate_scope") in {"domain-bounded", "global"}
                checks.append({
                    "id": f"gr.scope.{cid}",
                    "status": "pass" if ok else "fail",
                    "observed": scope.get("certificate_scope"),
                    "expected": "domain-bounded or explicitly global for the terminal frontier",
                    "message": "GR pilot claims must carry explicit certificate scope.",
                })
    return checks


def main() -> int:
    claims = load_claims()
    equivalence = load_json(REPORTS / "gr_successor_equivalence_report.json")
    compile_check = load_json(REPORTS / "compile_check_report.json")
    gr_compile = (compile_check.get("targets") or {}).get("gr_branch_successor", {})
    manifest_entries, prose_issues = prose_manifest(claims)
    render_checks = rendered_presence_checks(claims)
    scope_checks = dependency_scope_checks(claims)

    checks: List[Dict[str, Any]] = [
        {
            "id": "gr.l2.equivalence-report-passed",
            "status": "pass" if equivalence.get("status") == "passed" else "fail",
            "observed": equivalence.get("status"),
            "expected": "passed",
            "message": "Base GR successor equivalence report must pass before L2 hardening can pass.",
        },
        {
            "id": "gr.l2.compile-passed",
            "status": "pass" if gr_compile.get("status") == "passed" else "fail",
            "observed": gr_compile.get("status"),
            "expected": "passed",
            "message": "GR successor pilot PDF must compile and render.",
        },
        {
            "id": "gr.l2.posture-preserved",
            "status": "pass" if equivalence.get("posture") == EXPECTED_POSTURE else "fail",
            "observed": equivalence.get("posture"),
            "expected": EXPECTED_POSTURE,
            "message": "GR pilot posture must remain domain-bounded CERT-CLOSE.",
        },
        {
            "id": "gr.l2.frontier-preserved",
            "status": "pass" if equivalence.get("active_frontiers") == EXPECTED_FRONTIERS else "fail",
            "observed": equivalence.get("active_frontiers"),
            "expected": EXPECTED_FRONTIERS,
            "message": "GR global-subcriticality frontier must remain active.",
        },
        {
            "id": "gr.l2.no-supersession",
            "status": "pass" if equivalence.get("supersession_effect") == EXPECTED_NO_SUPERSESSION else "fail",
            "observed": equivalence.get("supersession_effect"),
            "expected": EXPECTED_NO_SUPERSESSION,
            "message": "L2 GR pilot must not supersede the canonical GR Branch Book.",
        },
        {
            "id": "gr.l2.prose-files-present",
            "status": "pass" if not prose_issues else "fail",
            "observed": len(prose_issues),
            "expected": 0,
            "message": "Every generated GR pilot claim must have non-empty human-authored body text; proof files are checked when declared.",
            "details": prose_issues,
        },
    ] + render_checks + scope_checks

    failed = [c for c in checks if c.get("status") == "fail"]
    report = {
        "status": "failed" if failed else "passed",
        "pilot_level": "L2-hardened",
        "claim_count": len(GR_ORDER),
        "prose_file_count": len(manifest_entries),
        "failed_count": len(failed),
        "checks": checks,
        "prose_issues": prose_issues,
        "supersession_effect": "none; pilot shell only",
    }

    with (REPORTS / "gr_l2_hardening_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with (REPORTS / "gr_prose_preservation_manifest.json").open("w", encoding="utf-8") as f:
        json.dump({"entries": manifest_entries}, f, indent=2)

    lines = [
        "# GR L2 Hardening Report",
        "",
        f"**Status:** {report['status']}",
        f"**Pilot level:** {report['pilot_level']}",
        f"**Claims checked:** {report['claim_count']}",
        f"**Prose files cataloged:** {report['prose_file_count']}",
        f"**Failed checks:** {report['failed_count']}",
        f"**Supersession effect:** {report['supersession_effect']}",
        "",
        "## Checks",
        "",
        "| Check | Status | Observed | Expected |",
        "|---|---:|---|---|",
    ]
    for c in checks:
        lines.append(f"| `{c['id']}` | **{c['status']}** | {c.get('observed')} | {c.get('expected')} |")
    lines += [
        "",
        "## Prose Preservation Manifest",
        "",
        "| Claim | Field | Path | Size | SHA-256 |",
        "|---|---|---|---:|---|",
    ]
    for e in manifest_entries:
        lines.append(f"| `{e['claim_id']}` | {e['field']} | `{e['path']}` | {e['size_bytes']} | `{e['sha256']}` |")
    (TABLES / "gr_l2_hardening_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": report["status"], "failed_count": len(failed), "prose_files": len(manifest_entries)}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
