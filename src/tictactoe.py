import numpy as np
from agent import Agent, AgentRandom, AgentFirst
from sides import Sides
import mpl_plot


class TicTacToe(object):
    def __init__(self):
        self.n = 3
        self.board = np.zeros((self.n, self.n))
        self.player_1 = AgentRandom("Player 1", Sides.NOUGHT)
        self.player_2 = AgentFirst("Player 2", Sides.CROSS)

    def run(self):
        while self.play(self.player_1) and self.play(self.player_2):
            pass

    def play(self, player):
        print self.board_str(), "\n"

        # Player turn
        (x, y) = player.move(self.board)
        self.board[x, y] = player.side

        # Check for win or draw
        winner = self.winner()
        if winner is None:
            if not Sides.EMPTY in self.board:
                # Board is full; game over
                print "Game over: draw\n", self.board_str()
                return False
        else:
            print "Game over: {0} wins\n".format(winner), self.board_str()
            return False

        return True

    # Checks whether a player has won and if so returns the winning side
    # TODO: just check from latest move and return true if winning move
    def winner(self):
        if False:
            return self.player_1
        else:
            return None

    # Formats the board state as a string replacing cell values with enum names
    def board_str(self):
        return str('\n'.join(['|'.join(['{:1}'.format(Sides.token(item)) \
                        for item in row]) for row in self.board]))


if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.run()
    mpl_plot.plot_board(ttt.board)
