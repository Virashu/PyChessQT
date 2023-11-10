from . import Piece
from ..utils import *


class Pawn(Piece):
    """Pawn"""

    def get_color(self) -> Color:
        return self.color

    def char(self) -> str:
        return "P"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        if col != col1:
            return False

        if board.get_piece(row1, col1) is not None:
            return False

        if self.color == Color.WHITE:
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        if row + direction == row1:
            return True

        if (
            row == start_row
            and row + 2 * direction == row1
            and board.field[row + direction][col] is None
        ):
            return True
        return False

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        direction = -1 if (self.color == Color.WHITE) else 1
        return row + direction == row1 and (col + 1 == col1 or col - 1 == col1)
