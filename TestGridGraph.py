import unittest
import networkx as nx
import numpy as np
from GridGraph import GridGraph

class TestGridGraph(unittest.TestCase):
    def setUp(self):
        self.n = 3  # Change this to the desired grid size
        self.grid = GridGraph(self.n)

    def test_create_empty_grid_graph(self):
        self.assertIsInstance(self.grid.graph, nx.Graph)
        self.assertEqual(len(self.grid.graph.nodes), (3 + 4 * (self.n - 1) + 2 * self.grid.padding) * (2 + 4 * (self.n - 1) + 2 * self.grid.padding))

    def test_set_occupied(self):
        self.grid.set_occupied(1, 1, occupied=True)
        self.assertTrue(self.grid.graph.nodes[(1, 1)]["occupied"])
        self.grid.set_occupied(2, 2, occupied=False)
        self.assertFalse(self.grid.graph.nodes[(2, 2)]["occupied"])

    def test_set_weight(self):
        self.grid.set_weight(1, 1, weight=5)
        self.assertEqual(self.grid.graph.nodes[(1, 1)]["weight"], 5)
        self.grid.set_weight(2, 2, weight=10)
        self.assertEqual(self.grid.graph.nodes[(2, 2)]["weight"], 10)

    def test_set_effective_bit(self):
        self.grid.set_effective_bit(1, 1, effective_bit=1)
        self.assertEqual(self.grid.graph.nodes[(1, 1)]["effective_bit"], 1)
        self.grid.set_effective_bit(2, 2, effective_bit=0)
        self.assertEqual(self.grid.graph.nodes[(2, 2)]["effective_bit"], 0)

    def test_optimize_row_order(self):
        adj_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])  # Example adjacency matrix
        initial_order = self.grid.row_order.copy()
        self.grid.optimize_row_order(adj_matrix)
        self.assertNotEqual(initial_order, self.grid.row_order)

    def test_populate_graph(self):
        adj_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])  # Example adjacency matrix
        self.grid.populate_graph(adj_matrix, list(self.grid.row_order), list(self.grid.col_order))
        # Add assertions to check the graph is populated correctly based on the adjacency matrix

if __name__ == '__main__':
    unittest.main()
