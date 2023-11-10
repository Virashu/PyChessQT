from . import Piece
from ..utils import *


class Rook(Piece):
    """Rook"""

    def get_color(self) -> Color:
        return self.color

    def char(self) -> str:
        return "R"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for _r in range(row + step, row1, step):
            if board.get_piece(_r, col) is not None:
                return False

        step = 1 if (col1 >= col) else -1
        for _c in range(col + step, col1, step):
            if board.get_piece(row, _c) is not None:
                return False
        return True

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)
