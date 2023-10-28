"""Chess"""


from enum import Enum
from itertools import product


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Board:
    """Main chess board"""

    def __init__(self):
        self.check: Color | None = None
        self.mate: Color | None = None
        self.color = Color.WHITE
        self.field: list[list[Piece | None]] = []

        for _ in range(8):
            self.field.append([None] * 8)

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
        self.field[6] = [
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
            Pawn(Color.WHITE),
        ]
        self.field[1] = [
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
            Pawn(Color.BLACK),
        ]
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

        # self.field[0] = [None, None, None, Pawn(Color.WHITE), King(Color.WHITE), Pawn(Color.WHITE), None, None]
        # self.field[1] = [None, None, None, Pawn(Color.WHITE), Pawn(Color.WHITE), Pawn(Color.WHITE), None, None]
        # self.field[7] = [None, None, None, Queen(Color.WHITE), King(Color.BLACK), Queen(Color.BLACK), None, None]

    def current_player_color(self) -> Color:
        """Returns active color"""
        return self.color

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
                return False
        elif dest.get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)
        self.check_check()
        return True

    def is_under_attack(self, row: int, col: int, color: Color) -> bool:
        """Check if cell is under attack.
        `row`: Row
        `col`: Column
        `color`: Attacking side's color
        """
        for i in range(8):
            for j in range(8):
                piece = self.field[i][j]
                if piece is None:
                    continue
                if piece.get_color() != color:
                    continue
                if piece.can_attack(self, i, j, row, col):
                    return True
        return False

    def is_promoting_move(self, piece, move: tuple) -> bool:
        color = piece.get_color()
        return (
            isinstance(piece, Pawn)
            and (color == Color.WHITE and move[0] == 7)
            or (color == Color.BLACK and move[0] == 0)
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
        if not (piece.get_color() == Color.WHITE and row1 == 7) and not (
            piece.get_color() == Color.BLACK and row1 == 0
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

        self.field[row][col] = None
        self.field[row1][col1] = new_piece
        self.check_check()
        self.color = opponent(self.color)
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
                    if self.is_under_attack(i, j, opponent(king_piece.get_color())):
                        self.check = king_piece.get_color()
                        self.mate_check(i, j, king_piece)

    def get_check(self) -> Color | None:
        """Returns current check state"""
        return self.check

    def mate_check(self, row: int, col: int, king_piece: "King") -> None:
        """Check for mate on board"""

        for i, j in product(range(-1, 1), range(-1, 1)):
            if king_piece.can_move(
                self, row, col, row + i, col + j
            ) or king_piece.can_attack(self, row, col, row + i, col + j):
                self.mate = None
        self.mate = king_piece.get_color()

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
        return piece.can_attack(self, row, col, row1, col1)

    def can_castle(self, row: int, col: int, row1: int, col1: int) -> bool:
        """Check for castlig possibility"""
        if col1 not in (0, 7):
            return False
        row_ = 0 if self.color == Color.WHITE else 7
        if row != row1 != row_:
            return False
        # king = self.field[row][4]
        king = self.field[row][col]

        if not isinstance(king, King):
            return False
        if king.get_color() != self.color:
            return False

        rook = self.field[row][col]

        if not isinstance(rook, Rook):
            return False
        if rook.get_color() != self.color:
            return False

        cells = 4 if col == 0 else 3
        for i in range(1, cells):
            if self.field[row][i] is not None:
                return False
        return True

    def castling(self):
        # TODO
        ...


class Piece:
    """Abstract Piece"""

    def __init__(self, color) -> None:
        self.color = color

    def get_color(self) -> Color:
        """Returns piece color"""
        return self.color

    def char(self) -> str:
        """Returns piece representation"""
        ...

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        """Check for abstract move possibility"""
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        return True

    def can_attack(
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        """Check for abstract attack possibility"""
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        return True


class Rook(Piece):
    """Rook"""

    def get_color(self) -> int:
        return self.color

    def char(self) -> str:
        return "R"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
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
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Pawn(Piece):
    """Pawn"""

    def get_color(self) -> int:
        return self.color

    def char(self) -> str:
        return "P"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        if col != col1:
            return False

        if board.get_piece(row1, col1) is not None:
            return False

        if self.color == Color.WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

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
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        direction = 1 if (self.color == Color.WHITE) else -1
        return row + direction == row1 and (col + 1 == col1 or col - 1 == col1)


class Knight(Piece):
    """Knight"""

    def char(self) -> str:
        return "N"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        delta_row = abs(row - row1)
        delta_col = abs(col - col1)

        if sorted([delta_row, delta_col]) == [1, 2]:
            return True
        return False

    def can_attack(
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    """Bishop"""

    def char(self) -> str:
        return "B"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        delta_row = row - row1
        delta_col = col - col1

        if abs(delta_row) != abs(delta_col):
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
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):
    """Queen"""

    def char(self) -> str:
        return "Q"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
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
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class King(Piece):
    """King"""

    def char(self) -> str:
        return "K"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        move_x = abs(col - col1)
        move_y = abs(row - row1)
        if move_x not in [0, 1]:
            return False
        if move_y not in [0, 1]:
            return False
        if board.is_under_attack(row1, col1, opponent(self.color)):
            return False
        return True

    def can_attack(
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


def opponent(color: Color):
    """Returns opposite color"""
    if color == Color.WHITE:
        return Color.BLACK
    return Color.WHITE


def correct_coords(row, col):
    """Check if coords is inside board bounds"""
    return 0 <= row < 8 and 0 <= col < 8


def print_board(board):
    """Output board to console"""
    print("     +----+----+----+----+----+----+----+----+")
    for row in range(7, -1, -1):
        print(" ", row, end="  ")
        for col in range(8):
            print("|", board.cell(row, col), end=" ")
        print("|")
        print("     +----+----+----+----+----+----+----+----+")
    print(end="        ")
    for col in range(8):
        print(col, end="    ")
    print()


def main():
    """main"""
    board = Board()

    while True:
        print_board(board)

        print(
            f"Commands:\n\texit\t\t\t\t-- exit\n\tmove <row> <col> <row1> <col1>\t\t\t\t-- move from (row, col) to (row1, col1)"
        )

        if board.current_player_color() == Color.WHITE:
            print("Turn of white:")
        else:
            print("Turn of black:")
        command = input()
        if command == "exit":
            break
        _, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print("Turn succeeded")
        else:
            print("Wrong coords! Try again!")


if __name__ == "__main__":
    main()
