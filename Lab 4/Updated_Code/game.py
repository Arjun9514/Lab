from board import Board
from rules import move_error, parse_move, completed_boxes
from computer import choose_move


class DotsAndBoxes:
    def __init__(self, vs_computer=False):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]
        self.vs_computer = vs_computer

    def play_move(self, orientation, row, col):
        """Apply one legal move; return newly scored boxes.

        Invalid moves leave the game state and turn unchanged.
        """
        if self.board.is_complete():
            raise ValueError('Game is already complete. No further moves allowed.')
        error = move_error(self.board, orientation, row, col)
        if error:
            raise ValueError(error)
        before = set(self.board.completed)
        self.board.add_line(orientation, row, col)
        gained = completed_boxes(self.board, before)
        if gained:
            self.scores[self.current] += gained
        else:
            self.current = 1 - self.current
        return gained

    def human_move(self):
        """Return a validated move, None for invalid input, or raise EOFError."""
        raw = input(f'Player {self.current + 1}, move: ')
        try:
            move = parse_move(raw)
            if self.board.is_complete():
                raise ValueError('Game is already complete. No further moves allowed.')
            error = move_error(self.board, *move)
            if error:
                raise ValueError(error)
        except ValueError as exc:
            print(exc)
            return None
        return move

    def run(self):
        print('Dots and Boxes')
        print('Mode: Human vs Computer' if self.vs_computer else 'Mode: Human vs Human')
        print('Enter moves as H row col or V row col.')
        print('Rows and columns start at 0. Example: H 0 1')

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            player = self.current
            if self.vs_computer and player == 1:
                move = choose_move(self.board)
                if move is None:
                    break
                print(f'Computer plays: {move[0]} {move[1]} {move[2]}')
            else:
                try:
                    move = self.human_move()
                except EOFError:
                    print('\nInput ended. Exiting game without changing the current turn.')
                    return
                if move is None:
                    continue

            gained = self.play_move(*move)
            if gained:
                name = 'Computer' if self.vs_computer and player == 1 else f'Player {player + 1}'
                print(f'{name} completed {gained} box(es) and plays again.')

        self.board.display(self.scores, self.current)
        print('Game over!')
        if self.scores[0] == self.scores[1]:
            print('The game is a draw.')
        else:
            winner = 0 if self.scores[0] > self.scores[1] else 1
            name = 'Computer' if self.vs_computer and winner == 1 else f'Player {winner + 1}'
            print(f'{name} wins!')
