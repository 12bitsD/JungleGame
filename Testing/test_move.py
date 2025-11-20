"""
Unit tests for Move serialization.
"""

import unittest
from model.move import Move
from model.piece import Piece, PieceType, Player
from model.board import Board

class TestMove(unittest.TestCase):
    
    def test_serialization(self):
        """
        Functionality: Verify Move to_dict/from_dict.
        """
        piece = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        captured = Piece.create(PieceType.ELEPHANT, Player.BLUE, 0, 1)
        
        # Test move with capture
        move = Move(piece, 0, 0, 0, 1, captured, 1)
        data = move.to_dict()
        
        recreated = Move.from_dict(data)
        self.assertEqual(recreated.piece.piece_type, PieceType.RAT)
        self.assertEqual(recreated.from_row, 0)
        self.assertEqual(recreated.captured.piece_type, PieceType.ELEPHANT)
        
        # Test move without capture
        move_no_cap = Move(piece, 0, 0, 1, 0, None, 2)
        data_no_cap = move_no_cap.to_dict()
        
        recreated_no_cap = Move.from_dict(data_no_cap)
        self.assertIsNone(recreated_no_cap.captured)

    def test_notation(self):
        """
        Functionality: Verify Move to_notation string generation.
        """
        board = Board()
        piece = Piece.create(PieceType.TIGER, Player.RED, 0, 0)
        
        # Simple move
        move = Move(piece, 0, 0, 0, 1, None, 5)
        # 0,0 is A1. 0,1 is B1.
        expected = "5. RED Tiger A1→B1"
        self.assertEqual(move.to_notation(board), expected)
        
        # Capture move
        captured = Piece.create(PieceType.WOLF, Player.BLUE, 0, 1)
        move_cap = Move(piece, 0, 0, 0, 1, captured, 10)
        expected_cap = "10. RED Tiger A1→B1 (captured Wolf)"
        self.assertEqual(move_cap.to_notation(board), expected_cap)

if __name__ == '__main__':
    unittest.main()
