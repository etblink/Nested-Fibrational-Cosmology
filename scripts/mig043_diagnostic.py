#!/usr/bin/env python3
"""MIG-043 Phase A mandatory exact diagnostic driver. Builds each LDL-PD H=8 profile
once, runs the exact residual-resolution diagnostic across eigenvector multipliers
(3,6,12,20), and writes the machine-readable diagnostic artifact. Diagnostic only:
does not generate any positivity certificate."""
import sys, json, time, hashlib, subprocess, os, pickle
sys.set_int_max_str_digits(1000000)  # exact center gaps have multi-thousand-digit num/den
sys.path.insert(0, "scripts")
import weil_engine as W
import flint
from fractions import Fraction as F

H = 8
scales = W.Q_height(H)
V = W.primitive_nullspace_basis(scales)
sfr = [F(s) for s in scales]
max_ratio = max(sfr) / min(sfr)
PROFILES = W.RH_PROFILES  # full authorized ladder
MULTS = (3, 6, 12, 20)

def _mk_ball(man, exp, rman, rexp):
    from flint import arb
    mid = arb(man) * arb(2) ** exp
    rad = arb(rman) * arb(2) ** rexp
    return mid.union(mid + rad).union(mid - rad)

def build_cached(bb, NN, MM):
    """Build (or load) the compressed midpoint+radius matrix, cached to /tmp as exact dyadics."""
    path = f"/tmp/h8_Mm_{bb}_{NN}_{MM}.pkl"
    if os.path.exists(path):
        data = pickle.load(open(path, "rb"))
        flint.ctx.prec = max(bb * 20, 4096)
        Mm = [[_mk_ball(mm[0], mm[1], rr[0], rr[1]) for (mm, rr) in row] for row in data]
        return Mm, True
    Mm = W._build_compressed(H, scales, V, bb, NN, MM)
    data = [[((int(x.mid().man_exp()[0]), int(x.mid().man_exp()[1])),
              (int(x.rad().man_exp()[0]), int(x.rad().man_exp()[1]))) for x in row] for row in Mm]
    pickle.dump(data, open(path, "wb"))
    return Mm, False

def midpoint_hash(Mm):
    h = hashlib.sha256()
    for row in Mm:
        for x in row:
            man, exp = x.mid().man_exp()
            h.update(f"{int(man)}:{int(exp)};".encode())
    return h.hexdigest()

gen_hash = hashlib.sha256(open("scripts/weil_engine.py", "rb").read()).hexdigest()
baseline_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

out = {
    "artifact": "H=8 residual-resolution diagnostic (MIG-043 Phase A); NOT a positivity certificate",
    "baseline_commit": baseline_commit,
    "generator_sha256": gen_hash,
    "H": H, "dim": len(V),
    "max_ratio_exact": [str(max_ratio.numerator), str(max_ratio.denominator)],
    "eigenvector_multipliers": list(MULTS),
    "profiles": [],
}

overall = []
for (bb, NN, MM) in PROFILES:
    entry = {"profile": {"bits": bb, "N": NN, "M": MM}}
    if not (F(NN) > max_ratio):
        entry["disposition"] = "STRUCTURALLY INAPPLICABLE"
        entry["comparison"] = f"N={NN} <= max_ratio={max_ratio}"
        out["profiles"].append(entry); print(f"[{bb},{NN},{MM}] INAPPLICABLE", flush=True); continue
    t = time.time()
    Mm, cached = build_cached(bb, NN, MM)
    piv, st = W.ldl_pivots(Mm)
    entry["ldl_status"] = st
    entry["build_seconds"] = round(time.time() - t, 1)
    entry["cached"] = cached
    print(f"[{bb},{NN},{MM}] {'cache' if cached else 'built'} {entry['build_seconds']}s LDL {st}", flush=True)
    if st != "PD":
        entry["disposition"] = f"LDL {st}"
        out["profiles"].append(entry)
        json.dump(out, open("metadata/weil_QH8_residual_diagnostic.json", "w"), indent=2)
        continue
    entry["midpoint_sha256"] = midpoint_hash(Mm)
    entry["multipliers"] = {}
    for mult in MULTS:
        W_prec = bb * mult
        tc = time.time()
        cand, Rinf = W._candidate_quantities(Mm, bb, mult)
        if cand is None:
            entry["multipliers"][str(mult)] = {"working_precision": W_prec, "error": "zero eigenvector"}
            print(f"    mult {mult}: zero eigenvector", flush=True); continue
        cls = W._classify_candidate(cand, Rinf, W_prec)
        # stringify big ints for JSON safety
        g = F(int(cls["min_center_gap"][0]), int(cls["min_center_gap"][1]))
        cls["min_center_gap"] = [str(g.numerator), str(g.denominator)]
        cls["failing_pairs_at_320"] = [
            [fp[0], fp[1], [str(fp[2][0]), str(fp[2][1])], fp[3]] for fp in cls["failing_pairs_at_320"]
        ]
        cls["working_precision"] = W_prec
        cls["eigenvector_multiplier"] = mult
        cls["Rinf_over_min_gap_float"] = float(Rinf / g)
        entry["multipliers"][str(mult)] = cls
        overall.append(cls["classification"])
        print(f"    mult {mult} W={W_prec}: {cls['classification']}  min_gap={cls['min_gap_float']:.3e}  gap/floor={cls['min_gap_over_floor_float']:.3e}  firstSepB={cls['first_separating_B']}  weylPos={cls['weyl_all_positive_at_first_sep']} ({round(time.time()-tc,1)}s)", flush=True)
    out["profiles"].append(entry)
    json.dump(out, open("metadata/weil_QH8_residual_diagnostic.json", "w"), indent=2)

priority = {"FULLY-SEPARABLE": 3, "QUANTIZATION-LIMITED": 2, "NONPOSITIVE-AFTER-WEYL": 1, "VECTOR-RESIDUAL-LIMITED": 0}
if overall:
    best = max(overall, key=lambda c: priority[c])
    out["overall_classification"] = best
    out["phase_B_authorized"] = best in ("FULLY-SEPARABLE", "QUANTIZATION-LIMITED")
else:
    out["overall_classification"] = "NO-LDL-PD-PROFILE"
    out["phase_B_authorized"] = False
out["diagnostic_sha256"] = hashlib.sha256(
    json.dumps({k: v for k, v in out.items() if k != "diagnostic_sha256"}, sort_keys=True).encode()
).hexdigest()
json.dump(out, open("metadata/weil_QH8_residual_diagnostic.json", "w"), indent=2)
print("OVERALL:", out["overall_classification"], "| Phase B authorized:", out["phase_B_authorized"], flush=True)

