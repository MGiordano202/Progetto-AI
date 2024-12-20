class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, direction, grid):
        moves = { "up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        if direction in moves:
            dr, dc = moves[direction]
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.isFree(new_row, new_col):
                self.row = new_row
                self.col = new_col

    def place_bomb(self, grid):
        grid.setCell(self.row, self.col, "bomb")
