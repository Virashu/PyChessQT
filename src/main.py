from PyQt6.QtWidgets import QApplication
import sys

from ui import ChessWindow

# Dependency injection?
#
# from chess.board import Board
# from database import Database
#
# ex = ChessWindow(Board(), Database())


app = QApplication(sys.argv)
ex = ChessWindow()
ex.show()
sys.exit(app.exec())
