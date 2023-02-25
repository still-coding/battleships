#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""UI and main loop module"""


from time import sleep

from curtsies import FSArray, FullscreenWindow, Input, fsarray
from curtsies.fmtfuncs import blue, bold, green, on_blue, on_red, red
from termtables import to_string as make_termtable

import game_classes
from config import BOARD_SIZE, SHIPS



brd = game_classes.Board()
# brd2 = game_classes.Board()

from game import Game

game = Game()
# r = g.random_board()
# while not r:
#     r = g.random_board()


# brd2 = g.ai_board

# def get_board_image(
#     left_board, cur_pos, right_board=None, warn=False, current_ship=None
# ):
#     header = [bold(blue(letter)) for letter in ascii_uppercase[: left_board.size]]

#     if not right_board:
#         lines = [header + [bold(blue("#"))]]
#         cells = left_board.cells
#         for i, row in enumerate(cells):
#             str_line = []
#             for j, cell in enumerate(row):
#                 if cur_pos.row == i and cur_pos.col == j:
#                     str_line.append(
#                         on_red(SYMBOL_MAPPING[cell])
#                         if warn
#                         else on_blue(SYMBOL_MAPPING[cell])
#                     )
#                 else:
#                     str_line.append(SYMBOL_MAPPING[cell])
#             str_line.append(bold(blue(str(i))))
#             lines.append(str_line)

#         if current_ship:
#             lines[current_ship.start.row + 1][current_ship.start.col] = (
#                 red(SYMBOL_MAPPING[game_classes.Symbol.Ship])
#                 if warn
#                 else green(SYMBOL_MAPPING[game_classes.Symbol.Ship])
#             )
#             for d in current_ship.dots[1:]:
#                 lines[d.row + 1][d.col] = (
#                     red(SYMBOL_MAPPING[game_classes.Symbol.Ship])
#                     if warn
#                     else green(SYMBOL_MAPPING[game_classes.Symbol.Ship])
#                 )
#         return make_termtable(lines).split("\n")

#     lines = [header + ["#"] + header]
#     cells = left_board.cells

#     for i, (rowl, rowr) in enumerate(zip(cells, right_board.cells)):
#         str_line = []
#         for j, cell in enumerate(rowl):
#             if cur_pos.row == i and cur_pos.col == j:
#                 str_line.append(
#                     on_red(SYMBOL_MAPPING[cell])
#                     if warn
#                     else on_blue(SYMBOL_MAPPING[cell])
#                 )
#             else:
#                 str_line.append(SYMBOL_MAPPING[cell])
#         str_line.append(str(i))
#         str_line.extend(map(lambda x: SYMBOL_MAPPING[x], rowr))
#         lines.append(str_line)
#     return make_termtable(lines).split("\n")


# def game_over_message(winner):
#     """Gives game over message (win, lose or draw).

#     Args:
#         winner (Symbol): Winner symbol

#     Returns:
#         FmtStr: Colored game over message
#     """
#     if winner == game.player_symbol:
#         return green("You have vanquished your foe! Congratulations!")
#     if winner == game.ai_symbol:
#         return red("You have been defeated by AI! Good luck next time!")
#     return blue("It's a draw! Not bad!")


