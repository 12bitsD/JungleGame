# Jungle Game (斗兽棋) - Project Specification

## Project Overview
Implementation of the traditional Chinese board game "Jungle Game" (Dou Shou Qi) with full game mechanics, save/load functionality, undo/redo, and replay features.

**Target**: Achieve maximum score through complete implementation of all requirements with clean MVC architecture.

---

## Appendix B: Game Rules (游戏规则) - Complete Specification

### 1. Board Layout (棋盘布局)

#### 1.1 Grid Structure
- **Dimensions**: 7 columns (A-G) × 9 rows (1-9)
- **Coordinate System**: 
  - Columns labeled A-G (left to right)
  - Rows labeled 1-9 (top to bottom from RED's perspective)
  - Example: Bottom-left corner is A1, top-right is G9

#### 1.2 Special Squares (Exact Positions)

**RED Player (Bottom, Rows 1-3)**:
- **RED Den (红方兽穴)**: D1
- **RED Traps (红方陷阱)**: C1, E1, D2

**BLUE Player (Top, Rows 7-9)**:
- **BLUE Den (蓝方兽穴)**: D9
- **BLUE Traps (蓝方陷阱)**: C9, E9, D8

**Rivers (河流)**: Two 3×2 water zones
- **Left River**: Columns A-B, Rows 4-6
  - Squares: A4, B4, A5, B5, A6, B6
- **Right River**: Columns F-G, Rows 4-6
  - Squares: F4, G4, F5, G5, F6, G6

**Normal Land**: All other 49 squares

```
   A  B  C  D  E  F  G
9  .  .  T  D  T  .  .   BLUE
8  .  .  .  T  .  .  .
7  .  .  .  .  .  .  .
6  W  W  .  .  .  W  W
5  W  W  .  .  .  W  W   River
4  W  W  .  .  .  W  W
3  .  .  .  .  .  .  .
2  .  .  .  T  .  .  .
1  .  .  T  D  T  .  .   RED

Legend: D=Den, T=Trap, W=Water, .=Normal
```

### 2. Pieces and Hierarchy (棋子等级)

#### 2.1 Piece Types
Each player controls 8 unique pieces:

| Rank | Piece | 中文 | Power | Special Abilities |
|------|-------|------|-------|-------------------|
| 8 | Elephant | 象 | 8 | Cannot enter water, defeated only by Rat |
| 7 | Lion | 狮 | 7 | Can jump over river (horizontally/vertically) |
| 6 | Tiger | 虎 | 6 | Can jump over river (horizontally/vertically) |
| 5 | Leopard | 豹 | 5 | None |
| 4 | Wolf | 狼 | 4 | None |
| 3 | Dog | 狗 | 3 | None |
| 2 | Cat | 猫 | 2 | None |
| 1 | Rat | 鼠 | 1 | Can swim, can defeat Elephant, can attack from/to water |

#### 2.2 Initial Setup (Starting Positions)

**RED Pieces (Rows 1-3)**:
```
Row 3: Lion(A3), Dog(B3), Cat(C3), Rat(E3), Leopard(F3), Tiger(G3)
Row 2: [empty except: Elephant(D2)]
Row 1: [empty except: Wolf(D1) is NOT placed - Wolf at C1]
```

**Corrected RED Starting Positions**:
- A3: Lion (狮)
- B3: Dog (狗) 
- C3: Cat (猫)
- D2: Elephant (象)
- E3: Rat (鼠)
- F3: Leopard (豹)
- G3: Tiger (虎)
- C1: Wolf (狼)

**BLUE Pieces (Rows 7-9)** - Mirror of RED:
- A7: Tiger (虎)
- B7: Leopard (豹)
- C7: Rat (鼠)
- D8: Elephant (象)
- E7: Cat (猫)
- F7: Dog (狗)
- G7: Lion (狮)
- E9: Wolf (狼)

**Note**: Each player starts with all 8 pieces. Setup is symmetric (rotational symmetry).

### 3. Movement Rules (移动规则)

#### 3.1 Basic Movement
- **Direction**: All pieces move **one square per turn** in 4 directions:
  - Up, Down, Left, Right (orthogonal only, NO diagonal movement)
- **Mandatory Move**: Player must move if any legal move exists
- **Turn Order**: RED moves first, then players alternate

#### 3.2 Movement by Terrain

**On Land (Normal/Trap/Den Squares)**:
- All pieces can move to adjacent land squares (if not blocked by own piece)

**On Water (River Squares)**:
- **Only RAT** can enter and stay in water squares
- RAT in water moves normally (one square at a time within water or to land)
- All other pieces: CANNOT enter water squares

#### 3.3 Special Movements

**Lion & Tiger Jumping (跳河)**:
- Can jump **across the entire river** (3 squares) in one move
- Jump direction: Horizontal or Vertical only
- **Requirements**:
  - Must jump from land square adjacent to river
  - Must land on land square on opposite side of river
  - Jump path must be clear (no Rat in any of the 3 water squares being crossed)
- **Example**: 
  - Tiger at C4 can jump to C7 (if A5, A6 have no Rat)
  - Lion at A3 can jump to A7 (if A4, A5, A6 have no Rat)
  
**Rat Swimming (游泳)**:
- Rat can move from land to water, water to water, or water to land
- Rat in water can attack pieces on land (see Capture Rules)

### 4. Capture Rules (捕获规则) - Complete Specification

#### 4.1 General Capture Rule
A piece captures by **moving into** a square occupied by an opponent's piece.

**Standard Hierarchy**:
- Higher-ranked piece defeats lower-ranked piece
- Equal-ranked pieces can capture each other
- Formal: Piece with rank R can capture opponent piece with rank ≤ R

#### 4.2 Special Capture Rules

**Rule 1: Rat defeats Elephant**
- **RAT (rank 1)** is the ONLY piece that can capture **ELEPHANT (rank 8)**
- Elephant CANNOT capture Rat
- Exception applies regardless of terrain (land or water)

**Rule 2: Rat in Water**
- Rat in water can attack opponent pieces on adjacent land squares
- Rat on land can attack Rat in adjacent water square
- **Important**: Land pieces (not Rat) CANNOT attack Rat in water
  - Example: Elephant on C4 CANNOT capture Rat on B4 (water)

**Rule 3: Traps (see § 4.3)**

**Rule 4: Pieces on Land vs Rat in Water**
- Non-Rat pieces on land **cannot** capture Rat in water (even if adjacent)
- Only Rat can enter water to fight Rat

#### 4.3 Trap Effects (陷阱效果)

**Entering Opponent's Trap**:
- Piece entering opponent's trap has **rank reduced to 0** (temporarily)
- While in trap (rank 0), can be captured by ANY opponent piece (including rank 1 Rat)
- **Example**: Elephant (rank 8) in opponent trap can be captured by opponent's Cat (rank 2)

**Own Traps**:
- Pieces in their own traps are **not** affected (retain full rank)

**Leaving Trap**:
- Piece regains full rank immediately upon leaving trap square

**Trap Locations**:
- RED traps (affect BLUE pieces): C1, E1, D2
- BLUE traps (affect RED pieces): C9, E9, D8

### 5. Den Rules (兽穴规则)

#### 5.1 Den Entry Rules
- **Own Den**: Pieces **cannot** enter their own den (illegal move)
- **Opponent Den**: Any piece can enter opponent's den

#### 5.2 Winning by Den Entry
- When **any piece** successfully enters **opponent's den**:
  - Game ends immediately
  - Player who entered opponent's den **wins**
  - No other win condition can trigger simultaneously

### 6. Win/Loss/Draw Conditions (胜负判定)

#### 6.1 Win Conditions (胜利)
**Condition W1: Den Occupation** (Primary Win Condition)
- Any player's piece enters opponent's den → That player wins immediately

**Condition W2: Opponent Has No Legal Moves**
- If a player has no legal moves on their turn → That player loses (opponent wins)
- All pieces blocked or captured

#### 6.2 Draw Conditions (平局)
**Condition D1: Move Limit Without Capture**
- If **50 consecutive moves** (25 per player) occur with NO captures → Draw
- Counter resets to 0 after any capture

**Condition D2: Threefold Repetition**
- If **exact same board position** occurs **3 times** → Draw
- Position includes: piece positions + current player's turn

**Condition D3: Mutual Agreement**
- Both players agree to draw (optional rule, not mandatory to implement)

#### 6.3 Edge Cases
- **No Draw by Insufficient Material**: Unlike chess, game continues even if only 1 piece remains
- **Perpetual Check**: Not applicable (no check concept in this game)

### 7. Complete Move Validation Algorithm (伪代码)

```
function isValidMove(piece, fromSquare, toSquare):
    // 1. Basic checks
    if distance(fromSquare, toSquare) != 1 AND not isJump(piece, fromSquare, toSquare):
        return false
    if not isOrthogonal(fromSquare, toSquare):
        return false  // No diagonal
    
    // 2. Terrain checks
    if toSquare is WATER:
        if piece is not RAT:
            return false
    
    // 3. Jump validation (Lion/Tiger)
    if isJump(piece, fromSquare, toSquare):
        if piece is not LION and piece is not TIGER:
            return false
        if not isRiverJumpPath(fromSquare, toSquare):
            return false
        if isRatInJumpPath(fromSquare, toSquare):
            return false  // Blocked by rat
    
    // 4. Den entry check
    if toSquare is DEN:
        if toSquare is piece.owner's den:
            return false  // Cannot enter own den
    
    // 5. Friendly piece collision
    if toSquare has piece of same owner:
        return false
    
    // 6. Capture validation
    if toSquare has opponent piece:
        return canCapture(piece, fromSquare, toSquare)
    
    return true

function canCapture(attacker, attackerSquare, defenderSquare):
    defender = getPieceAt(defenderSquare)
    
    // Rat in water protection
    if defender is RAT and defenderSquare is WATER:
        if attacker is not RAT:
            return false  // Only Rat can attack Rat in water
    
    // Trap effect
    attackerRank = attacker.rank
    if attackerSquare is opponent's TRAP:
        attackerRank = 0
    
    defenderRank = defender.rank
    if defenderSquare is opponent's TRAP:
        defenderRank = 0
    
    // Special rule: Rat defeats Elephant
    if attacker is RAT and defender is ELEPHANT:
        return true
    if attacker is ELEPHANT and defender is RAT:
        return false
    
    // General hierarchy
    return attackerRank >= defenderRank
```

---

## Appendix C: User Stories (US1-US10) - Detailed Requirements

### Category 1: Core Gameplay (Must-Have)

#### **US1: Start New Game**
**As a** player  
**I want to** start a new game  
**So that** I can begin a fresh match

**Acceptance Criteria**:
1. ✅ System displays a "New Game" button/menu option
2. ✅ When clicked, board resets to initial setup (see § 2.2)
3. ✅ All 16 pieces placed in starting positions
4. ✅ Current player set to RED
5. ✅ Move history cleared
6. ✅ Game status set to "In Progress"
7. ✅ UI displays "RED's Turn" message

**Technical Notes**:
- Clear undo/redo stacks
- Reset move counter (for 50-move rule)
- Clear position repetition history

---

#### **US2: Move Pieces**
**As a** player  
**I want to** move my pieces according to game rules  
**So that** I can make strategic moves

**Acceptance Criteria**:
1. ✅ Player can select own piece by clicking
2. ✅ **Legal move highlighting**:
   - System highlights all valid destination squares
   - Different color for empty squares vs capture moves
3. ✅ Player clicks destination square to move
4. ✅ **Move validation**:
   - Only current player's pieces are selectable
   - Movement follows rules in § 3 (direction, terrain, jump)
   - Invalid moves are rejected with error message
5. ✅ **Move execution**:
   - Piece position updated
   - If capture occurs, opponent piece removed
   - Turn switches to opponent
   - UI updates to show new board state
6. ✅ **Deselection**: Click same piece again or click empty space to deselect

**Error Messages**:
- "Not your turn" - if selecting opponent's piece
- "Invalid move" - if destination violates rules
- "Cannot enter water" - if non-Rat tries to enter river
- "Jump blocked by Rat" - if Lion/Tiger jump path has Rat

---

#### **US3: Capture Opponent Pieces**
**As a** player  
**I want to** capture opponent pieces following game rules  
**So that** I can gain advantage

**Acceptance Criteria**:
1. ✅ **Valid captures** (see § 4):
   - Higher rank captures lower/equal rank
   - Rat can capture Elephant
   - Elephant CANNOT capture Rat
   - Pieces in opponent's trap can be captured by any piece
   - Rat in water can only be captured by Rat
2. ✅ **Capture execution**:
   - Captured piece removed from board
   - Captured piece displayed in "Captured Pieces" area
   - Move counter (for 50-move rule) resets to 0
3. ✅ **Invalid captures blocked**:
   - Lower rank cannot capture higher rank (except Rat vs Elephant)
   - Land pieces cannot capture Rat in water
   - Elephant cannot capture Rat anywhere

**Visual Feedback**:
- Highlight capturable pieces in different color (e.g., red)
- Show capture animation (optional but recommended)

---

#### **US4: Win/Draw Detection**
**As a** player  
**I want** the system to detect game end conditions  
**So that** the winner is correctly determined

**Acceptance Criteria**:
1. ✅ **Win by Den Entry** (§ 5.2):
   - Any piece entering opponent's den triggers win
   - Game ends immediately
   - Message: "[Player] wins by entering the den!"
2. ✅ **Win by No Legal Moves** (§ 6.1 W2):
   - If current player has no legal moves, they lose
   - Message: "[Player] wins! Opponent has no legal moves."
3. ✅ **Draw by 50-Move Rule** (§ 6.2 D1):
   - Track moves without capture
   - At 50 moves, declare draw
   - Message: "Draw by 50-move rule"
4. ✅ **Draw by Repetition** (§ 6.2 D2):
   - Track board positions
   - If same position occurs 3 times, declare draw
   - Message: "Draw by threefold repetition"
5. ✅ **End Game Actions**:
   - Disable further moves
   - Display "New Game" button
   - Optionally show game summary

**Technical Notes**:
- Position hash: Include piece locations + current player
- Move counter: Increment each turn, reset on capture

---

### Category 2: Data Persistence (Must-Have)

#### **US5: Save Game**
**As a** player  
**I want to** save the current game state  
**So that** I can resume later

**Acceptance Criteria**:
1. ✅ System provides "Save Game" button/menu
2. ✅ **Save Dialog**:
   - User enters filename (default: "jungle_game_YYYYMMDD_HHMMSS.json")
   - System validates filename
3. ✅ **Data Saved**:
   - Current board state (all piece positions)
   - Current player (RED/BLUE)
   - Move history (full game record)
   - Move counter (for 50-move rule)
   - Position history (for repetition detection)
   - Timestamp
4. ✅ **File Format**: JSON or serialized object (see § Technical Requirements)
5. ✅ **Confirmation**: "Game saved successfully to [filename]"
6. ✅ **Error Handling**:
   - "Failed to save: [reason]" if write fails
   - Validate file path

**Example JSON Structure**:
```json
{
  "timestamp": "2025-11-19T14:30:00",
  "currentPlayer": "RED",
  "moveCount": 15,
  "board": [
    ["BLUE_TIGER", null, "BLUE_RAT", ...],
    ...
  ],
  "moveHistory": [
    {"piece": "RED_RAT", "from": "E3", "to": "E4", "captured": null},
    ...
  ]
}
```

---

#### **US6: Load Game**
**As a** player  
**I want to** load a previously saved game  
**So that** I can continue from where I left off

**Acceptance Criteria**:
1. ✅ System provides "Load Game" button/menu
2. ✅ **Load Dialog**:
   - File browser to select save file
   - Show available save files (*.json)
3. ✅ **Validation**:
   - Check file format is correct
   - Verify data integrity (all required fields present)
4. ✅ **State Restoration**:
   - Reconstruct board from saved positions
   - Set current player
   - Restore move history (for undo/replay)
   - Restore move counter
   - Restore position history
5. ✅ **UI Update**:
   - Render loaded board state
   - Display whose turn it is
   - Message: "Game loaded from [filename]"
6. ✅ **Error Handling**:
   - "File not found" 
   - "Invalid save file format"
   - "Corrupted save file"

**Technical Notes**:
- Validate piece positions (no two pieces on same square)
- Validate player has legal moves (prevent loading stuck position)

---

### Category 3: Undo/Redo (High-Value)

#### **US7: Undo Move**
**As a** player  
**I want to** undo my last move  
**So that** I can correct mistakes or try different strategies

**Acceptance Criteria**:
1. ✅ System provides "Undo" button
2. ✅ **Undo Limit**: Can undo up to **last 10 moves**
3. ✅ **Undo Execution**:
   - Revert last move (piece returns to previous position)
   - If move was a capture, restore captured piece
   - Switch current player back
   - Decrement move counter if needed
4. ✅ **Undo Stack**:
   - Store up to 10 game states OR 10 move records
   - FIFO: oldest state removed when stack full
5. ✅ **Button State**:
   - Disabled when no moves to undo (game start)
   - Disabled when undo stack empty
6. ✅ **UI Feedback**:
   - Board reverts to previous state
   - Message: "Move undone" (optional)

**Technical Notes**:
- **Option A**: Store complete GameState snapshots (simpler)
- **Option B**: Store move deltas (more memory-efficient)
- Redo stack is cleared when new move is made

---

#### **US8: Redo Move**
**As a** player  
**I want to** redo a previously undone move  
**So that** I can restore moves I undid by mistake

**Acceptance Criteria**:
1. ✅ System provides "Redo" button
2. ✅ **Redo Execution**:
   - Re-execute the last undone move
   - Update board state
   - Switch current player
3. ✅ **Redo Stack**:
   - Populated when Undo is performed
   - Cleared when new move is made (not undo)
4. ✅ **Button State**:
   - Disabled when no moves to redo
   - Enabled after Undo is performed
5. ✅ **UI Feedback**:
   - Board advances to next state
   - Message: "Move redone" (optional)

**Behavior Examples**:
```
Scenario 1: Normal Undo/Redo
1. Make moves A, B, C
2. Undo → back to state after B (can redo C)
3. Undo → back to state after A (can redo B, C)
4. Redo → state after B (can redo C)
5. Redo → state after C (no more redos)

Scenario 2: Undo then New Move
1. Make moves A, B, C
2. Undo → back to state after B
3. Make new move D
4. Redo button disabled (move C lost)
```

---

### Category 4: Replay System (High-Value)

#### **US9: View Move History**
**As a** player  
**I want to** view the history of all moves  
**So that** I can review the game's progression

**Acceptance Criteria**:
1. ✅ System provides "History" button/panel
2. ✅ **Display Format**:
   - List of moves in chronological order
   - Move notation: `[#] [Player] [Piece] [From]→[To] [Captured?]`
   - Example: 
     ```
     1. RED Rat E3→E4
     2. BLUE Lion G7→F7
     3. RED Rat E4→E5 (captured BLUE Cat)
     ```
3. ✅ **Scrollable List**: If many moves, provide scrollbar
4. ✅ **Current Move Indicator**: Highlight current position in history
5. ✅ **Click to Jump** (optional but recommended):
   - Click any move in history
   - Board jumps to that state
   - User can resume from there OR continue viewing

**Technical Notes**:
- Store move history as list: `List<Move>`
- Move object: `{moveNumber, player, piece, from, to, captured}`

---

#### **US10: Replay Game**
**As a** player  
**I want to** replay a game step-by-step automatically  
**So that** I can review completed games or analyze strategies

**Acceptance Criteria**:
1. ✅ **Replay Button**: System provides "Replay" button/mode
2. ✅ **Replay Activation**:
   - Can activate during game OR after game ends
   - Board resets to starting position
   - Replay controls appear
3. ✅ **Automatic Playback**:
   - Moves execute automatically with time delay
   - Default speed: 1 second per move
4. ✅ **Replay Controls**:
   - ▶️ **Play/Pause**: Start/stop automatic playback
   - ⏮️ **Step Back**: Go to previous move
   - ⏭️ **Step Forward**: Go to next move
   - ⏹️ **Stop**: Exit replay mode, return to current game
   - 🔄 **Restart**: Reset to beginning of replay
5. ✅ **Speed Control**:
   - Slider or buttons for speed: 0.5x, 1x, 2x, 5x
   - Speed setting: interval between moves
6. ✅ **Progress Indicator**:
   - Show current move number / total moves
   - Example: "Move 15 / 42"
   - Progress bar (optional)
7. ✅ **Visual Feedback**:
   - Highlight last moved piece
   - Show move notation on screen
   - Optionally show captured pieces accumulating

**Replay Modes** (Optional Advanced Feature):
- **Mode 1**: Replay entire game from start
- **Mode 2**: Replay from current position to end
- **Mode 3**: Replay specific move range (e.g., moves 10-20)

**Technical Implementation**:
```java
class ReplayEngine {
    private List<Move> moves;
    private int currentMoveIndex = 0;
    private double speed = 1.0;  // 1x normal speed
    
    void play() { /* auto-advance with timer */ }
    void pause() { /* stop timer */ }
    void stepForward() { currentMoveIndex++; applyMove(); }
    void stepBack() { currentMoveIndex--; revertMove(); }
    void setSpeed(double multiplier) { speed = multiplier; }
}
```

---

## Technical Requirements

### Architecture: MVC Pattern (Mandatory)
```
project/
├── model/              # Separate model package (required)
│   ├── Board.java/py
│   ├── Piece.java/py
│   ├── Player.java/py
│   ├── GameState.java/py
│   └── MoveHistory.java/py
├── view/
│   ├── GameView.java/py
│   ├── BoardRenderer.java/py
│   └── UIComponents.java/py
├── controller/
│   ├── GameController.java/py
│   └── MoveValidator.java/py
└── Main.java/py
```

### Model Package Requirements
**Must contain (minimum)**:
- `Board`: 7×9 grid, square types (normal/trap/den/water)
- `Piece`: Type, rank, position, owner
- `GameState`: Current board, turn, move history, game status
- `MoveValidator`: Rule validation logic
- `MoveHistory`: Stack for undo/redo, list for replay

### Technology Stack
- **Language**: Java or Python (standard library ONLY)
- **Libraries Allowed**:
  - **Java**: `java.util.*`, `java.io.*`, `javax.swing.*` (GUI), `java.awt.*`
  - **Python**: `tkinter` (GUI), `json` (save/load), built-in standard library
- **Prohibited**: No external frameworks, no third-party libraries, no Maven/Pip dependencies

### Data Persistence
- **Format**: Plain text (JSON/CSV) or serialized objects
- **Save Structure**:
```json
{
  "board": [[...]], 
  "currentPlayer": "RED",
  "moveHistory": [...],
  "timestamp": "2025-11-19T10:30:00"
}
```

### Undo/Redo Implementation
- **Data Structure**: Stack-based or List-based history
- **Storage**: Store complete GameState or incremental moves
- **Limit**: Minimum 10 undo levels

### Replay Implementation
- Store move sequence: `[{piece, from, to, captured}, ...]`
- Playback engine: Reconstruct board state for each move
- UI controls: Play/Pause/StepForward/StepBack/Speed

---

## Implementation Strategy (最简洁高分方案)

### Phase 1: Core Model (Week 1)
1. **Board & Piece classes**: Data structures only
2. **Move validation**: Implement all rules (hierarchy, traps, river, den)
3. **GameState**: Turn management, win condition checking

### Phase 2: Basic Gameplay (Week 1-2)
1. **Console version first**: Text-based I/O for rapid testing
2. **Move execution**: Apply moves, update board
3. **Game loop**: Player turns, input validation

### Phase 3: Save/Load/Undo (Week 2)
1. **Serialization**: JSON for game state
2. **Undo stack**: Store last 10 states
3. **File I/O**: Save/Load handlers

### Phase 4: GUI (Week 3)
1. **Board rendering**: Grid layout, piece images/text
2. **Click handlers**: Select piece → Show legal moves → Execute move
3. **Menus**: New/Save/Load/Undo/Redo buttons

### Phase 5: Replay & Polish (Week 3-4)
1. **Replay engine**: Step through move history
2. **UI controls**: Timeline, speed slider
3. **Testing & bug fixes**

### Code Quality Guidelines
- **Separation of Concerns**: Model has ZERO UI dependencies
- **Single Responsibility**: Each class has one clear purpose
- **DRY**: Reuse move validation logic
- **Comments**: Only for complex algorithms (trap logic, river jump validation)

### Testing Priorities
1. Move validation (all special cases)
2. Win condition detection
3. Save/Load integrity
4. Undo/Redo correctness
5. Replay accuracy

---

## Scoring Optimization

### Must-Have (80% score)
- ✅ Full game rules implementation
- ✅ MVC architecture with separate model package
- ✅ Save/Load functionality
- ✅ Undo (at least 1 level)
- ✅ Basic GUI

### High-Value Features (90-100% score)
- ✅ **Undo/Redo with 10+ levels**
- ✅ **Full replay system with controls**
- ✅ **Move history display**
- ✅ Robust error handling
- ✅ Clean code structure
- ✅ Edge case handling (stalemate, repetition)

### Bonus Points
- Highlight legal moves on selection
- Move notation display (algebraic notation)
- Replay speed control
- Professional UI layout

---

## Development Checklist

### Model Layer
- [ ] Board class with 7×9 grid
- [ ] Piece class with rank/type/position
- [ ] Square types (normal/trap/den/water)
- [ ] Move validation for each piece type
- [ ] Capture logic with special rules
- [ ] Trap/Den/River logic
- [ ] Win/Draw detection
- [ ] GameState serialization

### View Layer
- [ ] Board rendering
- [ ] Piece display (text or images)
- [ ] Legal move highlighting
- [ ] Status display (turn, captured pieces)
- [ ] Button/menu UI

### Controller Layer
- [ ] User input handling
- [ ] Move execution coordination
- [ ] File operations (save/load)
- [ ] Undo/Redo management
- [ ] Replay control

### Integration
- [ ] Game loop
- [ ] Event handling
- [ ] State synchronization
- [ ] Error messages

---

## File Structure Example (Java)
```java
// model/Piece.java
public class Piece {
    enum Type { RAT, CAT, DOG, WOLF, LEOPARD, TIGER, LION, ELEPHANT }
    enum Owner { RED, BLUE }
    private Type type;
    private Owner owner;
    private int row, col;
    public int getRank() { return type.ordinal() + 1; }
    // ...
}

// model/Board.java
public class Board {
    enum SquareType { NORMAL, TRAP, DEN, WATER }
    private Piece[][] grid = new Piece[9][7];
    private SquareType[][] squareTypes = new SquareType[9][7];
    public boolean isValidMove(Piece piece, int toRow, int toCol) { /*...*/ }
    // ...
}
```

---

## Estimated Timeline
- **Week 1**: Model + Console prototype
- **Week 2**: Save/Load + Undo + Basic GUI
- **Week 3**: Replay + Full GUI + Testing
- **Week 4**: Polish + Documentation

**Total**: 3-4 weeks for maximum score implementation

---

## Success Criteria
1. ✅ All game rules correctly implemented
2. ✅ MVC pattern strictly followed
3. ✅ Model package separate and UI-independent
4. ✅ Only standard library used
5. ✅ Save/Load works across sessions
6. ✅ Undo/Redo functional (10 levels)
7. ✅ Replay system with controls
8. ✅ Clean, readable code
9. ✅ No crashes, robust error handling
10. ✅ Professional user experience

---

**Document Version**: 1.0  
**Created**: 2025-11-19  
**Target Score**: 90-100/100
