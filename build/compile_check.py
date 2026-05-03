
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
TEX_DIR = ROOT / "output" / "tex"
PDF_DIR = ROOT / "output" / "pdf"
RENDER_DIR = ROOT / "output" / "pdf_render_check"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"

TARGETS = [
    {
        "id": "canon_governance_appendix",
        "tex": TEX_DIR / "canon_governance_appendix_standalone.tex",
        "pdf": PDF_DIR / "canon_governance_appendix_standalone.pdf",
        "render_dir": RENDER_DIR / "canon_governance_appendix",
    },
    {
        "id": "gr_branch_successor",
        "tex": TEX_DIR / "gr_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "gr_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "gr_branch_successor",
    },
    {
        "id": "ym_branch_successor",
        "tex": TEX_DIR / "ym_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "ym_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "ym_branch_successor",
    },
    {
        "id": "spec_branch_successor",
        "tex": TEX_DIR / "spec_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "spec_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "spec_branch_successor",
    },
    {
        "id": "scc_branch_successor",
        "tex": TEX_DIR / "scc_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "scc_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "scc_branch_successor",
    },
    {
        "id": "cryst_branch_successor",
        "tex": TEX_DIR / "cryst_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "cryst_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "cryst_branch_successor",
    },
    {
        "id": "ling_branch_successor",
        "tex": TEX_DIR / "ling_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "ling_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "ling_branch_successor",
    },
    {
        "id": "bio_branch_successor",
        "tex": TEX_DIR / "bio_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "bio_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "bio_branch_successor",
    },
    {
        "id": "sm_branch_successor",
        "tex": TEX_DIR / "sm_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "sm_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "sm_branch_successor",
    },
    {
        "id": "ns_branch_successor",
        "tex": TEX_DIR / "ns_branch_successor_standalone.tex",
        "pdf": PDF_DIR / "ns_branch_successor_standalone.pdf",
        "render_dir": RENDER_DIR / "ns_branch_successor",
    },
]


def run(cmd: List[str], cwd: Path, env: Dict[str, str] | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=timeout)


def count_pages_with_pdfinfo(pdf_path: Path) -> int | None:
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo or not pdf_path.exists():
        return None
    result = run([pdfinfo, str(pdf_path)], cwd=ROOT)
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def parse_latex_log(log_path: Path) -> Dict[str, Any]:
    text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    return {
        "latex_warnings": text.count("LaTeX Warning:"),
        "overfull_hbox": text.count("Overfull \\hbox"),
        "underfull_hbox": text.count("Underfull \\hbox"),
        "undefined_references": "undefined references" in text.lower(),
    }


def compile_target(target: Dict[str, Any]) -> Dict[str, Any]:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TEXINPUTS"] = str(TEX_DIR) + os.pathsep + env.get("TEXINPUTS", "")

    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        return {
            "id": target["id"],
            "status": "failed",
            "reason": "pdflatex not found",
            "runs": [],
            "pdf_exists": False,
            "pdf_path": None,
            "page_count": None,
            "log_summary": {},
        }

    tex_path: Path = target["tex"]
    pdf_path: Path = target["pdf"]
    if not tex_path.exists():
        return {
            "id": target["id"],
            "status": "failed",
            "reason": f"TeX file missing: {tex_path.relative_to(ROOT)}",
            "runs": [],
            "pdf_exists": False,
            "pdf_path": None,
            "page_count": None,
            "log_summary": {},
        }

    runs = []
    for i in range(2):
        result = run([
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            str(PDF_DIR),
            str(tex_path),
        ], cwd=ROOT, env=env)
        runs.append({
            "run": i + 1,
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-2000:],
            "stderr_tail": result.stderr[-1000:],
        })
        if result.returncode != 0:
            break

    log_path = PDF_DIR / f"{tex_path.stem}.log"
    log_summary = parse_latex_log(log_path)
    return {
        "id": target["id"],
        "status": "passed" if runs and all(r["returncode"] == 0 for r in runs) and pdf_path.exists() else "failed",
        "runs": runs,
        "pdf_exists": pdf_path.exists(),
        "pdf_path": str(pdf_path.relative_to(ROOT)) if pdf_path.exists() else None,
        "page_count": count_pages_with_pdfinfo(pdf_path),
        "log_summary": log_summary,
    }


