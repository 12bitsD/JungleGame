"""
Piece class for Jungle Game.
Represents a game piece with type, owner, rank, and position.
"""

from enum import Enum


class PieceType(Enum):
    """Enumeration of all piece types with their ranks."""
    RAT = 1
    CAT = 2
    DOG = 3
    WOLF = 4
    LEOPARD = 5
    TIGER = 6
    LION = 7
    ELEPHANT = 8


class Player(Enum):
    """Enumeration of players."""
    RED = "RED"
    BLUE = "BLUE"


class Piece:
    """
    Represents a game piece.
    
    Attributes:
        piece_type: Type of the piece (RAT, CAT, etc.)
        owner: Owner of the piece (RED or BLUE)
        row: Current row position (0-8)
        col: Current column position (0-6)
    """
    
    def __init__(self, piece_type: PieceType, owner: Player, row: int, col: int):
        self.piece_type = piece_type
        self.owner = owner
        self.row = row
        self.col = col
    
    @property
    def rank(self) -> int:
        """Returns the rank/power of the piece."""
        return self.piece_type.value
    
    def get_symbol(self) -> str:
        """Returns a display symbol for the piece."""
        symbols = {
            PieceType.RAT: 'R',
            PieceType.CAT: 'C',
            PieceType.DOG: 'D',
            PieceType.WOLF: 'W',
            PieceType.LEOPARD: 'L',
            PieceType.TIGER: 'T',
            PieceType.LION: 'N',  # L is taken by Leopard
            PieceType.ELEPHANT: 'E'
        }
        symbol = symbols[self.piece_type]
        return symbol.lower() if self.owner == Player.RED else symbol.upper()
    
    def get_name(self) -> str:
        """Returns the full name of the piece."""
        return self.piece_type.name.capitalize()
    
    def can_swim(self) -> bool:
        """Returns True if the piece can enter water."""
        return self.piece_type == PieceType.RAT
    
    def can_jump(self) -> bool:
        """Returns True if the piece can jump over river."""
        return self.piece_type in (PieceType.LION, PieceType.TIGER)
    
    def __repr__(self):
        return f"{self.owner.value}_{self.piece_type.name}"
    
    def to_dict(self) -> dict:
        """Serialize piece to dictionary for saving."""
        return {
            'type': self.piece_type.name,
            'owner': self.owner.value,
            'row': self.row,
            'col': self.col
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Piece':
        """Deserialize piece from dictionary."""
        return Piece(
            PieceType[data['type']],
            Player[data['owner']],
            data['row'],
            data['col']
        )
