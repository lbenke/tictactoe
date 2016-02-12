import random
from abc import ABCMeta, abstractmethod
import rules


class Player(object):
    """Abstract base class for players"""
    __metaclass__ = ABCMeta

    def __init__(self, side):
        """
        Constructor

        :param side: Sides.noughts or Sides.crosses
        :type side: int
        """
        self.side = side

    def __str__(self):
        return rules.Sides.side_name(self.side)

    @abstractmethod
    def move(self, board):
        """
        Returns the coordinates of the move the current player selects given the
        current board state.

        :param board: two dimensional array representing the current board
        :type board: numpy.ndarray
        :return: a tuple with the coordinates of the new move (x, y)
        :rtype: (int, int)
        """
        pass


class Agent01(Player):
    """Agent that selects the first empty cell"""
    def move(self, board):
        # Select the first empty cell
        empty_cells = rules.empty_cells(board)
        cell = empty_cells[0]
        return tuple(cell)


class Agent02(Player):
    """Agent that selects an empty cell at random"""
    def move(self, board):
        # Select an empty cell at random
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class Agent03(Player):
    """Agent that checks for a winning move"""
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
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class Agent04(Player):
    """Agent that checks for a winning move for itself, and blocks winning
    moves for its opponent"""
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
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class Human(Player):
    """Player for human input via the command line"""
    def move(self, board):
        return tuple(map(int,raw_input("Cell: ").split(',')))
