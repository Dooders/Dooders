from agents import Dooder
from model import Simulation

from mesa import visualization


def Avatar(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Dooder:
        portrayal["Shape"] = "wolf_sheep/resources/sheep.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

canvas_element = visualization.CanvasGrid(Avatar, 20, 20, 500, 500)
chart_element = visualization.ChartModule(
    [{"Label": "Dooders", "Color": "#AA0000"}])

model_params = {"title": visualization.StaticText(
    "Parameters:"), "initial_agents": visualization.Slider("Initial Dooder Population", 100, 10, 300)}

server = visualization.ModularServer(
    Simulation, [canvas_element, chart_element], "Wolf Sheep Predation", model_params)
server.port = 8521
