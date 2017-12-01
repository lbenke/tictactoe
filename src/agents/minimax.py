import rules
from players import Player


class MiniMaxAgent(Player):
    """
    Agent that applies minimax to choose the next move.

    This agent will always choose the optimal move, but is relatively slow as it 
    uses exhaustive search of the move tree.
    """

    def move(self, board):
        return self.calc_move(board, self.side)[1]

    def calc_move(self, board, player, move=None):
        """
        Recursive method that returns the ideal next move and its value.

        Args:
            state (numpy.ndarray): two dimensional array representing the
                board state
            player (int): the side of the current player
            move ((int, int)): tuple with the coordinates of the new move (x, y)

        Returns:
            retval (int): the return value of the move (1 for a win, 0 for a 
                draw and -1 for a loss)            
            next_move ((int, int)): tuple describing the optimal next move
        """
        # Choose the middle cell if the board is empty
        empty_cells = rules.empty_cells(board)
        if len(empty_cells) == board.size:
            return None, (1, 1)

        # Check if this move resulted in a win for either player
        if move is not None and rules.winning_move(board, move):
            # print "Winning move: ", board, move
            if player is self.side:
                return -1, None
            else:
                return 1, None
        elif len(empty_cells) == 0:
            return 0, None

        results_list = []  # list for appending the result
        for cell in empty_cells:
            cell = tuple(cell)
            board[cell] = player
            # print "Calling calc_move: ", -player, cell
            retval, move = self.calc_move(board, -player, cell)
            # print retval, move, player
            results_list.append(retval)
            board[cell] = rules.EMPTY
        if player is self.side:
            maxele = max(results_list)
            return maxele, tuple(empty_cells[results_list.index(maxele)])
        else:
            minele = min(results_list)
            return minele, tuple(empty_cells[results_list.index(minele)])