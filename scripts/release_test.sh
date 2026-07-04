#!/usr/bin/env bash
# MIG-028: prove the distributed archive validates independently of Git.
# Extracts to a clean dir, asserts no .git, runs make check, requires success.
set -euo pipefail
ZIP="${1:?usage: release_test.sh <archive.zip>}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
unzip -q "$ZIP" -d "$TMP"
ROOT="$TMP/nfc_working"
[ -d "$ROOT" ] || { echo "FAIL: nfc_working/ not found in archive"; exit 1; }
if [ -d "$ROOT/.git" ]; then echo "FAIL: archive contains a .git directory"; exit 1; fi
echo "no .git present — good; running make check in extracted tree..."
( cd "$ROOT" && make check >/tmp/release_check.log 2>&1 ) \
  && { echo "RELEASE TEST PASS: git-free archive validates"; } \
  || { echo "RELEASE TEST FAIL: make check failed in git-free archive"; tail -20 /tmp/release_check.log; exit 1; }
