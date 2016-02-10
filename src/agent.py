import random

class Agent(object):
    def __init__(self, player_name, side):
        self.player_name = player_name
        self.side = side  # NOUGHT or CROSS

    def __str__(self):
        return self.player_name

    def move(self, board):
        random_coord = (random.randint(0,2), random.randint(0,2))
        board[random_coord] = self.side
        return board

