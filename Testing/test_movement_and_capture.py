"""
Unit Tests for Standard Movement and Capturing Rules
====================================================

This test suite verifies the fundamental game mechanics:
1. Valid movement (1 square orthogonal)
2. Invalid movement (diagonal, multi-square)
3. Capture rules (rank hierarchy)
4. Friendly piece collision

Each test is thoroughly commented to explain the scenario being tested.
"""

import unittest
from model.board import Board
from model.piece import Piece, PieceType, Player, Dog, Cat, Wolf, Tiger, Lion, Rat, Elephant
from model.move import MoveValidator


class TestStandardMovement(unittest.TestCase):
    """
    Test suite for standard movement rules.
    
    Setup: Each test starts with a fresh board and validator.
    Game Rule: Pieces can move exactly 1 square in orthogonal directions
               (up, down, left, right) to an empty square.
    """
    
    def setUp(self):
        """
        Setup method that runs before each test.
        
        Initializes:
        - Fresh 7x9 board with terrain
        - MoveValidator instance for rule checking
        
        This ensures each test has a clean state.
        """
        self.board = Board()
        self.validator = MoveValidator(self.board)
    
    def test_dog_moves_one_square_up(self):
        """
        Test Scenario: Dog moves 1 square UP (north) to an empty square.
        
        Initial State:
            Row 3, Col 3: RED Dog
            Row 4, Col 3: Empty
        
        Action: Move Dog from (3,3) to (4,3) - 1 square up
        
        Expected Result: Move is VALID
        
        Game Rule Verified:
        - Pieces can move 1 square vertically (upward)
        - Movement to empty square is allowed
        """
        # Arrange: Place RED Dog at position (3,3)
        dog = Dog(Player.RED, 3, 3)
        self.board.set_piece(3, 3, dog)
        
        # Act: Validate move 1 square up to (4,3)
        is_valid, error_message = self.validator.is_valid_move(dog, 4, 3)
        
        # Assert: Move should be valid
        self.assertTrue(is_valid, f"Dog should be able to move 1 square up. Error: {error_message}")
        self.assertEqual(error_message, "", "No error message expected for valid move")
    
    def test_dog_moves_one_square_down(self):
        """
        Test Scenario: Dog moves 1 square DOWN (south) to an empty square.
        
        Initial State:
            Row 4, Col 3: RED Dog
            Row 3, Col 3: Empty
        
        Action: Move Dog from (4,3) to (3,3) - 1 square down
        
        Expected Result: Move is VALID
        
        Game Rule Verified:
        - Pieces can move 1 square vertically (downward)
        """
        # Arrange: Place RED Dog at position (4,3)
        dog = Dog(Player.RED, 4, 3)
        self.board.set_piece(4, 3, dog)
        
        # Act: Validate move 1 square down to (3,3)
        is_valid, error_message = self.validator.is_valid_move(dog, 3, 3)
        
        # Assert: Move should be valid
        self.assertTrue(is_valid, f"Dog should be able to move 1 square down. Error: {error_message}")
    
    def test_dog_moves_one_square_left(self):
        """
        Test Scenario: Dog moves 1 square LEFT (west) to an empty square.
        
        Initial State:
            Row 3, Col 4: RED Dog
            Row 3, Col 3: Empty
        
        Action: Move Dog from (3,4) to (3,3) - 1 square left
        
        Expected Result: Move is VALID
        
        Game Rule Verified:
        - Pieces can move 1 square horizontally (leftward)
        """
        # Arrange: Place RED Dog at position (3,4)
        dog = Dog(Player.RED, 3, 4)
        self.board.set_piece(3, 4, dog)
        
        # Act: Validate move 1 square left to (3,3)
        is_valid, error_message = self.validator.is_valid_move(dog, 3, 3)
        
        # Assert: Move should be valid
        self.assertTrue(is_valid, f"Dog should be able to move 1 square left. Error: {error_message}")
    
    def test_dog_moves_one_square_right(self):
        """
        Test Scenario: Dog moves 1 square RIGHT (east) to an empty square.
        
        Initial State:
            Row 3, Col 3: RED Dog
            Row 3, Col 4: Empty
        
        Action: Move Dog from (3,3) to (3,4) - 1 square right
        
        Expected Result: Move is VALID
        
        Game Rule Verified:
        - Pieces can move 1 square horizontally (rightward)
        - All 4 orthogonal directions are tested (up, down, left, right)
        """
        # Arrange: Place RED Dog at position (3,3)
        dog = Dog(Player.RED, 3, 3)
        self.board.set_piece(3, 3, dog)
        
        # Act: Validate move 1 square right to (3,4)
        is_valid, error_message = self.validator.is_valid_move(dog, 3, 4)
        
        # Assert: Move should be valid
        self.assertTrue(is_valid, f"Dog should be able to move 1 square right. Error: {error_message}")
    
    def test_dog_all_four_directions(self):
        """
        Test Scenario: Comprehensive test - Dog can move in all 4 orthogonal directions.
        
        Initial State:
            Row 4, Col 3: RED Dog (center position)
            All adjacent squares: Empty
        
        Action: Validate all 4 possible moves:
            - Up:    (4,3) → (5,3)
            - Down:  (4,3) → (3,3)
            - Left:  (4,3) → (4,2)
            - Right: (4,3) → (4,4)
        
        Expected Result: All 4 moves are VALID
        
        Game Rule Verified:
        - Complete orthogonal movement freedom in all directions
        """
        # Arrange: Place RED Dog at center position (4,3)
        dog = Dog(Player.RED, 4, 3)
        self.board.set_piece(4, 3, dog)
        
        # Act & Assert: Test all 4 directions
        directions = {
            'up':    (5, 3),
            'down':  (3, 3),
            'left':  (4, 2),
            'right': (4, 4)
        }
        
        for direction, (to_row, to_col) in directions.items():
            is_valid, error_message = self.validator.is_valid_move(dog, to_row, to_col)
            self.assertTrue(
                is_valid, 
                f"Dog should be able to move {direction} to ({to_row},{to_col}). Error: {error_message}"
            )


