"""
This module contains agents that use Monte Carlo tree search to select moves.
"""

from players import Player
import rules
import time
import random
import graphing.mcts_graph as graphing
import itertools
import datetime


class MCTSAgent(Player):
    """
    Agent that uses Monte Carlo tree search (MCTS) to choose the next move.
    """
    time_budget = 0.50  # number of seconds to build tree and choose move

    def move(self, board):
        return self.mcts(board)

    def is_terminal_state(self, board):
        if rules.board_full(board) or rules.winner(board) is not None:
            return True

    def mcts(self, board):
        max_time = time.time() + MCTSAgent.time_budget
        root_node = TreeNode(board)
        playout_count = 0

        while time.time() < max_time:
            # Pick tree root (current actual state)
            current_node = root_node
            current_player = self.side

            terminal_state = False
            while not terminal_state:
                # Pick a random move
                empty_cells = rules.empty_cells(current_node.state)
                move = tuple(random.choice(empty_cells))

                # Add to tree if not present
                if move not in current_node.child_nodes.keys():
                    # if not, create a TreeNode for it
                    new_board = current_node.state.copy()
                    new_board[move] = current_player
                    current_node.child_nodes[move] = TreeNode(new_board, current_node)
                current_node = current_node.child_nodes[move]

                # Check for win/loss/draw
                terminal_state = self.is_terminal_state(current_node.state)

                # Swap players
                current_player = -current_player

            # Terminal state reached so backpropagate result
            winner = rules.winner(current_node.state)
            while current_node is not root_node:
                current_node.visits += 1
                if winner == self.side:
                    current_node.score += 1.0
                elif winner == -self.side:
                    current_node.score += 0.0
                else:
                    current_node.score += 0.5
                # Move up the tree
                current_node = current_node.parent

            playout_count += 1

        print "Number of MCTS playouts:", playout_count

        # Visualise the tree
        print "Generating graph..."
        t = time.time()
        g = graphing.MCTSGraph(root_node=current_node)
        timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        path = "tree_graph_{}.{}".format(timestamp, 'png')
        g.draw_graph(path)
        print "Time to generate graph: ", time.time() - t, "seconds"

        # Return move with highest score
        best_move = root_node.best_move()

        return best_move


class TreeNode(object):
    new_id = itertools.count().next

    def __init__(self, board, parent=None):
        self.id = TreeNode.new_id()
        self.state = board
        self.parent = parent
        self.visits = 0;
        self.score = 0;
        self.child_nodes = {}

    def best_move(self):
        best_move = None
        for move in self.child_nodes:
            if (best_move is None or self.child_nodes[move].ratio() >
                    self.child_nodes[best_move].ratio()):
                best_move = move

        return best_move

    def ratio(self):
        if self.visits != 0:
            return float(self.score) / float(self.visits)
        else:
            return None

    def to_string(self):
        return rules.board_str(self.state)


if __name__ == "__main__":
    import numpy as np
    mcts_agent = MCTSAgent()
    mcts_agent.side = rules.CROSS
    # board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # board = np.asarray([[1, 0, 0], [0, -1, 0], [0, 1, 0]])
    # board = np.asarray([[1, 0, 1], [0, 0, 0], [0, 0, 0]])
    # board = np.asarray([[1, -1, 1], [0, -1, 0], [0, 1, 0]])
    board = np.asarray([[-1, 1, -1], [0, 1, 1], [0, -1, 0]])
    # board = np.asarray([[-1, 1, 1], [0, -1, 1], [-1, -1, 0]])
    mcts_agent.move(board)

    # import logging
    # import sys
    # from tictactoe import TicTacToe
    # # Set up the logger
    # logger = logging.getLogger()
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    #     format="\n%(message)s")
    #
    # # Create the players
    # from players import Human
    # human = Human(logger=logger)
    # from agents.mcts import MCTSAgent
    # agent = MCTSAgent(logger=logger)
    #
    # # Run the game
    # game = TicTacToe([human, agent], shuffle=True, logger=logger)
    # while True:
    #     game.run()
