"""
LADDER CERTIFICATE PIPELINE v2 — Diagnostic fixes + composite substrates

Fixes from v1:
  1. Eigenspace: use ALL eigenvalues with |λ| > eps, not just "stable across depth"
     (single-instance regime: stability = persistence within graph)
  2. Boundary: for regular graphs (no leaf peeling), use "distance from centroid" or 
     simply all vertices (declared)
  3. Composite substrates: bridge a grid to a cube to force NonRed
  4. WL initial labels enriched with gadget features for finer collar typing
"""

import itertools, numpy as np
from collections import defaultdict, Counter

# ============================================================
# GRAPH INFRASTRUCTURE
# ============================================================

def adjacency(graph, n):
    adj = {v: set() for v in range(n)}
    for e in graph:
        u, v = list(e)
        adj[u].add(v); adj[v].add(u)
    return adj

def radius_ball_set(adj, center, radius):
    ball = {center}; frontier = {center}
    for _ in range(radius):
        nf = set()
        for v in frontier:
            for u in adj[v]:
                if u not in ball: nf.add(u); ball.add(u)
        frontier = nf
    return frozenset(ball)

def induced_subgraph(graph, vertices):
    return frozenset(e for e in graph if e.issubset(vertices))

# ============================================================
# GRAPH BUILDERS
# ============================================================

def build_grid(rows, cols):
    n = rows * cols; edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c+1 < cols: edges.add(frozenset([v, v+1]))
            if r+1 < rows: edges.add(frozenset([v, v+cols]))
    return frozenset(edges), n

def build_hypercube(dim):
    n = 2**dim; edges = set()
    for v in range(n):
        for bit in range(dim):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([v, u]))
    return frozenset(edges), n

def build_cylinder(rows, cols):
    n = rows * cols; edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            edges.add(frozenset([v, r*cols + (c+1)%cols]))
            if r+1 < rows: edges.add(frozenset([v, v+cols]))
    return frozenset(edges), n

def build_composite_grid_cube(grid_rows, grid_cols, bridge_len=1):
    """Grid + Q3 connected by bridge. Forces structural diversity."""
    # Grid on vertices 0..grid_n-1
    grid_n = grid_rows * grid_cols
    grid_edges = set()
    for r in range(grid_rows):
        for c in range(grid_cols):
            v = r * grid_cols + c
            if c+1 < grid_cols: grid_edges.add(frozenset([v, v+1]))
            if r+1 < grid_rows: grid_edges.add(frozenset([v, v+grid_cols]))
    
    # Bridge vertices
    bridge_start = grid_n
    bridge_verts = list(range(bridge_start, bridge_start + bridge_len))
    
    # Q3 on vertices after bridge
    cube_start = bridge_start + bridge_len
    cube_edges = set()
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v: cube_edges.add(frozenset([cube_start + v, cube_start + u]))
    
    # Connect: grid corner → bridge → cube vertex 0
    all_edges = grid_edges | cube_edges
    grid_attach = grid_rows * grid_cols - 1  # bottom-right corner
    if bridge_len > 0:
        all_edges.add(frozenset([grid_attach, bridge_verts[0]]))
        for i in range(bridge_len - 1):
            all_edges.add(frozenset([bridge_verts[i], bridge_verts[i+1]]))
        all_edges.add(frozenset([bridge_verts[-1], cube_start]))
    else:
        all_edges.add(frozenset([grid_attach, cube_start]))
    
    n = cube_start + 8
    return frozenset(all_edges), n, grid_n, cube_start

