"""
build/connectivity_audit.py — v43 NFC Governance Engine Connectivity Audit

Performs a comprehensive machine-readable audit of the inter-book and
branch-to-spine dependency graph. This is the final governance layer
that verifies structural coherence across the entire claim corpus.

Six audit passes:
  Pass 1 — Branch status citation coverage (all 10 branches must cite
            thm:V.UBLT and thm:VII.6.4 from their status records)
  Pass 2 — Full reachability (every branch status record must transitively
            reach Books I, II, III, IV, V, VII; GR/NS/YM/SM also VI)
  Pass 3 — Status inheritance (no [U] result may depend on [C] or [O])
  Pass 4 — No dangling dependencies (every dep_id must resolve)
  Pass 5 — Spine→Spine edge direction (all forward; lower book → lower book)
  Pass 6 — Canonical xref completeness (≥ 90% of spine records annotated)

Outputs:
  output/reports/connectivity_audit.json
  output/tables/connectivity_audit.md
  output/tex/connectivity_audit.tex
  output/tex/connectivity_audit_standalone.tex
  output/pdf/connectivity_audit_standalone.pdf
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
TEX = ROOT / "output" / "tex"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)

BOOK_ORDER = ["I", "II", "III", "IV", "V", "VI", "VII"]

# Every branch status record must directly cite these
REQUIRED_SPINE_CITATIONS = {
    "thm:V.UBLT": "Universal Branch Legitimacy Theorem — every branch must satisfy 5 conditions",
    "thm:VII.6.4": "Canonical Closure Schema — every branch must declare 5 items",
}

# Expected spine-book reachability from each branch
BRANCHES = ["BIO", "CRYST", "GR", "LING", "NS", "RH", "SCC", "SM", "SPEC", "YM"]
VI_BRANCHES = {"GR", "NS", "YM", "SM"}  # branches that use continuum language
EXPECTED_BOOKS: Dict[str, Set[str]] = {
    b: ({"I", "II", "III", "IV", "V", "VII"} | ({"VI"} if b in VI_BRANCHES else set()))
    for b in BRANCHES
}


def load_all_claims() -> Dict[str, Dict[str, Any]]:
    claims: Dict[str, Dict[str, Any]] = {}
    for book in BOOK_ORDER:
        d = ROOT / "claims" / "spine" / book
        if d.exists():
            for p in sorted(d.glob("*.yaml")):
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
                if data and data.get("id"):
                    data["_spine_book"] = book
                    claims[data["id"]] = data
    branches_dir = ROOT / "claims" / "branches"
    if branches_dir.exists():
        for branch_dir in sorted(branches_dir.iterdir()):
            if branch_dir.is_dir():
                for p in sorted(branch_dir.glob("*.yaml")):
                    data = yaml.safe_load(p.read_text(encoding="utf-8"))
                    if data and data.get("id"):
                        data["_branch"] = branch_dir.name
                        claims[data["id"]] = data
    return claims


def get_reqs(cid: str, claims: Dict) -> List[str]:
    deps = claims.get(cid, {}).get("dependencies") or {}
    return deps.get("requires", []) if isinstance(deps, dict) else []


def transitive_reachable(cid: str, claims: Dict,
                          visited: Set[str] | None = None) -> Set[str]:
    if visited is None:
        visited = set()
    if cid in visited:
        return visited
    visited.add(cid)
    for dep in get_reqs(cid, claims):
        if dep in claims:
            transitive_reachable(dep, claims, visited)
    return visited


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


def run_audit(claims: Dict) -> Dict[str, Any]:
    spine_ids = {cid for cid, c in claims.items() if "_spine_book" in c}
    branch_ids = {cid for cid, c in claims.items() if "_branch" in c}

    issues: List[Dict[str, Any]] = []
    passes: List[Dict[str, Any]] = []

    def issue(severity, check, cid, message, detail=None):
        issues.append({"severity": severity, "check": check, "id": cid,
                       "message": message, "detail": detail or {}})

    def record_pass(pass_id, passed, observed, expected, details=None):
        passes.append({"id": pass_id, "status": "pass" if passed else "fail",
                       "observed": observed, "expected": expected,
                       "details": details or []})

    # ── Pass 1: Branch status citation coverage ──────────────────────────
    p1_details = []
    p1_ok = True
    for branch in BRANCHES:
        status_id = f"status:{branch}"
        reqs = get_reqs(status_id, claims)
        missing = [cid for cid in REQUIRED_SPINE_CITATIONS if cid not in reqs]
        row = {"branch": branch, "status_id": status_id, "missing": missing,
               "ok": not missing}
        p1_details.append(row)
        if missing:
            p1_ok = False
            for m in missing:
                issue("error", "pass1.citation-coverage", status_id,
                      f"{branch} status record missing required spine citation",
                      {"missing_citation": m, "description": REQUIRED_SPINE_CITATIONS[m]})
    record_pass("pass1.citation-coverage", p1_ok,
                f"{sum(1 for d in p1_details if d['ok'])}/{len(BRANCHES)} branches fully cited",
                "All 10 branch status records must cite thm:V.UBLT and thm:VII.6.4",
                p1_details)

    # ── Pass 2: Full reachability ─────────────────────────────────────────
    p2_details = []
    p2_ok = True
    for branch in BRANCHES:
        reachable = transitive_reachable(f"status:{branch}", claims)
        books_reached = sorted({claims[r].get("_spine_book", "?")
                                 for r in reachable if r in spine_ids})
        expected_books = EXPECTED_BOOKS[branch]
        missing_books = sorted(expected_books - set(books_reached))
        row = {"branch": branch, "books_reached": books_reached,
               "expected": sorted(expected_books), "missing": missing_books,
               "ok": not missing_books}
        p2_details.append(row)
        if missing_books:
            p2_ok = False
            issue("error", "pass2.reachability", f"status:{branch}",
                  f"{branch} does not reach spine Books {missing_books}",
                  {"books_reached": books_reached, "missing": missing_books})
    record_pass("pass2.reachability", p2_ok,
                f"{sum(1 for d in p2_details if d['ok'])}/{len(BRANCHES)} branches fully reach spine",
                "Every branch must transitively reach Books I-II-III-IV-V-VII (+ VI for GR/NS/YM/SM)",
                p2_details)

    # ── Pass 3: Status inheritance ────────────────────────────────────────
    violations = []
    for cid, claim in claims.items():
        if claim.get("declared_status") != "U":
            continue
        for dep_id in get_reqs(cid, claims):
            dep = claims.get(dep_id, {})
            dep_status = dep.get("declared_status", "")
            if dep_status in ("C", "O"):
                violations.append({"id": cid, "dep_id": dep_id, "dep_status": dep_status})
                issue("error", "pass3.status-inheritance", cid,
                      f"Illegal promotion: [U] {cid} depends on [{dep_status}] {dep_id}",
                      {"dep_id": dep_id, "dep_status": dep_status})
    record_pass("pass3.status-inheritance", not violations,
                f"{len(violations)} violations" if violations else "0 violations",
                "No [U] claim may depend on a [C] or [O] claim",
                violations[:20])

    # ── Pass 4: No dangling dependencies ─────────────────────────────────
    dangling = []
    for cid, claim in claims.items():
        for dep_id in get_reqs(cid, claims):
            if dep_id not in claims:
                dangling.append({"id": cid, "missing_dep": dep_id})
                issue("error", "pass4.dangling-deps", cid,
                      f"Dangling dependency: {cid} -> {dep_id} (not found)",
                      {"missing_dep": dep_id})
    record_pass("pass4.dangling-deps", not dangling,
                f"{len(dangling)} dangling" if dangling else "0 dangling",
                "All dep_ids must resolve to a known claim", dangling[:20])

    # ── Pass 5: Spine→Spine edge direction ───────────────────────────────
    backward_edges = []
    for cid, claim in claims.items():
        if "_spine_book" not in claim:
            continue
        src_num = BOOK_ORDER.index(claim["_spine_book"])
        for dep_id in get_reqs(cid, claims):
            dep = claims.get(dep_id, {})
            if "_spine_book" not in dep:
                continue
            tgt_num = BOOK_ORDER.index(dep["_spine_book"])
            if tgt_num > src_num:
                backward_edges.append({"id": cid, "dep_id": dep_id,
                                       "src_book": claim["_spine_book"],
                                       "tgt_book": dep["_spine_book"]})
                issue("error", "pass5.edge-direction", cid,
                      f"Backward edge: Book {claim['_spine_book']} -> Book {dep['_spine_book']}",
                      {"dep_id": dep_id})
    record_pass("pass5.edge-direction", not backward_edges,
                f"{len(backward_edges)} backward" if backward_edges else "0 backward",
                "All spine→spine inter-book edges must go to an earlier book number",
                backward_edges)

    # ── Pass 6: Canonical xref completeness ──────────────────────────────
    spine_with_xref = sum(1 for cid in spine_ids
                          if claims[cid].get("canonical_xref"))
    xref_rate = round(100 * spine_with_xref / len(spine_ids), 1) if spine_ids else 0
    spine_missing_xref = [cid for cid in spine_ids
                          if not claims[cid].get("canonical_xref")]
    xref_ok = xref_rate >= 90.0
    if not xref_ok:
        issue("warning", "pass6.xref-completeness", "GLOBAL",
              f"Spine xref completeness {xref_rate}% below 90% threshold",
              {"rate": xref_rate, "missing": spine_missing_xref[:10]})
    record_pass("pass6.xref-completeness", xref_ok,
                f"{xref_rate}% ({spine_with_xref}/{len(spine_ids)} spine records)",
                ">= 90% of spine records have canonical_xref annotations",
                [{"missing_xref": cid} for cid in spine_missing_xref[:10]])

    # ── Edge summary ─────────────────────────────────────────────────────
    branch_to_spine_edges = [
        (cid, dep_id)
        for cid, claim in claims.items() if "_branch" in claim
        for dep_id in get_reqs(cid, claims) if dep_id in spine_ids
    ]
    spine_to_spine_edges = [
        (cid, dep_id, claim["_spine_book"], claims[dep_id]["_spine_book"])
        for cid, claim in claims.items() if "_spine_book" in claim
        for dep_id in get_reqs(cid, claims)
        if dep_id in spine_ids and claims[dep_id]["_spine_book"] != claim["_spine_book"]
    ]

    errors = sum(1 for i in issues if i["severity"] == "error")
    warnings = sum(1 for i in issues if i["severity"] == "warning")
    all_pass = errors == 0

    return {
        "status": "passed" if all_pass else "failed",
        "schema_version": "0.43.0",
        "total_claims": len(claims),
        "spine_records": len(spine_ids),
        "branch_records": len(branch_ids),
        "branch_to_spine_edges": len(branch_to_spine_edges),
        "spine_to_spine_inter_book_edges": len(spine_to_spine_edges),
        "backward_spine_edges": len(backward_edges),
        "dangling_deps": len(dangling),
        "status_inheritance_violations": len(violations),
        "xref_completeness_pct": xref_rate,
        "errors": errors,
        "warnings": warnings,
        "passes": passes,
        "issues": issues[:50],
    }


def render_md(audit: Dict) -> str:
    lines = [
        "# NFC Governance Engine — Connectivity Audit",
        f"**Schema:** {audit['schema_version']} | "
        f"**Status:** {'✅ PASSED' if audit['status']=='passed' else '❌ FAILED'}",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total claims | {audit['total_claims']} |",
        f"| Spine records | {audit['spine_records']} |",
        f"| Branch records | {audit['branch_records']} |",
        f"| Branch→Spine edges | {audit['branch_to_spine_edges']} |",
        f"| Spine→Spine inter-book edges | {audit['spine_to_spine_inter_book_edges']} |",
        f"| Backward spine edges | {audit['backward_spine_edges']} |",
        f"| Dangling deps | {audit['dangling_deps']} |",
        f"| Status inheritance violations | {audit['status_inheritance_violations']} |",
        f"| Xref completeness | {audit['xref_completeness_pct']}% |",
        f"| Errors | {audit['errors']} |",
        f"| Warnings | {audit['warnings']} |",
        "",
        "## Six Audit Passes",
        "| Pass | Status | Observed | Expected |",
        "|------|--------|----------|----------|",
    ]
    for p in audit["passes"]:
        lines.append(f"| `{p['id']}` | {'✅' if p['status']=='pass' else '❌'} | "
                     f"{str(p['observed'])[:60]} | {str(p['expected'])[:60]} |")
    if audit["issues"]:
        lines += ["", "## Issues", "| Severity | Check | ID | Message |",
                  "|----------|-------|-----|---------|"]
        for i in audit["issues"]:
            lines.append(f"| {i['severity']} | `{i['check']}` | "
                         f"`{i['id'][:30]}` | {i['message'][:60]} |")
    lines += ["", "## Reachability Matrix (Pass 2)"]
    for p in audit["passes"]:
        if p["id"] == "pass2.reachability":
            lines += ["| Branch | Books Reached | Expected | OK |",
                      "|--------|--------------|---------|-----|"]
            for d in p.get("details", []):
                lines.append(f"| {d['branch']} | `{d['books_reached']}` | "
                             f"`{d['expected']}` | {'✓' if d['ok'] else '✗'} |")
    return "\n".join(lines) + "\n"


def render_tex(audit: Dict) -> str:
    criteria_passed = sum(1 for p in audit["passes"] if p["status"] == "pass")
    lines = [
        "% Connectivity Audit -- auto-generated by build/connectivity_audit.py",
        r"\section*{NFC Governance Engine --- Connectivity Audit}",
        r"\addcontentsline{toc}{section}{Connectivity Audit}",
        "",
        rf"\noindent\textbf{{Audit status:}} {'PASSED' if audit['status']=='passed' else 'FAILED'} ({criteria_passed}/{len(audit['passes'])} passes) $\cdot$ "
        + tex_escape(f"Schema {audit['schema_version']}"),
        "",
        r"\begin{longtable}{p{0.45\linewidth}p{0.48\linewidth}}",
        r"\textbf{Metric} & \textbf{Value}\\\hline\endfirsthead",
        r"\textbf{Metric} & \textbf{Value}\\\hline\endhead",
    ]
    metrics = [
        ("Total claims", str(audit["total_claims"])),
        ("Spine records", str(audit["spine_records"])),
        ("Branch records", str(audit["branch_records"])),
        ("Branch\\to{}Spine edges", str(audit["branch_to_spine_edges"])),
        ("Spine\\to{}Spine inter-book edges", str(audit["spine_to_spine_inter_book_edges"])),
        ("Backward spine edges", str(audit["backward_spine_edges"])),
        ("Dangling dependencies", str(audit["dangling_deps"])),
        ("Status inheritance violations", str(audit["status_inheritance_violations"])),
        ("Canonical xref completeness", f"{audit['xref_completeness_pct']}\\%"),
        ("Errors", str(audit["errors"])),
        ("Warnings", str(audit["warnings"])),
    ]
    for k, v in metrics:
        lines.append(tex_escape(k) + " & " + tex_escape(v) + r"\\")
    lines += [r"\end{longtable}", ""]

    lines += [
        r"\subsection*{Six Audit Passes}",
        r"\begin{longtable}{p{0.40\linewidth}p{0.08\linewidth}p{0.45\linewidth}}",
        r"\textbf{Pass} & \textbf{St.} & \textbf{Observed}\\\hline\endfirsthead",
        r"\textbf{Pass} & \textbf{St.} & \textbf{Observed}\\\hline\endhead",
    ]
    for p in audit["passes"]:
        badge = r"\checkmark" if p["status"] == "pass" else r"\texttimes"
        lines.append(tex_escape(p["id"]) + " & " + badge + " & " +
                     tex_escape(str(p["observed"])[:60]) + r"\\")
    lines += [r"\end{longtable}", ""]

    lines += [
        r"\subsection*{Pass 2: Reachability Matrix}",
        r"\begin{longtable}{p{0.14\linewidth}p{0.55\linewidth}p{0.10\linewidth}p{0.12\linewidth}}",
        r"\textbf{Branch} & \textbf{Spine Books Reached} & \textbf{St.} & \textbf{Missing}\\\hline\endfirsthead",
        r"\textbf{Branch} & \textbf{Spine Books Reached} & \textbf{St.} & \textbf{Missing}\\\hline\endhead",
    ]
    for p in audit["passes"]:
        if p["id"] == "pass2.reachability":
            for d in p.get("details", []):
                badge = r"\checkmark" if d["ok"] else r"\texttimes"
                lines.append(
                    tex_escape(d["branch"]) + " & " +
                    tex_escape(str(d["books_reached"])) + " & " +
                    badge + " & " +
                    tex_escape(str(d.get("missing", "")) if not d["ok"] else "--") + r"\\"
                )
    lines += [r"\end{longtable}"]

    if audit["issues"]:
        lines += [
            "",
            r"\subsection*{Issues}",
            r"\begin{longtable}{p{0.12\linewidth}p{0.25\linewidth}p{0.55\linewidth}}",
            r"\textbf{Sev.} & \textbf{Check} & \textbf{Message}\\\hline\endfirsthead",
            r"\textbf{Sev.} & \textbf{Check} & \textbf{Message}\\\hline\endhead",
        ]
        for i in audit["issues"][:20]:
            lines.append(tex_escape(i["severity"]) + " & " +
                         tex_escape(i["check"][:25]) + " & " +
                         tex_escape(i["message"][:60]) + r"\\")
        lines += [r"\end{longtable}"]

    return "\n".join(lines) + "\n"


def main() -> int:
    claims = load_all_claims()
    audit = run_audit(claims)

    (REPORTS / "connectivity_audit.json").write_text(
        json.dumps(audit, indent=2), encoding="utf-8")

    md = render_md(audit)
    (TABLES / "connectivity_audit.md").write_text(md, encoding="utf-8")

    inner_tex = render_tex(audit)
    (TEX / "connectivity_audit.tex").write_text(inner_tex, encoding="utf-8")

    standalone = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=0.85in]{{geometry}}
\usepackage{{longtable}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{hyperref}}
\title{{NFC Governance Engine\\[1ex]
Connectivity Audit Report\\[1ex]\large Schema v0.43.0\\[0.5ex]
\normalsize {'PASSED' if audit['status']=='passed' else 'FAILED'} --- {audit['errors']} errors, {audit['warnings']} warnings}}
\author{{Generated by NFC Governance Engine v43}}
\date{{}}
\begin{{document}}
\maketitle
\tableofcontents
\bigskip
\noindent This report documents the results of the six-pass connectivity audit
over the full NFC governance engine claim corpus.
It verifies: branch citation coverage, branch-to-spine reachability,
status inheritance consistency, dependency resolution, spine edge direction,
and canonical cross-reference completeness.
\vspace{{1em}}
\input{{connectivity_audit.tex}}
\end{{document}}
"""
    (TEX / "connectivity_audit_standalone.tex").write_text(standalone, encoding="utf-8")

    print(json.dumps({
        "status": audit["status"],
        "errors": audit["errors"],
        "warnings": audit["warnings"],
        "branch_to_spine_edges": audit["branch_to_spine_edges"],
        "spine_to_spine_inter_book_edges": audit["spine_to_spine_inter_book_edges"],
        "backward_edges": audit["backward_spine_edges"],
        "dangling": audit["dangling_deps"],
        "status_inheritance_violations": audit["status_inheritance_violations"],
        "xref_completeness": audit["xref_completeness_pct"],
    }, indent=2))
    return 0 if audit["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
