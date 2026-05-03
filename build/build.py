from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "output" / "reports"
TABLES_DIR = ROOT / "output" / "tables"
TEX_DIR = ROOT / "output" / "tex"
PDF_DIR = ROOT / "output" / "pdf"
PDF_RENDER_DIR = ROOT / "output" / "pdf_render_check"
MANIFEST_PATH = ROOT / "output" / "build_manifest.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_step(label: str, module_path: Path) -> Dict[str, Any]:
    """Run a build module in-process.

    v9 avoids subprocess-based build orchestration so the pipeline is faster and
    less exposed to environment startup noise. Individual scripts remain runnable
    directly for debugging.
    """
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        module = load_module(f"nfc_governance_{label}", module_path)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            module.main()
        return {
            "label": label,
            "module": str(module_path.relative_to(ROOT)),
            "returncode": 0,
            "stdout": stdout.getvalue().strip(),
            "stderr": stderr.getvalue().strip(),
        }
    except Exception as exc:  # pragma: no cover - build safety path
        return {
            "label": label,
            "module": str(module_path.relative_to(ROOT)),
            "returncode": 1,
            "stdout": stdout.getvalue().strip(),
            "stderr": (stderr.getvalue() + f"\n{type(exc).__name__}: {exc}").strip(),
        }


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_outputs() -> Dict[str, List[str]]:
    groups = {
        "reports": REPORTS_DIR,
        "tables": TABLES_DIR,
        "tex": TEX_DIR,
        "pdf": PDF_DIR,
        "pdf_render_check": PDF_RENDER_DIR,
    }
    out: Dict[str, List[str]] = {}
    for key, directory in groups.items():
        if directory.exists():
            out[key] = sorted(str(p.relative_to(ROOT)) for p in directory.glob("*") if p.is_file())
        else:
            out[key] = []
    return out


