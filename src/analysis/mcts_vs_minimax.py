"""
This module contains code to conduct comparative analysis of the different agent
types implemented in this project.
"""

import rules
import random
import time
import numpy as np
from agents.minimax import MiniMaxAgent
from agents.mcts_ucb1 import MCTSAgentUCB1, UCTTreeNode

def generate_random_board():
    """  Returns a random valid Tic Tac Toe game board with at least one move 
    remaining. """
    board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    # Choose a starting player and game length
    side = random.choice([rules.CROSS, rules.NOUGHT])
    game_length = random.randint(0, 8)

    # Select moves for each player until the game length has been reached
    move_count = 0
    while move_count < game_length:
        move_count += 1
        empty_cells = rules.empty_cells(board)
        move = tuple(empty_cells[random.randint(0, len(empty_cells) - 1)])
        board[move] = side
        if rules.winner(board):
            board[move] = rules.EMPTY
        else:
            side = -side

    # Return the game board and the side of the next player to move
    return board, side

board, side = generate_random_board()
# board = np.asarray([[-1, 0, 1], [1, -1, 1], [0, 0, 0]])
print("Starting board ({} moves next):\n{}".format(
        rules.token(side), rules.board_str(board)))

# Measure how long it takes the minimax agent to find the optimal moves
minimax_agent = MiniMaxAgent()
minimax_agent.side = side
t = time.time()
_, minimax_moves = minimax_agent.minimax(board, minimax_agent.side)
minimax_time = round(time.time() - t, 6)

# Measure how long it takes for the MCTS agent to select any of the optimal
# moves chosen by the minimax agent
mcts_agent = MCTSAgentUCB1(convergence_limit=20)
mcts_agent.side = side
t = time.time()
# mcts_move = [None]
# mcts_agent.root_node = UCTTreeNode(board, mcts_agent.side)
# mcts_agent.playout_count = 0
# minimax_moves = minimax_moves.tolist()
# while not mcts_move in minimax_moves:
#     mcts_agent.mcts(board)
#     mcts_move = list(mcts_agent.root_node.best_move())
#     print("Minimax: {}, MCTS: {}".format(minimax_moves, mcts_move))
mcts_moves = mcts_agent.moves(board)
mcts_time = round(time.time() - t, 6)

print("Minimax: {}, MCTS: {}".format(minimax_moves, mcts_moves))
print "Number of MCTS playouts:", mcts_agent.playout_count

print("Time to calculate optimal move {}:\n  Minimax\t{} s\n  MCTS\t\t{} s".
        format(mcts_moves, minimax_time, mcts_time))
