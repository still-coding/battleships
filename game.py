# -*- coding: utf-8 -*-
"""Game logic module."""

from random import randint
from string import ascii_uppercase

from curtsies import FSArray, FullscreenWindow, Input, fsarray
from curtsies.fmtfuncs import blue, bold, green, on_blue, on_red, red
from termtables import to_string as make_termtable

from config import BOARD_SIZE, SHIPS
from game_utils import (
    AI,
    Board,
    Dot,
    Mode,
    Player,
    Ship,
    ShipDirection,
    Symbol,
    UserWantsToExit,
)

SYMBOL_MAPPING = {
    Symbol.Empty: " ",
    Symbol.Ship: "■",
    Symbol.Hit: "☒",
    Symbol.Miss: "•",
}


class User(Player):
    "Basically incapsulates user input for shooting"
    def ask(self, window, input_generator):
        play_message = [
            blue("Sink your opponent's ships. Shoot accurately!"),
            "Controls:",
            f'> {bold("[↑] [↓] [←] [→]")} to move cursor',
            f'> {bold("[Space]")} to shoot',
            f'> {bold("[Esc]")} to exit game',
            "",
            f'{red("Enemy board".center(self.enemy_board.size * 4))} {green("Your board".center(self.own_board.size * 4))}',
        ]

        crosshair = self.previous_shot if self.previous_shot else Dot()
        window.render_to_terminal(
            play_message
            + Game.get_board_image(self.enemy_board, crosshair, self.own_board)
        )
        self.was_hit = False
        for c in input_generator:
            cant_shoot = False
            if c == "<ESC>":
                raise UserWantsToExit
            if c == "<RIGHT>":
                crosshair.right()
            if c == "<LEFT>":
                crosshair.left()
            if c == "<UP>":
                crosshair.up()
            if c == "<DOWN>":
                crosshair.down()
            if c == "<SPACE>":
                if self.enemy_board.is_empty(crosshair) or self.enemy_board.is_ship(
                    crosshair
                ):
                    return crosshair
                else:
                    cant_shoot = True
            window.render_to_terminal(
                play_message
                + Game.get_board_image(
                    self.enemy_board, crosshair, self.own_board, warn=cant_shoot
                )
            )


