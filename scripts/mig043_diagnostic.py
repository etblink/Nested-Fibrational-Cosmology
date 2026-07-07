#!/usr/bin/env python3
"""MIG-043/044 H=8 residual-resolution diagnostic driver (retained per MIG-044 item D as
an explicitly authorized diagnostic driver). Builds each LDL-PD H=8 profile once (cached),
runs the exact residual-resolution diagnostic across eigenvector multipliers (3,6,12,20),
binds every result to the delivered generator via canonical SHA-256 hashing, and identifies
the single completely-bound candidate set that produced the accepted H=8 certificate as the
load-bearing evidence. This is a diagnostic artifact, NOT a positivity certificate; H=8
positivity is established solely by metadata/weil_QH8_certificate.json and the flint-free
validator."""
import sys, json, time, hashlib, subprocess, os, pickle
sys.set_int_max_str_digits(1000000)  # exact quantities have multi-thousand-digit num/den
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

def build_fresh(bb, NN, MM):
    """MIG-044 correction: always rebuild the matrix directly via _build_compressed --
    the SAME function the certificate itself uses. An earlier pickle-cache reconstruction
    (via arb.union of mid+rad/mid-rad) was found to NOT preserve the exact original
    midpoint representation (union re-derives its own internal (mid,rad) approximation,
    which need not bitwise-match the source ball even though the enclosed interval is
    mathematically identical). Since MIG-044 requires bit-exact hash cross-binding to the
    delivered certificate, no reconstruction shortcut is used; every profile is rebuilt
    fresh. This costs some time but guarantees correctness."""
    return W._build_compressed(H, scales, V, bb, NN, MM)

def fr_pair(fr):
    return [str(fr.numerator), str(fr.denominator)]

def stringify_exact_data(cls):
    """Stringify all big-int exact fields in a _classify_candidate result for JSON safety."""
    g = F(int(cls["min_center_gap"][0]), int(cls["min_center_gap"][1]))
    cls["min_center_gap"] = fr_pair(g)
    new_fp = []
    for fp in cls["failing_pairs_at_320"]:
        new_fp.append({
            "indices": fp["indices"],
            "exact_center_gap": [str(fp["exact_center_gap"][0]), str(fp["exact_center_gap"][1])],
            "exact_s": [str(fp["exact_s"][0]), str(fp["exact_s"][1])],
            "exact_w2": [str(fp["exact_w2"][0]), str(fp["exact_w2"][1])],
            "exact_eta2": [[str(x) for x in fp["exact_eta2"][0]], [str(x) for x in fp["exact_eta2"][1]]],
            "exact_rho_at_320": [[str(x) for x in fp["exact_rho_at_320"][0]], [str(x) for x in fp["exact_rho_at_320"][1]]],
            "exact_separation_margin": [str(fp["exact_separation_margin"][0]), str(fp["exact_separation_margin"][1])],
            "separation_margin_float": fp["separation_margin_float"],
        })
    cls["failing_pairs_at_320"] = new_fp
    return cls

# --- generator / commit provenance ---
gen_hash = hashlib.sha256(open("scripts/weil_engine.py", "rb").read()).hexdigest()
baseline_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

# --- read the delivered certificate to identify the load-bearing (profile, mult) combo ---
cert = json.load(open("metadata/weil_QH8_certificate.json"))
cert_profile = cert["profile"]
cert_ec = cert["eigenvalue_certificate"]
load_bearing_profile = (cert_profile["bits"], cert_profile["N"], cert_profile["M"])
load_bearing_mult = cert_ec["eigenvector_multiplier"]
load_bearing_B = cert_ec["residual_resolution_bits"]

out = {
    "artifact": "H=8 residual-resolution diagnostic (MIG-043 Phase A; reconciled MIG-044)",
    "artifact_note": "This is a DIAGNOSTIC artifact, not a positivity certificate. H=8 positivity is established solely by metadata/weil_QH8_certificate.json and the flint-free validator.",
    "canonical_encoding_version": W.CANON_ENCODING_VERSION,
    "baseline_commit": baseline_commit,
    "generator_sha256": gen_hash,
    "H": H, "dim": len(V),
    "max_ratio_exact": [str(max_ratio.numerator), str(max_ratio.denominator)],
    "eigenvector_multipliers": list(MULTS),
    "coverage": "14/16 SUPPLEMENTAL COVERAGE",
    "coverage_note": ("14 of 16 (4 LDL-PD profiles x 4 multipliers) candidate sets were evaluated. "
                      "The 1600-bit profile's multipliers 12 and 20 (working precision 19200 and "
                      "32000 bits) were NOT evaluated: exact-rational candidate arithmetic on "
                      "~2e5-bit integers at that combination is computationally infeasible in this "
                      "environment. This sweep is SUPPLEMENTAL diagnostic evidence corroborating "
                      "that the quantization floor -- not a genuine spectral cluster -- was the "
                      "obstruction; it is NOT claimed as exhaustive coverage of every multiplier at "
                      "every LDL-PD profile. The load-bearing evidence for H=8 certification is the "
                      "single completely-bound candidate set identified below (load_bearing_candidate), "
                      "which independently demonstrates failure at B=320, separation at the selected "
                      "B, exact residual inequalities, and strict Weyl positivity, and whose matrix "
                      "and witness hashes are cross-bound to the delivered certificate."),
    "load_bearing_candidate_ref": {
        "profile": {"bits": load_bearing_profile[0], "N": load_bearing_profile[1], "M": load_bearing_profile[2]},
        "eigenvector_multiplier": load_bearing_mult,
        "residual_resolution_bits": load_bearing_B,
    },
    "profiles": [],
}

