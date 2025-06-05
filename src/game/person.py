from threading import Semaphore
from fastapi import WebSocket, WebSocketDisconnect
from .enums import EventsCode, EventsSendCode
import asyncio

class Player:
    
    def __init__(self, id: str, name: str, color:str, con: WebSocket, game: object):
        self.__name: str = name
        self.__color:str = color
        self.__con:WebSocket = con
        self.__semaphore = Semaphore()
        self.__id: str = id
        self.__game: object = game
        self.__isConect: bool = True
    
    def getId(self)->str:
        return self.__id
    
    def setColor(self, color: str) -> None:
        self.__color = color

    def getIsConnect(self) ->bool:
        self.__semaphore.acquire()
        is_connected = self.__isConect
        self.__semaphore.release()
        return is_connected
    
    def send(self, code:str,  message: str) -> None:
        self.__semaphore.acquire()
        data = {
            "code": code,
        }
        data.update(message)
        if self.__isConect:
            asyncio.create_task(self.__con.send_json(data))
            print(message)
        self.__semaphore.release()

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
                                    "success": self.__game.addPlayerColor(self.__id, color)
                                }
                            )

                    # case GameStateEnum.beginTurn.value:
                    #     print("si entra acá")
                    #     await self.__con.send_json(
                    #             {
                    #                 "code": GameStateEnum.beginTurn.value,
                    #                 "dice": self.__game.rollDices(self.__id),
                    #                 "success": True
                    #             }
                    #         )
                    
                    # case GameStateEnum.turn.value:
                    #     pass

                    # case GameStateEnum.endTurn.value:
                    #     pass

                    # case GameStateEnum.end.value:
                    #     pass

                    case _:
                        print(f"Evento no manejado: {opcode}")
            
        except WebSocketDisconnect as e:
            print(f"se ha desconectado un jugador: {e}")
            self.__semaphore.acquire()
            self.__isConect = False
            self.__semaphore.release()
