import sys
import os
import time
import glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import read_board, print_board, save_solution, clear_screen
from solver import QueensSolver


BANNER = """
╔══════════════════════════════════════════════════════╗
║         Queens LinkedIn Puzzle Solver                ║
║         IF2211 Tugas Kecil 1 - Brute Force           ║
╚══════════════════════════════════════════════════════╝
"""


def list_test_files() -> list[str]:
    test_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test')
    files = sorted(glob.glob(os.path.join(test_dir, '*.txt')))
    return files


def select_file() -> str:
    print(BANNER)
    test_files = list_test_files()

    print("  Available test cases:")
    print("  " + "─" * 40)

    if test_files:
        for i, f in enumerate(test_files, 1):
            print(f"  [{i}] {os.path.basename(f)}")
    else:
        print("  (no test files found in test/ directory)")

    print(f"  [0] Enter custom file path")
    print()

    while True:
        choice = input("  Select option: ").strip()

        if choice == '0':
            path = input("  Enter file path: ").strip()
            return path

        try:
            idx = int(choice)
            if 1 <= idx <= len(test_files):
                return test_files[idx - 1]
        except ValueError:
            pass

        print("  Invalid choice. Try again.")


def display_solution(board, queens, iterations, elapsed, found):
    clear_screen()
    print(BANNER)

    n = len(board)
    print(f"  Board size:  {n}×{n}")
    print(f"  Iterations:  {iterations:,}")
    print(f"  Time:        {elapsed:.4f}s")
    print()

    if found:
        print("  ✓ SOLUTION FOUND!")
        print_board(board, queens)

        print("  Queen positions:")
        print("  " + "─" * 40)
        for r, c in sorted(queens):
            region = board[r][c]
            print(f"    Row {r:2d}, Col {c:2d}  →  Region {region}")
        print()

        print("  Constraint verification:")
        cols = sorted(set(c for _, c in queens))
        regions = sorted(set(board[r][c] for r, c in queens))
        print(f"    ✓ One queen per row     ({len(queens)}/{n})")
        print(f"    ✓ One queen per column  ({len(cols)}/{n}): {cols}")
        print(f"    ✓ One queen per region  ({len(regions)}/{n}): {regions}")
        print(f"    ✓ No adjacent queens")
    else:
        print("  ✗ NO SOLUTION EXISTS for this board.")
        print_board(board, [])

    print()


def ask_save(board, queens, board_file):
    choice = input("  Save solution to file? [y/N]: ").strip().lower()
    if choice == 'y':
        base = os.path.splitext(os.path.basename(board_file))[0]
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test')
        out_file = os.path.join(out_dir, f"{base}_solution.txt")
        save_solution(out_file, board, queens)


def ask_live_update() -> bool:
    choice = input("  Enable live board visualization during solving? [y/N]: ").strip().lower()
    return choice == 'y'


def run_solver(board_file: str):
    print(BANNER)
    print(f"  Loading: {board_file}")
    print()

    try:
        board = read_board(board_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"  ERROR: {e}")
        return

    n = len(board)
    print(f"  Board loaded: {n}×{n} with {n} color regions")
    print()
    print("  Initial board:")
    print_board(board, [])

    live = ask_live_update()
    print()
    print("  Starting brute force solver...")
    print(f"  Worst case iterations: {n}^{n} = {n**n:,}")
    print()

    solver = QueensSolver(board)
    solver.live_update = live

    start = time.time()
    solution = solver.solve()
    elapsed = time.time() - start

    display_solution(board, solution or [], solver.iterations, elapsed, solution is not None)

    if solution:
        ask_save(board, solution, board_file)

    print()
    input("  Press Enter to continue...")


def main():
    if len(sys.argv) > 1:
        board_file = sys.argv[1]
    else:
        board_file = select_file()

    if not board_file:
        print("  No file selected. Exiting.")
        return

    run_solver(board_file)


if __name__ == '__main__':
    main()