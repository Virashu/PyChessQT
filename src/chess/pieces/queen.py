from . import Piece
from ..utils import *


class Queen(Piece):
    """Queen"""

    def char(self) -> str:
        return "Q"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False

        if col == col1:
            step = 1 if (row1 >= row) else -1
            for _row in range(row + step, row1, step):
                if board.get_piece(_row, col) is not None:
                    return False
            return True

        if row == row1:
            step = 1 if (col1 >= col) else -1
            for _col in range(col + step, col1, step):
                if board.get_piece(row, _col) is not None:
                    return False
            return True

        delta_row = row - row1
        delta_col = col - col1

        if abs(delta_row) == abs(delta_col):
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
        return False

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1, team_check):
            return False
        return self.can_move(board, row, col, row1, col1)
