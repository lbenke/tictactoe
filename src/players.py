import random
from abc import ABCMeta, abstractmethod
import rules
from hashlib import sha1
from numpy import all, array, uint8


class Player(object):
    """Abstract base class for players"""
    __metaclass__ = ABCMeta

    def __init__(self, side, logger):
        """
        Constructor

        :param side: Sides.noughts or Sides.crosses
        :type side: int
        """
        self.side = side
        self.logger = logger

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


class Human(Player):
    """Player for human input via the command line"""
    def move(self, board):
        return tuple(map(int,raw_input("Cell (row, column): ").split(',')))


class Agent01(Player):
    """Agent that selects the first empty cell"""
    def move(self, board):
        # Select the first empty cell
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[0])


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
                self.logger.debug("Blocked {0}".format(cell))
                return cell
        else:
            # Otherwise pick a random cell
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class Hashable(object):
    """
    Hashable wrapper for ndarray objects.

    Instances of ndarray are not hashable, meaning they cannot be added to
    sets, nor used as keys in dictionaries. This is by design - ndarray
    objects are mutable, and therefore cannot reliably implement the
    __hash__() method.

    The hashable class allows a way around this limitation. It implements
    the required methods for hashable objects in terms of an encapsulated
    ndarray object. This can be either a copied instance (which is safer)
    or the original object (which requires the user to be careful enough
    not to modify it).

    Source: http://machineawakening.blogspot.com.au/
    """
    def __init__(self, wrapped, tight=True):
        """
        Creates a new hashable object encapsulating an ndarray.

        :param wrapped: the wrapped ndarray
        :param tight: optional; if True a copy of the input ndaray is created
        """
        self.__tight = tight
        self.__wrapped = array(wrapped) if tight else wrapped
        self.__hash = int(sha1(wrapped.view(uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

    def unwrap(self):
        """
        Returns the encapsulated ndarray.

        If the wrapper is "tight", a copy of the encapsulated ndarray is
        returned. Otherwise, the encapsulated ndarray itself is returned.
        """
        if self.__tight:
            return array(self.__wrapped)

        return self.__wrapped


class ReinforcementAgent01(Player):
    """Agent that uses reinforcement learning to determine values for moves"""
    DEFAULT_VALUE = 0.5

    def __init__(self, side, logger):
        super(ReinforcementAgent01, self).__init__(side, logger)

        self.states = {}  # key is table at state


    def move(self, board):
        hashable = Hashable(board)
        if hashable in self.states:
            self.logger.info("State in list: {0}".format(self.states[hashable]))
            # Adjust value
            self.states[hashable] += 0.1
        else:
            self.logger.debug("State not in list")
            self.states[hashable] = self.DEFAULT_VALUE
        # Choose a random empty cell
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])