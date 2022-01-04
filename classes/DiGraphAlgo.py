import math
import sys
from collections import ChainMap
from queue import PriorityQueue
import json
import heapq
from typing import List

import numpy as np
from matplotlib import pyplot as plt


from interfaces.GraphAlgoInterface import GraphAlgoInterface
from interfaces.GraphInterface import GraphInterface
from classes.DiGraph import DiGraph


class DiGraphAlgo(GraphAlgoInterface):

    def __init__(self, DWG: DiGraph = None):

        self.djkhelper = {}

        if DWG is None:
            self.DWG = DiGraph()
        else:
            self.DWG = DWG

    def get_graph(self) -> GraphInterface:
        return self.DWG

    def load_from_json(self, file_name: str) -> bool:

        try:

            with open(file_name) as json_file:
                loaded_graph = DiGraph()
                data = json.load(json_file)

                for node in data['Nodes']:
                    if 'pos' in node.keys():
                        position = node['pos']
                        spl = position.split(",")
                        zval = float(spl.pop())
                        yval = float(spl.pop())
                        xval = float(spl.pop())
                        loc = (xval, yval, zval)
                        loaded_graph.add_node(int(node['id']), loc)

                    else:
                        # loc = Geolocation.nonegraph(self)
                        loaded_graph.add_node(int(node['id']))

                for edge in data['Edges']:
                    loaded_graph.add_edge(edge['src'], edge['dest'], edge['w'])
                self.DWG = loaded_graph
                return True

        except FileNotFoundError or FileExistsError or OSError:
            print("Cannot read the file")
            return False

        finally:
            json_file.close()


    def load_from_json2(self, json_content) -> bool:

        loaded_graph = DiGraph()
        data = json_content

        for node in data['Nodes']:

            if 'pos' in node.keys():
                position = node['pos']
                spl = position.split(",")
                zval = float(spl.pop())
                yval = float(spl.pop())
                xval = float(spl.pop())
                loc = (xval, yval, zval)
                loaded_graph.add_node(int(node['id']), loc)

            else:
                # loc = Geolocation.nonegraph(self)
                loaded_graph.add_node(int(node['id']))

        for edge in data['Edges']:
            loaded_graph.add_edge(edge['src'], edge['dest'], edge['w'])
        self.DWG = loaded_graph

        return True

    def save_to_json(self, file_name: str) -> bool:

        try:
            with open(file_name, 'w') as file:
                json.dump(self.DWG, default=lambda l: l.__dict__, fp=file, indent=2)
                return True

        except FileNotFoundError or FileExistsError or OSError:
            print("Cannot read the file")
            return False

        finally:
            file.close()

    def shortest_path(self, src, dest) -> (float, list):
        djk = self.dijkstra(src)[0]
        pathlen = self.shortest_path_dist(src, dest)
        path = []
        cur = dest
        if cur not in djk:
            return math.inf, []
        while cur != src:
            path.append(self.DWG.get_all_v()[cur])
            cur = djk[cur]
        path.append(self.DWG.get_all_v()[src])
        path.reverse()
        return pathlen, path

    def centerPoint(self) -> (int, float):

        if not self.connected():  # if the graph is not connected we asked to return a random Node and float = inf
            return self.get_graph().get_all_v()[0], math.inf

        max_lengths = dict.fromkeys(self.DWG.get_all_v().keys(), 0)

        for n in self.DWG.get_all_v().values():
            dist = self.dijkstra(n.get_key())[1]
            temp_max = max(dist.values())
            if temp_max > max_lengths[n.get_key()]:
                max_lengths[n.get_key()] = temp_max

        min = sys.float_info.max
        ret_key = 0

        for key in max_lengths.keys():
            if max_lengths[key] < min:
                min = max_lengths[key]
                ret_key = key
        return ret_key, min

    def connected(self):

        if self.DWG.v_size() == 0 or 1:
            return True

        for n in self.DWG.get_all_v():
            n.set_tag(-1)

        flag = True
        my_q = []
        finish = []

        if n in self.DWG.get_all_v().values():
            cur = n
        else:
            return False

        second = False
        k = 0

        while flag:
            while flag:
                flag = False
                if self.DWG.get_out(cur.get_key()) is None:
                    return False

                cur_edges = dict(ChainMap(cur.get_in(), cur.get_out()))

                if cur_edges:
                    return False

                for e in cur_edges:
                    if self.DWG.get_all_v()[e.get_destination].get_tag() != k:
                        self.DWG.get_all_v()[e.get_destination].set_tag(k)
                        my_q.append(self.DWG.get_all_v()[e.get_destination])
                    elif not second:
                        finish.append(cur)

                if not my_q:
                    cur = my_q.pop()
                    flag = True

            if not finish:
                cur = finish.pop()
                second = True
                flag = True

            for n in self.DWG.get_all_v().values():
                if n.get_tag() != k:
                    return False
            k += 1

        return True

    def plot_graph(self):

        self.draw_nodes()
        self.draw_edges()
        plt.show()

    def draw_nodes(self):
        locx = []
        locy = []
        for n in self.get_graph().get_all_v().values():
            locx.append(n.location[0])
            locy.append(n.location[1])
        plt.plot(locx, locy, 'ro')
        for r in range(len(locx)):
            plt.annotate(r, xy=(locx[r]*0.999989, locy[r]*1.000008))
            # plt.text(loc.x, loc.y, str(n.get_key()))

    def draw_edges(self):
        # ArrowStyle.Fancy(head_length=.4, head_width=.4, tail_width=.4)
        for n in self.get_graph().get_all_v().keys():
            for e in self.get_graph().all_out_edges_of_node(n).keys():
                locx1 = self.get_graph().get_all_v().get(n).location[0]  # x src
                locx2 = self.get_graph().get_all_v().get(e).location[0]  # x dest
                locy1 = self.get_graph().get_all_v().get(n).location[1]  # y src
                locy2 = self.get_graph().get_all_v().get(e).location[1]  # y dest
                plt.annotate("", xy=(locx1, locy1), xytext=(locx2, locy2), arrowprops={'arrowstyle': "<-", 'lw': 2})  # took from the internet

    def TSP(self, node_list: List[int]) -> (List[int], float):

        if len(node_list) == 0 or node_list is None:
            return None

        tsp_path = []
        curr_list = node_list
        listlen = 0

        temp = node_list[0]
        tsp_path.append(curr_list[0])

        while len(curr_list) > 1:
            short_list = []
            curr_list.remove(temp)
            shortest_path = math.inf
            for i in range(len(curr_list)):
                key = curr_list[i]
                path = self.shortest_path_dist(temp, key)
                if path < shortest_path:
                    short_list = self.shortest_path(temp, key)[1]  # the path
                    node_id = key
                    shortest_path = path
            if len(tsp_path) > 0:
                short_list.pop(0)  # removing the src node because it will show twice in the list if the list bigger than 1
                tsp_path.extend(short_list)
            else:
                tsp_path.extend(short_list)

            listlen = listlen + shortest_path
            temp = node_id

        return tsp_path, listlen

    def shortest_path_dist(self, src, dest):

        dist = self.dijkstra(src)[1].get(dest)
        return dist

    def connected(self):

        DGA_trans = DiGraphAlgo(self.getTranspose())
        DGA_BFS = self.BFS(list(self.DWG.get_all_v().values())[0].get_key())
        DGA_trans_BFS = DGA_trans.BFS(list(self.DWG.get_all_v().values())[0].get_key())
        return DGA_BFS == DGA_trans_BFS == self.DWG.v_size()

    def getTranspose(self):
        g = DiGraph()

        for n in self.DWG.get_all_v().values():
            g.add_node(n.get_key(), n.location)

        for n in self.DWG.get_all_v().values():
            for e in n.get_out().values():
                g.add_edge(e.get_destination(), e.get_source(), e.get_weight())

        return g

    def BFS(self, src):

        for n in self.DWG.get_all_v().values():
            n.set_info("white")

        q = []

        self.DWG.get_all_v()[src].set_info("gray")
        q.append(self.DWG.get_all_v()[src])

        counter = 1

        while q:
            cur = self.DWG.get_all_v()[q.pop().get_key()]
            if cur.get_info() == "gray":
                cur.set_info("black")
                for e in cur.get_out().values():
                    if self.DWG.get_all_v()[e.get_destination()].get_info() == "white":
                        q.append(self.DWG.get_all_v()[e.get_destination()])
                        self.DWG.get_all_v()[e.get_destination()].set_info("gray")
                        counter += 1
        return counter

    # Input(graph,int),Output(hashmap:int-double)
    # Uses priority queue to oreder nodes by their wights
    def dijkstra(self, start_node):
        unvisited_nodes = list(self.DWG.get_all_v().keys())

        shortest_path = {}

        previous_nodes = {}

        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        shortest_path[start_node] = 0

        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes:
                if current_min_node is None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            neighbors = self.DWG.get_all_v()[current_min_node].get_out()
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + self.DWG.get_all_v()[current_min_node].get_out()[
                    neighbor].get_weight()
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    previous_nodes[neighbor] = current_min_node

            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path

    def __str__(self):
        return self.DWG.get_all_v().keys()