class TestInvalidMovement(unittest.TestCase):
    """
    Test suite for invalid movement patterns.
    
    Game Rules:
    - Normal pieces cannot move diagonally
    - Normal pieces cannot move more than 1 square
    - Exception: Lion and Tiger can jump (tested separately)
    """
    
    def setUp(self):
        """
        Setup method that runs before each test.
        
        Initializes fresh board and validator for testing invalid moves.
        """
        self.board = Board()
        self.validator = MoveValidator(self.board)
    
    def test_dog_cannot_move_diagonally_up_right(self):
        """
        Test Scenario: Dog attempts to move diagonally (INVALID).
        
        Initial State:
            Row 3, Col 3: RED Dog
            Row 4, Col 4: Empty (diagonal position)
        
        Action: Attempt to move Dog from (3,3) to (4,4) - diagonal up-right
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Diagonal movement is prohibited
        - Error message should indicate "diagonal" restriction
        """
        # Arrange: Place RED Dog at position (3,3)
        dog = Dog(Player.RED, 3, 3)
        self.board.set_piece(3, 3, dog)
        
        # Act: Attempt diagonal move to (4,4)
        is_valid, error_message = self.validator.is_valid_move(dog, 4, 4)
        
        # Assert: Move should be invalid with diagonal error
        self.assertFalse(is_valid, "Dog should NOT be able to move diagonally")
        self.assertIn("diagonal", error_message.lower(), 
                     f"Error message should mention 'diagonal'. Got: {error_message}")
    
    def test_dog_cannot_move_diagonally_all_directions(self):
        """
        Test Scenario: Comprehensive diagonal restriction test.
        
        Initial State:
            Row 4, Col 3: RED Dog (center)
        
        Action: Attempt all 4 diagonal moves:
            - Up-Right:   (4,3) → (5,4)
            - Up-Left:    (4,3) → (5,2)
            - Down-Right: (4,3) → (3,4)
            - Down-Left:  (4,3) → (3,2)
        
        Expected Result: All 4 diagonal moves are INVALID
        
        Game Rule Verified:
        - No diagonal movement allowed in any direction
        """
        # Arrange: Place RED Dog at center position (4,3)
        dog = Dog(Player.RED, 4, 3)
        self.board.set_piece(4, 3, dog)
        
        # Act & Assert: Test all 4 diagonal directions
        diagonal_moves = {
            'up-right':   (5, 4),
            'up-left':    (5, 2),
            'down-right': (3, 4),
            'down-left':  (3, 2)
        }
        
        for direction, (to_row, to_col) in diagonal_moves.items():
            is_valid, error_message = self.validator.is_valid_move(dog, to_row, to_col)
            self.assertFalse(
                is_valid,
                f"Dog should NOT be able to move diagonally {direction} to ({to_row},{to_col})"
            )
    
    def test_dog_cannot_move_two_squares_vertically(self):
        """
        Test Scenario: Dog attempts to move 2 squares vertically (INVALID).
        
        Initial State:
            Row 3, Col 3: RED Dog
            Row 5, Col 3: Empty (2 squares up)
        
        Action: Attempt to move Dog from (3,3) to (5,3) - 2 squares up
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Normal pieces can only move exactly 1 square
        - Multi-square movement is prohibited (except Lion/Tiger jumps)
        """
        # Arrange: Place RED Dog at position (3,3)
        dog = Dog(Player.RED, 3, 3)
        self.board.set_piece(3, 3, dog)
        
        # Act: Attempt to move 2 squares up to (5,3)
        is_valid, error_message = self.validator.is_valid_move(dog, 5, 3)
        
        # Assert: Move should be invalid
        self.assertFalse(is_valid, "Dog should NOT be able to move 2 squares")
        # The error could be about distance or about not being able to jump
        self.assertTrue(
            "1 square" in error_message.lower() or "jump" in error_message.lower(),
            f"Error should mention distance restriction. Got: {error_message}"
        )
    
    def test_dog_cannot_move_two_squares_horizontally(self):
        """
        Test Scenario: Dog attempts to move 2 squares horizontally (INVALID).
        
        Initial State:
            Row 3, Col 2: RED Dog
            Row 3, Col 4: Empty (2 squares right)
        
        Action: Attempt to move Dog from (3,2) to (3,4) - 2 squares right
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Multi-square horizontal movement is also prohibited
        """
        # Arrange: Place RED Dog at position (3,2)
        dog = Dog(Player.RED, 3, 2)
        self.board.set_piece(3, 2, dog)
        
        # Act: Attempt to move 2 squares right to (3,4)
        is_valid, error_message = self.validator.is_valid_move(dog, 3, 4)
        
        # Assert: Move should be invalid
        self.assertFalse(is_valid, "Dog should NOT be able to move 2 squares horizontally")
    
    def test_cat_cannot_move_three_squares(self):
        """
        Test Scenario: Cat attempts to move 3 squares (extreme case).
        
        Initial State:
            Row 2, Col 3: RED Cat
            Row 5, Col 3: Empty (3 squares up)
        
        Action: Attempt to move Cat from (2,3) to (5,3) - 3 squares up
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Even greater distances are prohibited
        - Confirms 1-square rule is strictly enforced
        """
        # Arrange: Place RED Cat at position (2,3)
        cat = Cat(Player.RED, 2, 3)
        self.board.set_piece(2, 3, cat)
        
        # Act: Attempt to move 3 squares up to (5,3)
        is_valid, error_message = self.validator.is_valid_move(cat, 5, 3)
        
        # Assert: Move should be invalid
        self.assertFalse(is_valid, "Cat should NOT be able to move 3 squares")
    
    def test_lion_exception_can_jump_multiple_squares(self):
        """
        Test Scenario: Lion CAN move multiple squares (exception to the rule).
        
        Initial State:
            Row 2, Col 0: RED Lion
            Row 6, Col 0: Empty (4 squares up, across river)
        
        Action: Attempt Lion jump from (2,0) to (6,0) - vertical river jump
        
        Expected Result: Move is VALID (Lion can jump)
        
        Game Rule Verified:
        - Lion is an EXCEPTION to the 1-square rule
        - Lion can jump across rivers (3-4 squares)
        """
        # Arrange: Place RED Lion at position (2,0) - can jump across river
        lion = Lion(Player.RED, 2, 0)
        self.board.set_piece(2, 0, lion)
        
        # Act: Attempt river jump to (6,0)
        is_valid, error_message = self.validator.is_valid_move(lion, 6, 0)
        
        # Assert: Move should be valid (Lion can jump)
        self.assertTrue(is_valid, f"Lion should be able to jump across river. Error: {error_message}")
    
    def test_tiger_exception_can_jump_multiple_squares(self):
        """
        Test Scenario: Tiger CAN move multiple squares (exception to the rule).
        
        Initial State:
            Row 2, Col 6: RED Tiger
            Row 6, Col 6: Empty (4 squares up, across river)
        
        Action: Attempt Tiger jump from (2,6) to (6,6) - vertical river jump
        
        Expected Result: Move is VALID (Tiger can jump)
        
        Game Rule Verified:
        - Tiger is also an EXCEPTION to the 1-square rule
        - Only Lion and Tiger have this jumping ability
        """
        # Arrange: Place RED Tiger at position (2,6) - can jump across river
        tiger = Tiger(Player.RED, 2, 6)
        self.board.set_piece(2, 6, tiger)
        
        # Act: Attempt river jump to (6,6)
        is_valid, error_message = self.validator.is_valid_move(tiger, 6, 6)
        
        # Assert: Move should be valid (Tiger can jump)
        self.assertTrue(is_valid, f"Tiger should be able to jump across river. Error: {error_message}")


