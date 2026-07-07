#!/usr/bin/env bash
# Permanent adversarial validator tests. Each tamper MUST be rejected by validate.py
# with a genuine VALIDATION FAILURE (not an environment crash). Run from repo root.
# MIG-032 tampers 1-5; MIG-033 6-7; MIG-035 8-11; MIG-036 12 + hardened runner.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0

# MIG-036 (item 4): the harness distinguishes an intended validation rejection from an
# exception/environment crash. A tamper counts as PASS only when ALL hold:
#   (a) the baseline validator succeeds first (exit 0, "VALIDATION PASSED");
#   (b) the tampered validator returns the validation-failure code (exit 1);
#   (c) the expected diagnostic token "VALIDATION FAILED" is present;
#   (d) no Python traceback / uncaught exception appears.

echo "Baseline validator gate (must pass before any tamper is meaningful):"
base=$(python3 scripts/validate.py 2>&1); base_rc=$?
if [ $base_rc -ne 0 ] || ! grep -q "VALIDATION PASSED" <<<"$base" || grep -q "Traceback" <<<"$base"; then
  echo "  ABORT: baseline validation did not cleanly pass (rc=$base_rc). Environment/dependency problem;"
  echo "         adversarial results would be meaningless. First line(s):"
  echo "$base" | tail -5 | sed 's/^/    /'
  exit 2
fi
echo "  baseline PASSED"

_check_tamper_output() {   # $1=rc $2=output $3=desc  -> sets pass/fail
  local rc="$1" out="$2" desc="$3"
  if grep -q "Traceback" <<<"$out"; then
    echo "  FAIL (crashed, not a clean rejection): $desc"; fail=1; return
  fi
  if [ "$rc" -eq 1 ] && grep -q "VALIDATION FAILED" <<<"$out"; then
    echo "  PASS (rejected): $desc"
  else
    echo "  FAIL (slipped through or wrong code rc=$rc): $desc"; fail=1
  fi
}

