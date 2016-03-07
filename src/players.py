from numpy.random import choice
import numpy as np
import random
from abc import ABCMeta, abstractmethod
import rules
from collections import OrderedDict


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

        Params:
            side (int): the player side, defined in the game rules
        """
        self.side = side
        self.logger = logger

    @abstractmethod
    def move(self, board):
        """
        Returns the coordinates of the move the current player selects given the
        current board state.

        Params:
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

        Params:
            won (bool): boolean specifying whether the game was won or lost
        """
        pass


class Human(Player):
    """Player for human input via the command line."""
    def move(self, board):
        print "\n{}".format(rules.board_str(board))
        while True:
            try:
                move = tuple(map(int,raw_input("Cell (row, col): ").split(',')))
            except ValueError:
                continue
            if rules.valid_move(board, move):
                return move


class Agent01(Player):
    """Agent that selects the first empty cell."""
    def move(self, board):
        # Select the first empty cell
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[0])


class Agent02(Player):
    """Agent that selects an empty cell at random."""
    def move(self, board):
        # Select an empty cell at random
        empty_cells = rules.empty_cells(board)
        return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class Agent03(Player):
    """Agent that checks for a winning move."""
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
    moves for its opponent."""
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
                if self.logger:
                    self.logger.debug("Blocked {0}".format(cell))
                return cell
        else:
            # Otherwise pick a random cell
            return tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])


class ReinforcementAgent(Player):
    """
    Agent that uses reinforcement learning to determine values for moves.

    This agent records the state after each move it plays, and adjusts the
    values for all moves in each game depending on the game outcome.

    Moves are usually selected greedily, where the move with the highest value
    is selected. Occasionally the agent explores, randomly selecting a different
    move.

    During game, each move:
        1. Iterate through possible moves (empty_cells) and look up in states
        2. Choose either highest value (exploit) or random other cell (explore)
        3. Record move state for later

    After a win:
        Increase the value of each recorded move/state for that game (we are
        more likely to win from these states)

    After a loss or draw:
        Decrease the value of each recorded move/state (we are move likely to
        lose or draw from these states)
    """
    # Reinforcement learning parameters
    STEP_SIZE = 0.25  # step size parameter influences the rate of learning
    DEFAULT_VALUE = 0.5  # value given to new states
    MAX_VALUE = 1.0  # states with this value represent a win
    DRAW_VALUE = 0.75  # draw states move toward this value
    MIN_VALUE = 0.0  # states with this value represent a loss
    BIAS = 0.1  # the probability that the agent will explore during a move

    # Agent states
    EXPLOITING = 111
    EXPLORING = 222

    def __init__(self, side=None, logger=None):
        super(ReinforcementAgent, self).__init__(side, logger)

        # Dict of state values where state_values[state_hash] is (state, value)
        self.state_values = OrderedDict()

        # List of moves in the current game, used to make value assessments
        # Each move is recorded as a board state
        self.move_states = []

        # The agent state, dictates the method used to choose the next move
        self.state = self.EXPLOITING

    def value(self, state):
        """
        Looks up the given state in the list of known state values.

        Returns:
            float: value of the state if known, otherwise None
        """
        state_hash = hash(str(state.data))
        if state_hash in self.state_values:
            state, value = self.state_values[state_hash]
            return value
        else:
            return None

    def set_value(self, state, value):
        """
        Sets the value of the given state in the list of known state values.

        Params:
            state (numpy.ndarray): two dimensional array representing the
                board state
            value (float): value of the state
        """
        # Create a hash of the state array to use as the dict key, then store
        # the value and state as a tuple in the dictionary
        state_hash = hash(str(state.data))
        self.state_values[state_hash] = (state, value)

    def state_values_list(self):
        """
        Returns the current list of recorded states and values.

        Returns:
            [(numpy.ndarray, float)]: a list of state-value pairs in the form
                [(state, value)]
        """
        return self.state_values.values()

    def move_value(self, move, board):
        """
        Checks whether the specified move would result in a win and returns a
        value accordingly. States that have not been seen before are given a
        default value. Note that no values are stored here.
        TODO: remove the win check and just get the state, remove this method?

        Params:
            move ((int, int)): tuple with the coordinates of the new move (x, y)
            board (numpy.ndarray): two dimensional array representing the board

        Returns:
            float: the value of the state after the move is applied
        """
        move = tuple(move)
        board = board.copy()
        board[move] = self.side

        # Check if this is a new state with no recorded value
        if not self.value(board):
            # Check if this is a winning move for the player
            if rules.winning_move(board, move):
                # Return maximum value to the state
                return self.MAX_VALUE
            else:
                return self.DEFAULT_VALUE

        return self.value(board)

    def move(self, board):
        # Look up the possible moves in the state values list
        empty_cells = rules.empty_cells(board)
        possible_moves = []  # [[cell, value]]
        for cell in empty_cells:
            possible_moves.append([cell, self.move_value(cell, board)])

        # Sort moves by value (last element has highest value)
        possible_moves = np.asarray(possible_moves)
        possible_moves = possible_moves[possible_moves[:,1].argsort()]

        # Choose move behaviour based on the bias probability
        # TODO: adjust bias down over time
        if random.random() < self.BIAS:
            self.state = self.EXPLORING
        else:
            self.state = self.EXPLOITING

        # Choose either highest value (exploit) or a random other cell (explore)
        if self.state == self.EXPLOITING or len(possible_moves) == 1:
            # Find the highest value and get all free cells with this value,
            # then choose one at random
            best_value = possible_moves[-1][1]
            best_cells = [x[0] for x in possible_moves if x[1] == best_value]
            i = random.randint(0, len(best_cells) - 1)
            cell = tuple(best_cells[i])
        elif self.state == self.EXPLORING:
            # Choose a random cell that does not have the highest value
            # TODO: weight other moves according to value?
            i = random.randint(0, len(possible_moves) - 2)
            cell = tuple(possible_moves[i][0])
        else:
            raise ValueError("State is unexpected value: {0}".format(
                self.state))

        # Record move state for later
        move_state = board.copy()
        move_state[cell] = self.side
        self.move_states.append(move_state)

        return cell

    def start(self):
        # Clear the list of recorded moves
        self.move_states = []

    def finish(self, winner):
        # Iterate through the list of moves and assign a value for each one
        # according to the game outcome
        for move_state in self.move_states:
            # Look the state up in the state values dictionary
            value = self.value(move_state)

            # Give the state a value if not known previously
            if not value:
                if move_state is self.move_states[-1] and winner:
                    # Assign maximum value to the last move if won
                    # TODO: remove this? let it figure this out itself?
                    value = self.MAX_VALUE
                    self.set_value(self.move_states[-1], value)
                else:
                    value = self.DEFAULT_VALUE
                    self.set_value(move_state, value)

            # Increase or decrease the state value depending on the game outcome
            if winner == self.side:
                final_value = self.MAX_VALUE
            elif winner is None:
                final_value = self.DRAW_VALUE
            else:
                final_value = self.MIN_VALUE

            # Adjust value toward the final value of the game
            # i.e. V(s) = V(s) + a[V(s') - V(s)]
            new_value = value + self.STEP_SIZE * (final_value - value)
            self.set_value(move_state, new_value)


