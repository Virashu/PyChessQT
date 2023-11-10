from __future__ import annotations
from ..utils import *
from .. import board

class Piece:
    """Abstract Piece"""

    def __init__(self, color: Color):
        self.color = color
        self._moved = False

    def get_color(self) -> Color:
        """Returns piece color"""
        return self.color

    def char(self) -> str:
        """Returns piece representation"""
        ...

    def __str__(self) -> str:
        col = "w" if self.color == Color.WHITE else "b"
        return col + self.char()

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        """Check for abstract move possibility"""
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        if type(board.get_piece(row1, col1)) == "King":
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        return True

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        """Check for abstract attack possibility"""
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color and team_check:
                return False
        return True

    def set_moved(self):
        self._moved = True

    def moved(self):
        return self._moved
