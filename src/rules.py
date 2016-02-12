"""
This module contains methods defining the rules of the game.
"""
import numpy as np


class Sides(object):
    empty = 0
    noughts = 1
    crosses = -1
    __tokens = {empty: " ", noughts: "o", crosses: "x"}

    @staticmethod
    def token(value):
        """Returns the game token for a state given its value"""
        try:
            return Sides.__tokens[value]
        except KeyError:
            return "?"

    @staticmethod
    def side_name(value):
        """Returns the name of the side given its value"""
        for x in Sides.__dict__:
            if Sides.__dict__[x] == value:
                return x


def empty_cells(board):
    """
    Returns a list of empty cells remaining on a board.

    :param board: two dimensional array representing the current board
    :type board: numpy.ndarray
    :return: array containing the locations of empty cells as x,y pairs
    :rtype: numpy.ndarray
    """
    # Get list of empty cells and transpose into list of x,y pairs
    return np.transpose(np.nonzero(board == Sides.empty))


def winning_move(board, move):
    """
    Checks whether the given move results in a win.

    Calculates the sum of the row, column and diagonals of the new move and compares
    against the expected value for a full line, n.

    :param board: two dimensional array representing the board after the move
    :type board: numpy.ndarray
    :param move: tuple with the coordinates of the new move (x, y)
    :type move: (int, int)
    :return: True if move results in a win, False otherwise
    :rtype: boolean
    """
    n = board.shape[0]
    x, y = move

    # Row
    if abs(board[x].sum()) == n:
        return True
    # Column
    elif abs(board[:,y].sum()) == n:
        return True
    # Diagonal
    elif x == y and abs(board.diagonal().sum()) == n:
        return True
    # Anti-diagonal
    elif x == (n - 1) - y and abs(np.fliplr(board).diagonal().sum()) == n:
        return True
    else:
        return False


def draw(board):
    """
    Checks whether the given move results in a draw.

    :param board: two dimensional array representing the board after the move
    :type board: numpy.ndarray
    :return: True if move results in a draw, False otherwise
    :rtype: boolean
    """
    if not Sides.empty in board:
        # Board is full so game is a draw
        return True
    else:
        return False