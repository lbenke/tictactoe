"""
This module contains tests for the minimax agent.
"""

from unittest import TestCase
from tictactoe import TicTacToe
import numpy as np
from players import WinBlockRandomCellAgent
from agents.minimax import MiniMaxAgent


class TestMinimax(TestCase):
    def setUp(self):
        pass

    def test_win_single_move(self):
        """Tests that the agent chooses the correct single move to win."""
        # Create the players
        minimax1 = MiniMaxAgent()
        simple_agent = WinBlockRandomCellAgent()

        game = TicTacToe([minimax1, simple_agent], shuffle=False)
        board = np.asarray([[-1, -1, 0], [0, 0, 0], [0, 0, 0]])
        result = game.run(board)
        self.assertEqual(result, minimax1.side)

        game = TicTacToe([minimax1, simple_agent], shuffle=False)
        board = np.asarray([[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]])
        result = game.run(board)
        self.assertEqual(result, minimax1.side)

        game = TicTacToe([minimax1, simple_agent], shuffle=False)
        board = np.asarray([[-1, -1, 0], [1, -1, 0], [0, 0, -1]])
        result = game.run(board)
        self.assertEqual(result, minimax1.side)

    def test_win_vs_simple_agent(self):
        """Tests that the agent chooses the correct series of moves to win."""
        minimax = MiniMaxAgent()
        simple_agent = WinBlockRandomCellAgent()
        self.win_multiple_moves(minimax, simple_agent)

    def test_win_vs_minimax(self):
        """Tests that the agent chooses the correct series of moves to win."""
        minimax1 = MiniMaxAgent()
        minimax2 = MiniMaxAgent()
        self.win_multiple_moves(minimax1, minimax2)

    def win_multiple_moves(self, agent1, agent2):
        """Tests that the agent chooses the correct series of moves to win."""
        # Play first, single move to create a fork
        game = TicTacToe([agent1, agent2], shuffle=False)
        board = np.asarray([[-1, 0, 0], [0, 0, 0], [0, 0, -1]])
        result = game.run(board)
        self.assertEqual(result, agent1.side)

        # Play second, single move to create a fork
        game = TicTacToe([agent2, agent1], shuffle=False)
        board = np.asarray([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
        result = game.run(board)
        self.assertEqual(result, agent1.side)

        # Play second, different fork
        game = TicTacToe([agent2, agent1], shuffle=False)
        board = np.asarray([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
        result = game.run(board)
        self.assertEqual(result, agent1.side)

        # Unbeatable starting configuration
        game = TicTacToe([agent1, agent2], shuffle=False)
        board = np.asarray([[-1, 1, 0], [0, 0, 0], [0, 0, 0]])
        result = game.run(board)
        self.assertEqual(result, agent1.side)
