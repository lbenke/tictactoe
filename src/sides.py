class Sides(object):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2

    __tokens = {EMPTY: " ", NOUGHT: "o", CROSS: "x"}

    # Returns the name of a state given its value
    # TODO: remove, not needed?
    @staticmethod
    def state_name(value):
        for x in Sides.__dict__:
            if Sides.__dict__[x] == value:
                return x

    # Returns the game token for a state given its value
    @staticmethod
    def token(value):
        try:
            return Sides.__tokens[value]
        except KeyError:
            return "?"
