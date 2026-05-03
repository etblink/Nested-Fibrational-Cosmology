"""
build/book_vi_l4_pilot.py — v41 Book VI L4 Spine Pilot

Book VI (Continuum Bridge) is the tool-licensing book:
  - It establishes WHEN continuum language is lawful (not IF)
  - Its governing theorem (Thm. VI.9.1) is cited by GR and NS branch books
  - It closes the continuum-legitimacy gap in the dependency chain
  - thm:VI.9.1 = thm:VI.governing (Effective Continuum Legitimacy Theorem)

Book VI is architecturally distinctive:
  - Mostly [C]: the biconditionals for differential/integral legitimacy
  - Three [U] results: bridge-schema (structural), no-smuggling (structural),
    T_partial-stability (from K_0=7)
  - Honest posture: thinnest spine book; conceptual weight in definitions

L4 verification:
  1. thm:VI.9.1 = thm:VI.governing is present and [C]
  2. thm:VI.continuum-bridge-schema is [U] (structural — both ingredients required)
  3. thm:VI.no-smuggling is [U] (structural — continuum outside regime = non-canonical)
  4. thm:VI.T-partial-stability is [U] (unconditional from K_0=7)
  5. All four standing rules present
  6. Conditional theorems carry certified-interface-regime constraints
  7. thm:VI.NS-4B-sobolev is [C] (feeds NS branch through Book III ACA chain)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
VI_CLAIMS_DIR = ROOT / "claims" / "spine" / "VI"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

L4_CERT_ORDER = [
    "sr:VI.continuum-earned",
    "sr:VI.no-asymptotic-promotion",
    "sr:VI.no-derivative-without-increment",
    "sr:VI.interface-locality",
    "def:VI.cert-obs-family",
    "def:VI.scale-norm-increment",
    "def:VI.continuum-bridge",
    "def:VI.continuum-interface-regime",
    "def:VI.effective-smooth",
    "thm:VI.continuum-bridge-schema",
    "thm:VI.no-smuggling",
    "thm:VI.T-partial-stability",
    "thm:VI.differential-legitimacy",
    "thm:VI.integral-legitimacy",
    "thm:VI.NS-4B-sobolev",
    "thm:VI.governing",
    "cor:VI.joint-legitimacy",
    "status:VI",
]

MUST_BE_U = ["thm:VI.continuum-bridge-schema", "thm:VI.no-smuggling", "thm:VI.T-partial-stability"]
MUST_BE_C = ["thm:VI.differential-legitimacy", "thm:VI.integral-legitimacy",
             "thm:VI.governing", "cor:VI.joint-legitimacy"]

BRANCHES_CITING_VI91 = ["GR", "NS", "YM"]


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


def load_vi_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for path in sorted(VI_CLAIMS_DIR.glob("*.yaml")):
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

    # 1. thm:VI.governing (= Thm. VI.9.1) is [C]
    gov = claims.get("thm:VI.governing", {})
    gov_status = computed.get("thm:VI.governing", {}).get(
        "effective_status", gov.get("declared_status", ""))
    add("l4.vi.VI91-governing-conditional", gov_status == "C",
        f"thm:VI.governing (= Thm.VI.9.1) status = {gov_status}",
        "thm:VI.governing must be [C] — conditional on certified interface regime")

    # 2. Bridge schema is [U]
    bs = claims.get("thm:VI.continuum-bridge-schema", {})
    bs_status = computed.get("thm:VI.continuum-bridge-schema", {}).get(
        "effective_status", bs.get("declared_status", ""))
    add("l4.vi.bridge-schema-U", bs_status == "U",
        f"thm:VI.continuum-bridge-schema status = {bs_status}",
        "[U]: both ingredients required is a structural fact, not a specific case")

    # 3. No-smuggling is [U]
    ns = claims.get("thm:VI.no-smuggling", {})
    ns_status = computed.get("thm:VI.no-smuggling", {}).get(
        "effective_status", ns.get("declared_status", ""))
    add("l4.vi.no-smuggling-U", ns_status == "U",
        f"thm:VI.no-smuggling status = {ns_status}",
        "[U]: continuum outside regime = non-canonical is a structural fact")

    # 4. T_partial stability is [U]
    tp = claims.get("thm:VI.T-partial-stability", {})
    tp_status = computed.get("thm:VI.T-partial-stability", {}).get(
        "effective_status", tp.get("declared_status", ""))
    add("l4.vi.T-partial-stability-U", tp_status == "U",
        f"thm:VI.T-partial-stability status = {tp_status}",
        "[U]: unconditional from K_0=7 (thm:I.K0-prime)")

    # 5. All four standing rules present
    srs = ["sr:VI.continuum-earned", "sr:VI.no-asymptotic-promotion",
           "sr:VI.no-derivative-without-increment", "sr:VI.interface-locality"]
    missing_srs = [r for r in srs if r not in claims]
    add("l4.vi.standing-rules", not missing_srs,
        missing_srs or "all 4 present", "All 4 Book VI standing rules present")

    # 6. Conditional theorems carry interface constraints
    c_missing_constraints = [
        cid for cid in MUST_BE_C
        if cid in claims and not (claims[cid].get("scope", {}) or {}).get("inherited_constraints")
    ]
    add("l4.vi.c-layer-has-constraints", not c_missing_constraints,
        c_missing_constraints or "all have constraints",
        "[C] theorems must carry certified-interface-regime constraints")

    # 7. NS-4B Sobolev present and [C]
    nb = claims.get("thm:VI.NS-4B-sobolev", {})
    nb_status = computed.get("thm:VI.NS-4B-sobolev", {}).get(
        "effective_status", nb.get("declared_status", ""))
    add("l4.vi.NS-4B-sobolev-conditional", nb_status == "C",
        f"thm:VI.NS-4B-sobolev status = {nb_status}",
        "[C]: NS-4B Sobolev surrogate conditional on K_0=7+Phase-A+BUO+ACA")

    # 8. Closes the VI.9.1 citation gap (GR branch imports thm:VI.9.1)
    gr_vi91 = load_yaml(ROOT / "claims" / "branches" / "GR" / "thm_VI_9_1_stub.yaml")
    gr_vi91_body = gr_vi91.get("body_file", "")
    gap_closed = "text/spine/VI" in gr_vi91_body
    add("l4.vi.VI91-citation-gap-closed", gap_closed,
        f"GR thm:VI.9.1 body_file = {gr_vi91_body}",
        "GR branch thm:VI.9.1 stub should point to Book VI text (text/spine/VI/...)")

    # 9. Prose and xref
    prose_ok = sum(1 for c in claims.values() if check_prose(c))
    prose_score = round(100 * prose_ok / len(claims), 1) if claims else 0
    add("l4.vi.prose-completeness", prose_score >= 90.0,
        f"{prose_score}% ({prose_ok}/{len(claims)})",
        ">= 90% prose", severity="warning")

    xref_count = sum(1 for c in claims.values() if c.get("canonical_xref"))
    add("l4.vi.xref-annotations", xref_count >= len(L4_CERT_ORDER) - 2,
        f"{xref_count}/{len(claims)}", f">= {len(L4_CERT_ORDER)-2} xrefs")

    all_pass = all(c["status"] == "pass" for c in checks if c["severity"] == "error")

    return {
        "status": "passed" if all_pass else "needs_review",
        "book": "VI",
        "track": "spine",
        "l4_level": "spine_release_candidate" if all_pass else "l4_candidate",
        "schema_version": "0.41.0",
        "claim_count": len(claims),
        "xref_count": xref_count,
        "prose_score": prose_score,
        "VI91_status": gov_status,
        "bridge_schema_status": bs_status,
        "no_smuggling_status": ns_status,
        "T_partial_status": tp_status,
        "vi91_citation_gap_closed": gap_closed,
        "citing_branches": BRANCHES_CITING_VI91,
        "supersession_effect": "none",
        "honest_posture": (
            "Book VI is the thinnest spine book from source-content perspective. "
            "Its theorems are mostly biconditionals: differential notation is legitimate "
            "iff it encodes the right thing; integral notation is legitimate iff it "
            "encodes the right thing. The conceptual weight lies in the definitions. "
            "Its job is tool-licensing, not physics."
        ),
        "checks": checks,
    }


def render_shell_tex(claims: Dict, computed: Dict) -> str:
    parts = [
        "% Book VI L4 Shell -- auto-generated by build/book_vi_l4_pilot.py",
        r"\section*{Book VI Continuum Bridge --- L4 Generated Shell}",
        r"\addcontentsline{toc}{section}{Book VI L4 Shell}",
        "",
        r"\noindent\textit{Book~VI is the tool-licensing book. "
        r"It establishes \emph{when} continuum language is lawful. "
        r"The Effective Continuum Legitimacy Theorem (Thm.~VI.9.1 = "
        r"\texttt{thm:VI.governing} [C]) is cited by GR, NS, and YM branch books. "
        r"The Bridge Schema Theorem (\texttt{thm:VI.continuum-bridge-schema} [U]) "
        r"is unconditional: both scoped certificate and separately proved bridge are always required.}",
        "",
        r"\subsection*{Unconditional Results [U]}",
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
        r"\subsection*{Conditional Results [C] — Within a Certified Interface Regime}",
        r"\begin{longtable}{p{0.32\linewidth}p{0.08\linewidth}p{0.53\linewidth}}",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\",
        r"\hline\endfirsthead",
        r"\textbf{Machine ID} & \textbf{St.} & \textbf{Canonical label}\\\hline\endhead",
    ]
    for cid in MUST_BE_C + ["thm:VI.NS-4B-sobolev"]:
        claim = claims.get(cid, {})
        status = computed.get(cid, {}).get("effective_status", claim.get("declared_status", "?"))
        xref = claim.get("canonical_xref", {})
        label = xref.get("canonical_label", claim.get("title", cid))[:55]
        parts.append(r"\texttt{" + tex_escape(cid) + "} & [" +
                     tex_escape(status) + "] & " + tex_escape(label) + r"\\")
    parts += [r"\end{longtable}", ""]

    parts += [
        r"\subsection*{Thm.~VI.9.1 Citation Closure}",
        r"\noindent \texttt{thm:VI.governing} (= Thm.~VI.9.1, Effective Continuum Legitimacy Theorem) "
        r"is cited by: "
        + ", ".join(r"\texttt{" + tex_escape(b) + "}" for b in BRANCHES_CITING_VI91)
        + r".",
        r"With Book~VI machine records, the GR branch book import "
        r"(\texttt{thm:VI.9.1} = Thm.~VI.9.1) now resolves to a machine record "
        r"with a canonical cross-reference annotation and a body text stub.",
        "",
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
        "% Book VI L4 Certificate -- auto-generated",
        r"\section*{Book VI L4 Equivalence Certificate}",
        r"\addcontentsline{toc}{section}{Book VI L4 Certificate}",
        "",
        rf"\textbf{{L4 gate:}} {'PASSED' if cert['status']=='passed' else 'NEEDS REVIEW'} ({criteria_passed}/{len(cert['checks'])} criteria)\\",
        rf"\textbf{{Thm.~VI.9.1 (governing):}} \texttt{{[{cert['VI91_status']}]}} (must be [C])\\",
        rf"\textbf{{Bridge schema:}} \texttt{{[{cert['bridge_schema_status']}]}} (must be [U])\\",
        rf"\textbf{{No-smuggling:}} \texttt{{[{cert['no_smuggling_status']}]}} (must be [U])\\",
        rf"\textbf{{T\_partial stability:}} \texttt{{[{cert['T_partial_status']}]}} (must be [U])\\",
        rf"\textbf{{VI.9.1 citation gap closed:}} {cert['vi91_citation_gap_closed']}",
        "",
        r"\noindent\textit{" + tex_escape(cert["honest_posture"][:250]) + "}",
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
    claims = load_vi_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    cert = build_l4_certificate(claims, computed)

    (REPORTS / "book_vi_l4_certificate.json").write_text(
        json.dumps(cert, indent=2), encoding="utf-8")

    md_lines = [
        "# Book VI L4 Equivalence Certificate",
        "",
        f"**L4 gate:** {'✅ PASSED' if cert['status']=='passed' else '⚠️ NEEDS REVIEW'} "
        f"({sum(1 for c in cert['checks'] if c['status']=='pass')}/{len(cert['checks'])} criteria)",
        f"**Thm. VI.9.1:** `[{cert['VI91_status']}]` (must be [C])",
        f"**Bridge schema:** `[{cert['bridge_schema_status']}]` (must be [U])",
        f"**No-smuggling:** `[{cert['no_smuggling_status']}]` (must be [U])",
        f"**T_partial stability:** `[{cert['T_partial_status']}]` (must be [U])",
        f"**VI.9.1 citation gap closed:** {cert['vi91_citation_gap_closed']}",
        "",
        f"> {cert['honest_posture']}",
        "",
        "## L4 Criteria",
        "| Check | Status | Observed |",
        "|-------|--------|----------|",
    ]
    for c in cert["checks"]:
        md_lines.append(f"| `{c['id']}` | {'✅' if c['status']=='pass' else '❌'} | "
                        f"{str(c.get('observed',''))[:70]} |")
    (TABLES / "book_vi_l4_certificate.md").write_text("\n".join(md_lines) + "\n")

    shell_inner = render_shell_tex(claims, computed)
    (TEX / "book_vi_l4_shell.tex").write_text(shell_inner)
    cert_inner = render_cert_tex(cert, claims, computed)
    (TEX / "book_vi_l4_certificate.tex").write_text(cert_inner)

    for stem, title, inner in [
        ("book_vi_l4_shell",       "Book VI Continuum Bridge L4 Shell",    "book_vi_l4_shell.tex"),
        ("book_vi_l4_certificate", "Book VI L4 Equivalence Certificate",   "book_vi_l4_certificate.tex"),
    ]:
        standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC {tex_escape(title)}\\[1ex]\large Schema v0.41.0\\[0.5ex]
\normalsize L4 Spine Release Candidate\\[0.5ex]
\small Closes Thm.~VI.9.1 citation gap for GR, NS, YM branches}}
\author{{Generated by NFC Governance Engine v41}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent\textbf{{Book VI: tool-licensing.}} It establishes \emph{{when}} continuum
language is lawful. Thm.~VI.9.1 (Effective Continuum Legitimacy Theorem) is cited
by the GR, NS, and YM branch books. This is an L4 spine-pilot shell ---
the canonical Book~VI is the authoritative source.
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
        "VI91_status": cert["VI91_status"],
        "bridge_schema_status": cert["bridge_schema_status"],
        "no_smuggling_status": cert["no_smuggling_status"],
        "vi91_citation_gap_closed": cert["vi91_citation_gap_closed"],
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
