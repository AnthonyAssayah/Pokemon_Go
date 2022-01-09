"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import multiprocessing
import queue
from collections import defaultdict
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from classes.DiGraphAlgo import DiGraphAlgo
from classes.DiGraph import DiGraph
from classes.Node import Node
from classes.Edge import Edge
import sys
from math import sqrt
from math import pow

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption('Pokemon go!')
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

# set background image
background = pygame.image.load('imeges\wallpeper.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
screen.blit(pygame.transform.scale(background, (WIDTH, HEIGHT)), (0, 0))

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
# --------------------------------------------
DWGA = DiGraphAlgo()
DWGA.load_from_json2(json.loads(graph_json))
# --------------------------------------------
for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15
game_info = json.loads(client.get_info())
center = DWGA.centerPoint()[0]
number_of_agents = game_info['GameServer']['agents']
#center - (number_of_agents / 2) + i
for i in range(number_of_agents):
   client.add_agent("{\"id\":" + str(i) + "}")

# this commnad starts the server - the game is running now
client.start()
"""
drawing the stop button.
"""
text = "stop"
font = pygame.font.Font(None, 34)
txt = font.render(text, True, 'BLACK', 'PINK')
input_rect = pygame.Rect(150, 10, 130, 32)
input_rect.topleft
color = 'PINK'
screen.blit(txt, (190, 15))
pygame.draw.rect(screen, color, input_rect, 2)
pause = False
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


def assign_edges(pokemons, taken_agents) -> []:  # list of (int, int) tuples

    ret = []
    for p in pokemons:

        src, dest = get_edge(p)
        already_in = False
        for x, y in taken_agents.values():
            if src == x and dest == y:
                already_in = True

        if already_in:
            continue
        # if src in list(zip(*list(taken_agents.values())))[0] and dest in list(zip(*list(taken_agents.values())))[1]:
        #     continue

        if (src, dest) in taken_agents.values():
            continue

        if src is None and dest is None:
            return None

        ret.append((src, dest))

    return ret


def get_edge(pokemon) -> (int, int):

    x = pokemon.pos.x
    y = pokemon.pos.y

    for n in DWGA.get_graph().get_all_v().values():

        for e in n.get_out().keys():

            src_pos_x = my_scale(n.location[0], x=True)
            src_pos_y = my_scale(n.location[1], y=True)
            dest_pos_x = my_scale(DWGA.get_graph().get_all_v()[e].location[0], x=True)
            dest_pos_y = my_scale(DWGA.get_graph().get_all_v()[e].location[1], y=True)

            src_to_dest = sqrt(pow(src_pos_x - dest_pos_x, 2) + pow(src_pos_y - dest_pos_y, 2))
            src_to_poke = sqrt(pow(src_pos_x - x, 2) + pow(src_pos_y - y, 2))
            poke_to_dest = sqrt(pow(x - dest_pos_x, 2) + pow(y - dest_pos_y, 2))
            eps = 0.000001
            if src_to_dest + eps >= src_to_poke + poke_to_dest:

                if n.get_key() < e:

                    return (n.get_key(), e) if (pokemon.type < 0) else (e, n.get_key())
                else:

                    return (e, n.get_key()) if (pokemon.type > 0) else (n.get_key(), e)
    return None, None


def get_agent(id):
    for agent in agents:
        if id == agent.id:
            return agent
    return None

def matchagent(call, taken_agents) -> int:     # gets call in the form of a tuple (src_id, dest_id) representing the edge on which the pokemon is located. returns assigned agent id

    bestagent = None  # if stays none , no avalible agent
    min = sys.float_info.max
    for agent in agents:
        if agent.id in taken_agents.keys():
            continue

        if agent.dest == -1 and len(queues[agent.id]) == 0:
            tmp = dijkstra_distances[agent.id][call[0]]
            if tmp < min:
                min = tmp
                bestagent = agent.id
    return bestagent

dijkstra_paths = {}
dijkstra_distances = {}
for n in DWGA.get_graph().get_all_v().values():
    dijkstra_paths[n.get_key()], dijkstra_distances[n.get_key()] = DWGA.dijkstra(n.get_key())

agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents

agents = [agent.Agent for agent in agents]
queues = {}
for agent in agents:
    queues[agent.id] = []


def shortest_path(src, dest):
    djk = dijkstra_paths[src]
    path = []
    cur = dest
    if cur not in djk:
        return []
    while cur != src:
        path.append(cur)
        cur = djk[cur]
    path.append(src)
    path.reverse()
    return path

taken_agents = {}
assigned_edges = []

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 200 <= mouse[0] <= 200 + 150 and 15 <= mouse[1] <= 30:
                client.stop()

            # refresh surface
    screen.blit(pygame.transform.scale(background, (WIDTH, HEIGHT)), (0, 0))
    screen.blit(txt, (191, 15))
    pygame.draw.rect(screen, color, input_rect, 2)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, pygame.Color(0, 0, 0),
                         (src_x, src_y), (dest_x, dest_y), 2)

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)
        # pokeball nodes
        poke = pygame.image.load('imeges/pokeball.png')
        rect2 = poke.get_rect(center=(x, y))
        screen.blit(poke, rect2)

        # draw the node id
        id_srf = FONT.render(str(n.id), True, pygame.Color(0, 0, 0))
        rect = id_srf.get_rect(center=(x + 3, y - 3.2))
        screen.blit(id_srf, rect)


    # draw agents
    for agent in agents:
        # pygame.draw.circle(screen, Color(122, 61, 23),
        #                    (int(agent.pos.x), int(agent.pos.y)), 10)
        # ashe agents
        ashe = pygame.image.load('imeges/ashagent.png')
        rect2 = ashe.get_rect(center=(agent.pos.x, agent.pos.y))
        screen.blit(ashe, rect2)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        # pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        pika = pygame.image.load('imeges/pika.png')
        rect2 = pika.get_rect(center=(p.pos.x, p.pos.y))
        screen.blit(pika, rect2)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(10)

    print("taken_agents: " + str(taken_agents.keys()))
    if len(taken_agents) != len(agents):

        assigned_edges = assign_edges(pokemons, taken_agents)

        for agent in agents:
            if agent.id not in taken_agents.keys():
                min_dist = sys.float_info.max
                for e in assigned_edges:
                    if min_dist > dijkstra_distances[agent.src][e[0]]:
                        min_dist = dijkstra_distances[agent.src][e[0]]
                        poke_edge = e
                # adds the path to the agent's queue
                path = shortest_path(get_agent(agent.id).src, poke_edge[0])
                for node in path:
                    queues[agent.id].append(node)
                # adds the last edge to the agent's queue
                queues[agent.id].append(poke_edge[1])
                taken_agents[agent.id] = e

    for agent in agents:
        if len(queues[agent.id]) == 0 and agent.id in taken_agents and agent.dest == -1:
            print("agent " + str(agent.id) + " completed " + str(taken_agents[agent.id][0]) + " " + str(taken_agents[agent.id][1]))
            taken_agents.pop(agent.id)

        while agent.dest == -1 and not len(queues[agent.id]) == 0:
            next_node = queues[agent.id].pop()
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
        ttl = client.time_to_end()
    client.move()

# game over: