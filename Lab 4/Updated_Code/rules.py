"""Move validation and scoring rules."""


def move_error(board, orientation, row, col):
    """Return an explanation for an illegal move, or None if it is legal."""
    if not isinstance(orientation, str) or orientation not in ('H', 'V'):
        return 'Invalid orientation. Use H (horizontal) or V (vertical).'
    if type(row) is not int or type(col) is not int:
        return 'Row and column must be integers.'
    if row < 0 or col < 0:
        return 'Coordinates cannot be negative.'
    if orientation == 'H':
        if row > board.rows or col >= board.cols:
            return f'Horizontal coordinates out of range: row 0-{board.rows}, column 0-{board.cols - 1}.'
        if board.horizontal[row][col]:
            return 'That line is already occupied.'
    else:
        if row >= board.rows or col > board.cols:
            return f'Vertical coordinates out of range: row 0-{board.rows - 1}, column 0-{board.cols}.'
        if board.vertical[row][col]:
            return 'That line is already occupied.'
    return None


def valid_move(board, orientation, row, col):
    return move_error(board, orientation, row, col) is None


def parse_move(raw):
    """Parse a command without modifying game state."""
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError('Empty input. Enter a move such as H 0 1.')
    parts = raw.strip().split()
    if len(parts) != 3:
        raise ValueError('Invalid format. Use H row col or V row col (example: H 0 1).')
    orientation, row_text, col_text = parts
    orientation = orientation.upper()
    if orientation not in ('H', 'V'):
        raise ValueError('Invalid orientation. Use H (horizontal) or V (vertical).')
    try:
        row, col = int(row_text), int(col_text)
    except ValueError:
        raise ValueError('Row and column must be integers.') from None
    return orientation, row, col


def completed_boxes(board, before):
    return len(board.completed - before)
