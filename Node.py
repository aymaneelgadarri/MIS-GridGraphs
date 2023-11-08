class Node:
    def __init__(self, i, j, occupied = False, weight = 1):
        self.i = i
        self.j = j
        self.occupied = occupied
        self.weight = weight
        self.label = -1 # The effective bit that the node represents
    
    def __hash__(self):
        return hash((self.i, self.j))
    