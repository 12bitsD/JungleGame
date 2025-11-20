# Jungle Game - Testing Guide

## Quick Start

### Run All Tests
```bash
python3 test_model_complete.py
```

### Run Specific Test Class
```bash
python3 -m unittest test_model_complete.TestPieceHierarchy
python3 -m unittest test_model_complete.TestBoard
python3 -m unittest test_model_complete.TestMoveValidator
python3 -m unittest test_model_complete.TestGameState
python3 -m unittest test_model_complete.TestIntegration
```

### Run Single Test
```bash
python3 -m unittest test_model_complete.TestPieceHierarchy.test_rat_properties
python3 -m unittest test_model_complete.TestMoveValidator.test_capture_rat_defeats_elephant
```

### Verbose Output
```bash
python3 test_model_complete.py -v
```

---

## Test Files

### Primary Test Suite
- **`test_model_complete.py`** (NEW)
  - 86 comprehensive tests
  - 100% Model package coverage
  - All game rules validated

### Legacy Test Suite
- **`test_game.py`** (ORIGINAL)
  - 7 basic integration tests
  - Still functional, but superseded by comprehensive suite

---

## Test Categories

### 1. Piece Tests (13 tests)
**What they test:**
- Piece type properties (rank, symbol, name)
- Polymorphic behavior (can_swim, can_jump)
- Serialization/deserialization
- Factory pattern

**Example:**
```python
def test_rat_properties(self):
    rat = Rat(Player.RED, 2, 4)
    self.assertEqual(rat.rank, 1)
    self.assertTrue(rat.can_swim())
```

**Run:**
```bash
python3 -m unittest test_model_complete.TestPieceHierarchy
```

---

### 2. Board Tests (14 tests)
**What they test:**
- Grid initialization (7×9)
- Terrain management (water, traps, dens)
- Piece operations (get, set, move, remove)
- Notation conversions
- Deep copying

**Example:**
```python
def test_water_squares_count(self):
    water_count = sum(
        1 for row in range(9) for col in range(7)
        if self.board.is_water(row, col)
    )
    self.assertEqual(water_count, 12)
```

**Run:**
```bash
python3 -m unittest test_model_complete.TestBoard
```

---

### 3. Move Validator Tests (25 tests)
**What they test:**
- Basic movement (1-square, orthogonal)
- Terrain rules (water, traps, dens)
- Capture hierarchy
- Special rules (Rat-Elephant, Rat swimming, jump blocking)
- Legal move generation

**Example:**
```python
def test_capture_rat_defeats_elephant(self):
    rat = Rat(Player.RED, 2, 3)
    elephant = Elephant(Player.BLUE, 3, 3)
    self.board.set_piece(2, 3, rat)
    self.board.set_piece(3, 3, elephant)
    
    valid, _ = self.validator.is_valid_move(rat, 3, 3)
    self.assertTrue(valid)  # Rat can beat Elephant
```

**Run:**
```bash
python3 -m unittest test_model_complete.TestMoveValidator
```

---

### 4. GameState Tests (26 tests)
**What they test:**
- Game initialization
- Move execution
- Turn management
- Win/draw conditions
- Undo/redo system (10 levels)
- Save/load (JSON)
- Captured pieces tracking

**Example:**
```python
def test_undo_redo_sequence(self):
    game.make_move(2, 4, 3, 4)  # Move 1
    game.make_move(6, 2, 5, 2)  # Move 2
    game.undo()                 # Undo move 2
    game.redo()                 # Redo move 2
    self.assertEqual(game.current_player, Player.RED)
```

**Run:**
```bash
python3 -m unittest test_model_complete.TestGameState
```

---

### 5. Integration Tests (4 tests)
**What they test:**
- Complete game scenarios
- Multi-move sequences
- Special rule interactions
- State persistence

**Example:**
```python
def test_full_game_scenario(self):
    moves = [
        (2, 4, 3, 4),  # RED rat
        (6, 2, 5, 2),  # BLUE rat
        (3, 4, 4, 4),  # RED rat
        (5, 2, 4, 2),  # BLUE rat
    ]
    for move in moves:
        success, _ = game.make_move(*move)
        self.assertTrue(success)
```

**Run:**
```bash
python3 -m unittest test_model_complete.TestIntegration
```

---

## Understanding Test Output

