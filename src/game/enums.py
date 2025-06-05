from enum import Enum

class GameStateEnum(Enum):
    colorChoose = 1
    begin = 2
    beginTurn = 3,
    turn = 4,
    endturn = 5,
    end = 6

class EventsCode(Enum):
    setColor = 1
    
class EventsSendCode(Enum):
    setColor = 1
    availableColors = 2
    beginTurn = 3