def build_double_grid_cube(grid1_r, grid1_c, grid2_r, grid2_c, bridge_len=1):
    """Two grids of different sizes connected by bridge + one has Q3 attached."""
    # Grid 1
    g1_n = grid1_r * grid1_c
    edges = set()
    for r in range(grid1_r):
        for c in range(grid1_c):
            v = r * grid1_c + c
            if c+1 < grid1_c: edges.add(frozenset([v, v+1]))
            if r+1 < grid1_r: edges.add(frozenset([v, v+grid1_c]))
    
    # Grid 2 offset
    g2_start = g1_n
    for r in range(grid2_r):
        for c in range(grid2_c):
            v = g2_start + r * grid2_c + c
            if c+1 < grid2_c: edges.add(frozenset([v, v+1]))
            if r+1 < grid2_r: edges.add(frozenset([v, v+grid2_c]))
    
    g2_n = grid2_r * grid2_c
    
    # Q3 attached to grid2
    cube_start = g2_start + g2_n
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([cube_start + v, cube_start + u]))
    
    # Bridge: grid1 corner → grid2 corner
    edges.add(frozenset([g1_n - 1, g2_start]))
    # Attach cube to grid2 corner
    g2_attach = g2_start + g2_n - 1
    edges.add(frozenset([g2_attach, cube_start]))
    
    n = cube_start + 8
    return frozenset(edges), n

# ============================================================
# GADGET DETECTION
# ============================================================

def find_induced_triangles(graph, n):
    adj = adjacency(graph, n); tris = set()
    for a in range(n):
        for b in adj[a]:
            if b <= a: continue
            for c in adj[a] & adj[b]:
                if c <= b: continue
                tri = frozenset([a,b,c])
                if len(induced_subgraph(graph, tri)) == 3: tris.add(tri)
    return list(tris)

def find_induced_squares(graph, n):
    adj = adjacency(graph, n); sqs = set()
    for a in range(n):
        for b in adj[a]:
            if b <= a: continue
            for c in adj[b]:
                if c == a or c <= a: continue
                if frozenset([a,c]) in graph: continue
                for d in adj[c]:
                    if d == b or d <= a: continue
                    if frozenset([a,d]) not in graph: continue
                    if frozenset([b,d]) in graph: continue
                    sqs.add(frozenset([a,b,c,d]))
    return [sq for sq in sqs if len(induced_subgraph(graph, sq)) == 4]

def is_q3(graph_edges, vertices):
    if len(vertices) != 8: return False
    verts = sorted(vertices); sub_adj = defaultdict(set); ec = 0
    for e in graph_edges:
        if e.issubset(vertices):
            u,v = list(e); sub_adj[u].add(v); sub_adj[v].add(u); ec += 1
    if ec != 12: return False
    if not all(len(sub_adj[v]) == 3 for v in verts): return False
    color = {}; queue = [verts[0]]; color[verts[0]] = 0
    while queue:
        v = queue.pop(0)
        for u in sub_adj[v]:
            if u not in color: color[u] = 1 - color[v]; queue.append(u)
            elif color[u] == color[v]: return False
    if len(color) != 8: return False
    for v in verts:
        for u in sub_adj[v]:
            if sub_adj[v] & sub_adj[u]: return False
    return True

def find_induced_cubes(graph, n):
    if n < 8: return []
    return [frozenset(c) for c in itertools.combinations(range(n), 8) if is_q3(graph, frozenset(c))]

def cube_face_squares(graph, cube_verts):
    faces = []
    for combo in itertools.combinations(sorted(cube_verts), 4):
        cs = frozenset(combo); ei = induced_subgraph(graph, cs)
        if len(ei) == 4:
            degs = Counter()
            for e in ei:
                for v in e: degs[v] += 1
            if all(d == 2 for d in degs.values()): faces.append(cs)
    return faces

# ============================================================
# CARRIER OVERLAP
# ============================================================

def get_carriers(gadgets, graph):
    c2g = defaultdict(list)
    for g in gadgets:
        for e in induced_subgraph(graph, g): c2g[e].append(g)
    return c2g