### Successful Run
```
test_rat_properties (__main__.TestPieceHierarchy.test_rat_properties)
Test Rat piece properties. ... ok

----------------------------------------------------------------------
Ran 86 tests in 0.004s

OK
```

### Failed Test
```
FAIL: test_capture_rat_defeats_elephant (__main__.TestMoveValidator)
Test special rule: Rat defeats Elephant.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_model_complete.py", line 485, in test_capture_rat_defeats_elephant
    self.assertTrue(valid)
AssertionError: False is not true
```

**How to debug:**
1. Find the test in `test_model_complete.py` (line 485)
2. Read the test scenario
3. Check the assertion that failed
4. Verify the corresponding Model code

---

## Test Data Setup

### No External Files Needed
All tests create their own data:
- Board states created programmatically
- Pieces instantiated as needed
- Temporary JSON files for save/load tests (auto-cleaned)

### Cleanup
Tests automatically clean up:
```python
# Cleanup example from save/load test
os.remove("test_save.json")
```

---

## Adding New Tests

### 1. Choose Test Class
```python
class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()  # Fresh board for each test
```

### 2. Write Test Method
```python
def test_my_new_feature(self):
    """Test description for clarity."""
    # Arrange
    rat = Rat(Player.RED, 2, 4)
    self.board.set_piece(2, 4, rat)
    
    # Act
    result = self.board.get_piece(2, 4)
    
    # Assert
    self.assertEqual(result, rat)
```

### 3. Run New Test
```bash
python3 -m unittest test_model_complete.TestBoard.test_my_new_feature
```

---

## Coverage Checklist

### When writing new Model code, ensure tests cover:
- ✅ **Happy path** - Normal expected usage
- ✅ **Edge cases** - Boundary conditions (e.g., board edges)
- ✅ **Error cases** - Invalid inputs, out-of-bounds
- ✅ **Special rules** - Game-specific mechanics
- ✅ **State changes** - Verify side effects
- ✅ **Return values** - Check both success and error returns

---

## Performance Expectations

| Test Suite | Tests | Expected Time |
|------------|-------|---------------|
| TestPieceHierarchy | 13 | < 1ms |
| TestBoard | 14 | < 1ms |
| TestMoveValidator | 25 | < 2ms |
| TestGameState | 26 | < 1ms |
| TestIntegration | 4 | < 1ms |
| **Total** | **86** | **< 5ms** |

If tests run slower:
- Check for file I/O issues
- Verify no blocking operations
- Ensure proper test isolation

---

## Continuous Integration

### Pre-commit Hook (Recommended)
```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 test_model_complete.py
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

### GitHub Actions (Future)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python3 test_model_complete.py
```

---

## Troubleshooting

### Import Errors
```
ModuleNotFoundError: No module named 'model'
```
**Solution:** Run from project root directory
```bash
cd /path/to/JungleGame
python3 test_model_complete.py
```

### File Not Found (Save/Load Tests)
```
FileNotFoundError: [Errno 2] No such file or directory: 'test_save.json'
```
**Solution:** Check file permissions and working directory

### Random Test Failures
**Cause:** Likely test isolation issue
**Solution:** Verify `setUp()` creates fresh state for each test

---

## Test Philosophy

### Why 86 Tests?
- **Confidence**: Every Model method tested
- **Documentation**: Tests show intended usage
- **Refactoring Safety**: Tests catch regressions
- **Academic Rigor**: Demonstrates thorough engineering

### Test-Driven Development (TDD)
```
1. Write failing test
2. Implement minimal code to pass
3. Refactor while keeping tests green
4. Repeat
```

---

## Resources

- **Test Coverage Report**: `TEST_COVERAGE_REPORT.md`
- **Architecture Docs**: `ARCHITECTURE.md`
- **Game Rules**: `JungleGame_Spec.md`
- **Python unittest docs**: https://docs.python.org/3/library/unittest.html

---

## Quick Commands Reference

```bash
# Run all tests
python3 test_model_complete.py

# Run with verbose output
python3 test_model_complete.py -v

# Run specific test class
python3 -m unittest test_model_complete.TestPieceHierarchy

# Run specific test method
python3 -m unittest test_model_complete.TestPieceHierarchy.test_rat_properties

# Run tests matching pattern
python3 -m unittest discover -s . -p "test_*.py"

# Count test cases
grep -c "def test_" test_model_complete.py
```

---

**Total Tests**: 86  
**Pass Rate**: 100%
