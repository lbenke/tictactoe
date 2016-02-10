class Sides(object):
    EMPTY = 0
    NOUGHT = 1
    CROSS = -1
    __tokens = {EMPTY: " ", NOUGHT: "o", CROSS: "x"}

    # Returns the game token for a state given its value
    @staticmethod
    def token(value):
        try:
            return Sides.__tokens[value]
        except KeyError:
            return "?"