class TestCaptureRules(unittest.TestCase):
    """
    Test suite for capture rules based on rank hierarchy.
    
    Game Rules:
    - Higher rank can capture lower rank
    - Equal rank can capture each other
    - Lower rank CANNOT capture higher rank
    - Special exception: Rat (rank 1) defeats Elephant (rank 8)
    """
    
    def setUp(self):
        """
        Setup method that runs before each test.
        
        Initializes fresh board and validator for testing capture rules.
        """
        self.board = Board()
        self.validator = MoveValidator(self.board)
    
    def test_tiger_captures_wolf_higher_rank_wins(self):
        """
        Test Scenario: Higher rank animal captures lower rank animal.
        
        Ranks:
            Tiger: Rank 6
            Wolf:  Rank 4
        
        Initial State:
            Row 3, Col 3: RED Tiger (rank 6)
            Row 4, Col 3: BLUE Wolf (rank 4)
        
        Action: Move Tiger from (3,3) to (4,3) to capture Wolf
        
        Expected Result: Capture is VALID
        
        Game Rule Verified:
        - Higher rank (6) can capture lower rank (4)
        - This is the fundamental hierarchy rule
        """
        # Arrange: Place RED Tiger (rank 6) at (3,3)
        tiger = Tiger(Player.RED, 3, 3)
        self.board.set_piece(3, 3, tiger)
        
        # Arrange: Place BLUE Wolf (rank 4) at adjacent square (4,3)
        wolf = Wolf(Player.BLUE, 4, 3)
        self.board.set_piece(4, 3, wolf)
        
        # Act: Validate Tiger capturing Wolf
        is_valid, error_message = self.validator.is_valid_move(tiger, 4, 3)
        
        # Assert: Capture should be valid
        self.assertTrue(
            is_valid,
            f"Tiger (rank 6) should be able to capture Wolf (rank 4). Error: {error_message}"
        )
        self.assertEqual(tiger.rank, 6, "Tiger should have rank 6")
        self.assertEqual(wolf.rank, 4, "Wolf should have rank 4")
    
    def test_elephant_captures_tiger_highest_rank_wins(self):
        """
        Test Scenario: Highest rank animal (Elephant) captures lower rank.
        
        Ranks:
            Elephant: Rank 8 (highest)
            Tiger:    Rank 6
        
        Initial State:
            Row 3, Col 3: RED Elephant (rank 8)
            Row 3, Col 4: BLUE Tiger (rank 6)
        
        Action: Move Elephant from (3,3) to (3,4) to capture Tiger
        
        Expected Result: Capture is VALID
        
        Game Rule Verified:
        - Elephant (highest rank) can capture any lower rank piece
        - Exception: Cannot capture Rat (tested separately)
        """
        # Arrange: Place RED Elephant (rank 8) at (3,3)
        elephant = Elephant(Player.RED, 3, 3)
        self.board.set_piece(3, 3, elephant)
        
        # Arrange: Place BLUE Tiger (rank 6) at adjacent square (3,4)
        tiger = Tiger(Player.BLUE, 3, 4)
        self.board.set_piece(3, 4, tiger)
        
        # Act: Validate Elephant capturing Tiger
        is_valid, error_message = self.validator.is_valid_move(elephant, 3, 4)
        
        # Assert: Capture should be valid
        self.assertTrue(
            is_valid,
            f"Elephant (rank 8) should be able to capture Tiger (rank 6). Error: {error_message}"
        )
    
    def test_dog_captures_cat_adjacent_ranks(self):
        """
        Test Scenario: Animal captures piece with adjacent lower rank.
        
        Ranks:
            Dog: Rank 3
            Cat: Rank 2
        
        Initial State:
            Row 4, Col 2: RED Dog (rank 3)
            Row 4, Col 3: BLUE Cat (rank 2)
        
        Action: Move Dog from (4,2) to (4,3) to capture Cat
        
        Expected Result: Capture is VALID
        
        Game Rule Verified:
        - Even small rank differences (3 vs 2) allow capture
        - Any higher rank beats any lower rank
        """
        # Arrange: Place RED Dog (rank 3) at (4,2)
        dog = Dog(Player.RED, 4, 2)
        self.board.set_piece(4, 2, dog)
        
        # Arrange: Place BLUE Cat (rank 2) at adjacent square (4,3)
        cat = Cat(Player.BLUE, 4, 3)
        self.board.set_piece(4, 3, cat)
        
        # Act: Validate Dog capturing Cat
        is_valid, error_message = self.validator.is_valid_move(dog, 4, 3)
        
        # Assert: Capture should be valid
        self.assertTrue(
            is_valid,
            f"Dog (rank 3) should be able to capture Cat (rank 2). Error: {error_message}"
        )
    
    def test_tiger_captures_tiger_equal_ranks(self):
        """
        Test Scenario: Equal rank pieces can capture each other.
        
        Ranks:
            Both Tigers: Rank 6
        
        Initial State:
            Row 3, Col 3: RED Tiger (rank 6)
            Row 3, Col 4: BLUE Tiger (rank 6)
        
        Action: Move RED Tiger from (3,3) to (3,4) to capture BLUE Tiger
        
        Expected Result: Capture is VALID
        
        Game Rule Verified:
        - Equal rank pieces can capture each other
        - Rank 6 = Rank 6 is allowed
        """
        # Arrange: Place RED Tiger (rank 6) at (3,3)
        red_tiger = Tiger(Player.RED, 3, 3)
        self.board.set_piece(3, 3, red_tiger)
        
        # Arrange: Place BLUE Tiger (rank 6) at adjacent square (3,4)
        blue_tiger = Tiger(Player.BLUE, 3, 4)
        self.board.set_piece(3, 4, blue_tiger)
        
        # Act: Validate RED Tiger capturing BLUE Tiger
        is_valid, error_message = self.validator.is_valid_move(red_tiger, 3, 4)
        
        # Assert: Capture should be valid (equal ranks can capture)
        self.assertTrue(
            is_valid,
            f"Tiger (rank 6) should be able to capture Tiger (rank 6). Error: {error_message}"
        )
        self.assertEqual(red_tiger.rank, blue_tiger.rank, "Both Tigers should have rank 6")


