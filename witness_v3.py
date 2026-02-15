"""
Witness-Inequivalent Variables v3 — Full ChatGPT audit fixes applied.

Fixes from audit:
1. Q3 connectivity check (len(color)==8)
2. Strict coverage: gadget certifies cycle iff ALL gadget edges ⊂ cycle edges
3. φ-aware D9: use σ̃/φ, not raw σ
4. σ⊥ signatures sorted (order-invariant)
5. Triangle gadgets (C3) added → D9′ and D9″
6. Carrier-summed supply σ̃⊥ replaces class counts σ⊥
"""

import itertools
from collections import defaultdict, Counter

# ============================================================
# GRAPH INFRASTRUCTURE
# ============================================================

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

def radius_ball(graph, n, center, radius):
    adj = adjacency(graph, n)
    ball = {center}
    frontier = {center}
    for _ in range(radius):
        new_frontier = set()
        for v in frontier:
            for u in adj[v]:
                if u not in ball:
                    new_frontier.add(u)
                    ball.add(u)
        frontier = new_frontier
    return frozenset(ball)

def induced_subgraph(graph, vertices):
    return frozenset(e for e in graph if e.issubset(vertices))

# ============================================================
# GRAPH BUILDERS
# ============================================================

def build_barbell(k1, n_bridge, k2):
    n = k1 + n_bridge + k2
    edges = set()
    for i in range(k1):
        for j in range(i+1, k1):
            edges.add(frozenset([i, j]))
    left_attach = k1 - 1
    bridge_vertices = list(range(k1, k1 + n_bridge))
    right_attach = k1 + n_bridge
    if bridge_vertices:
        edges.add(frozenset([left_attach, bridge_vertices[0]]))
        for i in range(len(bridge_vertices) - 1):
            edges.add(frozenset([bridge_vertices[i], bridge_vertices[i+1]]))
        edges.add(frozenset([bridge_vertices[-1], right_attach]))
    else:
        edges.add(frozenset([left_attach, right_attach]))
    right_start = k1 + n_bridge
    for i in range(k2):
        for j in range(i+1, k2):
            edges.add(frozenset([right_start + i, right_start + j]))
    return frozenset(edges), n

def build_grid(rows, cols):
    n = rows * cols
    edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols: edges.add(frozenset([v, v + 1]))
            if r + 1 < rows: edges.add(frozenset([v, v + cols]))
    return frozenset(edges), n

def build_cylinder(rows, cols):
    n = rows * cols
    edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            edges.add(frozenset([v, r * cols + (c + 1) % cols]))
            if r + 1 < rows: edges.add(frozenset([v, v + cols]))
    return frozenset(edges), n

def build_torus(rows, cols):
    n = rows * cols
    edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            edges.add(frozenset([v, r * cols + (c + 1) % cols]))
            edges.add(frozenset([v, ((r + 1) % rows) * cols + c]))
    return frozenset(edges), n

def build_ladder(length):
    n = 2 * length
    edges = set()
    for i in range(length):
        edges.add(frozenset([i, i + length]))
        if i + 1 < length:
            edges.add(frozenset([i, i + 1]))
            edges.add(frozenset([i + length, i + 1 + length]))
    return frozenset(edges), n

def build_k4_ladder_k4(ladder_len):
    left_size = 4
    ladder_verts = 2 * ladder_len
    n = left_size + ladder_verts + 4
    edges = set()
    for i in range(4):
        for j in range(i+1, 4):
            edges.add(frozenset([i, j]))
    lad_start = 4
    for i in range(ladder_len):
        top = lad_start + i
        bot = lad_start + ladder_len + i
        edges.add(frozenset([top, bot]))
        if i + 1 < ladder_len:
            edges.add(frozenset([top, top + 1]))
            edges.add(frozenset([bot, bot + 1]))
    edges.add(frozenset([2, lad_start]))
    edges.add(frozenset([3, lad_start + ladder_len]))
    right_start = lad_start + ladder_verts
    for i in range(4):
        for j in range(i+1, 4):
            edges.add(frozenset([right_start + i, right_start + j]))
    top_end = lad_start + ladder_len - 1
    bot_end = lad_start + 2 * ladder_len - 1
    edges.add(frozenset([top_end, right_start]))
    edges.add(frozenset([bot_end, right_start + 1]))
    return frozenset(edges), n

