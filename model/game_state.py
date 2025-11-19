"""
GameState class for Jungle Game.
Manages the complete game state including board, turn, history, and win conditions.
"""

from typing import Optional, List, Tuple
from datetime import datetime
import json
from model.board import Board
from model.piece import Player, Piece
from model.move import Move, MoveValidator


class GameStatus:
    """Game status constants."""
    IN_PROGRESS = "IN_PROGRESS"
    RED_WIN = "RED_WIN"
    BLUE_WIN = "BLUE_WIN"
    DRAW = "DRAW"


class GameState:
    """
    Manages the complete state of a game.
    
    Attributes:
        board: The game board
        current_player: Player whose turn it is
        move_history: List of all moves made
        move_count_no_capture: Counter for 50-move rule
        position_history: For detecting threefold repetition
        game_status: Current status of the game
        undo_stack: Stack for undo functionality (max 10)
        redo_stack: Stack for redo functionality
    """
    
    MAX_UNDO_LEVELS = 10
    MAX_MOVES_WITHOUT_CAPTURE = 50
    
    def __init__(self):
        self.board = Board()
        self.current_player = Player.RED
        self.move_history: List[Move] = []
        self.move_count_no_capture = 0
        self.position_history: List[str] = []
        self.game_status = GameStatus.IN_PROGRESS
        self.captured_pieces = {Player.RED: [], Player.BLUE: []}
        
        # Undo/Redo stacks
        self.undo_stack: List[dict] = []
        self.redo_stack: List[dict] = []
    
    def start_new_game(self):
        """Initialize a new game."""
        self.board = Board()
        self.board.setup_initial_position()
        self.current_player = Player.RED
        self.move_history = []
        self.move_count_no_capture = 0
        self.position_history = [self._get_position_hash()]
        self.game_status = GameStatus.IN_PROGRESS
        self.captured_pieces = {Player.RED: [], Player.BLUE: []}
        self.undo_stack = []
        self.redo_stack = []
    
    def make_move(self, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> Tuple[bool, str]:
        """
        Execute a move if valid.
        Returns (success, message).
        """
        if self.game_status != GameStatus.IN_PROGRESS:
            return False, "Game has ended"
        
        piece = self.board.get_piece(from_row, from_col)
        if not piece:
            return False, "No piece at starting position"
        
        if piece.owner != self.current_player:
            return False, "Not your turn"
        
        # Validate move
        validator = MoveValidator(self.board)
        is_valid, error = validator.is_valid_move(piece, to_row, to_col)
        if not is_valid:
            return False, error
        
        # Save state for undo
        self._save_undo_state()
        
        # Execute move
        captured = self.board.move_piece(from_row, from_col, to_row, to_col)
        
        # Record move
        move = Move(
            piece, from_row, from_col, to_row, to_col,
            captured, len(self.move_history) + 1
        )
        self.move_history.append(move)
        
        # Update captured pieces
        if captured:
            opponent = Player.RED if self.current_player == Player.BLUE else Player.BLUE
            self.captured_pieces[opponent].append(captured)
            self.move_count_no_capture = 0
        else:
            self.move_count_no_capture += 1
        
        # Check win/draw conditions
        self._check_game_end(to_row, to_col)
        
        # Switch player
        if self.game_status == GameStatus.IN_PROGRESS:
            self.current_player = Player.BLUE if self.current_player == Player.RED else Player.RED
            
            # Update position history
            self.position_history.append(self._get_position_hash())
            
            # Check for threefold repetition
            if self._check_threefold_repetition():
                self.game_status = GameStatus.DRAW
                return True, "Draw by threefold repetition"
            
            # Check for 50-move rule
            if self.move_count_no_capture >= self.MAX_MOVES_WITHOUT_CAPTURE:
                self.game_status = GameStatus.DRAW
                return True, "Draw by 50-move rule"
            
            # Check if current player has any legal moves
            if not self._has_legal_moves(self.current_player):
                opponent = Player.RED if self.current_player == Player.BLUE else Player.BLUE
                self.game_status = GameStatus.RED_WIN if opponent == Player.RED else GameStatus.BLUE_WIN
                return True, f"{opponent.value} wins! Opponent has no legal moves"
        
        # Clear redo stack when new move is made
        self.redo_stack = []
        
        return True, "Move successful"
    
    def _save_undo_state(self):
        """Save current state to undo stack."""
        state = {
            'board': self._serialize_board(),
            'current_player': self.current_player.value,
            'move_count_no_capture': self.move_count_no_capture,
            'captured_pieces': {
                Player.RED.value: [p.to_dict() for p in self.captured_pieces[Player.RED]],
                Player.BLUE.value: [p.to_dict() for p in self.captured_pieces[Player.BLUE]]
            },
            'last_move': self.move_history[-1].to_dict() if self.move_history else None
        }
        
        self.undo_stack.append(state)
        
        # Limit undo stack size
        if len(self.undo_stack) > self.MAX_UNDO_LEVELS:
            self.undo_stack.pop(0)
    
    def undo(self) -> Tuple[bool, str]:
        """Undo the last move."""
        if not self.undo_stack:
            return False, "No moves to undo"
        
        if self.game_status != GameStatus.IN_PROGRESS:
            return False, "Cannot undo after game ended"
        
        # Save current state to redo stack
        current_state = {
            'board': self._serialize_board(),
            'current_player': self.current_player.value,
            'move_count_no_capture': self.move_count_no_capture,
            'captured_pieces': {
                Player.RED.value: [p.to_dict() for p in self.captured_pieces[Player.RED]],
                Player.BLUE.value: [p.to_dict() for p in self.captured_pieces[Player.BLUE]]
            },
            'last_move': self.move_history[-1].to_dict() if self.move_history else None
        }
        self.redo_stack.append(current_state)
        
        # Restore previous state
        state = self.undo_stack.pop()
        self._restore_state(state)
        
        # Remove last move from history
        if self.move_history:
            self.move_history.pop()
        
        # Remove last position from history
        if self.position_history:
            self.position_history.pop()
        
        return True, "Move undone"
    
    def redo(self) -> Tuple[bool, str]:
        """Redo a previously undone move."""
        if not self.redo_stack:
            return False, "No moves to redo"
        
        # Save current state to undo stack
        self._save_undo_state()
        
        # Restore redo state
        state = self.redo_stack.pop()
        self._restore_state(state)
        
        # Restore move to history
        if state['last_move']:
            move = Move.from_dict(state['last_move'])
            self.move_history.append(move)
        
        # Restore position to history
        self.position_history.append(self._get_position_hash())
        
        return True, "Move redone"
    
    def _restore_state(self, state: dict):
        """Restore game state from dictionary."""
        self._deserialize_board(state['board'])
        self.current_player = Player[state['current_player']]
        self.move_count_no_capture = state['move_count_no_capture']
        self.captured_pieces = {
            Player.RED: [Piece.from_dict(p) for p in state['captured_pieces']['RED']],
            Player.BLUE: [Piece.from_dict(p) for p in state['captured_pieces']['BLUE']]
        }
    
    def _check_game_end(self, to_row: int, to_col: int):
        """Check if game has ended after a move."""
        # Check den occupation
        if self.board.is_opponent_den(to_row, to_col, self.current_player):
            self.game_status = GameStatus.RED_WIN if self.current_player == Player.RED else GameStatus.BLUE_WIN
    
    def _has_legal_moves(self, player: Player) -> bool:
        """Check if player has any legal moves."""
        pieces = self.board.get_all_pieces(player)
        validator = MoveValidator(self.board)
        
        for piece in pieces:
            if validator.get_legal_moves(piece):
                return True
        
        return False
    
    def _get_position_hash(self) -> str:
        """Generate a hash of current position for repetition detection."""
        # Include piece positions and current player
        position_data = []
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                piece = self.board.get_piece(row, col)
                if piece:
                    position_data.append(f"{piece.owner.value}_{piece.piece_type.name}_{row}_{col}")
        
        position_data.append(f"TURN_{self.current_player.value}")
        return "|".join(sorted(position_data))
    
    def _check_threefold_repetition(self) -> bool:
        """Check if current position has occurred 3 times."""
        current_hash = self.position_history[-1]
        count = self.position_history.count(current_hash)
        return count >= 3
    
    def _serialize_board(self) -> List[List[Optional[dict]]]:
        """Serialize board to list of lists."""
        serialized = []
        for row in range(self.board.ROWS):
            row_data = []
            for col in range(self.board.COLS):
                piece = self.board.get_piece(row, col)
                row_data.append(piece.to_dict() if piece else None)
            serialized.append(row_data)
        return serialized
    
    def _deserialize_board(self, data: List[List[Optional[dict]]]):
        """Deserialize board from list of lists."""
        self.board = Board()
        for row in range(self.board.ROWS):
            for col in range(self.board.COLS):
                if data[row][col]:
                    piece = Piece.from_dict(data[row][col])
                    self.board.set_piece(row, col, piece)
    
    def save_to_file(self, filename: str) -> Tuple[bool, str]:
        """Save game state to JSON file."""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'current_player': self.current_player.value,
                'move_count_no_capture': self.move_count_no_capture,
                'game_status': self.game_status,
                'board': self._serialize_board(),
                'move_history': [move.to_dict() for move in self.move_history],
                'position_history': self.position_history,
                'captured_pieces': {
                    'RED': [p.to_dict() for p in self.captured_pieces[Player.RED]],
                    'BLUE': [p.to_dict() for p in self.captured_pieces[Player.BLUE]]
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True, f"Game saved to {filename}"
        except Exception as e:
            return False, f"Failed to save: {str(e)}"
    
    def load_from_file(self, filename: str) -> Tuple[bool, str]:
        """Load game state from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self._deserialize_board(data['board'])
            self.current_player = Player[data['current_player']]
            self.move_count_no_capture = data['move_count_no_capture']
            self.game_status = data['game_status']
            self.move_history = [Move.from_dict(m) for m in data['move_history']]
            self.position_history = data['position_history']
            self.captured_pieces = {
                Player.RED: [Piece.from_dict(p) for p in data['captured_pieces']['RED']],
                Player.BLUE: [Piece.from_dict(p) for p in data['captured_pieces']['BLUE']]
            }
            
            # Clear undo/redo stacks after load
            self.undo_stack = []
            self.redo_stack = []
            
            return True, f"Game loaded from {filename}"
        except FileNotFoundError:
            return False, "File not found"
        except json.JSONDecodeError:
            return False, "Invalid save file format"
        except Exception as e:
            return False, f"Failed to load: {str(e)}"