tamper_must_fail() {
  local desc="$1" target="$2" mutate="$3"
  local out rc
  out=$(python3 - "$target" "$mutate" << 'PY' 2>&1
import json, subprocess, shutil, sys
target, mutate = sys.argv[1], sys.argv[2]
shutil.copy(target, target+".advbak")
try:
    c=json.load(open(target))
    exec(mutate)
    json.dump(c, open(target,"w"), indent=2)
    r=subprocess.run(["python3","scripts/validate.py"], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stdout.write(r.stderr)
    code=r.returncode
finally:
    shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
sys.exit(code)
PY
) ; rc=$?
  _check_tamper_output "$rc" "$out" "$desc"
}

text_tamper_must_fail() {
  local desc="$1" target="$2" old="$3" new="$4"
  local out rc
  out=$(python3 - "$target" "$old" "$new" << 'PY' 2>&1
import subprocess, shutil, sys
target, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
shutil.copy(target, target+".advbak")
try:
    txt=open(target, encoding="utf-8").read()
    if old not in txt:
        print("tamper setup error: expected string not found", file=sys.stderr); code=99
    else:
        open(target,"w",encoding="utf-8").write(txt.replace(old,new,1))
        r=subprocess.run(["python3","scripts/validate.py"], capture_output=True, text=True)
        sys.stdout.write(r.stdout); sys.stdout.write(r.stderr); code=r.returncode
finally:
    shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
sys.exit(code)
PY
) ; rc=$?
  _check_tamper_output "$rc" "$out" "$desc"
}

echo "Adversarial validator tests (MIG-032 1-5; MIG-033 6-7; MIG-035 8-11; MIG-036 12; MIG-037 13-14; MIG-038 15; MIG-040 16; MIG-043 17; MIG-044 18):"
tamper_must_fail "counterfeit H=3 (H=2 payload, H:3 name)" metadata/weil_QH3_certificate.json \
  'q2=json.load(open("metadata/weil_QH2_certificate.json")); c["scales"]=q2["scales"]; c["basis"]=q2["basis"]; c["dim"]=q2["dim"]; c["pivots"]=q2["pivots"]'
tamper_must_fail "broken moment identity in basis[0]" metadata/weil_QH2_certificate.json \
  'c["basis"][0]=[3,-2,0]'
tamper_must_fail "PD pivot lower endpoint nonpositive" metadata/weil_QH2_certificate.json \
  'c["pivots"][0]["lower_decimal"]="-1e-50"'
tamper_must_fail "scales reordered" metadata/weil_QH3_certificate.json \
  'c["scales"]=[c["scales"][0]]+list(reversed(c["scales"][1:]))'
tamper_must_fail "dim tampered" metadata/weil_QH3_certificate.json \
  'c["dim"]=c["dim"]+1'
tamper_must_fail "tampered precision-ratio guard (profile.max_scale_ratio -> 1)" metadata/weil_QH3_certificate.json \
  'c["profile"]["max_scale_ratio"]=1'
text_tamper_must_fail "non-enclosing displayed interval (MIG-032 round-to-nearest reintroduced)" \
  RESEARCH_PACKET_RH_K0_W3.md \
  '[2.92475687744511383141046e-16, 2.92475687744511383141047e-16]' \
  '[2.924756877445113831410465e-16, 2.924756877445113831410465e-16]'
tamper_must_fail "broken Hermitian pair (M[0_1] != M[1_0])" metadata/weil_QH5_certificate.json \
  'b=c["compressed_matrix_balls"]["0_1"]["mid_dyadic"]; b["mantissa"]=str(int(b["mantissa"])+7)'
tamper_must_fail "eigenvalue lower endpoint below zero under all-positive claim" metadata/weil_QH5_certificate.json \
  'c["eigenvalue_enclosures"][0]["lower_decimal"]="-1e-70"'
tamper_must_fail "entry ball narrowed below its dyadic (non-enclosing)" metadata/weil_QH5_certificate.json \
  'e=c["compressed_matrix_balls"]["2_2"]; e["upper_decimal"]=e["lower_decimal"]'
tamper_must_fail "compressed matrix inconsistent with basis (broken moment nullvector)" metadata/weil_QH4_certificate.json \
  'c["basis"][0][0]=c["basis"][0][0]+1'

# 12. MIG-036: sum/product-preserving eigenvalue counterfeit (the verifier's passing
#     attack against trace/det ties). It must now be rejected because the residual
#     certificate binds each interval to the eigenvalues of the serialized A_0.
counterfeit_must_fail() {
  local desc="sum/product-preserving eigenvalue counterfeit (MIG-036)"
  local target="metadata/weil_QH5_certificate.json" out rc
  out=$(python3 - "$target" << 'PY' 2>&1
import json, subprocess, shutil, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 90
target = sys.argv[1]
shutil.copy(target, target+".advbak")
try:
    c = json.load(open(target))
    E = c["eigenvalue_enclosures"]
    mid = lambda e: (D(e["lower_decimal"]) + D(e["upper_decimal"])) / 2
    x, y, z = mid(E[0]), mid(E[1]), mid(E[2])
    xp = 2 * x                       # x' = 2x
    S = x + y + z; P = x * y * z     # preserve sum and product
    b = S - xp; cc = P / xp
    disc = (b * b - 4 * cc).sqrt()
    yp = (b + disc) / 2; zp = (b - disc) / 2
    for i, val in enumerate(sorted([xp, yp, zp])):
        lo = val * D("0.999999999"); hi = val * D("1.000000001")
        E[i]["lower_decimal"] = format(lo, ".40e")
        E[i]["upper_decimal"] = format(hi, ".40e")
    json.dump(c, open(target, "w"), indent=2)
    r = subprocess.run(["python3", "scripts/validate.py"], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stdout.write(r.stderr); code = r.returncode
finally:
    shutil.copy(target+".advbak", target); __import__("os").remove(target+".advbak")
sys.exit(code)
PY
) ; rc=$?
  _check_tamper_output "$rc" "$out" "$desc"
}
counterfeit_must_fail

# --- MIG-037 permanent tests (residual-certificate schema preconditions) ---

# 13. Negate every matrix-entry dyadic radius while preserving Hermitian pairing and the
#     existing decimal endpoints. Must be rejected (negative radius defeats ||R||_inf).
tamper_must_fail "negated matrix-entry dyadic radii (nonnegative-radius precondition)" metadata/weil_QH5_certificate.json \
  'import copy
for _k,_b in c["compressed_matrix_balls"].items():
    _m=_b["radius_dyadic"]["mantissa"]
    if not _m.startswith("-") and _m!="0": _b["radius_dyadic"]["mantissa"]="-"+_m'

# 14. Append one zero dyadic coordinate to each residual witness vector (dimension attack).
#     Must be rejected: v is no longer an element of the m-dimensional matrix space.
tamper_must_fail "surplus witness-vector coordinate (dimension precondition)" metadata/weil_QH4_certificate.json \
  'for _pr in c["eigenvalue_certificate"]["eigenpairs"]:
    _pr["v"].append({"mantissa":"0","exponent":0})'

# --- MIG-038 permanent test (H=6 payload binding) ---

# 15. Alter the first H=6 serialized eigenvalue enclosure so it no longer outward-contains
#     its residual-certified Weyl-widened interval (raise the lower endpoint above the
#     residual-certified widened lower endpoint while keeping it positive and below upper).
tamper_must_fail "H=6 eigenvalue enclosure fails outward containment (payload binding)" metadata/weil_QH6_certificate.json \
  'e=c["eigenvalue_enclosures"][0]
from decimal import Decimal as _D
lo=_D(e["lower_decimal"]); hi=_D(e["upper_decimal"])
e["lower_decimal"]=format(lo + (hi-lo)/2, ".45e")'

# --- MIG-040 permanent test (H=7 matrix-to-residual binding) ---

# 16. Alter an H=7 compressed-matrix midpoint (a diagonal, both triangles for Hermitian
#     symmetry) substantially, keep nonnegative radii and valid outward decimal endpoints,
#     and leave residual witnesses + eigenvalue enclosures unchanged. Rejection must arise
#     downstream from the matrix->residual / spectral binding (the recomputed A_0 no longer
#     matches the certified spectrum), NOT from malformed JSON, broken Hermitian pairing, or
#     a bad decimal enclosure.
tamper_must_fail "H=7 matrix midpoint altered, spectrum unchanged (matrix-to-residual binding)" metadata/weil_QH7_certificate.json \
  'b=c["compressed_matrix_balls"]["5_5"]
rd=b["radius_dyadic"]
from fractions import Fraction as _Fr
_rad=_Fr(int(rd["mantissa"]))*(_Fr(2)**int(rd["exponent"]))
from decimal import Decimal as _D, getcontext as _gc
_gc().prec=80
b["mid_dyadic"]={"mantissa":"1","exponent":-40}
v=_D(2)**-40; _r=_D(int(rd["mantissa"]))*(_D(2)**int(rd["exponent"]))
b["mid_decimal"]=format(v,".45e")
b["lower_decimal"]=format(v-_r-_D(10)**-50,".45e"); b["upper_decimal"]=format(v+_r+_D(10)**-50,".45e")
b["sign_certified"]="positive"'

# --- MIG-043 permanent test (H=8 matrix-to-residual binding) ---

# 17. Same attack against the newly certified H=8 matrix: alter a diagonal midpoint,
#     keep radius/Hermitian/endpoints valid, leave witnesses + enclosures unchanged.
#     Must reject via the residual bound (recomputed A_0 breaks the residual inequality),
#     NOT via syntax, Hermitian pairing, or decimal enclosure.
tamper_must_fail "H=8 matrix midpoint altered, spectrum unchanged (matrix-to-residual binding)" metadata/weil_QH8_certificate.json \
  'b=c["compressed_matrix_balls"]["7_7"]
rd=b["radius_dyadic"]
from decimal import Decimal as _D, getcontext as _gc
_gc().prec=80
b["mid_dyadic"]={"mantissa":"1","exponent":-40}
v=_D(2)**-40; _r=_D(int(rd["mantissa"]))*(_D(2)**int(rd["exponent"]))
b["mid_decimal"]=format(v,".45e")
b["lower_decimal"]=format(v-_r-_D(10)**-50,".45e"); b["upper_decimal"]=format(v+_r+_D(10)**-50,".45e")
b["sign_certified"]="positive"'

# --- MIG-044 permanent test (provenance-binding attack) ---

# 18. Alter the serialized H=8 ordered-witness hash (a single hex character) while leaving
#     the matrix, witness vectors, residual radii, and eigenvalue enclosures byte-identical.
#     Must reject cleanly via the hash-recomputation mismatch (item E.5), not via any other
#     check (matrix/vectors/radii/enclosures are untouched so all other checks still pass).
tamper_must_fail "H=8 ordered-witness hash altered (provenance-binding attack)" metadata/weil_QH8_certificate.json \
  'ec=c["eigenvalue_certificate"]
h=ec["ordered_witness_sha256"]
flipped = ("0" if h[0]!="0" else "1") + h[1:]
ec["ordered_witness_sha256"]=flipped'

exit $fail
