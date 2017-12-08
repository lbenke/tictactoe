"""
This module contains the core TicTacToe simulation class, along with a main 
method to run the game with a human and agent player.
"""

from itertools import cycle
import rules
import numpy as np
import logging
import random
import sys


class TicTacToe(object):
    """
    This class simulates Tic-Tac-Toe (Noughts and Crosses) of size n x n.

    It provides the simulation engine to model the flow of a single game,
    requesting moves from each player in turn and storing the state of the game
    board.

    Attributes:
        board (numpy.ndarray): two dimensional array representing the game board
        players ([Player]): list of game players
        logger (logging.Logger): logger
    """
    def __init__(self, players, n=3, shuffle=False, logger=None):
        # Initialise the board and players
        self.board = np.zeros((n, n))
        self.logger = logger
        self.shuffle = shuffle
        self.set_players(players)

    def set_players(self, players):
        """
        Sets the game players.

        The current game players are replaced with the players specified. Each
        player is assigned a side from the list specified in the rules module.
        The number of players must match the number of sides.

        Args:
            players ([Player]): the list of players

        Raises:
            ValueError: if `players` is not the same length as `rules.sides`
        """
        if len(players) != len(rules.sides):
            raise ValueError("Incorrect number of players, expected {0}.".
                    format(len(rules.sides)))

        if self.shuffle:
            random.shuffle(players)

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

    def player(self, side):
        """
        Returns the player with the specified side.
        
        Args:
            side (int): the side of the player
             
        Returns:
            Player: the player matching the side, or None 
        """
        for player in self.__players:
            if player.side == side:
                return player

        # No player found with the given side
        return None

    def run(self, board=None):
        """
        Executes a single run of the game.

        The board is initially set to empty, then the play method is called to
        request moves from each player until a winner is identified.

        The players are notified that the game is about to start, and again once
        the game has finished.
                        
        Args:
            board (numpy.ndarray): optional two dimensional array representing 
                the initial game board

        Returns:
            int: the side of the winning player, or None if there was a draw
        """
        # Use initial board state if provided
        if board is not None:
            self.board = board
        else:
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
        if self.shuffle:
            random.shuffle(self.players())

        player_cycle = cycle(self.players())

        # Request moves from each player until there is a win or draw
        for player in player_cycle:
            # Uncomment to log board state each turn
            # if self.logger:
            #     self.logger.debug(rules.board_str(self.board))

            # Check for a win or draw
            winning_side = rules.winner(self.board)
            if winning_side is not None:
                winner = self.player(winning_side)
                if self.logger:
                    self.logger.info("{2}\nGame over: {0} win ({1})".format(
                            rules.side_name(winning_side),
                            type(winner).__name__, rules.board_str(self.board)))
                # Return the side of the winning player
                return winning_side
            elif rules.board_full(self.board):
                # The board is full so the game concluded with a draw
                if self.logger:
                    self.logger.info("{0}\nGame over: Draw".format(
                        rules.board_str(self.board)))
                # Return None for a draw
                return None

            # Request a move from the player
            move = player.move(self.board.copy())

            # Apply the move if it is valid
            if rules.valid_move(self.board, move):
                self.board[move] = player.side
            else:
                if self.logger:
                    self.logger.fatal("Invalid move")
                raise ValueError("Not a valid move: {0}".format(move))


def main():
    # Set up the logger
    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
            format="\n%(message)s")

    # Create the players
    from players import Human
    human = Human(logger=logger)
    from agents.minimax import MiniMaxAgent
    agent = MiniMaxAgent(logger=logger)

    # Run the game
    game = TicTacToe([human, agent], shuffle=True, logger=logger)
    while True:
        game.run()


if __name__ == "__main__":
    main()
