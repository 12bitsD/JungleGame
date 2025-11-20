"""
Unit tests for the Piece class hierarchy.
Exercises functionality: Factory creation, properties, and polymorphic behaviors.
"""

import unittest
from model.piece import Piece, PieceType, Player, Rat, Tiger, Lion

class TestPiece(unittest.TestCase):
    
    def test_piece_creation_factory(self):
        """
        Functionality: Verify Piece.create factory method.
        Expected Result: Correct subclass instance is returned with proper attributes.
        """
        # Test Rat creation
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        self.assertIsInstance(rat, Rat)
        self.assertEqual(rat.piece_type, PieceType.RAT)
        self.assertEqual(rat.owner, Player.RED)
        self.assertEqual(rat.rank, 1)
        
        # Test Lion creation
        lion = Piece.create(PieceType.LION, Player.BLUE, 8, 6)
        self.assertIsInstance(lion, Lion)
        self.assertEqual(lion.piece_type, PieceType.LION)
        self.assertEqual(lion.owner, Player.BLUE)
        self.assertEqual(lion.rank, 7)

    def test_piece_properties(self):
        """
        Functionality: Verify piece intrinsic properties (rank, name).
        Expected Result: Rank matches PieceType value, name is capitalized.
        """
        tiger = Piece.create(PieceType.TIGER, Player.RED, 0, 0)
        self.assertEqual(tiger.rank, 6)
        self.assertEqual(tiger.get_name(), "Tiger")
        
        elephant = Piece.create(PieceType.ELEPHANT, Player.RED, 0, 0)
        self.assertEqual(elephant.rank, 8)

    def test_polymorphism_swimming(self):
        """
        Functionality: Verify can_swim() polymorphism.
        Expected Result: Only Rat returns True, others False.
        """
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        dog = Piece.create(PieceType.DOG, Player.RED, 0, 0)
        
        self.assertTrue(rat.can_swim(), "Rat should be able to swim")
        self.assertFalse(dog.can_swim(), "Dog should not be able to swim")

    def test_polymorphism_jumping(self):
        """
        Functionality: Verify can_jump() polymorphism.
        Expected Result: Tiger and Lion return True, others False.
        """
        tiger = Piece.create(PieceType.TIGER, Player.RED, 0, 0)
        lion = Piece.create(PieceType.LION, Player.RED, 0, 0)
        wolf = Piece.create(PieceType.WOLF, Player.RED, 0, 0)
        
        self.assertTrue(tiger.can_jump(), "Tiger should be able to jump")
        self.assertTrue(lion.can_jump(), "Lion should be able to jump")
        self.assertFalse(wolf.can_jump(), "Wolf should not be able to jump")

    def test_serialization(self):
        """
        Functionality: Verify to_dict and from_dict.
        Expected Result: Recreated piece matches original.
        """
        original = Piece.create(PieceType.CAT, Player.BLUE, 5, 5)
        data = original.to_dict()
        
        recreated = Piece.from_dict(data)
        
        self.assertEqual(recreated.piece_type, original.piece_type)
        self.assertEqual(recreated.owner, original.owner)
        self.assertEqual(recreated.row, original.row)
        self.assertEqual(recreated.col, original.col)

    def test_invalid_creation(self):
        """
        Functionality: Verify creation fails with invalid type.
        """
        with self.assertRaises(ValueError):
            Piece.create("INVALID_TYPE", Player.RED, 0, 0)

if __name__ == '__main__':
    unittest.main()
