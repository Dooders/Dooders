# uvicorn main:app --host 0.0.0.0 --port 8080 --reload

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dooders.experiment import Experiment
from dooders.parameters import Parameters

DEFAULT_PARAMETERS = Parameters(
    width=20,
    height=20,
    initial_agents=10,
    verbose=True,
    steps=100,
)

app = FastAPI()
experiment = Experiment(DEFAULT_PARAMETERS)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ServerResponse(BaseModel):
    status: str
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

@app.websocket("/test")
async def test(websocket: WebSocket):
    await websocket.accept()
    while True:
        request = await websocket.receive_json()
        message = request["message"]
        for i in range(10000):
            await websocket.send_json({
                "message": f"{message} - {i+1}",
                "number": i+1
            })