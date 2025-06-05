from enum import Enum

class GameStateEnum(Enum):
    colorChoose = 1
    begin = 2
    beginTurn = 3,
    turn = 4,
    endturn = 5,
    end = 6

class receive_json(Enum):
    setColor = 1