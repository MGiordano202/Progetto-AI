import random

class Enemy:
    def __init__(self, row, col, pathfinder,move_delay = 30):
        self.row = row
        self.col = col
        self.pathfinder = pathfinder
        self.move_delay = move_delay # Tempo di ritardo in frame
        self.move_counter = 0 # Contatore per il ritardo

    def update(self, grid):
        # Aggiorna il contatore per il ritardo
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move(grid)
            self.move_counter = 0


    def move(self, grid):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)
        moved = False
        for dr, dc in moves:
            new_row = self.row + dr
            new_col = self.col + dc
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.is_passable(new_row, new_col):
                grid.set_cell(self.row, self.col, 0) # Ripristina il blocco precedente
                self.row = new_row # Aggiorna la nuova posizione
                self.col = new_col
                grid.set_cell(self.row, self.col, "E") # Imposta il nuovo blocco come occupato dal nemico
                moved = True
                break
        if not moved:
            print(f"Enemy at {self.row}, {self.col} couldn't move.")