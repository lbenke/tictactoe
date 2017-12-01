"""
This module contains tests for the game rules defined in the `rules` module.
"""

from unittest import TestCase
import rules
import numpy as np


class TestRules(TestCase):
    def setUp(self):
        pass

    def test_board_full(self):
        board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertFalse(rules.board_full(board))

        board = np.asarray([[-1, 1, 1], [0, 1, -2], [1, 1, -1]])
        self.assertFalse(rules.board_full(board))

        board = np.asarray([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertTrue(rules.board_full(board))

        board = np.asarray([[1, -1, 1], [1, 1, -1], [-1, 1, 1]])
        self.assertTrue(rules.board_full(board))

    def test_winning_moves(self):
        # Empty board
        board = np.asarray([[0,0,0],[0,0,0],[0,0,0]])
        self.assertFalse(rules.winning_move(board))

        # Diagonal
        board = np.asarray([[1, 0, 0], [-1, 1, 0], [1, 0, 1]])
        self.assertTrue(rules.winning_move(board))
        board = np.asarray([[-1, 0, 0], [-1, 1, 0], [1, 0, 1]])
        self.assertFalse(rules.winning_move(board))

        # Anti-diagonal
        board = np.asarray([[0, 0, 1], [0, 1, -1], [1, -1, -1]])
        self.assertTrue(rules.winning_move(board))
        board = np.asarray([[0, 0, 1], [0, -1, -1], [1, -1, -1]])
        self.assertFalse(rules.winning_move(board))

        # Opponent diagonal
        board = np.asarray([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
        self.assertTrue(rules.winning_move(board))
        board = np.asarray([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
        self.assertFalse(rules.winning_move(board))

        # Opponent anti-diagonal
        board = np.asarray([[0, 0, -1], [1, -1, 0], [-1, 0, 0]])
        self.assertTrue(rules.winning_move(board))
        board = np.asarray([[0, 0, 0], [1, -1, 0], [-1, 0, 0]])
        self.assertFalse(rules.winning_move(board))

        # Rows
        board = np.asarray([[1, 1, 1], [0, 0, 0], [0, 0, 0]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[1, 1, 1], [0, -1, 0], [0, 0, -1]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[0, 0, 0], [-1, -1, -1], [0, 0, 0]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[0, 0, 0], [0, 0, 0], [1, -1, 1]])
        self.assertFalse(rules.winning_move(np.asarray(board)))
        board = np.asarray([[1, 1, 1], [0, 0, 0], [1, -1, 1]])
        self.assertTrue(rules.winning_move(np.asarray(board)))

        # Columns
        board = np.asarray([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[1, -1, -1], [1, 0, 0], [-1, 0, 0]])
        self.assertFalse(rules.winning_move(np.asarray(board)))
        board = np.asarray([[0, -1, 0], [0, -1, 0], [0, -1, 0]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[-1, -1, 1], [0, 0, 1], [0, -1, 1]])
        self.assertTrue(rules.winning_move(np.asarray(board)))
        board = np.asarray([[-1, -1, 1], [0, 0, 0], [0, -1, 1]])
        self.assertFalse(rules.winning_move(np.asarray(board)))

    def test_valid_move(self):
        board = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertTrue(rules.valid_move(board, (0, 0)))
        self.assertTrue(rules.valid_move(board, (1, 2)))
        self.assertTrue(rules.valid_move(board, (2, 0)))

        board = np.asarray([[1, -1, -1], [-1, 1, 1], [1, -1, 1]])
        self.assertFalse(rules.valid_move(board, (0, 0)))
        self.assertFalse(rules.valid_move(board, (2, 1)))
        self.assertFalse(rules.valid_move(board, (2, 0)))

    def test_empty_cells(self):
        board = np.asarray([[1, -1, -1], [-1, 1, 1], [1, -1, 1]])
        expected = []
        empty_cells = rules.empty_cells(board)
        self.assertEqual(list(empty_cells), expected)

        board = np.asarray([[1, 1, 1], [1, 1, 1], [0, 1, 1]])
        expected = [[2, 0]]
        empty_cells = rules.empty_cells(board)
        np.testing.assert_array_equal(empty_cells, expected)

        board = np.asarray([[1, 0, 1], [1, 1, 1], [0, 1, 1]])
        expected = [[0, 1], [2, 0]]
        empty_cells = rules.empty_cells(board)
        np.testing.assert_array_equal(empty_cells, expected)

        board = np.asarray([[1, 1, 1], [0, 0, 0], [-1, 1, 1]])
        expected = [[1, 0], [1, 1], [1, 2]]
        empty_cells = rules.empty_cells(board)
        np.testing.assert_array_equal(empty_cells, expected)
