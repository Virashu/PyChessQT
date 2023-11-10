__name__ = "Chess board module"
__all__ = ["Board"]

from itertools import product
from .utils import *
from .pieces import *


class Board:
    """Main chess board class"""

    def __init__(self):
        self.check: Color | None = None
        self.mate: Color | None = None
        self.color = Color.WHITE
        self.field: list[list[Piece | None]] = []

        # Fill the field with blank cells 8x8
        self.field.extend([[None] * 8 for _ in range(8)])

        self.field[0] = [
            Rook(Color.BLACK),
            Knight(Color.BLACK),
            Bishop(Color.BLACK),
            Queen(Color.BLACK),
            King(Color.BLACK),
            Bishop(Color.BLACK),
            Knight(Color.BLACK),
            Rook(Color.BLACK),
        ]

        #  PyLance says that `Pawn` is not `Piece` 😑
        self.field[1].clear()
        self.field[1].extend(
            [
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
                Pawn(Color.BLACK),
            ]
        )
        self.field[6].clear()
        self.field[6].extend(
            [
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
                Pawn(Color.WHITE),
            ]
        )
        self.field[7] = [
            Rook(Color.WHITE),
            Knight(Color.WHITE),
            Bishop(Color.WHITE),
            Queen(Color.WHITE),
            King(Color.WHITE),
            Bishop(Color.WHITE),
            Knight(Color.WHITE),
            Rook(Color.WHITE),
        ]

    def field_as_text(self) -> str:
        return ";".join(
            [",".join(map(lambda a: str(a) if a else "_", row)) for row in self.field]
        )

    def field_from_text(self, text: str) -> None:
        rows = text.split(";")
        for y, row in enumerate(rows):
            pieces = row.split(",")
            for x, piece_code in enumerate(pieces):
                if piece_code == "_":
                    self.field[y][x] = None
                else:
                    # `w`, `Q` = `wQ`
                    color_char, piece_char = piece_code
                    color = {"w": Color.WHITE, "b": Color.BLACK}[color_char]
                    piece_class = {
                        "P": Pawn,
                        "K": King,
                        "Q": Queen,
                        "B": Bishop,
                        "N": Knight,
                        "R": Rook,
                    }[piece_char]
                    self.field[y][x] = piece_class(color)

    def current_player_color(self) -> Color:
        """Returns active color"""
        return self.color

    def set_active_color(self, color: Color) -> None:
        self.color = color

    def cell(self, row: int, col: int) -> str:
        """Returns string of two symbols, color and piece type, if cell (row, col) is not empty, else two spaces"""
        piece = self.field[row][col]
        if piece is None:
            return "  "
        color = piece.get_color()
        color_char = "w" if color == Color.WHITE else "b"
        return color_char + piece.char()

    def move_piece(self, row: int, col: int, row1: int, col1: int) -> bool:
        """Move piece from point (row, col) to point (row1, col1).
        Returns whether move succeeded or not"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        dest = self.field[row1][col1]
        if dest is None:
            if not piece.can_move(self, row, col, row1, col1):
                if isinstance(piece, King):
                    if self.can_castle(row, col, row1, col1):
                        piece.set_moved()
                        self.color = self.color.opponent()
                        return self.castle(row, col, row1, col1)
                return False
        elif dest.get_color() == piece.get_color().opponent():
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        piece.set_moved()
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = self.color.opponent()
        self.check_check()
        return True

    def is_under_attack(self, row: int, col: int, color: Color) -> bool:
        """Check if cell is under attack.
        `row`: Row
        `col`: Column
        `color`: Attacking side's color
        """
        for i, j in product(range(8), range(8)):
            piece = self.field[i][j]
            if piece is None:
                continue
            if piece.get_color() != color:
                continue
            # if piece.can_attack(self, i, j, row, col):
            #     return True
            if piece.can_attack(self, i, j, row, col, team_check=False):
                return True
        return False

    def is_promoting_move(self, row, col, row1, col1) -> bool:
        piece = self.field[row][col]
        if not isinstance(piece, Pawn):
            return False
        if not self.can_move(row, col, row1, col1) and not self.can_attack(
            row, col, row1, col1
        ):
            return False
        color = piece.get_color()
        return (color == Color.WHITE and row1 == 0) or (
            color == Color.BLACK and row1 == 7
        )

    def get_piece(self, row: int, col: int) -> "Piece | None":
        """Returns piece in cell (row, col)"""
        return self.field[row][col]

    def move_and_promote_pawn(
        self, row: int, col: int, row1: int, col1: int, char: str
    ) -> bool:
        """Moves and promotes Pawn"""
        piece = self.get_piece(row, col)

        if piece is None:
            return False
        if not isinstance(piece, Pawn):
            return False
        if not piece.can_move(self, row, col, row1, col1) and not piece.can_attack(
            self, row, col, row1, col1
        ):
            return False
        if not (piece.get_color() == Color.WHITE and row1 == 0) and not (
            piece.get_color() == Color.BLACK and row1 == 7
        ):
            return False

        # https://pastebin.com/hmaJ5zDx
        color = piece.get_color()

        if char == "Q":
            new_piece = Queen(color)
        elif char == "R":
            new_piece = Rook(color)
        elif char == "B":
            new_piece = Bishop(color)
        elif char == "N":
            new_piece = Knight(color)
        else:
            return False

        new_piece.set_moved()
        self.field[row][col] = None
        self.field[row1][col1] = new_piece
        self.check_check()
        self.color = self.color.opponent()
        return True

    def check_check(self) -> None:
        """Check if king is under attack"""
        self.check = None
        for i in range(8):
            for j in range(8):
                king_piece = self.field[i][j]
                if king_piece is None:
                    continue
                if isinstance(king_piece, King):
                    if self.is_under_attack(i, j, king_piece.get_color().opponent()):
                        self.check = king_piece.get_color().opponent()
                        self.mate_check(i, j, king_piece)

    def get_check(self) -> Color | None:
        """Returns current check state"""
        return self.check

    def mate_check(self, row: int, col: int, king_piece: "King") -> None:
        """Check for mate on board"""

        for i, j in product(range(-1, 1), range(-1, 1)):
            if king_piece.can_move(
                self, row, col, row + i, col + j
            ):  # or king_piece.can_attack(self, row, col, row + i, col + j):
                self.mate = None
                return
        self.mate = king_piece.get_color().opponent()

    def get_mate(self) -> Color | None:
        """Returns current mate state"""
        return self.mate

    def can_move(self, row, col, row1, col1) -> bool:
        """Check for move possibility"""
        piece = self.field[row][col]
        if piece is None:
            return False
        color = piece.get_color()
        if self.color != color:
            return False
        if isinstance(piece, King):
            if self.can_castle(row, col, row1, col1):
                return True
        return piece.can_move(self, row, col, row1, col1)

    def can_attack(self, row, col, row1, col1) -> bool:
        """Check for attack possibility"""
        piece = self.field[row][col]
        if piece is None:
            return False
        att_piece = self.field[row1][col1]
        if att_piece is None:
            return False
        color = piece.get_color()
        if self.color != color:
            return False
        if att_piece.get_color() == color:
            return False
        if isinstance(att_piece, King):
            return False
        return piece.can_attack(self, row, col, row1, col1)

    def can_castle(self, row: int, col: int, row1: int, col1: int) -> bool:
        """Check for castlig possibility"""
        if col1 == 2:
            rook_col = 0
            empty = (1, 2, 3)
        elif col1 == 6:
            rook_col = 7
            empty = (5, 6)
        else:
            return False

        if row != row1:
            return False

        king = self.field[row][col]

        if not isinstance(king, King):
            return False

        if king.get_color() != self.color:
            return False

        rook = self.field[row][rook_col]

        if not isinstance(rook, Rook):
            return False

        if rook.get_color() != self.color:
            return False

        if king.moved() or rook.moved():
            return False

        for i in empty:
            if self.field[row][i]:
                return False

        return True

    def castle(self, row, col, row1, col1):
        """Castle"""
        if not self.can_castle(row, col, row1, col1):
            return False
        if col1 == 2:
            rook_col = 0
            rook_col_dest = 3
        else:
            rook_col = 7
            rook_col_dest = 5

        # Move king
        self.field[row][col1], self.field[row][col] = self.field[row][col], None

        # Move rook
        self.field[row][rook_col_dest], self.field[row][rook_col] = (
            self.field[row][rook_col],
            None,
        )

        self.field[row][rook_col_dest].set_moved()
        self.field[row][col1].set_moved()

        return True
