import enum


class MapValue(enum.Enum):
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    WINNER = 3


class WinMethod(enum.Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL_LEFT = 2
    DIAGONAL_RIGHT = 3

class GameStatus(enum.Enum):
    LOST = "Lost"
    REJECTED = "Rejected"
    DECLINED = "Declined"
    WAITING = "Waiting"
    ACCEPT = "To Accept"
    PROGRESS = "In Progress"
    DRAW = "Draw"
    WON = "Won"