def build_hypercube(dim):
    n = 2 ** dim
    edges = set()
    for v in range(n):
        for bit in range(dim):
            u = v ^ (1 << bit)
            if u > v: edges.add(frozenset([v, u]))
    return frozenset(edges), n

# ============================================================
# GADGET DETECTION
# ============================================================

def find_induced_triangles(graph, n):
    """Find all induced C3 (triangles)."""
    adj = adjacency(graph, n)
    triangles = set()
    for a in range(n):
        for b in adj[a]:
            if b <= a: continue
            for c in adj[a] & adj[b]:
                if c <= b: continue
                tri = frozenset([a, b, c])
                # Verify induced: exactly 3 edges
                if len(induced_subgraph(graph, tri)) == 3:
                    triangles.add(tri)
    return list(triangles)

def find_induced_squares(graph, n):
    adj = adjacency(graph, n)
    squares = set()
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
                    squares.add(frozenset([a,b,c,d]))
    verified = []
    for sq in squares:
        if len(induced_subgraph(graph, sq)) == 4:
            verified.append(sq)
    return verified

def is_q3(graph_edges, vertices):
    if len(vertices) != 8: return False
    verts = sorted(vertices)
    sub_adj = defaultdict(set)
    edge_count = 0
    for e in graph_edges:
        if e.issubset(vertices):
            u, v = list(e)
            sub_adj[u].add(v)
            sub_adj[v].add(u)
            edge_count += 1
    if edge_count != 12: return False
    if not all(len(sub_adj[v]) == 3 for v in verts): return False
    # Bipartite check with connectivity
    color = {}
    queue = [verts[0]]
    color[verts[0]] = 0
    bipartite = True
    while queue and bipartite:
        v = queue.pop(0)
        for u in sub_adj[v]:
            if u not in color:
                color[u] = 1 - color[v]
                queue.append(u)
            elif color[u] == color[v]:
                bipartite = False
    if not bipartite: return False
    # FIX #1: connectivity check
    if len(color) != 8: return False
    # Triangle-free check
    for v in verts:
        for u in sub_adj[v]:
            if sub_adj[v] & sub_adj[u]:
                return False
    part0 = [v for v in verts if color.get(v) == 0]
    part1 = [v for v in verts if color.get(v) == 1]
    if len(part0) != 4 or len(part1) != 4: return False
    return True

def find_induced_cubes(graph, n):
    if n < 8: return []
    cubes = []
    for combo in itertools.combinations(range(n), 8):
        if is_q3(graph, frozenset(combo)):
            cubes.append(frozenset(combo))
    return cubes

def cube_face_squares(graph, cube_verts):
    """Get the 6 face-squares of a Q3 cube."""
    sub_adj = defaultdict(set)
    for e in graph:
        if e.issubset(cube_verts):
            u, v = list(e)
            sub_adj[u].add(v)
            sub_adj[v].add(u)
    faces = []
    verts = sorted(cube_verts)
    for combo in itertools.combinations(verts, 4):
        combo_set = frozenset(combo)
        edges_in = induced_subgraph(graph, combo_set)
        if len(edges_in) == 4:
            degs = Counter()
            for e in edges_in:
                for v in e: degs[v] += 1
            if all(d == 2 for d in degs.values()):
                faces.append(combo_set)
    return faces

# ============================================================
# CARRIER OVERLAP AND WITNESS EQUIVALENCE
# ============================================================

def get_carriers(gadgets, graph):
    carrier_to_gadgets = defaultdict(list)
    for gadget in gadgets:
        gadget_edges = induced_subgraph(graph, gadget)
        for edge in gadget_edges:
            carrier_to_gadgets[edge].append(gadget)
    return carrier_to_gadgets

