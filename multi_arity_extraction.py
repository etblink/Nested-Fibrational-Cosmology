
"""Multi-arity label extraction (V+E+P2+P3+T+C4 style) for NFC Toy Model 5.

This module extends the existing ladder-certificate collar typing by adding:
- P2: induced length-2 path (wedge) counts per vertex
- P3: induced length-3 path counts with the vertex as an internal node
- E: neighbor-degree multiset (edge-local profile) within a chosen neighborhood U

It also includes a cube-seeded ladder construction to force Uniform NonRed locally.

Depends on witness_v3.py from the NFC codebase.
"""

from collections import Counter, defaultdict
import itertools

import witness_v3 as w3

def adjacency(graph, n):
    return w3.adjacency(graph, n)

def radius_ball(graph, n, center, radius):
    return w3.radius_ball(graph, n, center, radius)

def induced_subgraph(graph, vertices):
    return w3.induced_subgraph(graph, vertices)

def triangles(graph, n):
    adj = adjacency(graph, n)
    out = set()
    for a in range(n):
        for b in adj[a]:
            if b <= a: 
                continue
            for c in adj[a] & adj[b]:
                if c <= b:
                    continue
                tri = frozenset([a, b, c])
                if len(induced_subgraph(graph, tri)) == 3:
                    out.add(tri)
    return list(out)

def squares(graph, n):
    return w3.find_induced_squares(graph, n)

def p2_p3_counts(graph, n, adj=None):
    if adj is None:
        adj = adjacency(graph, n)
    p2 = Counter()
    for v in range(n):
        nbrs = list(adj[v])
        for i in range(len(nbrs)):
            a = nbrs[i]
            for j in range(i + 1, len(nbrs)):
                b = nbrs[j]
                if frozenset([a, b]) not in graph:
                    p2[v] += 1

    p3 = Counter()
    for v in range(n):
        for a in adj[v]:
            for c in adj[v]:
                if c == a:
                    continue
                if frozenset([a, c]) in graph:
                    continue
                for d in adj[c]:
                    if d == v or d == a:
                        continue
                    if frozenset([v, d]) in graph:
                        continue
                    if frozenset([a, d]) in graph:
                        continue
                    p3[v] += 1
    return p2, p3

def incidence_counters(tris, sqs):
    tri_inc = Counter()
    sq_inc = Counter()
    for t in tris:
        for v in t:
            tri_inc[v] += 1
    for s in sqs:
        for v in s:
            sq_inc[v] += 1
    return tri_inc, sq_inc

def cube_incidence_from_cubes(cubes):
    cube_inc = Counter()
    for c in cubes:
        for v in c:
            cube_inc[v] += 1
    return cube_inc

def collar_type_multi(adj, graph, n, center, U, tri_inc, sq_inc, cube_inc, p2, p3, kstar=1):
    dist = {center: 0}
    frontier = [center]
    for d in range(1, kstar + 1):
        new = []
        for v in frontier:
            for nb in adj[v]:
                if nb in U and nb not in dist:
                    dist[nb] = d
                    new.append(nb)
        frontier = new

    sig = []
    for v in sorted(dist.keys()):
        nbrs_in_U = adj[v] & U
        neigh_deg_multiset = tuple(sorted(len(adj[u]) for u in nbrs_in_U))
        sig.append(
            (
                dist[v],
                len(adj[v]),
                len(nbrs_in_U),
                tri_inc.get(v, 0),
                sq_inc.get(v, 0),
                cube_inc.get(v, 0),
                p2.get(v, 0),
                p3.get(v, 0),
                neigh_deg_multiset,
            )
        )
    return tuple(sorted(sig))

def local_loads(graph, n, R0=2, kstar=1, cubes=None):
    adj = adjacency(graph, n)
    tris = triangles(graph, n)
    sqs = squares(graph, n)
    tri_inc, sq_inc = incidence_counters(tris, sqs)
    cube_inc = cube_incidence_from_cubes(cubes or [])
    p2, p3 = p2_p3_counts(graph, n, adj)

    L = {}
    for v in range(n):
        U = radius_ball(graph, n, v, R0)
        labels = set()
        for u in U:
            labels.add(
                collar_type_multi(adj, graph, n, u, U, tri_inc, sq_inc, cube_inc, p2, p3, kstar=kstar)
            )
        L[v] = len(labels)
    return L, min(L.values()), max(L.values())

# -----------------------------
# Cube-seeded ladder builder
# -----------------------------

def add_fan3(edges, next_vid):
    c = next_vid
    next_vid += 1
    squares = []
    for _ in range(3):
        a, b, d = next_vid, next_vid + 1, next_vid + 2
        next_vid += 3
        edges.add(frozenset([c, a]))
        edges.add(frozenset([a, b]))
        edges.add(frozenset([b, d]))
        edges.add(frozenset([d, c]))
        squares.append(frozenset([c, a, b, d]))
    return c, squares, next_vid

def add_cube(edges, next_vid):
    verts = list(range(next_vid, next_vid + 8))
    next_vid += 8
    for v in range(8):
        for bit in range(3):
            u = v ^ (1 << bit)
            if u > v:
                edges.add(frozenset([verts[v], verts[u]]))
    return frozenset(verts), next_vid

def cube_seed_graph(base_graph, base_n, seed_vertices):
    edges = set(base_graph)
    next_vid = base_n
    cubes = []
    for u in seed_vertices:
        c, fan_sqs, next_vid = add_fan3(edges, next_vid)
        cube_verts, next_vid = add_cube(edges, next_vid)
        cubes.append(cube_verts)

        edges.add(frozenset([u, c]))

        cube_list = sorted(cube_verts)
        q0, q7 = cube_list[0], cube_list[-1]
        edges.add(frozenset([c, q0]))
        edges.add(frozenset([c, q7]))

        for sq in fan_sqs:
            # pick the vertex in sq not adjacent to c (this is b in c-a-b-d-c)
            for v in sq:
                if v == c:
                    continue
                if frozenset([c, v]) not in edges:
                    edges.add(frozenset([v, q0]))
                    break

    return frozenset(edges), next_vid, cubes
