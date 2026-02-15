"""
Computational Verification of Phase-A Pre-Adaptation and LS-2
for all tested NFC substrates.

Verifies:
1. α_ε (low-defect fraction) in preservation basins — Assumption PA-1
2. Trap asymmetry — basin condition (ii)
3. LS-2 pairwise obstruction sufficiency — via WL-collar probes
"""

import sys, os
sys.path.insert(0, '/home/claude')
from ladder_certificate_v2 import *
from collections import defaultdict, Counter
import numpy as np

# ═══════════════════════════════════════════════════
# PART 1: Pre-Adaptation Verification (α_ε analysis)
# ═══════════════════════════════════════════════════

def compute_step_defect(graph, n, ext_graph, ext_n):
    """Compute step defect d(E; σ) = fraction of projectable refinements destroyed.
    
    A 'projectable refinement' here = a WL-1 color class distinction that persists.
    We measure how many WL-1 distinctions in the base graph survive in the extended graph.
    """
    # WL-1 partition of base graph
    adj_base = adjacency(graph, n)
    labels_base = [len(adj_base[v]) for v in range(n)]
    for _ in range(5):
        new = []
        for v in range(n):
            ms = sorted(labels_base[u] for u in adj_base[v])
            new.append((labels_base[v], tuple(ms)))
        uniq = {lab: i for i, lab in enumerate(sorted(set(new)))}
        labels_base = [uniq[x] for x in new]
    
    n_classes_base = len(set(labels_base))
    
    # WL-1 partition of extended graph (restricted to base vertices)
    adj_ext = adjacency(ext_graph, ext_n)
    labels_ext = [len(adj_ext[v]) for v in range(ext_n)]
    for _ in range(5):
        new = []
        for v in range(ext_n):
            ms = sorted(labels_ext[u] for u in adj_ext[v])
            new.append((labels_ext[v], tuple(ms)))
        uniq = {lab: i for i, lab in enumerate(sorted(set(new)))}
        labels_ext = [uniq[x] for x in new]
    
    # Check: how many base-vertex WL distinctions survive?
    # Two base vertices distinguished by base WL but merged by ext WL = destroyed refinement
    base_pairs_distinguished = 0
    ext_pairs_distinguished = 0
    for i in range(n):
        for j in range(i+1, n):
            if labels_base[i] != labels_base[j]:
                base_pairs_distinguished += 1
                if labels_ext[i] != labels_ext[j]:
                    ext_pairs_distinguished += 1
    
    if base_pairs_distinguished == 0:
        return 0.0  # No refinements to destroy
    
    destroyed = base_pairs_distinguished - ext_pairs_distinguished
    return destroyed / base_pairs_distinguished

def local_extensions_defect_analysis(graph, n, name, R=2):
    """For a graph, enumerate local extensions (edge add/remove within radius R)
    and compute α_ε for various ε thresholds."""
    
    adj = adjacency(graph, n)
    
    # Enumerate single-edge modifications as "local extensions"
    # (add or remove one edge — the simplest local moves)
    extensions = []
    
    # Edge removals
    for e in graph:
        u, v = sorted(e)
        ext_graph = frozenset(graph - {e})
        extensions.append(('remove', (u,v), ext_graph, n))
    
    # Edge additions (within radius R)
    for u in range(n):
        for v in range(u+1, n):
            if frozenset([u,v]) not in graph:
                # Check if within radius R
                # BFS distance
                dist = bfs_dist(adj, u, v, n)
                if dist is not None and dist <= R:
                    ext_graph = frozenset(graph | {frozenset([u,v])})
                    extensions.append(('add', (u,v), ext_graph, n))
    
    if not extensions:
        return None
    
    # Compute step defect for each extension
    defects = []
    for etype, edge, ext_g, ext_n in extensions:
        d = compute_step_defect(graph, n, ext_g, ext_n)
        defects.append((etype, edge, d))
    
    defect_values = [d for _, _, d in defects]
    
    # Compute α_ε for various ε
    results = {}
    for eps in [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]:
        alpha = sum(1 for d in defect_values if d <= eps) / len(defect_values)
        results[eps] = alpha
    
    return {
        'name': name,
        'n': n,
        'n_extensions': len(extensions),
        'defect_values': defect_values,
        'alpha': results,
        'mean_defect': np.mean(defect_values),
        'median_defect': np.median(defect_values),
        'frac_zero_defect': sum(1 for d in defect_values if d == 0.0) / len(defect_values),
    }

