"""Basic greedy computer player for Dots and Boxes."""
import random
from rules import valid_move


def available_moves(board):
    """Return all currently legal, unoccupied edges."""
    moves = []
    for r in range(board.rows + 1):
        for c in range(board.cols):
            if valid_move(board, 'H', r, c):
                moves.append(('H', r, c))
    for r in range(board.rows):
        for c in range(board.cols + 1):
            if valid_move(board, 'V', r, c):
                moves.append(('V', r, c))
    return moves


def boxes_completed_by_move(board, move):
    """Count boxes this edge would complete without changing the board."""
    orientation, row, col = move
    if not valid_move(board, orientation, row, col):
        return 0
    adjacent = []
    if orientation == 'H':
        if row > 0:
            adjacent.append((row - 1, col))
        if row < board.rows:
            adjacent.append((row, col))
    else:
        if col > 0:
            adjacent.append((row, col - 1))
        if col < board.cols:
            adjacent.append((row, col))
    count = 0
    for r, c in adjacent:
        edges = (
            board.horizontal[r][c], board.horizontal[r + 1][c],
            board.vertical[r][c], board.vertical[r][c + 1],
        )
        if sum(edges) == 3:
            count += 1
    return count


def choose_move(board, rng=None):
    """Choose a legal move, prioritizing maximum immediate box completion."""
    moves = available_moves(board)
    if not moves:
        return None
    scores = [boxes_completed_by_move(board, move) for move in moves]
    highest = max(scores)
    best = [move for move, score in zip(moves, scores) if score == highest]
    return (rng or random).choice(best)
