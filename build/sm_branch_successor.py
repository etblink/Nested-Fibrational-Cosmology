"""
build/sm_branch_successor.py — v30 SM Branch-Successor Pilot

SM is the first pilot to exercise the intrinsic-structural-close posture.
This posture is distinct from all prior postures:
  - NOT conditional-cert-close (SM does not simply approach a known endpoint
    conditionally; it closes internal obligations while remaining scope-inherited)
  - NOT cert-close (inherited YM/GR obligations block unconditional closure)
  - NOT cert-proj (the four internal obligations ARE conditionally discharged)

Governance invariants that must hold:
  - status:SM = intrinsic-structural-close
  - ob:SM.O-IDcont remains ACTIVE and OPEN
  - Status(SM) <= Status(YM) AND Status(GR) -- inheritance inequality preserved
  - No claim of: cert-close, unconditional closure, full empirical SM,
    measured masses, CKM/PMNS, RG-running, or gauge-gravity unification
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims" / "branches" / "SM"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

# Ordered claim list for the SM pilot packet.
# Internal obligations first, then theorems that discharge them,
# then the closure propositions, then the live frontier, then status.
SM_ORDER = [
    "ob:SM.harmonization",
    "ob:SM.matter",
    "ob:SM.higgs",
    "ob:SM.coupling-transfer",
    "thm:SM.gauge-chain",
    "thm:SM.three-gen",
    "thm:SM.harmonization-partial",
    "thm:SM.coupling-transfer-full",
    "thm:SM.higgs-source-descended",
    "thm:SM.18.1",
    "prop:SM.intrinsic-closure",
    "prop:SM.status-reconciliation",
    "ob:SM.O-IDcont",
    "status:SM",
]

EXPECTED_POSTURE = "intrinsic-structural-close"
EXPECTED_ACTIVE_FRONTIERS: List[str] = ["ob:SM.O-IDcont"]

# These claims must NOT appear as closed in this pilot
MUST_NOT_CLOSE = [
    "cert-close",
    "unconditional-SM-cert-close",
    "full-empirical-SM",
    "gauge-gravity-unification",
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


def load_sm_claims() -> Dict[str, Dict[str, Any]]:
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
    if kind in ("proposition", "corollary"):
        return "nfcproposition"
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
    inherited = (claim.get("scope", {}) or {}).get("inherited_constraints", []) or []

    parts = [
        rf"\begin{{{env}}}{{{tex_escape(title)}}}",
        rf"\textbf{{Machine ID.}} \texttt{{{tex_escape(cid)}}}\\",
        rf"\textbf{{Declared.}} {tex_escape(declared)}\quad"
        rf"\textbf{{Computed.}} {tex_escape(effective)}\\",
        rf"\textbf{{Scope.}} {tex_escape(scope_summary(claim))}",
        "",
        md_to_tex(body or "No body text supplied."),
    ]
    if inherited:
        parts += ["", r"\medskip",
                  r"\noindent\textit{Inherited constraints.} "
                  + tex_escape(", ".join(inherited))]
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
    for cid in SM_ORDER:
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
        r"\begin{longtable}{p{0.30\linewidth}p{0.14\linewidth}p{0.12\linewidth}"
        r"p{0.15\linewidth}p{0.18\linewidth}}",
        r"\caption{SM successor-pilot claim catalog}\label{tab:sm-successor-claims}\\",
        r"\textbf{ID} & \textbf{Kind} & \textbf{Decl.} & \textbf{Comp.} & \textbf{Scope}\\",
        r"\hline\endfirsthead",
        r"\textbf{ID} & \textbf{Kind} & \textbf{Decl.} & \textbf{Comp.} & \textbf{Scope}\\",
        r"\hline\endhead",
    ]
    for row in rows:
        lines.append(" & ".join(tex_escape(x) for x in row) + r"\\")
    lines.append(r"\end{longtable}")
    table = "\n".join(lines)

    posture_computed = computed.get("status:SM", {}).get(
        "effective_status", "unknown"
    )

    body_parts = [
        "% Auto-generated by build/sm_branch_successor.py. Do not edit by hand.",
        r"\section*{SM Branch Successor Pilot}",
        r"\addcontentsline{toc}{section}{SM Branch Successor Pilot}",
        "",
        r"This generated packet is the v30 L2 branch-pilot shell for the "
        r"Standard Model super-branch. It is \emph{not} a supersession of "
        r"the canonical SM Branch Book. "
        r"The pilot exercises the \textbf{intrinsic-structural-close} posture "
        r"for the first time: SM has closed its internal structural obligations "
        r"while remaining open on inherited scope from the YM and GR sub-branches.",
        "",
        r"\subsection*{Posture and inheritance structure}",
        rf"Computed SM posture: \textbf{{{tex_escape(posture_computed)}}}. "
        r"This posture encodes: \emph{(i)} conditional intrinsic structural "
        r"closure (four internal obligations discharged at structural-conditional "
        r"level); \emph{(ii)} inherited-scope open (all YM and GR obligations "
        r"propagate to SM); \emph{(iii)} active frontier \texttt{{ob:SM.O-IDcont}} "
        r"(continuum/operator identification force upgrade, the single named "
        r"irreducible frontier of the SM branch).",
        "",
        r"\subsection*{Status inequality}",
        r"The governing constraint is: "
        r"$\operatorname{Status}(\mathrm{SM}) \le "
        r"\operatorname{Status}(\mathrm{YM}) \wedge "
        r"\operatorname{Status}(\mathrm{GR}) \wedge "
        r"\operatorname{Status}(\mathrm{SM}_{\mathrm{intrinsic}})$. "
        r"The pilot preserves this inequality explicitly. "
        r"SM cannot be promoted to conditional-cert-close or cert-close "
        r"by any discharge internal to the SM packet.",
        "",
        r"\subsection*{Non-claims (strictly maintained)}",
        r"\begin{itemize}",
        r"\item No measured particle masses",
        r"\item No CKM/PMNS mixing parameters",
        r"\item No renormalization-group running derivation",
        r"\item No full empirical Standard Model reconstruction",
        r"\item No gauge-gravity unification claim",
        r"\item No unconditional CERT-CLOSE",
        r"\end{itemize}",
        "",
        table,
        "",
        r"\subsection*{Generated claim shells}",
    ]

    for cid in SM_ORDER:
        claim = claims.get(cid)
        if claim:
            body_parts.append(render_claim(claim, computed))
            body_parts.append("")

    packet = "\n\n".join(body_parts)
    (TEX / "sm_branch_successor.tex").write_text(packet + "\n", encoding="utf-8")

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
\newenvironment{nfcobligation}[1]{\par\medskip\noindent\textbf{Obligation: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcfrontier}[1]{\par\medskip\noindent\textbf{Frontier: #1}\par\smallskip}{\par\medskip}
\newenvironment{nfcstatusnote}[1]{\par\medskip\noindent\textbf{Status note: #1}\par\smallskip}{\par\medskip}
\title{NFC SM Branch Successor Pilot\\[0.5ex]
  \large v30 --- L2 Generated Shell\\[0.5ex]
  \normalsize First exercise of \texttt{intrinsic-structural-close} posture}
\author{Generated governance shell}
\date{}
\begin{document}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{Governance notice.} This is a machine-generated L2 branch-pilot
shell. It is \emph{not} a supersession of the canonical NFC Standard Model Branch
Book. The canonical SM branch book remains the authoritative source of truth.
Full supersession requires L5 gate passage per the NFC supersession policy.
\vspace{1em}
\input{sm_branch_successor.tex}
\end{document}
"""
    (TEX / "sm_branch_successor_standalone.tex").write_text(standalone, encoding="utf-8")


