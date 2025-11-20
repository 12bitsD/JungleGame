"""
Unit tests for GameState.
Exercises functionality: Game flow, turn management, Undo/Redo, Save/Load.
"""

import unittest
import os
import json
from model.game_state import GameState, GameStatus
from model.piece import PieceType, Player
from model.board import Board
from unittest.mock import patch, mock_open

class TestGameState(unittest.TestCase):
    
    def setUp(self):
        self.game_state = GameState()
        self.game_state.start_new_game()

    def test_turn_switching(self):
        """
        Functionality: Verify turn switches after valid move.
        Expected Result: Current player changes from Red to Blue.
        """
        self.assertEqual(self.game_state.current_player, Player.RED)
        
        # Valid move: Red Lion (2,0) -> (1,0) [Backward to empty square]
        # (3,0) is Water, so forward is blocked. (2,1) is Dog, blocked.
        success, msg = self.game_state.make_move(2, 0, 1, 0)
        self.assertTrue(success, f"Move failed: {msg}")
        
        self.assertEqual(self.game_state.current_player, Player.BLUE)

    def test_undo_redo_functionality(self):
        """
        Functionality: Verify Undo and Redo logic.
        Expected Result: Board state and player revert correctly.
        """
        # Initial state
        initial_piece = self.game_state.board.get_piece(2, 0)
        self.assertIsNotNone(initial_piece)
        
        # Make a move: Red Lion (2,0) -> (1,0)
        success, msg = self.game_state.make_move(2, 0, 1, 0)
        self.assertTrue(success, f"Move failed: {msg}")
        
        self.assertIsNone(self.game_state.board.get_piece(2, 0))
        self.assertIsNotNone(self.game_state.board.get_piece(1, 0))
        self.assertEqual(self.game_state.current_player, Player.BLUE)
        
        # Undo
        success, _ = self.game_state.undo()
        self.assertTrue(success)
        self.assertEqual(self.game_state.current_player, Player.RED)
        self.assertIsNotNone(self.game_state.board.get_piece(2, 0))
        self.assertIsNone(self.game_state.board.get_piece(1, 0))
        
        # Redo
        success, _ = self.game_state.redo()
        self.assertTrue(success)
        self.assertEqual(self.game_state.current_player, Player.BLUE)
        self.assertIsNone(self.game_state.board.get_piece(2, 0))
        self.assertIsNotNone(self.game_state.board.get_piece(1, 0))

    def test_save_load_game(self):
        """
        Functionality: Verify Save and Load game state.
        Expected Result: Loaded state exactly matches saved state.
        """
        filename = "test_save.json"
        
        # Make a move to change state: Red Lion (2,0) -> (1,0)
        self.game_state.make_move(2, 0, 1, 0)
        current_history_len = len(self.game_state.move_history)
        
        # Save
        success, _ = self.game_state.save_to_file(filename)
        self.assertTrue(success)
        
        # Reset game
        self.game_state.start_new_game()
        self.assertEqual(len(self.game_state.move_history), 0)
        
        # Load
        success, _ = self.game_state.load_from_file(filename)
        self.assertTrue(success)
        
        # Verify state
        self.assertEqual(len(self.game_state.move_history), current_history_len)
        self.assertEqual(self.game_state.current_player, Player.BLUE)
        self.assertIsNotNone(self.game_state.board.get_piece(1, 0))
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

    def test_save_load_with_capture(self):
        """
        Functionality: Verify Save/Load preserves capture history.
        """
        filename = "test_save_capture.json"
        
        # Setup capture: Rat (0,0) captures Elephant (0,1)
        from model.piece import Piece
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        ele = Piece.create(PieceType.ELEPHANT, Player.BLUE, 0, 1)
        self.game_state.board = Board() # Clear
        self.game_state.board.set_piece(0, 0, rat)
        self.game_state.board.set_piece(0, 1, ele)
        self.game_state.move_history = [] # Clear history
        
        self.game_state.make_move(0, 0, 0, 1) # Capture
        
        self.game_state.save_to_file(filename)
        
        self.game_state.start_new_game()
        self.game_state.load_from_file(filename)
        
        last_move = self.game_state.move_history[-1]
        self.assertIsNotNone(last_move.captured)
        self.assertEqual(last_move.captured.piece_type, PieceType.ELEPHANT)
        
        if os.path.exists(filename):
            os.remove(filename)

    def test_win_condition(self):
        """
        Functionality: Verify game ends when entering opponent den.
        Expected Result: Game status updates to RED_WIN.
        """
        # Cheat: Move Red Lion directly near Blue Den (8,3)
        # Valid approach: Set board manually
        # Blue Den is at (8,3). Trap at (8,2).
        
        from model.piece import Piece
        lion = Piece.create(PieceType.LION, Player.RED, 8, 2) # In trap next to den
        self.game_state.board.set_piece(8, 2, lion)
        
        # Execute winning move
        success, msg = self.game_state.make_move(8, 2, 8, 3)
        self.assertTrue(success)
        
        self.assertEqual(self.game_state.game_status, GameStatus.RED_WIN)

    def test_50_move_rule(self):
        """
        Functionality: Verify 50-move draw rule.
        Expected Result: Game ends in DRAW.
        """
        # Set counter to 49
        self.game_state.move_count_no_capture = 49
        
        # Make a non-capture move
        # Move Red Lion (2,0) -> (1,0)
        self.game_state.make_move(2, 0, 1, 0)
        
        # Should now be 50 -> Draw
        self.assertEqual(self.game_state.move_count_no_capture, 50)
        self.assertEqual(self.game_state.game_status, GameStatus.DRAW)

    def test_no_legal_moves_win(self):
        """
        Functionality: Verify win if opponent has no moves.
        Expected Result: Current player wins.
        """
        # Clear board
        self.game_state.board = Board() # Empty
        
        # Place Red Rat at (0,0) surrounded by water/traps? Hard to construct fully trapped.
        # Easier: Just 1 piece for Red, 0 for Blue.
        # Blue has no pieces -> has no moves.
        # Red moves. Game checks if BLUE has moves.
        
        from model.piece import Piece
        rat = Piece.create(PieceType.RAT, Player.RED, 0, 0)
        self.game_state.board.set_piece(0, 0, rat)
        
        # Blue has no pieces.
        # Red moves (0,0) -> (0,1)
        self.game_state.make_move(0, 0, 0, 1)
        
        # Now it's Blue's turn. 
        # make_move logic:
        # ... Switch player ...
        # Check if current player (Blue) has moves.
        # If not, Red wins.
        
        self.assertEqual(self.game_state.game_status, GameStatus.RED_WIN)

    def test_save_load_errors(self):
        """
        Functionality: Verify error handling in Save/Load.
        Expected Result: Returns False and error message.
        """
        # Test FileNotFoundError
        success, msg = self.game_state.load_from_file("non_existent_file.json")
        self.assertFalse(success)
        self.assertEqual(msg, "File not found")
        
        # Test JSONDecodeError
        with patch("builtins.open", mock_open(read_data="invalid json")):
            success, msg = self.game_state.load_from_file("bad.json")
            self.assertFalse(success)
            self.assertEqual(msg, "Invalid save file format")
            
        # Test generic Exception during save (e.g., permission error)
        with patch("builtins.open", side_effect=PermissionError("Denied")):
            success, msg = self.game_state.save_to_file("readonly.json")
            self.assertFalse(success)
            self.assertIn("Failed to save", msg)
            
        # Test generic Exception during load
        with patch("builtins.open", side_effect=PermissionError("Denied")):
            success, msg = self.game_state.load_from_file("readonly.json")
            self.assertFalse(success)
            self.assertIn("Failed to load", msg)

    def test_game_end_checks(self):
        """
        Functionality: Verify game end conditions when moving.
        """
        # Simulate game end
        self.game_state.game_status = GameStatus.RED_WIN
        success, msg = self.game_state.make_move(0, 0, 0, 1)
        self.assertFalse(success)
        self.assertEqual(msg, "Game has ended")
        
        # Add a state to undo stack so we don't hit "No moves to undo" first
        self.game_state.undo_stack.append({}) 
        
        # Verify cannot undo after game end
        success, msg = self.game_state.undo()
        self.assertFalse(success)
        self.assertEqual(msg, "Cannot undo after game ended")

    def test_make_move_errors(self):
        """
        Functionality: Verify make_move error branches.
        """
        # No piece at source
        self.game_state.board.set_piece(0, 0, None)
        success, msg = self.game_state.make_move(0, 0, 0, 1)
        self.assertFalse(success)
        self.assertEqual(msg, "No piece at starting position")
        
        # Not your turn (Blue trying to move Red piece)
        # Reset board
        self.game_state.start_new_game()
        
        # Note: start_new_game puts Red Lion at (2,0). (8,6) is Blue Lion.
        # Game starts with Red turn.
        # If we try to move (8,6), it is Blue piece.
        # BUT (8,6) actually HAS a Blue piece in setup_initial_position.
        # Wait, (8,6) is G9. Blue Lion starts at (6,6) which is G7? No.
        # Let's check board.py:
        # Blue pieces: ... (LION, 6, 6), ... 
        # So at 8,6 there is nothing?
        # (8,4) is WOLF. 
        # Let's try moving (6,6) which is Blue Lion.
        
        success, msg = self.game_state.make_move(6, 6, 6, 5)
        self.assertFalse(success)
        self.assertEqual(msg, "Not your turn")
        
        # Invalid move (Validator returns False)
        # Try moving Red Lion (2,0) to (2,2) -> Jump 2 squares to land (invalid basic move)
        success, msg = self.game_state.make_move(2, 0, 2, 2)
        self.assertFalse(success)
        
    def test_empty_undo_redo(self):
        """
        Functionality: Verify undo/redo on empty stacks.
        """
        self.game_state.undo_stack = []
        success, msg = self.game_state.undo()
        self.assertFalse(success)
        
        self.game_state.redo_stack = []
        success, msg = self.game_state.redo()
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
