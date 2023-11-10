from . import Piece
from ..utils import *


class Bishop(Piece):
    """Bishop"""

    def char(self) -> str:
        return "B"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        delta_row = abs(row - row1)
        delta_col = abs(col - col1)

        if delta_row != delta_col:
            return False

        step_x = 1 if col < col1 else -1
        step_y = 1 if row < row1 else -1

        for i in range(1, abs(delta_row)):
            _row = i * step_y + row
            _col = i * step_x + col
            if not correct_coords(_row, _col):
                continue

            if board.get_piece(_row, _col) is not None:
                return False

        return True

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)
