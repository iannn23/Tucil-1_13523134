import os
import sys
from typing import Optional


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


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

def is_valid_board(board: list[list[int]]):
    n = len(board)
    if n < 2:
        return False

    for row in board:
        if len(row) != n:
            return False
        for val in row:
            if not isinstance(val, int) or val < 1 or val > n:
                return False

    regions = set()
    for row in board:
        for val in row:
            regions.add(val)

    if len(regions) != n:
        return False

    return True


def get_regions(board: list[list[int]]):
    regions: dict[int, list[tuple[int, int]]] = {}
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val not in regions:
                regions[val] = []
            regions[val].append((r, c))
    return regions


def print_board(board: list[list[int]], queens: list[tuple[int, int]] = None,
                iteration: int = None, elapsed: float = None):
    n = len(board)
    queen_set = set(queens) if queens else set()

    COLORS = [
        '\033[41m',  # Red 
        '\033[42m',  # Green 
        '\033[43m',  # Yellow 
        '\033[44m',  # Blue 
        '\033[45m',  # Magenta 
        '\033[46m',  # Cyan 
        '\033[47m',  # White 
        '\033[101m', # Bright Red 
        '\033[102m', # Bright Green 
        '\033[103m', # Bright Yellow 
    ]
    RESET = '\033[0m'
    BOLD = '\033[1m'

    print()
    print("   " + "  ".join(f"{c:2}" for c in range(n)))
    print("   " + "---" * n)

    for r in range(n):
        row_str = f"{r:2} |"
        for c in range(n):
            region = board[r][c]
            color = COLORS[(region - 1) % len(COLORS)]
            if (r, c) in queen_set:
                cell = f"{BOLD}{color} # {RESET}"
            else:
                cell = f"{color} {region} {RESET}"
            row_str += cell
        print(row_str)

    print()
    if iteration is not None:
        print(f"  Iterations: {iteration:,}")
    if elapsed is not None:
        print(f"  Elapsed:    {elapsed:.3f}s")
    print()


def save_solution(filename: str, board: list[list[int]], queens: list[tuple[int, int]]):
    n = len(board)
    queen_set = set(queens)

    with open(filename, 'w') as f:
        f.write("Queens LinkedIn Puzzle - Solution\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Board size: {n}×{n}\n")
        f.write(f"Queens placed: {len(queens)}\n\n")

        f.write("Board (# = queen, number = region):\n")
        f.write("   " + "  ".join(f"{c:2}" for c in range(n)) + "\n")
        f.write("   " + "---" * n + "\n")
        for r in range(n):
            row_str = f"{r:2} |"
            for c in range(n):
                if (r, c) in queen_set:
                    row_str += "  #"
                else:
                    row_str += f"  {board[r][c]}"
            f.write(row_str + "\n")

        f.write("\nQueen Positions (row, col):\n")
        for i, (r, c) in enumerate(sorted(queens)):
            f.write(f"  Row {r}, Col {c} -> Region {board[r][c]}\n")

    print(f"  Solution saved to: {filename}")