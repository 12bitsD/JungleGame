# Jungle Game (斗兽棋)

A Python implementation of the traditional Chinese board game "Dou Shou Qi" (Jungle Game).

## Features

✅ **Complete Game Rules**
- All 8 pieces with proper hierarchy (Elephant, Lion, Tiger, Leopard, Wolf, Dog, Cat, Rat)
- Special rules: Rat defeats Elephant, Lion/Tiger can jump rivers, Rat can swim
- Trap and Den mechanics
- Win/Draw conditions (Den occupation, no legal moves, 50-move rule, threefold repetition)

✅ **MVC Architecture**
- Separate `model/`, `view/`, and `controller/` packages
- Model layer completely independent of UI
- Follows all specification requirements

✅ **Save/Load System**
- Save games to JSON format
- Load previous games and continue playing
- Automatic timestamp recording

✅ **Undo/Redo** 
- Undo up to 10 moves
- Redo undone moves
- State preservation for captures

✅ **Replay System**
- Step through game history
- Auto-play with speed control
- Jump to specific moves

## Project Structure

```
JungleGame/
├── model/                  # Model layer (game logic)
│   ├── __init__.py
│   ├── piece.py           # Piece types and properties
│   ├── board.py           # 7×9 board with terrain
│   ├── move.py            # Move validation
│   └── game_state.py      # Game state management
├── view/                   # View layer (display)
│   ├── __init__.py
│   ├── cli_view.py        # Console interface
│   └── replay_engine.py   # Replay functionality
├── controller/             # Controller layer
│   ├── __init__.py
│   └── game_controller.py # Main game logic controller
├── main.py                 # Entry point
├── test_game.py            # Unit tests
└── README.md               # This file
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Installation

No installation required! Just run:

```bash
python3 main.py
```

## How to Play

### Starting the Game

```bash
cd /Users/bits12/Desktop/JungleGame
python3 main.py
```

### Commands

- **move <from> <to>** - Make a move
  - Example: `move E3 E4` (move piece from E3 to E4)
  
- **show <position>** - Show legal moves for a piece
  - Example: `show E3` (show where E3 piece can move)
  
- **undo** - Undo last move (up to 10 levels)
  
- **redo** - Redo previously undone move
  
- **history** - Display move history
  
- **save <filename>** - Save current game
  - Example: `save mygame` (saves to mygame.json)
  
- **load <filename>** - Load saved game
  - Example: `load mygame` (loads mygame.json)
  
- **new** - Start a new game
  
- **replay** - Enter replay mode
  - In replay mode:
    - `next` or `n` - Step forward
    - `prev` or `p` - Step backward
    - `goto <num>` - Jump to move number
    - `play` - Auto-play remaining moves
    - `exit` or `e` - Exit replay mode
  
- **quit** - Exit game

### Board Notation

- **Columns**: A-G (left to right)
- **Rows**: 1-9 (bottom to top, RED at bottom)
- **Example positions**: E3, D1, G7

### Piece Symbols

- **RED (lowercase)**:
  - `r` = Rat, `c` = Cat, `d` = Dog, `w` = Wolf
  - `l` = Leopard, `t` = Tiger, `n` = Lion, `e` = Elephant
  
- **BLUE (UPPERCASE)**:
  - `R` = Rat, `C` = Cat, `D` = Dog, `W` = Wolf
  - `L` = Leopard, `T` = Tiger, `N` = Lion, `E` = Elephant

### Terrain Symbols

- `·` = Normal land
- `≈` = Water (river)
- `△` = Trap
- `■` = Den

## Game Rules Summary

### Movement
- All pieces move 1 square orthogonally (up/down/left/right)
- Lion and Tiger can jump across rivers (3 squares)
- Only Rat can enter water

### Capture Rules
- Higher rank captures lower/equal rank
- **Special**: Rat (rank 1) defeats Elephant (rank 8)
- **Special**: Elephant cannot capture Rat
- Pieces in opponent's trap have rank 0 (can be captured by any piece)
- Rat in water cannot be captured by land pieces

### Win Conditions
1. Enter opponent's den
2. Opponent has no legal moves

### Draw Conditions
1. 50 consecutive moves without capture
2. Same position occurs 3 times

## Testing

Run the test suite:

```bash
python3 test_game.py
```

Tests cover:
- Board setup
- Basic movement
- Invalid move detection
- Special rules (Rat vs Elephant)
- Water movement
- Undo/Redo functionality
- Save/Load functionality

## Example Game Session

```
$ python3 main.py

Enter command: move E3 E4
✓ Move successful

Enter command: show G7
Legal moves for Lion at G7:
  G6
  F7

Enter command: move G7 G6

Enter command: history
--- Last 10 Moves ---
  1. RED Rat E3→E4
  2. BLUE Lion G7→G6

Enter command: save game1
✓ Game saved to game1.json

Enter command: undo
✓ Move undone

Enter command: replay
[Enters replay mode with step-by-step controls]
```

## Development Notes

### Code Style
- Follows PEP8 guidelines
- Type hints used for clarity
- Docstrings for all classes and methods

### Architecture
- **Model**: Pure game logic, no UI dependencies
- **View**: Display and input handling
- **Controller**: Coordinates model and view

### Extension Points
- Easy to add GUI (tkinter) by creating new view class
- AI player can be added by extending controller
- Network multiplayer possible by extending model

## Specification Compliance

This implementation strictly follows the project specification:

- ✅ Complete game rules (§ Appendix B)
- ✅ All user stories US1-US10 (§ Appendix C)
- ✅ MVC architecture with separate model package
- ✅ Standard library only (no external dependencies)
- ✅ Save/Load in JSON format
- ✅ Undo/Redo (10 levels)
- ✅ Replay system with controls
- ✅ Move history tracking
- ✅ Win/Draw detection

## Author

Developed for COMP3211 Project 2025

## License

Educational project for academic use.
