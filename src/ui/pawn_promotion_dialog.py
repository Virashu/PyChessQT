from PyQt6.QtWidgets import QPushButton, QDialog
from PyQt6.QtGui import QPixmap, QIcon


class PawnPromotionDialog(QDialog):
    def __init__(self, c, i, *a) -> None:
        self.color = c
        self.icons = i
        super().__init__(*a)
        self.initUI()

    def initUI(self):
        self.setFixedSize(210, 75)
        color_char = repr(self.color)

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
        self.res = sender.objectName()
        self.accept()