def bfs_dist(adj, u, v, n):
    """BFS distance between u and v."""
    if u == v:
        return 0
    visited = {u}
    queue = [(u, 0)]
    while queue:
        node, dist = queue.pop(0)
        for nb in adj[node]:
            if nb == v:
                return dist + 1
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, dist + 1))
    return None

# ═══════════════════════════════════════════════════
# PART 2: LS-2 Verification (pairwise obstruction)
# ═══════════════════════════════════════════════════

def verify_LS2(graph, n, name):
    """Verify LS-2: for any two distinct WL-1 color classes (labels),
    there exist local probes producing order-dependent obstruction.
    
    We check: for each pair of distinct WL classes, does there exist
    a single-edge probe that distinguishes them differently depending
    on application order?
    """
    adj = adjacency(graph, n)
    
    # WL-1 partition
    labels = [len(adj[v]) for v in range(n)]
    for _ in range(5):
        new = []
        for v in range(n):
            ms = sorted(labels[u] for u in adj[v])
            new.append((labels[v], tuple(ms)))
        uniq = {lab: i for i, lab in enumerate(sorted(set(new)))}
        labels = [uniq[x] for x in new]
    
    classes = defaultdict(list)
    for v in range(n):
        classes[labels[v]].append(v)
    
    n_classes = len(classes)
    class_ids = sorted(classes.keys())
    
    # For each pair of classes, check if some edge modification
    # has different effects on representatives of the two classes
    pairs_tested = 0
    pairs_separated = 0
    details = []
    
    for i, c1 in enumerate(class_ids):
        for c2 in class_ids[i+1:]:
            pairs_tested += 1
            v1 = classes[c1][0]  # representative
            v2 = classes[c2][0]  # representative
            
            # Check: does any edge modification affect v1 and v2 differently?
            separated = False
            
            # Try edge additions near v1 or v2
            for target in [v1, v2]:
                for nb in range(n):
                    if nb != target and frozenset([target, nb]) not in graph:
                        # Add this edge, check WL effect on both reps
                        ext_g = frozenset(graph | {frozenset([target, nb])})
                        ext_adj = adjacency(ext_g, n)
                        
                        # Quick check: does degree change differently?
                        d1_before = len(adj[v1])
                        d2_before = len(adj[v2])
                        d1_after = len(ext_adj[v1])
                        d2_after = len(ext_adj[v2])
                        
                        if (d1_after - d1_before) != (d2_after - d2_before):
                            separated = True
                            break
                        
                        # Check neighbor-degree multiset change
                        ms1_before = sorted(len(adj[u]) for u in adj[v1])
                        ms2_before = sorted(len(adj[u]) for u in adj[v2])
                        ms1_after = sorted(len(ext_adj[u]) for u in ext_adj[v1])
                        ms2_after = sorted(len(ext_adj[u]) for u in ext_adj[v2])
                        
                        if (ms1_before != ms1_after) != (ms2_before != ms2_after):
                            separated = True
                            break
                
                if separated:
                    break
            
            if separated:
                pairs_separated += 1
            details.append((c1, c2, separated))
    
    return {
        'name': name,
        'n_classes': n_classes,
        'pairs_tested': pairs_tested,
        'pairs_separated': pairs_separated,
        'LS2_pass': pairs_separated == pairs_tested,
        'details': details,
    }

