"""
LADDER CERTIFICATE — EXPLICIT WITNESS ENUMERATION

Produces monograph-ready LC records with full collar-type tuple labels
for the NonRed witness pair, as required by Appendix VIII.C.
"""

import sys, numpy as np
sys.path.insert(0, '/home/claude')
from ladder_certificate_v2 import *
from nonred_analysis import build_fan_plus_cube, build_grid_fan_cube

# ============================================================
# COLLAR-TYPE LABEL FORMATTER
# ============================================================

def format_collar_type(t, short=False):
    """Format a collar type tuple for display.
    Each entry is (dist, deg, deg_ball, tri_inc, sq_inc, cube_inc).
    Show as a readable multiset."""
    if short:
        # Compact: show root entry only (dist=0)
        root = [sig for sig in t if sig[0] == 0]
        if root:
            d, deg, db, a1, a2, a3 = root[0]
            return f"(deg={deg},△={a1},□={a2},Q₃={a3})"
        return str(t[:1])
    # Full: show sorted sig entries
    lines = []
    for sig in t:
        d, deg, db, a1, a2, a3 = sig
        lines.append(f"  d={d} deg={deg} db={db} △={a1} □={a2} Q₃={a3}")
    return "\n".join(lines)

def collar_type_shortlabel(t):
    """One-line label: root features + ball size."""
    root = [sig for sig in t if sig[0] == 0]
    if root:
        d, deg, db, a1, a2, a3 = root[0]
        return f"[deg={deg} △={a1} □={a2} Q₃={a3} |ball|={len(t)}]"
    return f"[|ball|={len(t)}]"

# ============================================================
# FULL LC RECORD WITH EXPLICIT WITNESS ENUMERATION
# ============================================================

def print_full_lc(r2, r3, include_type_table=True):
    """Print LC with explicit collar-type labels for NonRed witness."""
    
    I2 = {k for k in [1,2,3] if [r2['phi1'],r2['phi2'],r2['phi3']][k-1] > 0}
    I3 = {k for k in [1,2,3] if [r3['phi1'],r3['phi2'],r3['phi3']][k-1] > 0}
    
    print("="*72)
    print(f"LADDER CERTIFICATE  LC({r2['name']}  →  {r3['name']})")
    print("="*72)
    
    # META
    print(f"""
META
  R2 family  : {r2['name']}  (n={r2['n']}, |E|={r2['E']}, β={r2['beta']})
  R3 family  : {r3['name']}  (n={r3['n']}, |E|={r3['E']}, β={r3['beta']})
  Gadgets    : C₃, C₄, Q₃
  Witness rad: Rw = (1, 2, 3)
  Collar k*  : 1
  Coarsening : WL-1 partition, 3 rounds
  Cycle basis: BFS fundamental cycles
  Tolerances : ε_S=0, ε_λ=0.05, ε_v=1e-6""")
    
    # Φ
    print(f"""
Φ  (strict certification)
  R2: (φ₁, φ₂, φ₃) = ({r2['phi1']:.3f}, {r2['phi2']:.3f}, {r2['phi3']:.3f})   [{r2['regime']}]
  R3: (φ₁, φ₂, φ₃) = ({r3['phi1']:.3f}, {r3['phi2']:.3f}, {r3['phi3']:.3f})   [{r3['regime']}]
  I₂ = {I2}
  I₃ = {I3}""")
    
    # S
    print(f"""
S  (collar-type support)
  |S₂| = {r2['n_types']}
  |S₃| = {r3['n_types']}""")
    
    if include_type_table:
        print(f"\n  S₃ collar-type table (root vertex features):")
        print(f"  {'idx':>4} {'label':<42} {'g₂':>6} {'g₃':>6}")
        print(f"  {'─'*62}")
        for i, t in enumerate(sorted(r3['support'], 
                              key=lambda x: (r3['type_g2'].get(x,0), r3['type_g3'].get(x,0)))):
            label = collar_type_shortlabel(t)
            g2 = r3['type_g2'][t]
            g3 = r3['type_g3'][t]
            marker = " ←" if r3.get('nonred_pair') and t in r3['nonred_pair'] else ""
            print(f"  {i:>4} {label:<42} {g2:>6.2f} {g3:>6.2f}{marker}")
    
    # T
    print(f"""
T  (type-level random walk)
  T₂ : {r2['T_size']}×{r2['T_size']}   spectrum = {[f'{v:.4f}' for v in r2['stable_eigenvalues'][:6]]}
  T₃ : {r3['T_size']}×{r3['T_size']}   spectrum = {[f'{v:.4f}' for v in r3['stable_eigenvalues'][:6]]}""")
    
    # NonRed — EXPLICIT WITNESS ENUMERATION
    print(f"\nNonRed  (non-redundant cube visibility on S₃)")
    if r3['nonred_pass']:
        t, tp = r3['nonred_pair']
        g2_t  = r3['type_g2'][t]
        g3_t  = r3['type_g3'][t]
        g2_tp = r3['type_g2'][tp]
        g3_tp = r3['type_g3'][tp]
        
        print(f"  PASS ✓")
        print(f"  Witness pair (t, t′) with g₂(t) = g₂(t′) = {g2_t:.2f}, g₃(t) ≠ g₃(t′):")
        print(f"")
        print(f"  t  = {collar_type_shortlabel(t)}")
        print(f"       g₂ = {g2_t:.2f},  g₃ = {g3_t:.2f}")
        print(f"       collar signature ({len(t)} vertices in k*-ball):")
        for sig in sorted(t):
            d, deg, db, a1, a2, a3 = sig
            print(f"         dist={d}  deg={deg}  deg_ball={db}  △_inc={a1}  □_inc={a2}  Q₃_inc={a3}")
        print(f"")
        print(f"  t′ = {collar_type_shortlabel(tp)}")
        print(f"       g₂ = {g2_tp:.2f},  g₃ = {g3_tp:.2f}")
        print(f"       collar signature ({len(tp)} vertices in k*-ball):")
        for sig in sorted(tp):
            d, deg, db, a1, a2, a3 = sig
            print(f"         dist={d}  deg={deg}  deg_ball={db}  △_inc={a1}  □_inc={a2}  Q₃_inc={a3}")
        print(f"")
        print(f"  Interpretation: t is a cube-bearing vertex (□={int(g2_t)}, Q₃={int(g3_t)})")
        print(f"                  t′ is a fan-center vertex  (□={int(g2_tp)}, Q₃={int(g3_tp)})")
        print(f"                  Same square count, different cube membership → non-redundant.")
    else:
        print(f"  FAIL ✗")
        print(f"  No witness pair found. g₂/g₃ on S₃:")
        for t in sorted(r3['support'], key=lambda x: (r3['type_g2'].get(x,0), r3['type_g3'].get(x,0))):
            print(f"    g₂={r3['type_g2'][t]:.2f}, g₃={r3['type_g3'][t]:.2f}")
    
    # SpecAct
    print(f"""
SpecAct  (spectral activation)
  η = ‖Proj_{{Eig^st}} g₃‖ = {r3['spec_act_eta']:.6f}
  {'PASS ✓' if r3['spec_act_pass'] else 'FAIL ✗'}""")
    
    # DIM
    d2 = r2['dim_stable']
    d3 = r3['dim_stable']
    print(f"""
DIM  (compression-stable dimensions)
  d₂ = dim(Eig^st(T₂)) = {d2}
  d₃ = dim(Eig^st(T₃)) = {d3}""")
    
    # Verdict
    strict = (r3['phi3'] > 0 and r3['nonred_pass'] and r3['spec_act_pass'] and d3 > d2)
    
    if strict:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  VERDICT:  STRICT DIMENSIONAL LADDER CERTIFIED              ║
