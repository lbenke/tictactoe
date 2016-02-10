import numpy as np
from matplotlib import pyplot
from sides import Sides

def plot_board(board):
    n = board.shape[0]

    fig = pyplot.figure("TicTacToe", figsize=[8,8], facecolor=(1,1,1))
    ax = fig.add_subplot(111, xticks=range(n + 1),
            yticks=range(n + 1), axis_bgcolor='none')

    # Draw the game grid and border
    ax.grid(color='black', linestyle='-', linewidth=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(10)

    # Hide the tick labels
    ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
    ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')

    # Draw the board values
    font_blue = {'family': 'sans-serif', 'color': 'dodgerblue',
                 'weight': 'normal', 'size': 100,
                 'horizontalalignment': "center",
                 'verticalalignment': 'center'}
    font_red = {'family': 'sans-serif', 'color': 'crimson',
                'weight': 'normal', 'size': 100,
                'horizontalalignment': "center",
                'verticalalignment': 'center'}
    for (x, y), value in np.ndenumerate(board):
        if value == Sides.NOUGHT:
            pyplot.text(y + 0.5, n - x - 0.5, Sides.token(value), font_blue)
        else:
            pyplot.text(y + 0.5, n - x - 0.5, Sides.token(value), font_red)

    pyplot.show()