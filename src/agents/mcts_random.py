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


class MCTSAgentRandom(Player):
    """
    Agent that uses Monte Carlo tree search (MCTS) to choose the next move.
    
    This version uses purely random tree search.
    
    Attributes:
        time_budget (float): number of seconds to build tree and choose move
        tree_root (TreeNode): the root node of the MCTS tree
    """

    def __init__(self, time_budget=0.10, side=None, logger=None):
        """
        Constructor.
        
        Args:
            time_budget (float): number of seconds to build tree and choose move
            side (int): the player side, defined in the game rules
            logger (RootLogger): optional logger for output
        """
        super(MCTSAgentRandom, self).__init__(side, logger)
        self.time_budget = time_budget
        self.root_node = None

    def move(self, board):
        return self.mcts(board)

    def mcts(self, board):
        max_time = time.time() + self.time_budget
        root_node = TreeNode(board)
        playout_count = 0

        while time.time() < max_time:
            # Start at tree root (current actual state)
            current_node = root_node
            current_player = self.side

            while True:
                # Check for terminal state
                winner = rules.winner(current_node.state)
                if winner or rules.board_full(current_node.state):
                    break

                # Pick a random move
                empty_cells = rules.empty_cells(current_node.state)
                move = tuple(random.choice(empty_cells))

                # Add to tree if not present
                if move not in current_node.child_nodes.keys():
                    # If not, create a TreeNode for it
                    new_board = current_node.state.copy()
                    new_board[move] = current_player
                    current_node.child_nodes[move] = TreeNode(
                            new_board, current_node)
                current_node = current_node.child_nodes[move]

                # Swap players
                current_player = -current_player

            # Terminal state reached so backpropagate result
            if winner == self.side:
                result = 1.0
            elif winner == -self.side:
                result = 0.0
            else:
                result = 0.5
            while current_node is not root_node:
                current_node.visits += 1
                current_node.wins += result
                current_node = current_node.parent

            playout_count += 1

        print "Number of MCTS playouts:", playout_count

        self.root_node = current_node

        # Return move with highest score
        best_move = root_node.best_move()
        return best_move


class TreeNode(object):
    """
    Class representing a single node in the MCTS tree. 
    
    Attributes:
        id (int): unique number identifying the node in the tree
        state (numpy.ndarray): two dimensional array representing the game board
        parent (int): id of the parent of this node or None
        visits (int): number of times this node has been visited
        wins (int): number of visits to this node that have resulted in a win
        child_nodes ({(int, int):TreeNode}): dict of child nodes in the form 
            (Move:ChildNode), where Move is the tuple of coordinates required to 
            reach the board state corresponding to ChildNode 
    """
    new_id = itertools.count().next  # function that returns sequential integers

    def __init__(self, board, parent=None):
        """
        Constructor.
        
        Args:
            board (numpy.ndarray): two dimensional array representing the game 
                board
            parent (int): id of the parent of this node or None
        """
        self.id = TreeNode.new_id()  # get a unique number to identify the node
        self.state = board
        self.parent = parent
        self.visits = 0;
        self.wins = 0;
        self.child_nodes = {}

    def best_move(self):
        """
        Finds and returns the move leading to the child node with the highest
        score.
         
        Returns:
            (int, int): tuple with the coordinates of the new move (x, y)
        """
        best_move = None
        for move in self.child_nodes:
            if (best_move is None or self.child_nodes[move].score() >
                    self.child_nodes[best_move].score()):
                best_move = move

        return best_move

    def score(self):
        """Returns the score for this node, the ratio of wins resulting from 
        this node to the number of times it was visited."""
        if self.visits != 0:
            return float(self.wins) / float(self.visits)
        else:
            return None

    def __str__(self):
        """Returns a string representation of the board state represented by 
        this node."""
        return rules.board_str(self.state)


if __name__ == "__main__":
    import numpy as np
    mcts_agent = MCTSAgentRandom()
    mcts_agent.side = rules.CROSS
    # board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # board = np.asarray([[1, 0, 0], [0, -1, 0], [0, 1, 0]])
    # board = np.asarray([[1, 0, 1], [0, 0, 0], [0, 0, 0]])
    # board = np.asarray([[1, -1, 1], [0, -1, 0], [0, 1, 0]])
    board = np.asarray([[-1, 1, -1], [0, 1, 1], [0, -1, 0]])
    # board = np.asarray([[-1, 1, 1], [0, -1, 1], [-1, -1, 0]])
    mcts_agent.move(board)

    # Visualise the tree
    print "Generating graph..."
    t = time.time()
    g = graphing.MCTSGraph(root_node=mcts_agent.root_node)
    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    path = "tree_graph_{}.{}".format(timestamp, 'png')
    g.draw_graph(path)
    print "Time to generate graph: ", time.time() - t, "seconds"
    #
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
