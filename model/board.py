"""
Board class for Jungle Game.
Manages the 7x9 grid and special squares (traps, dens, rivers).
"""

from enum import Enum
from typing import Optional, List, Tuple
from model.piece import Piece, PieceType, Player


class SquareType(Enum):
    """Enumeration of square types on the board."""
    NORMAL = "NORMAL"
    TRAP = "TRAP"
    DEN = "DEN"
    WATER = "WATER"


class Board:
    """
    Represents the game board (7 columns x 9 rows).
    
    Coordinate system:
    - Columns: 0-6 (A-G)
    - Rows: 0-8 (1-9, where 0 is bottom RED side, 8 is top BLUE side)
    """
    
    ROWS = 9
    COLS = 7
    
    # Special square coordinates
    RED_DEN = (0, 3)  # D1
    RED_TRAPS = [(0, 2), (0, 4), (1, 3)]  # C1, E1, D2
    
    BLUE_DEN = (8, 3)  # D9
    BLUE_TRAPS = [(8, 2), (8, 4), (7, 3)]  # C9, E9, D8
    
    # Water squares (rivers): rows 3-5 (4-6 in 1-indexed), cols 0-1 and 5-6
    WATER_SQUARES = [
        (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1),  # Left river
        (3, 5), (3, 6), (4, 5), (4, 6), (5, 5), (5, 6)   # Right river
    ]
    
    def __init__(self):
        """Initialize empty board with terrain types."""
        self.grid: List[List[Optional[Piece]]] = [
            [None for _ in range(self.COLS)] for _ in range(self.ROWS)
        ]
        self.terrain = self._init_terrain()
    
    def _init_terrain(self) -> List[List[SquareType]]:
        """Initialize terrain types for all squares."""
        terrain = [[SquareType.NORMAL for _ in range(self.COLS)] 
                   for _ in range(self.ROWS)]
        
        # Set dens
        terrain[self.RED_DEN[0]][self.RED_DEN[1]] = SquareType.DEN
        terrain[self.BLUE_DEN[0]][self.BLUE_DEN[1]] = SquareType.DEN
        
        # Set traps
        for row, col in self.RED_TRAPS:
            terrain[row][col] = SquareType.TRAP
        for row, col in self.BLUE_TRAPS:
            terrain[row][col] = SquareType.TRAP
        
        # Set water
        for row, col in self.WATER_SQUARES:
            terrain[row][col] = SquareType.WATER
        
        return terrain
    
    def setup_initial_position(self):
        """Set up pieces in their starting positions."""
        # RED pieces (bottom, rows 0-2)
        red_pieces = [
            (PieceType.LION, 2, 0),     # A3
            (PieceType.DOG, 2, 1),      # B3
            (PieceType.CAT, 2, 2),      # C3
            (PieceType.ELEPHANT, 1, 3), # D2
            (PieceType.RAT, 2, 4),      # E3
            (PieceType.LEOPARD, 2, 5),  # F3
            (PieceType.TIGER, 2, 6),    # G3
            (PieceType.WOLF, 0, 2),     # C1
        ]
        
        for piece_type, row, col in red_pieces:
            self.grid[row][col] = Piece.create(piece_type, Player.RED, row, col)
        
        # BLUE pieces (top, rows 6-8, mirror of RED)
        blue_pieces = [
            (PieceType.TIGER, 6, 0),    # A7
            (PieceType.LEOPARD, 6, 1),  # B7
            (PieceType.RAT, 6, 2),      # C7
            (PieceType.ELEPHANT, 7, 3), # D8
            (PieceType.CAT, 6, 4),      # E7
            (PieceType.DOG, 6, 5),      # F7
            (PieceType.LION, 6, 6),     # G7
            (PieceType.WOLF, 8, 4),     # E9
        ]
        
        for piece_type, row, col in blue_pieces:
            self.grid[row][col] = Piece.create(piece_type, Player.BLUE, row, col)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at specified position."""
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]
    
    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        """Set piece at specified position."""
        if self.is_valid_position(row, col):
            self.grid[row][col] = piece
            if piece:
                piece.row = row
                piece.col = col
    
    def remove_piece(self, row: int, col: int) -> Optional[Piece]:
        """Remove and return piece at specified position."""
        piece = self.get_piece(row, col)
        if piece:
            self.grid[row][col] = None
        return piece
    
    def move_piece(self, from_row: int, from_col: int, 
                   to_row: int, to_col: int) -> Optional[Piece]:
        """
        Move piece from one position to another.
        Returns captured piece if any.
        """
        piece = self.remove_piece(from_row, from_col)
        captured = self.remove_piece(to_row, to_col)
        if piece:
            self.set_piece(to_row, to_col, piece)
        return captured
    
    def get_terrain(self, row: int, col: int) -> SquareType:
        """Get terrain type at specified position."""
        if not self.is_valid_position(row, col):
            return SquareType.NORMAL
        return self.terrain[row][col]
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board boundaries."""
        return 0 <= row < self.ROWS and 0 <= col < self.COLS
    
    def is_water(self, row: int, col: int) -> bool:
        """Check if square is water."""
        return self.get_terrain(row, col) == SquareType.WATER
    
    def is_trap(self, row: int, col: int, player: Player) -> bool:
        """Check if square is opponent's trap for given player."""
        terrain = self.get_terrain(row, col)
        if terrain != SquareType.TRAP:
            return False
        
        # Check if it's opponent's trap
        if player == Player.RED:
            return (row, col) in self.BLUE_TRAPS
        else:
            return (row, col) in self.RED_TRAPS
    
    def is_den(self, row: int, col: int, player: Player) -> bool:
        """Check if square is specific player's den."""
        if player == Player.RED:
            return (row, col) == self.RED_DEN
        else:
            return (row, col) == self.BLUE_DEN
    
    def is_opponent_den(self, row: int, col: int, player: Player) -> bool:
        """Check if square is opponent's den for given player."""
        if player == Player.RED:
            return (row, col) == self.BLUE_DEN
        else:
            return (row, col) == self.RED_DEN
    
    def get_all_pieces(self, player: Optional[Player] = None) -> List[Piece]:
        """Get all pieces on board, optionally filtered by player."""
        pieces = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.get_piece(row, col)
                if piece and (player is None or piece.owner == player):
                    pieces.append(piece)
        return pieces
    
    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.get_piece(row, col)
                if piece:
                    new_piece = Piece.create(piece.piece_type, piece.owner, row, col)
                    new_board.set_piece(row, col, new_piece)
        return new_board
    
    @staticmethod
    def col_to_letter(col: int) -> str:
        """Convert column index to letter (0->A, 1->B, etc.)."""
        return chr(ord('A') + col)
    
    @staticmethod
    def letter_to_col(letter: str) -> int:
        """Convert column letter to index (A->0, B->1, etc.)."""
        return ord(letter.upper()) - ord('A')
    
    @staticmethod
    def row_to_number(row: int) -> int:
        """Convert row index to display number (0->1, 1->2, etc.)."""
        return row + 1
    
    @staticmethod
    def number_to_row(number: int) -> int:
        """Convert display number to row index (1->0, 2->1, etc.)."""
        return number - 1
    
    def position_to_notation(self, row: int, col: int) -> str:
        """Convert position to algebraic notation (e.g., 'E3')."""
        return f"{self.col_to_letter(col)}{self.row_to_number(row)}"
    
    def notation_to_position(self, notation: str) -> Tuple[int, int]:
        """Convert algebraic notation to position (e.g., 'E3' -> (2, 4))."""
        col = self.letter_to_col(notation[0])
        row = self.number_to_row(int(notation[1]))
        return row, col
