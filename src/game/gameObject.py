from .enums import GameStateEnum
from .person import Player
from typing import List
from threading import Semaphore
import secrets

class Game:
    
    def __init__(self):
        self.__gamestate: GameState
        self.__players: List[Player] = []
        self.__id: str = secrets.token_hex(4)
        self.__turn: int = 0
        self.__diceNumber: tuple[int, int] = (0, 0)
        self.__semaphore = Semaphore()
        self.__gameColors: dict[str, bool] = { 
                                                'yellow':False,
                                                'red':False,
                                                'blue':False,
                                                'green':False
                                            }
        
    def getId(self)->str:
        return self.__id
    
    def getPlayer(self, playerId: str)->Player | None:
        i = 0
        while(i < len(self.__players)):
            if(self.__players[i].getId() == playerId):
                return self.__players[i]
            i+=1
        
    
    def changeState(self, gameState: GameStateEnum):
        self.__gamestate = self.__gamestate.changeState(gameState)
        
    def addPlayer(self, player: Player):
        self.__players.append(player)
        
    def eventHadler(self, message: str):
        pass

    def addPlayerColor(self,  playerId: str, color: str) ->bool:
        self.__semaphore.acquire()
        if (not self.__gameColors[color]):
            player = self.getPlayer(playerId)
            if(player is not None):
                player.setColor(color)
            self.__semaphore.release()
            return True
        return False
    
    def updateAvailableColors(self) -> dict[str, bool]:
        self.__semaphore.acquire()
        colors = self.__gameColors.copy()
        self.__gameColors = {key: value for key, value in colors.items() if not value}
        self.__semaphore.release()
        return colors
    
class GameState:
    
    def __init__(self, gameState: GameStateEnum, game: Game):
        self.__gameState: GameStateEnum = gameState
        self.__game = game
        
    def changeState(self, gameState: GameStateEnum)-> 'GameState':
        return self
    def run(self, message: str):
        pass