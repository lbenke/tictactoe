import random
import numpy as np
from sides import Sides


class Agent(object):
    def __init__(self, player_name, side):
        self.player_name = player_name
        self.side = side  # NOUGHT or CROSS

    def __str__(self):
        return self.player_name

    def move(self, board):
        # Find empty cells and select one at random
        empty_cells = np.transpose(np.nonzero(board == Sides.EMPTY))
        cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
        return cell
