import networkx as nx
import random
import numpy as np

class Layout:
    def __init__(self, vertices, vsep, neighbors, disconnected):
        self.vertices = vertices
        self.vsep = vsep
        self.neighbors = neighbors
        self.disconnected = disconnected

def create_Layout(G, vertices):
    vsep, neighbors = vsep_and_neighbors(G, vertices)
    return Layout(vertices, vsep, neighbors, list(G.nodes() - vertices))

def vsep_and_neighbors(G, vertices):
    vs, nbs = 0, []
    for i in range(len(vertices)):
        S = vertices[0:i+1]
        nbs = [v for v in set(G.nodes) - set(S) if any(G.has_edge(v, s) for s in S)]
        vsi = len(nbs)
        if vsi > vs:
            vs = vsi
    return vs, nbs

def vsep(layout):
    return layout.vsep

def vsep_last(layout):
    return len(layout.neighbors)

def vsep_updated(G, layout, v):
    vs = vsep_last(layout)
    if v in layout.neighbors:
        vs -= 1
    for w in G.neighbors(v):
        if w not in layout.vertices and w not in layout.neighbors:
            vs += 1
    vs = max(vs, layout.vsep)
    return vs

def vsep_updated_neighbors(G, layout, v):
    vs = vsep_last(layout)
    nbs = layout.neighbors.copy()
    disc = layout.disconnected.copy()
    if v in nbs:
        nbs.remove(v)
        vs -= 1
    else:
        disc.remove(v)
    for w in G.neighbors(v):
        if w not in layout.vertices and w not in nbs:
            vs += 1
            nbs.append(w)
            disc.remove(w)
    vs = max(vs, layout.vsep)
    return vs, nbs, disc

def compose(G, layout, v):
    vertices = layout.vertices + [v]
    vs_new, neighbors_new, disconnected = vsep_updated_neighbors(G, layout, v)
    vs_new = max(layout.vsep, vs_new)
    return Layout(vertices, vs_new, neighbors_new, disconnected)

def branch_and_bound_recursive(G, P, L, vP):
    V = list(G.nodes)
    
    if (vsep(P) < vsep(L)) and P not in vP:
        P2 = greedy_exact(G, P)
        vsep_P2 = vsep(P2)
        if sorted(P2.vertices) == V and vsep_P2 < vsep(L):
            return P2
        else:
            current = vsep(L)
            remaining = P2.neighbors + P2.disconnected
            vsep_order = sorted(remaining, key=lambda x: vsep_updated(G, P2, x))
            for v in vsep_order:
                if vsep_updated(G, P2, v) < vsep(L):
                    L3 = branch_and_bound_recursive(G, compose(G, P2, v), L, vP)
                    if vsep(L3) < vsep(L):
                        L = L3
            # update Layout table
            vP[P] = not (vsep(L) < current and vsep(P) == vsep(L))
    return L

def branch_and_bound(G):
    return branch_and_bound_recursive(G, create_Layout(G, []), create_Layout(G, list(G.nodes())), {})

def greedy_exact(G, P):
    keepgoing = True
    while keepgoing:
        keepgoing = False
        for lst in (P.disconnected, P.neighbors):
            for v in lst:
                if all(nb in P.vertices or nb in P.neighbors for nb in nx.neighbors(G, v)):
                    P = compose(G, P, v)
                    keepgoing = True
        for v in P.neighbors:
            if sum(1 for nb in nx.neighbors(G, v) if nb not in P.vertices and nb not in P.neighbors) == 1:
                P = compose(G, P, v)
                keepgoing = True
    return P

def greedy_decompose(G):
    P = create_Layout(G, [])
    while True:
        P = greedy_exact(G, P)
        if P.neighbors:
            P = greedy_step(G, P, P.neighbors)
        elif P.disconnected:
            P = greedy_step(G, P, P.disconnected)
        else:
            break
    return P

def greedy_step(G, P, lst):
    layouts = [compose(G, P, v) for v in lst]
    costs = [layout.vsep for layout in layouts]
    best_cost = min(costs)
    best_layouts = [layouts[i] for i in range(len(layouts)) if costs[i] == best_cost]
    return random.choice(best_layouts)


class Branching:
    pass

class Greedy:
    def __init__(self, nrepeat=10):
        self.nrepeat = nrepeat

def pathwidth(g, method):
    if isinstance(method, Branching):
        return branch_and_bound(g)
    elif isinstance(method, Greedy):
        res = []
        for _ in range(method.nrepeat):
            res.append(greedy_decompose(g))
        return min(res, key=lambda x: vsep(x))


adjacency_matrix = np.array([[0, 1, 0, 1,1],
                             [1, 0, 1, 0, 0],
                             [0, 1, 0, 1, 1],
                             [1, 0, 1, 0, 0],
                             [1,0,1,0,0]])

adjacency_matrix = np.array([[0, 0, 1, 0,0],
                             [0, 0, 0, 1, 0],
                             [1, 0, 0, 0, 1],
                             [0, 1, 0, 0, 1],
                             [0,1,0,1,0]])

# Create a graph from the adjacency matrix
G = nx.from_numpy_array(adjacency_matrix)
P = Layout([], 0, [0,1,2,3,4], [])
print(pathwidth(G, Greedy()).vertices)

