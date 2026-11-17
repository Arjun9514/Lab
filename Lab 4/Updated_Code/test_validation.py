"""Regression tests for input and game-state validation."""
import contextlib
import io
import unittest
from unittest.mock import patch

from board import Board
from computer import choose_move
from game import DotsAndBoxes
from main import main
from rules import parse_move, valid_move


def snapshot(game):
    board = game.board
    return (tuple(map(tuple, board.horizontal)), tuple(map(tuple, board.vertical)),
            frozenset(board.completed), tuple(game.scores), game.current)


class ValidationTests(unittest.TestCase):
    def test_parse_errors(self):
        invalid = ['', '  ', 'H', 'H 0', 'H 0 1 extra', 'X 0 0',
                   'H x 0', 'V 0 1.5', 'H 0 +', 'H 1, 0']
        for raw in invalid:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_move(raw)
        self.assertEqual(parse_move(' h 0 1 '), ('H', 0, 1))
        self.assertEqual(parse_move('V -1 0'), ('V', -1, 0))

    def test_invalid_moves_are_atomic(self):
        for mode in (False, True):
            with self.subTest(mode=mode):
                game = DotsAndBoxes(vs_computer=mode)
                game.play_move('H', 0, 0)
                original = snapshot(game)
                for move in [('X', 0, 0), ('H', -1, 0), ('H', 0, -1),
                             ('H', 3, 0), ('V', 2, 0), ('V', 0, 3),
                             ('H', '0', 0), ('H', True, 0), ('H', 0, 0)]:
                    with self.subTest(move=move), self.assertRaises(ValueError):
                        game.play_move(*move)
                    self.assertEqual(snapshot(game), original)

    def test_direct_board_calls_are_atomic(self):
        board = Board()
        for move in [('X', 0, 0), ('H', -1, 0), ('V', 3, 0)]:
            before = (repr(board.horizontal), repr(board.vertical), set(board.completed))
            with self.assertRaises(ValueError):
                board.add_line(*move)
            self.assertEqual((repr(board.horizontal), repr(board.vertical), board.completed), before)
        board.add_line('H', 0, 0)
        with self.assertRaisesRegex(ValueError, 'already occupied'):
            board.add_line('H', 0, 0)

    def test_completed_game_rejects_moves(self):
        game = DotsAndBoxes(vs_computer=True)
        game.board = Board(1, 1)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0), ('V', 0, 1)]:
            game.play_move(*move)
        self.assertEqual(sum(game.scores), 1)
        self.assertIsNone(choose_move(game.board))
        before = snapshot(game)
        with self.assertRaisesRegex(ValueError, 'already complete'):
            game.play_move('H', 0, 0)
        self.assertEqual(snapshot(game), before)

    def test_invalid_human_input_preserves_state(self):
        for mode in (False, True):
            game = DotsAndBoxes(vs_computer=mode)
            for raw in ('', 'H 0', 'X 0 0', 'H nope 0', 'H -1 0', 'V 0 99'):
                before = snapshot(game)
                with patch('builtins.input', return_value=raw), contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertIsNone(game.human_move())
                self.assertTrue(output.getvalue().strip())
                self.assertEqual(snapshot(game), before)

    def test_eof_in_both_modes(self):
        for mode in (False, True):
            game = DotsAndBoxes(vs_computer=mode)
            before = snapshot(game)
            with patch('builtins.input', side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()) as output:
                game.run()
            self.assertIn('Input ended', output.getvalue())
            self.assertEqual(snapshot(game), before)

    def test_eof_at_menu(self):
        with patch('builtins.input', side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()) as output:
            main()
        self.assertIn('Input ended', output.getvalue())

    def test_valid_scoring_and_extra_turns(self):
        game = DotsAndBoxes(vs_computer=True)
        game.board = Board(1, 2)
        for move in [('H', 0, 0), ('H', 1, 0), ('V', 0, 0),
                     ('H', 0, 1), ('H', 1, 1), ('V', 0, 2)]:
            game.play_move(*move)
        player = game.current
        self.assertEqual(game.play_move('V', 0, 1), 2)
        self.assertEqual(game.current, player)
        self.assertEqual(game.scores[player], 2)


if __name__ == '__main__':
    unittest.main()
