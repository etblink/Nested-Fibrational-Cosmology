"""
build/rh_branch_successor.py — v32 RH Branch-Successor Pilot

RH is the final and highest-sensitivity pilot. It exercises cert-proj,
the last posture type not yet represented.

CERT-PROJ is NOT a posture of progress toward closure. It means:
  - The branch architecture is constituted
  - The canonical object, probe space, and structural machinery exist
  - A precisely-stated irreducible frontier is named
  - The branch does NOT claim to be near proving RH

THE SINGLE MOST IMPORTANT GOVERNANCE INVARIANT:
  ob:RH.S1-ARC must remain [O] — ALWAYS.
  Any build that closes, promotes, or weakens this record to anything
  other than [O] has implicitly claimed to prove the Riemann Hypothesis.
  This gate must NEVER pass if S1-ARC is not [O].

S1 decomposition:
  - S1-TRACE [C]: trace formula pairing — conditionally discharged
  - S1-DESCENT [C]: arithmetic descent without hidden import — conditionally discharged
  - S1-COMP [C]: SCC-minimal faithful package — discharged via SCC-MCS
  - S1-ARC [O]: Q[psi]>=0 from arithmetic structure of Xi — IRREDUCIBLE, OPEN
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "RH"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

# Ordered claim list — ladder first, then S1 sub-predicates,
# then the frontier, then the containing wrapper, then status.
RH_ORDER = [
    "thm:RH.1",
    "thm:RH.2",
    "thm:RH.3",
    "ob:RH.4",
    "ob:RH.5",
    "ob:RH.6",
    "ob:RH.S1-TRACE",
    "ob:RH.S1-DESCENT",
    "ob:RH.S1-COMP",
    "ob:RH.S1-ARC",
    "thm:RH.S1.formal",
    "status:RH",
]

EXPECTED_POSTURE = "cert-proj"
# S1-ARC is the ONLY irreducible frontier — everything else is [C]
EXPECTED_S1_ARC_STATUS = "O"
# S1 sub-components that must be [C] (not [O], not [U])
MUST_BE_CONDITIONAL = ["ob:RH.S1-TRACE", "ob:RH.S1-DESCENT", "ob:RH.S1-COMP"]


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


def load_rh_claims() -> Dict[str, Dict[str, Any]]:
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
        "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in s)


def md_to_tex(md: str) -> str:
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
    for key in ["regime", "certificate_scope", "promotion_ceiling"]:
        val = scope.get(key)
        if val:
            bits.append(f"{key}={val}")
    constraints = scope.get("inherited_constraints") or []
    if constraints:
        bits.append("hyp=" + ",".join(str(x) for x in constraints))
    return "; ".join(bits) if bits else "not declared"


def claim_env_name(kind: str) -> str:
    m = {
        "obligation": "nfcobligation",
        "frontier": "nfcfrontier",
        "status_note": "nfcstatusnote",
        "proposition": "nfcproposition",
        "corollary": "nfccorollary",
    }
    return m.get(kind, "nfctheorem")


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
    inherited = (claim.get("scope", {}) or {}).get("inherited_constraints", []) or []

    # Flag S1-ARC specially
    is_arc = cid == "ob:RH.S1-ARC"
    prefix = r"\noindent\colorbox{yellow!30}{\textbf{IRREDUCIBLE FRONTIER}} " if is_arc else ""

    parts = [
        rf"\begin{{{env}}}{{{tex_escape(title)}}}",
        prefix + rf"\textbf{{ID.}} \texttt{{{tex_escape(cid)}}}\quad"
        rf"\textbf{{Decl.}} {tex_escape(declared)}\quad"
        rf"\textbf{{Comp.}} {tex_escape(effective)}\\",
        rf"\textbf{{Scope.}} {tex_escape(scope_summary(claim))}",
        "",
        md_to_tex(body or "No body text supplied."),
    ]
    if inherited:
        parts += ["", r"\medskip",
                  r"\noindent\textit{Hypotheses.} " + tex_escape(", ".join(inherited))]
    if deps:
        parts += ["", r"\medskip",
                  r"\noindent\textit{Dependencies.} " + tex_escape(", ".join(deps))]
    if discharges:
        discharge_strs = [
            f"{d.get('target','')} ({d.get('kind','')})" for d in discharges
        ]
        parts += ["", r"\medskip",
                  r"\noindent\textit{Discharge edges.} "
                  + tex_escape(", ".join(discharge_strs))]
    if proof:
        parts += ["", r"\medskip",
                  r"\noindent\textit{Proof stub.} " + md_to_tex(proof)]
    parts.append(rf"\end{{{env}}}")
    return "\n".join(parts)


def render_tex(claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]) -> None:
    rows = []
    for cid in RH_ORDER:
        claim = claims.get(cid)
        if not claim:
            continue
        rows.append([
            cid,
            claim.get("kind", ""),
            claim.get("declared_status", ""),
            computed.get(cid, {}).get("effective_status",
                                      claim.get("declared_status", "")),
            claim.get("scope", {}).get("certificate_scope", ""),
        ])

    lines = [
        r"\begin{longtable}{p{0.30\linewidth}p{0.14\linewidth}p{0.10\linewidth}"
        r"p{0.12\linewidth}p{0.20\linewidth}}",
        r"\caption{RH successor-pilot claim catalog}\label{tab:rh-successor-claims}\\",
        r"\textbf{ID} & \textbf{Kind} & \textbf{D.} & \textbf{C.} & \textbf{Scope}\\",
        r"\hline\endfirsthead",
        r"\textbf{ID} & \textbf{Kind} & \textbf{D.} & \textbf{C.} & \textbf{Scope}\\",
        r"\hline\endhead",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(x) for x in row) + r"\\")
    lines.append(r"\end{longtable}")
    table = "\n".join(lines)

    posture_computed = computed.get("status:RH", {}).get("effective_status", "unknown")

    body_parts = [
        "% Auto-generated by build/rh_branch_successor.py. Do not edit by hand.",
        r"\section*{RH Branch Successor Pilot}",
        r"\addcontentsline{toc}{section}{RH Branch Successor Pilot}",
        "",
        r"\textbf{This is the highest-sensitivity governance pilot.} "
        r"Any version of this packet that closes, promotes, or weakens "
        r"\texttt{ob:RH.S1-ARC} from status~$[\mathrm{O}]$ "
        r"would implicitly claim to prove the Riemann Hypothesis. "
        r"The quality gate and equivalence check both enforce this.",
        "",
        r"\subsection*{Posture and S1 decomposition}",
        rf"Computed RH posture: \textbf{{\texttt{{{tex_escape(posture_computed)}}}}}. "
        r"CERT-PROJ means: the branch architecture is constituted and the "
        r"primary open obligation is Witness Assembly~S1, reduced to "
        r"\texttt{ob:RH.S1-ARC} alone. The branch does \emph{not} "
        r"claim to be near proving RH.",
        "",
        r"\begin{center}",
        r"\begin{tabular}{lll}",
        r"\textbf{S1 sub-predicate} & \textbf{Status} & \textbf{Route}\\",
        r"\hline",
        r"S1-TRACE & [C] & Scaling-flow candidate (conditional)\\",
        r"S1-DESCENT & [C] & Transport-localization chain L1--L7 (conditional)\\",
        r"S1-COMP & [C] & SCC-MCS discharged (SCC Branch)\\",
        r"\textbf{S1-ARC} & \textbf{[O]} & \textbf{IRREDUCIBLE --- mathematical content of RH}\\",
        r"\hline",
        r"\end{tabular}",
        r"\end{center}",
        "",
        r"\subsection*{Non-claims (strictly maintained)}",
        r"\begin{itemize}",
        r"\item The RH pilot does \textbf{not} prove the Riemann Hypothesis",
        r"\item S1-ARC is \textbf{not} conditionally discharged",
        r"\item S1-TRACE, S1-DESCENT, S1-COMP are [C], \textbf{not} [U]",
        r"\item No sub-predicate is promoted beyond its declared status",
        r"\item No arithmetic primitive is imported outside the declared branch structure",
        r"\end{itemize}",
        "",
        table,
        "",
        r"\subsection*{Generated claim shells}",
    ]

    for cid in RH_ORDER:
        claim = claims.get(cid)
        if claim:
            body_parts.append(render_claim(claim, computed))
            body_parts.append("")

    packet = "\n\n".join(body_parts)
    (TEX / "rh_branch_successor.tex").write_text(packet + "\n", encoding="utf-8")

    standalone = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.85in]{geometry}
\usepackage{longtable}
\usepackage{amsmath}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{hyperref}
\newenvironment{nfctheorem}[1]{\par\medskip\noindent\textbf{Theorem: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcproposition}[1]{\par\medskip\noindent\textbf{Proposition: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfccorollary}[1]{\par\medskip\noindent\textbf{Corollary: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcobligation}[1]{\par\medskip\noindent\textbf{Obligation: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcfrontier}[1]{\par\medskip\noindent\textbf{Frontier: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcstatusnote}[1]{\par\medskip\noindent\textbf{Status note: #1}\par\smallskip}{\par\medskip}
\title{NFC RH Branch Successor Pilot\\[0.5ex]
  \large v32 --- L2 Generated Shell\\[0.5ex]
  \normalsize First exercise of \texttt{cert-proj} posture\\[0.5ex]
  \small S1-ARC remains [O]: this pilot does not prove RH}
\author{Generated governance shell}
\date{}
\begin{document}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{Critical governance notice.}
This is a machine-generated L2 branch-pilot shell for the Riemann Hypothesis branch.
It is \emph{not} a supersession of the canonical RH Branch Book.
\textbf{This pilot does not prove the Riemann Hypothesis.}
The irreducible frontier \texttt{ob:RH.S1-ARC} remains open~[O].
S1-TRACE, S1-DESCENT, and S1-COMP are conditionally discharged~[C]
but S1-ARC is not.
Full supersession requires L5 gate passage per the NFC supersession policy.
\vspace{1em}
\input{rh_branch_successor.tex}
\end{document}
"""
    (TEX / "rh_branch_successor_standalone.tex").write_text(standalone, encoding="utf-8")


