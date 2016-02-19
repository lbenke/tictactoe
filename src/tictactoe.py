from players import *
import rules
import mpl_plot
import numpy as np
import logging
import sys


class TicTacToe(object):
    # TODO: make this a generic game engine and encapslate ttt rules in rules.py
    # n player by having a list and iterating through it (n=2 for ttt)
    def __init__(self, n, player1_class, player2_class,
            log_level=logging.DEBUG):
        # Set up logger
        self.logger = logging.getLogger()
        logging.basicConfig(stream=sys.stdout, level=log_level,
                            format="\n%(message)s")

        # Initialise the board and players
        self.board = np.zeros((n, n))
        self.player1 = player1_class(rules.NOUGHT, self.logger)
        self.player2 = player2_class(rules.CROSS, self.logger)

    def run(self):
        # Reset the game board
        self.board.fill(rules.EMPTY)

        # Notify the players that the game is starting
        self.player1.start()
        self.player2.start()

        # Play the game
        winner = self.play()

        # Notify the players that the game has finished
        self.player1.finish(winner)
        self.player2.finish(winner)

    def play(self):
        """
        Plays the game, alternative turns between the players.

        :return: the winning player, or False if nobody has won
        """
        player = self.player1

        while True:
            self.logger.debug(self.board_str())

            # Get the coordinates of the player's move
            move = player.move(self.board)

            # Make the move if it is valid
            if list(move) in rules.empty_cells(self.board).tolist():
                self.board[move] = player.side
            else:
                # Not a valid move since not in list of empty cells
                self.logger.fatal("Invalid move")
                sys.exit()

            # Check for a win or draw
            if rules.winning_move(self.board, move):
                self.logger.info("Game over: {0} win \n{1}".format(
                        rules.side_name(player.side), self.board_str()))
                # Return winning player
                return player
            elif rules.draw(self.board):
                self.logger.info("Game over: draw \n{0}".format(self.board_str()))
                # Return None for draw (no winning player)
                return None

            # Change player
            player = self.player2 if player is self.player1 else self.player1

    def board_str(self):
        """ Formats the board state as a string replacing cell values with
        enum names """
        # Join columns using '|' and rows using line-feeds
        return str('\n'.join(['|'.join([rules.token(item) for item in row])
                for row in self.board]))


if __name__ == "__main__":
    ttt = TicTacToe(3, ReinforcementAgent, Agent04, logging.INFO)

    for _ in range(0, 3):
        ttt.run()

    # mpl_plot.plot_board(ttt.board)
