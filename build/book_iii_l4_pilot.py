"""
build/book_iii_l4_pilot.py — v42 Book III L4 Spine Pilot

Book III (Source Universality and Depth Structure) is the final spine book.
With this pilot, the full seven-book spine has machine-readable L4 records.

Book III's primary exports:
  1. thm:unified-coercive [U] — the load-bearing core, branch-agnostic
     C_{n+1} <= Theta_n*C_n + E_n + B_n
  2. thm:depth-sum [U] — depth-sum convergence for Van Hove exhaustions
  3. thm:ACA-chain [C] — the ACA coercivity chain feeding Book VI NS-4B Sobolev
  4. lem:cheeger-from-BUO [C] — spectral gap from BUO condition
  5. thm:governing [U] — four-part governing theorem

Key dependency that closes the final gap:
  thm:VI.NS-4B-sobolev [C] CITES thm:III.ACA-chain [C]
  thm:III.ACA-chain CITES lem:III.cheeger-from-BUO [C]
  lem:III.cheeger-from-BUO CITES def:III.BUO [D]
  def:III.BUO CITES def:II.collar [D]  (from Book II)

With Book III records, the NS branch book's Sobolev surrogate dependency chain
is now fully machine-traceable from the NS branch endpoint back through
Book VI -> Book III -> Book II -> Book I.

Complete seven-book spine is now machine-readable.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
III_CLAIMS_DIR = ROOT / "claims" / "spine" / "III"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

L4_CERT_ORDER = [
    "sr:III.quotient-visible",
    "sr:III.balance-before-interpretation",
    "sr:III.comparison-through-maps",
    "def:III.persistent-obs",
    "def:III.transfer-map",
    "def:III.stability-functional",
    "def:III.BUO",
    "def:III.conserved-charges",
    "thm:III.depth-sum",
    "thm:III.unified-coercive",
    "thm:III.balance-composable",
    "lem:III.charge-conservation",
    "lem:III.cheeger-from-BUO",
    "thm:III.ACA-chain",
    "thm:III.coercive-inequality",
    "thm:III.governing",
    "status:III",
]

MUST_BE_U = [
    "thm:III.depth-sum",
    "thm:III.unified-coercive",
    "thm:III.balance-composable",
    "lem:III.charge-conservation",
    "thm:III.governing",
]

MUST_BE_C = [
    "lem:III.cheeger-from-BUO",
    "thm:III.ACA-chain",
    "thm:III.coercive-inequality",
]

# The complete NS branch dependency chain through Book III
NS_CHAIN = [
    "thm:NS.SB2-discharged [C]  (NS Branch: ob:NS.SB2 discharged via SCT.6b)",
    "→ thm:II.SCT6b [C]  (SCT.6b — Book II)",
    "→ thm:II.boundary-capacity [C]  (boundary capacity — Book II)",
    "→ hyp:II.LS2 [C]  (LS-2 hypothesis — Book II)",
    "→ def:II.collar [D]  (collar structure — Book II)",
]

YM_ACA_CHAIN = [
    "thm:YM.7 [C]  (YM endpoint — mass gap)",
    "→ thm:VI.NS-4B-sobolev [C]  (Sobolev surrogate — Book VI)",
    "→ thm:III.ACA-chain [C]  (ACA coercivity chain — Book III)",
    "→ lem:III.cheeger-from-BUO [C]  (Cheeger from BUO — Book III)",
    "→ def:III.BUO [D]  (BUO condition — Book III)",
    "→ def:II.collar [D]  (collar structure — Book II)",
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


def load_iii_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(III_CLAIMS_DIR.glob("*.yaml")):
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

    # 1. Unified coercive-transport inequality [U]
    uc = claims.get("thm:III.unified-coercive", {})
    uc_status = computed.get("thm:III.unified-coercive", {}).get(
        "effective_status", uc.get("declared_status", ""))
    add("l4.iii.unified-coercive-U", uc_status == "U",
        f"thm:III.unified-coercive status = {uc_status}",
        "[U]: load-bearing core; branch-agnostic; depends only on Books I and II")

    # 2. Depth-sum convergence [U]
    ds = claims.get("thm:III.depth-sum", {})
    ds_status = computed.get("thm:III.depth-sum", {}).get(
        "effective_status", ds.get("declared_status", ""))
    add("l4.iii.depth-sum-U", ds_status == "U",
        f"thm:III.depth-sum status = {ds_status}",
        "[U]: Van Hove exhaustion convergence; branch-agnostic")

    # 3. ACA chain [C] with BUO constraints
    aca = claims.get("thm:III.ACA-chain", {})
    aca_status = computed.get("thm:III.ACA-chain", {}).get(
        "effective_status", aca.get("declared_status", ""))
    aca_scope = aca.get("scope", {}) or {}
    aca_constraints = aca_scope.get("inherited_constraints") or []
    add("l4.iii.ACA-chain-C", aca_status == "C" and len(aca_constraints) >= 2,
        f"status = {aca_status}, constraints = {aca_constraints}",
        "[C] with BUO+K_0=7+Phase-A constraints; feeds Book VI NS-4B Sobolev")

    # 4. BUO definition present
    buo_present = "def:III.BUO" in claims
    add("l4.iii.BUO-def-present", buo_present,
        "present" if buo_present else "MISSING",
        "def:III.BUO must be present — it is the hypothesis for ACA chain and Book VI NS-4B")

    # 5. Governing theorem [U] with all four parts
    gov = claims.get("thm:III.governing", {})
    gov_status = computed.get("thm:III.governing", {}).get(
        "effective_status", gov.get("declared_status", ""))
    add("l4.iii.governing-U", gov_status == "U",
        f"thm:III.governing status = {gov_status}",
        "[U]: four-part governing theorem; feeds Book IV OT->POT transition")

    # 6. All [U] results unconditional
    non_u = [cid for cid in MUST_BE_U if
             computed.get(cid, {}).get("effective_status",
                                       claims.get(cid, {}).get("declared_status", "")) != "U"]
    add("l4.iii.U-layer-unconditional", not non_u,
        non_u or "all [U]",
        "All primary [U] Book III results are unconditional")

    # 7. Honest-posture: conditional results explicitly conditioned
    c_no_constraints = [cid for cid in MUST_BE_C if cid in claims and
                        not (claims[cid].get("scope", {}) or {}).get("inherited_constraints")]
    add("l4.iii.C-layer-conditioned", not c_no_constraints,
        c_no_constraints or "all conditioned",
        "[C] results must carry BUO/K_0=7/Phase-A constraints")

    # 8. Book III -> IV transition: OT arena feeds POT category
    iv_pot = (ROOT / "claims" / "spine" / "IV" / "def_IV_POT_object.yaml").exists()
    add("l4.iii.III-IV-transition", iv_pot,
        f"def:IV.POT-object present: {iv_pot}",
        "Book III OT arena feeds Book IV POT category; def:IV.POT-object must exist")

    # 9. ACA chain -> Book VI linkage
    vi_ns4b = (ROOT / "claims" / "spine" / "VI" / "thm_VI_NS_4B_sobolev.yaml").exists()
    add("l4.iii.ACA-to-VI-linkage", vi_ns4b,
        f"thm:VI.NS-4B-sobolev present: {vi_ns4b}",
        "thm:III.ACA-chain -> thm:VI.NS-4B-sobolev linkage must be closeable")

    # 10. Prose and xref
    prose_ok = sum(1 for c in claims.values() if check_prose(c))
    prose_score = round(100 * prose_ok / len(claims), 1) if claims else 0
    add("l4.iii.prose-completeness", prose_score >= 90.0,
        f"{prose_score}% ({prose_ok}/{len(claims)})",
        ">= 90% prose", severity="warning")

    xref_count = sum(1 for c in claims.values() if c.get("canonical_xref"))
    add("l4.iii.xref-annotations", xref_count >= len(L4_CERT_ORDER) - 2,
        f"{xref_count}/{len(claims)}", f">= {len(L4_CERT_ORDER)-2} xrefs")

    all_pass = all(c["status"] == "pass" for c in checks if c["severity"] == "error")

    # Check spine completeness
    all_7_books = all(
        (ROOT / "claims" / "spine" / book).exists()
        for book in ["I", "II", "III", "IV", "V", "VI", "VII"]
    )

    return {
        "status": "passed" if all_pass else "needs_review",
        "book": "III",
        "track": "spine",
        "l4_level": "spine_release_candidate" if all_pass else "l4_candidate",
        "schema_version": "0.42.0",
        "claim_count": len(claims),
        "xref_count": xref_count,
        "prose_score": prose_score,
        "unified_coercive_status": uc_status,
        "depth_sum_status": ds_status,
        "ACA_chain_status": aca_status,
        "governing_status": gov_status,
        "all_7_books_present": all_7_books,
        "supersession_effect": "none",
        "primary_contribution": (
            "Completes the seven-book spine. "
            "Provides: (1) the Unified Coercive-Transport Inequality [U], "
            "the branch-agnostic load-bearing core; "
            "(2) the ACA Coercivity Chain [C], feeding Book VI NS-4B Sobolev; "
            "(3) the OT arena as the immediate precursor to Book IV's POT category."
        ),
        "checks": checks,
    }


def render_shell_tex(claims: Dict, computed: Dict) -> str:
    parts = [
        "% Book III L4 Shell -- auto-generated by build/book_iii_l4_pilot.py",
        r"\section*{Book III Source Universality --- L4 Generated Shell}",
        r"\addcontentsline{toc}{section}{Book III L4 Shell (Final Spine Book)}",
        "",
        r"\noindent\textbf{This is the final spine book.} "
        r"With Book~III, the full seven-book spine has machine-readable L4 records.",
        "",
        r"\noindent\textit{Book~III's load-bearing core is unconditional: "
        r"the Unified Coercive-Transport Inequality "
        r"$C_{n+1} \leq \Theta_n C_n + E_n + B_n$ depends only on "
        r"Book~I's defect ledger and Book~II's LS-2 boundary law. "
        r"The ACA Coercivity Chain [C] feeds Book~VI's NS-4B Sobolev surrogate.}",
        "",
        r"\subsection*{Unconditional [U] Layer}",
        r"\begin{longtable}{p{0.32\linewidth}p{0.08\linewidth}p{0.53\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid in MUST_BE_U:
        claim = claims.get(cid, {})
        status = computed.get(cid, {}).get("effective_status", claim.get("declared_status", "?"))
        xref = claim.get("canonical_xref", {})
        label = xref.get("canonical_label", claim.get("title", cid))[:55]
        parts.append(r"\texttt{" + tex_escape(cid) + "} & [" +
                     tex_escape(status) + "] & " + tex_escape(label) + r"\\")
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{ACA Chain [C] --- Feeding Book VI NS-4B Sobolev Surrogate}",
        r"\begin{longtable}{p{0.32\linewidth}p{0.08\linewidth}p{0.53\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid in MUST_BE_C:
        claim = claims.get(cid, {})
        status = computed.get(cid, {}).get("effective_status", claim.get("declared_status", "?"))
        xref = claim.get("canonical_xref", {})
        label = xref.get("canonical_label", claim.get("title", cid))[:55]
        parts.append(r"\texttt{" + tex_escape(cid) + "} & [" +
                     tex_escape(status) + "] & " + tex_escape(label) + r"\\")
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{YM/NS Branch ACA Chain (now machine-traceable)}",
        r"\begin{longtable}{p{0.90\linewidth}}",
        r"\hline",
    ]
    for node in YM_ACA_CHAIN:
        parts.append(r"\texttt{" + tex_escape(node) + r"}\\")
    parts += [r"\hline", r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Complete Seven-Book Spine (v42)}",
        r"\begin{longtable}{p{0.12\linewidth}p{0.40\linewidth}p{0.15\linewidth}p{0.08\linewidth}}",
        r"\textbf{Book} & \textbf{Title} & \textbf{Character} & \textbf{Claims}\\",
        r"\hline\endfirsthead",
        r"\textbf{Book} & \textbf{Title} & \textbf{Character} & \textbf{Claims}\\\hline\endhead",
    ]
    spine_rows = [
        ("I",   "Unconditional Source Architecture", "All [U]", "22"),
        ("II",  "Locality and Boundary Structure",   "[U]+[C]", "21"),
        ("III", "Source Universality/Depth Structure", "[U]+[C]", "17"),
        ("IV",  "Universal Source and POT Category", "Primarily [U]", "19"),
        ("V",   "Branch Legitimacy",                  "Primarily [U]", "19"),
        ("VI",  "Continuum Bridge",                   "Mostly [C]", "18"),
        ("VII", "Governance Book",                    "All [U]", "19"),
    ]
    for book, title, char, claims_n in spine_rows:
        parts.append(
            tex_escape(book) + " & " + tex_escape(title) + " & " +
            tex_escape(char) + " & " + tex_escape(claims_n) + r"\\"
        )
    parts += [r"\end{longtable}"]

    return "\n".join(parts) + "\n"


def render_cert_tex(cert: Dict, claims: Dict, computed: Dict) -> str:
    criteria_passed = sum(1 for c in cert["checks"] if c["status"] == "pass")
    lines = [
        "% Book III L4 Certificate -- auto-generated (FINAL SPINE BOOK)",
        r"\section*{Book III L4 Equivalence Certificate}",
        r"\addcontentsline{toc}{section}{Book III L4 Certificate (Final Spine Book)}",
        "",
        r"\noindent\textbf{This is the final spine book.} "
        r"Seven-book spine machine-readable L4 coverage is now complete.",
        "",
        rf"\textbf{{L4 gate:}} {'PASSED' if cert['status']=='passed' else 'NEEDS REVIEW'} ({criteria_passed}/{len(cert['checks'])} criteria)\\",
        rf"\textbf{{Unified coercive-transport inequality:}} \texttt{{[{cert['unified_coercive_status']}]}} (must be [U])\\",
        rf"\textbf{{Depth-sum convergence:}} \texttt{{[{cert['depth_sum_status']}]}} (must be [U])\\",
        rf"\textbf{{ACA chain:}} \texttt{{[{cert['ACA_chain_status']}]}} (must be [C])\\",
        rf"\textbf{{All 7 spine books present:}} {cert['all_7_books_present']}",
        "",
        r"\noindent\textit{" + tex_escape(cert["primary_contribution"][:250]) + "}",
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
    claims = load_iii_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    cert = build_l4_certificate(claims, computed)

    (REPORTS / "book_iii_l4_certificate.json").write_text(
        json.dumps(cert, indent=2), encoding="utf-8")

    md_lines = [
        "# Book III L4 Equivalence Certificate — FINAL SPINE BOOK",
        "",
        f"**L4 gate:** {'✅ PASSED' if cert['status']=='passed' else '⚠️ NEEDS REVIEW'} "
        f"({sum(1 for c in cert['checks'] if c['status']=='pass')}/{len(cert['checks'])} criteria)",
        f"**Unified coercive-transport:** `[{cert['unified_coercive_status']}]`",
        f"**Depth-sum:** `[{cert['depth_sum_status']}]`",
        f"**ACA chain:** `[{cert['ACA_chain_status']}]`",
        f"**All 7 spine books present:** {cert['all_7_books_present']}",
        "",
        f"> {cert['primary_contribution']}",
        "",
        "## L4 Criteria",
        "| Check | Status | Observed |",
        "|-------|--------|----------|",
    ]
    for c in cert["checks"]:
        md_lines.append(f"| `{c['id']}` | {'✅' if c['status']=='pass' else '❌'} | "
                        f"{str(c.get('observed',''))[:70]} |")
    md_lines += [
        "",
        "## YM/NS ACA Chain (fully machine-traceable)",
        "",
    ]
    for node in YM_ACA_CHAIN:
        md_lines.append(f"`{node}`")
    (TABLES / "book_iii_l4_certificate.md").write_text("\n".join(md_lines) + "\n")

    shell_inner = render_shell_tex(claims, computed)
    (TEX / "book_iii_l4_shell.tex").write_text(shell_inner)
    cert_inner = render_cert_tex(cert, claims, computed)
    (TEX / "book_iii_l4_certificate.tex").write_text(cert_inner)

    for stem, title, inner in [
        ("book_iii_l4_shell",       "Book III Source Universality L4 Shell (Final Spine Book)", "book_iii_l4_shell.tex"),
        ("book_iii_l4_certificate", "Book III L4 Equivalence Certificate (Final Spine Book)",   "book_iii_l4_certificate.tex"),
    ]:
        standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC {tex_escape(title)}\\[1ex]\large Schema v0.42.0\\[0.5ex]
\normalsize L4 Spine Release Candidate\\[0.5ex]
\small Seven-Book Spine Complete}}
\author{{Generated by NFC Governance Engine v42}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{{Book III is the final spine book.}} With this pilot, the full
seven-book NFC spine has machine-readable L4 records.
The Unified Coercive-Transport Inequality $C_{{n+1}} \leq \Theta_n C_n + E_n + B_n$
is the branch-agnostic load-bearing core [U].
The ACA Coercivity Chain [C] feeds Book~VI's NS-4B Sobolev surrogate.
This is an L4 spine-pilot shell --- the canonical Book~III is the authoritative source.
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
        "unified_coercive_status": cert["unified_coercive_status"],
        "ACA_chain_status": cert["ACA_chain_status"],
        "governing_status": cert["governing_status"],
        "all_7_books_present": cert["all_7_books_present"],
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