def local_pattern(graph, n, carrier_edge, gadget, radius):
    u, v = sorted(carrier_edge); adj = adjacency(graph, n)
    ball = set()
    for c in [u, v]: ball |= radius_ball_set(adj, c, radius)
    ball = frozenset(ball)
    def bfs_d(s, t, a, md):
        if s == t: return 0
        vis = {s}; fr = {s}
        for d in range(1, md+1):
            nf = set()
            for x in fr:
                for y in a[x]:
                    if y not in vis:
                        if y == t: return d
                        vis.add(y); nf.add(y)
            fr = nf
        return md + 1
    sigs = []
    for w in sorted(ball):
        sigs.append((bfs_d(u,w,adj,radius+1), bfs_d(v,w,adj,radius+1),
                     len(adj[w]), 1 if w in gadget else 0, len(adj[w]&ball)))
    return (tuple(sorted(sigs)), len(ball))

def compute_m_perp(graph, n, c2g, rw=2):
    mp = {}
    for c, gs in c2g.items():
        pats = defaultdict(list)
        for g in gs: pats[local_pattern(graph, n, c, g, rw)].append(g)
        mp[c] = len(pats)
    return mp

# ============================================================
# CYCLE ANALYSIS
# ============================================================

def cycle_rank(graph, n):
    adj = adjacency(graph, n); vis = set(); comp = 0
    for v in range(n):
        if v not in vis:
            comp += 1; stk = [v]
            while stk:
                u = stk.pop()
                if u in vis: continue
                vis.add(u)
                for w in adj[u]:
                    if w not in vis: stk.append(w)
    return len(graph) - n + comp

def fundamental_cycles(graph, n):
    adj = adjacency(graph, n); tree = set(); par = {}; vis = set()
    for s in range(n):
        if s in vis: continue
        q = [s]; vis.add(s); par[s] = -1
        while q:
            v = q.pop(0)
            for u in adj[v]:
                if u not in vis:
                    vis.add(u); par[u] = v; tree.add(frozenset([u,v])); q.append(u)
    cycles = []
    for e in graph:
        if e in tree: continue
        u, v = sorted(e)
        def p2r(x):
            p = []
            while x != -1: p.append(x); x = par[x]
            return p
        pu, pv = p2r(u), p2r(v); su = set(pu)
        lca = next((x for x in pv if x in su), None)
        if lca is None: continue
        ce = {frozenset([u,v])}
        x = u
        while x != lca: ce.add(frozenset([x, par[x]])); x = par[x]
        x = v
        while x != lca: ce.add(frozenset([x, par[x]])); x = par[x]
        cycles.append(frozenset(ce))
    return cycles

def compute_strict_coverage(graph, n, cycles, tris, sqs, cubes):
    c1, c2, c3 = set(), set(), set()
    for i, ce in enumerate(cycles):
        for t in tris:
            if induced_subgraph(graph, t).issubset(ce): c1.add(i); break
        for sq in sqs:
            if induced_subgraph(graph, sq).issubset(ce): c2.add(i); break
        for cube in cubes:
            for face in cube_face_squares(graph, cube):
                if induced_subgraph(graph, face).issubset(ce): c3.add(i); break
            if i in c3: break
    return c1, c2, c3

# ============================================================
# COLLAR TYPES (enriched: vertex degree + gadget incidence + distance)
# ============================================================

def collar_type_v2(adj, n, root, kstar, tri_inc, sq_inc, cube_inc):
    """Collar type: multiset of (dist, degree, #tri_inc, #sq_inc, #cube_inc) in kstar-ball."""
    ball = {root}; frontier = {root}
    for _ in range(kstar):
        nf = set()
        for v in frontier:
            for u in adj[v]:
                if u not in ball: nf.add(u); ball.add(u)
        frontier = nf
    
    dist = {root: 0}; q = [root]
    while q:
        v = q.pop(0)
        for u in adj[v]:
            if u in ball and u not in dist:
                dist[u] = dist[v] + 1; q.append(u)
    
    sigs = []
    for v in sorted(ball):
        deg = len(adj[v])
        deg_ball = len(adj[v] & ball)
        sigs.append((dist.get(v, kstar+1), deg, deg_ball,
                     tri_inc.get(v, 0), sq_inc.get(v, 0), cube_inc.get(v, 0)))
    return tuple(sorted(sigs))

