import random

class Enemy:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, grid):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)
        for dr, dc in moves:
            new_row = self.row + dr
            new_col = self.col + dc
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.isFree(new_row, new_col):
                self.row = new_row
                self.col = new_col
                break
