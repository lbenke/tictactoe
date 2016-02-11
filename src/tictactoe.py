from agent import *
import rules
import mpl_plot


class TicTacToe(object):
    def __init__(self, agent1_class, agent2_class):
        n = 3
        self.board = np.zeros((n, n))
        self.player_1 = agent1_class("Player 1", rules.Sides.NOUGHT)
        self.player_2 = agent2_class("Player 2", rules.Sides.CROSS)

    def run(self):
        self.board.fill(0)

        while self.play(self.player_1) and self.play(self.player_2):
            pass

    def play(self, player):
        print self.board_str(), "\n"

        # Player turn
        move = player.move(self.board)
        self.board[move] = player.side

        # Check for win or draw
        if rules.winning_move(self.board, move):
            print "Game over: {0} wins\n".format(player), self.board_str()
            return False
        elif rules.draw(self.board, move):
            print "Game over: draw\n", self.board_str()
            return False
        else:
            return True

    # Formats the board state as a string replacing cell values with enum names
    def board_str(self):
        # Join columns using '|' and rows using line-feeds
        return str('\n'.join(['|'.join([rules.Sides.token(item) for item in row])
                for row in self.board]))


if __name__ == "__main__":
    ttt = TicTacToe(Agent04, Agent04)
    ttt.run()
    # mpl_plot.plot_board(ttt.board)

    # TODO: repeated runs, comparing wins for agent types
