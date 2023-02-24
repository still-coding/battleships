# -*- coding: utf-8 -*-
"""Game logic module."""


from config import BOARD_SIZE, SHIPS
from game_classes import Dot, Board, ShipDirection, User, AI, Ship
from random import randint


class Game:
    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.player_board = Board(board_size)
        self.ai_board = Board(board_size)
        self.user = User(self.player_board, self.ai_board)
        self.ai = AI(self.ai_board, self.player_board)

    def random_board(self):
        self.ai_board = Board.random_ships_arrangement()
        


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
