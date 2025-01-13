class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move_towards_goal(self, grid, pathfinder, goal):
        path = pathfinder.find_path((self.row, self.col), goal)  # Trova il percorso
        if path:
            new_row, new_col = path[0]

            # Controlla se la nuova posizione è valida
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.is_passable(new_row, new_col):
                # Libera la cella precedente
                grid.set_cell(self.row, self.col, 0)
                # Aggiorna la posizione del giocatore
                self.row, self.col = new_row, new_col
                # Imposta la nuova posizione sulla griglia
                grid.set_cell(self.row, self.col, "P")

    def place_bomb(self, grid):
        grid.set_cell(self.row, self.col, "B")
