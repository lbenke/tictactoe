from players import *
import rules
import mpl_plot
import numpy as np
import logging
import sys


class TicTacToe(object):
    def __init__(self, n, player1_class, player2_class, log_level=logging.DEBUG):
        self.logger = logging.getLogger()
        logging.basicConfig(stream=sys.stdout, level=log_level,
                            format="\n%(message)s")

        self.board = np.zeros((n, n))
        self.player_1 = player1_class(rules.Sides.noughts, self.logger)
        self.player_2 = player2_class(rules.Sides.crosses, self.logger)

    def run(self):
        self.board.fill(0)

        while self.play(self.player_1) and self.play(self.player_2):
            pass

    def play(self, player):
        self.logger.debug(self.board_str())

        # Player turn
        move = player.move(self.board)

        # Check if move is in empty_cells
        if list(move) in rules.empty_cells(self.board).tolist():
            self.board[move] = player.side
        else:
            self.logger.fatal("Invalid move")
            return False

        # Check for win or draw
        if rules.winning_move(self.board, move):
            self.logger.info("Game over: {0} win \n{1}".format(player,
                    self.board_str()))
            return False
        elif rules.draw(self.board):
            self.logger.info("Game over: draw \n{0}".format(self.board_str()))
            return False
        else:
            return True

    # Formats the board state as a string replacing cell values with enum names
    def board_str(self):
        # Join columns using '|' and rows using line-feeds
        return str('\n'.join(['|'.join([rules.Sides.token(item) for item in row])
                for row in self.board]))


if __name__ == "__main__":
    ttt = TicTacToe(3, ReinforcementAgent01, Agent04, logging.INFO)

    for _ in range(0, 100):
        ttt.run()

    # mpl_plot.plot_board(ttt.board)
