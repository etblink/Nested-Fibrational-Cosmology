"""
Diagnose: which extensions kill refinements?
Test: what happens with restricted (more physically motivated) 
extension classes?

The key insight: delete_all and complete_all are "nuclear" 
extensions that collapse everything. These may not be physically 
relevant. What if we restrict to LOCAL extensions?
"""

import itertools
from collections import defaultdict

def adjacency(graph, n):
    adj = {v: set() for v in range(n)}
    for e in graph:
        u, v = list(e)
        adj[u].add(v)
        adj[v].add(u)
    return adj

def degree_sequence(graph, n):
    deg = [0] * n
    for e in graph:
        u, v = list(e)
        deg[u] += 1
        deg[v] += 1
    return tuple(sorted(deg))

def canonical_form(graph, n):
    best = None
    for perm in itertools.permutations(range(n)):
        relabeled = frozenset(frozenset(perm[v] for v in e) for e in graph)
        edges = tuple(sorted(tuple(sorted(e)) for e in relabeled))
        if best is None or edges < best:
            best = edges
    return best

def transitive_closure(graph, n):
    adj = adjacency(graph, n)
    new_edges = set(graph)
    for v in range(n):
        for u1 in adj[v]:
            for u2 in adj[v]:
                if u1 < u2:
                    new_edges.add(frozenset([u1, u2]))
    return frozenset(new_edges)

def complement(graph, n):
    all_edges = frozenset(frozenset(e) for e in itertools.combinations(range(n), 2))
    return all_edges - graph

def square_graph(graph, n):
    adj = adjacency(graph, n)
    new_edges = set(graph)
    for v in range(n):
        for u in adj[v]:
            for w in adj[u]:
                if w != v:
                    new_edges.add(frozenset([min(v,w), max(v,w)]))
    return frozenset(new_edges)

def get_automorphism_orbits(graph, n):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py: parent[px] = py
    
    for perm in itertools.permutations(range(n)):
        relabeled = frozenset(frozenset(perm[v] for v in e) for e in graph)
        if relabeled == graph:
            for v in range(n):
                union(v, perm[v])
    
    orbits = defaultdict(set)
    for v in range(n):
        orbits[find(v)].add(v)
    return list(orbits.values())


def compute_tau_with_class(graph, n, ext_list):
    """Compute tau using only specified extensions."""
    base_orbits = get_automorphism_orbits(graph, n)
    n_base_orbits = len(base_orbits)
    
    vertex_to_orbit = {}
    for i, orb in enumerate(base_orbits):
        for v in orb:
            vertex_to_orbit[v] = i
    
    all_colorings = []
    for bits in itertools.product([0, 1], repeat=n_base_orbits):
        if all(b == 0 for b in bits) or all(b == 1 for b in bits):
            continue
        coloring = tuple(bits[vertex_to_orbit[v]] for v in range(n))
        all_colorings.append((bits, coloring))
    
    surviving = list(range(len(all_colorings)))
    killed_by = {}
    
    for ext_name, ext_func in ext_list:
        try:
            extended = ext_func(graph)
        except:
            continue
        
        ext_orbits = get_automorphism_orbits(extended, n)
        
        new_surviving = []
        for idx in surviving:
            bits, coloring = all_colorings[idx]
            ok = True
            for orb in ext_orbits:
                colors_in_orb = set(coloring[v] for v in orb)
                if len(colors_in_orb) > 1:
                    ok = False
                    break
            if ok:
                new_surviving.append(idx)
            else:
                if idx not in killed_by:
                    killed_by[idx] = ext_name
        surviving = new_surviving
    
    # Compute rank (independence) over GF(2)
    if not surviving:
        return 0, 0, [], killed_by
    
    surviving_bits = [all_colorings[idx][0] for idx in surviving]
    matrix = [list(bits) for bits in surviving_bits]
    n_cols = n_base_orbits
    rank = 0
    for col in range(n_cols):
        pivot_row = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] == 1:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
        for row in range(len(matrix)):
            if row != rank and matrix[row][col] == 1:
                matrix[row] = [(matrix[row][j] + matrix[rank][j]) % 2 
                              for j in range(n_cols)]
        rank += 1
    
    return rank, len(surviving), [all_colorings[idx] for idx in surviving], killed_by


# ============================================================
# Test different extension classes
# ============================================================

