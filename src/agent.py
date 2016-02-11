import random
import numpy as np
from abc import ABCMeta, abstractmethod
import rules


# Abstract base class for agents
class Agent(object):
    __metaclass__ = ABCMeta

    def __init__(self, player_name, side):
        self.player_name = player_name
        self.side = side  # NOUGHT or CROSS

    def __str__(self):
        return self.player_name

    @abstractmethod
    def move(self, board):
        """
        Returns the coordinates of the move the current player selects given the
        current board state.

        :param board: two dimensional array representing the current board
        :type board: numpy.ndarray
        :return: a tuple with the coordinates of the new move (x, y)
        """
        pass


# Agent that selects the first empty cell
class Agent01(Agent):
    def move(self, board):
        # Select the first empty cell
        empty_cells = rules.empty_cells(board)
        cell = empty_cells[0]
        return tuple(cell)


# Agent that selects an empty cell at random
class Agent02(Agent):
    def move(self, board):
        # Select an empty cell at random
        empty_cells = rules.empty_cells(board)
        cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
        return tuple(cell)


# Agent that checks for a winning move
class Agent03(Agent):
    def move(self, board):
        empty_cells = rules.empty_cells(board)

        # Check if any of the empty cells represents a winning move
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = self.side
            if rules.winning_move(new_board, cell):
                return cell
        else:
            # Otherwise pick a random cell
            cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
            return tuple(cell)


# Agent that checks for a winning move for itself, and blocks winning moves for
# its opponent.
class Agent04(Agent):
    def move(self, board):
        empty_cells = rules.empty_cells(board)

        # Check if any of the empty cells represents a winning move
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = self.side
            if rules.winning_move(new_board, cell):
                return cell
        # Check if any of the empty cells represents a winning move for the
        # other player, if so block it
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = -self.side
            if rules.winning_move(new_board, cell):
                print "Blocked ", cell
                return cell
        else:
            # Otherwise pick a random cell
            cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
            return tuple(cell)
