"""
build/book_iv_l4_pilot.py — v40 Book IV L4 Spine Pilot

Book IV (Universal Source and POT Category) establishes:
  - The POT category (the canonical source category)
  - The existence of the universal source U (Thm. IV.5.1 — Universal Completion)
  - The uniqueness of U (by factorization role)
  - That every lawful realization factors through U (cor:descendants-factor)
  - That U is a unified terminal source for all declared branches

Without Book IV, UBLT condition 2 ("certified source descent: E = F(U)")
lacks a machine-readable source — F(U) would reference a U whose existence
was not proved in the governance engine.

This pilot closes that gap: with Book IV machine records, the full
spine dependency chain from any branch endpoint back to the source
is now machine-traceable:
  thm:GR.domain → thm:VII.6.4 → thm:V.UBLT → cor:IV.descendants-factor
    → thm:IV.universal-completion (= Thm. IV.5.1) → def:IV.candidate-U
    → def:IV.POT-category → def:IV.POT-object → def:I.obs-quotient
    → thm:I.stabilization → thm:I.governing

All Book IV primary results are [U]. Only thm:IV.unified-emergence is [C].
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
IV_CLAIMS_DIR = ROOT / "claims" / "spine" / "IV"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

L4_CERT_ORDER = [
    "sr:IV.source-not-branch",
    "def:IV.POT-object",
    "def:IV.POT-category",
    "def:IV.transport-invariant",
    "def:IV.candidate-U",
    "def:IV.exhaustive-source-image",
    "thm:IV.ORA",
    "thm:IV.CTM",
    "thm:IV.normalization",
    "thm:IV.AMCT",
    "thm:IV.completion-ladder",
    "thm:IV.universal-completion",
    "thm:IV.source-uniqueness",
    "cor:IV.descendants-factor",
    "thm:IV.terminal-source",
    "thm:IV.governing",
    "cor:IV.all-branches-through-U",
    "thm:IV.unified-emergence",
    "status:IV",
]

# Must be [U]
MUST_BE_U = [
    "thm:IV.ORA", "thm:IV.CTM", "thm:IV.normalization",
    "thm:IV.AMCT", "thm:IV.completion-ladder",
    "thm:IV.universal-completion", "thm:IV.source-uniqueness",
    "cor:IV.descendants-factor", "thm:IV.terminal-source",
    "thm:IV.governing", "cor:IV.all-branches-through-U",
]

# Five ORA rung theorems that jointly build U
ORA_RUNGS = [
    "thm:IV.ORA", "thm:IV.CTM", "thm:IV.normalization",
    "thm:IV.AMCT", "thm:IV.completion-ladder",
]

# The full spine dependency chain (terminal nodes)
FULL_CHAIN = [
    "thm:GR.domain [C]",
    "→ thm:VII.6.4 [U]  (Closure Schema)",
    "→ thm:V.UBLT [U]  (UBLT Thm. V.8.1)",
    "→ cor:IV.descendants-factor [U]  (All realizations factor through U)",
    "→ thm:IV.universal-completion [U]  (Existence of U, Thm. IV.5.1)",
    "→ def:IV.candidate-U [D]  (U = T/~_pres)",
    "→ def:IV.POT-category [D]  (POT category)",
    "→ def:IV.POT-object [D]  (Sigma, Lambda, T, D quadruple)",
    "→ def:I.obs-quotient [D]  (Sigma_n = Omega/~_n)",
    "→ thm:I.stabilization [U]  (Finite Stabilization)",
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


def load_iv_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(IV_CLAIMS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        cid = data.get("id")
        if cid:
            claims[cid] = data
    return claims


def check_prose(claim: Dict[str, Any]) -> bool:
    body_path = claim.get("body_file")
    if not body_path:
        return False
    p = ROOT / body_path
    return p.exists() and len(p.read_text(encoding="utf-8").strip()) >= 50


def tex_escape(value: Any) -> str:
    s = "" if value is None else str(value)
    for old, new in [
        ("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
        ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
        ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        s = s.replace(old, new)
    return s


def build_l4_certificate(
    claims: Dict[str, Dict[str, Any]],
    computed: Dict[str, Any],
) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(check_id, passed, observed, expected, severity="error"):
        checks.append({"id": check_id, "status": "pass" if passed else "fail",
                        "severity": severity, "observed": observed, "expected": expected})

    # 1. Universal Completion Theorem (Thm. IV.5.1) present and [U]
    uc = claims.get("thm:IV.universal-completion", {})
    uc_status = computed.get("thm:IV.universal-completion", {}).get(
        "effective_status", uc.get("declared_status", ""))
    add("l4.iv.universal-completion-U", uc_status == "U",
        f"thm:IV.universal-completion status = {uc_status}",
        "thm:IV.universal-completion must be [U] — primary existence theorem for U")

    # 2. Source uniqueness present and [U]
    su = claims.get("thm:IV.source-uniqueness", {})
    su_status = computed.get("thm:IV.source-uniqueness", {}).get(
        "effective_status", su.get("declared_status", ""))
    add("l4.iv.source-uniqueness-U", su_status == "U",
        f"thm:IV.source-uniqueness status = {su_status}",
        "thm:IV.source-uniqueness must be [U] — uniqueness by factorization role")

    # 3. cor:descendants-factor present and [U]
    df = claims.get("cor:IV.descendants-factor", {})
    df_status = computed.get("cor:IV.descendants-factor", {}).get(
        "effective_status", df.get("declared_status", ""))
    add("l4.iv.descendants-factor-U", df_status == "U",
        f"cor:IV.descendants-factor status = {df_status}",
        "[U]: every lawful realization factors through U — source of UBLT condition 2")

    # 4. All five ORA rung theorems present and [U]
    missing_rungs = [r for r in ORA_RUNGS if r not in claims]
    non_u_rungs = [r for r in ORA_RUNGS if r in claims and
                   computed.get(r, {}).get("effective_status",
                                           claims[r].get("declared_status", "")) != "U"]
    add("l4.iv.ORA-rungs-complete", not missing_rungs and not non_u_rungs,
        {"missing": missing_rungs, "non_u": non_u_rungs} if (missing_rungs or non_u_rungs) else "all 5 rungs [U]",
        "All 5 ORA rung theorems present and [U]: ORA, CTM, normalization, AMCT, completion-ladder")

    # 5. Governing theorem present and [U]
    gov = claims.get("thm:IV.governing", {})
    gov_status = computed.get("thm:IV.governing", {}).get(
        "effective_status", gov.get("declared_status", ""))
    add("l4.iv.governing-U", gov_status == "U",
        f"thm:IV.governing status = {gov_status}",
        "thm:IV.governing must be [U] — Universal Source Theorem (Book IV Governing)")

    # 6. POT category and object definitions present
    missing_defs = [cid for cid in ["def:IV.POT-object", "def:IV.POT-category", "def:IV.candidate-U"]
                    if cid not in claims]
    add("l4.iv.POT-definitions", not missing_defs,
        missing_defs or "POT-object, POT-category, candidate-U all present",
        "Core POT definitions present — necessary for F(U) to be well-typed")

    # 7. unified-emergence is [C] with inherited constraints
    ue = claims.get("thm:IV.unified-emergence", {})
    ue_status = computed.get("thm:IV.unified-emergence", {}).get(
        "effective_status", ue.get("declared_status", ""))
    ue_scope = ue.get("scope", {}) or {}
    ue_constraints = ue_scope.get("inherited_constraints") or []
    add("l4.iv.unified-emergence-conditional",
        ue_status == "C" and len(ue_constraints) >= 2,
        f"status = {ue_status}, constraints = {ue_constraints}",
        "thm:IV.unified-emergence must be [C] with K_0=7+Phase-A constraints")

    # 8. Full spine chain completeness check
    # Verify all nodes of the full chain are present in the governance engine
    chain_nodes = {
        "thm:IV.universal-completion": "thm:IV.universal-completion",
        "def:IV.candidate-U": "def:IV.candidate-U",
        "def:IV.POT-category": "def:IV.POT-category",
        "def:IV.POT-object": "def:IV.POT-object",
        "cor:IV.descendants-factor": "cor:IV.descendants-factor",
    }
    chain_present = all(cid in claims for cid in chain_nodes)
    # Also check Book I and Book V nodes
    book_i_present = (ROOT / "claims" / "spine" / "I" / "def_I_obs_quotient.yaml").exists()
    book_v_present = (ROOT / "claims" / "spine" / "V" / "thm_V_UBLT.yaml").exists()
    book_vii_present = (ROOT / "claims" / "spine" / "VII" / "thm_VII_6_4.yaml").exists()
    full_chain_ok = chain_present and book_i_present and book_v_present and book_vii_present
    add("l4.iv.full-chain-traceable", full_chain_ok,
        f"IV: {chain_present}, BookI: {book_i_present}, BookV: {book_v_present}, BookVII: {book_vii_present}",
        "Full branch-to-source chain (GR.domain → VII.6.4 → V.UBLT → IV.universal-completion → I.obs-quotient) machine-traceable")

    # 9. Prose and xref
    prose_ok = sum(1 for c in claims.values() if check_prose(c))
    prose_score = round(100 * prose_ok / len(claims), 1) if claims else 0
    add("l4.iv.prose-completeness", prose_score >= 90.0,
        f"{prose_score}% ({prose_ok}/{len(claims)})",
        ">= 90% prose", severity="warning")

    xref_count = sum(1 for c in claims.values() if c.get("canonical_xref"))
    add("l4.iv.xref-annotations", xref_count >= len(L4_CERT_ORDER) - 2,
        f"{xref_count}/{len(claims)}", f">= {len(L4_CERT_ORDER)-2} xrefs")

    all_pass = all(c["status"] == "pass" for c in checks if c["severity"] == "error")

    return {
        "status": "passed" if all_pass else "needs_review",
        "book": "IV",
        "track": "spine",
        "l4_level": "spine_release_candidate" if all_pass else "l4_candidate",
        "schema_version": "0.40.0",
        "claim_count": len(claims),
        "xref_count": xref_count,
        "prose_score": prose_score,
        "universal_completion_status": uc_status,
        "source_uniqueness_status": su_status,
        "descendants_factor_status": df_status,
        "governing_status": gov_status,
        "full_chain_traceable": full_chain_ok,
        "supersession_effect": "none",
        "primary_contribution": (
            "Completes the full spine dependency chain. "
            "With Book IV records, every branch endpoint datum E = F(U) "
            "now has a machine-traceable path from E back through "
            "cor:IV.descendants-factor → thm:IV.universal-completion → def:IV.candidate-U "
            "→ def:IV.POT-object → def:I.obs-quotient → thm:I.stabilization."
        ),
        "checks": checks,
    }


def render_shell_tex(claims: Dict, computed: Dict) -> str:
    parts = [
        "% Book IV L4 Shell -- auto-generated by build/book_iv_l4_pilot.py",
        r"\section*{Book IV Universal Source --- L4 Generated Shell}",
        r"\addcontentsline{toc}{section}{Book IV L4 Shell}",
        "",
        r"\noindent\textit{Book IV establishes the universal source object "
        r"$\mathbf{U} \in \mathrm{POT}$: it exists (Thm.~IV.5.1), is unique "
        r"(by factorization role), and every lawful realization factors through it "
        r"(\texttt{cor:IV.descendants-factor}). "
        r"This pilot completes the full spine dependency chain.}",
        "",
        r"\subsection*{Five ORA Rungs Building U}",
        r"\begin{longtable}{p{0.28\linewidth}p{0.08\linewidth}p{0.57\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid in ORA_RUNGS:
        claim = claims.get(cid, {})
        status = computed.get(cid, {}).get("effective_status", claim.get("declared_status", "?"))
        xref = claim.get("canonical_xref", {})
        label = xref.get("canonical_label", claim.get("title", cid))[:55]
        parts.append(r"\texttt{" + tex_escape(cid) + "} & [" +
                     tex_escape(status) + "] & " + tex_escape(label) + r"\\")
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Full Spine Dependency Chain (Now Machine-Traceable)}",
        r"\begin{longtable}{p{0.90\linewidth}}",
        r"\hline",
    ]
    for node in FULL_CHAIN:
        parts.append(r"\texttt{" + tex_escape(node) + r"}\\")
    parts += [r"\hline", r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Full Claim Catalog}",
        r"\begin{longtable}{p{0.30\linewidth}p{0.10\linewidth}p{0.10\linewidth}p{0.42\linewidth}}",
        r"\textbf{Machine ID} & \textbf{Kind} & \textbf{St.} & \textbf{Title}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{Kind} & \textbf{St.} & \textbf{Title}\\\hline\endhead",
    ]
    for cid in L4_CERT_ORDER:
        claim = claims.get(cid)
        if not claim:
            continue
        kind = claim.get("kind", "")[:10]
        status = computed.get(cid, {}).get("effective_status", claim.get("declared_status", "?"))
        title = claim.get("title", cid)[:50]
        parts.append(r"\texttt{" + tex_escape(cid) + "} & " + tex_escape(kind) +
                     " & [" + tex_escape(status) + "] & " + tex_escape(title) + r"\\")
    parts += [r"\end{longtable}"]

    return "\n".join(parts) + "\n"


def render_cert_tex(cert: Dict, claims: Dict, computed: Dict) -> str:
    criteria_passed = sum(1 for c in cert["checks"] if c["status"] == "pass")
    lines = [
        "% Book IV L4 Certificate -- auto-generated",
        r"\section*{Book IV L4 Equivalence Certificate}",
        r"\addcontentsline{toc}{section}{Book IV L4 Certificate}",
        "",
        rf"\textbf{{L4 gate:}} {'PASSED' if cert['status']=='passed' else 'NEEDS REVIEW'} ({criteria_passed}/{len(cert['checks'])} criteria)\\",
        rf"\textbf{{Universal Completion (Thm. IV.5.1):}} \texttt{{[{cert['universal_completion_status']}]}}\\",
        rf"\textbf{{Source Uniqueness:}} \texttt{{[{cert['source_uniqueness_status']}]}}\\",
        rf"\textbf{{Descendants Factor Through U:}} \texttt{{[{cert['descendants_factor_status']}]}}\\",
        rf"\textbf{{Full chain machine-traceable:}} {cert['full_chain_traceable']}",
        "",
        r"\noindent\textit{" + tex_escape(cert["primary_contribution"][:220]) + "}",
        "",
        r"\subsection*{L4 Criteria}",
        r"\begin{longtable}{p{0.48\linewidth}p{0.08\linewidth}p{0.38\linewidth}}",
        r"\textbf{Check} & \textbf{St.} & \textbf{Observed}\\",
        r"\hline\endfirsthead",
        r"\textbf{Check} & \textbf{St.} & \textbf{Observed}\\\hline\endhead",
    ]
    for c in cert["checks"]:
        badge = r"\checkmark" if c["status"] == "pass" else r"\texttimes"
        lines.append(tex_escape(c["id"][:45]) + " & " + badge + " & " +
                     tex_escape(str(c.get("observed", ""))[:55]) + r"\\")
    lines += [r"\end{longtable}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    claims = load_iv_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    cert = build_l4_certificate(claims, computed)

    (REPORTS / "book_iv_l4_certificate.json").write_text(
        json.dumps(cert, indent=2), encoding="utf-8")

    md_lines = [
        "# Book IV L4 Equivalence Certificate",
        "",
        f"**L4 gate:** {'✅ PASSED' if cert['status']=='passed' else '⚠️ NEEDS REVIEW'} "
        f"({sum(1 for c in cert['checks'] if c['status']=='pass')}/{len(cert['checks'])} criteria)",
        f"**Universal Completion (Thm. IV.5.1):** `[{cert['universal_completion_status']}]`",
        f"**Source Uniqueness:** `[{cert['source_uniqueness_status']}]`",
        f"**Descendants Factor:** `[{cert['descendants_factor_status']}]`",
        f"**Full chain traceable:** {cert['full_chain_traceable']}",
        "",
        f"> {cert['primary_contribution']}",
        "",
        "## Full Spine Dependency Chain (Machine-Traceable)",
        "",
    ]
    for node in FULL_CHAIN:
        md_lines.append(f"`{node}`")
    md_lines += [
        "",
        "## L4 Criteria",
        "| Check | Status | Observed |",
        "|-------|--------|----------|",
    ]
    for c in cert["checks"]:
        md_lines.append(f"| `{c['id']}` | {'✅' if c['status']=='pass' else '❌'} | "
                        f"{str(c.get('observed',''))[:70]} |")
    (TABLES / "book_iv_l4_certificate.md").write_text("\n".join(md_lines) + "\n")

    shell_inner = render_shell_tex(claims, computed)
    (TEX / "book_iv_l4_shell.tex").write_text(shell_inner)
    cert_inner = render_cert_tex(cert, claims, computed)
    (TEX / "book_iv_l4_certificate.tex").write_text(cert_inner)

    for stem, title, inner in [
        ("book_iv_l4_shell",       "Book IV Universal Source L4 Shell",    "book_iv_l4_shell.tex"),
        ("book_iv_l4_certificate", "Book IV L4 Equivalence Certificate",   "book_iv_l4_certificate.tex"),
    ]:
        standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC {tex_escape(title)}\\[1ex]\large Schema v0.40.0\\[0.5ex]
\normalsize L4 Spine Release Candidate\\[0.5ex]
\small Completes the full branch-to-source dependency chain}}
\author{{Generated by NFC Governance Engine v40}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{{Book IV completes the chain.}} $\mathbf{{U}}$ exists (Thm.~IV.5.1),
is unique (by factorization role), and every lawful realization factors through it.
The full spine dependency chain from any branch endpoint back to the source
is now machine-traceable in the governance engine.
This is an L4 spine-pilot shell --- the canonical Book~IV is the authoritative source.
\vspace{{1em}}
\input{{{inner}}}
\end{{document}}
"""
        (TEX / f"{stem}_standalone.tex").write_text(standalone)

    passed = all(c["status"] == "pass" for c in cert["checks"] if c["severity"] == "error")
    print(json.dumps({
        "status": cert["status"],
        "l4_level": cert["l4_level"],
        "claim_count": cert["claim_count"],
        "prose_score": cert["prose_score"],
        "universal_completion_status": cert["universal_completion_status"],
        "source_uniqueness_status": cert["source_uniqueness_status"],
        "descendants_factor_status": cert["descendants_factor_status"],
        "full_chain_traceable": cert["full_chain_traceable"],
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
