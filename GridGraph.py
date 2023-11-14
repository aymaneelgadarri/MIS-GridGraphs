import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import flatten, nodes_or_number, pairwise
import numpy as np
import Block

class GridGraph:   
    def __init__(self, n, padding = 2):
        self.padding = padding
        self.n = n
        self.graph = self.create_empty_grid_graph(n, padding)
        self.row_order = np.arange(n)
        self.col_order = np.arange(n)


    def create_empty_grid_graph(self, n, padding = 2):
        G = nx.empty_graph()
        rows = 3 + 4 * (n - 1) + 2 * padding
        cols = 2 + 4 * (n-1) + 2 * padding
        G.add_nodes_from(( (i, j) for i in range(rows) for j in range(cols) ), occupied = False, weight = 1, effective_bit = -1)
        G.add_edges_from(((i, j), (pi, j)) for pi, i in pairwise(range(rows)) for j in range(cols))
        G.add_edges_from(((i, j), (i, pj)) for i in range(rows) for pj, j in pairwise(range(cols)))
        G.add_edges_from(((i, j), (i - 1, pj)) for i in range(1, rows) for pj, j in pairwise(range(cols)))
        G.add_edges_from(((i, j), (i + 1, pj)) for i in range(rows - 1) for pj, j in pairwise(range(cols)))
        return G
        
    def draw(self):
        G = self.graph
        pos = {(x, y): (y, - x) for x, y in G}
        occupied_nodes = [node for node in G.nodes if G.nodes[node]['occupied']]
        # Draw only the edges of occupied nodes
        edges_to_draw = [(u, v) for u, v in G.edges() if u in occupied_nodes and v in occupied_nodes]
        labels = nx.get_node_attributes(G, 'effective_bit')
        labels = {node: label for node, label in labels.items() if label != -1}
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='r', width=2)
        nx.draw_networkx_nodes(G, pos, occupied_nodes)
        nx.draw_networkx_labels(G, pos, labels = labels)
        plt.show()

    def set_occupied(self, i, j, occupied = True):
        self.graph.nodes[(i,j)]["occupied"] = occupied
    
    def set_weight(self, i, j , weight):
        self.graph.nodes[(i,j)]["weight"] = weight
    
    def set_effective_bit(self, i, j , effective_bit):
        self.graph.nodes[(i,j)]["effective_bit"] = effective_bit

  
    def populate_graph(self, adj_mat, row_order, col_order):
        padding = self.padding
        # We put the row bits in the first line after the padding
        for i in range(self.n):
            self.set_occupied(padding, padding + 2 + 4 * i)
            self.set_effective_bit(padding, padding + 2 + 4 * i, effective_bit = col_order[i])

        # We construct the graph block by block
        # block 1 : (padding + 1, padding)
        for i in range(self.n - 1):
            for j in range(self.n):
                # We consider the block (i,j) with the block (0,0) being the upper left block
                col = col_order[j]
                row = row_order[i]
                if row == col:
                    Block.turn(self, padding + 1 + 4 * i, padding + 4 * j)
                
                
                elif row_order.index(col) > i and j < col_order.index(row):
                    Block.vertical_lign(self, padding + 1 + 4 * i, padding + 4 * j)
                elif j > col_order.index(row) and i > row_order.index(col):
                    Block.horizontal_lign(self, padding + 1 + 4 * i, padding + 4 * j)
                elif j > i :
                    if adj_mat[row,col] == 1:
                        Block.crossing_with_edge(self, padding + 1 + 4 * i, padding + 4 * j)
                    else:
                        Block.crossing_without_edge(self, padding + 1 + 4 * i, padding + 4 * j)
        
    def optimize_row_order(self, adj_mat):
        for i in range(self.n):
            j = i + 1
            while j < self.n - 1 and adj_mat[self.col_order[i],self.row_order[j]] == 0 and np.where(self.col_order == self.row_order[j])[0] > i:
                self.row_order[j-1], self.row_order[j] = self.row_order[j], self.row_order[j - 1]
                j += 1
            
                
                    
# !!! Note that the crossing lattice representation requires that the last element of row order is same as column since it ll be just a vertical lign (This doesn't clash with the row optimization algorithm)
        
