"""
NonRed-Forcing Substrate Analysis

The core problem: Q3 vertices all have g₂=3 (3 squares per vertex),
but no grid vertex has exactly g₂=3. So NonRed fails (no pair with
same g₂, different g₃).

Solution: build a "square fan" where the center vertex has g₂=3
and g₃=0, matching the cube vertices on g₂ but differing on g₃.
"""

# Import everything from the LC pipeline
import sys
sys.path.insert(0, '/home/claude')
from ladder_certificate_v2 import *

def build_fan_plus_cube(n_fan_squares=3):
    """Fan of n squares sharing center vertex 0, then bridge to Q3."""
    edges = set()
    fan_n = 1
    for i in range(n_fan_squares):
        a, b, c = fan_n, fan_n+1, fan_n+2
        edges.update([frozenset([0,a]), frozenset([a,b]), 
                      frozenset([b,c]), frozenset([c,0])])
        fan_n += 3
    bridge = fan_n; fan_n += 1
    edges.add(frozenset([0, bridge]))
    cube_start = fan_n
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([cube_start+v, cube_start+u]))
    edges.add(frozenset([bridge, cube_start]))
    return frozenset(edges), cube_start + 8

def build_grid_fan_cube(grid_r, grid_c, n_fan_squares=3):
    """Grid + fan + Q3: grid provides square diversity, fan forces NonRed,
    cube provides g₃ visibility."""
    # Grid
    gn = grid_r * grid_c; edges = set()
    for r in range(grid_r):
        for c in range(grid_c):
            v = r * grid_c + c
            if c+1 < grid_c: edges.add(frozenset([v, v+1]))
            if r+1 < grid_r: edges.add(frozenset([v, v+grid_c]))
    
    # Fan center = gn
    fan_center = gn; fan_n = gn + 1
    for i in range(n_fan_squares):
        a, b, c = fan_n, fan_n+1, fan_n+2
        edges.update([frozenset([fan_center,a]), frozenset([a,b]),
                      frozenset([b,c]), frozenset([c,fan_center])])
        fan_n += 3
    # Connect grid to fan
    edges.add(frozenset([gn-1, fan_center]))
    
    # Bridge to cube
    bridge = fan_n; fan_n += 1
    edges.add(frozenset([fan_center, bridge]))
    
    cube_start = fan_n
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([cube_start+v, cube_start+u]))
    edges.add(frozenset([bridge, cube_start]))
    
    return frozenset(edges), cube_start + 8

print("="*70)
print("NONRED-FORCING SUBSTRATE ANALYSIS")
print("="*70)

# First: check what fan center looks like
print("\n--- Fan vertex analysis ---")
for nf in [3]:
    g, n = build_fan_plus_cube(nf)
    adj_g = adjacency(g, n)
    tris = find_induced_triangles(g, n)
    sqs = find_induced_squares(g, n)
    cubes = find_induced_cubes(g, n)
    
    print(f"Fan{nf}+Q3: n={n}, |E|={len(g)}, tri={len(tris)}, sq={len(sqs)}, cube={len(cubes)}")
    for v in range(n):
        ns = sum(1 for s in sqs if v in s)
        nc = sum(1 for c in cubes if v in c)
        if ns > 0 or nc > 0:
            print(f"  v={v}: deg={len(adj_g[v])}, sq_inc={ns}, cube_inc={nc}")

# Full LC on fan substrates
print("\n--- Fan+Q3 LC analysis ---")
fan_results = {}
for nf in [3, 4, 6]:
    g, n = build_fan_plus_cube(nf)
    res = full_lc_analysis(g, n, name=f"Fan{nf}+Q3")
    fan_results[res['name']] = res
    
    print(f"\n{res['name']}: n={n}, beta={res['beta']}, regime={res['regime']}")
    print(f"  phi=({res['phi1']:.3f}, {res['phi2']:.3f}, {res['phi3']:.3f})")
    print(f"  |S|={res['n_types']}, d={res['dim_stable']}")
    nr = 'PASS' if res['nonred_pass'] else 'FAIL'
    sa = 'PASS' if res['spec_act_pass'] else 'FAIL'
    print(f"  NonRed={nr}, SpecAct={sa} (eta={res['spec_act_eta']:.4f})")
    print(f"  g2/g3 table:")
    for t in sorted(res['support'], key=lambda x: (res['type_g2'].get(x,0), res['type_g3'].get(x,0))):
        print(f"    g2={res['type_g2'][t]:.2f}, g3={res['type_g3'][t]:.2f}")

# Grid+Fan+Cube composites
print("\n\n--- Grid+Fan+Cube LC analysis ---")
gfc_results = {}
for gr, gc, nf in [(3,3,3), (4,4,3), (3,4,3)]:
    g, n = build_grid_fan_cube(gr, gc, nf)
    res = full_lc_analysis(g, n, name=f"G{gr}x{gc}+Fan{nf}+Q3")
    gfc_results[res['name']] = res
    
    print(f"\n{res['name']}: n={n}, beta={res['beta']}, regime={res['regime']}")
    print(f"  phi=({res['phi1']:.3f}, {res['phi2']:.3f}, {res['phi3']:.3f})")
    print(f"  |S|={res['n_types']}, d={res['dim_stable']}")
    nr = 'PASS' if res['nonred_pass'] else 'FAIL'
    sa = 'PASS' if res['spec_act_pass'] else 'FAIL'
    print(f"  NonRed={nr}, SpecAct={sa} (eta={res['spec_act_eta']:.4f})")
    print(f"  g2/g3 table:")
    for t in sorted(res['support'], key=lambda x: (res['type_g2'].get(x,0), res['type_g3'].get(x,0))):
        print(f"    g2={res['type_g2'][t]:.2f}, g3={res['type_g3'][t]:.2f}")

# Produce actual LC records for the best candidates
print("\n\n" + "="*70)
print("FORMAL LADDER CERTIFICATES")
print("="*70)

# R2: Grid-4x4
g_r2, n_r2 = build_grid(4, 4)
r2 = full_lc_analysis(g_r2, n_r2, name="Grid-4x4")

# R3 candidates from above
all_r3 = {}
all_r3.update(fan_results)
all_r3.update(gfc_results)

lc_records = []
for r3name, r3 in sorted(all_r3.items()):
    if r3['phi3'] > 0:
        print(f"\n")
        jump, failing = print_lc(r2, r3)
        lc_records.append((r3name, jump, failing, r3))

# GRAND SUMMARY
print("\n\n" + "="*70)
print("GRAND LC SUMMARY")
print("="*70)
hdr = f"{'R3 substrate':<22} {'phi3':>5} {'|S|':>4} {'NonRed':>7} {'SpecAct':>8} {'d2':>3} {'d3':>3} {'Verdict':>10}"
print(hdr)
print("-"*70)
for r3name, jump, failing, r3 in lc_records:
    print(f"{r3name:<22} {r3['phi3']:>5.2f} {r3['n_types']:>4} "
          f"{'PASS' if r3['nonred_pass'] else 'FAIL':>7} "
          f"{'PASS' if r3['spec_act_pass'] else 'FAIL':>8} "
          f"{r2['dim_stable']:>3} {r3['dim_stable']:>3} "
          f"{'JUMP!' if jump else failing:>10}")

print(f"""
KEY FINDING: The NonRed gate requires that some collar types in S₃ have
identical g₂ (square incidence) but different g₃ (cube incidence). This is
a genuine structural constraint on which substrates can exhibit a strict
dimensional ladder jump. It is the NFC analogue of requiring that the new
Lovelock term is not merely a polynomial in previously available invariants.
""")
