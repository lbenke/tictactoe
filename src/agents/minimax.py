"""
This module contains agents that use minimax to select optimal moves.
"""

import rules
from players import Player


class MiniMaxAgent(Player):
    """
    Agent that applies minimax to choose the next move.

    This agent will always choose the optimal move, but is comparatively slow to
    execute as it uses exhaustive search of the move tree.
    """

    def move(self, board):
        return self.calc_move(board, self.side)[1]

    def calc_move(self, board, player):
        """
        Recursive method that returns the ideal next move and its value.

        Args:
            state (numpy.ndarray): two dimensional array representing the
                board state
            player (int): the side of the current player

        Returns:
            retval (int): the return value of the move (1 for a win, 0 for a 
                draw and -1 for a loss)            
            next_move ((int, int)): tuple describing the optimal next move
        """
        empty_cells = rules.empty_cells(board)

        # Choose default cell if board is empty to reduce processing time
        if len(empty_cells) == board.size:
            return None, (0, 0)

        # Check if this move resulted in a win for either player (base case)
        if rules.winning_move(board):
            if player is self.side:
                # Opponent won so return loss
                return -1, None
            else:
                # Player won so return win
                return 1, None
        elif rules.board_full(board):
            # Board is full so return draw
            return 0, None

        results_list = []
        for cell in empty_cells:
            # Test child moves recursively and add the results to the list
            cell = tuple(cell)
            board[cell] = player
            retval, move = self.calc_move(board, -player)
            results_list.append(retval)
            board[cell] = rules.EMPTY

        if player is self.side:
            # Return the best move for the player
            maxele = max(results_list)
            return maxele, tuple(empty_cells[results_list.index(maxele)])
        else:
            # Return the worst move for the opponent
            minele = min(results_list)
            return minele, tuple(empty_cells[results_list.index(minele)])