class Game:
    "Main game logic and UI. Very bloated -_-"
    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.user_board = Board(board_size)
        self.ai_board = Board.random_ships_arrangement()
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def greet(self):
        with FullscreenWindow() as window:
            with Input() as input_generator:
                welcome_message = [
                    bold(blue("Welcome to BATTLESHIPS game!")),
                    "* At first - you need to place your ships on the game board.",
                    "* After that - get ready to battle against AI.",
                    "In order to win you need to sink all of your opponent's ships.",
                    "Good luck!",
                    f"Press {bold('any key')} to start.",
                ]
                window.render_to_terminal(welcome_message)
                next(input_generator)

    @staticmethod
    def get_board_image(
        left_board, cur_pos, right_board=None, warn=False, current_ship=None
    ):
        header = [bold(blue(letter)) for letter in ascii_uppercase[: left_board.size]]

        if not right_board:
            lines = [header + [bold(blue("#"))]]
            cells = left_board.cells
            for i, row in enumerate(cells):
                str_line = []
                for j, cell in enumerate(row):
                    if cur_pos == Dot(i, j):
                        str_line.append(
                            on_red(SYMBOL_MAPPING[cell])
                            if warn
                            else on_blue(SYMBOL_MAPPING[cell])
                        )
                    else:
                        str_line.append(SYMBOL_MAPPING[cell])
                str_line.append(bold(blue(str(i))))
                lines.append(str_line)

            if current_ship:
                lines[current_ship.start.row + 1][current_ship.start.col] = (
                    red(SYMBOL_MAPPING[Symbol.Ship])
                    if warn
                    else green(SYMBOL_MAPPING[Symbol.Ship])
                )
                for d in current_ship.dots[1:]:
                    lines[d.row + 1][d.col] = (
                        red(SYMBOL_MAPPING[Symbol.Ship])
                        if warn
                        else green(SYMBOL_MAPPING[Symbol.Ship])
                    )
            return make_termtable(lines).split("\n")

        lines = [header + [bold(blue("#"))] + header]
        cells = left_board.cells

        for i, (rowl, rowr) in enumerate(zip(cells, right_board.cells)):
            str_line = []
            for j, cell in enumerate(rowl):
                to_print = SYMBOL_MAPPING[cell]
                if cell == Symbol.Ship and left_board.hid:
                    to_print = SYMBOL_MAPPING[Symbol.Empty]

                if cur_pos == Dot(i, j):
                    str_line.append(on_red(to_print) if warn else on_blue(to_print))
                else:
                    str_line.append(to_print)
            str_line.append(bold(blue(str(i))))
            str_line.extend(map(lambda x: SYMBOL_MAPPING[x], rowr))
            lines.append(str_line)
        return make_termtable(lines).split("\n")

    def arrange_user_ships(self):
        total_ships = sum(i["count"] for i in SHIPS)
        with FullscreenWindow() as window:
            with Input() as input_generator:
                current_ship_num = 1
                for ship_data in SHIPS:
                    for _ in range(ship_data["count"]):
                        ship = Ship(length=ship_data["size"], name=ship_data["name"])
                        arrange_message = [
                            blue("Arrange your battleships on the game board."),
                            "Controls:",
                            f'> {bold("[↑] [↓] [←] [→]")} to move ship',
                            f'> {bold("[Space]")} to rotate ship',
                            f'> {bold("[Enter]")} to place ship and continue',
                            f'> {bold("[Esc]")} to exit game',
                            f"Current ship: {ship.name}, {current_ship_num} of {total_ships}",
                            "",
                            green("Your board".center(self.user_board.size * 4)),
                        ]

                        warning_draw = not all(map(self.user_board.is_empty, ship.dots))
                        window.render_to_terminal(
                            arrange_message
                            + self.get_board_image(
                                self.user_board,
                                ship.start,
                                warn=warning_draw,
                                current_ship=ship,
                            )
                        )
                        for c in input_generator:
                            can_rotate = True
                            if c == "<ESC>":
                                return False
                            if c == "<RIGHT>":
                                if (
                                    ship.start.col
                                    < self.user_board.size
                                    - ship.length
                                    * (ship.direction == ShipDirection.Horizontal)
                                ):
                                    ship.start.right()
                            if c == "<LEFT>":
                                ship.start.left()
                            if c == "<UP>":
                                ship.start.up()
                            if c == "<DOWN>":
                                if (
                                    ship.start.row
                                    < self.user_board.size
                                    - ship.length
                                    * (ship.direction == ShipDirection.Vertical)
                                ):
                                    ship.start.down()
                            if c == "<SPACE>":
                                if (
                                    ship.start.row
                                    < self.user_board.size - ship.length + 1
                                    and ship.start.col
                                    < self.user_board.size - ship.length + 1
                                ):
                                    ship.rotate()
                                else:
                                    can_rotate = False
                            if c == "<Ctrl-j>":
                                if all(map(self.user_board.is_empty, ship.dots)):
                                    self.user_board.add_ship(ship)
                                    current_ship_num += 1
                                    break
                            warning_draw = not all(
                                map(self.user_board.is_empty, ship.dots)
                            )
                            window.render_to_terminal(
                                arrange_message
                                + self.get_board_image(
                                    self.user_board,
                                    ship.start,
                                    warn=warning_draw or not can_rotate,
                                    current_ship=ship,
                                )
                            )
        return True

    def grats(self, user_won=True):
        if user_won:
            return bold(green("You have vanquished your foe! Congratulations!"))
        else:
            return bold(red("You have been defeated by AI! Good luck next time!"))

    def loop(self):
        with FullscreenWindow() as window:
            with Input() as input_generator:
                while True:
                    if not self.user.move(window, input_generator):
                        return
                    if not self.ai_board.has_alive_ships():
                        window.render_to_terminal(
                            [self.grats(), bold("Press any key to exit.")]
                        )
                        next(input_generator)
                        return
                    if not self.ai.move():
                        return
                    if not self.user_board.has_alive_ships():
                        window.render_to_terminal(
                            [self.grats(user_won=False), bold("Press any key to exit.")]
                        )
                        next(input_generator)
                        return

    def start(self):
        self.greet()
        # self.user_board = Board.random_ships_arrangement()
        # self.user_board.hid = False
        # self.ai_board.hid = False
        continue_game = self.arrange_user_ships()
        if not continue_game:
            return
        self.user_board.mode = Mode.Play
        self.loop()
