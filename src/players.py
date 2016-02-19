import random
from abc import ABCMeta, abstractmethod
import rules
from utils import Hashable


class Player(object):
    """Abstract base class for players"""
    __metaclass__ = ABCMeta

    def __init__(self, side, logger):
        """
        Constructor

        :param side: rules.NOUGHTS or rules.CROSSES
        :type side: int
        """
        self.side = side
        self.logger = logger

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

    def start(self):
        """
        This method is called before the game starts. It gives the player a
        chance to do any initialisation required before the game.
        """
        pass

    def finish(self, won):
        """
        This method is called when the game has finished. It gives the player a
        chance to respond to the outcome of the game.

        :param won: boolean specifying whether the game was won or lost
        :type won: bool
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


class ReinforcementAgent(Player):
    """Agent that uses reinforcement learning to determine values for moves"""
    DEFAULT_VALUE = 0.5
    MAX_VALUE = 1.0
    MIN_VALUE = 0.0

    # Agent states
    EXPLOITING = 0
    EXPLORING = 1

    def __init__(self, side, logger):
        super(ReinforcementAgent, self).__init__(side, logger)

        # Dict of state values; key is table at state, value is probability that
        # state will lead to a winning move
        self.state_values = {}

        # List of moves in the current game, used to make value assessments
        # Each move is recorded as a board state
        self.move_states = []

        # The agent state, dictates the method used to choose the next move
        self.state = self.EXPLOITING

    def value(self, state):
        """
        Looks up the given state in the list of known state values.

        :return: value of the state if known, otherwise None
        :rtype: float
        """
        # Wrap the state so it can be used as a key in the values dictionary
        hashable = Hashable(state)
        if hashable in self.state_values:
            return self.state_values[hashable]
        else:
            return None

    def set_value(self, state, value):
        """
        Sets the value of the given state in the list of known state values.

        :param state: two dimensional array representing the board state
        :type state: numpy.ndarray
        :param value: value of the state
        :type value: float
        """
        # Wrap the state so it can be used as a key in the values dictionary
        hashable = Hashable(state)
        self.state_values[hashable] = value

    def check_cell(self, cell, board):
        """
        Checks whether the specified cell represents a win or loss state and
        assigns a value accordingly. States that have not been seen before are
        given a default value.

        :param cell: a tuple with the coordinates of the new move (x, y)
        :type cell: (int, int)
        :param board: two dimensional array representing the current board
        :type board: numpy.ndarray
        :return: the value of state represented by
        """
        cell = tuple(cell)
        board = board.copy()

        # Check if this is a winning move for the current player
        board[cell] = self.side
        if rules.winning_move(board, cell):
            # Automatically assign maximum value to winning states
            self.set_value(board, self.MAX_VALUE)
            self.logger.debug("Winning state, value set to maximum")
            return self.MAX_VALUE

        """
        Do we care if this could be a winning move for the opponent?
        We could give every other move in the list a zero?
        """
        # # Check if this is a winning move for the opponent
        # board[cell] = rules.opponent(self.side)
        # if rules.winning_move(board, cell):
        #     self.set_value(board, self.MIN_VALUE)
        #     self.logger.debug("Losing state, value set to minimum")
        #     return self.MIN_VALUE

        # Set the default value if the state has no value
        board[cell] = self.side
        if not self.value(board):
            self.set_value(board, self.DEFAULT_VALUE)
            self.logger.debug("State not in list, value set to default")
            return self.DEFAULT_VALUE

        return self.value(board)

    def move(self, board):
        """
        During game, each move:
        1. Iterate through possible moves (empty_cells) and look up in states
        2. States that include a full row are automatically assigned value=1.0
           States where the opponent wins are assigned value=0.0
           - This happens before the move is selected
        3. Choose either highest value (exploit) or random other cell (explore)
            - could use weighted function (bias?) to choose, never choose 0/1
        4. Record move/state for later

        After win:
        Increase the value of each recorded move/state for that game (we are
        more likely to win from these states)

        After lose or draw:
        Decrease the value of each recorded move/state (we are move likely to
        lose or draw from these states)
        """
        # Look up possible moves in known state values list
        empty_cells = rules.empty_cells(board)
        moves = []  # [(cell, value)]
        for cell in empty_cells:
            moves.append(cell, self.check_cell(cell, board))
        # Sort moves by value so we can choose first for exploit

        # Choose either highest value (exploit) or random cell (explore)
        if self.state == self.EXPLOITING:
            # Choose the cell that has the highest value
            cell = tuple(moves[0])
        elif self.state == self.EXPLORING:
            # Choose a random cell that does not have the highest value
            i = random.randint(1, len(moves) - 2)
            cell = tuple(moves[i])
        else:
            raise ValueError("State is unexpected value: {0}".format(
                self.state))

        # Record move state for later TODO: why aren't we storing hashable here?
        move_state = board.copy()
        move_state[cell] = self.side
        self.move_states.append(move_state)

        return cell

    def start(self):
        """
        This method is called before the game starts. It gives the player a
        chance to do any initialisation required before the game.
        """
        # Clear the list of recorded moves
        self.move_states = []

    def finish(self, won):
        """
        This method is called when the game has finished. It gives the player a
        chance to process to the outcome of the game.

        TODO: do we need the final board state? in case the other player won
        so we can mark it as value = 0.0? or is this done during move()
        # :param board: final state of the game board
        :param won: boolean specifying whether the game was won or lost
        :type won: bool
        """
        # Iterate through the list of moves and assign a value for each one
        # according to the game outcome
        for move_state in self.move_states:
            # Look the state up in the state values dictionary
            value = self.value(move_state)

            # Give the state a default value if not known previously
            if not value:
                self.set_value(move_state, self.DEFAULT_VALUE)

            # TODO: Increase or decrease the state value depending on the game outcome
            if won:
                self.set_value(move_state, value + 0.1)
            else:
                self.set_value(move_state, value - 0.1)