def local_pattern(graph, n, carrier_edge, gadget, radius):
    u, v = sorted(carrier_edge)
    adj = adjacency(graph, n)
    ball = set()
    for center in [u, v]:
        ball |= radius_ball(graph, n, center, radius)
    ball = frozenset(ball)
    def bfs_dist(source, target, adj_map, max_d):
        if source == target: return 0
        visited = {source}; frontier = {source}
        for d in range(1, max_d+1):
            new_f = set()
            for x in frontier:
                for y in adj_map[x]:
                    if y not in visited:
                        if y == target: return d
                        visited.add(y); new_f.add(y)
            frontier = new_f
        return max_d + 1
    vertex_sigs = []
    for w in sorted(ball):
        d_u = bfs_dist(u, w, adj, radius + 1)
        d_v = bfs_dist(v, w, adj, radius + 1)
        deg_w = len(adj[w])
        in_gadget = 1 if w in gadget else 0
        nbrs_in_ball = len(adj[w] & ball)
        vertex_sigs.append((d_u, d_v, deg_w, in_gadget, nbrs_in_ball))
    return (tuple(sorted(vertex_sigs)), len(ball))

def compute_m_perp(graph, n, carrier_to_gadgets, radius_w=2):
    carrier_m_perp = {}
    for carrier, gadgets in carrier_to_gadgets.items():
        patterns = defaultdict(list)
        for gadget in gadgets:
            pat = local_pattern(graph, n, carrier, gadget, radius_w)
            patterns[pat].append(gadget)
        carrier_m_perp[carrier] = len(patterns)
    return carrier_m_perp

# FIX #4: order-invariant gadget signatures
def compute_sigma_perp(graph, n, gadgets, radius_w=2):
    gadget_sigs = set()
    for g in gadgets:
        sig_parts = []
        g_edges = sorted(induced_subgraph(graph, g), key=lambda e: tuple(sorted(e)))
        for edge in g_edges:
            pat = local_pattern(graph, n, edge, g, radius_w)
            sig_parts.append(pat)
        gadget_sigs.add(tuple(sorted(sig_parts)))  # FIX: sorted for order-invariance
    return len(gadget_sigs)

# ============================================================
# CYCLE ANALYSIS
# ============================================================

def cycle_rank(graph, n):
    adj = adjacency(graph, n)
    visited = set(); components = 0
    for v in range(n):
        if v not in visited:
            components += 1
            stack = [v]
            while stack:
                u = stack.pop()
                if u in visited: continue
                visited.add(u)
                for w in adj[u]:
                    if w not in visited: stack.append(w)
    return len(graph) - n + components

def fundamental_cycles(graph, n):
    adj = adjacency(graph, n)
    tree_edges = set(); parent = {}; visited = set()
    for start in range(n):
        if start in visited: continue
        queue = [start]; visited.add(start); parent[start] = -1
        while queue:
            v = queue.pop(0)
            for u in adj[v]:
                if u not in visited:
                    visited.add(u); parent[u] = v
                    tree_edges.add(frozenset([u, v])); queue.append(u)
    non_tree = [e for e in graph if e not in tree_edges]
    cycles = []
    for edge in non_tree:
        u, v = sorted(edge)
        def path_to_root(x):
            path = []
            while x != -1: path.append(x); x = parent[x]
            return path
        path_u = path_to_root(u); path_v = path_to_root(v)
        set_u = set(path_u)
        lca = None
        for x in path_v:
            if x in set_u: lca = x; break
        if lca is None: continue
        cycle_edges = {frozenset([u, v])}
        x = u
        while x != lca: cycle_edges.add(frozenset([x, parent[x]])); x = parent[x]
        x = v
        while x != lca: cycle_edges.add(frozenset([x, parent[x]])); x = parent[x]
        cycles.append({'edges': frozenset(cycle_edges), 'length': len(cycle_edges)})
    return cycles

