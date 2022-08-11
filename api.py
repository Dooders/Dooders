# uvicorn main:app --host 0.0.0.0 --port 8080 --reload

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Tuple

from dooders.experiment import Experiment, SessionManager
from dooders.parameters import ExperimentParameters

DEFAULT_PARAMETERS = ExperimentParameters(
    width=20,
    height=20,
    agents=10,
    verbose=True,
    verbosity=1,
    steps=100,
    initial_energy_value = 1,
    initial_energy_count = 10
)

app = FastAPI()
manager = SessionManager()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ServerResponse(BaseModel):
    status: int
    message: Tuple[str, str]


@app.get("/")
async def main() -> ServerResponse:
    return ServerResponse(status=200, message="Hello World!")


@app.get("/start")
async def main() -> ServerResponse:
    response, _ = experiment.start()
    print(response)
    return ServerResponse(status=200, message=response)


@app.get("/stop")
async def main() -> ServerResponse:
    response, _ = experiment.stop()
    return ServerResponse(status=200, message=response)


@app.get("/reset")
async def main() -> ServerResponse:
    response, _ = experiment.reset()
    return ServerResponse(status=200, message=response)


@app.websocket("/ExperimentData")
async def websocket_endpoint(websocket: WebSocket):
    """ 
    Websocket endpoint for the experiment.
    Sends experiment data to the client every time the simulation finishes a step. 
    """
    await manager.connect(websocket)
    try:
        experiment = Experiment(DEFAULT_PARAMETERS)
        manager.add_experiment(experiment)

        while True:
            parameters = await websocket.receive_json()
            experiment.set_parameters(ExperimentParameters(**parameters))

            while experiment.simulation.running and experiment.simulation.schedule.time < parameters['steps']:
                # experiment.agent_count = experiment.simulation.schedule.get_agent_count()
                experiment.simulation.step()
                results = experiment.simulation.get_results()
                await websocket.send_json(results)
                # snooze for 1 second
                await asyncio.sleep(.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('api:app', host="localhost", port=8080,
                reload=True, debug=True, workers=1)