def main():
    """Main game loop and UI draw logic. Very bloated. -_-"""

    game.greet()
    game.arrange_user_ships()
    game.loop()

    # with FullscreenWindow() as window:
    #     with Input() as input_generator:
    #         # welcome screen
    #         welcome_message = [
    #             bold(blue("Welcome to BATTLESHIPS game!")),
    #             "* At first - you need to place your ships on the game board.",
    #             "* After that - get ready to battle against AI.",
    #             "In order to win you need to sink all of your opponent's ships.",
    #             "Good luck!",
    #             f"Press {bold('any key')} to start.",
    #         ]
    #         window.render_to_terminal(welcome_message)
    #         for c in input_generator:
    #             break

    #         # ship arrangement
    #         total_ships = sum(i["count"] for i in SHIPS)
    #         current_ship = 1
    #         esc_pressed = False
    #         for ship_data in SHIPS:
    #             for _ in range(ship_data["count"]):
    #                 ship = game_classes.Ship(
    #                     length=ship_data["size"], name=ship_data["name"]
    #                 )

    #                 arrange_message = [
    #                     blue("Arrange your battleships on the game board."),
    #                     "Controls:",
    #                     f'> {bold("[↑] [↓] [←] [→]")} to move ship',
    #                     f'> {bold("[Space]")} to rotate ship',
    #                     f'> {bold("[Enter]")} to place ship and continue',
    #                     f'> {bold("[Esc]")} to exit game',
    #                     f"Current ship: {ship.name}, {current_ship} of {total_ships}",
    #                     "",
    #                     green("Your board".center(brd.size * 4)),
    #                 ]

    #                 warning_draw = not all(map(brd.isempty, ship.dots))
    #                 window.render_to_terminal(
    #                     arrange_message
    #                     + get_board_image(
    #                         brd, ship.start, warn=warning_draw, current_ship=ship
    #                     )
    #                 )
    #                 for c in input_generator:
    #                     can_rotate = True
    #                     if c == "<ESC>":
    #                         esc_pressed = True
    #                         break
    #                     if c == "<RIGHT>":
    #                         if ship.start.col < brd.size - ship.length * (
    #                             ship.direction == game_classes.ShipDirection.Horizontal
    #                         ):
    #                             ship.start.right()
    #                     if c == "<LEFT>":
    #                         ship.start.left()
    #                     if c == "<UP>":
    #                         ship.start.up()
    #                     if c == "<DOWN>":
    #                         if ship.start.row < brd.size - ship.length * (
    #                             ship.direction == game_classes.ShipDirection.Vertical
    #                         ):
    #                             ship.start.down()
    #                     if c == "<SPACE>":
    #                         if (
    #                             ship.start.row < brd.size - ship.length + 1
    #                             and ship.start.col < brd.size - ship.length + 1
    #                         ):
    #                             ship.rotate()
    #                         else:
    #                             can_rotate = False
    #                     if c == "<Ctrl-j>":
    #                         if all(map(brd.isempty, ship.dots)):
    #                             brd.add_ship(ship)
    #                             current_ship += 1
    #                             break
    #                     warning_draw = not all(map(brd.isempty, ship.dots))
    #                     window.render_to_terminal(
    #                         arrange_message
    #                         + get_board_image(
    #                             brd,
    #                             ship.start,
    #                             warn=warning_draw or not can_rotate,
    #                             current_ship=ship,
    #                         )
    #                     )
    #                 if esc_pressed:
    #                     break
    #             if esc_pressed:
    #                 break
    #         brd.mode = "play"
    #         brd.update()
    #         # play
    #         if not esc_pressed:
    #             play_message = [
    #                 blue("Sink your opponent's ships. Shoot accurately!"),
    #                 "Controls:",
    #                 f'> {bold("[↑] [↓] [←] [→]")} to move cursor',
    #                 f'> {bold("[Space]")} to shoot',
    #                 f'> {bold("[Esc]")} to exit game',
    #                 "",
    #                 f'{red("Enemy board".center(brd.size * 4))} {green("Your board".center(brd.size * 4))}',
    #             ]

    #             crosshair = game_classes.Dot()
    #             window.render_to_terminal(
    #                 play_message + get_board_image(brd2, crosshair, brd)
    #             )

    #             for c in input_generator:
    #                 can_rotate = True
    #                 if c == "<ESC>":
    #                     break
    #                 if c == "<RIGHT>":
    #                     crosshair.right()
    #                 if c == "<LEFT>":
    #                     crosshair.left()
    #                 if c == "<UP>":
    #                     crosshair.up()
    #                 if c == "<DOWN>":
    #                     crosshair.down()
    #                 if c == "<SPACE>":
    #                     pass
    #                 window.render_to_terminal(
    #                     play_message + get_board_image(brd2, crosshair, brd)
    #                 )


if __name__ == "__main__":
    main()
