from threading import Thread, Semaphore
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class Player(Thread):
    
    def __init__(self, id: str, name: str, color:List[float], con: WebSocket, game: object):
        self.__name: str = name
        self.__color: List[float] = color
        self.__con:WebSocket = con
        self.__semaphore = Semaphore()
        self.__id: str = id
        self.__game = game
        self.__isConect: bool = True
    
    def getId(self)->str:
        return self.__id
        
    def run(self):
        try:
            while(self.__isConect):
                pass
        except WebSocketDisconnect:
            print("se ha desconectado un jugador")
