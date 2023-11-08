import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import flatten, nodes_or_number, pairwise

delta = 1
class grid_graph:
    def __init__(self, n, padding = 2):
        self.graph = create_empty_grid_graph(n , padding)
        self.n = n
    
def create_empty_grid_graph(n , padding = 2):
    G =nx.empty_graph()
    rows = 3 + 4 * (n - 1) + 2 * padding
    cols = 2 + 4 * (n-1) + 2 * padding
    G.add_nodes_from(( (-i, j) for i in range(rows) for j in range(cols) ), occupied = False, weight = 0, effective_bit = -1)
    G.add_edges_from(((-i, j), (-pi, j)) for pi, i in pairwise(range(rows)) for j in range(cols))
    G.add_edges_from(((-i, j), (-i, pj)) for i in range(rows) for pj, j in pairwise(range(cols)))
    G.add_edges_from(((-i, j), (-i - 1, pj)) for i in range(rows-1) for pj, j in pairwise(range(cols)))
    G.add_edges_from(((-i, j), (-i + 1, pj)) for i in range(1, rows) for pj, j in pairwise(range(cols)))
    return G


def populate_graph(G, n,  adj_mat, row_order, col_order, padding = 2):
        for j in range(padding, padding + 4 * (n - 1) + 1, 4):
            G.add_node((- padding, j), occupied = True, weight = delta, effective_bit = j)
        #for i in row_order for j in col_order:


def add_cell_crossing_without_edge(G : grid_graph, i, j): # i and j are the indices of the upper left corner of the cell
    for k,l in [(i-1,j),(i-2,j+1),(i,j+2),(i-1,j+2),(i-2,j+2),(i-3,j+2),(i-2,j+3)]:
        G.nodes[(k,l)]['occupied'] = True
        G.nodes[(k,l)]['weight'] = 1



# Create an empty grid graph
G = create_empty_grid_graph(2) 

# Assign the 'occupied' attribute to the nodes
for node in G.nodes:
    G.nodes[node]['occupied'] = False  # You can set this to True for specific nodes

populate_graph(G,2,  [], range(2), range(2))
# Create a list of nodes with 'occupied == True' for visualization
G.nodes[(-1,0)]['occupied'] = True

add_cell_crossing_without_edge(G,0,0)
occupied_nodes = [node for node in G.nodes if G.nodes[node]['occupied']]

# Create a graph layout for drawing
pos = {(x, y): (8-x, -y) for x, y in G.nodes}

G.nodes[(0,0)]['weight'] = 1
print(G.nodes[(0,0)]['weight'])
# Create a figure and draw the occupied nodes
plt.figure(figsize=(8, 16))
nx.draw(G, pos, nodelist=occupied_nodes, node_color='r', node_size=300)
mis = nx.algorithms.approximation.maximum_independent_set(G.subgraph(occupied_nodes))
# Draw only the edges of occupied nodes
edges_to_draw = [(u, v) for u, v in G.edges() if u in occupied_nodes and v in occupied_nodes]
nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='b', width=2)
nx.draw_networkx_nodes(G,pos, occupied_nodes) 
nx.draw_networkx_nodes(G, pos, mis, node_color= 'r')
plt.show()