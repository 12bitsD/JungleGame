"""
Piece class hierarchy for Jungle Game.
Implements the polymorphic design described in architecture documentation.
"""

from enum import Enum
from abc import ABC, abstractmethod


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


class Piece(ABC):
    """
    Abstract base class for game pieces.
    """
    
    def __init__(self, owner: Player, row: int, col: int):
        self.owner = owner
        self.row = row
        self.col = col
    
    @property
    @abstractmethod
    def piece_type(self) -> PieceType:
        """Return the type of the piece."""
        pass
    
    @property
    def rank(self) -> int:
        """Returns the rank/power of the piece."""
        return self.piece_type.value
    
    def get_symbol(self) -> str:
        """Returns a display symbol for the piece."""
        # Default implementation using a mapping
        symbols = {
            PieceType.RAT: 'R',
            PieceType.CAT: 'C',
            PieceType.DOG: 'D',
            PieceType.WOLF: 'W',
            PieceType.LEOPARD: 'L',
            PieceType.TIGER: 'T',
            PieceType.LION: 'N',
            PieceType.ELEPHANT: 'E'
        }
        symbol = symbols[self.piece_type]
        return symbol.lower() if self.owner == Player.RED else symbol.upper()
    
    def get_name(self) -> str:
        """Returns the full name of the piece."""
        return self.piece_type.name.capitalize()
    
    def can_swim(self) -> bool:
        """Returns True if the piece can enter water."""
        return False
    
    def can_jump(self) -> bool:
        """Returns True if the piece can jump over river."""
        return False
    
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
        """Deserialize piece from dictionary using factory pattern."""
        piece_type = PieceType[data['type']]
        owner = Player[data['owner']]
        row = data['row']
        col = data['col']
        
        return Piece.create(piece_type, owner, row, col)
        
    @staticmethod
    def create(piece_type: PieceType, owner: Player, row: int, col: int) -> 'Piece':
        """Factory method to create specific piece instances."""
        class_map = {
            PieceType.RAT: Rat,
            PieceType.CAT: Cat,
            PieceType.DOG: Dog,
            PieceType.WOLF: Wolf,
            PieceType.LEOPARD: Leopard,
            PieceType.TIGER: Tiger,
            PieceType.LION: Lion,
            PieceType.ELEPHANT: Elephant
        }
        
        if piece_type not in class_map:
            raise ValueError(f"Unknown piece type: {piece_type}")
            
        return class_map[piece_type](owner, row, col)


# Concrete Piece Classes

class Rat(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.RAT
        
    def can_swim(self) -> bool:
        return True


class Cat(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.CAT


class Dog(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.DOG


class Wolf(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.WOLF


class Leopard(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.LEOPARD


class Tiger(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.TIGER
        
    def can_jump(self) -> bool:
        return True


class Lion(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.LION
        
    def can_jump(self) -> bool:
        return True


class Elephant(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.ELEPHANT