overall = []
load_bearing_section = None
for (bb, NN, MM) in PROFILES:
    entry = {"profile": {"bits": bb, "N": NN, "M": MM}}
    if not (F(NN) > max_ratio):
        entry["disposition"] = "STRUCTURALLY INAPPLICABLE"
        entry["comparison"] = f"N={NN} <= max_ratio={max_ratio}"
        out["profiles"].append(entry); print(f"[{bb},{NN},{MM}] INAPPLICABLE", flush=True); continue
    t = time.time()
    Mm = build_fresh(bb, NN, MM)
    piv, st = W.ldl_pivots(Mm)
    entry["ldl_status"] = st
    entry["build_seconds"] = round(time.time() - t, 1)
    print(f"[{bb},{NN},{MM}] built {entry['build_seconds']}s LDL {st}", flush=True)
    if st != "PD":
        entry["disposition"] = f"LDL {st}"
        out["profiles"].append(entry)
        json.dump(out, open("metadata/weil_QH8_residual_diagnostic.json", "w"), indent=2)
        continue
    entry["midpoint_sha256"] = W._canonical_midpoint_hash(Mm)
    entry["multipliers"] = {}
    is_lb_profile = (bb, NN, MM) == load_bearing_profile
    for mult in MULTS:
        if bb == 1600 and mult in (12, 20):
            entry["multipliers"][str(mult)] = {
                "working_precision": bb * mult,
                "omitted": True,
                "omission_reason": "exact-rational candidate arithmetic on ~2e5-bit integers is prohibitively slow; see coverage_note",
            }
            print(f"    mult {mult}: OMITTED (see coverage_note)", flush=True)
            continue
        W_prec = bb * mult
        tc = time.time()
        cand, Rinf = W._candidate_quantities(Mm, bb, mult)
        if cand is None:
            entry["multipliers"][str(mult)] = {"working_precision": W_prec, "error": "zero eigenvector"}
            print(f"    mult {mult}: zero eigenvector", flush=True); continue
        witness_hash = W._canonical_witness_hash([c["v"] for c in cand])
        cls = W._classify_candidate(cand, Rinf, W_prec)
        cls = stringify_exact_data(cls)
        cls["working_precision"] = W_prec
        cls["eigenvector_multiplier"] = mult
        cls["ordered_witness_sha256"] = witness_hash
        cls["Rinf_over_min_gap_float"] = float(Rinf / F(int(cls["min_center_gap"][0]), int(cls["min_center_gap"][1])))
        entry["multipliers"][str(mult)] = cls
        overall.append(cls["classification"])
        print(f"    mult {mult} W={W_prec}: {cls['classification']}  min_gap={cls['min_gap_float']:.3e}  "
              f"gap/floor={cls['min_gap_over_floor_float']:.3e}  firstSepB={cls['first_separating_B']}  "
              f"weylPos={cls['weyl_all_positive_at_first_sep']} ({round(time.time()-tc,1)}s)", flush=True)
        if is_lb_profile and mult == load_bearing_mult:
            # MIG-044: the single completely-bound candidate set that generated the accepted
            # H=8 certificate. Cross-bind its matrix/witness hashes to the certificate's.
            load_bearing_section = {
                "profile": {"bits": bb, "N": NN, "M": MM},
                "eigenvector_multiplier": mult,
                "eigenvector_working_precision_bits": W_prec,
                "midpoint_matrix_sha256": entry["midpoint_sha256"],
                "ordered_witness_sha256": witness_hash,
                "midpoint_hash_matches_certificate": entry["midpoint_sha256"] == cert_ec["midpoint_matrix_sha256"],
                "witness_hash_matches_certificate": witness_hash == cert_ec["ordered_witness_sha256"],
                "generator_hash_matches_certificate": gen_hash == cert["provenance"]["generator_script_sha256"],
                "failure_at_320_demonstrated": not cls["disjoint_at_320"],
                "failing_pairs_at_320_count": len(cls["failing_pairs_at_320"]),
                "separation_at_selected_B_demonstrated": (cls["first_separating_B"] == load_bearing_B),
                "residual_inequalities_hold": True,  # enforced by assert in _adaptive_rho for every candidate
                "weyl_strict_positivity_demonstrated": cls["weyl_all_positive_at_first_sep"],
                "classification": cls["classification"],
            }
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
out["candidate_sets_evaluated"] = len(overall)
out["load_bearing_candidate"] = load_bearing_section
if load_bearing_section is None:
    raise RuntimeError("load-bearing candidate (matching the delivered certificate's profile/mult) was not found in the sweep")
out["diagnostic_sha256"] = hashlib.sha256(
    json.dumps({k: v for k, v in out.items() if k != "diagnostic_sha256"}, sort_keys=True).encode()
).hexdigest()
json.dump(out, open("metadata/weil_QH8_residual_diagnostic.json", "w"), indent=2)
print("OVERALL:", out["overall_classification"], "| Phase B authorized:", out["phase_B_authorized"], flush=True)
print("load_bearing matches certificate:",
      load_bearing_section["midpoint_hash_matches_certificate"],
      load_bearing_section["witness_hash_matches_certificate"],
      load_bearing_section["generator_hash_matches_certificate"], flush=True)
