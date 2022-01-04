"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
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

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
# --------------------------------------------
DWGA = DiGraphAlgo()
DWGA.load_from_json(graph_json)
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

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


def assign_edges() -> []:  # list of (int, int) tuples

    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]

    ret = {}
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        src, dest = get_edge(p)
        print(str(src) + "----" + str(dest))
        print(str(type(src))+"*****"+str(type(dest)))
        print(str(p.type))
        if src is None and dest is None:
            return None

        ret[0] = (src, dest)
    return ret


def get_edge(pokemon) -> (int, int):

    x = float(p.pos.split(',')[0])
    y = float(p.pos.split(',')[1])

    for n in DWGA.get_graph().get_all_v().values():

        for e in n.get_out():
            # check if the slope between src
            m1 = (y - n.pos.location()[1])/(x - n.pos.location()[0])
            dest_loc = DWGA.get_graph().get_all_v()[e.get_destination()].location()
            m2 = (dest_loc[1] - n.pos.location()[1])/(dest_loc[0] - n.pos.location()[0])

            eps = 0.0000001

            if m2 + eps > m1 > m2 - eps:
                #diraction
                if n.get_key() < e.get_destination():

                    return (n.get_key(), e.get_destination()) if (p.type() < 0) else (e.get_destination(), n.get_key())
                else:

                    return (e.get_destination(), n.get_key()) if (pokemon.type > 0) else (n.get_key(), e.get_destination())
    return None, None


def get_agent(id) :
    for agent in agents:
        if id == agent.id:
            return agent
    return None

def matchagent(call) -> int:  # gets call in the form of a tuple (src_id, dest_id) representing the edge on which the pokemon is located. returns assigned agent id
    bestagent = None  # if stays none , no avalible agent
    min = sys.float_info.max
    for agent in agents:

        # if queues[agent.id] is None:
        #     queues[agent.id] = queue.Queue()

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

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

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
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    list = assign_edges()
    # queues = [a]

    for p in pokemons:
        agent_id = matchagent(list[0])
        if agent_id is None:
            continue

        path = shortest_path(get_agent(agent_id).src, list[0][0])
        for node in path:
            queues[agent_id].append(node)

        queues[agent_id].append(list[0][1])


    # choose next edge
    for agent in agents:

        if agent.dest == -1 and not len(queues[agent.id]) == 0:

            next_node = queues[agent.id].pop()
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over:
