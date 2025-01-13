from pygame.examples import grid


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, rows, cols, value):
        self.grid[rows][cols] = value

    def get_cell(self, rows, cols):
        return self.grid[rows][cols]

    def is_passable(self, rows, cols):
        return self.grid[rows][cols] in [0, "P"]  # Consente al nemico di muoversi su celle libere o occupate dal giocatore

    def set_wall(self, rows, cols):
        self.grid[rows][cols] = "W"

    def is_wall(self, rows, cols):
        return self.grid[rows][cols] == "W"

    def is_free(self, rows, cols):
        return self.grid[rows][cols] == 0

    def get_neighbors(self, rows, cols):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #movivimenti sulla griglia
            new_row, new_col = rows + dr, cols + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                if self.is_passable(new_row, new_col):
                    neighbors.append((new_row, new_col))
        return neighbors

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
