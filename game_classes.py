from dataclasses import dataclass, field
from typing import ClassVar, List
from enum import Enum
from abc import ABC, abstractmethod
from config import BOARD_SIZE, SHIPS
from random import randint

Symbol = Enum("Symbol", ["Empty", "Ship", "Miss", "Hit"])
ShipDirection = Enum("ShipDirection", ["Horizontal", "Vertical"])
Mode = Enum("Mode", ["Arrange", "Play"])


class UsedDotShot(ValueError):
    def __str__(self):
        return "Used dot shot"

@dataclass
class Dot:
    """Board position store and management for ease of use in game logic."""

    _board_size: ClassVar[int] = BOARD_SIZE
    row: int = 0
    col: int = 0

    def __post_init__(self):
        if not (isinstance(self.row, self.__class__) or isinstance(self.row, int)):
            raise TypeError("Dot first arg must be int or Dot object")
        if not isinstance(self.col, int):
            raise TypeError("Dot second arg must be int")
        if isinstance(self.row, self.__class__):
            self.row, self.col = self.row.row, self.row.col
        if self.row < 0 or self.row >= self.__class__._board_size:
            raise ValueError("Dot row must be in [0, board_size)")
        if self.col < 0 or self.col >= self.__class__._board_size:
            raise ValueError("Dot col must be in [0, board_size)")

    def up(self):
        self.row = self.row - 1 if self.row else 0

    def down(self):
        self.row = (
            self.row + 1
            if self.row < self.__class__._board_size - 1
            else self.__class__._board_size - 1
        )

    def left(self):
        self.col = self.col - 1 if self.col else 0

    def right(self):
        self.col = (
            self.col + 1
            if self.col < self.__class__._board_size - 1
            else self.__class__._board_size - 1
        )
        
    @classmethod
    def random(cls):
        return Dot(randint(0, cls._board_size - 1), randint(0, cls._board_size - 1))


    # def linearize(self):
    #     return self.row * self.__class__._board_size + self.col

    # @classmethod
    # def from_linear_index(cls, i):
    #     if not isinstance(i, int):
    #         raise TypeError("index must be an integer")
    #     if i < 0 or i >= cls._board_size * cls._board_size:
    #         raise ValueError("index must be in [0, board_size * board_size)")
    #     r = i // cls._board_size
    #     c = i % cls._board_size
    #     return Dot(r, c)

    def surrounding(self):
        result = []
        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                try:
                    new_dot = Dot(i, j)
                except ValueError:
                    continue
                if new_dot != self:
                    result.append(new_dot)
        return result


class Board:
    def clear(self):
        self.cells = [[Symbol.Empty] * self.size for _ in range(self.size)]

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.clear()
        self.ready = False
        self.ships = []
        self.hid = True
        self.__mode = Mode.Arrange
        

    def update(self):
        self.clear()
        for ship in self.ships:
            for d in ship.dots:
                self.cells[d.row][d.col] = Symbol.Ship
        if self.mode == Mode.Arrange:
            self.contour_ships()
        
    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, Mode):
            raise TypeError("mode must be a correct Mode instance")
        self.__mode = value
        self.update()


    def add_ship(self, ship):
        self.ships.append(ship)
        self.update()

    def contour_ships(self):
        for ship in self.ships:
            for d in ship.contour:
                self.cells[d.row][d.col] = Symbol.Miss


        # ids = []
        # for i, row in enumerate(self.cells):
        #     for j, cell in enumerate(row):
        #         if cell == Symbol.Ship:
        #             continue
        #         if any(
        #             map(
        #                 lambda x: self.cells[x.row][x.col] == Symbol.Ship,
        #                 Dot(i, j).surrounding(),
        #             )
        #         ):
        #             ids.append((i, j))
        # for r, c in ids:
        #     self.cells[r][c] = Symbol.Miss

    def is_empty(self, dot):
        return self.cells[dot.row][dot.col] == Symbol.Empty

    def is_ship(self, dot):
        return self.cells[dot.row][dot.col] == Symbol.Ship

    @classmethod
    def random_ships_arrangement(cls):
        result = cls()
        for ship_data in SHIPS:
            for _ in range(ship_data["count"]):
                ship = Ship(length=ship_data["size"], name=ship_data["name"])
                while True:
                    ship.start = Dot.random()
                    ship.direction = (
                        ShipDirection.Horizontal
                        if randint(0, 100) > 50
                        else ShipDirection.Vertical
                    )
                    try:
                        if all(map(result.is_empty, ship.dots)):
                            result.add_ship(ship)
                            break
                    except:
                        continue
        result.mode = Mode.Play
        return result

    def shot(self, dot):
        if self.cells[dot.row][dot.col] == Symbol.Ship:
            self.cells[dot.row][dot.col] = Symbol.Hit
            return True
        if self.cells[dot.row][dot.col] == Symbol.Empty:
            self.cells[dot.row][dot.col] = Symbol.Miss
            return False
        raise UsedDotShot


@dataclass
class Ship:
    start: Dot = field(default_factory=lambda: Dot(0, 0))
    length: int = 1
    name: str = ""
    direction: ShipDirection = ShipDirection.Horizontal
    hits: List[Dot] = field(default_factory=list)
    on_board: Board | None = None

    def rotate(self):
        self.direction = (
            ShipDirection.Vertical
            if self.direction == ShipDirection.Horizontal
            else ShipDirection.Horizontal
        )

    @property
    def dots(self):
        if self.length == 1:
            return [self.start]
        return [
            Dot(self.start.row + i, self.start.col)
            if self.direction == ShipDirection.Vertical
            else Dot(self.start.row, self.start.col + i)
            for i in range(self.length)
        ]

    @property
    def contour(self):
        result = []
        if self.direction == ShipDirection.Horizontal:
            for c in range(self.start.col - 1, self.start.col + self.length + 1):
                for r in (self.start.row - 1, self.start.row + 1):
                    try:
                        result.append(Dot(r, c))
                    except ValueError:
                        pass
            try:
                result.append(Dot(self.start.row, self.start.col - 1))
            except ValueError:
                pass
            try:
                result.append(Dot(self.start.row, self.start.col + self.length))
            except ValueError:
                pass
            return result
        
        if self.direction == ShipDirection.Vertical:
            for r in range(self.start.row - 1, self.start.row + self.length + 1):
                for c in (self.start.col - 1, self.start.col + 1):
                    try:
                        result.append(Dot(r, c))
                    except ValueError:
                        continue
            try:
                result.append(Dot(self.start.row - 1, self.start.col))
            except ValueError:
                pass
            try:
                result.append(Dot(self.start.row + self.length, self.start.col))
            except ValueError:
                pass
        return result




class Player(ABC):
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    @abstractmethod
    def ask():
        pass

    def move():
        try:
            enemy_board.shot(self.ask())
        except:
            return False
        else:
            return True


class AI(Player):
    def ask():
        return Dot.random()






