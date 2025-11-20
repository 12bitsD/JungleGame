"""
Unit tests for the Board class.
Exercises functionality: Grid management, terrain initialization, and piece placement.
"""

import unittest
from model.board import Board, SquareType
from model.piece import PieceType, Player

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = Board()

    def test_initial_terrain_setup(self):
        """
        Functionality: Verify board terrain initialization (Dens, Traps, Rivers).
        Expected Result: Special squares match the specification.
        """
        # Check Dens
        self.assertTrue(self.board.is_den(0, 3, Player.RED), "Red Den should be at (0, 3)")
        self.assertTrue(self.board.is_den(8, 3, Player.BLUE), "Blue Den should be at (8, 3)")
        
        # Check Traps (Red side)
        self.assertTrue(self.board.is_trap(0, 2, Player.BLUE), "Trap at (0,2) should be opponent trap for Blue")
        self.assertTrue(self.board.is_trap(1, 3, Player.BLUE), "Trap at (1,3) should be opponent trap for Blue")
        
        # Check Water (River)
        self.assertTrue(self.board.is_water(3, 1), "(3,1) should be water")
        self.assertTrue(self.board.is_water(5, 5), "(5,5) should be water")
        self.assertFalse(self.board.is_water(3, 3), "(3,3) is the land bridge between rivers")

    def test_initial_piece_setup(self):
        """
        Functionality: Verify setup_initial_position().
        Expected Result: Pieces are placed at correct starting coordinates.
        """
        self.board.setup_initial_position()
        
        # Check Red Lion at A3 (2, 0)
        lion = self.board.get_piece(2, 0)
        self.assertIsNotNone(lion)
        self.assertEqual(lion.piece_type, PieceType.LION)
        self.assertEqual(lion.owner, Player.RED)
        
        # Check Blue Tiger at A7 (6, 0)
        tiger = self.board.get_piece(6, 0)
        self.assertIsNotNone(tiger)
        self.assertEqual(tiger.piece_type, PieceType.TIGER)
        self.assertEqual(tiger.owner, Player.BLUE)

    def test_move_piece_mechanic(self):
        """
        Functionality: Verify basic move_piece() on grid.
        Expected Result: Piece moves from origin to dest, origin becomes None.
        """
        self.board.setup_initial_position()
        
        # Move Red Lion from (2,0) to (3,0)
        piece = self.board.get_piece(2, 0)
        captured = self.board.move_piece(2, 0, 3, 0)
        
        self.assertIsNone(captured)
        self.assertIsNone(self.board.get_piece(2, 0))
        self.assertEqual(self.board.get_piece(3, 0), piece)
        self.assertEqual(piece.row, 3) # Check internal state update

    def test_out_of_bounds(self):
        """
        Functionality: Verify is_valid_position() and defensive checks.
        Expected Result: Returns False/None for coordinates outside 9x7 grid.
        """
        self.assertTrue(self.board.is_valid_position(0, 0))
        self.assertTrue(self.board.is_valid_position(8, 6))
        
        self.assertFalse(self.board.is_valid_position(-1, 0))
        self.assertFalse(self.board.is_valid_position(0, 7))
        self.assertFalse(self.board.is_valid_position(9, 0))
        
        # Test defensive getters
        self.assertIsNone(self.board.get_piece(10, 10))
        self.assertEqual(self.board.get_terrain(10, 10), SquareType.NORMAL)
        
        # Test defensive setter
        # Should not raise error, just do nothing
        self.board.set_piece(10, 10, None) 

    def test_board_copy(self):
        """
        Functionality: Verify deep copy of board.
        """
        self.board.setup_initial_position()
        original_piece = self.board.get_piece(2, 0) # Red Lion
        
        board_copy = self.board.copy()
        copied_piece = board_copy.get_piece(2, 0)
        
        self.assertIsNotNone(copied_piece)
        self.assertNotEqual(id(original_piece), id(copied_piece))
        self.assertEqual(original_piece.piece_type, copied_piece.piece_type)
        
        # Modify copy, ensure original is untouched
        board_copy.remove_piece(2, 0)
        self.assertIsNone(board_copy.get_piece(2, 0))
        self.assertIsNotNone(self.board.get_piece(2, 0))

    def test_get_all_pieces(self):
        """
        Functionality: Verify get_all_pieces filtering.
        """
        self.board.setup_initial_position()
        
        all_pieces = self.board.get_all_pieces()
        self.assertEqual(len(all_pieces), 16)
        
        red_pieces = self.board.get_all_pieces(Player.RED)
        self.assertEqual(len(red_pieces), 8)
        for p in red_pieces:
            self.assertEqual(p.owner, Player.RED)
            
        blue_pieces = self.board.get_all_pieces(Player.BLUE)
        self.assertEqual(len(blue_pieces), 8)

    def test_helpers(self):
        """
        Functionality: Verify coordinate helpers.
        """
        # Row/Number conversion
        self.assertEqual(Board.row_to_number(0), 1)
        self.assertEqual(Board.number_to_row(1), 0)
        
        # Col/Letter conversion
        self.assertEqual(Board.col_to_letter(0), 'A')
        self.assertEqual(Board.letter_to_col('A'), 0)
        self.assertEqual(Board.letter_to_col('a'), 0) # Case insensitive usually handled by caller but good to check
        
        # Notation
        self.assertEqual(self.board.position_to_notation(0, 0), "A1")
        self.assertEqual(self.board.notation_to_position("A1"), (0, 0))
        self.assertEqual(self.board.notation_to_position("G9"), (8, 6))

    def test_boolean_methods(self):
        """
        Functionality: Verify is_trap, is_den, is_water negative cases.
        """
        # is_water
        self.assertFalse(self.board.is_water(0, 0)) # Land
        self.assertFalse(self.board.is_water(-1, 0)) # OOB
        
        # is_trap
        # (0,0) is not a trap
        self.assertFalse(self.board.is_trap(0, 0, Player.RED))
        self.assertFalse(self.board.is_trap(0, 0, Player.BLUE))
        # (0,2) is a trap (Red side).
        # is_trap(..., RED) -> checks BLUE traps. (0,2) is NOT Blue trap.
        self.assertFalse(self.board.is_trap(0, 2, Player.RED))
        # is_trap(..., BLUE) -> checks RED traps. (0,2) IS Red trap.
        self.assertTrue(self.board.is_trap(0, 2, Player.BLUE))
        
        # is_den
        # (0,0) not den
        self.assertFalse(self.board.is_den(0, 0, Player.RED))
        # (0,3) is Red Den
        self.assertTrue(self.board.is_den(0, 3, Player.RED))
        self.assertFalse(self.board.is_den(0, 3, Player.BLUE))
        
        # is_opponent_den
        self.assertTrue(self.board.is_opponent_den(8, 3, Player.RED))
        self.assertFalse(self.board.is_opponent_den(0, 3, Player.RED))

if __name__ == '__main__':
    unittest.main()
