from .gameService import GameEventsService
from fastapi import APIRouter, WebSocket, WebSocketException

route = APIRouter(
    prefix="/game",
    tags=["game"]
)

gameManeger = GameEventsService()

@route.post("")
def createGame():
    value = gameManeger.createGame()
    print("Se ha creado un juego con id:", value)
    return value

@route.websocket("/addPlayer")
async def addPlayer(websocket: WebSocket):
    try:
        await websocket.accept()
        json = await websocket.receive_json(mode='text')
        print("Recibido:", json)
        if(json["gameId"] == "" or json["gameId"] is None):
            raise ValueError("El gameId no puede ser nulo o vacio")
        if(json["playerId"] == "" or json["playerId"] is None):
            raise ValueError("El playerId no puede ser nulo o vacio")
        if(json["name"] == "" or json["name"] is None):
            raise ValueError("El name no puede ser nulo o vacio")
        if not await gameManeger.addPlayer(websocket, json["playerId"], json["gameId"], json["name"]):
            await websocket.send_json({
                "code": -1
            })
    except WebSocketException:
        print("se desconecto")
    except ValueError as e:
        await websocket.close(code=1008, reason=str(e))
        print(f"Error: {e}")