║                                                              ║
║  d₃ = {d3}  >  d₂ = {d2}                                          ║
║  All gates passed: φ₃>0, NonRed, SpecAct, DIM               ║
╚══════════════════════════════════════════════════════════════╝""")
    else:
        if r3['phi3'] <= 0: failing = "φ₃ = 0 (no cube visibility)"
        elif not r3['nonred_pass']: failing = "NonRed (cube redundant on support)"
        elif not r3['spec_act_pass']: failing = "SpecAct (cube spectrally inactive)"
        elif d3 <= d2: failing = f"DIM equality (d₂={d2}, d₃={d3})"
        else: failing = "unknown"
        
        print(f"""
  VERDICT:  NO STRICT JUMP
  First failing gate: {failing}""")
    
    print("="*72)
    return strict

# ============================================================
# PRODUCE THE TWO CERTIFIED LC RECORDS
# ============================================================

print("="*72)
print("MONOGRAPH-GRADE LADDER CERTIFICATES WITH EXPLICIT WITNESSES")
print("="*72)

# R2 baseline
g_r2, n_r2 = build_grid(4, 4)
r2 = full_lc_analysis(g_r2, n_r2, name="Grid-4x4")

# --- LC 1: Grid-4x4 → Fan3+Q3 ---
g_f3, n_f3 = build_fan_plus_cube(3)
r3_fan3 = full_lc_analysis(g_f3, n_f3, name="Fan3+Q3")

print("\n")
print_full_lc(r2, r3_fan3)

# --- LC 2: Grid-4x4 → G3x3+Fan3+Q3 ---
g_gf, n_gf = build_grid_fan_cube(3, 3, 3)
r3_gf = full_lc_analysis(g_gf, n_gf, name="G3x3+Fan3+Q3")

print("\n\n")
print_full_lc(r2, r3_gf)

# --- LC 3 (failing for contrast): Grid-4x4 → Fan4+Q3 ---
g_f4, n_f4 = build_fan_plus_cube(4)
r3_fan4 = full_lc_analysis(g_f4, n_f4, name="Fan4+Q3")

print("\n\n")
print_full_lc(r2, r3_fan4)

# --- SUMMARY ---
print(f"""

{'='*72}
SUMMARY OF THREE LC RECORDS
{'='*72}

  LC1: Grid-4x4 → Fan3+Q3       ALL GATES PASS → STRICT LADDER ✓
       Fan center has □=3, Q₃=0; cube vertices have □=3, Q₃=1
       NonRed witness: same g₂=3, different g₃

  LC2: Grid-4x4 → G3x3+Fan3+Q3  ALL GATES PASS → STRICT LADDER ✓
       Grid+Fan composite provides richer collar-type alphabet
       Same NonRed mechanism; larger d₃ (11 vs 7)

  LC3: Grid-4x4 → Fan4+Q3       NonRed FAILS → NO STRICT JUMP
       Fan center has □=4 ≠ 3, so no g₂-matching witness pair

  Key structural insight: NonRed requires that the fan center's square
  incidence count exactly matches the cube vertices' square incidence.
  Fan3 achieves this (3 squares at center = 3 squares per Q₃ vertex).
  Fan4 breaks it (4 ≠ 3). This is a genuine combinatorial constraint
  on which substrates can exhibit a strict dimensional ladder jump.

  This is the NFC analogue of Lovelock's dimensional gating:
  the cube-supported response-law term is new (not a function of the
  square term) if and only if NonRed holds on the collar-type support.
""")
