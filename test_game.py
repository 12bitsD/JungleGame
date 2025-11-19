"""
Simple test script to verify game functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import GameState, Board, MoveValidator, Player, PieceType


def test_board_setup():
    """Test initial board setup."""
    print("Testing board setup...")
    board = Board()
    board.setup_initial_position()
    
    # Check RED pieces
    assert board.get_piece(2, 0).piece_type == PieceType.LION
    assert board.get_piece(2, 4).piece_type == PieceType.RAT
    assert board.get_piece(1, 3).piece_type == PieceType.ELEPHANT
    
    # Check BLUE pieces
    assert board.get_piece(6, 6).piece_type == PieceType.LION
    assert board.get_piece(6, 2).piece_type == PieceType.RAT
    
    print("✓ Board setup correct!")


def test_basic_move():
    """Test basic piece movement."""
    print("\nTesting basic move...")
    game = GameState()
    game.start_new_game()
    
    # Move RED rat from E3 to E4
    success, msg = game.make_move(2, 4, 3, 4)
    assert success, f"Move failed: {msg}"
    
    # Check piece moved
    assert game.board.get_piece(3, 4).piece_type == PieceType.RAT
    assert game.board.get_piece(2, 4) is None
    
    print("✓ Basic move works!")


def test_invalid_moves():
    """Test invalid move detection."""
    print("\nTesting invalid moves...")
    game = GameState()
    game.start_new_game()
    
    # Try to move BLUE piece on RED's turn
    success, msg = game.make_move(6, 2, 5, 2)
    assert not success, "Should not allow moving opponent's piece"
    
    # Try diagonal move
    success, msg = game.make_move(2, 4, 3, 5)
    assert not success, "Should not allow diagonal move"
    
    print("✓ Invalid moves blocked!")


def test_rat_vs_elephant():
    """Test special rule: Rat defeats Elephant."""
    print("\nTesting Rat vs Elephant rule...")
    board = Board()
    
    # Place RED rat and BLUE elephant next to each other
    from model.piece import Piece
    rat = Piece(PieceType.RAT, Player.RED, 4, 4)
    elephant = Piece(PieceType.ELEPHANT, Player.BLUE, 4, 5)
    
    board.set_piece(4, 4, rat)
    board.set_piece(4, 5, elephant)
    
    validator = MoveValidator(board)
    can_capture, _ = validator._can_capture(rat, 4, 4, elephant, 4, 5)
    
    assert can_capture, "Rat should be able to capture Elephant"
    
    # Test reverse
    can_capture, _ = validator._can_capture(elephant, 4, 5, rat, 4, 4)
    assert not can_capture, "Elephant should NOT capture Rat"
    
    print("✓ Rat vs Elephant rule works!")


def test_water_movement():
    """Test water movement rules."""
    print("\nTesting water movement...")
    board = Board()
    
    from model.piece import Piece
    rat = Piece(PieceType.RAT, Player.RED, 3, 2)
    lion = Piece(PieceType.LION, Player.RED, 3, 2)
    
    board.set_piece(3, 2, rat)
    
    validator = MoveValidator(board)
    
    # Rat should be able to enter water
    can_move, _ = validator.is_valid_move(rat, 3, 1)  # A4 is water
    assert can_move, "Rat should be able to enter water"
    
    # Replace with Lion
    board.set_piece(3, 2, lion)
    
    # Lion should NOT be able to enter water
    can_move, _ = validator.is_valid_move(lion, 3, 1)
    assert not can_move, "Lion should NOT be able to enter water"
    
    print("✓ Water movement rules work!")


def test_undo_redo():
    """Test undo/redo functionality."""
    print("\nTesting undo/redo...")
    game = GameState()
    game.start_new_game()
    
    # Make a move
    original_piece = game.board.get_piece(2, 4)
    game.make_move(2, 4, 3, 4)
    
    # Undo
    success, _ = game.undo()
    assert success, "Undo should succeed"
    assert game.board.get_piece(2, 4) is not None, "Piece should be back at original position"
    assert game.board.get_piece(3, 4) is None, "Destination should be empty"
    
    # Redo
    success, _ = game.redo()
    assert success, "Redo should succeed"
    assert game.board.get_piece(3, 4) is not None, "Piece should be at new position"
    assert game.board.get_piece(2, 4) is None, "Original position should be empty"
    
    print("✓ Undo/redo works!")


def test_save_load():
    """Test save/load functionality."""
    print("\nTesting save/load...")
    game = GameState()
    game.start_new_game()
    
    # Make some moves
    game.make_move(2, 4, 3, 4)  # RED rat
    game.make_move(6, 2, 5, 2)  # BLUE rat
    
    # Save
    success, _ = game.save_to_file("test_save.json")
    assert success, "Save should succeed"
    
    # Create new game and load
    game2 = GameState()
    success, _ = game2.load_from_file("test_save.json")
    assert success, "Load should succeed"
    
    # Verify state
    assert len(game2.move_history) == 2, "Should have 2 moves"
    assert game2.board.get_piece(3, 4) is not None, "RED rat should be at E4"
    assert game2.board.get_piece(5, 2) is not None, "BLUE rat should be at C6"
    
    # Clean up
    import os
    os.remove("test_save.json")
    
    print("✓ Save/load works!")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("RUNNING TESTS")
    print("=" * 50)
    
    try:
        test_board_setup()
        test_basic_move()
        test_invalid_moves()
        test_rat_vs_elephant()
        test_water_movement()
        test_undo_redo()
        test_save_load()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