# FIX #2: STRICT coverage — gadget certifies cycle iff ALL gadget edges ⊂ cycle edges
def compute_strict_coverage(graph, n, cycles, triangles, squares, cubes):
    cov_1 = set()  # triangle-certified
    cov_2 = set()  # square-certified
    cov_3 = set()  # cube-certified (via face-square)
    
    for i, cycle in enumerate(cycles):
        cycle_edges = cycle['edges']
        
        # Triangle certifies iff all 3 edges ⊂ cycle
        for tri in triangles:
            tri_edges = induced_subgraph(graph, tri)
            if tri_edges.issubset(cycle_edges):
                cov_1.add(i)
                break
        
        # Square certifies iff all 4 edges ⊂ cycle
        for sq in squares:
            sq_edges = induced_subgraph(graph, sq)
            if sq_edges.issubset(cycle_edges):
                cov_2.add(i)
                break
        
        # Cube certifies iff at least one face-square has all 4 edges ⊂ cycle
        for cube in cubes:
            faces = cube_face_squares(graph, cube)
            for face in faces:
                face_edges = induced_subgraph(graph, face)
                if face_edges.issubset(cycle_edges):
                    cov_3.add(i)
                    break
            if i in cov_3:
                break
    
    return cov_1, cov_2, cov_3

# ============================================================
# MAIN ANALYSIS (v3)
# ============================================================

