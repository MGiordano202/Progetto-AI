class Grid:
    def __init__(self, row, cols):
        self.row = row
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(row)]

    def setCell(self, row, col, value):
        self.grid[row][col] = value

    def getCell(self, row, col):
        return self.grid[row][col]

    def isFree(self, row, col):
        return self.grid[row][col] == 0

    def printGrid(self, screen, images, cell_size):
        for r in range(self.row):
            for c in range(self.cols):
                value = self.grid[r][c]
                image = images.get(value, images["empty"])
                screen.blit(image, (r * cell_size, c * cell_size))