# ============================================================
# WL PARTITION
# ============================================================

def wl_partition(adj, n, init_labels, rounds=3):
    labels = list(init_labels)
    for _ in range(rounds):
        new = []
        for v in range(n):
            ms = sorted(labels[u] for u in adj[v])
            new.append((labels[v], tuple(ms)))
        uniq = {lab: i for i, lab in enumerate(sorted(set(new)))}
        labels = [uniq[x] for x in new]
    classes = defaultdict(list)
    for v, c in enumerate(labels): classes[c].append(v)
    return list(classes.values()), labels

def coarse_grain(graph, n, partition):
    idx = {}
    for i, block in enumerate(partition):
        for v in block: idx[v] = i
    edges = set()
    for e in graph:
        u, v = list(e); a, b = idx[u], idx[v]
        if a != b: edges.add(frozenset([a, b]))
    return frozenset(edges), len(partition), idx

# ============================================================
# T⊥: TYPE-LEVEL RANDOM WALK (monograph Πb pushforward)
# ============================================================

def build_type_random_walk(adj, n, vertex_types):
    """Build random walk transition matrix on collar types.
    P[b,a] = Prob(random walk from type-a vertex lands in type-b vertex)
    """
    all_types = sorted(set(vertex_types.values()))
    type_idx = {t: i for i, t in enumerate(all_types)}
    k = len(all_types)
    
    # Count transitions
    trans = np.zeros((k, k))
    for v in range(n):
        tv = vertex_types[v]
        deg = len(adj[v])
        if deg == 0: continue
        for u in adj[v]:
            tu = vertex_types[u]
            trans[type_idx[tu], type_idx[tv]] += 1.0 / deg
    
    # Normalize columns (make column-stochastic)
    col_sums = trans.sum(axis=0)
    col_sums[col_sums == 0] = 1
    T = trans / col_sums
    
    return all_types, T

# ============================================================
# FULL LC ANALYSIS
# ============================================================