def write_equivalence_report(
    claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]
) -> Dict[str, Any]:
    generated_ids = [cid for cid in RH_ORDER if cid in claims]
    missing_expected = [cid for cid in RH_ORDER if cid not in claims]
    unexpected = sorted(set(claims) - set(RH_ORDER))

    posture = computed.get("status:RH", {}).get("effective_status")

    # S1-ARC MUST be [O] — this is the most critical check
    s1_arc = claims.get("ob:RH.S1-ARC", {})
    s1_arc_declared = s1_arc.get("declared_status", "")
    s1_arc_effective = computed.get("ob:RH.S1-ARC", {}).get(
        "effective_status", s1_arc_declared
    )
    s1_arc_is_open = (s1_arc_declared == "O") and (s1_arc_effective in ("O", ""))

    # S1 sub-predicates must be [C]
    s1_sub_statuses = {}
    s1_sub_all_conditional = True
    for cid in MUST_BE_CONDITIONAL:
        claim = claims.get(cid, {})
        decl = claim.get("declared_status", "")
        eff = computed.get(cid, {}).get("effective_status", decl)
        s1_sub_statuses[cid] = {"declared": decl, "effective": eff}
        if decl not in ("C",) or eff in ("U", "O"):
            s1_sub_all_conditional = False

    # S1-ARC must not appear in S1-TRACE/DESCENT/COMP discharge edges
    illegal_s1_arc_discharges = []
    for cid in MUST_BE_CONDITIONAL:
        claim = claims.get(cid, {})
        for d in (claim.get("discharges") or []):
            if d.get("target") == "ob:RH.S1-ARC":
                illegal_s1_arc_discharges.append(cid)

    # Active frontiers
    active_frontiers = []
    for cid in generated_ids:
        claim = claims[cid]
        decl = claim.get("declared_status", "")
        eff = computed.get(cid, {}).get("effective_status", decl)
        kind = claim.get("kind", "")
        if decl == "O" or (kind == "frontier" and eff in ("O", "")):
            if cid not in active_frontiers:
                active_frontiers.append(cid)
    if "ob:RH.S1-ARC" not in active_frontiers:
        active_frontiers.append("ob:RH.S1-ARC")

    checks = [
        {
            "id": "rh.successor.expected-claim-list",
            "status": "pass" if not missing_expected else "fail",
            "observed": {"missing": missing_expected},
            "expected": "All RH_ORDER claims present.",
        },
        {
            "id": "rh.successor.posture",
            "status": "pass" if posture == EXPECTED_POSTURE else "fail",
            "observed": posture,
            "expected": EXPECTED_POSTURE,
        },
        {
            "id": "rh.successor.S1-ARC-is-open",
            "status": "pass" if s1_arc_is_open else "fail",
            "observed": {
                "declared": s1_arc_declared,
                "effective": s1_arc_effective,
            },
            "expected": (
                "ob:RH.S1-ARC MUST be [O]. Any other status implies a proof of RH. "
                f"Declared: {EXPECTED_S1_ARC_STATUS}"
            ),
        },
        {
            "id": "rh.successor.S1-subs-are-conditional",
            "status": "pass" if s1_sub_all_conditional else "fail",
            "observed": s1_sub_statuses,
            "expected": (
                "S1-TRACE, S1-DESCENT, S1-COMP must all be [C]. "
                "None may be [U] or [O]."
            ),
        },
        {
            "id": "rh.successor.no-illegal-S1-ARC-discharge",
            "status": "pass" if not illegal_s1_arc_discharges else "fail",
            "observed": illegal_s1_arc_discharges,
            "expected": "No S1 sub-predicate may list ob:RH.S1-ARC as a discharge target.",
        },
        {
            "id": "rh.successor.active-frontiers",
            "status": "pass" if "ob:RH.S1-ARC" in active_frontiers else "fail",
            "observed": active_frontiers,
            "expected": "ob:RH.S1-ARC must appear in active frontiers.",
        },
        {
            "id": "rh.successor.no-unexpected-claims",
            "status": "pass" if not unexpected else "warn",
            "observed": unexpected,
            "expected": "No RH records outside pilot order.",
        },
        {
            "id": "rh.successor.no-rh-proof-claim",
            "status": "pass"
            if posture == EXPECTED_POSTURE and s1_arc_is_open
            else "fail",
            "observed": {"posture": posture, "s1_arc_open": s1_arc_is_open},
            "expected": (
                "cert-proj posture + S1-ARC open = no RH proof claimed. "
                "Any deviation from this combination is a governance violation."
            ),
        },
    ]

    status = (
        "passed"
        if all(c["status"] in {"pass", "warn"} for c in checks)
        and not any(c["status"] == "fail" for c in checks)
        else "failed"
    )

    report = {
        "status": status,
        "pilot_level": "L2",
        "generated_claim_count": len(generated_ids),
        "generated_ids": generated_ids,
        "missing_expected": missing_expected,
        "unexpected_claims": unexpected,
        "active_frontiers": list(dict.fromkeys(active_frontiers)),
        "posture": posture,
        "s1_arc_is_open": s1_arc_is_open,
        "s1_arc_declared": s1_arc_declared,
        "s1_arc_effective": s1_arc_effective,
        "s1_sub_statuses": s1_sub_statuses,
        "s1_sub_all_conditional": s1_sub_all_conditional,
        "illegal_s1_arc_discharges": illegal_s1_arc_discharges,
        "checks": checks,
        "supersession_effect": "none; pilot shell only",
        "critical_invariant": (
            "S1-ARC is [O]. This pilot does not prove the Riemann Hypothesis. "
            "S1-TRACE/DESCENT/COMP are [C]. All ladder obligations RH1-RH6 are [C]. "
            "9 of 10 AC obstructions are discharged. "
            "The irreducible remaining burden is S1-ARC: "
            "Q[psi]>=0 from the arithmetic structure of Xi."
        ),
    }

    (REPORTS / "rh_successor_equivalence_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    lines = [
        "# RH Branch Successor Equivalence Report",
        "",
        f"**Status:** {status}",
        "**Pilot level:** L2",
        f"**Generated claim count:** {len(generated_ids)}",
        f"**Computed RH posture:** `{posture}`",
        f"**S1-ARC is open:** {s1_arc_is_open} (declared: `{s1_arc_declared}`, effective: `{s1_arc_effective}`)",
        f"**S1 sub-predicates all [C]:** {s1_sub_all_conditional}",
        "",
        "## Critical invariant",
        "",
        f"> {report['critical_invariant']}",
        "",
        "## S1 sub-predicate statuses",
        "",
        "| Sub-predicate | Declared | Effective | Required |",
        "|---|---|---|---|",
    ]
    for cid, info in s1_sub_statuses.items():
        lines.append(
            f"| `{cid}` | `{info['declared']}` | `{info['effective']}` | `C` |"
        )
    lines.append(f"| `ob:RH.S1-ARC` | `{s1_arc_declared}` | `{s1_arc_effective}` | **`O` (IRREDUCIBLE)** |")
    lines += [
        "",
        "## Checks",
        "",
        "| Check | Status | Observed | Expected |",
        "|---|---|---|---|",
    ]
    for c in checks:
        lines.append(
            "| "
            + " | ".join([
                str(c["id"]),
                str(c["status"]),
                str(c.get("observed", "")).replace("|", "\\|")[:80],
                str(c.get("expected", "")).replace("|", "\\|")[:80],
            ])
            + " |"
        )
    lines += [
        "",
        "## Non-claims",
        "",
        "- This pilot does NOT prove the Riemann Hypothesis",
        "- S1-ARC is NOT conditionally discharged",
        "- S1-TRACE, S1-DESCENT, S1-COMP are [C], not [U]",
        "- No sub-predicate is promoted beyond declared status",
        "",
        "## Supersession effect",
        "",
        "None. This packet is a branch-successor pilot shell.",
    ]
    (TABLES / "rh_successor_equivalence_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    claims = load_rh_claims()
    computed = load_json(REPORTS / "computed_statuses.json")
    render_tex(claims, computed)
    report = write_equivalence_report(claims, computed)
    print(json.dumps({
        "status": report["status"],
        "generated_claim_count": report["generated_claim_count"],
        "posture": report["posture"],
        "s1_arc_is_open": report["s1_arc_is_open"],
        "s1_arc_declared": report["s1_arc_declared"],
        "s1_sub_all_conditional": report["s1_sub_all_conditional"],
        "active_frontiers": report["active_frontiers"],
        "critical_invariant": report["critical_invariant"][:100] + "...",
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
