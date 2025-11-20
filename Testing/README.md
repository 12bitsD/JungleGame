# Unit Testing Documentation

## Overview
This directory contains the unit test suite for the Jungle Game Model.
The tests are designed to verify the correctness of the game logic, including piece movement, board management, and game state transitions.

## Test Structure
The tests are organized into separate modules, each focusing on a specific component of the application:

*   **`test_piece.py`**:
    *   Verifies the Factory Pattern implementation (`Piece.create`).
    *   Checks intrinsic properties of pieces (Rank, Name, Owner).
    *   Tests polymorphic behaviors (`can_swim`, `can_jump`).
    *   Ensures correct serialization (`to_dict`/`from_dict`).

*   **`test_board.py`**:
    *   Verifies the grid structure (9 rows x 7 columns).
    *   Checks proper initialization of terrain (Dens, Traps, Rivers).
    *   Tests the initial setup of pieces on the board.
    *   Validates basic `move_piece` mechanics (updating internal grid state).
    *   Checks boundary conditions (`is_valid_position`).

*   **`test_move_validator.py`**:
    *   **Core Logic Tests**: This is the most critical test file.
    *   Verifies standard movement (1 step orthogonal).
    *   Tests River rules (Rat can swim, others cannot).
    *   Tests Jumping rules (Lion/Tiger jump over river, blocked by Rat).
    *   Tests Capture logic (Rank hierarchy, Trap effectiveness).
    *   Tests Den protection (cannot enter own Den).

*   **`test_move.py`**:
    *   Verifies `Move` object serialization.
    *   Tests standard algebraic notation generation (e.g., "A1->B1").

*   **`test_game_state.py`**:
    *   Verifies the Game Loop flow (Turn switching).
    *   Tests **Undo/Redo** functionality (verifying state rollback).
    *   Tests **Save/Load** functionality (serialization consistency).
    *   Verifies Win Conditions (occupying opponent's Den).

## Execution
To run all tests and generate a coverage report:

```bash
# Run tests with coverage
python3 -m coverage run -m unittest discover Testing

# Display report in terminal
python3 -m coverage report -m --include="model/*"

# Generate HTML report (optional)
python3 -m coverage html
```

