import unittest
from classes.DiGraph import DiGraph
from classes.DiGraphAlgo import DiGraphAlgo


def create_graph() -> DiGraphAlgo:
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

    GraphAlgo = DiGraphAlgo(DWG)

    return GraphAlgo


class TestGraphAlgo(unittest.TestCase):

    def test_get_graph(self):
        graph_Algo = create_graph()
        graph = graph_Algo.get_graph()
        self.assertTrue(graph_Algo.get_graph, graph)

    def test_loadsaved_from_json(self):

        ##################### A0 ######################

        AlgoA0 = create_graph()
        A0 = AlgoA0.get_graph()
        AlgoA0.__init__(A0)
        loadedA0 = AlgoA0.load_from_json("../data/A0")
        savedA0 = AlgoA0.save_to_json("A0Nodes.json")
        new_AlgoA0 = AlgoA0.get_graph()

        self.assertTrue(loadedA0)
        self.assertTrue(savedA0)
        self.assertEqual(AlgoA0.get_graph(), new_AlgoA0)

        # # ##################### A1 ######################

        AlgoA1 = create_graph()
        A1 = AlgoA1.get_graph()
        AlgoA1.__init__(A1)
        loadedA1 = AlgoA1.load_from_json("../data/A1")
        savedA1 = AlgoA1.save_to_json("A1Nodes.json")
        new_AlgoA1 = AlgoA1.get_graph()

        self.assertTrue(loadedA1)
        self.assertTrue(savedA1)
        self.assertEqual(AlgoA1.get_graph(), new_AlgoA1)

        # # ##################### A2 ######################

        AlgoA2 = create_graph()
        A2 = AlgoA2.get_graph()
        AlgoA2.__init__(A2)
        loadedA2 = AlgoA2.load_from_json("../data/A2")
        savedA2 = AlgoA2.save_to_json("A2Nodes.json")
        new_AlgoA2 = AlgoA2.get_graph()

        self.assertTrue(loadedA2)
        self.assertTrue(savedA2)
        self.assertEqual(AlgoA2.get_graph(), new_AlgoA2)

        # # ##################### A3 ######################

        AlgoA3 = create_graph()
        A3 = AlgoA3.get_graph()
        AlgoA3.__init__(A3)
        loadedA3 = AlgoA3.load_from_json("../data/A3")
        savedA3 = AlgoA3.save_to_json("A3Nodes.json")
        new_AlgoA3 = AlgoA3.get_graph()

        self.assertTrue(loadedA3)
        self.assertTrue(savedA3)
        self.assertEqual(AlgoA3.get_graph(), new_AlgoA3)

    def test_shortest_path(self):

        ##################### A0 ######################

        AlgoA0 = DiGraphAlgo()
        AlgoA0.load_from_json("../data/A0")
        distA0 = str(AlgoA0.shortest_path(0, 2))
        compA0 = "(3.165136835245062, [0, 1, 2])"
        self.assertEqual(distA0, compA0)

        # ##################### A1 ######################

        AlgoA1 = DiGraphAlgo()
        AlgoA1.load_from_json("../data/A1")
        distA1 = str(AlgoA1.shortest_path(0, 2))
        compA1 = "(3.0336329076522373, [0, 1, 2])"
        self.assertEqual(distA1, compA1)

        # # # # ##################### A2 ######################

        AlgoA2 = DiGraphAlgo()
        AlgoA2.load_from_json("../data/A2")
        distA2 = str(AlgoA2.shortest_path(0, 2))
        compA2 = "(3.0336329076522373, [0, 1, 2])"
        self.assertEqual(distA2, compA2)
        #
        # # # # ##################### A3 ######################

        AlgoA3 = DiGraphAlgo()
        AlgoA3.load_from_json("../data/A3")
        distA3 = str(AlgoA3.shortest_path(0, 2))
        compA3 = "(2.095850038785596, [0, 1, 2])"
        self.assertEqual(distA3, compA3)

    def test_center_point(self):

        ##################### A0 ######################
        AlgoA0 = DiGraphAlgo()
        AlgoA0.load_from_json("../data/A0")
        distA0 = AlgoA0.centerPoint()
        resA0 = (7, 6.806805834715163)
        self.assertEqual(distA0, resA0)

        ##################### A1 ######################

        AlgoA1 = DiGraphAlgo()
        AlgoA1.load_from_json("../data/A1")
        distA1 = AlgoA1.centerPoint()
        resA1 = (8, 9.925289024973141)
        self.assertEqual(distA1, resA1)

        # # ##################### A2 ######################

        AlgoA2 = DiGraphAlgo()
        AlgoA2.load_from_json("../data/A2")
        distA2 = AlgoA2.centerPoint()
        resA2 = (0, 7.819910602212574)
        self.assertEqual(distA2, resA2)

        # ##################### A3 ######################

        AlgoA3 = DiGraphAlgo()
        AlgoA3.load_from_json("../data/A3")
        distA3 = AlgoA3.centerPoint()
        resA3 = (6, 8.071366078651435)
        self.assertEqual(distA3, resA3)


    def test_connected(self):
        Algo = DiGraphAlgo()
        Algo.load_from_json("../data/A0")
        self.assertTrue(Algo.connected())
        Algo.get_graph().remove_node(7)
        Algo.get_graph().remove_node(10)
        self.assertFalse(Algo.connected())

    def test_BFS(self):
        Algo = DiGraphAlgo()
        Algo.load_from_json("../data/A0")
        Algo.BFS(0)
        Algo.get_graph().remove_node(7)
        Algo.get_graph().remove_node(10)
        Algo.BFS(0)



    def test_TSP(self):

        # ##################### A0 ######################

        Algo = DiGraphAlgo()
        Algo.load_from_json("../data/A0")
        dist = str(Algo.TSP([0, 2]))
        comp = "([0, 1, 2], 3.165136835245062)"
        self.assertEqual(dist, comp)

        ##################### A1 ######################

        AlgoA1 = DiGraphAlgo()
        AlgoA1.load_from_json("../data/A1")
        distA1 = str(AlgoA1.TSP([0, 2]))
        resA1 = "([0, 1, 2], 3.0336329076522373)"
        self.assertEqual(distA1, resA1)

        # # ##################### A2 ######################

        AlgoA2 = DiGraphAlgo()
        AlgoA2.load_from_json("../data/A2")
        distA2 = str(AlgoA2.TSP([0, 2]))
        resA2 = "([0, 1, 2], 3.0336329076522373)"
        self.assertEqual(distA2, resA2)

        # # # ##################### A3 ######################

        AlgoA3 = DiGraphAlgo()
        AlgoA3.load_from_json("../data/A3")
        distA3 = str(AlgoA3.TSP([0, 2]))
        resA3 = "([0, 1, 2], 2.095850038785596)"
        self.assertEqual(distA3, resA3)