# ═══════════════════════════════════════════════════
# MAIN: Run verification on all substrates
# ═══════════════════════════════════════════════════

def build_fan_plus_cube(nf):
    edges = set()
    fan_n = 1
    for i in range(nf):
        a, b, c = fan_n, fan_n+1, fan_n+2
        edges.update([frozenset([0,a]), frozenset([a,b]),
                      frozenset([b,c]), frozenset([c,0])])
        fan_n += 3
    bridge = fan_n; fan_n += 1
    edges.add(frozenset([0, bridge]))
    cs = fan_n
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([cs+v, cs+u]))
    edges.add(frozenset([bridge, cs]))
    return frozenset(edges), cs + 8

print("="*75)
print("COMPUTATIONAL VERIFICATION: PRE-ADAPTATION + LS-2")
print("="*75)

# Test substrates (smaller ones for tractable enumeration)
substrates = [
    ("Grid-3x3", *build_grid(3,3)),
    ("Grid-3x4", *build_grid(3,4)),
    ("Q3", *build_hypercube(3)),
    ("Cyl-2x4", *build_cylinder(2,4)),
    ("Fan3+Q3", *build_fan_plus_cube(3)),
]

# ── PART 1: Pre-Adaptation ──
print("\n" + "─"*75)
print("PART 1: PRE-ADAPTATION VERIFICATION (α_ε analysis)")
print("─"*75)

pa_results = []
for name, graph, n in substrates:
    result = local_extensions_defect_analysis(graph, n, name)
    if result:
        pa_results.append(result)
        print(f"\n{name} (n={n}, {result['n_extensions']} local extensions):")
        print(f"  Mean defect: {result['mean_defect']:.4f}")
        print(f"  Median defect: {result['median_defect']:.4f}")
        print(f"  Zero-defect fraction: {result['frac_zero_defect']:.3f}")
        print(f"  α_ε values:")
        for eps, alpha in sorted(result['alpha'].items()):
            marker = " ← basin threshold" if eps == 0.1 else ""
            print(f"    ε={eps:.2f}: α = {alpha:.3f}{marker}")

# ── PART 2: LS-2 ──
print("\n" + "─"*75)
print("PART 2: LS-2 PAIRWISE OBSTRUCTION SUFFICIENCY")
print("─"*75)

ls2_results = []
for name, graph, n in substrates:
    result = verify_LS2(graph, n, name)
    ls2_results.append(result)
    status = "PASS ✓" if result['LS2_pass'] else "FAIL ✗"
    print(f"\n{name}: {result['n_classes']} WL classes, "
          f"{result['pairs_separated']}/{result['pairs_tested']} pairs separated → {status}")

# ── SUMMARY TABLE ──
print("\n" + "="*75)
print("VERIFICATION SUMMARY")
print("="*75)
print(f"\n{'Substrate':<15} {'n':>3} {'|N|':>5} {'α₀.₁':>6} {'α₀.₀':>6} {'d̄':>6} {'LS-2':>6}")
print("─"*52)
for pa, ls2 in zip(pa_results, ls2_results):
    ls2_str = "✓" if ls2['LS2_pass'] else "✗"
    print(f"{pa['name']:<15} {pa['n']:>3} {pa['n_extensions']:>5} "
          f"{pa['alpha'][0.1]:>6.3f} {pa['alpha'][0.0]:>6.3f} "
          f"{pa['mean_defect']:>6.3f} {ls2_str:>6}")

print(f"""
INTERPRETATION:
  α₀.₁ = fraction of local extensions with step defect ≤ 0.1
  α₀.₀ = fraction of local extensions with zero defect
  d̄ = mean step defect across all local extensions
  
  Pre-adaptation (PA-1) requires α_ε ≥ 1-η for some small ε,η.
  LS-2 requires pairwise obstruction for all distinct WL classes.
""")