def analyze(graph, n, name=""):
    print(f"\n{'─'*60}")
    print(f"{name} (n={n}, |E|={len(graph)})")
    print(f"{'─'*60}")
    
    beta = cycle_rank(graph, n)
    
    # Detect all gadget types
    triangles = find_induced_triangles(graph, n)
    squares = find_induced_squares(graph, n)
    cubes = find_induced_cubes(graph, n) if n <= 16 else []
    
    print(f"β={beta}, △={len(triangles)}, □={len(squares)}, Q₃={len(cubes)}")
    
    # Carrier overlap M⊥
    tri_carriers = get_carriers(triangles, graph)
    sq_carriers = get_carriers(squares, graph)
    cube_carriers = get_carriers(cubes, graph)
    
    tri_m_perp = compute_m_perp(graph, n, tri_carriers, radius_w=1) if tri_carriers else {}
    sq_m_perp = compute_m_perp(graph, n, sq_carriers, radius_w=2) if sq_carriers else {}
    cube_m_perp = compute_m_perp(graph, n, cube_carriers, radius_w=3) if cube_carriers else {}
    
    # σ⊥ (witness-inequivalent class counts)
    sigma_1 = compute_sigma_perp(graph, n, triangles, radius_w=1) if triangles else 0
    sigma_2 = compute_sigma_perp(graph, n, squares, radius_w=2) if squares else 0
    sigma_3 = compute_sigma_perp(graph, n, cubes, radius_w=3) if cubes else 0
    
    # FIX #6: Carrier-summed supply σ̃⊥
    Sigma_1 = sum(tri_m_perp.values()) if tri_m_perp else 0
    Sigma_2 = sum(sq_m_perp.values()) if sq_m_perp else 0
    Sigma_3 = sum(cube_m_perp.values()) if cube_m_perp else 0
    
    tilde_sigma_1 = Sigma_1 / 3.0 if Sigma_1 > 0 else 0
    tilde_sigma_2 = Sigma_2 / 4.0 if Sigma_2 > 0 else 0
    tilde_sigma_3 = Sigma_3 / 6.0 if Sigma_3 > 0 else 0
    
    # Strict coverage fractions
    cycles = fundamental_cycles(graph, n)
    cov_1, cov_2, cov_3 = compute_strict_coverage(graph, n, cycles, triangles, squares, cubes)
    
    phi_1 = len(cov_1) / beta if beta > 0 else 0
    phi_2 = len(cov_2) / beta if beta > 0 else 0
    phi_3 = len(cov_3) / beta if beta > 0 else 0
    
    # Overlap ceilings
    L1 = max(tri_m_perp.values()) if tri_m_perp else 0
    L2 = max(sq_m_perp.values()) if sq_m_perp else 0
    L3 = max(cube_m_perp.values()) if cube_m_perp else 0
    
    # FIX #3: φ-aware D9 (square+cube only)
    rhs_d9 = 0.0
    if phi_2 > 0: rhs_d9 += tilde_sigma_2 / phi_2
    if phi_3 > 0: rhs_d9 += tilde_sigma_3 / phi_3
    d9_ok = (beta <= rhs_d9) if (phi_2 > 0 or phi_3 > 0) else False
    
    # FIX #5: D9″ (triangles + squares + cubes, carrier-summed, φ-aware)
    rhs_d9pp = 0.0
    if phi_1 > 0: rhs_d9pp += tilde_sigma_1 / phi_1
    if phi_2 > 0: rhs_d9pp += tilde_sigma_2 / phi_2
    if phi_3 > 0: rhs_d9pp += tilde_sigma_3 / phi_3
    d9pp_ok = (beta <= rhs_d9pp) if (phi_1 > 0 or phi_2 > 0 or phi_3 > 0) else False
    
    # Regime classification
    if phi_3 > 0:
        regime = "3-cell"
    elif phi_2 > 0 and phi_1 > 0:
        regime = "mixed"
    elif phi_2 > 0:
        regime = "2-cell"
    elif phi_1 > 0:
        regime = "tri"
    else:
        regime = "sub-1"
    
    print(f"σ₁⊥={sigma_1}, σ₂⊥={sigma_2}, σ₃⊥={sigma_3}")
    print(f"σ̃₁⊥={tilde_sigma_1:.2f}, σ̃₂⊥={tilde_sigma_2:.2f}, σ̃₃⊥={tilde_sigma_3:.2f}")
    print(f"φ₁={phi_1:.3f}, φ₂={phi_2:.3f}, φ₃={phi_3:.3f}")
    print(f"Λ₁={L1}, Λ₂={L2}, Λ₃={L3}")
    print(f"D9(φ): β={beta} vs RHS={rhs_d9:.2f} → {'✓' if d9_ok else '✗'}")
    print(f"D9″:   β={beta} vs RHS={rhs_d9pp:.2f} → {'✓' if d9pp_ok else '✗'}")
    print(f"Regime: {regime}")
    
    return {
        'n': n, 'E': len(graph), 'beta': beta,
        'tri': len(triangles), 'sq': len(squares), 'Q3': len(cubes),
        'sigma1': sigma_1, 'sigma2': sigma_2, 'sigma3': sigma_3,
        'ts1': tilde_sigma_1, 'ts2': tilde_sigma_2, 'ts3': tilde_sigma_3,
        'phi1': phi_1, 'phi2': phi_2, 'phi3': phi_3,
        'L1': L1, 'L2': L2, 'L3': L3,
        'D9': d9_ok, 'D9pp': d9pp_ok, 'regime': regime,
        'rhs_d9': rhs_d9, 'rhs_d9pp': rhs_d9pp,
    }

# ============================================================
# RUN ON ALL GRAPH FAMILIES
# ============================================================

print("="*70)
print("WITNESS-INEQUIVALENT VARIABLES v3: FULL AUDIT FIXES")
print("  - Strict certification (full edge containment)")
print("  - Triangles (C3) as gadget family")
print("  - Carrier-summed supply σ̃⊥")  
print("  - φ-aware D9 and D9″")
print("="*70)

all_results = {}

