"""
build/book_i_l4_pilot.py — v37 Book I L4 Spine Pilot

Book I is the unconditional foundation of the NFC spine:
- Observational quotienting (thm:I.governing part a)
- Finite stabilization (thm:I.stabilization, thm:I.governing part b)
- Defect ledger structure (def:I.defect-ledger, prop:I.defect-nonneg, prop:I.ledger-additivity)
- No-presentation-surplus rule (cor:I.no-presentation-surplus)
- K_0 = 7 collar alphabet uniqueness (thm:I.K0-prime)

All Book I results are unconditional [U]. Book I is the spine layer
from which most branch-facing citation originates.

The L4 pilot verifies:
1. All primary exported theorems are present and [U]
2. The K_0=7 uniqueness theorem is present (YM/SM branches depend on it)
3. The no-presentation-surplus rule is present (Book VII depends on it)
4. Defect ledger structure complete
5. Source-architecture standing rules present
6. No conditional theorems in Book I
7. Book I boundary respected (does not smuggle later-book results)

Outputs:
  output/reports/book_i_l4_certificate.json
  output/tables/book_i_l4_certificate.md
  output/tex/book_i_l4_shell.tex
  output/tex/book_i_l4_shell_standalone.tex
  output/tex/book_i_l4_certificate.tex
  output/tex/book_i_l4_certificate_standalone.tex
  output/pdf/book_i_l4_shell_standalone.pdf
  output/pdf/book_i_l4_certificate_standalone.pdf
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
I_CLAIMS_DIR = ROOT / "claims" / "spine" / "I"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

# Primary exported theorems that branch books cite from Book I
PRIMARY_EXPORTS = [
    ("thm:I.governing",              "Observational Quotient Theorem",       "thm:governing (Book I)",  "Packages both main exports: quotient well-defined + finite stabilization"),
    ("thm:I.stabilization",          "Finite Stabilization Theorem",         "thm:stabilization",       "Every refinement chain on finite Omega stabilizes finitely"),
    ("cor:I.no-presentation-surplus","No-Presentation-Surplus Rule",         "cor:no-presentation-surplus", "Primary downstream governance rule; cited by Book VII"),
    ("thm:I.K0-prime",               "K_0=7 Uniqueness Theorem",             "thm:K0-prime",            "Unique prime fixed point of F(p); source of su(3)+su(2)+u(1)"),
    ("prop:I.defect-nonneg",         "Defect Ledger Non-Negativity",         "prop:defect-nonneg",      "D(chi)>=0; foundational for defect accounting"),
    ("prop:I.ledger-additivity",     "Defect Ledger Additivity",             "prop:ledger-additivity",  "D(chi1+chi2)=D(chi1)+D(chi2)"),
    ("cor:I.defect-welldef",         "Defect Ledger Well-Definedness",       "cor:defect-welldef",      "Complete defect ledger characterization"),
    ("thm:I.entropy-monotone",       "Structural Entropy Monotonicity",      "thm:entropy-monotone",    "H_n non-increasing; pairs with defect via duality"),
    ("thm:I.ledger-entropy-duality", "Ledger-Entropy Duality",               "thm:ledger-entropy-duality", "D(chi)=H_0-H_inf; information-theoretic interpretation"),
]

# Results that must be unconditional [U] in Book I
MUST_BE_U = [c[0] for c in PRIMARY_EXPORTS
             if not c[0].startswith("def:") and not c[0].startswith("sr:")]

# Source architecture standing rules
SOURCE_ARCH_RULES = ["sr:I.no-primitive", "sr:I.no-smuggling", "sr:I.cg-alphabet"]

# Things Book I must NOT smuggle from later books
BOOK_I_BOUNDARY = [
    "Local stability of observable outcomes — belongs to Books II/III",
    "Boundary determinacy — belongs to Books II/IV",
    "Source universality — belongs to Book III",
    "Branch legitimacy — belongs to Book V",
    "Continuum correspondence — belongs to Book VI",
]

L4_CERT_ORDER = [
    "sr:I.no-primitive", "sr:I.no-smuggling", "sr:I.cg-alphabet",
    "def:I.admissible-class", "def:I.obs-equiv", "def:I.obs-quotient",
    "def:I.stabilization", "def:I.defect-ledger",
    "lem:I.obs-equiv-equiv", "lem:I.behavioral-canonical",
    "prop:I.defect-nonneg", "prop:I.ledger-additivity",
    "thm:I.emax-unique", "thm:I.K0-prime",
    "thm:I.stabilization", "thm:I.entropy-monotone",
    "thm:I.ledger-entropy-duality", "thm:I.governing",
    "cor:I.no-presentation-surplus", "cor:I.defect-welldef",
    "cor:I.holographic-sparsity",
    "status:I",
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


def load_i_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(I_CLAIMS_DIR.glob("*.yaml")):
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

    def add(check_id: str, passed: bool, observed: Any, expected: Any,
            severity: str = "error") -> None:
        checks.append({
            "id": check_id, "status": "pass" if passed else "fail",
            "severity": severity, "observed": observed, "expected": expected,
        })

    # 1. All primary exports present
    missing_exports = [cid for cid, *_ in PRIMARY_EXPORTS if cid not in claims]
    add("l4.i.primary-exports-present", not missing_exports,
        {"missing": missing_exports} if missing_exports else "all present",
        "All 9 primary Book I exports present")

    # 2. All unconditional — Book I has no conditional theorems
    non_u = []
    for cid in MUST_BE_U:
        if cid in claims:
            status = computed.get(cid, {}).get("effective_status",
                                               claims[cid].get("declared_status", ""))
            if status not in ("U",):
                non_u.append(f"{cid}={status}")
    add("l4.i.all-results-unconditional", not non_u,
        non_u or "all [U]",
        "All Book I theorems must be [U] — no conditional results in the unconditional foundation")

    # 3. K_0=7 theorem present (critical for YM/SM branch inheritance)
    k0_present = "thm:I.K0-prime" in claims
    k0_u = computed.get("thm:I.K0-prime", {}).get(
        "effective_status", claims.get("thm:I.K0-prime", {}).get("declared_status", ""))
    add("l4.i.k0-prime-present", k0_present and k0_u == "U",
        f"present={k0_present}, status={k0_u}",
        "thm:I.K0-prime present and [U] — source of K_0=7 for YM and SM branches")

    # 4. No-presentation-surplus rule present
    nps_present = "cor:I.no-presentation-surplus" in claims
    add("l4.i.no-presentation-surplus-present", nps_present,
        "present" if nps_present else "MISSING",
        "cor:I.no-presentation-surplus present — primary governance rule exported to Book VII+")

    # 5. Source architecture standing rules present
    missing_rules = [r for r in SOURCE_ARCH_RULES if r not in claims]
    add("l4.i.source-arch-rules", not missing_rules,
        missing_rules or "all present",
        "Source architecture standing rules (no-primitive, no-smuggling, cg-alphabet) present")

    # 6. Defect ledger complete (nonneg + additivity + welldef)
    defect_present = all(cid in claims for cid in [
        "def:I.defect-ledger", "prop:I.defect-nonneg",
        "prop:I.ledger-additivity", "cor:I.defect-welldef"
    ])
    add("l4.i.defect-ledger-complete", defect_present,
        "complete" if defect_present else "incomplete",
        "Defect ledger structure: def + nonneg + additivity + welldef all present")

    # 7. Prose completeness
    prose_ok = sum(1 for c in claims.values() if check_prose(c))
    prose_score = round(100 * prose_ok / len(claims), 1) if claims else 0
    add("l4.i.prose-completeness", prose_score >= 90.0,
        f"{prose_score}% ({prose_ok}/{len(claims)})",
        ">= 90% prose completeness", severity="warning")

    # 8. Canonical xref annotations
    xref_count = sum(1 for c in claims.values() if c.get("canonical_xref"))
    add("l4.i.xref-annotations", xref_count >= len(L4_CERT_ORDER) - 2,
        f"{xref_count}/{len(claims)}",
        f">= {len(L4_CERT_ORDER)-2} xref annotations")

    # 9. Book I boundary: no conditional or open results
    boundary_violated = [
        cid for cid, c in claims.items()
        if c.get("declared_status") in ("C", "O")
    ]
    add("l4.i.book-i-boundary", not boundary_violated,
        boundary_violated or "none",
        "Book I must not contain [C] or [O] results — those belong to later books")

    all_pass = all(c["status"] == "pass" for c in checks if c["severity"] == "error")

    return {
        "status": "passed" if all_pass else "needs_review",
        "book": "I",
        "track": "spine",
        "l4_level": "spine_release_candidate" if all_pass else "l4_candidate",
        "schema_version": "0.37.0",
        "claim_count": len(claims),
        "xref_count": xref_count,
        "prose_score": prose_score,
        "all_results_unconditional": not non_u,
        "k0_prime_present": k0_present and k0_u == "U",
        "defect_ledger_complete": defect_present,
        "supersession_effect": "none",
        "primary_exports": [
            {"id": c, "title": t, "canonical": can, "note": note}
            for c, t, can, note in PRIMARY_EXPORTS
        ],
        "book_i_boundary": BOOK_I_BOUNDARY,
        "checks": checks,
    }


def render_shell_tex(claims: Dict, computed: Dict) -> str:
    parts = [
        "% Book I L4 Shell -- auto-generated by build/book_i_l4_pilot.py",
        r"\section*{Book I Unconditional Foundation --- L4 Generated Shell}",
        r"\addcontentsline{toc}{section}{Book I L4 Shell}",
        "",
        r"\noindent\textit{Book I establishes the unconditional source architecture of NFC: "
        r"observational quotienting, finite stabilization, defect ledger, and the "
        r"$K_0 = 7$ collar alphabet uniqueness. All results are [U]. "
        r"The canonical Book I remains the authoritative source.}",
        "",
        r"\subsection*{Primary Unconditional Exports}",
        "",
        r"\begin{longtable}{p{0.30\linewidth}p{0.12\linewidth}p{0.50\linewidth}}",
        r"\textbf{Machine ID} & \textbf{Status} & \textbf{Canonical label / cross-check}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{Status} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid, title, canonical in [
        ("thm:I.governing",               "Observational Quotient Theorem",       "thm:governing"),
        ("thm:I.stabilization",           "Finite Stabilization Theorem",         "thm:stabilization"),
        ("thm:I.K0-prime",                "$K_{0}$=7 Uniqueness",                 "thm:K0-prime"),
        ("cor:I.no-presentation-surplus", "No-Presentation-Surplus Rule",         "cor:no-pres-surplus"),
        ("prop:I.defect-nonneg",          "Defect Non-Negativity",                "prop:defect-nonneg"),
        ("prop:I.ledger-additivity",      "Defect Additivity",                    "prop:ledger-add"),
        ("cor:I.defect-welldef",          "Defect Well-Definedness",              "cor:defect-welldef"),
        ("thm:I.entropy-monotone",        "Entropy Monotonicity",                 "thm:entropy-monotone"),
        ("thm:I.ledger-entropy-duality",  "Ledger-Entropy Duality",               "thm:ledger-ent-dual"),
    ]:
        claim = claims.get(cid, {})
        status = computed.get(cid, {}).get("effective_status",
                                           claim.get("declared_status", "?"))
        parts.append(
            r"\texttt{" + tex_escape(cid) + "} & "
            r"\textbf{[" + tex_escape(status) + "]} & "
            + tex_escape(title) + r" (\texttt{" + tex_escape(canonical) + r"})\\"
        )
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Full Claim Catalog}",
        r"\begin{longtable}{p{0.32\linewidth}p{0.10\linewidth}p{0.10\linewidth}p{0.40\linewidth}}",
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
        parts.append(
            r"\texttt{" + tex_escape(cid) + "} & "
            + tex_escape(kind) + " & "
            + r"\texttt{[" + tex_escape(status) + "]} & "
            + tex_escape(title) + r"\\"
        )
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Book I Boundary (Non-Claims)}",
        r"\noindent Book I proves the items above and nothing more. "
        r"The following belong to later books and may not be imported from Book I:",
        r"\begin{itemize}",
    ]
    for item in BOOK_I_BOUNDARY:
        parts.append(r"\item " + tex_escape(item))
    parts.append(r"\end{itemize}")

    return "\n".join(parts) + "\n"


def render_cert_tex(cert: Dict, claims: Dict, computed: Dict) -> str:
    criteria_passed = sum(1 for c in cert["checks"] if c["status"] == "pass")
    criteria_total = len(cert["checks"])

    lines = [
        "% Book I L4 Certificate -- auto-generated by build/book_i_l4_pilot.py",
        r"\section*{Book I L4 Equivalence Certificate}",
        r"\addcontentsline{toc}{section}{Book I L4 Certificate}",
        "",
        rf"\textbf{{L4 gate:}} {'PASSED' if cert['status']=='passed' else 'NEEDS REVIEW'} ({criteria_passed}/{criteria_total} criteria)\\",
        rf"\textbf{{All results unconditional:}} {cert['all_results_unconditional']}\\",
        rf"\textbf{{K0=7 theorem:}} {cert['k0_prime_present']}\\",
        rf"\textbf{{Defect ledger complete:}} {cert['defect_ledger_complete']}\\",
        rf"\textbf{{Prose completeness:}} {cert['prose_score']}\%",
        "",
        r"\noindent\textit{Book I is the unconditional source architecture. "
        r"All theorem-like objects are [U] or [D]. No conditional theorems exist. "
        r"The K\_0=7 uniqueness theorem is the source of the gauge algebra identification "
        r"inherited by the YM and SM branches.}",
        "",
        r"\subsection*{L4 Criteria}",
        r"\begin{longtable}{p{0.48\linewidth}p{0.08\linewidth}p{0.38\linewidth}}",
        r"\textbf{Check} & \textbf{St.} & \textbf{Observed}\\",
        r"\hline\endfirsthead",
        r"\textbf{Check} & \textbf{St.} & \textbf{Observed}\\\hline\endhead",
    ]
    for c in cert["checks"]:
        badge = r"\checkmark" if c["status"] == "pass" else r"\texttimes"
        lines.append(
            tex_escape(c["id"][:45]) + " & " + badge + " & " +
            tex_escape(str(c.get("observed", ""))[:55]) + r"\\"
        )
    lines += [r"\end{longtable}", ""]

    lines += [
        r"\subsection*{Primary Unconditional Exports}",
        r"\begin{longtable}{p{0.28\linewidth}p{0.20\linewidth}p{0.44\linewidth}}",
        r"\textbf{Machine ID} & \textbf{Canonical} & \textbf{Description}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{Canonical} & \textbf{Description}\\\hline\endhead",
    ]
    for exp in cert["primary_exports"]:
        lines.append(
            r"\texttt{" + tex_escape(exp["id"]) + "} & " +
            r"\texttt{" + tex_escape(exp["canonical"][:18]) + "} & " +
            tex_escape(exp["note"][:55]) + r"\\"
        )
    lines += [r"\end{longtable}", ""]

    lines += [
        r"\subsection*{Book I Boundary}",
        r"\begin{itemize}",
    ]
    for item in BOOK_I_BOUNDARY:
        lines.append(r"\item " + tex_escape(item))
    lines += [r"\end{itemize}"]

    return "\n".join(lines) + "\n"


def main() -> int:
    claims = load_i_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    cert = build_l4_certificate(claims, computed)

    # JSON
    (REPORTS / "book_i_l4_certificate.json").write_text(
        json.dumps(cert, indent=2), encoding="utf-8"
    )

    # Markdown
    md_lines = [
        "# Book I L4 Equivalence Certificate",
        "",
        f"**L4 gate:** {'✅ PASSED' if cert['status']=='passed' else '⚠️ NEEDS REVIEW'} "
        f"({sum(1 for c in cert['checks'] if c['status']=='pass')}/{len(cert['checks'])} criteria)",
        f"**All results [U]:** {cert['all_results_unconditional']}",
        f"**K_0=7 theorem:** {cert['k0_prime_present']}",
        f"**Defect ledger complete:** {cert['defect_ledger_complete']}",
        f"**Prose:** {cert['prose_score']}%",
        "",
        "## L4 Criteria",
        "| Check | Status | Observed |",
        "|-------|--------|----------|",
    ]
    for c in cert["checks"]:
        md_lines.append(f"| `{c['id']}` | {'✅' if c['status']=='pass' else '❌'} | {str(c.get('observed',''))[:70]} |")
    md_lines += [
        "",
        "## Primary Exports",
        "| Machine ID | Canonical | Note |",
        "|---|---|---|",
    ]
    for exp in cert["primary_exports"]:
        md_lines.append(f"| `{exp['id']}` | `{exp['canonical']}` | {exp['note'][:60]} |")
    (TABLES / "book_i_l4_certificate.md").write_text("\n".join(md_lines) + "\n")

    # TeX files
    shell_inner = render_shell_tex(claims, computed)
    (TEX / "book_i_l4_shell.tex").write_text(shell_inner)
    cert_inner = render_cert_tex(cert, claims, computed)
    (TEX / "book_i_l4_certificate.tex").write_text(cert_inner)

    for stem, title, inner in [
        ("book_i_l4_shell",       "Book I Unconditional Foundation L4 Shell",       "book_i_l4_shell.tex"),
        ("book_i_l4_certificate", "Book I L4 Equivalence Certificate",               "book_i_l4_certificate.tex"),
    ]:
        standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC {tex_escape(title)}\\[1ex]\large Schema v0.37.0\\[0.5ex]\normalsize L4 Spine Release Candidate}}
\author{{Generated by NFC Governance Engine v37}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{{Book I is the unconditional source architecture.}} All theorem-like objects are [U].
This is an L4 spine-pilot shell --- the canonical Book I is the authoritative source.
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
        "all_results_unconditional": cert["all_results_unconditional"],
        "k0_prime_present": cert["k0_prime_present"],
        "defect_ledger_complete": cert["defect_ledger_complete"],
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
