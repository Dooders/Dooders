from dooders.agents import Dooder
from dooders.model import Simulation

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

# from mesa.visualization.UserParam import Slider, StaticText

def Avatar(agent):
    if agent is None:
        return

    portrayal = {}

    portrayal["Shape"] = "dooders/resources/red_dot.png"
    # https://icons8.com/web-app/433/sheep
    portrayal["scale"] = 0.9
    portrayal["Layer"] = 1

    return portrayal

canvas_element = CanvasGrid(Avatar, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Dooders", "Color": "#AA0000"}])

# model_params = {"title": mesa.visualization.UserParam.StaticText(
#     "Parameters:"), "initial_agents": mesa.visualization.Slider("Initial Dooder Population", 100, 10, 300)}

model_params = {}

server = ModularServer(
    Simulation, [canvas_element, chart_element], "Wolf Sheep Predation", model_params)
server.port = 8521