configs = [
    # Barbells
    ('K3-b1-K3', lambda: build_barbell(3,1,3)),
    ('K3-b3-K3', lambda: build_barbell(3,3,3)),
    ('K3-b5-K3', lambda: build_barbell(3,5,3)),
    ('K4-b1-K4', lambda: build_barbell(4,1,4)),
    ('K4-b2-K4', lambda: build_barbell(4,2,4)),
    ('K4-b3-K4', lambda: build_barbell(4,3,4)),
    # Grids
    ('Grid-2x3', lambda: build_grid(2,3)),
    ('Grid-2x4', lambda: build_grid(2,4)),
    ('Grid-3x3', lambda: build_grid(3,3)),
    ('Grid-3x4', lambda: build_grid(3,4)),
    ('Grid-4x4', lambda: build_grid(4,4)),
    # Cylinders
    ('Cyl-2x4', lambda: build_cylinder(2,4)),
    ('Cyl-3x4', lambda: build_cylinder(3,4)),
    ('Cyl-2x6', lambda: build_cylinder(2,6)),
    # Tori
    ('Tor-3x3', lambda: build_torus(3,3)),
    ('Tor-3x4', lambda: build_torus(3,4)),
    ('Tor-4x4', lambda: build_torus(4,4)),
    # Ladders
    ('Ladder-3', lambda: build_ladder(3)),
    ('Ladder-4', lambda: build_ladder(4)),
    ('Ladder-5', lambda: build_ladder(5)),
    ('Ladder-6', lambda: build_ladder(6)),
    # K4-ladder-K4
    ('K4-lad2-K4', lambda: build_k4_ladder_k4(2)),
    ('K4-lad3-K4', lambda: build_k4_ladder_k4(3)),
    # Hypercubes
    ('Q2', lambda: build_hypercube(2)),
    ('Q3', lambda: build_hypercube(3)),
]

for name, builder in configs:
    g, n = builder()
    all_results[name] = analyze(g, n, name)

# ============================================================
# MASTER SUMMARY TABLE
# ============================================================

print(f"\n\n{'='*110}")
print(f"MASTER SUMMARY TABLE (v3 — strict certification, carrier-summed supply, φ-aware D9″)")
print(f"{'='*110}")
header = (f"{'Graph':<16} {'n':>3} {'β':>3} {'△':>3} {'□':>3} {'Q₃':>3} "
          f"{'σ̃₁⊥':>6} {'σ̃₂⊥':>6} {'σ̃₃⊥':>6} "
          f"{'φ₁':>5} {'φ₂':>5} {'φ₃':>5} "
          f"{'D9(φ)':>6} {'D9″':>4} {'Regime':>7}")
print(header)
print("─" * 110)

for name, builder in configs:
    r = all_results[name]
    print(f"{name:<16} {r['n']:>3} {r['beta']:>3} "
          f"{r['tri']:>3} {r['sq']:>3} {r['Q3']:>3} "
          f"{r['ts1']:>6.2f} {r['ts2']:>6.2f} {r['ts3']:>6.2f} "
          f"{r['phi1']:>5.2f} {r['phi2']:>5.2f} {r['phi3']:>5.2f} "
          f"{'✓' if r['D9'] else '✗':>6} {'✓' if r['D9pp'] else '✗':>4} "
          f"{r['regime']:>7}")

# ============================================================
# CROSS-VALIDATION WITH CHATGPT TABLE
# ============================================================

print(f"\n\n{'='*70}")
print(f"CROSS-VALIDATION: Our results vs ChatGPT's claimed table")
print(f"{'='*70}")

# ChatGPT claimed these key results:
chatgpt_claims = {
    'K3-b1-K3': {'phi1': 1.00, 'phi2': 0.00, 'D9pp': True, 'regime': 'tri'},
    'K3-b3-K3': {'phi1': 1.00, 'phi2': 0.00, 'D9pp': True, 'regime': 'tri'},
    'K4-b1-K4': {'phi1': 1.00, 'phi2': 0.00, 'D9pp': True, 'regime': 'tri'},
    'K4-b2-K4': {'phi1': 1.00, 'phi2': 0.00, 'D9pp': True, 'regime': 'tri'},
    'Grid-2x4':  {'phi1': 0.00, 'phi2': 1.00, 'D9pp': True, 'regime': '2-cell'},
    'Grid-3x3':  {'phi1': 0.00, 'phi2': 0.50, 'D9pp': True, 'regime': '2-cell'},
    'Grid-4x4':  {'phi1': 0.00, 'phi2': 0.22, 'D9pp': True, 'regime': '2-cell'},
    'Q3':        {'phi1': 0.00, 'phi2': 0.80, 'phi3': 0.80, 'D9pp': True, 'regime': '3-cell'},
    'Cyl-2x4':   {'phi1': 0.00, 'phi2': 0.80, 'phi3': 0.80, 'D9pp': True, 'regime': '3-cell'},
    'Tor-4x4':   {'phi1': 0.00, 'phi2': 0.65, 'D9pp': False, 'regime': '2-cell'},
    'K4-lad2-K4': {'D9pp': True, 'regime': 'tri'},  # ChatGPT says tri with φ1>0
    'K4-lad3-K4': {'D9pp': True, 'regime': 'tri'},
}

