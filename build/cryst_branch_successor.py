
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "CRYST"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

CRYST_ORDER = [
    "thm:CRYST.END",
    "ob:CRYST.phase-problem",
    "status:CRYST",
]

EXPECTED_FRONTIERS: List[str] = ["ob:CRYST.phase-problem"]
EXPECTED_POSTURE = "conditional-cert-close"


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


def load_cryst_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(CLAIMS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            data["_path"] = str(path.relative_to(ROOT))
            claims[cid] = data
    return claims


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


def md_to_tex(md: str) -> str:
    """Tiny conservative Markdown-to-TeX converter for pilot stubs."""
    lines: List[str] = []
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            lines.append("")
            continue
        if line.startswith("# "):
            lines.append(r"\paragraph{" + tex_escape(line[2:].strip()) + "}")
        elif line.startswith("## "):
            lines.append(r"\subparagraph{" + tex_escape(line[3:].strip()) + "}")
        elif line.startswith("- "):
            lines.append(r"\noindent\textbullet{} " + tex_escape(line[2:].strip()) + r"\\")
        else:
            lines.append(tex_escape(line))
    return "\n".join(lines)


def scope_summary(claim: Dict[str, Any]) -> str:
    scope = claim.get("scope", {}) or {}
    bits = []
    for key in ["regime", "domain", "certificate_scope", "continuum_license", "promotion_ceiling"]:
        val = scope.get(key)
        if val:
            bits.append(f"{key}={val}")
    constraints = scope.get("inherited_constraints") or []
    if constraints:
        bits.append("constraints=" + ",".join(str(x) for x in constraints))
    return "; ".join(bits) if bits else "scope not declared"


def claim_env_name(kind: str) -> str:
    if kind == "obligation":
        return "nfcobligation"
    if kind == "frontier":
        return "nfcfrontier"
    if kind == "status_note":
        return "nfcstatusnote"
    return "nfctheorem"


def render_claim(claim: Dict[str, Any], computed: Dict[str, Any]) -> str:
    cid = claim["id"]
    kind = claim.get("kind", "")
    env = claim_env_name(kind)
    title = claim.get("title", cid)
    declared = claim.get("declared_status", "")
    effective = computed.get(cid, {}).get("effective_status", declared)

    body_path = claim.get("body_file")
    body = ""
    if body_path:
        p = ROOT / body_path
        body = p.read_text(encoding="utf-8") if p.exists() else ""
    proof_path = claim.get("proof_file")
    proof = ""
    if proof_path:
        p = ROOT / proof_path
        if p.exists():
            proof = p.read_text(encoding="utf-8")

    deps_raw = claim.get("dependencies", {})
    deps = deps_raw.get("requires", []) if isinstance(deps_raw, dict) else deps_raw or []
    discharges = claim.get("discharges", []) or []

    parts = [
        rf"\begin{{{env}}}{{{tex_escape(title)}}}",
        rf"\textbf{{Machine ID.}} \texttt{{{tex_escape(cid)}}}\\",
        rf"\textbf{{Declared status.}} {tex_escape(declared)}\quad \textbf{{Computed status.}} {tex_escape(effective)}\\",
        rf"\textbf{{Scope.}} {tex_escape(scope_summary(claim))}",
        "",
        md_to_tex(body or "No body text supplied in pilot source."),
    ]
    if deps:
        parts += ["", r"\medskip", r"\noindent\textit{Dependencies.} " + tex_escape(", ".join(deps))]
    if discharges:
        targets = [d.get("target", "") for d in discharges]
        parts += ["", r"\medskip", r"\noindent\textit{Discharge edges.} " + tex_escape(", ".join(targets))]
    if proof:
        parts += ["", r"\medskip", r"\noindent\textit{Proof stub.} " + md_to_tex(proof)]
    parts.append(rf"\end{{{env}}}")
    return "\n".join(parts)


def render_tex(claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]) -> None:
    rows = []
    for cid in CRYST_ORDER:
        claim = claims.get(cid)
        if not claim:
            continue
        rows.append([
            cid,
            claim.get("kind", ""),
            claim.get("declared_status", ""),
            computed.get(cid, {}).get("effective_status", claim.get("declared_status", "")),
            claim.get("scope", {}).get("certificate_scope", ""),
        ])

    lines = [
        r"\begin{longtable}{p{0.32\linewidth}p{0.18\linewidth}p{0.12\linewidth}p{0.15\linewidth}p{0.13\linewidth}}",
        r"\caption{CRYST successor-pilot claim catalog}\label{tab:cryst-successor-claims}\\",
        r"\textbf{ID} & \textbf{Kind} & \textbf{Declared} & \textbf{Computed} & \textbf{Scope}\\",
        r"\hline",
        r"\endfirsthead",
        r"\textbf{ID} & \textbf{Kind} & \textbf{Declared} & \textbf{Computed} & \textbf{Scope}\\",
        r"\hline",
        r"\endhead",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(x) for x in row) + r"\\")
    lines.append(r"\end{longtable}")
    table = "\n".join(lines)

    body_parts = [
        "% Auto-generated by build/cryst_branch_successor.py. Do not edit by hand.",
        r"\section*{CRYST Branch Successor Pilot}",
        r"\addcontentsline{toc}{section}{CRYST Branch Successor Pilot}",
        "",
        "This generated packet is an L2 branch-pilot shell. It is not a supersession of the canonical CRYST Branch Book. It tests the zero-frontier case: a branch may be closed on its declared gauge-response regime without claiming closure over downstream matter-rich spectroscopy.",
        "",
        r"\subsection*{Pilot posture}",
        rf"Computed CRYST posture: \textbf{{{tex_escape(computed.get('status:CRYST', {}).get('effective_status', 'unknown'))}}}. The phase problem remains active and is intentionally preserved in this pilot.",
        "",
        table,
        "",
        r"\subsection*{Generated claim shells}",
    ]
    for cid in CRYST_ORDER:
        claim = claims.get(cid)
        if claim:
            body_parts.append(render_claim(claim, computed))
            body_parts.append("")

    packet = "\n\n".join(body_parts)
    (TEX / "cryst_branch_successor.tex").write_text(packet + "\n", encoding="utf-8")

    standalone = r"""\documentclass[11pt]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage{xcolor}
\newenvironment{nfctheorem}[1]{\par\medskip\noindent\textbf{Theorem-like claim: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcobligation}[1]{\par\medskip\noindent\textbf{Obligation: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcfrontier}[1]{\par\medskip\noindent\textbf{Frontier: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcstatusnote}[1]{\par\medskip\noindent\textbf{Status note: #1}\par\smallskip}{\par\medskip}
\title{NFC CRYST Branch Successor Pilot}
\author{Generated governance shell}
\date{}
\begin{document}
\maketitle
\tableofcontents
\input{cryst_branch_successor.tex}
\end{document}
"""
    (TEX / "cryst_branch_successor_standalone.tex").write_text(standalone, encoding="utf-8")