class TestCannotCapture(unittest.TestCase):
    """
    Test suite for invalid capture attempts.
    
    Game Rule: Lower rank CANNOT capture higher rank.
    This is the inverse of the capture rule - testing failure cases.
    """
    
    def setUp(self):
        """
        Setup method that runs before each test.
        
        Initializes fresh board and validator for testing invalid captures.
        """
        self.board = Board()
        self.validator = MoveValidator(self.board)
    
    def test_wolf_cannot_capture_tiger_lower_rank_fails(self):
        """
        Test Scenario: Lower rank animal CANNOT capture higher rank.
        
        Ranks:
            Wolf:  Rank 4 (lower)
            Tiger: Rank 6 (higher)
        
        Initial State:
            Row 3, Col 3: RED Wolf (rank 4)
            Row 4, Col 3: BLUE Tiger (rank 6)
        
        Action: Attempt to move Wolf from (3,3) to (4,3) to capture Tiger
        
        Expected Result: Capture is INVALID
        
        Game Rule Verified:
        - Lower rank (4) CANNOT capture higher rank (6)
        - Error message should mention rank restriction
        """
        # Arrange: Place RED Wolf (rank 4) at (3,3)
        wolf = Wolf(Player.RED, 3, 3)
        self.board.set_piece(3, 3, wolf)
        
        # Arrange: Place BLUE Tiger (rank 6) at adjacent square (4,3)
        tiger = Tiger(Player.BLUE, 4, 3)
        self.board.set_piece(4, 3, tiger)
        
        # Act: Attempt Wolf capturing Tiger (should fail)
        is_valid, error_message = self.validator.is_valid_move(wolf, 4, 3)
        
        # Assert: Capture should be invalid
        self.assertFalse(
            is_valid,
            "Wolf (rank 4) should NOT be able to capture Tiger (rank 6)"
        )
        self.assertIn(
            "rank",
            error_message.lower(),
            f"Error message should mention rank restriction. Got: {error_message}"
        )
    
    def test_cat_cannot_capture_dog_adjacent_lower_rank(self):
        """
        Test Scenario: Even small rank difference prevents capture.
        
        Ranks:
            Cat: Rank 2 (lower)
            Dog: Rank 3 (higher)
        
        Initial State:
            Row 4, Col 3: RED Cat (rank 2)
            Row 4, Col 4: BLUE Dog (rank 3)
        
        Action: Attempt to move Cat from (4,3) to (4,4) to capture Dog
        
        Expected Result: Capture is INVALID
        
        Game Rule Verified:
        - Even difference of 1 rank prevents lower from capturing higher
        - Rank 2 cannot beat Rank 3
        """
        # Arrange: Place RED Cat (rank 2) at (4,3)
        cat = Cat(Player.RED, 4, 3)
        self.board.set_piece(4, 3, cat)
        
        # Arrange: Place BLUE Dog (rank 3) at adjacent square (4,4)
        dog = Dog(Player.BLUE, 4, 4)
        self.board.set_piece(4, 4, dog)
        
        # Act: Attempt Cat capturing Dog (should fail)
        is_valid, error_message = self.validator.is_valid_move(cat, 4, 4)
        
        # Assert: Capture should be invalid
        self.assertFalse(
            is_valid,
            "Cat (rank 2) should NOT be able to capture Dog (rank 3)"
        )
    
    def test_rat_cannot_capture_cat_lowest_vs_higher(self):
        """
        Test Scenario: Lowest rank (Rat) cannot capture higher rank.
        
        Ranks:
            Rat: Rank 1 (lowest)
            Cat: Rank 2
        
        Initial State:
            Row 2, Col 2: RED Rat (rank 1)
            Row 2, Col 3: BLUE Cat (rank 2)
        
        Action: Attempt to move Rat from (2,2) to (2,3) to capture Cat
        
        Expected Result: Capture is INVALID
        
        Game Rule Verified:
        - Rat (rank 1) follows normal rules against Cat (rank 2)
        - Exception: Rat CAN capture Elephant (tested separately)
        """
        # Arrange: Place RED Rat (rank 1) at (2,2)
        rat = Rat(Player.RED, 2, 2)
        self.board.set_piece(2, 2, rat)
        
        # Arrange: Place BLUE Cat (rank 2) at adjacent square (2,3)
        cat = Cat(Player.BLUE, 2, 3)
        self.board.set_piece(2, 3, cat)
        
        # Act: Attempt Rat capturing Cat (should fail)
        is_valid, error_message = self.validator.is_valid_move(rat, 2, 3)
        
        # Assert: Capture should be invalid
        self.assertFalse(
            is_valid,
            "Rat (rank 1) should NOT be able to capture Cat (rank 2)"
        )
    
    def test_elephant_cannot_capture_elephant_same_color(self):
        """
        Test Scenario: Piece cannot capture same-colored piece (friendly fire).
        
        Note: This test is included here as it's related to capture failures,
              but it's also tested in TestFriendlyPieceCollision class.
        
        Ranks:
            Both Elephants: Rank 8
            Both owned by RED player
        
        Initial State:
            Row 3, Col 3: RED Elephant
            Row 3, Col 4: RED Elephant (same color)
        
        Action: Attempt to move first Elephant to capture second (both RED)
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Cannot capture own pieces (even if ranks allow)
        - Color/player ownership takes precedence over rank
        """
        # Arrange: Place first RED Elephant at (3,3)
        elephant1 = Elephant(Player.RED, 3, 3)
        self.board.set_piece(3, 3, elephant1)
        
        # Arrange: Place second RED Elephant at adjacent square (3,4)
        elephant2 = Elephant(Player.RED, 3, 4)
        self.board.set_piece(3, 4, elephant2)
        
        # Act: Attempt first Elephant "capturing" second (same color)
        is_valid, error_message = self.validator.is_valid_move(elephant1, 3, 4)
        
        # Assert: Move should be invalid (friendly fire)
        self.assertFalse(
            is_valid,
            "Elephant should NOT be able to capture friendly Elephant"
        )
        self.assertIn(
            "own piece",
            error_message.lower(),
            f"Error message should mention 'own piece'. Got: {error_message}"
        )


