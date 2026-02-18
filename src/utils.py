import os

def read_board(filename: str) -> list[list[int]]:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    board = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                row = list(map(int, line.split()))
            except ValueError:
                raise ValueError(f"Invalid board format in line: '{line}'")
            board.append(row)

    if not board:
        raise ValueError("Board file is empty.")

    if not is_valid_board(board):
        raise ValueError("Board configuration is invalid.")

    return board