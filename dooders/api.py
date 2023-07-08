# uvicorn main:app --host 0.0.0.0 --port 8080 --reload

import asyncio

from experiment import Experiment, SessionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dooders.sdk.config import default_config
from dooders.sdk.strategies import *

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
    message: str


@app.get("/")
async def main() -> ServerResponse:
    return ServerResponse(status=200, message="Hello World!")


@app.get("/start")
async def main() -> ServerResponse:
    response, _ = experiment.start()
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
        experiment = Experiment(default_config)
        manager.add_experiment(experiment)

        while True:
            parameters = await websocket.receive_json()
            # experiment.set_parameters(parameters)

            experiment.setup_experiment()

            while experiment.simulation.running == True:
                experiment.execute_cycle()
                results = experiment.get_cycle_results()
                await websocket.send_json(results['simulation'])
                # snooze for 1 second
                await asyncio.sleep(.1)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Websocket disconnected")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('api:app', host="localhost", port=8080,
                reload=True, debug=True, workers=1)
