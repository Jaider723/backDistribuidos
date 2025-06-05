from threading import Semaphore
from fastapi import WebSocket, WebSocketDisconnect
from .enums import EventsCode, EventsSendCode
from typing import Dict

class Player:
    
    def __init__(self, id: str, name: str, color:str, con: WebSocket, game: object):
        self.__name: str = name
        self.__color:str = color
        self.__con:WebSocket = con
        self.__semaphore = Semaphore()
        self.__id: str = id
        self.__game: object = game
        self.__isConect: bool = True
        self.__isOut: bool = False
    
    def getId(self)->str:
        return self.__id
    
    def setColor(self, color: str) -> None:
        self.__color = color

    def getIsConnect(self) ->bool:
        is_connected = self.__isConect
        return is_connected
    
    async def send(self, code:int,  message: Dict[str, str]) -> None:
        message["code"] = str(code)
        if self.__isConect:
            await self.__con.send_json(message)

    async def run(self):
        try:
            while(self.getIsConnect()):
                json = await self.__con.receive_json(mode='text')
                print(json)
                opcode = json.get("code")
                if opcode is None:
                    raise ValueError("El codigo del evento no puede ser nulo")
                match opcode:
                    case EventsCode.setColor.value:
                        color = json.get("color")
                        await self.__con.send_json(
                            {
                                "code": EventsSendCode.setColor.value,
                                "color": color,
                                "success": str(await self.__game.addPlayerColor(self.__id, color))
                            }
                        )

                    case EventsCode.ready.value:
                        ready = self.__game.getReadyNumber() + 1
                        if ready >= 4:
                            await self.__game.readyBroadcast()
                            playerId = self.__game.getTurnPlayer().getId()
                            await self.__game.rollDices(playerId)
                            continue
                        self.__game.setReadyNumber(ready)

                    case EventsCode.rollDices.value:
                        playerId = self.__game.getTurnPlayer().getId()
                        await self.__game.rollDices(playerId)
                    
                    case EventsCode.move.value:
                        await self.__game.moveBroadcast(json.get("playerId"), json.get("box"), json.get("pawn"))

                    case EventsCode.endTurn.value:
                        await self.__game.endTurn()


                    case _:
                        print(f"Evento no manejado: {opcode}")
            
        except WebSocketDisconnect as e:
            print(f"se ha desconectado un jugador: {e}")
            self.__semaphore.acquire()
            self.__isConect = False
            self.__semaphore.release()