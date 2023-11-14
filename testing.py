from GridGraph import GridGraph
from Simplifiers import *
import numpy as np

def chain_example(n):
    g = GridGraph(n, padding = 2)
    adj_mat = np.zeros((n,n))
    for i in range(n-1):
        adj_mat[i,i+1] = 1
        adj_mat[i+1,i] = 1
    g.optimize_row_order(adj_mat)
    g.populate_graph(adj_mat, list(g.row_order), list(g.col_order))
    print(g.row_order)
    g.draw()


def complete_example(n):
    g = GridGraph(n, padding = 2)
    adj_mat = np.ones((n,n))
    g.optimize_row_order(adj_mat)
    g.populate_graph(adj_mat, list(g.row_order), list(g.col_order))
    print(g.row_order)
    g.draw()

def custom_example():
    adj_mat = np.ones((4,4))
    adj_mat[0, 1] = 0
    adj_mat[1,0] = 0
    adj_mat[0, 2] = 0
    adj_mat[2,0] = 0
    adj_mat[2,3] = 0
    adj_mat[3,2] = 0
    g = GridGraph(4,2)
    # Comment the line below to see unoptimized rows representation
    g.optimize_row_order(adj_mat)
    print( g.row_order)
    g.populate_graph(adj_mat, list(g.row_order), list(g.col_order))
    vertical_simplify(g)
    turn1_simplify(g)
    turn2_simplify(g)
    horizontal_simplify(g)
    g.draw()

def optimisation2_example():
    adj_mat = np.ones((4,4))
    adj_mat[0, 1] = 1
    adj_mat[1,0] = 1
    adj_mat[0, 2] = 0
    adj_mat[2,0] = 0
    adj_mat[0,3] = 0
    adj_mat[3,0] = 0
    g = GridGraph(4,2)
    # Comment the line below to see unoptimized rows representation
    g.optimize_row_order(adj_mat)
    print( g.row_order)
    g.populate_graph(adj_mat, list(g.row_order), list(g.col_order))
    
    g.draw()

chain_example(6)