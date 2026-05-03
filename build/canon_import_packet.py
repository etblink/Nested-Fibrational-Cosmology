from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"
CANON = ROOT / "canon"

TEX.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)


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



def load_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted((ROOT / "claims").rglob("*.yaml")):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            claims[cid] = data
    return claims


def load_release_postures() -> Dict[str, str]:
    release = load_yaml(CANON / "releases" / "L_plus_4.yaml")
    return release.get("effective_branch_postures", {})

def tex_escape(value: Any) -> str:
    s = "" if value is None else str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in s)


def longtable(label: str, caption: str, headers: List[str], rows: List[List[Any]]) -> str:
    cols = "p{0.23\\linewidth}p{0.17\\linewidth}p{0.17\\linewidth}p{0.17\\linewidth}p{0.18\\linewidth}"[:]
    # Use a generic p-column layout sized by number of columns.
    if len(headers) == 2:
        colspec = r"p{0.35\linewidth}p{0.55\linewidth}"
    elif len(headers) == 3:
        colspec = r"p{0.28\linewidth}p{0.28\linewidth}p{0.34\linewidth}"
    elif len(headers) == 4:
        colspec = r"p{0.23\linewidth}p{0.18\linewidth}p{0.22\linewidth}p{0.27\linewidth}"
    else:
        colspec = r"p{0.20\linewidth}p{0.15\linewidth}p{0.18\linewidth}p{0.18\linewidth}p{0.19\linewidth}"

    lines = [
        rf"\begin{{longtable}}{{{colspec}}}",
        rf"\caption{{{tex_escape(caption)}}}\label{{{label}}}\\",
        " & ".join(rf"\textbf{{{tex_escape(h)}}}" for h in headers) + r"\\",
        r"\hline",
        r"\endfirsthead",
        " & ".join(rf"\textbf{{{tex_escape(h)}}}" for h in headers) + r"\\",
        r"\hline",
        r"\endhead",
    ]
    if rows:
        for row in rows:
            padded = list(row) + [""] * (len(headers) - len(row))
            lines.append(" & ".join(tex_escape(cell) for cell in padded[:len(headers)]) + r"\\")
    else:
        lines.append(r"\multicolumn{" + str(len(headers)) + r"}{l}{No rows generated.}\\")
    lines.append(r"\end{longtable}")
    return "\n".join(lines)


