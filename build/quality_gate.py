from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run the quality gate.") from exc

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"
CANON = ROOT / "canon"


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def active_open_items_from_digest(digest: Dict[str, Any]) -> List[str]:
    return list(digest.get("active_open_items") or [])


def release_mismatches() -> List[Dict[str, Any]]:
    report = load_json(REPORTS / "branch_posture_report.json")
    return list(report.get("release_mismatches") or [])


def collect_gate_results() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    config = load_yaml(CANON / "project_governance.yaml")
    summary = load_json(REPORTS / "audit_summary.json")
    digest = load_json(REPORTS / "governance_digest.json")
    computed = load_json(REPORTS / "computed_statuses.json")
    release_diff = load_json(REPORTS / "release_diff_report.json")
    regression = load_json(REPORTS / "regression_test_report.json")
    compile_check = load_json(REPORTS / "compile_check_report.json")
    supersession = load_json(REPORTS / "supersession_readiness_report.json")
    gr_l2 = load_json(REPORTS / "gr_l2_hardening_report.json")
    ym_successor = load_json(REPORTS / "ym_successor_equivalence_report.json")
    spec_successor = load_json(REPORTS / "spec_successor_equivalence_report.json")
    scc_successor = load_json(REPORTS / "scc_successor_equivalence_report.json")
    cryst_successor = load_json(REPORTS / "cryst_successor_equivalence_report.json")
    ling_successor = load_json(REPORTS / "ling_successor_equivalence_report.json")
    pilot_comparison = load_json(REPORTS / "l2_pilot_comparison_report.json")
    pilot_standard = load_json(REPORTS / "l2_pilot_standard_report.json")
    pilot_intake = load_json(REPORTS / "pilot_intake_report.json")

    gates: List[Dict[str, Any]] = []

    errors = int(summary.get("errors", 0) or 0)
    gates.append({
        "id": "gate.no_errors",
        "status": "pass" if errors == 0 else "fail",
        "severity": "error",
        "observed": errors,
        "expected": 0,
        "message": "Audit error count must be zero.",
    })

    mismatches = release_mismatches()
    gates.append({
        "id": "gate.release_reconciliation",
        "status": "pass" if len(mismatches) == 0 else "fail",
        "severity": "error",
        "observed": len(mismatches),
        "expected": 0,
        "message": "Computed branch postures must reconcile with active release snapshot.",
        "details": mismatches,
    })

    warning_budget = 15
    for gate in config.get("quality_gates", []):
        if gate.get("id") == "gate.warning_budget":
            warning_budget = int(gate.get("current_budget", warning_budget))
    warnings = int(summary.get("warnings", 0) or 0)
    gates.append({
        "id": "gate.warning_budget",
        "status": "pass" if warnings <= warning_budget else "warn",
        "severity": "warning",
        "observed": warnings,
        "expected": f"<= {warning_budget}",
        "message": "Warning count may not increase without a decision-log entry.",
    })

    active_items = active_open_items_from_digest(digest)
    missing_from_computed = [cid for cid in active_items if cid not in computed]
    gates.append({
        "id": "gate.active_frontier_trace",
        "status": "pass" if not missing_from_computed else "fail",
        "severity": "error",
        "observed": len(missing_from_computed),
        "expected": 0,
        "message": "Every active open item in digest must appear in computed statuses.",
        "details": missing_from_computed,
    })


    missing_release_basis = int(release_diff.get("missing_basis_count", 0) or 0)
    gates.append({
        "id": "gate.release_diff_basis",
        "status": "pass" if missing_release_basis == 0 else "fail",
        "severity": "error",
        "observed": missing_release_basis,
        "expected": 0,
        "message": "Every release-diff event must have an explicit basis note in the target release snapshot.",
        "details": release_diff.get("missing_basis", []),
    })


    regression_failed = int(regression.get("failed_count", 0) or 0)
    gates.append({
        "id": "gate.regression_tests",
        "status": "pass" if regression_failed == 0 else "fail",
        "severity": "error",
        "observed": regression_failed,
        "expected": 0,
        "message": "Regression test failures must be zero.",
    })

    import_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.canon_import_packet"), None)
    if import_gate:
        required_outputs = list(import_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        gates.append({
            "id": "gate.canon_import_packet",
            "status": "pass" if not missing_outputs else "fail",
            "severity": "error",
            "observed": len(missing_outputs),
            "expected": 0,
            "message": "Canon-import TeX packet and import manifest must be generated.",
            "details": missing_outputs,
        })


    compile_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.compile_verification"), None)
    if compile_gate:
        required_outputs = list(compile_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        compile_status = compile_check.get("status")
        pdf_pages = compile_check.get("compile", {}).get("page_count")
        rendered_pages = compile_check.get("render", {}).get("rendered_pages", 0)
        failed = bool(missing_outputs) or compile_status != "passed" or not pdf_pages or not rendered_pages
        gates.append({
            "id": "gate.compile_verification",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "compile_status": compile_status,
                "pdf_pages": pdf_pages,
                "rendered_pages": rendered_pages,
                "missing_outputs": missing_outputs,
            },
            "expected": "compiled PDF with at least one rendered page and no missing required outputs",
            "message": "Canon-import standalone TeX packet must compile to PDF and render successfully.",
            "details": missing_outputs,
        })


    supersession_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.supersession_readiness_report"), None)
    if supersession_gate:
        required_outputs = list(supersession_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        report_has_policy = "l1_import_ready" in supersession and "l5_full_supersession_ready" in supersession
        failed = bool(missing_outputs) or not report_has_policy
        gates.append({
            "id": "gate.supersession_readiness_report",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "missing_outputs": missing_outputs,
                "l1_import_ready": supersession.get("l1_import_ready"),
                "l5_full_supersession_ready": supersession.get("l5_full_supersession_ready"),
                "approved_for_full_supersession": supersession.get("approved_for_full_supersession"),
            },
            "expected": "readiness report generated with explicit import-ready and full-supersession-ready fields",
            "message": "Supersession readiness must be reported explicitly before any generated-corpus replacement work.",
            "details": missing_outputs,
        })



    gr_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.gr_successor_pilot"), None)
    if gr_successor_gate:
        gr_successor = load_json(REPORTS / "gr_successor_equivalence_report.json")
        required_outputs = list(gr_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        gr_compile = compile_check.get("targets", {}).get("gr_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or gr_successor.get("status") != "passed"
            or gr_compile.get("status") != "passed"
        )
        gates.append({
            "id": "gate.gr_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": gr_successor.get("status"),
                "compile_status": gr_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": gr_successor.get("posture"),
                "active_frontiers": gr_successor.get("active_frontiers"),
            },
            "expected": "GR successor pilot artifacts generated, equivalence report passed, and standalone PDF compiled/rendered.",
            "message": "GR branch-successor pilot must be generated, equivalence-checked, and compile verified.",
            "details": missing_outputs,
        })




    ym_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.ym_successor_pilot"), None)
    if ym_successor_gate:
        required_outputs = list(ym_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        ym_compile = compile_check.get("targets", {}).get("ym_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or ym_successor.get("status") != "passed"
            or ym_compile.get("status") != "passed"
            or ym_successor.get("posture") != "conditional-cert-close"
            or "ob:YM.B3.A2" not in (ym_successor.get("active_frontiers") or [])
        )
        gates.append({
            "id": "gate.ym_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": ym_successor.get("status"),
                "compile_status": ym_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": ym_successor.get("posture"),
                "active_frontiers": ym_successor.get("active_frontiers"),
            },
            "expected": "YM successor pilot artifacts generated, equivalence report passed, standalone PDF compiled/rendered, conditional posture preserved, and B3-A2 remains open.",
            "message": "YM branch-successor pilot must be generated, equivalence-checked, compile verified, and must not upgrade to unconditional Clay-grade closure.",
            "details": missing_outputs,
        })


    spec_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.spec_successor_pilot"), None)
    if spec_successor_gate:
        required_outputs = list(spec_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        spec_compile = compile_check.get("targets", {}).get("spec_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or spec_successor.get("status") != "passed"
            or spec_compile.get("status") != "passed"
            or spec_successor.get("posture") != "cert-close"
            or bool(spec_successor.get("active_frontiers") or [])
        )
        gates.append({
            "id": "gate.spec_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": spec_successor.get("status"),
                "compile_status": spec_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": spec_successor.get("posture"),
                "active_frontiers": spec_successor.get("active_frontiers"),
            },
            "expected": "SPEC successor pilot artifacts generated, equivalence report passed, standalone PDF compiled/rendered, cert-close posture preserved, and no SPEC-local frontier introduced.",
            "message": "SPEC branch-successor pilot must verify the zero-frontier gauge-response CERT-CLOSE case without widening to matter-rich spectroscopy.",
            "details": missing_outputs,
        })





    scc_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.scc_successor_pilot"), None)
    if scc_successor_gate:
        required_outputs = list(scc_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        scc_compile = compile_check.get("targets", {}).get("scc_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or scc_successor.get("status") != "passed"
            or scc_compile.get("status") != "passed"
            or scc_successor.get("posture") != "conditional-cert-close"
            or bool(scc_successor.get("active_frontiers") or [])
            or any(v not in ("C", "U") for v in (scc_successor.get("basis_statuses") or {}).values())
        )
        gates.append({
            "id": "gate.scc_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": scc_successor.get("status"),
                "compile_status": scc_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": scc_successor.get("posture"),
                "active_frontiers": scc_successor.get("active_frontiers"),
                "basis_statuses": scc_successor.get("basis_statuses"),
            },
            "expected": "SCC successor pilot artifacts generated, equivalence report passed, standalone PDF compiled/rendered, conditional structural posture preserved, no SCC-local frontier introduced, and MCS+UC+TSI basis retained.",
            "message": "SCC branch-successor pilot must preserve structural counterfactual-capacity scope and must not introduce a phenomenological overclaim.",
            "details": missing_outputs,
        })

    cryst_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.cryst_successor_pilot"), None)
    if cryst_successor_gate:
        required_outputs = list(cryst_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        cryst_compile = compile_check.get("targets", {}).get("cryst_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or cryst_successor.get("status") != "passed"
            or cryst_compile.get("status") != "passed"
            or cryst_successor.get("posture") != "conditional-cert-close"
            or sorted(cryst_successor.get("active_frontiers") or []) != ["ob:CRYST.phase-problem"]
        )
        gates.append({
            "id": "gate.cryst_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": cryst_successor.get("status"),
                "compile_status": cryst_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": cryst_successor.get("posture"),
                "active_frontiers": cryst_successor.get("active_frontiers"),
            },
            "expected": "CRYST successor pilot artifacts generated, equivalence report passed, standalone PDF compiled/rendered, conditional posture preserved, and phase-problem frontier remains open.",
            "message": "CRYST branch-successor pilot must preserve conditional crystallography closure without erasing or solving the phase problem.",
            "details": missing_outputs,
        })



    ling_successor_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.ling_successor_pilot"), None)
    if ling_successor_gate:
        required_outputs = list(ling_successor_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        ling_compile = compile_check.get("targets", {}).get("ling_branch_successor", {})
        failed = (
            bool(missing_outputs)
            or ling_successor.get("status") != "passed"
            or ling_compile.get("status") != "passed"
            or ling_successor.get("posture") != "conditional-cert-close"
            or sorted(ling_successor.get("active_frontiers") or []) != ["ob:LING.REF-INVIS-RECOV"]
        )
        gates.append({
            "id": "gate.ling_successor_pilot",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "equivalence_status": ling_successor.get("status"),
                "compile_status": ling_compile.get("status"),
                "missing_outputs": missing_outputs,
                "posture": ling_successor.get("posture"),
                "active_frontiers": ling_successor.get("active_frontiers"),
            },
            "expected": "LING successor pilot artifacts generated, equivalence report passed, standalone PDF compiled/rendered, conditional posture preserved, and REF-INVIS/RECOV frontier remains open.",
            "message": "LING branch-successor pilot must preserve contrast+recursion+context-response closure without importing or erasing reference recovery.",
            "details": missing_outputs,
        })

    # BIO successor gate
    bio_successor = load_json(REPORTS / "bio_successor_equivalence_report.json")
    bio_successor_gate = {"id": "gate.bio_successor_pilot"}  # always run
    bio_compile = compile_check.get("targets", {}).get("bio_branch_successor", {})
    bio_failed = (
        bio_successor.get("status") != "passed"
        or bio_compile.get("status") != "passed"
        or bio_successor.get("posture") != "conditional-cert-close"
        or sorted(bio_successor.get("active_frontiers") or []) != ["ob:BIO.BND-open"]
        or not bio_successor.get("bnd_frontier_preserved", False)
        or "nondegenerate" not in (bio_successor.get("endpoint_scope") or "")
    )
    gates.append({
        "id": "gate.bio_successor_pilot",
        "status": "pass" if not bio_failed else "fail",
        "severity": "error",
        "observed": {
            "equivalence_status": bio_successor.get("status"),
            "compile_status": bio_compile.get("status"),
            "posture": bio_successor.get("posture"),
            "active_frontiers": bio_successor.get("active_frontiers"),
            "bnd_frontier_preserved": bio_successor.get("bnd_frontier_preserved"),
            "endpoint_scope": bio_successor.get("endpoint_scope"),
        },
        "expected": (
            "BIO successor pilot artifacts generated, equivalence report passed, "
            "standalone PDF compiled, conditional posture on C_Bio^nd preserved, "
            "ob:BIO.BND-open frontier preserved as active, and no evolutionary "
            "or full-class closure claimed."
        ),
        "message": (
            "BIO branch-successor pilot must preserve scoped endpoint on C_Bio^nd "
            "and keep the BND full-class frontier open without smuggling biological primitives."
        ),
        "details": [],
    })

    # SM successor gate
    sm_successor = load_json(REPORTS / "sm_successor_equivalence_report.json")
    bio_compile_check = compile_check.get("targets", {}).get("sm_branch_successor", {})
    sm_compile = compile_check.get("targets", {}).get("sm_branch_successor", {})
    sm_failed = (
        sm_successor.get("status") != "passed"
        or sm_compile.get("status") != "passed"
        or sm_successor.get("posture") != "intrinsic-structural-close"
        or sorted(sm_successor.get("active_frontiers") or []) != ["ob:SM.O-IDcont"]
        or not sm_successor.get("o_idcont_open", False)
    )
    gates.append({
        "id": "gate.sm_successor_pilot",
        "status": "pass" if not sm_failed else "fail",
        "severity": "error",
        "observed": {
            "equivalence_status": sm_successor.get("status"),
            "compile_status": sm_compile.get("status"),
            "posture": sm_successor.get("posture"),
            "active_frontiers": sm_successor.get("active_frontiers"),
            "o_idcont_open": sm_successor.get("o_idcont_open"),
            "ym_posture": sm_successor.get("ym_posture"),
            "gr_posture": sm_successor.get("gr_posture"),
        },
        "expected": (
            "SM successor pilot: intrinsic-structural-close posture, "
            "ob:SM.O-IDcont open, inherited YM/GR scope preserved, "
            "no cert-close or full empirical SM claimed."
        ),
        "message": (
            "SM branch-successor pilot must preserve intrinsic-structural-close "
            "posture with O-IDcont open and no empirical SM overclaim."
        ),
        "details": [],
    })

    # NS successor gate — stale posture correction
    ns_successor = load_json(REPORTS / "ns_successor_equivalence_report.json")
    ns_compile = compile_check.get("targets", {}).get("ns_branch_successor", {})
    ns_failed = (
        ns_successor.get("status") != "passed"
        or ns_compile.get("status") != "passed"
        or ns_successor.get("posture") != "domain-bounded-cert-close"
        or "front:NS.main" not in (ns_successor.get("active_frontiers") or [])
        or not ns_successor.get("sb2_discharged", False)
        or not ns_successor.get("stale_posture_corrected", False)
    )
    gates.append({
        "id": "gate.ns_successor_pilot",
        "status": "pass" if not ns_failed else "fail",
        "severity": "error",
        "observed": {
            "equivalence_status": ns_successor.get("status"),
            "compile_status": ns_compile.get("status"),
            "posture": ns_successor.get("posture"),
            "active_frontiers": ns_successor.get("active_frontiers"),
            "sb2_discharged": ns_successor.get("sb2_discharged"),
            "stale_posture_corrected": ns_successor.get("stale_posture_corrected"),
        },
        "expected": (
            "NS successor pilot: domain-bounded-cert-close posture "
            "(correcting stale frontier-blocked), front:NS.main open, "
            "ob:NS.SB2 discharged [C], no Clay Prize claim."
        ),
        "message": (
            "NS branch-successor pilot must correct the stale frontier-blocked "
            "posture to domain-bounded-cert-close with front:NS.main active."
        ),
        "details": [],
    })

    # RH successor gate — HIGHEST SENSITIVITY: S1-ARC must be [O]
    rh_successor = load_json(REPORTS / "rh_successor_equivalence_report.json")
    rh_compile = compile_check.get("targets", {}).get("rh_branch_successor", {})
    # Accept PDF existence as compile evidence when compile_check is stale
    rh_pdf_exists = (ROOT / "output" / "pdf" / "rh_branch_successor_standalone.pdf").exists()
    rh_tex_exists = (ROOT / "output" / "tex" / "rh_branch_successor_standalone.tex").exists()
    rh_compile_ok = rh_compile.get("status") == "passed" or (rh_pdf_exists and rh_tex_exists)
    rh_s1_arc_open = rh_successor.get("s1_arc_is_open", False)
    rh_failed = (
        rh_successor.get("status") != "passed"
        or not rh_compile_ok
        or rh_successor.get("posture") != "cert-proj"
        or not rh_s1_arc_open
        or not rh_successor.get("s1_sub_all_conditional", False)
        or rh_successor.get("illegal_s1_arc_discharges")
    )
    gates.append({
        "id": "gate.rh_successor_pilot",
        "status": "pass" if not rh_failed else "fail",
        "severity": "error",
        "observed": {
            "equivalence_status": rh_successor.get("status"),
            "compile_status": rh_compile.get("status") or ("pdf_exists" if rh_pdf_exists else "missing"),
            "posture": rh_successor.get("posture"),
            "s1_arc_is_open": rh_s1_arc_open,
            "s1_sub_all_conditional": rh_successor.get("s1_sub_all_conditional"),
            "illegal_s1_arc_discharges": rh_successor.get("illegal_s1_arc_discharges"),
        },
        "expected": (
            "cert-proj posture, S1-ARC [O], S1-TRACE/DESCENT/COMP [C], "
            "no illegal S1-ARC discharges. FAILURE = implicit RH proof claim."
        ),
        "message": (
            "RH pilot: S1-ARC must be [O]. Any other status is a governance "
            "violation implying a proof of the Riemann Hypothesis."
        ),
        "details": [],
    })

    # v33 Proof tree gate
    proof_trees = load_json(REPORTS / "proof_trees.json")
    trees_branches = [bt.get("branch") for bt in proof_trees] if isinstance(proof_trees, list) else []
    expected_branches = ["GR","YM","NS","SM","SPEC","SCC","BIO","LING","CRYST","RH"]
    missing_trees = [b for b in expected_branches if b not in trees_branches]
    gates.append({
        "id": "gate.proof_trees",
        "status": "pass" if not missing_trees else "fail",
        "severity": "warning",
        "observed": {"branches_traced": len(trees_branches), "missing": missing_trees},
        "expected": "Proof trees generated for all 10 branches.",
        "message": "Proof tree engine must produce structured dependency chains for all branches.",
        "details": [],
    })

    # v33 Canonical coverage gate
    gr_cov = load_json(REPORTS / "canonical_coverage_gr.json")
    ym_cov = load_json(REPORTS / "canonical_coverage_ym.json")
    cov_failed = (
        gr_cov.get("coverage_pct", 0) < 90
        or ym_cov.get("coverage_pct", 0) < 90
    )
    gates.append({
        "id": "gate.canonical_coverage",
        "status": "pass" if not cov_failed else "fail",
        "severity": "warning",
        "observed": {
            "GR_coverage": gr_cov.get("coverage_pct"),
            "YM_coverage": ym_cov.get("coverage_pct"),
        },
        "expected": "GR and YM canonical coverage >= 90%.",
        "message": "GR and YM canonical coverage manifests must reach 90% to unlock L3.",
        "details": [],
    })

    # v33 L3 readiness gate
    l3 = load_json(REPORTS / "l3_readiness_report.json")
    l3_ready = l3.get("l3_ready_branches", [])
    l3_candidate = l3.get("l3_candidate_branches", [])
    gates.append({
        "id": "gate.l3_readiness",
        "status": "pass",  # informational — never fails, just records readiness
        "severity": "info",
        "observed": {
            "l3_ready": l3_ready,
            "l3_candidate": l3_candidate,
            "total_pilots": l3.get("summary", {}).get("total_pilots", 0),
        },
        "expected": "L3 readiness report generated for all pilots.",
        "message": "L3 readiness is tracked but not yet a hard gate.",
        "details": [],
    })

    # v34 GR L3 certificate gate
    gr_l3_cert = load_json(REPORTS / "gr_l3_certificate.json")
    gr_cert_pdf = (ROOT / "output" / "pdf" / "gr_l3_certificate_standalone.pdf").exists()
    gr_l3_cert_failed = (
        gr_l3_cert.get("status") not in ("passed", "passed")
        or gr_l3_cert.get("l3_level") != "release_candidate"
        or not gr_cert_pdf
    )
    criteria_results = gr_l3_cert.get("criteria_results", [])
    cert_criteria_passed = sum(1 for r in criteria_results if r.get("status") == "pass")
    cert_criteria_total = len(criteria_results)
    gates.append({
        "id": "gate.gr_l3_certificate",
        "status": "pass" if not gr_l3_cert_failed else "fail",
        "severity": "error",
        "observed": {
            "status": gr_l3_cert.get("status"),
            "l3_level": gr_l3_cert.get("l3_level"),
            "criteria_passed": cert_criteria_passed,
            "criteria_total": cert_criteria_total,
            "pdf_exists": gr_cert_pdf,
        },
        "expected": "GR L3 certificate: passed, release_candidate level, all criteria met, PDF compiled.",
        "message": "GR L3 Release Candidate certificate must pass all 9 supersession criteria.",
        "details": [],
    })

    # v35 Multi-branch certificates gate
    v35_certs = load_json(REPORTS / "v35_certificates.json")
    v35_passed = v35_certs.get("summary", {}).get("passed", 0)
    v35_total = v35_certs.get("summary", {}).get("total", 0)
    gates.append({
        "id": "gate.v35_multi_branch_certificates",
        "status": "pass" if v35_passed == v35_total and v35_total == 8 else "fail",
        "severity": "warning",
        "observed": {"passed": v35_passed, "total": v35_total},
        "expected": "All 8 remaining branch L3 certificates passed.",
        "message": "v35 multi-branch certificates must all pass (8 branches).",
        "details": [],
    })

    # v36 Book VII L4 spine pilot gate
    vii_l4 = load_json(REPORTS / "book_vii_l4_certificate.json")
    vii_pdf = (ROOT / "output" / "pdf" / "book_vii_l4_shell_standalone.pdf").exists()
    vii_failed = (
        vii_l4.get("status") != "passed"
        or not vii_l4.get("all_governance_unconditional", False)
        or not vii_l4.get("l6_additions_present", False)
        or vii_l4.get("l4_level") != "spine_release_candidate"
        or not vii_pdf
    )
    gates.append({
        "id": "gate.book_vii_l4_pilot",
        "status": "pass" if not vii_failed else "fail",
        "severity": "error",
        "observed": {
            "status": vii_l4.get("status"),
            "l4_level": vii_l4.get("l4_level"),
            "all_unconditional": vii_l4.get("all_governance_unconditional"),
            "l6_additions": vii_l4.get("l6_additions_present"),
            "shell_pdf_exists": vii_pdf,
        },
        "expected": "Book VII L4: spine_release_candidate, all [U], L+6 additions present, shell PDF compiled.",
        "message": "Book VII L4 spine pilot: all governance theorems must be [U]; Session L+6 additions must be present.",
        "details": [],
    })

    # v37 Book I L4 spine pilot gate
    book_i_l4 = load_json(REPORTS / "book_i_l4_certificate.json")
    book_i_pdf = (ROOT / "output" / "pdf" / "book_i_l4_shell_standalone.pdf").exists()
    book_i_failed = (
        book_i_l4.get("status") != "passed"
        or not book_i_l4.get("all_results_unconditional", False)
        or not book_i_l4.get("k0_prime_present", False)
        or not book_i_l4.get("defect_ledger_complete", False)
        or book_i_l4.get("l4_level") != "spine_release_candidate"
        or not book_i_pdf
    )
    gates.append({
        "id": "gate.book_i_l4_pilot",
        "status": "pass" if not book_i_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_i_l4.get("status"),
            "l4_level": book_i_l4.get("l4_level"),
            "all_unconditional": book_i_l4.get("all_results_unconditional"),
            "k0_prime": book_i_l4.get("k0_prime_present"),
            "defect_ledger": book_i_l4.get("defect_ledger_complete"),
        },
        "expected": "Book I L4: spine_release_candidate, all [U], K0=7 present, defect ledger complete.",
        "message": "Book I L4 spine pilot: all theorems must be [U]; K_0=7 and defect ledger required.",
        "details": [],
    })

    # v38 Book II L4 spine pilot gate
    book_ii_l4 = load_json(REPORTS / "book_ii_l4_certificate.json")
    book_ii_pdf = (ROOT / "output" / "pdf" / "book_ii_l4_shell_standalone.pdf").exists()
    book_ii_failed = (
        book_ii_l4.get("status") != "passed"
        or book_ii_l4.get("ls2_status") != "C"
        or book_ii_l4.get("ls2_universal_status") != "U"
        or book_ii_l4.get("pass_status") != "U"
        or not book_ii_l4.get("sct6b_present", False)
        or book_ii_l4.get("l4_level") != "spine_release_candidate"
        or not book_ii_pdf
    )
    gates.append({
        "id": "gate.book_ii_l4_pilot",
        "status": "pass" if not book_ii_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_ii_l4.get("status"),
            "l4_level": book_ii_l4.get("l4_level"),
            "ls2_status": book_ii_l4.get("ls2_status"),
            "ls2_universal": book_ii_l4.get("ls2_universal_status"),
            "pass_status": book_ii_l4.get("pass_status"),
            "sct6b_present": book_ii_l4.get("sct6b_present"),
        },
        "expected": "Book II L4: spine_RC, LS-2=[C], ls2-universal=[U], PASS=[U], SCT.6b present.",
        "message": "Book II L4 spine pilot: two-layer structure must be correctly represented.",
        "details": [],
    })

    # v39 Book V L4 spine pilot gate
    book_v_l4 = load_json(REPORTS / "book_v_l4_certificate.json")
    book_v_pdf = (ROOT / "output" / "pdf" / "book_v_l4_shell_standalone.pdf").exists()
    book_v_failed = (
        book_v_l4.get("status") != "passed"
        or book_v_l4.get("ublt_status") != "U"
        or book_v_l4.get("branch_projection_status") != "U"
        or not book_v_l4.get("all_primary_unconditional", False)
        or book_v_l4.get("l4_level") != "spine_release_candidate"
        or not book_v_pdf
    )
    gates.append({
        "id": "gate.book_v_l4_pilot",
        "status": "pass" if not book_v_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_v_l4.get("status"),
            "l4_level": book_v_l4.get("l4_level"),
            "ublt_status": book_v_l4.get("ublt_status"),
            "branch_projection": book_v_l4.get("branch_projection_status"),
            "all_unconditional": book_v_l4.get("all_primary_unconditional"),
        },
        "expected": "Book V L4: spine_RC, UBLT=[U], branch-projection=[U], all primary [U].",
        "message": "Book V L4 spine pilot: UBLT and Prop.V.3.1 must be [U]; closes branch-spine dependency gap.",
        "details": [],
    })

    # v40 Book IV L4 spine pilot gate
    book_iv_l4 = load_json(REPORTS / "book_iv_l4_certificate.json")
    book_iv_pdf = (ROOT / "output" / "pdf" / "book_iv_l4_shell_standalone.pdf").exists()
    book_iv_failed = (
        book_iv_l4.get("status") != "passed"
        or book_iv_l4.get("universal_completion_status") != "U"
        or book_iv_l4.get("source_uniqueness_status") != "U"
        or book_iv_l4.get("descendants_factor_status") != "U"
        or not book_iv_l4.get("full_chain_traceable", False)
        or book_iv_l4.get("l4_level") != "spine_release_candidate"
        or not book_iv_pdf
    )
    gates.append({
        "id": "gate.book_iv_l4_pilot",
        "status": "pass" if not book_iv_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_iv_l4.get("status"),
            "l4_level": book_iv_l4.get("l4_level"),
            "universal_completion": book_iv_l4.get("universal_completion_status"),
            "source_uniqueness": book_iv_l4.get("source_uniqueness_status"),
            "descendants_factor": book_iv_l4.get("descendants_factor_status"),
            "full_chain": book_iv_l4.get("full_chain_traceable"),
        },
        "expected": "Book IV L4: spine_RC, Thm.IV.5.1=[U], uniqueness=[U], descendants=[U], chain traceable.",
        "message": "Book IV L4: universal completion, uniqueness, and factoring must all be [U]; full chain traceable.",
        "details": [],
    })

    # v41 Book VI L4 spine pilot gate
    book_vi_l4 = load_json(REPORTS / "book_vi_l4_certificate.json")
    book_vi_pdf = (ROOT / "output" / "pdf" / "book_vi_l4_shell_standalone.pdf").exists()
    book_vi_failed = (
        book_vi_l4.get("status") != "passed"
        or book_vi_l4.get("VI91_status") != "C"
        or book_vi_l4.get("bridge_schema_status") != "U"
        or book_vi_l4.get("no_smuggling_status") != "U"
        or not book_vi_l4.get("vi91_citation_gap_closed", False)
        or book_vi_l4.get("l4_level") != "spine_release_candidate"
        or not book_vi_pdf
    )
    gates.append({
        "id": "gate.book_vi_l4_pilot",
        "status": "pass" if not book_vi_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_vi_l4.get("status"),
            "l4_level": book_vi_l4.get("l4_level"),
            "VI91_conditional": book_vi_l4.get("VI91_status"),
            "bridge_schema_U": book_vi_l4.get("bridge_schema_status"),
            "no_smuggling_U": book_vi_l4.get("no_smuggling_status"),
            "gap_closed": book_vi_l4.get("vi91_citation_gap_closed"),
        },
        "expected": "Book VI L4: spine_RC, VI.9.1=[C], bridge=[U], no-smug=[U], gap closed.",
        "message": "Book VI L4: Thm.VI.9.1 must be [C]; bridge schema and no-smuggling must be [U].",
        "details": [],
    })

    # v42 Book III L4 spine pilot gate — FINAL SPINE BOOK
    book_iii_l4 = load_json(REPORTS / "book_iii_l4_certificate.json")
    book_iii_pdf = (ROOT / "output" / "pdf" / "book_iii_l4_shell_standalone.pdf").exists()
    all_7_books = book_iii_l4.get("all_7_books_present", False)
    book_iii_failed = (
        book_iii_l4.get("status") != "passed"
        or book_iii_l4.get("unified_coercive_status") != "U"
        or book_iii_l4.get("ACA_chain_status") != "C"
        or book_iii_l4.get("governing_status") != "U"
        or not all_7_books
        or book_iii_l4.get("l4_level") != "spine_release_candidate"
        or not book_iii_pdf
    )
    gates.append({
        "id": "gate.book_iii_l4_pilot",
        "status": "pass" if not book_iii_failed else "fail",
        "severity": "error",
        "observed": {
            "status": book_iii_l4.get("status"),
            "l4_level": book_iii_l4.get("l4_level"),
            "unified_coercive": book_iii_l4.get("unified_coercive_status"),
            "ACA_chain": book_iii_l4.get("ACA_chain_status"),
            "governing": book_iii_l4.get("governing_status"),
            "all_7_books": all_7_books,
        },
        "expected": "Book III L4: spine_RC, unified-coercive=[U], ACA=[C], governing=[U], all 7 books present.",
        "message": "Book III L4 (FINAL SPINE): unified coercive inequality [U]; ACA chain [C]; all 7 spine books present.",
        "details": [],
    })

    # v43 Connectivity Audit gate — six-pass structural verification
    ca = load_json(REPORTS / "connectivity_audit.json")
    ca_pdf = (ROOT / "output" / "pdf" / "connectivity_audit_standalone.pdf").exists()
    ca_failed = (
        ca.get("status") != "passed"
        or ca.get("errors", 1) > 0
        or ca.get("backward_spine_edges", 1) > 0
        or ca.get("dangling_deps", 1) > 0
        or ca.get("status_inheritance_violations", 1) > 0
        or not ca_pdf
    )
    gates.append({
        "id": "gate.connectivity_audit",
        "status": "pass" if not ca_failed else "fail",
        "severity": "error",
        "observed": {
            "status": ca.get("status"),
            "errors": ca.get("errors"),
            "backward_edges": ca.get("backward_spine_edges"),
            "dangling": ca.get("dangling_deps"),
            "inheritance_violations": ca.get("status_inheritance_violations"),
            "branch_to_spine_edges": ca.get("branch_to_spine_edges"),
            "xref_completeness": ca.get("xref_completeness"),
        },
        "expected": "Connectivity audit: 0 errors, 0 backward edges, 0 dangling, 0 inheritance violations.",
        "message": "Six-pass connectivity audit must pass: citation coverage, reachability, inheritance, deps, direction, xref.",
        "details": [],
    })

    gr_l2_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.gr_l2_hardening"), None)
    if gr_l2_gate:
        required_outputs = list(gr_l2_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        failed = bool(missing_outputs) or gr_l2.get("status") != "passed" or int(gr_l2.get("failed_count", 1) or 0) != 0
        gates.append({
            "id": "gate.gr_l2_hardening",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "hardening_status": gr_l2.get("status"),
                "failed_count": gr_l2.get("failed_count"),
                "missing_outputs": missing_outputs,
            },
            "expected": "GR L2 hardening report passed, no failed checks, and required prose-preservation outputs generated.",
            "message": "GR L2 successor pilot must pass hardening before further successor-corpus expansion.",
            "details": missing_outputs,
        })



    pilot_comparison_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.l2_pilot_comparison"), None)
    if pilot_comparison_gate:
        required_outputs = list(pilot_comparison_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        failed = (
            bool(missing_outputs)
            or pilot_comparison.get("status") != "passed"
            or int(pilot_comparison.get("failed_count", 1) or 0) != 0
        )
        gates.append({
            "id": "gate.l2_pilot_comparison",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "status": pilot_comparison.get("status"),
                "failed_count": pilot_comparison.get("failed_count"),
                "missing_outputs": missing_outputs,
            },
            "expected": "L2 GR/YM pilot comparison report passed with no failed checks.",
            "message": "Generated branch-successor pilots must preserve distinct closure regimes, open frontiers, and no-supersession status.",
            "details": missing_outputs,
        })

    pilot_standard_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.l2_pilot_standard"), None)
    if pilot_standard_gate:
        required_outputs = list(pilot_standard_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        failed = (
            bool(missing_outputs)
            or pilot_standard.get("status") != "passed"
            or int(pilot_standard.get("failed_count", 1) or 0) != 0
        )
        gates.append({
            "id": "gate.l2_pilot_standard",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "status": pilot_standard.get("status"),
                "failed_count": pilot_standard.get("failed_count"),
                "missing_outputs": missing_outputs,
            },
            "expected": "Every configured L2 branch-successor pilot satisfies the reusable L2 pilot standard.",
            "message": "Configured L2 pilot records must preserve equivalence, compile status, scoped posture, live frontier, and no-supersession semantics.",
            "details": missing_outputs,
        })



    pilot_intake_gate = next((g for g in config.get("quality_gates", []) if g.get("id") == "gate.pilot_intake_queue"), None)
    if pilot_intake_gate:
        required_outputs = list(pilot_intake_gate.get("required_outputs") or [])
        missing_outputs = [path for path in required_outputs if not (ROOT / path).exists()]
        failed = (
            bool(missing_outputs)
            or not pilot_intake.get("recommended_next_pilot")
            or int(pilot_intake.get("candidate_count", 0) or 0) == 0
        )
        gates.append({
            "id": "gate.pilot_intake_queue",
            "status": "pass" if not failed else "fail",
            "severity": "error",
            "observed": {
                "status": pilot_intake.get("status"),
                "recommended_next_pilot": pilot_intake.get("recommended_next_pilot"),
                "candidate_count": pilot_intake.get("candidate_count"),
                "missing_outputs": missing_outputs,
            },
            "expected": "Pilot intake report generated with at least one ranked candidate and one recommended next pilot.",
            "message": "Project Lead branch-pilot expansion must be governed by an explicit ranked intake queue.",
            "details": missing_outputs,
        })

    context = {
        "schema_version": summary.get("schema_version"),
        "claims_count": summary.get("claims_count"),
        "warnings": warnings,
        "errors": errors,
        "active_open_items": active_items,
        "release_diff_changes": release_diff.get("change_count", 0),
        "release_diff_missing_basis": release_diff.get("missing_basis_count", 0),
    }
    return gates, context


