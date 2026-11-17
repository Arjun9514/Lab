# Dots and Boxes

A terminal-based Python Dots and Boxes game with Human vs Human and Human vs Computer modes. Uses only the Python standard library.

## Run

```bash
python main.py
```

Select `1` for Human vs Human or `2` for Human vs Computer. The human is Player 1 and the computer is Player 2. Enter edges using `H row col` or `V row col`, with zero-based coordinates, for example `H 0 1`. Input is case-insensitive. The default board has 2 rows and 2 columns of boxes.

## Run automated tests

From the project directory:

```bash
python -m unittest discover -v
```

The suite uses `unittest` from the standard library. `test_regression.py` covers legal horizontal and vertical edges, invalid and repeated moves, single- and double-box completion, points, extra turns, game-over behavior, state immutability after rejected moves, and computer move legality and priority. `test_game.py` additionally checks all 5,040 edge orders on a 1×2 board, and `test_validation.py` covers parsing and EOF handling.

## Design decisions

- **Modular responsibilities:** `board.py` owns the edge grids and completed-box set; `rules.py` owns command parsing, move validation, and score deltas; `game.py` owns players, scores, turns, and the gameplay loop; `computer.py` chooses computer moves; `main.py` contains the mode menu.
- **One move path:** Human and computer moves both go through `DotsAndBoxes.play_move()`, so the same validation, scoring, and extra-turn rules apply.
- **Atomic invalid moves:** Validate before changing any edge, completed-box record, score, or current player. Both the game method and direct board mutation reject invalid moves with `ValueError`.
- **Score only new boxes:** The board stores completed boxes in a set. The game compares completed boxes before and after a move; a move closing two boxes scores two points. A scoring player keeps the turn; otherwise the turn alternates.
- **Computer policy:** Enumerate valid unoccupied edges and choose among moves with the highest immediate box-completion count; break ties randomly. This is a simple greedy opponent, not an optimal solver. Move evaluation does not mutate the board.
- **Completion:** A game ends once every edge is occupied. Subsequent attempts to play are rejected without changing state. EOF exits the terminal session gracefully.
- **Testing:** Tests use small boards and deterministic random generators where helpful. They assert both outcomes and state invariants, rather than relying only on printed messages.

## File layout

```text
board.py             Board storage, completion tracking, rendering
rules.py             Parsing, validation, scoring delta
computer.py          Greedy computer opponent
game.py              Shared turn and score management
main.py              Mode selection and entry point
test_game.py         Existing scoring/AI sequence tests
test_validation.py   Existing input validation tests
test_regression.py   Additional behavior and state-invariant tests
```
