"""
This module contains methods defining the rules of the game.
"""
import numpy as np
import rules


EMPTY = 0
NOUGHT = 1
CROSS = -1
sides = [CROSS, NOUGHT]
__tokens = {EMPTY: " ", NOUGHT: "o", CROSS: "x"}
__names = {EMPTY: " ", NOUGHT: "Noughts", CROSS: "Crosses"}


def token(value):
    """Returns the game token for a value"""
    try:
        return __tokens[value]
    except KeyError:
        return "?"


def side_name(value):
    """Returns the side name for a value"""
    try:
        return __names[value]
    except KeyError:
        return "?"


def opponent(side):
    """Returns the side of the opponent"""
    return -side


def empty_cells(board):
    """
    Returns a list of empty cells remaining on a board.

    :param board: two dimensional array representing the current board
    :type board: numpy.ndarray
    :return: array containing the locations of empty cells as x,y pairs
    :rtype: numpy.ndarray
    """
    # Get list of empty cells and transpose into list of x,y pairs
    return np.transpose(np.nonzero(board == rules.EMPTY))


def valid_move(board, move):
    """
    Returns whether the move is valid for the given board, i.e. whether it is
    one of the empty cells.

    Params:
        board (numpy.ndarray):
        move ((int, int)): tuple with the coordinates of the new move (x, y)

    Returns:
        bool: True if the move is valid, False otherwise
    """
    return list(move) in rules.empty_cells(board).tolist()


def winning_move(board, move):
    """
    Checks whether the given move results in a win.

    Calculates the sum of the row, column and diagonals of the new move and
    compares against the expected value for a full line.

    :param board: two dimensional array representing the board after the move
    :type board: numpy.ndarray
    :param move: tuple with the coordinates of the new move (x, y)
    :type move: (int, int)
    :return: True if move results in a win, False otherwise
    :rtype: bool
    """
    # A full line sums to n or -n if the sides are 1 and -1
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
    :rtype: bool
    """
    if EMPTY in board:
        return False
    else:
        # Board is full so game is a draw
        return True


def board_str(board):
        """ Formats a board state as a string replacing cell values with
        enum names """
        # Join columns using '|' and rows using line-feeds
        return str('\n'.join(['|'.join([rules.token(item) for item in row])
                for row in board]))