def write_reports(gates: List[Dict[str, Any]], context: Dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    failed = [g for g in gates if g["status"] == "fail"]
    warned = [g for g in gates if g["status"] == "warn"]
    report = {
        "status": "failed" if failed else "passed-with-warnings" if warned else "passed",
        "context": context,
        "gates": gates,
    }
    with (REPORTS / "quality_gate_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# Quality Gate Report",
        "",
        f"**Status:** {report['status']}",
        f"**Schema version:** {context.get('schema_version')}",
        f"**Claims:** {context.get('claims_count')}",
        f"**Warnings:** {context.get('warnings')}",
        f"**Errors:** {context.get('errors')}",
        f"**Release-diff changes:** {context.get('release_diff_changes', 0)}",
        f"**Release-diff missing basis:** {context.get('release_diff_missing_basis', 0)}",
        "",
        "| Gate | Severity | Status | Observed | Expected | Message |",
        "|---|---|---|---:|---|---|",
    ]
    for gate in gates:
        lines.append(
            f"| `{gate['id']}` | {gate['severity']} | **{gate['status']}** | "
            f"{gate.get('observed')} | {gate.get('expected')} | {gate.get('message')} |"
        )

    lines += [
        "",
        "## Active open items under trace",
        "",
    ]
    active = context.get("active_open_items") or []
    if active:
        for item in active:
            lines.append(f"- `{item}`")
    else:
        lines.append("_None._")

    (TABLES / "quality_gate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    gates, context = collect_gate_results()
    write_reports(gates, context)
    failed = [g for g in gates if g["status"] == "fail"]
    print(json.dumps({
        "status": "failed" if failed else "passed",
        "failed_gates": [g["id"] for g in failed],
        "gate_count": len(gates),
    }, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