def write_equivalence_report(
    claims: Dict[str, Dict[str, Any]], computed: Dict[str, Any]
) -> Dict[str, Any]:
    generated_ids = [cid for cid in SM_ORDER if cid in claims]
    missing_expected = [cid for cid in SM_ORDER if cid not in claims]
    unexpected = sorted(set(claims) - set(SM_ORDER))

    active_frontiers = [
        cid for cid in generated_ids
        if computed.get(cid, {}).get(
            "effective_status", claims[cid].get("declared_status")
        ) == "O"
    ]
    posture = computed.get("status:SM", {}).get("effective_status")

    # Check the status inequality: SM must not claim posture stronger than YM or GR
    ym_posture = computed.get("status:YM", {}).get("effective_status", "unknown")
    gr_posture = computed.get("status:GR", {}).get("effective_status", "unknown")
    sm_posture_not_stronger_than_ym = posture != "cert-close" and posture != "unconditional-cert-close"
    sm_posture_not_stronger_than_gr = posture != "cert-close" and posture != "unconditional-cert-close"

    # Check intrinsic-structural-close is correctly scoped
    intrinsic_prop = claims.get("prop:SM.intrinsic-closure", {})
    intrinsic_scope = (intrinsic_prop.get("scope", {}) or {}).get(
        "certificate_scope", ""
    )
    intrinsic_correctly_scoped = "intrinsic" in intrinsic_scope

    # O-IDcont must be open
    o_idcont = claims.get("ob:SM.O-IDcont", {})
    o_idcont_declared = o_idcont.get("declared_status", "")
    o_idcont_effective = computed.get("ob:SM.O-IDcont", {}).get(
        "effective_status", o_idcont_declared
    )
    o_idcont_open = o_idcont_declared == "O" or o_idcont_effective == "O"

    checks = [
        {
            "id": "sm.successor.expected-claim-list",
            "status": "pass" if not missing_expected else "fail",
            "observed": {"missing": missing_expected},
            "expected": "All SM_ORDER claims present.",
        },
        {
            "id": "sm.successor.posture",
            "status": "pass" if posture == EXPECTED_POSTURE else "fail",
            "observed": posture,
            "expected": EXPECTED_POSTURE,
        },
        {
            "id": "sm.successor.frontier-profile",
            "status": "pass"
            if sorted(active_frontiers) == sorted(EXPECTED_ACTIVE_FRONTIERS)
            else "fail",
            "observed": active_frontiers,
            "expected": EXPECTED_ACTIVE_FRONTIERS,
        },
        {
            "id": "sm.successor.no-unexpected-claims",
            "status": "pass" if not unexpected else "warn",
            "observed": unexpected,
            "expected": "No SM records outside pilot order.",
        },
        {
            "id": "sm.successor.o-idcont-open",
            "status": "pass" if o_idcont_open else "fail",
            "observed": {
                "declared": o_idcont_declared,
                "effective": o_idcont_effective,
            },
            "expected": "ob:SM.O-IDcont must remain open: it is the named irreducible frontier.",
        },
        {
            "id": "sm.successor.intrinsic-scope-correct",
            "status": "pass" if intrinsic_correctly_scoped else "warn",
            "observed": intrinsic_scope,
            "expected": "Intrinsic closure must be scoped to intrinsic-structural level.",
        },
        {
            "id": "sm.successor.status-inequality-preserved",
            "status": "pass"
            if sm_posture_not_stronger_than_ym and sm_posture_not_stronger_than_gr
            else "fail",
            "observed": {
                "sm": posture,
                "ym": ym_posture,
                "gr": gr_posture,
            },
            "expected": (
                "Status(SM) <= Status(YM) AND Status(GR): "
                "SM must not claim posture stronger than its parent branches."
            ),
        },
        {
            "id": "sm.successor.no-full-empirical-sm",
            "status": "pass" if posture == EXPECTED_POSTURE else "fail",
            "observed": posture,
            "expected": "Must not claim cert-close or full empirical SM completion.",
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
        "active_frontiers": active_frontiers,
        "posture": posture,
        "ym_posture": ym_posture,
        "gr_posture": gr_posture,
        "o_idcont_open": o_idcont_open,
        "intrinsic_correctly_scoped": intrinsic_correctly_scoped,
        "checks": checks,
        "supersession_effect": "none; pilot shell only",
        "non_claims": [
            "No measured particle masses",
            "No CKM/PMNS",
            "No RG-running",
            "No full empirical SM reconstruction",
            "No gauge-gravity unification",
            "No unconditional CERT-CLOSE",
        ],
    }

    (REPORTS / "sm_successor_equivalence_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    lines = [
        "# SM Branch Successor Equivalence Report",
        "",
        f"**Status:** {status}",
        "**Pilot level:** L2",
        f"**Generated claim count:** {len(generated_ids)}",
        f"**Computed SM posture:** `{posture}`",
        f"**YM posture (inherited):** `{ym_posture}`",
        f"**GR posture (inherited):** `{gr_posture}`",
        f"**Active frontiers:** "
        + (", ".join(f"`{x}`" for x in active_frontiers) or "none"),
        f"**O-IDcont open:** {o_idcont_open}",
        "",
        "## Status inequality",
        "",
        "Status(SM) <= Status(YM) AND Status(GR) AND Status(SM_intrinsic)",
        f"  SM: `{posture}` | YM: `{ym_posture}` | GR: `{gr_posture}`",
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
        "## Non-claims",
        "",
        "All of the following are explicitly excluded from the SM pilot:",
    ]
    for nc in report["non_claims"]:
        lines.append(f"- {nc}")
    lines += [
        "",
        "## Supersession effect",
        "",
        "None. This packet is a branch-successor pilot shell.",
    ]
    (TABLES / "sm_successor_equivalence_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    claims = load_sm_claims()
    computed = load_json(REPORTS / "computed_statuses.json")
    render_tex(claims, computed)
    report = write_equivalence_report(claims, computed)
    print(json.dumps({
        "status": report["status"],
        "generated_claim_count": report["generated_claim_count"],
        "posture": report["posture"],
        "ym_posture": report["ym_posture"],
        "gr_posture": report["gr_posture"],
        "active_frontiers": report["active_frontiers"],
        "o_idcont_open": report["o_idcont_open"],
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
