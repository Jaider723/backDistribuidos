from .enums import GameStateEnum
from typing import List
from .person import Player
from threading import Semaphore
from .enums import EventsSendCode, GameStateEnum
import secrets
import random

class Game:
    
    def __init__(self):
        self.__gamestate: GameState
        self.__players: List[Player] = []
        self.__id: str = secrets.token_hex(4)
        self.__turn: int = 0
        self.__diceNumber: tuple[int, int] = (0, 0)
        self.__semaphore = Semaphore()
        self.__readyNumber = 0
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
    
    def getIsOut(self) -> bool:
        return self.__
    
    def setReadyNumber(self, number: int):
        self.__readyNumber = number
    
    def changeState(self, gameState: GameStateEnum):
        self.__gamestate = self.__gamestate.changeState(gameState)
        
    async def addPlayer(self, player: Player):
        self.__players.append(player)
        await player.run()
        
    def eventHadler(self, message: str):
        pass

    async def addPlayerColor(self,  playerId: str, color: str) ->bool:
        self.__semaphore.acquire()
        if (not self.__gameColors[color]):
            player = self.getPlayer(playerId)
            if(player is not None):
                player.setColor(color)
                self.__gameColors[color] = True
                self.updateAvailableColors()
            data = {
                "colors": ",".join(list(self.__gameColors.keys()))
            }
            for player in self.__players:
                await player.send(EventsSendCode.availableColors.value, data)
            self.__semaphore.release()
            return True
        return False
    
    def updateAvailableColors(self):
        colors = self.__gameColors.copy()
        self.__gameColors = {key: value for key, value in colors.items() if not value}      

    async def rollDices(self, playerId: str) -> tuple[int, int]:
        player = self.getPlayer(playerId)
        print(f"Jugador {playerId} ha lanzado los dados")

        self.__diceNumber = (random.randint(0, 5), random.randint(0, 5))
        data = {
            "dices": ",".join(map(str, self.__diceNumber)),
        }
        print(f"Dados lanzados: {data['dices']}")

        if player is not None:

            if player.__isOut:
                print(f"Enviando evento de roll dice de jugador {playerId}")
                await player.send(EventsSendCode.sendDices.value, data)

            else:
                print(f"Enviando evento de inicio de turno al jugador {playerId}")
                await player.send(EventsSendCode.beginTurn.value, data)

        return self.__diceNumber
    
    def defineTurn(self):
        playerTurn = self.__turn % len(self.__players)
        return playerTurn
    
    def getTurnPlayer(self) -> Player:
        playerTurn = self.defineTurn()
        return self.__players[playerTurn]
    
    async def readyBroadcast(self):
        for player in self.__players:
            await player.send(EventsSendCode.ready.value, {})
    
    async def moveBroadcast(self,data):
        currentPlayer = self.getTurnPlayer()
        for player in self.__players:
            if player.getId() != currentPlayer.getId():
                await player.send(EventsSendCode.move.value, data)

class GameState:

    def __init__(self, gameState: GameStateEnum, game: Game):
        self.__gameState: GameStateEnum = gameState
        self.__game = game
        
    def changeState(self, gameState: GameStateEnum)-> 'GameState':
        return self
    
    def run(self, message: str):
        pass
    