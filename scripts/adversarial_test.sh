#!/usr/bin/env bash
# MIG-032: permanent adversarial validator tests. Each tamper MUST be rejected by validate.py.
# Run from repo root. Non-zero exit if any tamper slips through.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
tamper_must_fail() {
  local desc="$1"; shift
  python3 - "$@" << 'PY'
import json, subprocess, shutil, sys
target, mutate = sys.argv[1], sys.argv[2]
shutil.copy(target, target+".advbak")
c=json.load(open(target))
exec(mutate)                      # mutates dict c
json.dump(c, open(target,"w"), indent=2)
r=subprocess.run(["python3","scripts/validate.py"], capture_output=True, text=True)
shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
sys.exit(0 if r.returncode!=0 else 7)   # want rejection (nonzero validate)
PY
  if [ $? -eq 0 ]; then echo "  PASS (rejected): $desc"; else echo "  FAIL (slipped through): $desc"; fail=1; fi
}

echo "Adversarial validator tests (MIG-032):"
# 1. counterfeit H=3 = H=2 payload under H:3 name
tamper_must_fail "counterfeit H=3 (H=2 payload, H:3 name)" metadata/weil_QH3_certificate.json \
  'q2=json.load(open("metadata/weil_QH2_certificate.json")); c["scales"]=q2["scales"]; c["basis"]=q2["basis"]; c["dim"]=q2["dim"]; c["pivots"]=q2["pivots"]'
# 2. broken moment identity
tamper_must_fail "broken moment identity in basis[0]" metadata/weil_QH2_certificate.json \
  'c["basis"][0]=[3,-2,0]'
# 3. PD pivot lower endpoint made nonpositive
tamper_must_fail "PD pivot lower endpoint nonpositive" metadata/weil_QH2_certificate.json \
  'c["pivots"][0]["lower_decimal"]="-1e-50"'
# 4. scale set reordered (violates deterministic Q_height ordering)
tamper_must_fail "scales reordered" metadata/weil_QH3_certificate.json \
  'c["scales"]=[c["scales"][0]]+list(reversed(c["scales"][1:]))'
# 5. dim inconsistent with |Q_H|-2
tamper_must_fail "dim tampered" metadata/weil_QH3_certificate.json \
  'c["dim"]=c["dim"]+1'

exit $fail