def write_governance_digest(summary: Dict[str, Any], render_summary: Dict[str, Any], audit: Dict[str, Any], computed: Dict[str, Any]) -> None:
    issues = audit.get("issues", [])
    warnings = [i for i in issues if i.get("severity") == "warning"]
    errors = [i for i in issues if i.get("severity") == "error"]
    infos = [i for i in issues if i.get("severity") == "info"]
    active_frontiers = []
    for cid, info in sorted(computed.items()):
        if info.get("effective_status") == "O":
            active_frontiers.append(cid)

    digest = {
        "schema_version": summary.get("schema_version"),
        "build_status": "failed" if errors else "passed-with-warnings" if warnings else "passed",
        "claims_count": summary.get("claims_count", 0),
        "computed_statuses": summary.get("computed_statuses", 0),
        "errors": len(errors),
        "warnings": len(warnings),
        "info": len(infos),
        "tex_files": render_summary.get("tex_files", 0),
        "active_open_items": active_frontiers,
        "top_warning_types": sorted({i.get("type", "") for i in warnings}),
    }
    with (REPORTS_DIR / "governance_digest.json").open("w", encoding="utf-8") as f:
        json.dump(digest, f, indent=2)

    lines = [
        "# Governance Build Digest",
        "",
        f"**Schema version:** {digest['schema_version']}",
        f"**Build status:** {digest['build_status']}",
        f"**Claims:** {digest['claims_count']}",
        f"**Computed statuses:** {digest['computed_statuses']}",
        f"**Errors:** {digest['errors']}",
        f"**Warnings:** {digest['warnings']}",
        f"**Generated TeX files:** {digest['tex_files']}",
        "",
        "## Active open items",
        "",
    ]
    if active_frontiers:
        for item in active_frontiers:
            lines.append(f"- `{item}`")
    else:
        lines.append("_None detected._")

    lines += [
        "",
        "## Warning types",
        "",
    ]
    if digest["top_warning_types"]:
        for item in digest["top_warning_types"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("_None._")
    (TABLES_DIR / "governance_digest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_json_from_stdout(stdout: str) -> Dict[str, Any]:
    if not stdout:
        return {}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {}


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    TEX_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    steps = [
        run_step("validate", ROOT / "build" / "validate.py"),
        run_step("render", ROOT / "build" / "render.py"),
        run_step("gr_pilot_report", ROOT / "build" / "gr_pilot_report.py"),
        run_step("ym_pilot_report", ROOT / "build" / "ym_pilot_report.py"),
        run_step("release_diff", ROOT / "build" / "release_diff.py"),
        run_step("regression_tests", ROOT / "build" / "regression_tests.py"),
    ]

    summary = load_json(REPORTS_DIR / "audit_summary.json")
    audit = load_json(REPORTS_DIR / "audit_report.json")
    computed = load_json(REPORTS_DIR / "computed_statuses.json")

    render_summary: Dict[str, Any] = {}
    for step in steps:
        if step["label"] == "render":
            render_summary = parse_json_from_stdout(step.get("stdout", ""))

    write_governance_digest(summary, render_summary, audit, computed)

    canon_import_step = run_step("canon_import_packet", ROOT / "build" / "canon_import_packet.py")
    steps.append(canon_import_step)

    gr_successor_step = run_step("gr_branch_successor", ROOT / "build" / "gr_branch_successor.py")
    steps.append(gr_successor_step)

    ym_successor_step = run_step("ym_branch_successor", ROOT / "build" / "ym_branch_successor.py")
    steps.append(ym_successor_step)

    spec_successor_step = run_step("spec_branch_successor", ROOT / "build" / "spec_branch_successor.py")
    steps.append(spec_successor_step)

    scc_successor_step = run_step("scc_branch_successor", ROOT / "build" / "scc_branch_successor.py")
    steps.append(scc_successor_step)

    cryst_successor_step = run_step("cryst_branch_successor", ROOT / "build" / "cryst_branch_successor.py")
    steps.append(cryst_successor_step)

    ling_successor_step = run_step("ling_branch_successor", ROOT / "build" / "ling_branch_successor.py")
    steps.append(ling_successor_step)

    bio_successor_step = run_step("bio_branch_successor", ROOT / "build" / "bio_branch_successor.py")
    steps.append(bio_successor_step)

    sm_successor_step = run_step("sm_branch_successor", ROOT / "build" / "sm_branch_successor.py")
    steps.append(sm_successor_step)

    ns_successor_step = run_step("ns_branch_successor", ROOT / "build" / "ns_branch_successor.py")
    steps.append(ns_successor_step)

    rh_successor_step = run_step("rh_branch_successor", ROOT / "build" / "rh_branch_successor.py")
    steps.append(rh_successor_step)

    proof_tree_step = run_step("proof_tree", ROOT / "build" / "proof_tree.py")
    steps.append(proof_tree_step)

    canonical_coverage_step = run_step("canonical_coverage", ROOT / "build" / "canonical_coverage.py")
    steps.append(canonical_coverage_step)

    l3_readiness_step = run_step("l3_readiness", ROOT / "build" / "l3_readiness.py")
    steps.append(l3_readiness_step)

    gr_l3_cert_step = run_step("gr_l3_certificate", ROOT / "build" / "gr_l3_certificate.py")
    steps.append(gr_l3_cert_step)

    multi_branch_cert_step = run_step("multi_branch_certificate", ROOT / "build" / "multi_branch_certificate.py")
    steps.append(multi_branch_cert_step)

    book_vii_l4_step = run_step("book_vii_l4_pilot", ROOT / "build" / "book_vii_l4_pilot.py")
    steps.append(book_vii_l4_step)

    book_i_l4_step = run_step("book_i_l4_pilot", ROOT / "build" / "book_i_l4_pilot.py")
    steps.append(book_i_l4_step)

    book_ii_l4_step = run_step("book_ii_l4_pilot", ROOT / "build" / "book_ii_l4_pilot.py")
    steps.append(book_ii_l4_step)

    book_v_l4_step = run_step("book_v_l4_pilot", ROOT / "build" / "book_v_l4_pilot.py")
    steps.append(book_v_l4_step)

    book_iv_l4_step = run_step("book_iv_l4_pilot", ROOT / "build" / "book_iv_l4_pilot.py")
    steps.append(book_iv_l4_step)

    book_vi_l4_step = run_step("book_vi_l4_pilot", ROOT / "build" / "book_vi_l4_pilot.py")
    steps.append(book_vi_l4_step)

    compile_check_step = run_step("compile_check", ROOT / "build" / "compile_check.py")
    steps.append(compile_check_step)

    gr_l2_step = run_step("gr_l2_hardening", ROOT / "build" / "gr_l2_hardening.py")
    steps.append(gr_l2_step)

    pilot_comparison_step = run_step("pilot_comparison", ROOT / "build" / "pilot_comparison.py")
    steps.append(pilot_comparison_step)

    pilot_standard_step = run_step("pilot_standard", ROOT / "build" / "pilot_standard.py")
    steps.append(pilot_standard_step)

    pilot_intake_step = run_step("pilot_intake", ROOT / "build" / "pilot_intake.py")
    steps.append(pilot_intake_step)

    supersession_step = run_step("supersession_readiness", ROOT / "build" / "supersession_readiness.py")
    steps.append(supersession_step)

    quality_gate_step = run_step("quality_gate", ROOT / "build" / "quality_gate.py")
    steps.append(quality_gate_step)
    quality_gate_report = load_json(REPORTS_DIR / "quality_gate_report.json")
    release_diff_report = load_json(REPORTS_DIR / "release_diff_report.json")
    regression_report = load_json(REPORTS_DIR / "regression_test_report.json")
    compile_check_report = load_json(REPORTS_DIR / "compile_check_report.json")
    gr_successor_report = load_json(REPORTS_DIR / "gr_successor_equivalence_report.json")
    ym_successor_report = load_json(REPORTS_DIR / "ym_successor_equivalence_report.json")
    spec_successor_report = load_json(REPORTS_DIR / "spec_successor_equivalence_report.json")
    scc_successor_report = load_json(REPORTS_DIR / "scc_successor_equivalence_report.json")
    cryst_successor_report = load_json(REPORTS_DIR / "cryst_successor_equivalence_report.json")
    ling_successor_report = load_json(REPORTS_DIR / "ling_successor_equivalence_report.json")
    supersession_report = load_json(REPORTS_DIR / "supersession_readiness_report.json")
    gr_l2_report = load_json(REPORTS_DIR / "gr_l2_hardening_report.json")
    pilot_comparison_report = load_json(REPORTS_DIR / "l2_pilot_comparison_report.json")
    pilot_standard_report = load_json(REPORTS_DIR / "l2_pilot_standard_report.json")
    pilot_intake_report = load_json(REPORTS_DIR / "pilot_intake_report.json")

    manifest = {
        "schema_version": summary.get("schema_version"),
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
        "summary": summary,
        "render_summary": render_summary,
        "quality_gate": quality_gate_report,
        "release_diff": release_diff_report,
        "regression_tests": regression_report,
        "compile_check": compile_check_report,
        "gr_successor_equivalence": gr_successor_report,
        "ym_successor_equivalence": ym_successor_report,
        "spec_successor_equivalence": spec_successor_report,
        "scc_successor_equivalence": scc_successor_report,
        "cryst_successor_equivalence": cryst_successor_report,
        "ling_successor_equivalence": ling_successor_report,
        "supersession_readiness": supersession_report,
        "gr_l2_hardening": gr_l2_report,
        "l2_pilot_comparison": pilot_comparison_report,
        "l2_pilot_standard": pilot_standard_report,
        "pilot_intake": pilot_intake_report,
        "outputs": collect_outputs(),
    }
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    crashed = any(step["returncode"] != 0 for step in steps)
    audit_errors = int(summary.get("errors", 0) or 0)
    build_status = "failed" if crashed or audit_errors else "passed-with-warnings" if summary.get("warnings", 0) else "passed"
    print(json.dumps({
        "schema_version": summary.get("schema_version"),
        "status": build_status,
        "claims_count": summary.get("claims_count", 0),
        "computed_statuses": summary.get("computed_statuses", 0),
        "warnings": summary.get("warnings", 0),
        "errors": audit_errors,
        "quality_gate_status": quality_gate_report.get("status"),
        "release_diff_changes": release_diff_report.get("change_count", 0),
        "release_diff_missing_basis": release_diff_report.get("missing_basis_count", 0),
        "regression_test_status": regression_report.get("status"),
        "regression_test_failures": regression_report.get("failed_count", 0),
        "compile_check_status": compile_check_report.get("status"),
        "gr_successor_equivalence_status": gr_successor_report.get("status"),
        "gr_successor_posture": gr_successor_report.get("posture"),
        "ym_successor_equivalence_status": ym_successor_report.get("status"),
        "ym_successor_posture": ym_successor_report.get("posture"),
        "spec_successor_equivalence_status": spec_successor_report.get("status"),
        "spec_successor_posture": spec_successor_report.get("posture"),
        "scc_successor_equivalence_status": scc_successor_report.get("status"),
        "scc_successor_posture": scc_successor_report.get("posture"),
        "cryst_successor_equivalence_status": cryst_successor_report.get("status"),
        "cryst_successor_posture": cryst_successor_report.get("posture"),
        "ling_successor_equivalence_status": ling_successor_report.get("status"),
        "ling_successor_posture": ling_successor_report.get("posture"),
        "supersession_l1_import_ready": supersession_report.get("l1_import_ready"),
        "supersession_l5_full_ready": supersession_report.get("l5_full_supersession_ready"),
        "gr_l2_hardening_status": gr_l2_report.get("status"),
        "gr_l2_failed_checks": gr_l2_report.get("failed_count"),
        "l2_pilot_comparison_status": pilot_comparison_report.get("status"),
        "l2_pilot_comparison_failed_checks": pilot_comparison_report.get("failed_count"),
        "l2_pilot_standard_status": pilot_standard_report.get("status"),
        "l2_pilot_standard_failed_checks": pilot_standard_report.get("failed_count"),
        "pilot_intake_status": pilot_intake_report.get("status"),
        "pilot_intake_recommended_next": pilot_intake_report.get("recommended_next_pilot"),
        "outputs": collect_outputs(),
    }, indent=2))
    return 1 if crashed or audit_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
