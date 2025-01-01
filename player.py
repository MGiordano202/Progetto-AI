class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, direction, grid):
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        if direction in moves:
            dr, dc = moves[direction]
            new_row, new_col = self.row + dr, self.col + dc

            # Controlla se la nuova posizione è valida
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.isFree(new_row, new_col):
                # Libera la cella precedente
                grid.setCell(self.row, self.col, "empty")
                # Aggiorna la posizione del giocatore
                self.row, self.col = new_row, new_col
                # Imposta la nuova posizione sulla griglia
                grid.setCell(self.row, self.col, "player")

    def place_bomb(self, grid):
        grid.setCell(self.row, self.col, "bomb")
