from interfaces.GraphInterface import GraphInterface
from classes.Edge import Edge
from classes.Node import Node


class DiGraph(GraphInterface):

    # Initialize a new Directed Graph
    def __init__(self):

        self.number_of_edges = 0
        self.number_of_nodes = 0
        self.nodes = {}
        self.edges = {}
        self.mc = 0

    # Return the amount of nodes of the graph
    def v_size(self) -> int:
        return self.number_of_nodes

    # Return the amount of edges of the graph
    def e_size(self) -> int:
        return self.number_of_edges

    # Return the mode counter (amount of changes) of the graph
    def get_mc(self) -> int:
        return self.mc

    # Return a dictionary of all the nodes in the graph
    def get_all_v(self) -> dict:
        return self.nodes

    # Return a dictionary of all the nodes connected to this node in the graph
    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes.get(id1).get_in()

    # Return a dictionary of all the nodes connected from this node in the graph
    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes.get(id1).get_out()

    # Add an edge to the graph
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:

        if id1 not in self.nodes or id2 not in self.nodes:
            return False
        elif id1 == id2 or weight < 0:
            return False
        if id1 not in self.edges:
            self.edges[id1] = {}
        print()
        if id2 not in self.nodes.get(id1).get_out():
            self.number_of_edges += 1
        self.edges[id1][id2] = Edge(id1, id2, weight)
        self.nodes.get(id1).add_out(id2, weight)
        self.nodes.get(id2).add_in(id1, weight)
        self.mc += 1
        return True

    # Add a node to the graph
    def add_node(self, node_id: int, pos: tuple = None) -> bool:

        if node_id in self.nodes:
            return False

        self.nodes[node_id] = Node(node_id, location=pos)
        self.number_of_nodes += 1
        self.mc += 1
        return True

    # Remove the node_id from the graph
    def remove_node(self, node_id: int) -> bool:

        if node_id not in self.nodes:
            return False

        for data_in in list(self.all_in_edges_of_node(node_id).keys()):
            self.remove_edge(data_in, node_id)

        for data_out in list(self.all_out_edges_of_node(node_id).keys()):
            self.remove_edge(node_id, data_out)

        if not self.nodes.pop(node_id, False):
            return False
        self.number_of_nodes -= 1
        self.mc += 1
        return True

    # Remove the edge (source: id1, dest: id2) from the graph
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if not self.edges[node_id1].pop(node_id2, False):
            return False
        if len(self.edges[node_id1]) == 0:
            self.edges.pop(node_id1)
        self.nodes.get(node_id1).remove_out(node_id2)
        self.nodes.get(node_id2).remove_in(node_id1)
        self.number_of_edges -= 1
        self.mc += 1
        return True

    def __str__(self) -> str:

        return "DiGraph: |V|=" + str(self.v_size()) + " , |E|=" + str(self.e_size())




