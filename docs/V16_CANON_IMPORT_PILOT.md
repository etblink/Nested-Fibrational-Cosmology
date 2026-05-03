# v16 Canon Import Pilot

v16 adds an import layer for canon-facing governance appendices without migrating
full book prose.

The import layer generates:

- `output/tex/canon_governance_appendix.tex`
- `output/tex/canon_governance_appendix_standalone.tex`
- `output/reports/canon_import_manifest.json`
- `output/tables/canon_import_manifest.md`

The generated appendix contains:

- branch posture reconciliation
- active open items under trace
- current audit issues
- release-diff events
- quality-gate summary

This is deliberately an appendix/status-packet layer. It does not generate theorem
prose, and it does not replace the human-authored branch books.

Run:

```bash
python build/build.py
```

The quality gate now includes `gate.canon_import_packet`, which fails if the import
packet or manifest is missing.
