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
    
    Note that there is no concept of depth; in cases where there all moves lead
    eventually to a win, the agent chooses arbitrarily (e.g. it may ignore an 
    obvious immediate winning move since it knows it will win eventually 
    anyway). This also applies in reverse; if the agent is put in a position 
    where all paths lead to a loss, it does not differentiate between losing 
    immediately and losing in a number of moves, and may choose a move that 
    loses immediately instead of one that keeps it in the game for longer.
    This can be remedied by recording depth and favouring paths with more or 
    less depth depending on the expected game result.
    """

    def move(self, board):
        return self.minimax(board, self.side)[1]

    def minimax(self, board, player):
        """
        Recursive method that returns the optimal next move and its value.

        Args:
            state (numpy.ndarray): two dimensional array representing the
                board state
            player (int): the side of the current player

        Returns:
            retval (int): the return value of the move (1 for a win, 0 for a 
                draw or -1 for a loss)
            next_move ((int, int)): the location of the optimal next move
        """
        empty_cells = rules.empty_cells(board)

        # Choose default cell if board is empty to reduce processing time
        if len(empty_cells) == board.size:
            return None, (0, 0)

        # Check if this move resulted in a win or draw (base case)
        winner = rules.winner(board)
        if winner is not None:
            if winner == self.side:
                # Player won so return score for a win
                return 1, None
            else:
                # Opponent won so return score for a loss
                return -1, None
        elif rules.board_full(board):
            # Board is full so return score for a draw
            return 0, None

        # Test child moves recursively and add results to the list
        results_list = []
        for cell in empty_cells:
            # Make the move
            cell = tuple(cell)
            board[cell] = player

            # Get the value of this child move and add it to the results
            retval, move = self.minimax(board, -player)
            results_list.append(retval)

            # Reverse the move
            board[cell] = rules.EMPTY

        if player is self.side:
            # Return best move for player from list of child moves
            max_element = max(results_list)
            move = tuple(empty_cells[results_list.index(max_element)])
            return max_element, move
        else:
            # Return worst move for opponent from list of child moves
            min_element = min(results_list)
            move = tuple(empty_cells[results_list.index(min_element)])
            return min_element, move