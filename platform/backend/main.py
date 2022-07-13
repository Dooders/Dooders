# uvicorn main:app --host 0.0.0.0 --port 8080 --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# data class for the response
class Response(BaseModel):
    status: str
    message: str


@app.get("/")
async def main() -> Response:
    return Response(status=200, message="Hello World!")

@app.get("/start")
async def main() -> Response:
    return Response(status=200, message="This has started")

@app.get("/stop")
async def main() -> Response:
    return Response(status=200, message="This has stopped")

@app.get("/reset")
async def main() -> Response:
    return Response(status=200, message="This has reset")