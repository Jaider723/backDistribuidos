from threading import Thread, Semaphore
from fastapi import WebSocket, WebSocketDisconnect
from .enums import receiveJson

class Player(Thread):
    
    def __init__(self, id: str, name: str, color:str, con: WebSocket, game: object):
        self.__name: str = name
        self.__color:str = color
        self.__con:WebSocket = con
        self.__semaphore = Semaphore()
        self.__id: str = id
        self.__game = game
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

    async def run(self):
        print("funcionando")
        try:
            while(self.getIsConnect()):
                json = await self.__con.receive_json(mode='text')
                print(json)
                opcode = json.get("code")
                match opcode:
                    case receiveJson:
                        if opcode == receiveJson.setColor:
                            color = json.get("color")
                            self.__game.addPlayerColor(self.__id, color)
            
        except WebSocketDisconnect:
            print("se ha desconectado un jugador")
