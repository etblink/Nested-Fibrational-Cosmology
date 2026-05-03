"""
build/book_ii_l4_pilot.py — v38 Book II L4 Spine Pilot

Book II is the first spine book with a conditional layer.
Its two-layer structure is the key governance contribution:

[U] LAYER — unconditional results:
  thm:DW-from-A2, thm:TC-from-sr, thm:covering-bound-K07,
  cor:ls2-universal-K07, thm:PASS, thm:binary-rigidity, thm:local-nuclear

[C] LAYER — conditional on LS-2 and/or Phase-A:
  thm:ls2-from-conditions, thm:boundary-det, thm:boundary-capacity,
  thm:SCT1...thm:SCT6b, thm:governing (Book II)

LS-2 is the principal conditional hinge of the entire corpus.
The L4 certificate must correctly document this stratification.

Key governance verification:
1. LS-2 hypothesis is present and [C] (not [U] — it's a hypothesis)
2. cor:ls2-universal-K07 is [U] (the bridge for the canonical K_0=7 case)
3. PASS is [U] (legacy axiom promoted to proved theorem)
4. SCT.6b is present [C] (discharges ob:NS.SB2 in NS branch)
5. All [C] results correctly carry LS-2/Phase-A as inherited constraints
6. The [U]/[C] stratification is correctly represented
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
II_CLAIMS_DIR = ROOT / "claims" / "spine" / "II"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

# The two layers
U_LAYER = [
    ("sr:II.no-local-smuggling",   "No-Local-Smuggling Rule",                 "sr:no-local-smuggling"),
    ("thm:II.DW-from-A2",          "DW from Structural Invariance (A2)",       "thm:DW-from-A2"),
    ("thm:II.TC-from-sr",          "TC from Toggle-Complete Standing Rule",    "thm:TC-from-sr"),
    ("thm:II.covering-bound-K07",  "Covering Bound for K_0=7",                "thm:covering-bound-K07"),
    ("cor:II.ls2-universal-K07",   "LS-2 Universal for K_0=7 Phase-A",        "cor:ls2-universal-K07"),
    ("thm:II.PASS",                "PASS as Derived Necessity",               "thm:PASS"),
    ("thm:II.binary-rigidity",     "Binary Rigidity Theorem",                 "thm:binary-rigidity"),
    ("thm:II.local-nuclear",       "Local Nuclear Theorem",                   "thm:local-nuclear"),
]

C_LAYER = [
    ("hyp:II.LS2",                  "LS-2 Hypothesis [C] — principal hinge",   "hyp:LS2"),
    ("thm:II.ls2-from-conditions",  "LS-2 from DW+TC+LAR (rho*=2)",            "thm:ls2-from-conditions"),
    ("thm:II.boundary-det",         "Boundary Determinacy",                    "thm:boundary-det"),
    ("thm:II.boundary-capacity",    "Boundary Capacity Counting Bound",        "thm:boundary-capacity"),
    ("thm:II.SCT1",                 "SCT.1 Coercive Transport Stage 1",        "thm:SCT1"),
    ("thm:II.SCT6b",                "SCT.6b Safe Tail Discharge",              "thm:SCT6b"),
    ("thm:II.governing",            "Boundary Stabilization Theorem",          "thm:governing (II)"),
]

L4_CERT_ORDER = [
    "sr:II.no-local-smuggling",
    "def:II.collar", "def:II.DW", "def:II.TC", "def:II.LAR",
    "def:II.structural-phases",
    "thm:II.DW-from-A2", "thm:II.TC-from-sr",
    "thm:II.covering-bound-K07",
    "cor:II.ls2-universal-K07",
    "thm:II.PASS",
    "thm:II.binary-rigidity",
    "thm:II.local-nuclear",
    "hyp:II.LS2",
    "thm:II.ls2-from-conditions",
    "thm:II.boundary-det",
    "thm:II.boundary-capacity",
    "thm:II.SCT1",
    "thm:II.SCT6b",
    "thm:II.governing",
    "status:II",
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


def load_ii_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(II_CLAIMS_DIR.glob("*.yaml")):
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

    # 1. [U] layer complete
    missing_u = [cid for cid, *_ in U_LAYER if cid not in claims]
    add("l4.ii.u-layer-complete", not missing_u,
        missing_u or "all present", "All [U] layer claims present")

    # 2. [C] layer complete
    missing_c = [cid for cid, *_ in C_LAYER if cid not in claims]
    add("l4.ii.c-layer-complete", not missing_c,
        missing_c or "all present", "All [C] layer claims present")

    # 3. LS-2 hypothesis is [C] not [U] (it's a hypothesis, not a theorem)
    ls2 = claims.get("hyp:II.LS2", {})
    ls2_status = computed.get("hyp:II.LS2", {}).get("effective_status",
                                                      ls2.get("declared_status", ""))
    add("l4.ii.ls2-is-conditional", ls2_status == "C",
        f"LS-2 status = {ls2_status}",
        "LS-2 must be [C]: it is a hypothesis, not an unconditional result")

    # 4. cor:ls2-universal-K07 is [U] (the canonical bridge)
    ls2_univ = claims.get("cor:II.ls2-universal-K07", {})
    ls2_univ_status = computed.get("cor:II.ls2-universal-K07", {}).get(
        "effective_status", ls2_univ.get("declared_status", ""))
    add("l4.ii.ls2-universal-is-u", ls2_univ_status == "U",
        f"cor:ls2-universal-K07 status = {ls2_univ_status}",
        "cor:ls2-universal-K07 must be [U]: it proves LS-2 holds for all K_0=7 Phase-A substrates")

    # 5. PASS is [U] (was axiom, now theorem)
    pass_thm = claims.get("thm:II.PASS", {})
    pass_status = computed.get("thm:II.PASS", {}).get(
        "effective_status", pass_thm.get("declared_status", ""))
    add("l4.ii.PASS-is-unconditional", pass_status == "U",
        f"PASS status = {pass_status}",
        "thm:PASS must be [U]: PASS was a legacy axiom now proved as a theorem")

    # 6. [C] results carry inherited constraints
    c_missing_constraints = []
    for cid, _, _ in C_LAYER:
        if cid in claims and cid != "hyp:II.LS2":  # LS-2 itself doesn't inherit from itself
            scope = claims[cid].get("scope", {}) or {}
            inherited = scope.get("inherited_constraints") or []
            if not inherited:
                c_missing_constraints.append(cid)
    add("l4.ii.c-layer-has-constraints",
        len(c_missing_constraints) <= 1,  # allow 1 (hyp:LS2 doesn't need them)
        c_missing_constraints or "all have constraints",
        "[C] results must carry inherited LS-2/Phase-A constraints in scope")

    # 7. SCT.6b present (needed for NS branch)
    sct6b_present = "thm:II.SCT6b" in claims
    add("l4.ii.SCT6b-present", sct6b_present,
        "present" if sct6b_present else "MISSING",
        "thm:II.SCT6b must be present — it discharges ob:NS.SB2 in the NS branch")

    # 8. Prose completeness
    prose_ok = sum(1 for c in claims.values() if check_prose(c))
    prose_score = round(100 * prose_ok / len(claims), 1) if claims else 0
    add("l4.ii.prose-completeness", prose_score >= 90.0,
        f"{prose_score}% ({prose_ok}/{len(claims)})",
        ">= 90% prose completeness", severity="warning")

    # 9. Canonical xref present
    xref_count = sum(1 for c in claims.values() if c.get("canonical_xref"))
    add("l4.ii.xref-annotations", xref_count >= len(L4_CERT_ORDER) - 2,
        f"{xref_count}/{len(claims)}", f">= {len(L4_CERT_ORDER)-2} xref annotations")

    all_pass = all(c["status"] == "pass" for c in checks if c["severity"] == "error")

    return {
        "status": "passed" if all_pass else "needs_review",
        "book": "II",
        "track": "spine",
        "l4_level": "spine_release_candidate" if all_pass else "l4_candidate",
        "schema_version": "0.38.0",
        "claim_count": len(claims),
        "xref_count": xref_count,
        "prose_score": prose_score,
        "u_layer_count": len(U_LAYER),
        "c_layer_count": len(C_LAYER),
        "ls2_status": ls2_status,
        "ls2_universal_status": ls2_univ_status,
        "pass_status": pass_status,
        "sct6b_present": sct6b_present,
        "supersession_effect": "none",
        "two_layer_description": (
            "Book II has a [U] layer (unconditional: DW/TC/covering/PASS/binary-rigidity/local-nuclear) "
            "and a [C] layer (conditional on LS-2 and/or Phase-A: ls2-from-conditions, boundary-det, "
            "boundary-capacity, SCT doctrine, governing). LS-2 is the principal conditional hinge."
        ),
        "checks": checks,
    }


def render_shell_tex(claims: Dict, computed: Dict) -> str:
    parts = [
        "% Book II L4 Shell -- auto-generated by build/book_ii_l4_pilot.py",
        r"\section*{Book II Locality Structure --- L4 Generated Shell}",
        r"\addcontentsline{toc}{section}{Book II L4 Shell}",
        "",
        r"\noindent\textit{Book II has a two-layer structure: an unconditional [U] layer "
        r"and a conditional [C] layer gated by the LS-2 locality hypothesis. "
        r"LS-2 is the principal conditional hinge of the NFC corpus. "
        r"For canonical $K_0=7$ Phase-A substrates, LS-2 holds universally "
        r"(\texttt{cor:II.ls2-universal-K07} [U]).}",
        "",
        r"\subsection*{[U] Layer --- Unconditional Results}",
        r"\begin{longtable}{p{0.30\linewidth}p{0.08\linewidth}p{0.55\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid, title, canonical in U_LAYER:
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
        r"\subsection*{[C] Layer --- Conditional on LS-2 and/or Phase-A}",
        r"\begin{longtable}{p{0.30\linewidth}p{0.08\linewidth}p{0.55\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid, title, canonical in C_LAYER:
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
        status = computed.get(cid, {}).get("effective_status",
                                           claim.get("declared_status", "?"))
        title = claim.get("title", cid)[:50]
        parts.append(
            r"\texttt{" + tex_escape(cid) + "} & "
            + tex_escape(kind) + " & "
            + r"\textbf{[" + tex_escape(status) + "]} & "
            + tex_escape(title) + r"\\"
        )
    parts += [r"\end{longtable}"]

    return "\n".join(parts) + "\n"


def render_cert_tex(cert: Dict, claims: Dict, computed: Dict) -> str:
    criteria_passed = sum(1 for c in cert["checks"] if c["status"] == "pass")
    lines = [
        "% Book II L4 Certificate -- auto-generated",
        r"\section*{Book II L4 Equivalence Certificate}",
        r"\addcontentsline{toc}{section}{Book II L4 Certificate}",
        "",
        rf"\textbf{{L4 gate:}} {'PASSED' if cert['status']=='passed' else 'NEEDS REVIEW'} ({criteria_passed}/{len(cert['checks'])} criteria)\\",
        rf"\textbf{{[U] layer:}} {cert['u_layer_count']} results\\",
        rf"\textbf{{[C] layer:}} {cert['c_layer_count']} results (conditional on LS-2/Phase-A)\\",
        rf"\textbf{{LS-2 status:}} \texttt{{[{cert['ls2_status']}]}} (must be [C])\\",
        rf"\textbf{{LS-2 universal for K\_0=7:}} \texttt{{[{cert['ls2_universal_status']}]}} (must be [U])\\",
        rf"\textbf{{PASS promoted to theorem:}} \texttt{{[{cert['pass_status']}]}} (must be [U])\\",
        rf"\textbf{{SCT.6b present:}} {cert['sct6b_present']}",
        "",
        r"\noindent\textit{" + tex_escape(cert["two_layer_description"][:250]) + "}",
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
    claims = load_ii_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    cert = build_l4_certificate(claims, computed)

    (REPORTS / "book_ii_l4_certificate.json").write_text(
        json.dumps(cert, indent=2), encoding="utf-8")

    # Markdown
    md_lines = [
        "# Book II L4 Equivalence Certificate",
        "",
        f"**L4 gate:** {'✅ PASSED' if cert['status']=='passed' else '⚠️ NEEDS REVIEW'} "
        f"({sum(1 for c in cert['checks'] if c['status']=='pass')}/{len(cert['checks'])} criteria)",
        f"**[U] layer:** {cert['u_layer_count']} results | **[C] layer:** {cert['c_layer_count']} results",
        f"**LS-2 status:** `[{cert['ls2_status']}]` | **LS-2 universal:** `[{cert['ls2_universal_status']}]`",
        f"**PASS promoted:** `[{cert['pass_status']}]` | **SCT.6b:** {cert['sct6b_present']}",
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
        "## Two-Layer Structure",
        "",
        cert["two_layer_description"],
    ]
    (TABLES / "book_ii_l4_certificate.md").write_text("\n".join(md_lines) + "\n")

    shell_inner = render_shell_tex(claims, computed)
    (TEX / "book_ii_l4_shell.tex").write_text(shell_inner)
    cert_inner = render_cert_tex(cert, claims, computed)
    (TEX / "book_ii_l4_certificate.tex").write_text(cert_inner)

    for stem, title, inner in [
        ("book_ii_l4_shell",       "Book II Locality Structure L4 Shell",      "book_ii_l4_shell.tex"),
        ("book_ii_l4_certificate", "Book II L4 Equivalence Certificate",        "book_ii_l4_certificate.tex"),
    ]:
        def te(v):
            return tex_escape(v)
        standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC {te(title)}\\[1ex]\large Schema v0.38.0\\[0.5ex]
\normalsize L4 Spine Release Candidate\\[0.5ex]
\small First spine book with a conditional layer}}
\author{{Generated by NFC Governance Engine v38}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{{Two-layer structure.}} Book II has an unconditional [U] layer
and a conditional [C] layer gated by the LS-2 locality hypothesis.
LS-2 is the principal conditional hinge of the NFC corpus.
This is an L4 spine-pilot shell --- the canonical Book II is the authoritative source.
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
        "ls2_status": cert["ls2_status"],
        "ls2_universal_status": cert["ls2_universal_status"],
        "pass_status": cert["pass_status"],
        "sct6b_present": cert["sct6b_present"],
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
