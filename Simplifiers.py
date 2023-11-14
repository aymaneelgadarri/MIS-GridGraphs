from GridGraph import GridGraph



'''
....      ....
..●.      ....
..●.   -> ....
..●.      ..●.
'''

def vertical_simplify(G):
    g = G.graph
    for i in range(0, 3 + 4 * (G.n - 1) + 2 * G.padding - 3):
        for j in range(0, 2 + 4 * (G.n-1) + 2 * G.padding - 3):
            nodes = g.subgraph([(i + k, j + l) for k in range(4) for l in range(4)]).nodes
            occupied_nodes_block = set(node for node in nodes if nodes[node]['occupied'])
            #print(occupied_nodes_block)
            print(set([(i + 1,j + 2),(i + 2,j + 2),(i + 3,j + 2)]) - occupied_nodes_block)
            if occupied_nodes_block != set([(i + 1,j + 2),(i + 2,j + 2),(i + 3,j + 2)]):
                continue
            G.set_effective_bit(i + 3, j + 2, g.nodes[(i + 1, j + 2)]['effective_bit'])
            G.set_effective_bit(i + 1, j + 2, -1)
            G.set_occupied(i + 1, j + 2, False)
            G.set_occupied(i + 2, j + 2, False)

'''
...      ...
.●.      ...
.●.   -> ...
..●      ..●
'''

def turn1_simplify(G):
    g = G.graph
    for i in range(0, 3 + 4 * (G.n - 1) + 2 * G.padding - 3):
        for j in range(0, 2 + 4 * (G.n-1) + 2 * G.padding - 3):
            nodes = g.subgraph([(i + k, j + l) for k in range(4) for l in range(3)]).nodes
            occupied_nodes_block = set(node for node in nodes if nodes[node]['occupied'])
            #print(occupied_nodes_block)
            #print(set([(i + 1,j + 2),(i + 2,j + 2),(i + 3,j + 2)]) - occupied_nodes_block)
            if occupied_nodes_block != set([(i + 1,j + 1),(i + 2,j + 1),(i + 3,j + 2)]):
                continue
            G.set_effective_bit(i + 3, j + 2, g.nodes[(i + 1, j + 1)]['effective_bit'])
            G.set_effective_bit(i + 1, j + 1, -1)
            G.set_occupied(i + 1, j + 1, False)
            G.set_occupied(i + 2, j + 1, False)

'''
....      ....
.●..      ....
..●●   -> ...●
....      ....
'''

def turn2_simplify(G):
    g = G.graph
    for i in range(0, 3 + 4 * (G.n - 1) + 2 * G.padding - 3):
        for j in range(0, 2 + 4 * (G.n-1) + 2 * G.padding - 3):
            nodes = g.subgraph([(i + k, j + l) for k in range(4) for l in range(4)]).nodes
            occupied_nodes_block = set(node for node in nodes if nodes[node]['occupied'])
            #print(occupied_nodes_block)
            #print(set([(i + 1,j + 2),(i + 2,j + 2),(i + 3,j + 2)]) - occupied_nodes_block)
            if occupied_nodes_block != set([(i + 1,j + 1),(i + 2,j + 2),(i + 2,j + 3)]):
                continue
            G.set_effective_bit(i + 2, j + 3, g.nodes[(i + 1, j + 1)]['effective_bit'])
            G.set_effective_bit(i + 1, j + 1, -1)
            G.set_occupied(i + 1, j + 1, False)
            G.set_occupied(i + 2, j + 2, False)

'''
....      ....
....      ....
.●●●   -> ...●
....      ....
'''

def horizontal_simplify(G):
    g = G.graph
    for i in range(0, 3 + 4 * (G.n - 1) + 2 * G.padding - 3):
        for j in range(0, 2 + 4 * (G.n-1) + 2 * G.padding - 3):
            nodes = g.subgraph([(i + k, j + l) for k in range(4) for l in range(4)]).nodes
            occupied_nodes_block = set(node for node in nodes if nodes[node]['occupied'])
            #print(occupied_nodes_block)
            #print(set([(i + 1,j + 2),(i + 2,j + 2),(i + 3,j + 2)]) - occupied_nodes_block)
            if occupied_nodes_block != set([(i + 2,j + 1),(i + 2,j + 2),(i + 2,j + 3)]):
                continue
            G.set_effective_bit(i + 2, j + 3, g.nodes[(i + 2, j + 1)]['effective_bit'])
            G.set_effective_bit(i + 2, j + 1, -1)
            G.set_occupied(i + 2, j + 1, False)
            G.set_occupied(i + 2, j + 2, False)

def apply_simplifiers(G):
    # Note: The order of simplifications is important.
    g = G.graph
    vertical_simplify(g)
    turn1_simplify(g)
    turn2_simplify(g)
    horizontal_simplify(g)


# Not used yet.    
def apply_simplifier(G, block, block_simplified, i, j):
    # check if the block with (i,j) as upper left coordinates matches with block.
    


def apply_simplifier(G, block, block_simplified):
    n, padding = G.n, G.padding
    rows = 3 + 4 * (n - 1) + 2 * padding - 3
    cols = 2 + 4 * (n-1) + 2 * padding - 3
    for i in range(rows):
        for j in range(cols):
            apply_simplifier(G, block, block_simplified, i, j)