def full_lc_analysis(graph, n, name="", kstar=1, wl_rounds=3):
    adj = adjacency(graph, n)
    beta = cycle_rank(graph, n)
    
    # Gadgets
    tris = find_induced_triangles(graph, n)
    sqs = find_induced_squares(graph, n)
    cubes = find_induced_cubes(graph, n) if n <= 30 else []
    
    # Per-vertex gadget incidence
    tri_inc = Counter(); sq_inc = Counter(); cube_inc = Counter()
    for t in tris:
        for v in t: tri_inc[v] += 1
    for s in sqs:
        for v in s: sq_inc[v] += 1
    for c in cubes:
        for v in c: cube_inc[v] += 1
    
    # Carrier overlap
    tri_c = get_carriers(tris, graph)
    sq_c = get_carriers(sqs, graph)
    cube_c = get_carriers(cubes, graph)
    m1p = compute_m_perp(graph, n, tri_c, rw=1) if tri_c else {}
    m2p = compute_m_perp(graph, n, sq_c, rw=2) if sq_c else {}
    m3p = compute_m_perp(graph, n, cube_c, rw=3) if cube_c else {}
    
    # Carrier-summed supply
    ts1 = sum(m1p.values())/3.0 if m1p else 0
    ts2 = sum(m2p.values())/4.0 if m2p else 0
    ts3 = sum(m3p.values())/6.0 if m3p else 0
    
    # Strict coverage
    cycles = fundamental_cycles(graph, n)
    c1, c2, c3 = compute_strict_coverage(graph, n, cycles, tris, sqs, cubes)
    phi1 = len(c1)/beta if beta > 0 else 0
    phi2 = len(c2)/beta if beta > 0 else 0
    phi3 = len(c3)/beta if beta > 0 else 0
    
    # Collar types on ALL vertices (boundary = all for these small graphs)
    vtx_types = {}
    for v in range(n):
        vtx_types[v] = collar_type_v2(adj, n, v, kstar, tri_inc, sq_inc, cube_inc)
    
    support = sorted(set(vtx_types.values()))
    type_freq = Counter(vtx_types.values())
    
    # Feature maps g2, g3 on types
    type_g2 = {}; type_g3 = {}
    for t in support:
        verts_of_type = [v for v in range(n) if vtx_types[v] == t]
        type_g2[t] = np.mean([sq_inc.get(v, 0) for v in verts_of_type])
        type_g3[t] = np.mean([cube_inc.get(v, 0) for v in verts_of_type])
    
    # T⊥ via type-level random walk
    type_list, T_matrix = build_type_random_walk(adj, n, vtx_types)
    
    # Eigendecomposition of T^T (left eigenvectors of T)
    k = len(type_list)
    if k > 0:
        eigvals, eigvecs = np.linalg.eig(T_matrix.T)
        # Keep real eigenvalues with |λ| > 0.05
        real_mask = np.abs(eigvals.imag) < 0.01
        stable_vals = [eigvals[i].real for i in range(len(eigvals)) if real_mask[i] and abs(eigvals[i].real) > 0.05]
        stable_vecs = [eigvecs[:, i].real for i in range(len(eigvals)) if real_mask[i] and abs(eigvals[i].real) > 0.05]
        dim_stable = len(stable_vals)
    else:
        stable_vals = []; stable_vecs = []; dim_stable = 0
    
    # NonRed: find t, t' with g2(t)=g2(t') but g3(t)≠g3(t')
    nonred_pass = False; nonred_pair = None
    for i in range(len(support)):
        for j in range(i+1, len(support)):
            t, tp = support[i], support[j]
            if abs(type_g2[t] - type_g2[tp]) < 1e-9 and abs(type_g3[t] - type_g3[tp]) > 1e-9:
                nonred_pass = True; nonred_pair = (t, tp); break
        if nonred_pass: break
    
    # SpecAct: projection of g3 onto stable eigenspace
    eta = 0.0
    if stable_vecs and k > 0:
        g3_vec = np.array([type_g3[t] for t in type_list])
        if np.linalg.norm(g3_vec) > 1e-12:
            E = np.column_stack(stable_vecs)
            proj = E @ np.linalg.lstsq(E, g3_vec, rcond=None)[0]
            eta = np.linalg.norm(proj)
    
    regime = "3-cell" if phi3 > 0 else ("mixed" if phi2 > 0 and phi1 > 0 else 
             ("2-cell" if phi2 > 0 else ("tri" if phi1 > 0 else "sub-1")))
    
    return {
        'name': name, 'n': n, 'E': len(graph), 'beta': beta,
        'tri': len(tris), 'sq': len(sqs), 'Q3': len(cubes),
        'ts1': ts1, 'ts2': ts2, 'ts3': ts3,
        'phi1': phi1, 'phi2': phi2, 'phi3': phi3,
        'regime': regime,
        'n_types': len(support), 'support': support,
        'type_g2': type_g2, 'type_g3': type_g3,
        'T_size': k, 'T_matrix': T_matrix,
        'stable_eigenvalues': sorted(stable_vals, reverse=True),
        'dim_stable': dim_stable,
        'nonred_pass': nonred_pass, 'nonred_pair': nonred_pair,
        'spec_act_eta': eta, 'spec_act_pass': eta > 1e-6,
    }

# ============================================================
# LC PRINTER
# ============================================================

