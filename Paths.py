################

""" Dijkstra's algorithm for finding the shortest path in a weighted graph. """

#An implementation of a weighted graph. 

class Vertex: 
    def __init__(self):
        self.edges = []
        self.since_last_sorted = 0
    
    def add_edge(self, edge):
        if edge.fr == self:
            self.edges.append(edge)
        else: 
            print("This edge does not originate from here!")

class Edge:
    def __init__(self, fr, to, weight):
        self.fr = fr
        self.to = to
        self.weight = weight
    
class Graph:
    def __init__(self):
        self.vertexes = []
        self.edges = []