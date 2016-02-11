"""
This module contains methods relating to the rules of the game.
"""
import numpy as np


class Sides(object):
    EMPTY = 0
    NOUGHT = 1
    CROSS = -1
    __tokens = {EMPTY: " ", NOUGHT: "o", CROSS: "x"}

    # Returns the game token for a state given its value
    @staticmethod
    def token(value):
        try:
            return Sides.__tokens[value]
        except KeyError:
            return "?"


def empty_cells(board):
    # TODO: convert to array of tuples for easier use
    return np.transpose(np.nonzero(board == Sides.EMPTY))


"""
Checks whether the given move results in a win.

:param board: board state after the move has been mad
:param move: a tuple with the coordinates of the new move (x, y)
:type board: numpy.ndarray
:type move: (int, int)
:return: True if move results in a win, False otherwise
"""
def winning_move(board, move):
    side = board[move]
    n = board.shape[0]
    x, y = move
    full = abs(side * n)

    # Check row
    if abs(board[x].sum()) == full:
        return True
    # Check column
    elif abs(board[:,y].sum()) == full:
        return True
    # Check diagonal
    elif x == y and abs(board.diagonal().sum()) == full:
        return True
    # Check anti-diagonal
    elif x == (n - 1) - y and abs(np.fliplr(board).diagonal().sum()) == full:
        return True
    else:
        return False


"""
Checks whether the given move results in a draw.

:param board: board state after the move has been made
:param move: a tuple with the coordinates of the new move (x, y)
:type board: numpy.ndarray
:type move: (int, int)
:return: True if move results in a draw, False otherwise
"""
def draw(board, move):
    if not Sides.EMPTY in board:
        # Board is full so game is a draw
        return True
    else:
        return False