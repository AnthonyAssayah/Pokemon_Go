import json
from types import SimpleNamespace
import pygame
import pygame_gui
from pygame import RESIZABLE, VIDEORESIZE, gfxdraw, display
# default port
from classes.DiGraphAlgo import DiGraphAlgo
from client_python.client import Client

PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
# init pygame
pygame.init()
# set window size
WIDTH, HEIGHT = 1080, 720
# upper title
pygame.font.init()
pygame.display.set_caption('Pokemon go!')
# resizeble window
window_surface = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# set background image
background = pygame.image.load('imeges\wallpeper.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
window_surface.blit(pygame.transform.scale(background, (WIDTH, HEIGHT)), (0, 0))
# set time
clock = pygame.time.Clock()
# connect to client
client = Client()
client.start_connection(HOST, PORT)
# font of ids
FONT = pygame.font.SysFont('Arial', 16, bold=True)
# load the json string into SimpleNamespace Object
graph_json = client.get_graph()
graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
# scale window
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
        return scale(data, 50, window_surface.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, window_surface.get_height()-50, min_y, max_y)

radius = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()
# play gui
is_running = True
while is_running:

    # time_delta = clock.tick(60) / 1000.0
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            pygame.quit()
            exit(0)
        # resize event
        elif event.type == VIDEORESIZE:
            window_surface = pygame.display.set_mode(
                event.dict['size'], RESIZABLE)
            window_surface.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))

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
            pygame.draw.line(window_surface, pygame.Color(0, 0, 0),
                             (src_x, src_y), (dest_x, dest_y), 2)

            # draw nodes
        for n in graph.Nodes:
            x = my_scale(n.pos.x, x=True)
            y = my_scale(n.pos.y, y=True)

            # pokeball nodes
            poke = pygame.image.load('imeges/pokeball.png')
            rect2 = poke.get_rect(center=(x, y))
            window_surface.blit(poke, rect2)

            # draw the node id in the middle of pokeball
            id_srf = FONT.render(str(n.id), True, pygame.Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x + 3, y - 3.2))
            window_surface.blit(id_srf, rect)

        # draw agents
        for agent in agents:
            # ashe agents
            ashe = pygame.image.load('imeges/ashagent.png')
            rect2 = ashe.get_rect(center=(agent.pos.x, agent.pos.y))
            window_surface.blit(ashe, rect2)
        # draw pokemons
        for p in pokemons:
            pika = pygame.image.load('imeges/pika.png')
            rect2 = pika.get_rect(center=(p.pos.x, p.pos.y))
            window_surface.blit(pika, rect2)

        # update screen changes
        display.update()

        # refresh rate
        clock.tick(60)
    pygame.display.update()