from sides import Sides

class Agent(object):
    def __init__(self, player_name, side):
        self.player_name = player_name
        self.side = side  # NOUGHT or CROSS

    def __str__(self):
        return self.player_name + " " + Sides.token(self.side)

