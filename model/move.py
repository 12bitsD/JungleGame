"""
Move class and move validation logic for Jungle Game.
Implements all game rules from specification.
"""

from typing import Optional, Tuple
from model.piece import Piece, PieceType, Player
from model.board import Board, SquareType


class Move:
    """
    Represents a single move in the game.
    
    Attributes:
        piece: The piece being moved
        from_row, from_col: Starting position
        to_row, to_col: Destination position
        captured: Piece captured (if any)
        move_number: Sequential move number in game
    """
    
    def __init__(self, piece: Piece, from_row: int, from_col: int,
                 to_row: int, to_col: int, captured: Optional[Piece] = None,
                 move_number: int = 0):
        self.piece = piece
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.captured = captured
        self.move_number = move_number
    
    def to_notation(self, board: Board) -> str:
        """Convert move to readable notation."""
        piece_name = self.piece.get_name()
        player = self.piece.owner.value
        from_pos = board.position_to_notation(self.from_row, self.from_col)
        to_pos = board.position_to_notation(self.to_row, self.to_col)
        
        if self.captured:
            captured_name = self.captured.get_name()
            return f"{self.move_number}. {player} {piece_name} {from_pos}→{to_pos} (captured {captured_name})"
        else:
            return f"{self.move_number}. {player} {piece_name} {from_pos}→{to_pos}"
    
    def to_dict(self) -> dict:
        """Serialize move to dictionary."""
        return {
            'piece': self.piece.to_dict(),
            'from_row': self.from_row,
            'from_col': self.from_col,
            'to_row': self.to_row,
            'to_col': self.to_col,
            'captured': self.captured.to_dict() if self.captured else None,
            'move_number': self.move_number
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Move':
        """Deserialize move from dictionary."""
        from model.piece import Piece
        return Move(
            Piece.from_dict(data['piece']),
            data['from_row'],
            data['from_col'],
            data['to_row'],
            data['to_col'],
            Piece.from_dict(data['captured']) if data['captured'] else None,
            data['move_number']
        )


class MoveValidator:
    """
    Validates moves according to game rules.
    Implements the validation algorithm from specification § 7.
    """
    
    def __init__(self, board: Board):
        self.board = board
    
    def is_valid_move(self, piece: Piece, to_row: int, to_col: int) -> Tuple[bool, str]:
        """
        Validate if piece can move to destination.
        Returns (is_valid, error_message).
        """
        from_row, from_col = piece.row, piece.col
        
        # 1. Basic checks
        if not self.board.is_valid_position(to_row, to_col):
            return False, "Move out of bounds"
        
        # Check if it's a jump move
        is_jump = self._is_jump_move(from_row, from_col, to_row, to_col)
        
        if not is_jump:
            # Normal move: must be exactly 1 square
            distance = abs(to_row - from_row) + abs(to_col - from_col)
            if distance != 1:
                return False, "Can only move 1 square at a time"
        
        # Must be orthogonal (no diagonal)
        if not self._is_orthogonal(from_row, from_col, to_row, to_col):
            return False, "Cannot move diagonally"
        
        # 2. Terrain checks
        to_terrain = self.board.get_terrain(to_row, to_col)
        
        if to_terrain == SquareType.WATER:
            if not piece.can_swim():
                return False, "Cannot enter water"
        
        # 3. Jump validation (Lion/Tiger)
        if is_jump:
            if not piece.can_jump():
                return False, "Only Lion and Tiger can jump"
            
            is_valid_jump, error = self._validate_jump(from_row, from_col, to_row, to_col)
            if not is_valid_jump:
                return False, error
        
        # 4. Den entry check
        if to_terrain == SquareType.DEN:
            if self.board.is_den(to_row, to_col, piece.owner):
                return False, "Cannot enter own den"
        
        # 5. Friendly piece collision
        target_piece = self.board.get_piece(to_row, to_col)
        if target_piece and target_piece.owner == piece.owner:
            return False, "Cannot capture own piece"
        
        # 6. Capture validation
        if target_piece:
            can_capture, error = self._can_capture(
                piece, from_row, from_col, target_piece, to_row, to_col
            )
            if not can_capture:
                return False, error
        
        return True, ""
    
    def _is_orthogonal(self, from_row: int, from_col: int, 
                      to_row: int, to_col: int) -> bool:
        """Check if move is orthogonal (horizontal or vertical)."""
        return from_row == to_row or from_col == to_col
    
    def _is_jump_move(self, from_row: int, from_col: int,
                     to_row: int, to_col: int) -> bool:
        """Check if move is a jump (distance > 1)."""
        distance = abs(to_row - from_row) + abs(to_col - from_col)
        return distance > 1
    
    def _validate_jump(self, from_row: int, from_col: int,
                      to_row: int, to_col: int) -> Tuple[bool, str]:
        """Validate river jump for Lion/Tiger."""
        # Check if jump is horizontal or vertical
        if from_row != to_row and from_col != to_col:
            return False, "Can only jump horizontally or vertically"
        
        # Get the water squares in the jump path
        water_squares = self._get_jump_path_squares(from_row, from_col, to_row, to_col)
        
        if not water_squares:
            return False, "Jump path is not a valid river crossing"
        
        # Check if all squares in path are water
        for row, col in water_squares:
            if not self.board.is_water(row, col):
                return False, "Can only jump over river"
        
        # Check if any Rat is in the water path
        for row, col in water_squares:
            piece = self.board.get_piece(row, col)
            if piece and piece.piece_type == PieceType.RAT:
                return False, "Jump blocked by Rat"
        
        # Validate landing square is land
        if self.board.is_water(to_row, to_col):
            return False, "Must land on land square"
        
        return True, ""
    
    def _get_jump_path_squares(self, from_row: int, from_col: int,
                               to_row: int, to_col: int) -> list:
        """Get the water squares in jump path."""
        squares = []
        
        if from_row == to_row:  # Horizontal jump
            min_col = min(from_col, to_col)
            max_col = max(from_col, to_col)
            for col in range(min_col + 1, max_col):
                squares.append((from_row, col))
        else:  # Vertical jump
            min_row = min(from_row, to_row)
            max_row = max(from_row, to_row)
            for row in range(min_row + 1, max_row):
                squares.append((row, from_col))
        
        # Validate this is a river crossing (should be exactly 3 water squares)
        if len(squares) != 3:
            return []
        
        return squares
    
    def _can_capture(self, attacker: Piece, attacker_row: int, attacker_col: int,
                    defender: Piece, defender_row: int, defender_col: int) -> Tuple[bool, str]:
        """
        Validate if attacker can capture defender.
        Implements capture rules from specification § 4.
        """
        # Rat in water protection
        if defender.piece_type == PieceType.RAT and self.board.is_water(defender_row, defender_col):
            if attacker.piece_type != PieceType.RAT:
                return False, "Only Rat can attack Rat in water"
        
        # Get effective ranks (accounting for traps)
        attacker_rank = attacker.rank
        if self.board.is_trap(attacker_row, attacker_col, attacker.owner):
            attacker_rank = 0
        
        defender_rank = defender.rank
        if self.board.is_trap(defender_row, defender_col, defender.owner):
            defender_rank = 0
        
        # Special rule: Rat defeats Elephant
        if attacker.piece_type == PieceType.RAT and defender.piece_type == PieceType.ELEPHANT:
            return True, ""
        
        if attacker.piece_type == PieceType.ELEPHANT and defender.piece_type == PieceType.RAT:
            return False, "Elephant cannot capture Rat"
        
        # General hierarchy rule
        if attacker_rank >= defender_rank:
            return True, ""
        else:
            return False, f"Cannot capture higher rank piece (rank {attacker_rank} vs {defender_rank})"
    
    def get_legal_moves(self, piece: Piece) -> list:
        """Get all legal destination squares for a piece."""
        legal_moves = []
        from_row, from_col = piece.row, piece.col
        
        # Check normal moves (4 adjacent squares)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            to_row, to_col = from_row + dr, from_col + dc
            if self.board.is_valid_position(to_row, to_col):
                is_valid, _ = self.is_valid_move(piece, to_row, to_col)
                if is_valid:
                    legal_moves.append((to_row, to_col))
        
        # Check jump moves for Lion/Tiger
        if piece.can_jump():
            jump_targets = self._get_jump_targets(from_row, from_col)
            for to_row, to_col in jump_targets:
                is_valid, _ = self.is_valid_move(piece, to_row, to_col)
                if is_valid:
                    legal_moves.append((to_row, to_col))
        
        return legal_moves
    
    def _get_jump_targets(self, from_row: int, from_col: int) -> list:
        """Get potential jump target squares for Lion/Tiger."""
        targets = []
        
        # Horizontal jumps (across rivers)
        # Left river: cols 0-1, right river: cols 5-6
        if 3 <= from_row <= 5:  # In river row range
            # Jump across left river
            if from_col == 2:
                targets.append((from_row, 0))
                targets.append((from_row, 1))
            elif from_col in (0, 1):
                targets.append((from_row, 2))
            
            # Jump across right river
            if from_col == 4:
                targets.append((from_row, 5))
                targets.append((from_row, 6))
            elif from_col in (5, 6):
                targets.append((from_row, 4))
        
        # Vertical jumps
        # Can jump from row 2 to 6 or vice versa (crossing rows 3-5)
        if from_col in (0, 1, 5, 6):  # In river columns
            if from_row == 2:
                targets.append((6, from_col))
            elif from_row == 6:
                targets.append((2, from_col))
        
        return targets
