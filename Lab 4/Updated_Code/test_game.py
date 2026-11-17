import itertools
import random
import unittest
from board import Board
from computer import available_moves, boxes_completed_by_move, choose_move
from game import DotsAndBoxes


class GameTests(unittest.TestCase):
    def test_computer_never_plays_occupied_edge(self):
        for seed in range(50):
            game = DotsAndBoxes(vs_computer=True)
            rng = random.Random(seed)
            while not game.board.is_complete():
                legal = available_moves(game.board)
                move = choose_move(game.board, rng)
                self.assertIn(move, legal)
                game.play_move(*move)
            self.assertEqual(sum(game.scores), 4)

    def test_computer_prioritizes_double_box(self):
        board = Board(1, 2)
        for move in [('H',0,0),('H',1,0),('V',0,0),('H',0,1),('H',1,1),('V',0,2)]:
            board.add_line(*move)
        self.assertEqual(choose_move(board), ('V',0,1))
        self.assertEqual(boxes_completed_by_move(board, ('V',0,1)), 2)

    def test_extra_turn_and_invalid_move(self):
        game = DotsAndBoxes()
        for move in [('H',0,0),('H',1,0),('V',0,0)]:
            game.play_move(*move)
        player = game.current
        self.assertEqual(game.play_move('V',0,1), 1)
        self.assertEqual(game.current, player)
        self.assertEqual(game.scores[player], 1)
        with self.assertRaises(ValueError):
            game.play_move('V',0,1)
        self.assertEqual(game.current, player)
        self.assertEqual(game.scores[player], 1)

    def test_all_sequences_one_by_two(self):
        board = Board(1, 2)
        edges = available_moves(board)
        for order in itertools.permutations(edges):
            game = DotsAndBoxes()
            game.board = Board(1, 2)
            for move in order:
                old_player = game.current
                before = len(game.board.completed)
                gained = game.play_move(*move)
                self.assertEqual(gained, len(game.board.completed) - before)
                self.assertEqual(game.current, old_player if gained else 1-old_player)
                self.assertEqual(sum(game.scores), len(game.board.completed))
            self.assertEqual(sum(game.scores), 2)


if __name__ == '__main__':
    unittest.main()
