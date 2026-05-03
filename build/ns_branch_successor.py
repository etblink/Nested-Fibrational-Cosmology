"""
build/ns_branch_successor.py — v31 NS Branch-Successor Pilot

Primary governance function: STALE-POSTURE CORRECTION.

The NS governance repo has been computing frontier-blocked (from the
inference rule: front:NS.main == O → frontier-blocked). But the canonical
NS branch book contains prop:NS-status [C], thm:NS71 [C], and
cor:NS-both-give-endpoint [C] establishing domain-bounded conditional
CERT-CLOSE. The NS preamble is stale. This pilot corrects the posture.

Governance invariants:
  - status:NS = domain-bounded-cert-close  (correcting stale frontier-blocked)
  - front:NS.main = O  (Stage-3 global unconditional = Clay Prize, external)
  - ob:NS.SB2 = C  (conditionally discharged via SCT.6b / Ren.5 chain)
  - ob:NS.bridge-stage2 = O  (partial discharge records stage-boundary progress)
  - Domain-bounded scope: Phase-A/K_0=7/PASS/LS-2
  - NOT claimed: unconditional global regularity, Clay Prize solution
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "NS"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

# Ordered claim list — unconditional foundation first, then conditional chain,
# then discharge theorems, then closure, then status, then live frontier
NS_ORDER = [
    "thm:NS.stage0",
    "thm:NS.stage1",
    "thm:NS.stage2a",
    "thm:NS.stage2b",
    "thm:NS.leray",
    "thm:NS.window-uniformity",
    "thm:NS.6.1",
    "thm:NS.Ren5",
    "thm:NS.SB2-discharged",
    "ob:NS.SB2",
    "ob:NS.bridge-stage2",
    "thm:NS.7.1",
    "cor:NS.domain-bounded-cert-close",
    "prop:NS.status",
    "front:NS.main",
    "status:NS",
]

EXPECTED_POSTURE = "domain-bounded-cert-close"
EXPECTED_ACTIVE_FRONTIERS: List[str] = ["front:NS.main"]
STALE_POSTURE_CORRECTED_FROM = "frontier-blocked"

DOMAIN_BOUNDED_HYPOTHESES = [
    "Phase-A", "K_0=7", "PASS", "LS-2"
]


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


def load_ns_claims() -> Dict[str, Dict[str, Any]]:
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
    for key in ["regime", "domain", "certificate_scope", "promotion_ceiling"]:
        val = scope.get(key)
        if val:
            bits.append(f"{key}={val}")
    constraints = scope.get("inherited_constraints") or []
    if constraints:
        bits.append("hyp=" + ",".join(str(x) for x in constraints))
    return "; ".join(bits) if bits else "scope not declared"


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

    parts = [
        rf"\begin{{{env}}}{{{tex_escape(title)}}}",
        rf"\textbf{{ID.}} \texttt{{{tex_escape(cid)}}}\quad"
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
            f"{d.get('target','')} ({d.get('kind','')})"
            for d in discharges
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
    for cid in NS_ORDER:
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
        r"\caption{NS successor-pilot claim catalog}\label{tab:ns-successor-claims}\\",
        r"\textbf{ID} & \textbf{Kind} & \textbf{D.} & \textbf{C.} & \textbf{Scope}\\",
        r"\hline\endfirsthead",
        r"\textbf{ID} & \textbf{Kind} & \textbf{D.} & \textbf{C.} & \textbf{Scope}\\",
        r"\hline\endhead",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(x) for x in row) + r"\\")
    lines.append(r"\end{longtable}")
    table = "\n".join(lines)

    posture_computed = computed.get("status:NS", {}).get(
        "effective_status", "unknown"
    )

    body_parts = [
        "% Auto-generated by build/ns_branch_successor.py. Do not edit by hand.",
        r"\section*{NS Branch Successor Pilot}",
        r"\addcontentsline{toc}{section}{NS Branch Successor Pilot}",
        "",
        r"\textbf{Primary governance function: stale-posture correction.} "
        r"The NS governance repo has been computing \texttt{frontier-blocked} "
        r"(from the stale inference rule \texttt{front:NS.main == O} "
        r"$\Rightarrow$ \texttt{frontier-blocked}). "
        r"The canonical NS branch book contains "
        r"\texttt{prop:NS-status [C]}, \texttt{thm:NS71 [C]}, and "
        r"\texttt{cor:NS-both-give-endpoint [C]} establishing "
        r"\textbf{domain-bounded conditional CERT-CLOSE}. "
        r"The NS preamble (``frontier-blocked'') is stale relative to the "
        r"later sections of the same canonical file. "
        r"This pilot corrects the posture and records the correction "
        r"as a formal governance finding.",
        "",
        r"\subsection*{Stale-posture correction record}",
        rf"Stale declared posture: \texttt{{{tex_escape(STALE_POSTURE_CORRECTED_FROM)}}}\\",
        rf"Corrected computed posture: \textbf{{\texttt{{{tex_escape(posture_computed)}}}}}\\",
        r"Basis: \texttt{thm:NS.7.1 [C]} $+$ \texttt{thm:NS.6.1 [C]} $+$ "
        r"\texttt{front:NS.main == O}\\",
        r"Source: \texttt{prop:NS-status [C]} in canonical NS Branch Book",
        "",
        r"\subsection*{Domain-bounded closure hypotheses}",
        r"Phase-A, $K_0=7$, PASS, LS-2. "
        r"Removing any hypothesis reopens the domain-bounded closure claim.",
        "",
        r"\subsection*{Active frontier}",
        r"\texttt{front:NS.main}: Stage-3 global unconditional closure "
        r"(Navier-Stokes Clay Millennium Prize Problem). "
        r"This is an \emph{external} frontier outside the current NFC toolkit. "
        r"No admissible discharge mode exists within the current architecture.",
        "",
        r"\subsection*{SB2 and Ren.5 status}",
        r"\texttt{ob:NS.SB2}: conditionally discharged [C] via SCT.6b "
        r"(\texttt{thm:NS.SB2-discharged}).\\",
        r"\texttt{thm:NS.Ren5}: conditionally discharged [C] via sub-lemma chain.",
        "",
        table,
        "",
        r"\subsection*{Generated claim shells}",
    ]

    for cid in NS_ORDER:
        claim = claims.get(cid)
        if claim:
            body_parts.append(render_claim(claim, computed))
            body_parts.append("")

    packet = "\n\n".join(body_parts)
    (TEX / "ns_branch_successor.tex").write_text(packet + "\n", encoding="utf-8")

    standalone = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.85in]{geometry}
\usepackage{longtable}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{xcolor}
\newenvironment{nfctheorem}[1]{\par\medskip\noindent\textbf{Theorem: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcproposition}[1]{\par\medskip\noindent\textbf{Proposition: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfccorollary}[1]{\par\medskip\noindent\textbf{Corollary: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcobligation}[1]{\par\medskip\noindent\textbf{Obligation: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcfrontier}[1]{\par\medskip\noindent\textbf{Frontier: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcstatusnote}[1]{\par\medskip\noindent\textbf{Status note: #1}\par\smallskip}{\par\medskip}
\title{NFC NS Branch Successor Pilot\\[0.5ex]
  \large v31 --- L2 Generated Shell\\[0.5ex]
  \normalsize Stale-Posture Correction: \texttt{frontier-blocked}
  $\Rightarrow$ \texttt{domain-bounded-cert-close}}
\author{Generated governance shell}
\date{}
\begin{document}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{Governance notice.} This is a machine-generated L2
branch-pilot shell. It is \emph{not} a supersession of the canonical
NFC Navier-Stokes Branch Book. The canonical NS branch book remains
the authoritative source. Full supersession requires L5 gate passage.
\vspace{1em}
\input{ns_branch_successor.tex}
\end{document}
"""
    (TEX / "ns_branch_successor_standalone.tex").write_text(standalone, encoding="utf-8")


