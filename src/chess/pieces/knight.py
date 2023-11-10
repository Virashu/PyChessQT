from . import Piece


class Knight(Piece):
    """Knight"""

    def char(self) -> str:
        return "N"

    def can_move(self, board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        delta_row = abs(row - row1)
        delta_col = abs(col - col1)

        if sorted([delta_row, delta_col]) == [1, 2]:
            return True
        return False

    def can_attack(
        self, board, row: int, col: int, row1: int, col1: int, team_check=True
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)
