from . import Piece
from ..utils import *


class King(Piece):
    """King"""

    def char(self) -> str:
        return "K"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        move_x = abs(col - col1)
        move_y = abs(row - row1)
        if move_x not in [0, 1]:
            return False
        if move_y not in [0, 1]:
            return False
        if board.is_under_attack(row1, col1, self.color.opponent()):
            return False
        return True

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)
