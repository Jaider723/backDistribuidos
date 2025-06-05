from .gameService import GameEventsService
from fastapi import APIRouter, WebSocket, WebSocketException

route = APIRouter(
    prefix="/game",
    tags=["game"]
)

gameManeger = GameEventsService()

@route.post("")
def createGame():
    return gameManeger.createGame()

@route.websocket("/ws")
async def addPlayer(websocket: WebSocket):
    try:
        await websocket.accept()
        print("conectado")
        data = await websocket.receive_json(mode="text")
        print(data)
        await websocket.send_text('{"code": 1, "pawn": 15, "box": 101}')
        await websocket.close()
    except WebSocketException:
        print("se desconecto")