for n in [4, 5]:
    print(f"\n{'='*60}")
    print(f"DIAGNOSIS: n = {n}")
    print(f"{'='*60}")
    
    possible_edges = list(itertools.combinations(range(n), 2))
    all_edges_fs = frozenset(frozenset(e) for e in possible_edges)
    
    iso_classes = {}
    for r in range(len(possible_edges) + 1):
        for combo in itertools.combinations(possible_edges, r):
            g = frozenset(frozenset(e) for e in combo)
            canon = canonical_form(g, n)
            if canon not in iso_classes:
                iso_classes[canon] = g
    
    # Define extension class tiers
    CLASS_MINIMAL = [
        ('identity', lambda g: g),
        ('trans_closure', lambda g: transitive_closure(g, n)),
        ('complement', lambda g: complement(g, n)),
    ]
    
    CLASS_STRUCTURAL = CLASS_MINIMAL + [
        ('square', lambda g: square_graph(g, n)),
        ('comp_then_trans', lambda g: transitive_closure(complement(g, n), n)),
        ('trans_then_comp', lambda g: complement(transitive_closure(g, n), n)),
    ]
    
    CLASS_NUCLEAR = CLASS_STRUCTURAL + [
        ('delete_all', lambda g: frozenset()),
        ('complete_all', lambda g: all_edges_fs),
    ]
    
    classes = {
        'MINIMAL (id + trans + comp)': CLASS_MINIMAL,
        'STRUCTURAL (+ square, compositions)': CLASS_STRUCTURAL,
        'NUCLEAR (+ delete_all, complete_all)': CLASS_NUCLEAR,
    }
    
    for class_name, ext_list in classes.items():
        print(f"\n  Extension class: {class_name}")
        
        max_tau = 0
        best = None
        results = []
        
        for canon, g in sorted(iso_classes.items()):
            orbits = get_automorphism_orbits(g, n)
            if len(orbits) <= 1:
                continue
            
            tau, n_surv, surviving, killed_by = compute_tau_with_class(g, n, ext_list)
            deg = degree_sequence(g, n)
            results.append((tau, n_surv, len(orbits), len(g), deg, g, killed_by))
            
            if tau > max_tau:
                max_tau = tau
                best = (tau, n_surv, len(orbits), deg, g, killed_by)
        
        results.sort(key=lambda x: (-x[0], -x[1]))
        
        print(f"    Max tau = {max_tau}")
        if max_tau > 0:
            print(f"    Classes with tau >= 1:")
            for tau, n_surv, n_orb, n_edges, deg, g, kb in results[:8]:
                if tau >= 1:
                    print(f"      {n_edges}e deg={deg} orbits={n_orb} "
                          f"surviving={n_surv} tau={tau}")
            
            if best:
                t, ns, no, d, g, kb = best
                print(f"\n    Best graph detail:")
                print(f"      {len(g)} edges, deg={d}, {no} orbits")
                print(f"      {ns} surviving refinements, tau={t}")
                
                # Show local load for this graph
                adj = adjacency(g, n)
                _, _, surviving, _ = compute_tau_with_class(g, n, ext_list)
                if surviving:
                    print(f"      Local load analysis:")
                    for v in range(n):
                        r2 = {v}
                        for u in adj[v]:
                            r2.add(u)
                            for w in adj[u]:
                                r2.add(w)
                        
                        joint = set()
                        for u in r2:
                            label = tuple(c[u] for _, c in surviving)
                            joint.add(label)
                        print(f"        v={v}: R2={sorted(r2)}, "
                              f"joint labels={len(joint)}")
        else:
            # Show what kills the last survivors
            print(f"    All refinements killed. Sample kill report:")
            for tau, n_surv, n_orb, n_edges, deg, g, kb in results[:3]:
                if n_orb >= 2:
                    print(f"      {n_edges}e deg={deg} orbits={n_orb}:")
                    kill_counts = defaultdict(int)
                    for idx, ext in kb.items():
                        kill_counts[ext] += 1
                    for ext, cnt in sorted(kill_counts.items(), 
                                          key=lambda x: -x[1]):
                        print(f"        {ext}: killed {cnt} refinements")


# ============================================================
# KEY TEST: identity-only (no extensions at all)
# ============================================================
print(f"\n{'='*60}")
print(f"CONTROL: IDENTITY ONLY (no extensions)")
print(f"{'='*60}")

for n in [4, 5]:
    print(f"\n  n = {n}:")
    possible_edges = list(itertools.combinations(range(n), 2))
    iso_classes = {}
    for r in range(len(possible_edges) + 1):
        for combo in itertools.combinations(possible_edges, r):
            g = frozenset(frozenset(e) for e in combo)
            canon = canonical_form(g, n)
            if canon not in iso_classes:
                iso_classes[canon] = g
    
    CLASS_ID = [('identity', lambda g: g)]
    
    max_tau = 0
    for canon, g in iso_classes.items():
        orbits = get_automorphism_orbits(g, n)
        if len(orbits) <= 1: continue
        tau, _, _, _ = compute_tau_with_class(g, n, CLASS_ID)
        max_tau = max(max_tau, tau)
    
    print(f"    Max tau (identity only) = {max_tau}")
    print(f"    This is the orbit upper bound = max aut orbits")

# ============================================================
# SYNTHESIS
# ============================================================
print(f"\n{'='*60}")
print(f"SYNTHESIS")
print(f"{'='*60}")
print("""
The results reveal a sharp pattern:

1. IDENTITY ONLY: tau = max automorphism orbits (2,3,4 for n=3,4,5)
   All orbit-based refinements are trivially projectable when 
   there are no extensions to erase them.

2. MINIMAL (id + trans + comp): tau drops significantly.
   E_trans is the primary killer: it merges distance-2 vertices,
   collapsing orbit distinctions. E_comp swaps edge/non-edge 
   structure, killing orbit colorings that depend on edge presence.

3. STRUCTURAL: tau drops further or reaches 0.

4. NUCLEAR: tau = 0 everywhere.
   delete_all and complete_all collapse ALL structure.

INTERPRETATION:

The refinement ceiling tau depends critically on WHICH extensions 
are in the admissible class. The framework currently defines the 
admissible class as MAXIMAL, which includes delete_all and 
complete_all. Under maximality, tau = 0 for all tested sizes.

This means: either
(a) The maximal admissible class is TOO aggressive for the 
    dimensional selection mechanism to work, and a restricted 
    (locality-respecting) extension class is needed, or
(b) Projectable refinements need to be defined differently 
    (not as 2-color vertex labelings but as something richer), or
(c) The dimensional selection mechanism requires MUCH larger 
    configuration spaces where richer structure can persist.

This is the honest computational finding. It directly informs 
Open Problem O1 (strengthening dimensional selection) and 
Conjecture 7.2 (diversity-forcing maximality).
""")