def render_target(target: Dict[str, Any]) -> Dict[str, Any]:
    """Render the PDF with PyMuPDF for a fast build-time smoke check.

    The earlier pdftoppm path was correct but could be slow in some notebook
    environments. For governance CI, the invariant is simple: the PDF opens and
    at least one page can render to PNG. Full visual regression remains a
    separate PDF-skill workflow.
    """
    pdf_path: Path = target["pdf"]
    render_dir: Path = target["render_dir"]
    if not pdf_path.exists():
        return {"id": target["id"], "status": "skipped", "reason": "PDF missing", "rendered_pages": 0}

    shutil.rmtree(render_dir, ignore_errors=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        rendered = 0
        # Render up to two pages for a quick smoke check.
        for idx in range(min(len(doc), 2)):
            page = doc.load_page(idx)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
            pix.save(str(render_dir / f"page-{idx + 1}.png"))
            rendered += 1
        doc.close()
        return {
            "id": target["id"],
            "status": "passed" if rendered else "failed",
            "returncode": 0 if rendered else 1,
            "rendered_pages": rendered,
            "render_dir": str(render_dir.relative_to(ROOT)),
            "renderer": "pymupdf",
            "stdout_tail": "",
            "stderr_tail": "",
        }
    except Exception as exc:  # pragma: no cover - render smoke failure path
        return {
            "id": target["id"],
            "status": "failed",
            "returncode": 1,
            "rendered_pages": 0,
            "render_dir": str(render_dir.relative_to(ROOT)),
            "renderer": "pymupdf",
            "stderr_tail": f"{type(exc).__name__}: {exc}",
        }


def write_reports(report: Dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    with (REPORTS / "compile_check_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# Compile Check Report",
        "",
        f"**Status:** {report.get('status')}",
        "",
        "| Target | Compile | Render | PDF | Pages | Rendered pages | LaTeX warnings | Overfull | Underfull | Undefined refs |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for target_id, row in report.get("targets", {}).items():
        comp = row.get("compile", {})
        rend = row.get("render", {})
        log = comp.get("log_summary", {})
        lines.append("| " + " | ".join([
            target_id,
            str(comp.get("status")),
            str(rend.get("status")),
            f"`{comp.get('pdf_path')}`",
            str(comp.get("page_count")),
            str(rend.get("rendered_pages")),
            str(log.get("latex_warnings", 0)),
            str(log.get("overfull_hbox", 0)),
            str(log.get("underfull_hbox", 0)),
            str(log.get("undefined_references", False)),
        ]) + " |")
    lines += [
        "",
        "Overfull/underfull box counts are reported for layout review but do not fail the gate unless compilation or rendering fails.",
    ]
    (TABLES / "compile_check_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    target_reports: Dict[str, Dict[str, Any]] = {}
    all_passed = True
    for target in TARGETS:
        compile_result = compile_target(target)
        render_result = render_target(target)
        ok = compile_result.get("status") == "passed" and render_result.get("status") == "passed"
        all_passed = all_passed and ok
        target_reports[target["id"]] = {
            "status": "passed" if ok else "failed",
            "compile": compile_result,
            "render": render_result,
        }

    report = {
        "status": "passed" if all_passed else "failed",
        "targets": target_reports,
        # Backward-compatible top-level fields for existing gates/reports.
        "compile": target_reports.get("canon_governance_appendix", {}).get("compile", {}),
        "render": target_reports.get("canon_governance_appendix", {}).get("render", {}),
    }
    write_reports(report)
    print(json.dumps({
        "status": report["status"],
        "targets": {k: {"status": v["status"], "pdf": v["compile"].get("pdf_path"), "pages": v["compile"].get("page_count")} for k, v in target_reports.items()},
    }, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
