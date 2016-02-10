import random
import numpy as np
from sides import Sides
from abc import ABCMeta, abstractmethod

# Abstract base class for agents
class Agent(object):
    __metaclass__ = ABCMeta

    def __init__(self, player_name, side):
        self.player_name = player_name
        self.side = side  # NOUGHT or CROSS

    def __str__(self):
        return self.player_name

    @abstractmethod
    def move(self, board):
        pass


# Agent that selects cells randomly
class AgentRandom(Agent):
    def move(self, board):
        # Find empty cells and select one at random
        empty_cells = np.transpose(np.nonzero(board == Sides.EMPTY))
        cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
        return cell


# Agent that selects cells sequentially
class AgentFirst(AgentRandom):
    def move(self, board):
        # Find empty cells and select the first one
        empty_cells = np.transpose(np.nonzero(board == Sides.EMPTY))
        cell = empty_cells[0]
        return cell