def main() -> int:
    schema = load_yaml(CANON / "schema_version.yaml").get("schema", {})
    summary = load_json(REPORTS / "audit_summary.json")
    digest = load_json(REPORTS / "governance_digest.json")
    quality = load_json(REPORTS / "quality_gate_report.json")
    branch_report = load_json(REPORTS / "branch_posture_report.json")
    release_diff = load_json(REPORTS / "release_diff_report.json")
    regression = load_json(REPORTS / "regression_test_report.json")
    computed = load_json(REPORTS / "computed_statuses.json")
    audit = load_json(REPORTS / "audit_report.json")
    claims = load_claims()
    release_postures = load_release_postures()

    branch_rows: List[List[Any]] = []
    for cid, info in sorted(computed.items()):
        if cid.startswith("status:"):
            branch = cid.split(":", 1)[1]
            declared = claims.get(cid, {}).get("declared_status", "")
            computed_value = info.get("effective_status", "")
            release_value = release_postures.get(branch, "")
            result = "match" if release_value == computed_value else "mismatch" if release_value else "computed"
            branch_rows.append([branch, declared, computed_value, release_value, result])

    open_rows: List[List[Any]] = []
    for item in digest.get("active_open_items", []):
        info = computed.get(item, {})
        open_rows.append([
            item,
            info.get("effective_status", "O"),
            info.get("source", ""),
            info.get("reason", ""),
        ])

    audit_rows: List[List[Any]] = []
    for issue in audit.get("issues", []):
        audit_rows.append([
            issue.get("severity", ""),
            issue.get("type", ""),
            issue.get("id", issue.get("branch", "")),
            issue.get("reason", issue.get("alias", "")),
        ])

    release_rows: List[List[Any]] = []
    for change in release_diff.get("changes", []):
        basis = ", ".join(str(item) for item in change.get("basis", []))
        release_rows.append([
            change.get("change_type", ""),
            change.get("item", change.get("branch", "")),
            change.get("before", ""),
            change.get("after", ""),
            basis,
        ])

    quality_rows: List[List[Any]] = []
    for gate in quality.get("gates", []):
        quality_rows.append([
            gate.get("id", ""),
            gate.get("severity", ""),
            gate.get("status", ""),
            gate.get("observed", ""),
            gate.get("expected", ""),
        ])

    appendix = [
        "% Auto-generated by build/canon_import_packet.py. Do not edit by hand.",
        "% Import this file from a canon appendix/status packet.",
        rf"\section{{NFC Governance Status Packet}}",
        rf"\label{{sec:nfc-governance-status-packet}}",
        "",
        "This appendix fragment is generated from the governance registry. It is intended",
        "for canon import, not as a replacement for theorem prose.",
        "",
        rf"\paragraph{{Schema.}} Version {tex_escape(schema.get('version', 'unknown'))}.",
        rf"\paragraph{{Build.}} Claims: {tex_escape(summary.get('claims_count', 0))}; "
        rf"computed statuses: {tex_escape(summary.get('computed_statuses', 0))}; "
        rf"errors: {tex_escape(summary.get('errors', 0))}; "
        rf"warnings: {tex_escape(summary.get('warnings', 0))}.",
        "",
        longtable(
            "tab:nfc-branch-postures",
            "Branch posture reconciliation",
            ["Branch", "Declared", "Computed", "Release", "Result"],
            branch_rows,
        ),
        "",
        longtable(
            "tab:nfc-active-open-items",
            "Active open items under governance trace",
            ["ID", "Status", "Source", "Reason"],
            open_rows,
        ),
        "",
        longtable(
            "tab:nfc-audit-issues",
            "Current governance audit issues",
            ["Severity", "Type", "ID/Branch", "Reason"],
            audit_rows,
        ),
        "",
        longtable(
            "tab:nfc-release-diff",
            "Release-diff events",
            ["Type", "ID/Branch", "From", "To", "Basis"],
            release_rows,
        ),
        "",
        longtable(
            "tab:nfc-quality-gates",
            "Quality gate report",
            ["Gate", "Severity", "Status", "Observed", "Expected"],
            quality_rows,
        ),
    ]

    appendix_path = TEX / "canon_governance_appendix.tex"
    appendix_path.write_text("\n\n".join(appendix) + "\n", encoding="utf-8")

    standalone = [
        "% Auto-generated standalone wrapper for the NFC governance appendix.",
        r"\documentclass{article}",
        r"\usepackage[margin=0.8in]{geometry}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{longtable}",
        r"\usepackage{array}",
        r"\usepackage{hyperref}",
        r"\begin{document}",
        r"\input{canon_governance_appendix.tex}",
        r"\end{document}",
    ]
    standalone_path = TEX / "canon_governance_appendix_standalone.tex"
    standalone_path.write_text("\n".join(standalone) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": schema.get("version"),
        "purpose": "canon-import-pilot",
        "files": [
            str(appendix_path.relative_to(ROOT)),
            str(standalone_path.relative_to(ROOT)),
        ],
        "required_latex_packages": ["longtable", "array", "hyperref"],
        "tables": {
            "branch_postures": len(branch_rows),
            "active_open_items": len(open_rows),
            "audit_issues": len(audit_rows),
            "release_diff_events": len(release_rows),
            "quality_gates": len(quality_rows),
        },
        "status": "generated",
    }
    with (REPORTS / "canon_import_manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    md = [
        "# Canon Import Manifest",
        "",
        f"**Schema version:** {manifest['schema_version']}",
        f"**Status:** {manifest['status']}",
        "",
        "## Generated files",
        "",
    ]
    for file in manifest["files"]:
        md.append(f"- `{file}`")
    md += [
        "",
        "## Required LaTeX packages",
        "",
    ]
    for pkg in manifest["required_latex_packages"]:
        md.append(f"- `{pkg}`")
    md += [
        "",
        "## Table row counts",
        "",
        "| Table | Rows |",
        "|---|---:|",
    ]
    for key, count in manifest["tables"].items():
        md.append(f"| `{key}` | {count} |")
    (TABLES / "canon_import_manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "generated",
        "files": manifest["files"],
        "tables": manifest["tables"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