def print_lc(r2, r3):
    print("="*70)
    print(f"LADDER CERTIFICATE LC({r2['name']} → {r3['name']})")
    print("="*70)
    
    I2 = {k for k in [1,2,3] if [r2['phi1'],r2['phi2'],r2['phi3']][k-1]>0}
    I3 = {k for k in [1,2,3] if [r3['phi1'],r3['phi2'],r3['phi3']][k-1]>0}
    
    print(f"""META:
  R2: {r2['name']} (n={r2['n']}, |E|={r2['E']}, β={r2['beta']})
  R3: {r3['name']} (n={r3['n']}, |E|={r3['E']}, β={r3['beta']})
  gadgets: C3, C4, Q3  |  Rw=(1,2,3)  |  k*=1  |  WL rounds=3

Φ (strict certification):
  R2: (φ₁,φ₂,φ₃) = ({r2['phi1']:.3f}, {r2['phi2']:.3f}, {r2['phi3']:.3f})  regime={r2['regime']}
  R3: (φ₁,φ₂,φ₃) = ({r3['phi1']:.3f}, {r3['phi2']:.3f}, {r3['phi3']:.3f})  regime={r3['regime']}
  I₂={I2}, I₃={I3}

S (collar-type support):
  |S₂|={r2['n_types']}, |S₃|={r3['n_types']}

T (type-level random walk):
  T₂: {r2['T_size']}×{r2['T_size']}, spectrum: {[f'{v:.4f}' for v in r2['stable_eigenvalues'][:6]]}
  T₃: {r3['T_size']}×{r3['T_size']}, spectrum: {[f'{v:.4f}' for v in r3['stable_eigenvalues'][:6]]}
  d₂ = {r2['dim_stable']},  d₃ = {r3['dim_stable']}""")
    
    print(f"\nNonRed (non-redundant cube visibility on S₃):")
    if r3['nonred_pass']:
        t, tp = r3['nonred_pair']
        print(f"  Witness pair: g₂={r3['type_g2'][t]:.2f}={r3['type_g2'][tp]:.2f}, "
              f"g₃={r3['type_g3'][t]:.2f}≠{r3['type_g3'][tp]:.2f}")
        print(f"  PASS ✓")
    else:
        print(f"  g₂/g₃ on support:")
        for t in sorted(r3['support'], key=lambda x: (r3['type_g2'].get(x,0), r3['type_g3'].get(x,0))):
            freq = sum(1 for v in range(r3['n']) if True)  # placeholder
            print(f"    g₂={r3['type_g2'][t]:.2f}, g₃={r3['type_g3'][t]:.2f}")
        print(f"  FAIL ✗")
    
    print(f"\nSpecAct: η = {r3['spec_act_eta']:.6f}  {'PASS ✓' if r3['spec_act_pass'] else 'FAIL ✗'}")
    
    d2, d3 = r2['dim_stable'], r3['dim_stable']
    strict = r3['phi3'] > 0 and r3['nonred_pass'] and r3['spec_act_pass'] and d3 > d2
    
    if strict:
        failing = "none — all gates passed"
    elif r3['phi3'] <= 0: failing = "φ₃ = 0"
    elif not r3['nonred_pass']: failing = "NonRed"
    elif not r3['spec_act_pass']: failing = "SpecAct"
    elif d3 <= d2: failing = f"DIM equality (d₂={d2}, d₃={d3})"
    else: failing = "unknown"
    
    print(f"\nVERDICT: {'STRICT LADDER CERTIFIED ✓' if strict else 'NO STRICT JUMP'}")
    print(f"  First failing gate: {failing}")
    print("="*70)
    return strict, failing

# ============================================================
# RUN
# ============================================================

print("="*70)
print("LADDER CERTIFICATE PIPELINE v2")
print("  Fixed eigenspace, composite substrates, enriched collar types")
print("="*70)

# ---- R2: Pure grids (2-cell, no cubes) ----
print("\n── R2 FAMILY: Grids ──")
r2_configs = [(3,3), (3,4), (4,4), (5,5)]
r2_results = {}
for r, c in r2_configs:
    g, n = build_grid(r, c)
    res = full_lc_analysis(g, n, name=f"Grid-{r}x{c}")
    r2_results[res['name']] = res
    print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
          f"|S|={res['n_types']}, d={res['dim_stable']}, "
          f"spec={[f'{v:.3f}' for v in res['stable_eigenvalues'][:4]]}")

