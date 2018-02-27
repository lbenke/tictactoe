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
import math


class MCTSAgentUCB1(Player):
    """
    Agent that uses Monte Carlo tree search (MCTS) to choose the next move.

    This version uses UCB1 to select nodes.

    Attributes:
        tree_root (TreeNode): the root node of the MCTS tree
        playout_count (int): total number of MCTS playouts, i.e. the number
                of visits at the root node
        time_budget (float): number of seconds to build tree and choose move
        max_playouts (int): number of playouts to build tree and choose move
    """

    def __init__(self, time_budget=0.50, max_playouts=1000000,
            uctk=math.sqrt(2), side=None, logger=None):
        """
        Constructor.

        Args:
            time_budget (float): number of seconds to build tree and choose move
            uctk (float): constant for UCB1 calculation
            side (int): the player side, defined in the game rules
            logger (RootLogger): optional logger for output
        """
        super(MCTSAgentUCB1, self).__init__(side, logger)
        self.time_budget = time_budget
        self.max_playouts = max_playouts
        self.root_node = None
        self.uctk = uctk

    def move(self, board):
        return self.mcts(board)

    def mcts(self, board):
        max_time = time.time() + self.time_budget
        self.root_node = UCTTreeNode(board, self.side)
        self.playout_count = 0

        while time.time() < max_time and self.playout_count < self.max_playouts:
            # Start at tree root (current actual state)
            current_node = self.root_node
            current_player = self.side

            # Select
            while current_node.child_nodes and not current_node.untried_moves:
                # This node has been fully expanded (no untried moves) and is
                # not terminal so use UCB1 to select a child and descend tree
                ucb1 = lambda child: self.ucb1_score(child, current_player)
                child_nodes = sorted(current_node.child_nodes.values(), key=ucb1)

                # Choose move with highest UCB1 score after sorting
                current_node = child_nodes[-1]

                # Swap players
                current_player = -current_player

            # Expand / rollout
            if current_node.untried_moves != []:
                # Now do a random playout since we don't have any
                # information from this move on
                while True:
                    # Check for terminal state
                    winner = rules.winner(current_node.state)
                    if winner or rules.board_full(current_node.state):
                        break

                    # There are untried moves so pick one at random
                    move = current_node.untried_moves.pop(
                            random.randrange(len(current_node.untried_moves)))
                    move = tuple(move)

                    # XXX:
                    # Note that usually only the first new move is added to the
                    # tree (i.e. one node per iteration) possibly to save space,
                    # not sure yet

                    # Add new node to the tree and remove from untried moves
                    new_board = current_node.state.copy()
                    new_board[move] = current_player  # apply the move
                    current_node.child_nodes[move] = UCTTreeNode(new_board,
                        current_player, current_node)

                    # Move down the tree
                    current_node = current_node.child_nodes[move]

                    # Swap players
                    current_player = -current_player

            self.playout_count += 1

            # Backpropagate
            # Terminal state reached so backpropagate result
            winner = rules.winner(current_node.state)
            while current_node:
                current_node.visits += 1
                if winner == self.side:
                    current_node.wins += 1
                elif winner == -self.side:
                    current_node.wins += 0
                else:
                    current_node.wins += 0.5
                current_node = current_node.parent

            # # Visualise the tree
            # g = graphing.MCTSGraph(root_node=self.root_node, sort_nodes=False)
            # path = "tree_graph_{}.{}".format(playout_count, 'png')
            # g.draw_graph(path)

        print "Number of MCTS playouts:", self.playout_count

        # Return move with highest score
        best_move = self.root_node.best_move()
        return best_move

    def ucb1_score(self, node, player):
        """Returns the UCB1 score for this node and updates the value in the 
        node."""
        # Calculate the score for this node based on the side of the player
        if player == self.side:
            score = node.wins / float(node.visits)
        else:
            # Get score from opponent's point of view
            score = (1.0 - node.wins) / float(node.visits)

        node.ucb1_score = (score + self.uctk *
                math.sqrt(math.log(self.playout_count) / node.visits))

        return node.ucb1_score


class UCTTreeNode(object):
    """
    Class representing a single node in the MCTS tree. 

    Attributes:
        id (int): unique number identifying the node in the tree
        state (numpy.ndarray): two dimensional array representing the game board
        side (int): the player side, defined in the game rules
        parent (int): id of the parent of this node or None
        visits (int): number of times this node has been visited
        wins (int): number of visits to this node that have resulted in a win
        untried_moves ([(int, int)]): list of child moves that haven't been 
            explored yet in the form [Move], where Move is the tuple of 
            coordinates required to reach a child board state
        child_nodes ({(int, int):TreeNode}): dict of child nodes in the form 
            (Move:ChildNode), where Move is the tuple of coordinates required to 
            reach the board state corresponding to ChildNode 
    """
    new_id = itertools.count().next  # function that returns sequential integers

    def __init__(self, board, side, parent=None):
        """
        Constructor.

        Args:
            board (numpy.ndarray): two dimensional array representing the game 
                board
            side (int): the player side, defined in the game rules
            parent (int): id of the parent of this node or None
        """
        self.id = UCTTreeNode.new_id()  # get a unique number to identify the node
        self.state = board
        self.side = side
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.ucb1_score = None
        self.untried_moves = rules.empty_cells(self.state).tolist()
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


def generate_graph(root_node):
    # Visualise the tree
    print "Generating graph..."
    t = time.time()

    g = graphing.MCTSGraph()
    # g.verbose_score = False
    g.generate_graph(root_node)

    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    path = "tree_graph_{}.{}".format(timestamp, 'png')
    g.draw_graph(path)

    print "Time to generate graph: ", time.time() - t, "seconds"

if __name__ == "__main__":
    import numpy as np

    interactive = False

    if interactive:
        import logging
        import sys
        from tictactoe import TicTacToe
        # Set up the logger
        logger = logging.getLogger()
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
            format="\n%(message)s")

        # Create the players
        from players import Human
        human = Human(logger=logger)
        # from agents.minimax import MiniMaxAgent
        # human = MiniMaxAgent()

        mcts_agent = MCTSAgentUCB1(logger=logger)

        # Run the game
        game = TicTacToe([human, mcts_agent], shuffle=True, logger=logger)
        while True:
            game.run()
            generate_graph(mcts_agent.root_node)

    else:
        random.seed(7)

        mcts_agent = MCTSAgentUCB1()
        mcts_agent.max_playouts = 100
        mcts_agent.side = rules.CROSS
        # board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        # board = np.asarray([[1, 0, 0], [0, -1, 0], [0, 1, 0]])
        # board = np.asarray([[1, 0, -1], [0, 0, 0], [0, 0, 0]])
        # board = np.asarray([[1, 0, -1], [0, 0, -1], [0, 0, 0]])
        # board = np.asarray([[1, -1, 1], [0, -1, 0], [0, 1, 0]])
        # board = np.asarray([[-1, 0, 1], [0, -1, 1], [-1, 1, 0]])
        # board = np.asarray([[-1, 1, -1], [0, 1, 1], [0, -1, 0]])
        board = np.asarray([[-1, 1, 1], [0, -1, 1], [1, -1, 0]])
        mcts_agent.move(board)

        generate_graph(mcts_agent.root_node)
