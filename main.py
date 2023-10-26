from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from PyQt6.QtGui import QPixmap, QIcon, QColorConstants

import sys

from backend import Board, Color


class PawnPromotionDialog(QDialog):
    def __init__(self, c, i, *a) -> None:
        self.color = c
        self.icons = i
        super().__init__(*a)
        self.initUI()

    def initUI(self):
        self.setFixedSize(210, 75)
        color_char = "w" if self.color == Color.WHITE else "b"

        # Player can select Queen, Rook, Bishop or Knight
        piece_chars = ("Q", "R", "B", "N")
        for i, x in enumerate(piece_chars):
            btn = QPushButton(self)
            btn.setGeometry(i * 45 + 15, 15, 45, 45)
            btn.setIcon(QIcon(self.icons[f"{color_char}{x}".lower()]))
            btn.setIconSize(QPixmap(45, 45).size())
            btn.clicked.connect(self.onclick)
            btn.setObjectName(x)

    def onclick(self):
        sender = self.sender()
        if not sender:
            return
        # TODO: somehow return this thing
        self.res = sender.objectName()
        self.accept()


class ChessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_images()
        self.board = Board()
        self.buttons: list[list[QPushButton]] = []
        self.initUI()
        self.select = None
        self.update()

    def initUI(self) -> None:
        self.setWindowTitle("Chess")
        self.setGeometry(100, 100, 390, 390)

        for y in range(8):
            self.buttons.append([])
            for x in range(8):
                btn = QPushButton(self)
                btn.setGeometry(x * 45 + 15, y * 45 + 15, 45, 45)
                id = self.board.cell(y, x)
                btn.setIcon(QIcon(self.icons[id.lower()]))
                btn.setIconSize(QPixmap(45, 45).size())
                btn.clicked.connect(self.onclick)
                btn.setObjectName(f"{y}:{x}")
                self.buttons[y].append(btn)

    def load_images(self) -> None:
        chars = ("wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp")
        self.icons = {}

        for char in chars:
            self.icons[char] = QPixmap(f"icons/{char.lower()}.png")
        self.icons["  "] = QPixmap(45, 45)
        self.icons["  "].fill(QColorConstants.Transparent)

    def onclick(self) -> None:
        sender = self.sender()
        if not sender:
            return
        coords = tuple(map(int, sender.objectName().split(":")))
        if not self.select:
            if not self.board.get_piece(*coords):
                return
            self.select = coords
        else:
            piece = self.board.get_piece(*self.select)
            color = piece.get_color()
            if self.board.is_promoting_move(piece, coords):
                char = self.select_char(color)
                print(char)
                (yf, xf), (y, x) = self.select, coords
                print(self.board.move_and_promote_pawn(yf, xf, y, x, char))
            else:
                self.board.move_piece(*self.select, *coords)
            self.select = None
        self.update()

    def update(self) -> None:
        """Redraw the board"""
        if self.board.get_mate():
            # TODO: show results window
            ...
        # TODO: show who should move on some label
        # board.current_player_color()

        for y in range(8):
            for x in range(8):
                type = (y + x) % 2
                bg = ("#663300", "#ebdbb2")[type]
                if self.select:
                    yf, xf = self.select
                    if self.select == (y, x):
                        bg = "#00cc00"
                    elif self.board.can_castle(yf, xf, y, x):
                        bg = "#00cccc"
                    elif self.board.can_attack(yf, xf, y, x):
                        bg = ["#aa0000", "#ff0000"][type]
                    elif self.board.can_move(yf, xf, y, x):
                        bg = ["#00aaaa", "#00ffff"][type]
                cell = self.board.cell(y, x)
                icon = self.icons[cell.lower()]
                self.buttons[y][x].setStyleSheet(
                    f"background-color: {bg}; border: none;"
                )
                self.buttons[y][x].setIcon(QIcon(icon))
                self.buttons[y][x].update()

    def select_char(self, color: Color) -> str:
        """Creates dialog with selection for Pawn promotion
        :param color: Color of promoted Pawn
        """
        dialog = PawnPromotionDialog(color, self.icons, self)
        dialog.exec()
        return dialog.res


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ChessWindow()
    ex.show()
    sys.exit(app.exec())