class ReinforcementAgent2(Player):
    """
    Agent that uses reinforcement learning to determine values for moves.

    This version of the agent adjusts each state toward the value of the
    following move state rather than the final value of the game, so that good
    early moves are not drowned out by large numbers of bad final moves.

    Moves are selected using a weighted random function, such that potential
    moves with higher recorded values are more likely to be chosen.

    During game, each move:
        1. Iterate through possible moves (empty_cells) and look up in states
        2. Choose a cell using a weighted random function according to values
        3. Record move state for later

    After the game:
        Move the value of each move toward the value of the following move
    """
    # Reinforcement learning parameters
    STEP_SIZE = 0.25  # step size parameter influences the rate of learning
    DEFAULT_VALUE = 0.5  # value given to new states
    MAX_VALUE = 1.0  # states with this value represent a win
    DRAW_VALUE = 0.51  # draw states move toward this value
    MIN_VALUE = 0.0  # states with this value represent a loss
    BIAS = 0.1  # the probability that the agent will explore during a move

    def __init__(self, side=None, logger=None):
        super(ReinforcementAgent2, self).__init__(side, logger)

        # Dict of state values where state_values[state_hash] is (state, value)
        self.state_values = OrderedDict()

        # List of moves in the current game, used to make value assessments
        # Each move is recorded as a board state
        self.move_states = []

    def value(self, state):
        """
        Looks up the given state in the list of known state values.

        Returns:
            float: value of the state if known, otherwise None
        """
        state_hash = hash(str(state.data))
        if state_hash in self.state_values:
            state, value = self.state_values[state_hash]
            return value
        else:
            return None

    def set_value(self, state, value):
        """
        Sets the value of the given state in the list of known state values.

        Params:
            state (numpy.ndarray): two dimensional array representing the
                board state
            value (float): value of the state
        """
        # Create a hash of the state array to use as the dict key, then store
        # the value and state as a tuple in the dictionary
        state_hash = hash(str(state.data))
        self.state_values[state_hash] = (state, value)

    def state_values_list(self):
        """
        Returns the current list of recorded states and values.

        Returns:
            [(numpy.ndarray, float)]: a list of state-value pairs in the form
                [(state, value)]
        """
        return self.state_values.values()

    def move_value(self, move, board):
        """
        Checks whether the specified move would result in a win and returns a
        value accordingly. States that have not been seen before are given a
        default value. Note that no values are stored here.
        TODO: remove the win check and just get the state, remove this method?

        Params:
            move ((int, int)): tuple with the coordinates of the new move (x, y)
            board (numpy.ndarray): two dimensional array representing the board

        Returns:
            float: the value of the state after the move is applied
        """
        move = tuple(move)
        board = board.copy()
        board[move] = self.side

        # Check if this is a new state with no recorded value
        if not self.value(board):
            # Check if this is a winning move for the player
            if rules.winning_move(board, move):
                # Return maximum value to the state
                return self.MAX_VALUE
            else:
                return self.DEFAULT_VALUE

        return self.value(board)

    def move(self, board):
        # Look up the possible moves in the state values list
        empty_cells = rules.empty_cells(board)
        possible_moves = []  # [[cell, value]]
        for cell in empty_cells:
            possible_moves.append([cell, self.move_value(cell, board)])
        possible_moves = np.asarray(possible_moves)
        values = possible_moves[:,1]
        cells = possible_moves[:,0]

        # Choose an empty cell using a weighted random function
        weights = [w * 1.0 / sum(values) for w in values]  # normalise values
        weighted_choice = choice(cells, p=weights)
        move = tuple(weighted_choice)

        # Record move state for later
        move_state = board.copy()
        move_state[move] = self.side
        self.move_states.append(move_state)

        return move

    def start(self):
        # Clear the list of recorded moves
        self.move_states = []

    def finish(self, winner):
        # Iterate through the list of moves and assign a value for each one
        # according to the game outcome

        # Assign a value to the final state depending on the game outcome
        if winner == self.side:
            final_value = self.MAX_VALUE
        elif winner is None:
            final_value = self.DRAW_VALUE
        else:
            final_value = self.MIN_VALUE
        self.set_value(self.move_states[-1], final_value)

        # Iterate through the list of moves in reverse, adjusting values toward
        # the value of the following move
        for move_state in reversed(self.move_states[:-1]):
            # Adjust state value toward the following state value using
            # function V(s) = V(s) + a[V(s') - V(s)]
            value = self.value(move_state)
            if not value:
                value = self.DEFAULT_VALUE
            new_value = value + self.STEP_SIZE * (final_value - value)
            self.set_value(move_state, new_value)

        # for move_state in self.move_states:
        #     # Look the state up in the state values dictionary
        #     value = self.value(move_state)
        #
        #     # Give the state a value if not known previously
        #     if not value:
        #         if move_state is self.move_states[-1] and winner:
        #             # Assign maximum value to the last move if won
        #             # TODO: remove this? let it figure this out itself?
        #             value = self.MAX_VALUE
        #             self.set_value(self.move_states[-1], value)
        #         else:
        #             value = self.DEFAULT_VALUE
        #             self.set_value(move_state, value)
        #
        #         # value = self.DEFAULT_VALUE
        #         # self.set_value(move_state, value)
        #
        #     # Set the final value depending on the game outcome
        #     if winner == self.side:
        #         final_value = self.MAX_VALUE
        #     elif winner is None:
        #         final_value = self.DRAW_VALUE
        #     else:
        #         final_value = self.MIN_VALUE
        #
        #     # Adjust state value toward the final value of the game using
        #     # function V(s) = V(s) + a[V(s') - V(s)]
        #     new_value = value + self.STEP_SIZE * (final_value - value)
        #     self.set_value(move_state, new_value)