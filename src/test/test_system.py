"""
This module contains system and integration tests.
"""

from unittest import TestCase
from tictactoe import TicTacToe
import numpy as np
from players import Human
from agents.minimax import MiniMaxAgent


class TestSystem(TestCase):
    def setUp(self):
        pass

    def test_game_result(self):
        """Tests that the game returns the correct result when passed an initial
        board with a win or draw state."""
        # Create the players
        human = Human()
        agent = MiniMaxAgent()

        # Test draw result
        game = TicTacToe([human, agent], shuffle=False)
        board = np.asarray([[1, -1, -1], [-1, 1, 1], [1, -1, -1]])
        result = game.run(board)
        self.assertEqual(result, None)

        game = TicTacToe([agent, human], shuffle=False)
        board = np.asarray([[1, -1, -1], [-1, 1, 1], [1, -1, -1]])
        result = game.run(board)
        self.assertEqual(result, None)

        # Test side 1 wins
        game = TicTacToe([human, agent], shuffle=False)
        board = np.asarray([[1, -1, -1], [1, 1, 1], [1, -1, -1]])
        result = game.run(board)
        self.assertEqual(result, 1)

        # Test side -1 wins
        game = TicTacToe([human, agent], shuffle=False)
        board = np.asarray([[-1, -1, -1], [1, 1, 1], [1, -1, -1]])
        result = game.run(board)
        self.assertEqual(result, -1)
