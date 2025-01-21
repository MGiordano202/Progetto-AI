import time


class Bomb:
    def __init__(self, row, col, timer=0.5):
        self.row = row
        self.col = col
        self.timer = timer
        self.start_time = time.time()
        self.exploded = False  # Per tracciare lo stato della bomba

    def has_exploded(self):
        """Verifica se la bomba è esplosa in base al timer."""
        return time.time() - self.start_time >= self.timer

    def explode(self, grid):
        """Gestisce l'esplosione della bomba."""
        if self.exploded:  # Evita esplosioni multiple
            return

        print(f"Bomba esplode in posizione ({self.row}, {self.col})!")
        radius = 2
        grid.set_cell(self.row, self.col, "0")  # Rimuove la bomba dalla cella

        # Gestione delle celle coinvolte nell'esplosione
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Direzioni: sopra, sotto, sinistra, destra
            for i in range(1, radius + 1):
                r, c = self.row + dr * i, self.col + dc * i
                if 0 <= r < grid.rows and 0 <= c < grid.cols:
                    cell = grid.get_cell(r, c)
                    if cell == "W" or cell == "G":  # Blocchi indistruttibili
                        break
                    elif cell == "D":  # Blocchi distruttibili
                        print(f"Distrutto blocco distruttibile in ({r}, {c})")
                        grid.set_cell(r, c, "0")
                    elif cell == "P":  # Se il giocatore è nella zona di esplosione
                        print(f"Giocatore colpito in posizione ({r}, {c})!")
                        grid.set_cell(r, c, "0")
                    else:  # Celle vuote o altre
                        grid.set_cell(r, c, "0")
        self.exploded = True

    def update(self, grid):
        """Aggiorna lo stato della bomba, facendo esplodere quando necessario."""
        if self.has_exploded() and not self.exploded:
            self.explode(grid)
            return True
        return False
