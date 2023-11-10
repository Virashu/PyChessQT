from .utils import *
from .board import Board


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
