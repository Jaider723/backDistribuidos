from .gameService import GameEventsService
from .gameObject import Game, GameState
from fastapi import APIRouter, WebSocket, WebSocketException

route = APIRouter(
    prefix="/game",
    tags=["game"]
)

gameManeger = GameEventsService()

@route.post("")
def createGame():
    return gameManeger.createGame()

@route.websocket("/addPlayer")
async def addPlayer(websocket: WebSocket):
    try:
        await websocket.accept()
        print("conectado")
        data = await websocket.receive_json(mode="text")
        await websocket.send_text('{"code": 1, "pawn": 15, "box": 101}')
        await websocket.close()

    except WebSocketException:
        print("se desconecto")
