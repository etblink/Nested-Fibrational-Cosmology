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

echo "Adversarial validator tests (MIG-032 tampers 1-5; MIG-033 tampers 6-7):"
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

# --- MIG-033 permanent tests ---

# 6. dynamic precision guard tampered: profile.max_scale_ratio 10 -> 1 must be
#    rejected (before MIG-033 the validator checked only max_min_ratio and this
#    tamper passed; the guard feeds the elevated S_m-table precision).
tamper_must_fail "tampered precision-ratio guard (profile.max_scale_ratio -> 1)" metadata/weil_QH3_certificate.json \
  'c["profile"]["max_scale_ratio"]=1'

# 7. non-enclosing displayed interval in prose: reintroduce the MIG-032
#    round-to-nearest display (whose lower endpoint sits ~9.02e-42 above the
#    certified lower endpoint) into the K0-W3 packet; validate.py check 8b must
#    reject it.
text_tamper_must_fail() {
  local desc="$1" target="$2" old="$3" new="$4"
  python3 - "$target" "$old" "$new" << 'PY'
import subprocess, shutil, sys
target, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
shutil.copy(target, target+".advbak")
txt=open(target, encoding="utf-8").read()
if old not in txt:
    shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
    print(f"  tamper setup error: expected string not found in {target}", file=sys.stderr); sys.exit(7)
open(target, "w", encoding="utf-8").write(txt.replace(old, new, 1))
r=subprocess.run(["python3","scripts/validate.py"], capture_output=True, text=True)
shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
sys.exit(0 if r.returncode!=0 else 7)   # want rejection (nonzero validate)
PY
  if [ $? -eq 0 ]; then echo "  PASS (rejected): $desc"; else echo "  FAIL (slipped through): $desc"; fail=1; fi
}
text_tamper_must_fail "non-enclosing displayed interval (MIG-032 round-to-nearest reintroduced)" \
  RESEARCH_PACKET_RH_K0_W3.md \
  '[2.92475687744511383141046e-16, 2.92475687744511383141047e-16]' \
  '[2.924756877445113831410465e-16, 2.924756877445113831410465e-16]'

exit $fail
