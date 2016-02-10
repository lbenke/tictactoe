import numpy
from matplotlib import pyplot
from agent import Agent


class Sides(object):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2
    __tokens = {EMPTY: "_", NOUGHT: "o", CROSS: "x"}

    # Returns the game token for a state given its value
    @staticmethod
    def token(value):
        try:
            return Sides.__tokens[value]
        except KeyError:
            return "?"


class TicTacToe(object):
    def __init__(self):
        self.board = numpy.zeros((3,3))
        self.player_1 = Agent("Player 1", Sides.NOUGHT)
        self.player_2 = Agent("Player 2", Sides.CROSS)

        # Main loop
        game_over = False
        while not game_over:
            print self.board_str(), "\n"

            self.board = self.player_1.move(self.board)

            if not Sides.EMPTY in self.board:  # check for wincondition or drawcondition
                game_over = True

            self.board = self.player_2.move(self.board)

            # Check for win or draw conditions
            if False:  # TODO: identify win
                winner = self.player_1
                print "Game over: {0} wins\n".format(winner), self.board_str()
                game_over = True
            elif not Sides.EMPTY in self.board:
                print "Game over: draw\n", self.board_str()
                game_over = True

    # Formats the board state as a string replacing cell values with enum names
    def board_str(self):
        return str('\n'.join(['|'.join(['{:1}'.format(Sides.token(item)) \
                        for item in row]) for row in self.board]))

    def plot(self):
        pyplot.ion()
        fig = pyplot.figure("TicTacToe", figsize=[8,8], facecolor=(1,1,1))
        ax = fig.add_subplot(111, xticks=range(4), yticks=range(4),
                             axis_bgcolor='none')

        # Draw the game grid and border
        ax.grid(color='black', linestyle='-', linewidth=10)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(10)

        # Hide the tick labels
        ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
        ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')

        # Draw test marks
        self.font_blue = {'family': 'sans-serif', 'color': 'dodgerblue',
                     'weight': 'normal', 'size': 100,
                     'horizontalalignment': "center",
                     'verticalalignment': 'center'}
        font_red = {'family': 'sans-serif', 'color': 'crimson',
                    'weight': 'normal', 'size': 100,
                    'horizontalalignment': "center",
                    'verticalalignment': 'center'}

        self.ax = ax

        pyplot.show()
        self.update_plot()

    def update_plot(self):
        for (x, y), value in numpy.ndenumerate(self.board):
            pyplot.text(x + 0.5, y + 0.5, Sides.token(value), self.font_blue)

        # pyplot.draw()
        # In interactive mode pyplot needs to be paused temporarily to update
        pyplot.pause(1.e-6)  # includes draw()
        # TODO: ion might not be the way to do it; aimed at console use?

        # TODO: maybe just render a new plot each time (no update) or animate
        # final version?
        # OR: get rid of mpl and use pyqt

if __name__ == "__main__":
    ttt = TicTacToe()
    # ttt.plot()
    #
    # ttt.board[0, 0] = Sides.NOUGHT
    # ttt.update_plot()
    # ttt.board[1, 2] = Sides.CROSS
    # ttt.update_plot()
    # ttt.board[2, 2] = Sides.NOUGHT
    # ttt.update_plot()
    # ttt.board[1, 1] = Sides.CROSS
    # ttt.update_plot()
    # ttt.board[2, 0] = Sides.NOUGHT
    # ttt.update_plot()
    # raw_input("Press Enter to close...")

