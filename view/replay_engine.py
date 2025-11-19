"""
Replay Engine for Jungle Game.
Allows stepping through game history.
"""

import time
from model import GameState, Board, Move


class ReplayEngine:
    """
    Engine for replaying games step-by-step.
    """
    
    def __init__(self, game_state: GameState):
        self.moves = game_state.move_history.copy()
        self.current_index = 0
        self.speed = 1.0  # 1x normal speed
        self.is_playing = False
        
        # Create initial board state
        self.board = Board()
        self.board.setup_initial_position()
    
    def reset(self):
        """Reset to beginning of replay."""
        self.current_index = 0
        self.board = Board()
        self.board.setup_initial_position()
    
    def step_forward(self) -> bool:
        """
        Advance one move forward.
        Returns True if successful, False if at end.
        """
        if self.current_index >= len(self.moves):
            return False
        
        move = self.moves[self.current_index]
        self.board.move_piece(move.from_row, move.from_col, move.to_row, move.to_col)
        self.current_index += 1
        return True
    
    def step_backward(self) -> bool:
        """
        Go back one move.
        Returns True if successful, False if at start.
        """
        if self.current_index <= 0:
            return False
        
        self.current_index -= 1
        
        # Rebuild board up to current index
        self.board = Board()
        self.board.setup_initial_position()
        
        for i in range(self.current_index):
            move = self.moves[i]
            self.board.move_piece(move.from_row, move.from_col, move.to_row, move.to_col)
        
        return True
    
    def goto_move(self, move_number: int) -> bool:
        """
        Jump to specific move number (1-indexed).
        Returns True if successful.
        """
        if move_number < 0 or move_number > len(self.moves):
            return False
        
        self.reset()
        for _ in range(move_number):
            if not self.step_forward():
                return False
        
        return True
    
    def play_auto(self, view, delay: float = 1.0):
        """
        Automatically play remaining moves with delay.
        """
        self.is_playing = True
        
        while self.current_index < len(self.moves) and self.is_playing:
            view.clear_screen()
            view.display_board(self.board)
            
            current_move = self.moves[self.current_index]
            print(f"\nMove {current_move.move_number}: {current_move.to_notation(self.board)}")
            print(f"Progress: {self.current_index + 1}/{len(self.moves)}")
            
            time.sleep(delay / self.speed)
            
            if not self.step_forward():
                break
        
        self.is_playing = False
        
        if self.current_index >= len(self.moves):
            print("\n✓ Replay complete!")
    
    def stop_playing(self):
        """Stop auto-play."""
        self.is_playing = False
    
    def set_speed(self, multiplier: float):
        """Set playback speed multiplier."""
        self.speed = max(0.1, min(10.0, multiplier))
    
    def get_current_move(self) -> Move:
        """Get the current move being displayed."""
        if 0 < self.current_index <= len(self.moves):
            return self.moves[self.current_index - 1]
        return None
    
    def get_progress(self) -> tuple:
        """Get current progress (current, total)."""
        return (self.current_index, len(self.moves))
