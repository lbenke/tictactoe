import numpy
import matplotlib.pyplot as plt
from agent import Agent
from sides import Sides

class TicTacToe(object):
    def __init__(self):
        self.board = numpy.zeros((3,3))
        self.player_1 = Agent("Player 1", Sides.NOUGHT)
        self.player_2 = Agent("Player 2", Sides.CROSS)

    def plot(self):
        fig = plt.figure("TicTacToe", figsize=[8,8], facecolor=(1,1,1))
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
        font_blue = {'family': 'sans-serif', 'color': 'dodgerblue',
                     'weight': 'normal', 'size': 100,
                     'horizontalalignment': "center",
                     'verticalalignment': 'center'}
        font_red = {'family': 'sans-serif', 'color': 'crimson',
                    'weight': 'normal', 'size': 100,
                    'horizontalalignment': "center",
                    'verticalalignment': 'center'}

        for (x, y), value in numpy.ndenumerate(self.board):
            plt.text(x + 0.5, y + 0.5, Sides.token(value), font_blue)

        plt.show()

if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.board[0, 0] = Sides.NOUGHT
    ttt.board[1, 1] = Sides.NOUGHT
    ttt.board[2, 2] = Sides.CROSS
    ttt.board[1, 2] = Sides.CROSS

    print ttt
    ttt.plot()