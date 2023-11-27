import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import flatten, nodes_or_number, pairwise
import numpy as np
import Block
from PathDecomposition import pathwidth, Branching, Greedy
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
        nx.draw_networkx_nodes(G, pos, nodelist= occupied_nodes, node_size= 10)
        nx.draw_networkx_labels(G, pos, labels = labels)
        plt.title('Number of nodes: ' + str(len(occupied_nodes)))
        plt.figure(figsize=(20,100))
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
            self.set_occupied(padding, padding + 4 * i)
            self.set_effective_bit(padding, padding + 4 * i, effective_bit = col_order[i])

        # put the last column of lone bits
        for j in range(self.n - 1):
            self.set_occupied(padding + 2 + 4 * j, padding + 2 + 4 * (self.n - 1)) 

        # We construct the graph block by block
        # block 1 : (padding + 1, padding)
        for i in range(self.n - 1):
            for j in range(self.n):
                # We consider the block (i,j) with the block (0,0) being the upper left block
                col = col_order[j]
                row = row_order[i]
                if row == col:
                    Block.turn(self, padding + 1 + 4 * i, padding + 4 * j - 2)
                
                
                elif row_order.index(col) > i and j < col_order.index(row):
                    Block.vertical_lign(self, padding + 1 + 4 * i, padding + 4 * j - 2)
                elif j > col_order.index(row) and i > row_order.index(col):
                    Block.horizontal_lign(self, padding + 1 + 4 * i, padding + 4 * j - 2)
                elif j > i :
                    if adj_mat[row,col] == 1:
                        Block.crossing_with_edge(self, padding + 1 + 4 * i, padding + 4 * j - 2)
                    else:
                        Block.crossing_without_edge(self, padding + 1 + 4 * i, padding + 4 * j - 2)
        
    def optimize_row_order(self, adj_mat):
        col_order_map = {self.col_order[i]: i for i in range(self.n)}
        row_order_map = {self.row_order[i]: i for i in range(self.n)}
        for i in range(self.n):
            j = row_order_map[self.col_order[i]] + 1
            while j < self.n and adj_mat[self.col_order[i],self.row_order[j]] == 0 and col_order_map[self.row_order[j]] > i :
                row_order_map[self.row_order[j-1]], row_order_map[self.row_order[j]] = j, j - 1
                self.row_order[j-1], self.row_order[j] = self.row_order[j], self.row_order[j - 1]
                 
                j += 1

    '''
    Deletes the last crossings with no edge in a lign with vertical ligns when there are no more crossings with edge.
    ..●..      ..●.
    ●●●.●      ●.●.
    .●●●.   -> ..●.
    .●...      ..●.

    Use after populating and optimizing the row order.
    '''

    def optimize_crossings_no_edge(self, adj_mat):
        # TODO : Careful when modifying weights later for the lone node.             
        for i in range(self.n - 1):
            j = self.n - 1
            while j > i and adj_mat[self.row_order[i], self.col_order[j]] == 0 and self.row_order[i] != self.col_order[j]:
                row = self.padding + 1 + 4 * i
                col = self.padding + 4 * j - 2
                self.set_occupied(row + 1, col + 1, False)
                self.set_occupied(row + 2, col + 1, False)
                self.set_occupied(row + 2, col + 3, False)
                self.set_occupied(row + 3, col + 1, False)
                self.set_occupied(row + 3, col + 2, True)
                self.set_occupied(row + 1, col + 4, False)
                j -= 1

    """
    Set the rows and columns with path decomposition with pathwidth from PathDecomposition class.
    Takes as argument:
    adj_mat : Adjacency Matrix
    method : Exact using branch and Bound : "Branching()" or greedy : "Greedy(n_repeat = 10)" with best result among n_repeat iterations of greedy.
    """
    def set_cols_rows_with_path_decomposition(self, adj_mat, method = Branching()):
        g = nx.from_numpy_array(adj_mat)
        nodes_order = np.array(pathwidth(g, method).vertices)
        self.col_order = nodes_order.copy()
        self.row_order = nodes_order.copy()


# !!! Note that the crossing lattice representation requires that the last element of row order is same as column since it ll be just a vertical lign (This doesn't clash with the row optimization algorithm)
        
