from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2

    def opponent(self) -> "Color":
        return Color.WHITE if self == Color.BLACK else Color.BLACK

    def __repr__(self) -> str:
        return "w" if self == Color.WHITE else "b"

    def __str__(self) -> str:
        return "White" if self == Color.WHITE else "Black"


def correct_coords(row, col):
    """Check if coords is inside board bounds"""
    return 0 <= row < 8 and 0 <= col < 8


if __name__ == "__main__":
    col = Color.WHITE
    print(col.opponent())
