"""Behavioral regression tests for the modular Dots and Boxes game."""
import copy
import random
import unittest
from unittest.mock import patch

from board import Board
from computer import available_moves, boxes_completed_by_move, choose_move
from game import DotsAndBoxes
from rules import valid_move


def state(game):
    return (copy.deepcopy(game.board.horizontal), copy.deepcopy(game.board.vertical),
            set(game.board.completed), list(game.scores), game.current)


class BoardRulesTests(unittest.TestCase):
    def test_horizontal_and_vertical_moves(self):
        board = Board(1, 1)
        self.assertTrue(valid_move(board, 'H', 0, 0))
        self.assertTrue(valid_move(board, 'V', 0, 0))
        board.add_line('H', 0, 0)
        board.add_line('V', 0, 0)
        self.assertTrue(board.horizontal[0][0])
        self.assertTrue(board.vertical[0][0])
        self.assertFalse(valid_move(board, 'H', 0, 0))
        self.assertFalse(valid_move(board, 'V', 0, 0))

    def test_invalid_and_duplicate_direct_board_moves_are_atomic(self):
        board = Board()
        board.add_line('H', 0, 0)
        before = (copy.deepcopy(board.horizontal), copy.deepcopy(board.vertical), set(board.completed))
        for move in [('H', 0, 0), ('V', -1, 0), ('H', 3, 0),
                     ('V', 0, 3), ('X', 0, 0), ('H', '0', 0)]:
            with self.subTest(move=move), self.assertRaises(ValueError):
                board.add_line(*move)
            self.assertEqual((board.horizontal, board.vertical, board.completed), before)

    def test_box_completed_once(self):
        board = Board(1, 1)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0)]:
            board.add_line(*move)
            self.assertEqual(len(board.completed), 0)
        board.add_line('V', 0, 1)
        self.assertEqual(board.completed, {(0, 0)})
        with self.assertRaises(ValueError):
            board.add_line('V', 0, 1)
        self.assertEqual(len(board.completed), 1)


class GameRulesTests(unittest.TestCase):
    def test_no_score_switches_turn(self):
        for mode in (False, True):
            with self.subTest(vs_computer=mode):
                game = DotsAndBoxes(vs_computer=mode)
                self.assertEqual(game.play_move('H', 0, 0), 0)
                self.assertEqual(game.current, 1)
                self.assertEqual(game.scores, [0, 0])

    def test_single_box_scores_one_and_grants_extra_turn(self):
        game = DotsAndBoxes()
        game.board = Board(1, 1)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0)]:
            game.play_move(*move)
        scorer = game.current
        self.assertEqual(game.play_move('V', 0, 1), 1)
        self.assertEqual(game.current, scorer)
        self.assertEqual(game.scores[scorer], 1)

    def test_double_box_scores_two_and_grants_extra_turn(self):
        for mode in (False, True):
            with self.subTest(vs_computer=mode):
                game = DotsAndBoxes(vs_computer=mode)
                game.board = Board(1, 2)
                for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0),
                             ('H', 0, 1), ('H', 1, 1), ('V', 0, 2)]:
                    game.play_move(*move)
                scorer = game.current
                self.assertEqual(game.play_move('V', 0, 1), 2)
                self.assertEqual(game.scores[scorer], 2)
                self.assertEqual(game.current, scorer)
                self.assertEqual(sum(game.scores), 2)

    def test_invalid_moves_preserve_every_state_component(self):
        for mode in (False, True):
            game = DotsAndBoxes(vs_computer=mode)
            game.play_move('H', 0, 0)
            before = state(game)
            for move in [('H', 0, 0), ('V', -1, 0), ('H', 3, 0),
                         ('V', 0, 3), ('X', 0, 0), ('H', 'zero', 0)]:
                with self.subTest(mode=mode, move=move), self.assertRaises(ValueError):
                    game.play_move(*move)
                self.assertEqual(state(game), before)

    def test_game_over_and_no_further_moves(self):
        game = DotsAndBoxes()
        game.board = Board(1, 1)
        for move in [('H', 0, 0), ('V', 0, 0), ('H', 1, 0), ('V', 0, 1)]:
            game.play_move(*move)
        self.assertTrue(game.board.is_complete())
        self.assertEqual(sum(game.scores), 1)
        before = state(game)
        with self.assertRaisesRegex(ValueError, 'already complete'):
            game.play_move('H', 0, 0)
        self.assertEqual(state(game), before)

    def test_computer_moves_are_legal_and_do_not_mutate_board(self):
        for seed in range(40):
            game = DotsAndBoxes(vs_computer=True)
            rng = random.Random(seed)
            while not game.board.is_complete():
                before = state(game)
                legal = available_moves(game.board)
                choice = choose_move(game.board, rng)
                self.assertEqual(state(game), before)
                self.assertIn(choice, legal)
                self.assertTrue(valid_move(game.board, *choice))
                game.play_move(*choice)
                self.assertEqual(sum(game.scores), len(game.board.completed))
            self.assertIsNone(choose_move(game.board, rng))
            self.assertEqual(sum(game.scores), 4)

    def test_computer_prefers_double_box_completion(self):
        board = Board(1, 2)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0),
                     ('H', 0, 1), ('H', 1, 1), ('V', 0, 2)]:
            board.add_line(*move)
        self.assertEqual(boxes_completed_by_move(board, ('V', 0, 1)), 2)
        self.assertEqual(choose_move(board, random.Random(3)), ('V', 0, 1))

    def test_computer_turns_follow_same_scoring_rules(self):
        game = DotsAndBoxes(vs_computer=True)
        game.board = Board(1, 1)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0)]:
            game.play_move(*move)
        self.assertEqual(game.current, 1)
        choice = choose_move(game.board, random.Random(1))
        self.assertEqual(choice, ('V', 0, 1))
        self.assertEqual(game.play_move(*choice), 1)
        self.assertEqual(game.current, 1)
        self.assertEqual(game.scores, [0, 1])


if __name__ == '__main__':
    unittest.main()
