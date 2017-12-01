"""
This module defines the base class that is inherited when implementing a 
TicTacToe player. It also includes a Human player for command line input, and a 
number of simple hand-coded agents for testing. More complex agents should be 
defined in the `agents` subpackage.
"""

import random
from abc import ABCMeta, abstractmethod
import rules


class Player(object):
    """
    Abstract base class for players.

    This class represents the template for game players, including both humans
    and agents.

    Attributes:
        side (int): the player side, defined in the game rules
        logger (logging.Logger): logger
    """
    __metaclass__ = ABCMeta

    def __init__(self, side=None, logger=None):
        """
        Constructor for the class.

        Args:
            side (int): the player side, defined in the game rules
        """
        self.side = side
        self.logger = logger

    @abstractmethod
    def move(self, board):
        """
        Returns the coordinates of the move the current player selects given the
        current board state.

        Args:
            board (numpy.ndarray): two dimensional array representing the game board

        Returns:
            (int, int): tuple with the coordinates of the new move (x, y)
        """
        pass

    def start(self):
        """
        Called before the game starts.

        This method gives the player a chance to do any initialisation required
        before the game.
        """
        pass

    def finish(self, won):
        """
        This method is called when the game has finished. It gives the player a
        chance to respond to the outcome of the game.

        Args:
            won (bool): boolean specifying whether the game was won or lost
        """
        pass


class Human(Player):
    """
    Player for human input via the command line.
        
    Moves are specified using numpad 1-9 (1 is the bottom left cell and 9 is the
    top right).
    """
    def move(self, board):
        print "\n{}".format(rules.board_str(board))
        while True:
            try:
                num = int(raw_input("Cell (1-9): "))
                if num not in range(1, 10):
                    continue
                cell = (int((9 - num) / 3), (num - 1) % 3)
            except ValueError:
                continue
            if rules.valid_move(board, cell):
                return cell


class FirstEmptyCellAgent(Player):
    """Agent that selects the first empty cell."""
    def move(self, board):
        # Select the first empty cell
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[0])


class RandomCellAgent(Player):
    """Agent that selects an empty cell at random."""
    def move(self, board):
        # Select an empty cell at random
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class WinRandomCellAgent(Player):
    """Agent that checks for a winning move."""
    def move(self, board):
        empty_cells = rules.empty_cells(board)

        # Check if any of the empty cells represents a winning move
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = self.side
            if rules.winning_move(new_board):
                return cell
        else:
            # Otherwise pick a random cell
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class WinBlockRandomCellAgent(Player):
    """Agent that checks for a winning move for itself, and blocks winning
    moves for its opponent."""
    def move(self, board):
        empty_cells = rules.empty_cells(board)

        # Check if any of the empty cells represents a winning move
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = self.side
            if rules.winning_move(new_board):
                return cell

        # Check if any of the empty cells represents a winning move for the
        # other player, if so block it
        for cell in empty_cells:
            cell = tuple(cell)
            new_board = board.copy()
            new_board[cell] = -self.side
            if rules.winning_move(new_board):
                if self.logger:
                    self.logger.debug("Blocked {0}".format(cell))
                return cell

        else:
            # Otherwise pick a random cell
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class OptimalRulesAgent(Player):
    """
    Agent that makes the optimal move using a set of predefined rules. This 
    agent blocks forks (including double forks) and should always win or draw.
    """
    def move(self, board):
        raise NotImplementedError()
        return None;