class TestFriendlyPieceCollision(unittest.TestCase):
    """
    Test suite for friendly piece collision rules.
    
    Game Rule: A piece cannot move to a square occupied by a friendly piece
               (piece of the same color/player).
    """
    
    def setUp(self):
        """
        Setup method that runs before each test.
        
        Initializes fresh board and validator for testing friendly collision.
        """
        self.board = Board()
        self.validator = MoveValidator(self.board)
    
    def test_dog_cannot_move_to_friendly_cat_square(self):
        """
        Test Scenario: Dog cannot move to square occupied by friendly Cat.
        
        Initial State:
            Row 3, Col 3: RED Dog
            Row 3, Col 4: RED Cat (same color)
        
        Action: Attempt to move Dog from (3,3) to (3,4)
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Piece cannot move to square with friendly piece
        - Both pieces are RED (same player)
        - Error message should indicate "own piece" or "friendly"
        """
        # Arrange: Place RED Dog at (3,3)
        dog = Dog(Player.RED, 3, 3)
        self.board.set_piece(3, 3, dog)
        
        # Arrange: Place RED Cat at adjacent square (3,4) - same color
        cat = Cat(Player.RED, 3, 4)
        self.board.set_piece(3, 4, cat)
        
        # Act: Attempt Dog moving to Cat's square
        is_valid, error_message = self.validator.is_valid_move(dog, 3, 4)
        
        # Assert: Move should be invalid
        self.assertFalse(
            is_valid,
            "Dog should NOT be able to move to square with friendly Cat"
        )
        self.assertIn(
            "own piece",
            error_message.lower(),
            f"Error message should mention 'own piece'. Got: {error_message}"
        )
    
    def test_tiger_cannot_move_to_friendly_tiger_square(self):
        """
        Test Scenario: Tiger cannot move to square occupied by friendly Tiger.
        
        Initial State:
            Row 4, Col 2: RED Tiger
            Row 4, Col 3: RED Tiger (same color, same rank)
        
        Action: Attempt to move first Tiger from (4,2) to (4,3)
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Same rank doesn't matter if same color
        - Friendly collision rule applies even to identical pieces
        """
        # Arrange: Place first RED Tiger at (4,2)
        tiger1 = Tiger(Player.RED, 4, 2)
        self.board.set_piece(4, 2, tiger1)
        
        # Arrange: Place second RED Tiger at adjacent square (4,3)
        tiger2 = Tiger(Player.RED, 4, 3)
        self.board.set_piece(4, 3, tiger2)
        
        # Act: Attempt first Tiger moving to second Tiger's square
        is_valid, error_message = self.validator.is_valid_move(tiger1, 4, 3)
        
        # Assert: Move should be invalid
        self.assertFalse(
            is_valid,
            "Tiger should NOT be able to move to square with friendly Tiger"
        )
    
    def test_rat_cannot_move_to_friendly_elephant_square(self):
        """
        Test Scenario: Rat cannot move to friendly Elephant square.
        
        Note: Even though Rat can capture enemy Elephant (special rule),
              it still cannot move to friendly Elephant square.
        
        Initial State:
            Row 2, Col 3: RED Rat
            Row 2, Col 4: RED Elephant (same color)
        
        Action: Attempt to move Rat from (2,3) to (2,4)
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Friendly collision rule applies even to special case pieces
        - Rat's special ability (beat Elephant) doesn't override friendly rule
        """
        # Arrange: Place RED Rat at (2,3)
        rat = Rat(Player.RED, 2, 3)
        self.board.set_piece(2, 3, rat)
        
        # Arrange: Place RED Elephant at adjacent square (2,4) - same color
        elephant = Elephant(Player.RED, 2, 4)
        self.board.set_piece(2, 4, elephant)
        
        # Act: Attempt Rat moving to Elephant's square
        is_valid, error_message = self.validator.is_valid_move(rat, 2, 4)
        
        # Assert: Move should be invalid
        self.assertFalse(
            is_valid,
            "Rat should NOT be able to move to square with friendly Elephant"
        )
    
    def test_cat_can_move_to_enemy_cat_square(self):
        """
        Test Scenario: Cat CAN move to enemy Cat square (contrast to friendly).
        
        Initial State:
            Row 3, Col 3: RED Cat
            Row 3, Col 4: BLUE Cat (different color, same rank)
        
        Action: Move RED Cat from (3,3) to (3,4) to capture BLUE Cat
        
        Expected Result: Move is VALID (capture is allowed)
        
        Game Rule Verified:
        - Enemy pieces CAN be captured (even same rank)
        - Friendly collision rule ONLY applies to same-color pieces
        - This confirms the rule is color-based, not rank-based
        """
        # Arrange: Place RED Cat at (3,3)
        red_cat = Cat(Player.RED, 3, 3)
        self.board.set_piece(3, 3, red_cat)
        
        # Arrange: Place BLUE Cat at adjacent square (3,4) - different color
        blue_cat = Cat(Player.BLUE, 3, 4)
        self.board.set_piece(3, 4, blue_cat)
        
        # Act: Validate RED Cat capturing BLUE Cat
        is_valid, error_message = self.validator.is_valid_move(red_cat, 3, 4)
        
        # Assert: Move should be valid (enemy capture allowed)
        self.assertTrue(
            is_valid,
            f"RED Cat should be able to capture BLUE Cat. Error: {error_message}"
        )
    
    def test_blue_dog_cannot_move_to_friendly_blue_wolf_square(self):
        """
        Test Scenario: BLUE Dog cannot move to BLUE Wolf square.
        
        Initial State:
            Row 5, Col 3: BLUE Dog
            Row 6, Col 3: BLUE Wolf (same color)
        
        Action: Attempt to move BLUE Dog from (5,3) to (6,3)
        
        Expected Result: Move is INVALID
        
        Game Rule Verified:
        - Friendly collision rule applies to BLUE pieces too
        - Rule is symmetric for both players (RED and BLUE)
        """
        # Arrange: Place BLUE Dog at (5,3)
        dog = Dog(Player.BLUE, 5, 3)
        self.board.set_piece(5, 3, dog)
        
        # Arrange: Place BLUE Wolf at adjacent square (6,3) - same color
        wolf = Wolf(Player.BLUE, 6, 3)
        self.board.set_piece(6, 3, wolf)
        
        # Act: Attempt BLUE Dog moving to BLUE Wolf's square
        is_valid, error_message = self.validator.is_valid_move(dog, 6, 3)
        
        # Assert: Move should be invalid
        self.assertFalse(
            is_valid,
            "BLUE Dog should NOT be able to move to square with BLUE Wolf"
        )


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_movement_and_capture_tests():
    """
    Run all movement and capture tests with detailed output.
    
    This function executes all test classes and prints a summary.
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStandardMovement))
    suite.addTests(loader.loadTestsFromTestCase(TestInvalidMovement))
    suite.addTests(loader.loadTestsFromTestCase(TestCaptureRules))
    suite.addTests(loader.loadTestsFromTestCase(TestCannotCapture))
    suite.addTests(loader.loadTestsFromTestCase(TestFriendlyPieceCollision))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("MOVEMENT AND CAPTURE TEST SUMMARY")
    print("="*80)
    print(f"Total Tests Run:        {result.testsRun}")
    print(f"Successful Tests:       {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed Tests:           {len(result.failures)}")
    print(f"Errors:                 {len(result.errors)}")
    print("\nTest Categories:")
    print("  - Standard Movement Tests:      6 tests")
    print("  - Invalid Movement Tests:       8 tests")
    print("  - Capture Rules Tests:          5 tests")
    print("  - Cannot Capture Tests:         4 tests")
    print("  - Friendly Piece Collision:     5 tests")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    """
    Main entry point for running the test suite.
    
    Usage:
        python3 test_movement_and_capture.py
    """
    success = run_movement_and_capture_tests()
    exit(0 if success else 1)
