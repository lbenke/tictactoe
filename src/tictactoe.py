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
        # TODO: maybe just pass in the actual objects and set player.side here?
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

        return winner

    def play(self):
        """
        Plays the game, alternative turns between the players.

        :return: the side of the winning player, or None if there was a draw
        """
        player = self.player1

        while True:
            self.logger.debug(rules.board_str(self.board))

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
                        rules.side_name(player.side), rules.board_str(
                        self.board)))
                # Return winning player
                return player.side
            elif rules.draw(self.board):
                self.logger.info("Game over: draw \n{0}".format(
                    rules.board_str(self.board)))
                # Return None for draw (no winning player)
                return None

            # Change player
            player = self.player2 if player is self.player1 else self.player1


if __name__ == "__main__":
    player1_class = ReinforcementAgent
    player2_class = ReinforcementAgent  #Agent03

    n = 3

    ttt = TicTacToe(n, player1_class, player2_class, logging.FATAL)
    # mpl_plot.plot_board(ttt.board)

    player1_wins = 0
    player2_wins = 0
    draws = 0
    played = 0

    for _ in range(0, 10000):
        winner = ttt.run()
        played += 1

        if not winner:
            draws += 1
        elif winner is ttt.player1.side:
            player1_wins += 1
        elif winner is ttt.player2.side:
            player2_wins += 1

    # Print the known states and associated values
    for k, v in ttt.player1.state_values.items():
        print "{0}\nValue: {1}\n".format(rules.board_str(k.unwrap()), v)

    # Print results
    print "Player 1: {0}\nPlayer 2: {1}\nDraw: {2}\nTotal: {3}".format(
        player1_wins, player2_wins, draws, played)
    print "Number of states stored: {0}".format(len(ttt.player1.state_values))

    """
    Upper bound on complexity (number of states) for a 3x3 board is 3^9 = 19,683
    (three states for each cell and nine cells).
    Excluding illegal moves (e.g. five noughts and no crosses), the number of
    possible states is 5478.
    Most of these are rotations or reflections of other states; excluding these
    gives 765 unique states.
    """