def write_equivalence_report(
    claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]
) -> Dict[str, Any]:
    generated_ids = [cid for cid in NS_ORDER if cid in claims]
    missing_expected = [cid for cid in NS_ORDER if cid not in claims]
    unexpected = sorted(set(claims) - set(NS_ORDER))

    active_frontiers = [
        cid for cid in generated_ids
        if computed.get(cid, {}).get(
            "effective_status", claims[cid].get("declared_status")
        ) in ("O", "frontier-blocked")
    ]
    # Also catch declared frontier objects
    for cid in generated_ids:
        claim = claims[cid]
        if claim.get("kind") == "frontier" and cid not in active_frontiers:
            decl = claim.get("declared_status", "")
            if decl == "O":
                active_frontiers.append(cid)

    posture = computed.get("status:NS", {}).get("effective_status")

    # Check SB2 is now [C]
    sb2 = claims.get("ob:NS.SB2", {})
    sb2_declared = sb2.get("declared_status", "")
    sb2_discharged = sb2_declared == "C"

    # Check the stale-posture correction
    stale_posture_corrected = posture == EXPECTED_POSTURE

    # Check Stage-3 global frontier preserved
    main_frontier = claims.get("front:NS.main", {})
    main_declared = main_frontier.get("declared_status", "")
    stage3_frontier_preserved = main_declared == "O"

    checks = [
        {
            "id": "ns.successor.expected-claim-list",
            "status": "pass" if not missing_expected else "fail",
            "observed": {"missing": missing_expected},
            "expected": "All NS_ORDER claims present.",
        },
        {
            "id": "ns.successor.posture-correction",
            "status": "pass" if stale_posture_corrected else "fail",
            "observed": posture,
            "expected": (
                f"{EXPECTED_POSTURE} "
                f"(correcting stale {STALE_POSTURE_CORRECTED_FROM})"
            ),
        },
        {
            "id": "ns.successor.frontier-profile",
            "status": "pass"
            if "front:NS.main" in active_frontiers
            else "fail",
            "observed": active_frontiers,
            "expected": ["front:NS.main"],
        },
        {
            "id": "ns.successor.sb2-discharged",
            "status": "pass" if sb2_discharged else "fail",
            "observed": {"declared": sb2_declared},
            "expected": "ob:NS.SB2 must be [C] — conditionally discharged via SCT.6b.",
        },
        {
            "id": "ns.successor.stage3-frontier-preserved",
            "status": "pass" if stage3_frontier_preserved else "fail",
            "observed": {"declared": main_declared},
            "expected": "front:NS.main must remain [O] — Stage-3 global unconditional is external frontier.",
        },
        {
            "id": "ns.successor.no-unexpected-claims",
            "status": "pass" if not unexpected else "warn",
            "observed": unexpected,
            "expected": "No NS records outside pilot order.",
        },
        {
            "id": "ns.successor.no-clay-prize-claim",
            "status": "pass" if posture != "cert-close" and posture != "unconditional-cert-close"
            else "fail",
            "observed": posture,
            "expected": "Must not claim unconditional global regularity or Clay Prize solution.",
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
        "stale_posture_corrected_from": STALE_POSTURE_CORRECTED_FROM,
        "stale_posture_corrected": stale_posture_corrected,
        "sb2_discharged": sb2_discharged,
        "stage3_frontier_preserved": stage3_frontier_preserved,
        "domain_bounded_hypotheses": DOMAIN_BOUNDED_HYPOTHESES,
        "checks": checks,
        "supersession_effect": "none; pilot shell only",
        "governance_finding": (
            "STALE-POSTURE CORRECTION: NS preamble says frontier-blocked but "
            "canonical NS branch book (prop:NS-status, thm:NS71, "
            "cor:NS-both-give-endpoint) establishes domain-bounded conditional "
            "CERT-CLOSE. Pilot corrects the governance repo posture and documents "
            "the NS preamble as requiring a canon maintenance update."
        ),
    }

    (REPORTS / "ns_successor_equivalence_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    lines = [
        "# NS Branch Successor Equivalence Report",
        "",
        f"**Status:** {status}",
        "**Pilot level:** L2",
        f"**Generated claim count:** {len(generated_ids)}",
        f"**Computed NS posture:** `{posture}`",
        f"**Stale posture corrected from:** `{STALE_POSTURE_CORRECTED_FROM}`",
        f"**Stale posture corrected:** {stale_posture_corrected}",
        f"**SB2 discharged:** {sb2_discharged}",
        f"**Stage-3 frontier preserved:** {stage3_frontier_preserved}",
        f"**Active frontiers:** "
        + (", ".join(f"`{x}`" for x in active_frontiers) or "none"),
        "",
        "## Governance finding",
        "",
        f"> {report['governance_finding']}",
        "",
        "## Domain-bounded hypotheses",
        "",
        ", ".join(DOMAIN_BOUNDED_HYPOTHESES),
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
                str(c.get("observed", "")).replace("|", "\\|"),
                str(c.get("expected", "")).replace("|", "\\|"),
            ])
            + " |"
        )
    lines += [
        "",
        "## Supersession effect",
        "",
        "None. This packet is a branch-successor pilot shell.",
        "",
        "## Canon maintenance note",
        "",
        "The NS branch preamble (front block) should be updated to reflect "
        "domain-bounded conditional CERT-CLOSE, correcting the stale "
        "``frontier-blocked'' language. This is a canon editorial task "
        "separate from the governance pilot.",
    ]
    (TABLES / "ns_successor_equivalence_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    claims = load_ns_claims()
    computed = load_json(REPORTS / "computed_statuses.json")
    render_tex(claims, computed)
    report = write_equivalence_report(claims, computed)
    print(json.dumps({
        "status": report["status"],
        "generated_claim_count": report["generated_claim_count"],
        "posture": report["posture"],
        "stale_posture_corrected_from": report["stale_posture_corrected_from"],
        "stale_posture_corrected": report["stale_posture_corrected"],
        "active_frontiers": report["active_frontiers"],
        "sb2_discharged": report["sb2_discharged"],
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
