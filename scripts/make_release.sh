#!/usr/bin/env bash
# MIG-028: package a git-free source archive that still passes `make check`.
# Writes the tracked-text manifest (so check 9 works without git), then zips
# the working tree excluding .git and build cruft.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p release
git ls-files > release/TRACKED_TEXT_MANIFEST.txt
echo "wrote release/TRACKED_TEXT_MANIFEST.txt ($(wc -l < release/TRACKED_TEXT_MANIFEST.txt) entries)"
OUT="${1:-/tmp/NFC_v1.1_maintenance.zip}"
# stage the manifest into the commit-tracked set if it changed
git add release/TRACKED_TEXT_MANIFEST.txt 2>/dev/null || true
( cd .. && zip -qr "$OUT" nfc_working \
    -x "nfc_working/.git/*" "nfc_working/*.aux" "nfc_working/*.log" \
       "nfc_working/*.out" "nfc_working/*.toc" \
       "nfc_working/__pycache__/*" "nfc_working/scripts/__pycache__/*" )
echo "wrote $OUT"
