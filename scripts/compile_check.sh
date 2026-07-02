#!/usr/bin/env bash
# NFC compile gate. Compiles each canon .tex twice (resolve cross-refs) in isolation.
# Fails (exit 1) if any file has a fatal error or fails to produce a PDF.
# Usage: scripts/compile_check.sh [file1.tex ...]   (default: all 17 canon files)
set -u
CANON=(NFC_Book_I NFC_Book_II NFC_Book_III NFC_Book_IV NFC_Book_V NFC_Book_VI NFC_Book_VII \
       NFC_BIO_Branch NFC_CRYST_Branch NFC_GR_Branch NFC_LING_Branch NFC_NS_Branch \
       NFC_RH_Branch NFC_SCC_Branch NFC_SM_Branch NFC_SPEC_Branch NFC_YM_Branch)
if [ "$#" -gt 0 ]; then FILES=("$@"); else FILES=("${CANON[@]/%/.tex}"); fi
WORK=$(mktemp -d); rc=0
echo "file,exit,pages,fatal"
for f in "${FILES[@]}"; do
  stem="${f%.tex}"; d="$WORK/$stem"; mkdir -p "$d"; cp "$f" "$d/"
  ( cd "$d" && timeout 180 pdflatex -interaction=nonstopmode -halt-on-error "$f" >p1.log 2>&1 \
    && timeout 180 pdflatex -interaction=nonstopmode -halt-on-error "$f" >p2.log 2>&1 )
  ec=$?
  pages=$(grep -oE 'Output written on .*\(([0-9]+) page' "$d/p2.log" | grep -oE '[0-9]+ page' | grep -oE '[0-9]+' | head -1)
  fatal=$(grep -c '^! ' "$d/p2.log" 2>/dev/null)
  echo "$f,$ec,${pages:-0},${fatal:-0}"
  if [ "$ec" -ne 0 ] || [ "${fatal:-0}" -ne 0 ] || [ -z "$pages" ]; then rc=1; fi
done
rm -rf "$WORK"
if [ "$rc" -ne 0 ]; then echo "COMPILE GATE FAILED" >&2; fi
exit $rc
