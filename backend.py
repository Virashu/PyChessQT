"""Шахматы"""


class Board:
    """Main chess board"""

    def __init__(self):
        self.check = None
        self.mate = None
        self.color = WHITE
        self.field = []
        for _ in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE),
            Knight(WHITE),
            Bishop(WHITE),
            Queen(WHITE),
            King(WHITE),
            Bishop(WHITE),
            Knight(WHITE),
            Rook(WHITE),
        ]
        self.field[1] = [
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
            Pawn(WHITE),
        ]
        self.field[6] = [
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
            Pawn(BLACK),
        ]
        self.field[7] = [
            Rook(BLACK),
            Knight(BLACK),
            Bishop(BLACK),
            Queen(BLACK),
            King(BLACK),
            Bishop(BLACK),
            Knight(BLACK),
            Rook(BLACK),
        ]
        # self.field[0] = [None, None, None, Pawn(WHITE), King(WHITE), Pawn(WHITE), None, None]
        # self.field[1] = [None, None, None, Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), None, None]
        # self.field[7] = [None, None, None, Queen(WHITE), King(BLACK), Queen(BLACK), None, None]

    def current_player_color(self) -> int:
        """Возвращает ходящую в данный момент сторону"""
        return self.color

    def cell(self, row: int, col: int) -> str:
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return "  "
        color = piece.get_color()
        color_char = "w" if color == WHITE else "b"
        return color_char + piece.char()

    def move_piece(self, row: int, col: int, row1: int, col1: int) -> bool:
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        self.check_check()
        return True

    def is_under_attack(self, row: int, col: int, color: int) -> bool:
        """Метод, проверяющий бито ли поле.
        `row`: Ряд
        `col`: Колонка
        `color`: Атакующая сторона
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
            and (color == WHITE and move[0] == 7)
            or (color == BLACK and move[0] == 0)
        )

    def get_piece(self, row: int, col: int) -> "Piece":
        """Возвращает фигуру по координатам row, col"""
        return self.field[row][col]

    def move_and_promote_pawn(
        self, row: int, col: int, row1: int, col1: int, char: str
    ) -> bool:
        """Двигает пешку и выполняет превращение"""
        piece = self.get_piece(row, col)

        if piece is None:
            return False
        if not isinstance(piece, Pawn):
            return False
        if not piece.can_move(self, row, col, row1, col1) and not piece.can_attack(
            self, row, col, row1, col1
        ):
            return False
        if not (piece.get_color() == WHITE and row1 == 7) and not (
            piece.get_color() == BLACK and row1 == 0
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
        """Проверяет наличие шаха на доске"""
        self.check = None
        for i in range(8):
            for j in range(8):
                kpiece = self.field[i][j]
                if kpiece is None:
                    continue
                if isinstance(kpiece, King):
                    if self.is_under_attack(i, j, opponent(kpiece.get_color())):
                        self.check = kpiece.get_color()
                        self.mate_check(i, j)

    def get_check(self) -> int:
        """Возаращает состояние шаха"""
        return self.check or 0

    def mate_check(self, row: int, col: int) -> bool:
        """Проверяет, есть ли мат на доске"""
        king = self.field[row][col]

        for i in range(-1, 1):
            for j in range(-1, 1):
                if king.can_move(self, row, col, row + i, col + j) or king.can_attack(
                    self, row, col, row + i, col + j
                ):
                    return False
        self.mate = king.get_color()
        return True

    def get_mate(self):
        """Возвращает состояние мата"""
        return self.mate

    def can_move(self, row, col, row1, col1) -> bool:
        """Проверка на возможность хода"""
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
        """Проверка на возможность взятия"""
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
        """Проверка на возможность рокировки Короля"""
        if col1 not in (0, 7):
            return False
        row_ = 0 if self.color == WHITE else 7
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
    """Абстрактная фигура"""

    def __init__(self, color: int) -> None:
        self.color = color

    def get_color(self) -> int:
        """Возвращает цвет фигуры"""
        return self.color

    def char(self) -> str:
        """Возвращает кодовое имя фигуры"""
        ...

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        """Проверка на возможность хода"""
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
        """Проверка на возможность взятия"""
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
    """Rook - ладья"""

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
    """Pawn - пешка"""

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

        if self.color == WHITE:
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
        direction = 1 if (self.color == WHITE) else -1
        return row + direction == row1 and (col + 1 == col1 or col - 1 == col1)


class Knight(Piece):
    """Knight - конь"""

    def char(self) -> str:
        return "N"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        posr = abs(row - row1)
        posc = abs(col - col1)

        if sorted([posr, posc]) == [1, 2]:
            return True
        return False

    def can_attack(
        self, board: Board, row: int, col: int, row1: int, col1: int
    ) -> bool:
        if not super().can_attack(board, row, col, row1, col1):
            return False
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    """Bishop - слон"""

    def char(self) -> str:
        return "B"

    def can_move(self, board: Board, row: int, col: int, row1: int, col1: int) -> bool:
        if not super().can_move(board, row, col, row1, col1):
            return False
        posr = row - row1
        posc = col - col1

        if abs(posr) != abs(posc):
            return False

        step_x = 1 if col < col1 else -1
        step_y = 1 if row < row1 else -1

        for i in range(1, abs(posr)):
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
    """Queen - ферзь"""

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

        posr = row - row1
        posc = col - col1

        if abs(posr) == abs(posc):
            step_x = 1 if col < col1 else -1
            step_y = 1 if row < row1 else -1

            for i in range(1, abs(posr)):
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
    """King - король"""

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


def opponent(color: int):
    """Возвращает цвет противника"""
    if color == WHITE:
        return BLACK
    return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


def print_board(board):
    """Вывод доски в консоль"""
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

        print("Команды:")
        print("    exit                               -- выход")
        print("    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)")
        print("                                          в клетку (row1, col1)")

        if board.current_player_color() == WHITE:
            print("Ход белых:")
        else:
            print("Ход черных:")
        command = input()
        if command == "exit":
            break
        _, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print("Ход успешен")
        else:
            print("Координаты некорректы! Попробуйте другой ход!")


if __name__ == "__main__":
    WHITE = 1
    BLACK = 2
    main()

WHITE = 1
BLACK = 2
