# -*- coding: utf-8 -*-
"""Game logic module."""

from string import ascii_uppercase
from curtsies import FSArray, FullscreenWindow, Input, fsarray
from curtsies.fmtfuncs import blue, bold, green, on_blue, on_red, red
from termtables import to_string as make_termtable


from config import BOARD_SIZE, SHIPS
from game_classes import Dot, Board, ShipDirection, Player, AI, Ship, Symbol
from random import randint


SYMBOL_MAPPING = {
    Symbol.Empty: " ",
    Symbol.Ship: "■",
    Symbol.Hit: "☒",
    Symbol.Miss: "•",
}

class User(Player):
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

        crosshair = Dot()
        window.render_to_terminal(
            play_message + Game.get_board_image(self.enemy_board, crosshair, self.own_board)
        )

        for c in input_generator:
            can_shoot = True
            if c == "<ESC>":
                break
            if c == "<RIGHT>":
                crosshair.right()
            if c == "<LEFT>":
                crosshair.left()
            if c == "<UP>":
                crosshair.up()
            if c == "<DOWN>":
                crosshair.down()
            if c == "<SPACE>":
                if self.enemy_board.is_empty(crosshair) or self.enemy_board.is_ship(crosshair):
                    return crosshair
                else:
                    can_shoot = False
            window.render_to_terminal(
                play_message + Game.get_board_image(self.enemy_board, crosshair, self.own_board)
            )



class Game:
    # def random_board(self):
    #     self.ai_board = Board.random_ships_arrangement()

    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.user_board = Board(board_size)
        self.ai_board = Board.random_ships_arrangement()
        # self.ai_board = None
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    
    def greet(self):
        with FullscreenWindow() as window:
            with Input() as input_generator:
                # welcome screen
                welcome_message = [
                    bold(blue("Welcome to BATTLESHIPS game!")),
                    "* At first - you need to place your ships on the game board.",
                    "* After that - get ready to battle against AI.",
                    "In order to win you need to sink all of your opponent's ships.",
                    "Good luck!",
                    f"Press {bold('any key')} to start.",
                ]
                window.render_to_terminal(welcome_message)
                input_generator.__next__()
                # for c in input_generator:
                #     break
        
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

        lines = [header + ["#"] + header]
        cells = left_board.cells

        for i, (rowl, rowr) in enumerate(zip(cells, right_board.cells)):
            str_line = []
            for j, cell in enumerate(rowl):
                if cur_pos == Dot(i, j):
                    str_line.append(
                        on_red(SYMBOL_MAPPING[cell])
                        if warn
                        else on_blue(SYMBOL_MAPPING[cell])
                    )
                else:
                    str_line.append(SYMBOL_MAPPING[cell])
            str_line.append(str(i))
            str_line.extend(map(lambda x: SYMBOL_MAPPING[x], rowr))
            lines.append(str_line)
        return make_termtable(lines).split("\n")


    def arrange_user_ships(self):
        total_ships = sum(i["count"] for i in SHIPS)
        with FullscreenWindow() as window:
            with Input() as input_generator:
                current_ship_num = 1
                esc_pressed = False
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
                                self.user_board, ship.start, warn=warning_draw, current_ship=ship
                            )
                        )
                        for c in input_generator:
                            can_rotate = True
                            if c == "<ESC>":
                                esc_pressed = True
                                break
                            if c == "<RIGHT>":
                                if ship.start.col < self.user_board.size - ship.length * (
                                    ship.direction == ShipDirection.Horizontal
                                ):
                                    ship.start.right()
                            if c == "<LEFT>":
                                ship.start.left()
                            if c == "<UP>":
                                ship.start.up()
                            if c == "<DOWN>":
                                if ship.start.row < self.user_board.size - ship.length * (
                                    ship.direction == ShipDirection.Vertical
                                ):
                                    ship.start.down()
                            if c == "<SPACE>":
                                if (
                                    ship.start.row < self.user_board.size - ship.length + 1
                                    and ship.start.col < self.user_board.size - ship.length + 1
                                ):
                                    ship.rotate()
                                else:
                                    can_rotate = False
                            if c == "<Ctrl-j>":
                                if all(map(self.user_board.is_empty, ship.dots)):
                                    self.user_board.add_ship(ship)
                                    current_ship_num += 1
                                    break
                            warning_draw = not all(map(self.user_board.is_empty, ship.dots))
                            window.render_to_terminal(
                                arrange_message
                                + self.get_board_image(
                                    self.user_board,
                                    ship.start,
                                    warn=warning_draw or not can_rotate,
                                    current_ship=ship,
                                )
                            )
                        if esc_pressed:
                            break
                    if esc_pressed:
                        break

    def loop(self):
        with FullscreenWindow() as window:
            with Input() as input_generator:
                self.user.ask(window, input_generator)


# def new_game():
#     """Empties the board and defaults necessary internal game variables.

#     Args:
#         selected_player_symbol (Symbol, optional): Symbol player selects in the beginning of the game. Defaults to Symbol.X.
#     """
#     Dot._board_size = BOARD_SIZE
#     global board, turn_num

#     turn_num = 0


# def player_move(position):
#     """Checks if player can mark ones position on the board.

#     Args:
#         position (Position): current player position

#     Returns:
#         bool: success of move
#     """
#     if board[position.linearize()] != Symbol.E:
#         return False
#     board[position.linearize()] = player_symbol
#     return True


# def ai_move():
#     """Dumbest strategy - AI chooses first empty random position.
#     """
#     ai_pos = BOARD_SIZE * BOARD_SIZE // 2
#     while board[ai_pos] != Symbol.E:
#         ai_pos = randint(0, BOARD_SIZE * BOARD_SIZE - 1)
#     board[ai_pos] = ai_symbol


# def win_conditions():
#     """Generates every win condition mask for the given board size.

#     Yields:
#         list of bool: win condition board mask
#     """
#     zeros = [False for _ in range(BOARD_SIZE)]
#     ones = [True for _ in range(BOARD_SIZE)]
#     for i in range(BOARD_SIZE):
#         # lines
#         yield zeros[:] * i + ones[:] + zeros[:] * (BOARD_SIZE - i - 1)
#         # columns
#         yield [j % BOARD_SIZE == i for j in range(BOARD_SIZE * BOARD_SIZE)]
#     del zeros, ones
#     # diagonals
#     yield [i == j for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
#     yield [
#         i == BOARD_SIZE - j - 1 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
#     ]


# def we_have_a_winner():
#     """Checks if there is a winner.
#     Returns:
#         Symbol or None: winner symbol if there is one, None otherwise.
#     """
#     for candidate in (Symbol.X, Symbol.O):
#         for cond in win_conditions():
#             if list(map(lambda x, y: x == candidate and y, board, cond)) == cond:
#                 return candidate
#     if all([place != Symbol.E for place in board]):
#         return Symbol.E
#     return None


if __name__ == "__main__":
    new_game()
    p = Dot(7, 2)
    print(Dot._board_size)
    print(p._board_size)
    print(p.dots)
