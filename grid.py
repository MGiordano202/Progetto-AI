class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def setCell(self, rows, cols, value):
        self.grid[rows][cols] = value

    def getCell(self, rows, cols):
        return self.grid[rows][cols]

    def isFree(self, rows, cols):
        return self.grid[rows][cols] == 0

    def printGrid(self, screen, images, cell_size):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                image = images.get(value, images["empty"])
                screen.blit(image, (r * cell_size, c * cell_size))
