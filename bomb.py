import pygame
import time

class Bomb:
    def __init__(self, row, col, timer=3):
        self.row = row
        self.col = col
        self.timer = timer
        self.start_time = time.time()

    def has_exploded(self):
        return time.time() - self.start_time >= self.timer

    def explode(self, grid):
        radius = 2
        grid.set_cell(self.row, self.col, "0")

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for i in range(1, radius + 1): #prima -1, radius + 1
                r, c = self.row + dr * i, self.col + dc * i
                if 0 <= r < grid.rows and 0 <= c < grid.cols:
                    if grid.get_cell(r, c) == "W" or grid.get_cell(r, c) == "G":  # Blocchi indistruttibili
                        break  # Ferma l'esplosione
                    elif grid.get_cell(r, c) == "D":
                        grid.set_cell(r, c, "e")
                        continue
                    else:  # Celle vuote o altre
                        grid.set_cell(r, c, "e")

    def update(self):
        if self.has_exploded():
            self.timer = 0