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
        json = await websocket.receive_json(mode='text')
        if(json["gameId"] == "" or json["gameId"] is None):
            raise ValueError("El gameId no puede ser nulo o vacio")
        if(json["playerId"] == "" or json["playerId"] is None):
            raise ValueError("El playerId no puede ser nulo o vacio")
        if(json["name"] == "" or json["name"] is None):
            raise ValueError("El name no puede ser nulo o vacio")
        print(json)
        if  gameManeger.addPlayer(websocket, json["playerId"], json["gameId"], json["name"]):
            await websocket.send_json({
                "code": -1
            })
    except WebSocketException:
        print("se desconecto")
    except ValueError as e:
        await websocket.close(code=1008, reason=str(e))
        print(f"Error: {e}")