# ---- R3: Composite Grid+Cube substrates ----
print("\n── R3 FAMILY: Composite Grid+Cube ──")
r3_results = {}

# Grid-3x3 + Q3 (bridge=1)
g, n, _, _ = build_composite_grid_cube(3, 3, bridge_len=1)
res = full_lc_analysis(g, n, name="Grid3x3+Q3(b1)")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Grid-4x4 + Q3 (bridge=1)
g, n, _, _ = build_composite_grid_cube(4, 4, bridge_len=1)
res = full_lc_analysis(g, n, name="Grid4x4+Q3(b1)")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Grid-4x4 + Q3 (bridge=0, direct attachment)
g, n, _, _ = build_composite_grid_cube(4, 4, bridge_len=0)
res = full_lc_analysis(g, n, name="Grid4x4+Q3(b0)")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Grid-3x4 + Q3
g, n, _, _ = build_composite_grid_cube(3, 4, bridge_len=1)
res = full_lc_analysis(g, n, name="Grid3x4+Q3(b1)")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Double grid + cube
g, n = build_double_grid_cube(3, 3, 2, 3, bridge_len=1)
res = full_lc_analysis(g, n, name="DblGrid3+Q3")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Pure Q3 for comparison
g, n = build_hypercube(3)
res = full_lc_analysis(g, n, name="Q3")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# Cyl-3x4
g, n = build_cylinder(3, 4)
res = full_lc_analysis(g, n, name="Cyl-3x4")
r3_results[res['name']] = res
print(f"  {res['name']}: n={n}, β={res['beta']}, φ₂={res['phi2']:.3f}, "
      f"φ₃={res['phi3']:.3f}, |S|={res['n_types']}, d={res['dim_stable']}")

# ---- PRODUCE LC RECORDS ----
print("\n\n")

lc_pairs = [
    ("Grid-4x4", "Grid4x4+Q3(b1)"),
    ("Grid-4x4", "Grid4x4+Q3(b0)"),
    ("Grid-3x3", "Grid3x3+Q3(b1)"),
    ("Grid-3x4", "Grid3x4+Q3(b1)"),
    ("Grid-4x4", "DblGrid3+Q3"),
    ("Grid-4x4", "Q3"),
    ("Grid-4x4", "Cyl-3x4"),
]

results_all = {}
results_all.update(r2_results)
results_all.update(r3_results)

lc_verdicts = []
for r2name, r3name in lc_pairs:
    if r2name not in results_all or r3name not in results_all:
        continue
    jump, failing = print_lc(results_all[r2name], results_all[r3name])
    lc_verdicts.append((r2name, r3name, jump, failing))
    print()

# ---- SUMMARY ----
print("\n" + "="*80)
print("LC SUMMARY TABLE")
print("="*80)
print(f"{'R2':<14} {'R3':<20} {'φ₃':>5} {'|S₃|':>5} {'NonRed':>8} {'SpecAct':>8} {'d₂':>4} {'d₃':>4} {'Verdict':>12}")
print("─"*80)
for r2n, r3n, jump, failing in lc_verdicts:
    r2 = results_all[r2n]; r3 = results_all[r3n]
    print(f"{r2n:<14} {r3n:<20} {r3['phi3']:>5.2f} {r3['n_types']:>5} "
          f"{'✓' if r3['nonred_pass'] else '✗':>8} {'✓' if r3['spec_act_pass'] else '✗':>8} "
          f"{r2['dim_stable']:>4} {r3['dim_stable']:>4} "
          f"{'JUMP ✓' if jump else failing:>12}")

print(f"""
ANALYSIS:
  The composite substrates (Grid+Q3) force structural diversity: some vertices 
  participate in squares only, others in cubes, creating the collar-type variation
  needed for NonRed. The key diagnostic question is whether this variation also
  creates genuinely new stable eigenmodes (SpecAct + dim jump).
""")

# ============================================================
