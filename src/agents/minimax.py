"""
This module contains agents that use minimax to select optimal moves.
"""

from players import Player
import rules


class MiniMaxAgent(Player):
    """
    Agent that applies minimax to choose the next move.

    This agent will always choose the optimal move, but is comparatively slow to
    execute as it uses exhaustive search of the move tree. It does not consider 
    depth.
    """

    def move(self, board):
        # Return the first move in the list of optimal moves found
        move = self.minimax(board, self.side)[1][0]
        return tuple(move)

    def minimax(self, board, player):
        """
        Recursive method that returns the optimal next moves and their value.

        The depth of the current move in the tree is recorded so that the agent 
        can favour moves that win quicker (or lose slower) when there are 
        multiple moves with the same expected game result.

        Args:
            state (numpy.ndarray): two dimensional array representing the
                board state
            player (int): the side of the current player
            depth (int): the depth of the move

        Returns:
            result (int): the return value of the moves (100 - depth for a win, 
                0 for a draw or depth - 100 for a loss)
            optimal_moves ([(int, int)]): a list of the optimal next moves
        """
        empty_cells = rules.empty_cells(board)

        # Choose default cell if board is empty to reduce processing time
        # if len(empty_cells) == board.size:
        #     import numpy as np
        #     return None, np.asarray([(0, 0)])

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

        # Test each child move recursively and add results to the list
        results_list = []
        for cell in empty_cells:
            # Make the move
            cell = tuple(cell)
            board[cell] = player

            # Get the value of this child move and add it to the results
            result, _ = self.minimax(board, -player)
            results_list.append(result)

            # Reverse the move
            board[cell] = rules.EMPTY

        if player is self.side:
            # Return best move for player from list of child moves
            max_score = max(results_list)
            max_inds = [i for i, x in enumerate(results_list) if x == max_score]
            optimal_moves = empty_cells[max_inds]
            return max_score, optimal_moves
        else:
            # Return worst move for opponent from list of child moves
            min_element = min(results_list)
            # move = tuple(empty_cells[results_list.index(min_element)])
            # return min_element, move
            return min_element, None  # don't need the actual move


class MiniMaxDepthAgent(Player):
    """
    Agent that applies minimax to choose the next move.

    This agent will always choose the optimal move, but is comparatively slow to
    execute as it uses exhaustive search of the move tree. Depth is included 
    when calculating move values, so moves than win quickly or lose slowly are 
    favoured.
    """

    def move(self, board):
        # Return the first move in the list of optimal moves found
        move = self.minimax(board, self.side)[1][0]
        return tuple(move)

    def minimax(self, board, player, depth=0):
        """
        Recursive method that returns the optimal next moves and their value.

        The depth of the current move in the tree is recorded so that the agent 
        can favour moves that win quicker (or lose slower) when there are 
        multiple moves with the same expected game result.

        Args:
            state (numpy.ndarray): two dimensional array representing the
                board state
            player (int): the side of the current player
            depth (int): the depth of the move

        Returns:
            result (int): the return value of the moves (100 - depth for a win, 
                0 for a draw or depth - 100 for a loss)
            optimal_moves ([(int, int)]): a list of the optimal next moves
        """
        empty_cells = rules.empty_cells(board)

        # Choose default cell if board is empty to reduce processing time
        # if len(empty_cells) == board.size:
        #     import numpy as np
        #     return None, np.asarray([(0, 0)])

        # Check if this move resulted in a win or draw (base case)
        winner = rules.winner(board)
        if winner is not None:
            if winner == self.side:
                # Player won so return score for a win
                return 100 - depth, None
            else:
                # Opponent won so return score for a loss
                return depth - 100, None
        elif rules.board_full(board):
            # Board is full so return score for a draw
            return 0, None

        # Test each child move recursively and add results to the list
        results_list = []
        for cell in empty_cells:
            # Make the move
            cell = tuple(cell)
            board[cell] = player

            # Get the value of this child move and add it to the results
            result, _ = self.minimax(board, -player, depth + 1)
            results_list.append(result)

            # Reverse the move
            board[cell] = rules.EMPTY

        if player is self.side:
            # Return best move for player from list of child moves
            max_score = max(results_list)
            max_inds = [i for i, x in enumerate(results_list) if x == max_score]
            optimal_moves = empty_cells[max_inds]
            return max_score, optimal_moves
        else:
            # Return worst move for opponent from list of child moves
            min_element = min(results_list)
            # move = tuple(empty_cells[results_list.index(min_element)])
            # return min_element, move
            return min_element, None  # don't need the actual move
