import unittest
from unittest import TestCase
from classes.DiGraph import DiGraph
from classes.Node import Node



def create_graph() -> DiGraph:
    DWG = DiGraph()

    for i in range(9):
        DWG.add_node(i)

    DWG.add_edge(0, 1, 1)  # 1
    DWG.add_edge(0, 2, 3)  # 2
    DWG.add_edge(3, 0, 5)  # 3
    DWG.add_edge(3, 1, 2)  # 4
    DWG.add_edge(1, 3, 6)  # 5
    DWG.add_edge(3, 4, 1)  # 6
    DWG.add_edge(1, 4, 2)  # 7
    DWG.add_edge(5, 1, 4)  # 8
    DWG.add_edge(4, 5, 4)  # 9
    DWG.add_edge(4, 2, 9)  # 10
    DWG.add_edge(2, 5, 3)  # 11
    return DWG


class TestDiGraph(unittest.TestCase):

    def test_v_size(self):
        graph = create_graph()

        self.assertEqual(9, graph.v_size())
        # add new node 9
        graph.add_node(9)
        self.assertEqual(10, graph.v_size())
        # add a node already in the graph
        graph.add_node(4)
        self.assertEqual(10, graph.v_size())

    def test_e_size(self):
        graph = create_graph()

        self.assertEqual(11, graph.e_size())

        # checking that adding an edge updates the total size of the edge dict
        graph.add_edge(2, 1, 3)
        self.assertEqual(12, graph.e_size())

        # checking that the number of edges is updated both in the node's data and the graph's data
        self.assertEqual(graph.all_in_edges_of_node(1), graph.nodes.get(1).get_in())
        self.assertEqual(graph.all_out_edges_of_node(1), graph.nodes.get(1).get_out())

    def test_get_all_v(self):
        graph = create_graph()

        self.assertEqual(graph.get_all_v().__len__(), 9)
        test_index = 0
        for i in graph.get_all_v().keys():
            self.assertEqual(graph.get_all_v().get(i).get_key(), test_index)
            test_index += 1

    def test_get_mc(self):
        graph = create_graph()

        curr_mc = graph.mc
        graph.add_node(10)
        new_mc = graph.mc
        self.assertEqual(curr_mc + 1, new_mc)

        graph.add_node(15)
        graph.add_node(16)
        graph.remove_node(5)
        new_mc2 = graph.mc
        self.assertEqual(curr_mc + 7, new_mc2)

        graph.add_node(11)
        graph.add_edge(10, 11, 20)
        graph.add_edge(11, 10, 1)
        new_mc3 = graph.mc
        self.assertEqual(curr_mc + 10, new_mc3)

    def test_all_in_edges_of_node(self):
        graph = create_graph()
        for key in graph.get_all_v().keys():
            expected = graph.get_all_v().get(key).get_in()
            actual = graph.all_in_edges_of_node(key)
            self.assertEqual(expected, actual)

    def test_add_node(self):
        graph = create_graph()
        size = graph.v_size()
        graph.add_node(13)
        graph.add_node(14)
        newsize = graph.v_size()
        self.assertEqual(newsize, size + 2)

        graph.add_node(15)
        graph.add_node(15)
        graph.add_node(16)
        newsize2 = graph.v_size()
        self.assertEqual(newsize2, size + 4)

    def test_remove_node(self):
        graph = create_graph()
        edge_size = graph.e_size()
        size = graph.v_size()

        self.assertTrue(graph.remove_node(4))
        self.assertTrue(graph.remove_node(5))
        newsize = graph.v_size()
        new_edgesize = graph.e_size()

        self.assertEqual(newsize, size - 2)
        self.assertEqual(new_edgesize, edge_size - 6)
        self.assertTrue(11, edge_size)
        self.assertTrue(5, new_edgesize)

    def test_add_edge(self):
        graph = create_graph()
        size = graph.e_size()
        graph.add_edge(1, 3, 6)
        graph.add_edge(0, 5, 6)
        newsize = graph.e_size()
        self.assertEqual(newsize, size + 1)

        graph.add_edge(1, 3, 6)
        graph.add_edge(0, 5, 6)
        graph.add_edge(2, 1, 6)
        newsize2 = graph.e_size()
        self.assertEqual(newsize2, size + 2)

    def test_remove_edge(self):
        graph = create_graph()

        size = graph.e_size()
        graph.remove_edge(0, 1)
        graph.remove_edge(3, 1)
        graph.remove_edge(2, 5)
        new_size = graph.e_size()
        self.assertEqual(new_size, size - 3)

        graph.add_edge(0, 1, 1)
        graph.add_edge(3, 1, 2)
        graph.add_edge(2, 5, 3)
        graph.remove_edge(0, 1)
        graph.remove_edge(3, 1)
        graph.remove_edge(2, 5)
        new_size2 = graph.e_size()
        self.assertTrue(new_size2, size)