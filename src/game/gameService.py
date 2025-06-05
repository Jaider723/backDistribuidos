from .gameObject import Game
from .person import Player
from typing import List
from fastapi import WebSocket

class GameEventsService:
    
    def __init__(self):
        self.__games: List[Game] = []
        
    def createGame(self)->str:
        game = Game()
        self.__games.append(game)
        return game.getId()
        
    def addPlayer(self, con: WebSocket,  playerId: str, gameId: str, name: str)->bool:
        for game in self.__games:
            if(game.getId() == gameId):
                game.addPlayer(Player(playerId, name, "", con, game))
                return True
        return False
