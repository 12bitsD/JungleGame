"""
Unit tests for MoveValidator class.
Exercises functionality: Complex game rules validation (Movement, Capture, Jumps, Terrain).
"""

import unittest
from model.board import Board
from model.piece import Piece, PieceType, Player
from model.move import MoveValidator

class TestMoveValidator(unittest.TestCase):
    
    def setUp(self):
        self.board = Board()
        self.validator = MoveValidator(self.board)

    def test_basic_movement(self):
        """
        Functionality: Verify standard 1-step orthogonal movement.
        Expected Result: Valid for adjacent squares, Invalid for diagonal/far.
        """
        dog = Piece.create(PieceType.DOG, Player.RED, 2, 2)
        self.board.set_piece(2, 2, dog)
        
        # Valid move (Up)
        valid, _ = self.validator.is_valid_move(dog, 3, 2)
        self.assertTrue(valid)
        
        # Invalid move (Diagonal)
        valid, _ = self.validator.is_valid_move(dog, 3, 3)
        self.assertFalse(valid)
        
        # Invalid move (2 steps)
        valid, _ = self.validator.is_valid_move(dog, 4, 2)
        self.assertFalse(valid)

    def test_rat_swimming(self):
        """
        Functionality: Verify Rat entering water.
        Expected Result: Valid for Rat, Invalid for others.
        """
        rat = Piece.create(PieceType.RAT, Player.RED, 3, 0) # Adjacent to water (3,1) is water
        self.board.set_piece(3, 0, rat)
        
        # Rat enters water
        valid, _ = self.validator.is_valid_move(rat, 3, 1)
        self.assertTrue(valid, "Rat should be able to enter water")
        
        # Dog tries to enter water
        dog = Piece.create(PieceType.DOG, Player.RED, 3, 0)
        self.board.set_piece(3, 0, dog) # Replace rat
        valid, msg = self.validator.is_valid_move(dog, 3, 1)
        self.assertFalse(valid, "Dog should not enter water")
        self.assertIn("Cannot enter water", msg)

    def test_lion_jump_over_river(self):
        """
        Functionality: Verify Lion/Tiger jumping over river.
        Expected Result: Valid horizontal/vertical jump over water.
        """
        lion = Piece.create(PieceType.LION, Player.RED, 3, 2) # Land between rivers
        self.board.set_piece(3, 2, lion)
        
        # Valid jump left to (3, -1)? No, river is col 0,1. Land is 2.
        # Let's setup at (2, 0) -> jump vertical to (6, 0)
        
        lion.row, lion.col = 2, 0
        self.board.set_piece(2, 0, lion)
        
        # Valid vertical jump (2,0) -> (6,0) crossing 3,4,5
        valid, _ = self.validator.is_valid_move(lion, 6, 0)
        self.assertTrue(valid, "Lion should jump vertically over river")
        
        # Blocked jump (Rat in river)
        rat = Piece.create(PieceType.RAT, Player.BLUE, 4, 0)
        self.board.set_piece(4, 0, rat)
        valid, msg = self.validator.is_valid_move(lion, 6, 0)
        self.assertFalse(valid, "Jump blocked by Rat")
        self.assertIn("blocked", msg)
        
        # Invalid Jump (Too short/long/not river)
        self.board.remove_piece(4, 0) # Clear rat
        
        # Try jumping to (5,0) - inside river (Wait, Lion can't enter river)
        # Try jumping to (7,0) - distance 5. Valid river width is 3 (rows 3,4,5).
        # Jump from 2 to 7 = dist 5. 
        # Logic: _get_jump_path_squares checks len == 3.
        # If we jump to 7, squares will be 3,4,5,6. Len 4.
        valid, msg = self.validator.is_valid_move(lion, 7, 0)
        self.assertFalse(valid, "Jump too long")
        self.assertIn("not a valid river crossing", msg)

    def test_capture_hierarchy(self):
        """
        Functionality: Verify rank-based capture.
        Expected Result: Higher rank captures lower, Exception for Rat vs Elephant.
        """
        tiger = Piece.create(PieceType.TIGER, Player.RED, 0, 0)
        wolf = Piece.create(PieceType.WOLF, Player.BLUE, 0, 1)
        self.board.set_piece(0, 0, tiger)
        self.board.set_piece(0, 1, wolf)
        
        # Tiger (6) captures Wolf (4)
        valid, _ = self.validator.is_valid_move(tiger, 0, 1)
        self.assertTrue(valid)
        
        # Wolf cannot capture Tiger
        self.board.move_piece(0, 0, 1, 0) # Move tiger away
        self.board.set_piece(0, 0, wolf)
        self.board.set_piece(0, 1, tiger)
        wolf.row, wolf.col = 0, 0
        valid, msg = self.validator.is_valid_move(wolf, 0, 1)
        self.assertFalse(valid)
        self.assertIn("rank", msg)

    def test_rat_elephant_paradox(self):
        """
        Functionality: Verify Rat > Elephant and Elephant !> Rat rule.
        Expected Result: Rat captures Elephant, Elephant cannot capture Rat.
        """
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        elephant = Piece.create(PieceType.ELEPHANT, Player.BLUE, 0, 1)
        self.board.set_piece(0, 0, rat)
        self.board.set_piece(0, 1, elephant)
        
        # Rat captures Elephant
        valid, _ = self.validator.is_valid_move(rat, 0, 1)
        self.assertTrue(valid, "Rat should capture Elephant")
        
        # Elephant captures Rat?
        self.board.set_piece(0, 0, elephant)
        self.board.set_piece(0, 1, rat)
        elephant.row, elephant.col = 0, 0
        valid, msg = self.validator.is_valid_move(elephant, 0, 1)
        self.assertFalse(valid, "Elephant cannot capture Rat")

    def test_trap_effectiveness(self):
        """
        Functionality: Verify Traps reduce rank to 0.
        Expected Result: Any piece can capture a stronger piece in a trap.
        """
        # Blue Trap at (0,2) relative to Red? No, Red traps are at row 0/1.
        # Red Traps: (0,2), (0,4), (1,3).
        # Place Blue Elephant in Red Trap (0,2)
        elephant = Piece.create(PieceType.ELEPHANT, Player.BLUE, 0, 2)
        self.board.set_piece(0, 2, elephant)
        
        # Red Rat at (0,1)
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 1)
        self.board.set_piece(0, 1, rat)
        
        # Rat captures Elephant (valid anyway due to special rule, let's test Wolf vs Tiger)
        
        # Blue Tiger in Red Trap (0,2)
        tiger = Piece.create(PieceType.TIGER, Player.BLUE, 0, 2)
        self.board.set_piece(0, 2, tiger)
        
        # Red Wolf (Rank 4) attacks Tiger (Rank 6) in Trap
        wolf = Piece.create(PieceType.WOLF, Player.RED, 0, 1)
        self.board.set_piece(0, 1, wolf)
        
        valid, _ = self.validator.is_valid_move(wolf, 0, 2)
        self.assertTrue(valid, "Wolf should capture trapped Tiger")

    def test_den_protection(self):
        """
        Functionality: Verify Den rules.
        Expected Result: Cannot enter own den.
        """
        # Red Den at (0,3)
        lion = Piece.create(PieceType.LION, Player.RED, 0, 2)
        self.board.set_piece(0, 2, lion)
        
        valid, msg = self.validator.is_valid_move(lion, 0, 3)
        self.assertFalse(valid)
        self.assertIn("own den", msg)

    def test_friendly_fire(self):
        """
        Functionality: Verify cannot capture own pieces.
        """
        lion = Piece.create(PieceType.LION, Player.RED, 0, 0)
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 1)
        self.board.set_piece(0, 0, lion)
        self.board.set_piece(0, 1, rat)
        
        valid, msg = self.validator.is_valid_move(lion, 0, 1)
        self.assertFalse(valid)
        self.assertIn("own piece", msg)

    def test_invalid_jumps(self):
        """
        Functionality: Verify invalid jump scenarios.
        """
        tiger = Piece.create(PieceType.TIGER, Player.RED, 2, 2) # Not near river
        self.board.set_piece(2, 2, tiger)
        
        # Jump diagonally? (2,2) -> (4,4)
        valid, msg = self.validator.is_valid_move(tiger, 4, 4)
        self.assertFalse(valid)
        # Should be caught by orthogonal check first actually
        
        # Setup tiger at (2,0) (Left bank)
        tiger.row, tiger.col = 2, 0
        self.board.set_piece(2, 0, tiger)
        
        # Try to jump NOT across river but just 2 squares on land?
        # (2,0) -> (2,2) is valid jump.
        # (2,0) -> (4,0) is on land? No col 0 is river path.
        
        # Try jumping from (0,0) to (0,2) - Land jump
        self.board.set_piece(0, 0, tiger)
        valid, msg = self.validator.is_valid_move(tiger, 0, 2)
        self.assertFalse(valid) # "Jump path is not a valid river crossing"
        
        # Try jumping non-jumping piece
        dog = Piece.create(PieceType.DOG, Player.RED, 2, 0)
        self.board.set_piece(2, 0, dog)
        valid, msg = self.validator.is_valid_move(dog, 2, 2) # Attempt jump over river (2,1 is water)
        self.assertFalse(valid)
        self.assertIn("Only Lion and Tiger can jump", msg)

    def test_get_legal_moves(self):
        """
        Functionality: Verify get_legal_moves returns correct list.
        """
        # Place Tiger at (2,0) - Can move up/down/right(into water-no)/left(off), Jump right(to 2,3?)
        # River is cols 0,1 at rows 3-5.
        # (2,0) is land. (3,0) is water.
        
        # Setup: Red Tiger at (2,0)
        tiger = Piece.create(PieceType.TIGER, Player.RED, 2, 0)
        self.board.set_piece(2, 0, tiger)
        
        # Legal moves:
        # 1. (1,0) - Land
        # 2. (2,1) - Land
        # 3. (3,0) - Water? Tiger cannot swim.
        # 4. Jump? (2,0) is adjacent to river col? No.
        # River is at rows 3,4,5 for cols 0,1.
        # (2,0) is adjacent to (3,0) which is water.
        # Vertical jump from 2 to 6?
        # Col 0 has water at 3,4,5. So yes, vertical jump (2,0)->(6,0) is possible.
        
        moves = self.validator.get_legal_moves(tiger)
        self.assertIn((6, 0), moves) # Jump
        self.assertIn((1, 0), moves) # Normal
        self.assertIn((2, 1), moves) # Normal
        self.assertNotIn((3, 0), moves) # Water

    def test_get_legal_moves_no_jumps(self):
        """
        Functionality: Verify get_legal_moves for Tiger far from river.
        """
        tiger = Piece.create(PieceType.TIGER, Player.RED, 0, 0)
        self.board.set_piece(0, 0, tiger)
        
        # At (0,0), can move to (0,1) and (1,0). No jumps possible.
        moves = self.validator.get_legal_moves(tiger)
        self.assertEqual(len(moves), 2)
        self.assertIn((0, 1), moves)
        self.assertIn((1, 0), moves)
        
        # Test surrounded by own pieces (no moves)
        # Surround (0,0) with Red pieces at (0,1) and (1,0)
        p1 = Piece.create(PieceType.RAT, Player.RED, 0, 1)
        p2 = Piece.create(PieceType.RAT, Player.RED, 1, 0)
        self.board.set_piece(0, 1, p1)
        self.board.set_piece(1, 0, p2)
        
        moves = self.validator.get_legal_moves(tiger)
        self.assertEqual(len(moves), 0)

if __name__ == '__main__':
    unittest.main()
