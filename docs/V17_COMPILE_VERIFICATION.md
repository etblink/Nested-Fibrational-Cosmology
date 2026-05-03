# v17 Compile Verification

v17 is a controlled import-layer reliability increment.

It adds a compile verification step for the generated canon-governance appendix:

1. compile `output/tex/canon_governance_appendix_standalone.tex` with `pdflatex`,
2. verify that `output/pdf/canon_governance_appendix_standalone.pdf` exists,
3. render the PDF to page images using the PDF render check,
4. emit machine-readable and Markdown compile reports,
5. enforce the result through `gate.compile_verification`.

This milestone does not expand canon coverage and does not migrate theorem prose. It verifies that the generated governance fragments are not merely present, but actually usable as an importable PDF/status packet.

Expected outputs:

- `output/pdf/canon_governance_appendix_standalone.pdf`
- `output/pdf_render_check/page-1.png`
- `output/reports/compile_check_report.json`
- `output/tables/compile_check_report.md`

Overfull and underfull box counts are surfaced for layout review. They are not build failures unless compilation or rendering fails.