def write_equivalence_report(claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]) -> Dict[str, Any]:
    generated_ids = [cid for cid in CRYST_ORDER if cid in claims]
    missing_expected = [cid for cid in CRYST_ORDER if cid not in claims]
    unexpected = sorted(set(claims) - set(CRYST_ORDER))
    active_frontiers = [
        cid for cid in generated_ids
        if computed.get(cid, {}).get("effective_status", claims[cid].get("declared_status")) == "O"
    ]
    posture = computed.get("status:CRYST", {}).get("effective_status")
    checks = [
        {
            "id": "cryst.successor.expected-claim-list",
            "status": "pass" if not missing_expected else "fail",
            "observed": {"missing": missing_expected},
            "expected": "All CRYST_ORDER claims are present.",
        },
        {
            "id": "cryst.successor.posture",
            "status": "pass" if posture == EXPECTED_POSTURE else "fail",
            "observed": posture,
            "expected": EXPECTED_POSTURE,
        },
        {
            "id": "cryst.successor.frontier-profile",
            "status": "pass" if sorted(active_frontiers) == sorted(EXPECTED_FRONTIERS) else "fail",
            "observed": active_frontiers,
            "expected": EXPECTED_FRONTIERS,
        },
        {
            "id": "cryst.successor.no-unexpected-claims",
            "status": "pass" if not unexpected else "warn",
            "observed": unexpected,
            "expected": "No branch-local CRYST records outside the pilot order.",
        },
        {
            "id": "cryst.successor.no-phase-problem-erasure",
            "status": "pass" if posture == EXPECTED_POSTURE and "ob:CRYST.phase-problem" in active_frontiers else "fail",
            "observed": {"posture": posture, "active_frontiers": active_frontiers},
            "expected": "Conditional closure is preserved while the phase-problem frontier remains active.",
        },
    ]
    status = "passed" if all(c["status"] in {"pass", "warn"} for c in checks) and not any(c["status"] == "fail" for c in checks) else "failed"
    report = {
        "status": status,
        "pilot_level": "L2",
        "generated_claim_count": len(generated_ids),
        "generated_ids": generated_ids,
        "missing_expected": missing_expected,
        "unexpected_claims": unexpected,
        "active_frontiers": active_frontiers,
        "posture": posture,
        "checks": checks,
        "supersession_effect": "none; pilot shell only",
    }

    (REPORTS / "cryst_successor_equivalence_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "# CRYST Branch Successor Equivalence Report",
        "",
        f"**Status:** {status}",
        f"**Pilot level:** L2",
        f"**Generated claim count:** {len(generated_ids)}",
        f"**Computed CRYST posture:** `{posture}`",
        f"**Active frontiers:** {', '.join(f'`{x}`' for x in active_frontiers) or 'none'}",
        "",
        "## Checks",
        "",
        "| Check | Status | Observed | Expected |",
        "|---|---|---|---|",
    ]
    for c in checks:
        lines.append("| " + " | ".join([
            str(c["id"]),
            str(c["status"]),
            str(c.get("observed", "")).replace("|", "\\|"),
            str(c.get("expected", "")).replace("|", "\\|"),
        ]) + " |")
    lines += [
        "",
        "## Supersession effect",
        "",
        "None. This packet is a branch-successor pilot shell, not a replacement for the canonical CRYST Branch Book.",
    ]
    (TABLES / "cryst_successor_equivalence_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    claims = load_cryst_claims()
    computed = load_json(REPORTS / "computed_statuses.json")
    render_tex(claims, computed)
    report = write_equivalence_report(claims, computed)
    print(json.dumps({
        "status": report["status"],
        "generated_claim_count": report["generated_claim_count"],
        "posture": report["posture"],
        "active_frontiers": report["active_frontiers"],
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
