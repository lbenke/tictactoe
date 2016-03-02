from itertools import cycle
import cProfile
from players import *
import rules
import numpy as np
import logging
import sys


class TicTacToe(object):
    """
    This class simulates Tic-Tac-Toe (Noughts and Crosses) of size n.

    It provides the simulation engine to model the flow of a single game,
    requesting moves from each player in turn and storing the state of the game
    board.

    `Wikipedia <https://en.wikipedia.org/wiki/M,n,k-game>`_:
    An m,n,k-game is an abstract board game in which two players take turns in
    placing a stone of their color on an m*n board, the winner being the player
    who first gets k stones of their own color in a row, horizontally,
    vertically, or diagonally. Thus, tic-tac-toe is the 3,3,3-game and
    free-style gomoku is the 19,19,5-game. m,n,k-game is also called a
    k-in-a-row game on m*n board.

    Attributes:
        board (numpy.ndarray): two dimensional array representing the game board
        players ([Player]): list of game players
        logger (logging.Logger): logger
    """
    def __init__(self, n, players, logger=None):
        # Initialise the board and players
        self.board = np.zeros((n, n))
        self.__players = None
        self.set_players(players)
        self.logger = logger

    def set_players(self, players):
        """
        Sets the game players.

        The current game players are replaced with the players specified. Each
        player is assigned a side from the list specified in the rules module.
        The number of players must match the number of sides.

        Params:
            players ([Player]): the list of players

        Raises:
            ValueError: if `players` is not the same length as `rules.sides`
        """
        if len(players) != len(rules.sides):
            raise ValueError("Incorrect number of players, expected {0}.".
                    format(len(rules.sides)))
        for player, side in zip(players, rules.sides):
            player.side = side

        self.__players = players

    def players(self):
        """
        Returns the list of players.

        Returns:
            [Player]: the current list of game players
        """
        return self.__players

    def run(self):
        """
        Executes a single run of the game.

        The board is initially set to empty, then the play method is called to
        request moves from each player until a winner is identified.

        The players are notified that the game is about to start, and again once
        the game has finished.

        Returns:
            int: the side of the winning player, or None if there was a draw
        """
        # Reset the game board
        self.board.fill(rules.EMPTY)

        # Notify the players that the game is starting
        for player in self.players():
            player.start()

        # Play the game
        winner = self.play()

        # Notify the players that the game has finished
        for player in self.players():
            player.finish(winner)

        return winner

    def play(self):
        """
        Plays the game, alternating turns between the players.

        Moves are requested sequentially from each player in turn until there is
        a winner. The moves are checked for validity.

        Returns:
            int: the side of the winning player, or None if there was a draw
        """
        player_loop = cycle(self.players())

        for player in player_loop:
            # if self.logger:
            #     self.logger.debug(rules.board_str(self.board))

            # Get the coordinates of the player's move
            move = player.move(self.board)

            # Make the move if it is valid
            if list(move) in rules.empty_cells(self.board).tolist():
                self.board[move] = player.side
            else:
                # Not a valid move since it is not in the list of empty cells
                if self.logger:
                    self.logger.fatal("Invalid move")
                raise ValueError("Not a valid move: {0}".format(move))

            # Check for a win or draw
            if rules.winning_move(self.board, move):
                if self.logger:
                    self.logger.info("Game over: {0} win ({1})\n{2}\n".format(
                            rules.side_name(player.side),
                        type(player).__name__, rules.board_str(self.board)))
                # Return winning player
                return player.side
            elif rules.draw(self.board):
                if self.logger:
                    self.logger.info("Game over: draw \n{0}\n".format(
                        rules.board_str(self.board)))
                # Return None for draw
                return None


if __name__ == "__main__":
    # Set up the logger
    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.FATAL,
            format="\n%(message)s")

    # Set up the game
    n = 3
    player_1 = ReinforcementAgent(logger=logger)
    player_2 = ReinforcementAgent(logger=logger)
    game = TicTacToe(n, [player_1, player_2], logger)

    # Profiling start
    pr = cProfile.Profile()
    pr.enable()

    # Set up the MOEs
    player_1_wins = 0
    player_2_wins = 0
    draws = 0
    played = 0

    # Train agents over a large number of runs
    for _ in range(0, 40000):
        winner = game.run()

        played += 1
        if played % 1000 == 0:
            print played

        if not winner:
            draws += 1
        elif winner is player_1.side:
            player_1_wins += 1
        elif winner is player_2.side:
            player_2_wins += 1
        else:
            raise ValueError("Unexpected winner: {0}".format(winner))

    # Print the recorded states and associated values
    print "Player 1 state values:"
    for array, value in player_1.state_values_list():
        print "{0}\nValue: {1}\n".format(rules.board_str(array), value)

    # Print the training results
    print "Player 1: {0}\nPlayer 2: {1}\nDraw: {2}\nTotal: {3}".format(
        player_1_wins, player_2_wins, draws, played)
    print "Number of states stored Player 1: {0}".format(len(
        player_1.state_values))
    print "Number of states stored Player 2: {0}".format(len(
        player_2.state_values))

    # Profiling end
    pr.disable()
    pr.print_stats(sort='cumtime')

    # Insert a human player
    logger.setLevel(logging.INFO)
    player_2 = Human(logger=logger)
    game.set_players([player_1, player_2])
    while True:
        game.run()
