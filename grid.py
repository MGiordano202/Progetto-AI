class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, rows, cols, value):
        self.grid[rows][cols] = value

    def get_cell(self, rows, cols):
        return self.grid[rows][cols]

    def is_passable(self, row, col):
        return self.grid[row][col] in [0, "player"]  # Consente al nemico di muoversi su celle libere o occupate dal giocatore

    def is_free(self, rows, cols):
        return self.grid[rows][cols] == 0

    def print_grid(self, screen, images, cell_size):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                image = images.get(value, images["empty"])
                screen.blit(image, (c * cell_size, r * cell_size))

    def print_debug(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
        print("\n")