for name, claims in sorted(chatgpt_claims.items()):
    if name not in all_results:
        continue
    r = all_results[name]
    mismatches = []
    for key in ['phi1', 'phi2', 'phi3']:
        if key in claims:
            ours = r.get(key, 0)
            theirs = claims[key]
            if abs(ours - theirs) > 0.05:
                mismatches.append(f"{key}: ours={ours:.3f} vs theirs={theirs:.2f}")
    if 'D9pp' in claims:
        if r['D9pp'] != claims['D9pp']:
            mismatches.append(f"D9″: ours={r['D9pp']} vs theirs={claims['D9pp']}")
    if 'regime' in claims:
        # Allow "mixed" to match "tri" if phi1>0 and phi2>0
        regime_match = (r['regime'] == claims['regime'] or 
                       (r['regime'] == 'mixed' and claims['regime'] in ['tri', '2-cell']))
        if not regime_match:
            mismatches.append(f"regime: ours={r['regime']} vs theirs={claims['regime']}")
    
    status = "✓ MATCH" if not mismatches else "✗ DIFFERS"
    print(f"  {name:<16}: {status}")
    for m in mismatches:
        print(f"    → {m}")

# ============================================================
# KEY FINDINGS
# ============================================================

print(f"\n\n{'='*70}")
print(f"KEY FINDINGS (v3)")
print(f"{'='*70}")

# Count D9″ passes/fails
d9pp_pass = sum(1 for r in all_results.values() if r['D9pp'])
d9pp_fail = sum(1 for r in all_results.values() if not r['D9pp'])

print(f"""
1. D9″ (full φ-aware, carrier-summed, triangles included):
   Passed: {d9pp_pass}/{d9pp_pass+d9pp_fail}
   Failed: {d9pp_fail}/{d9pp_pass+d9pp_fail}
""")

print("   Failures:")
for name, _ in configs:
    r = all_results[name]
    if not r['D9pp']:
        print(f"     {name}: β={r['beta']}, RHS={r['rhs_d9pp']:.2f}, "
              f"φ=({r['phi1']:.2f},{r['phi2']:.2f},{r['phi3']:.2f})")

print(f"""
2. Triangle inclusion (D9 vs D9″ comparison):""")
d9_only_fail = sum(1 for r in all_results.values() if not r['D9'] and r['D9pp'])
print(f"   Graphs rescued by triangles (D9 fails, D9″ passes): {d9_only_fail}")
for name, _ in configs:
    r = all_results[name]
    if not r['D9'] and r['D9pp']:
        print(f"     {name}: D9 ✗ → D9″ ✓ (φ₁={r['phi1']:.2f}, σ̃₁⊥={r['ts1']:.2f})")

print(f"""
3. Certification regime classification:""")
for regime in ["sub-1", "tri", "mixed", "2-cell", "3-cell"]:
    graphs = [name for name, _ in configs if all_results[name]['regime'] == regime]
    if graphs:
        print(f"   {regime}: {', '.join(graphs)}")

print(f"""
4. τ vs D9″ tension status:
   Barbell family (τ-optimal): {"all pass D9″" if all(all_results[n]['D9pp'] for n,_ in configs if 'K3-b' in n or 'K4-b' in n) else "some fail D9″"}
   Grid family (D9-optimal):   {"all pass D9″" if all(all_results[n]['D9pp'] for n,_ in configs if 'Grid' in n) else "some fail D9″"}
""")
