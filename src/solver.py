import time
from utils import get_regions, print_board, clear_screen

class QueensSolver:
    def __init__(self, board: list[list[int]]):
        self.board = board
        self.n = len(board)
        self.regions = get_regions(board)
        self.solution: list[tuple[int, int]] | None = None
        self.iterations = 0
        self.start_time = 0.0
        self.live_update = False
        self.update_interval = 50000
    def is_safe(self, row: int, col: int, queens: list[tuple[int, int]]) -> bool:
        for (qr, qc) in queens:
            if abs(qr - row) <= 1 and abs(qc - col) <= 1:
                return False
        return True

    def is_valid_configuration(self, queens: list[tuple[int, int]]) -> bool:
        n = self.n

        cols = [c for (_, c) in queens]
        if len(set(cols)) != n:
            return False
        regions_used = [self.board[r][c] for (r, c) in queens]
        if len(set(regions_used)) != n:
            return False
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                    return False

        return True

    def solve(self) -> list[tuple[int, int]] | None:
        self.solution = None
        self.iterations = 0
        self.start_time = time.time()

        self.solve_recursive(0, [])
        return self.solution

    def solve_recursive(self, row: int, queens: list[tuple[int, int]]) -> bool:
        n = self.n

        if row == n:
            self.iterations += 1

            if self.live_update and self.iterations % self.update_interval == 0:
                elapsed = time.time() - self.start_time
                clear_screen()
                print("  ╔══════════════════════════════╗")
                print("  ║   Queens Solver - RUNNING    ║")
                print("  ╚══════════════════════════════╝")
                print_board(self.board, queens, self.iterations, elapsed)

            if self.is_valid_configuration(queens):
                self.solution = list(queens)
                return True
            return False

        for col in range(n):
            queens.append((row, col))
            if self.solve_recursive(row + 1, queens):
                return True
            queens.pop()

        return False