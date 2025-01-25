import time


class Bomb:
    def __init__(self, row, col, timer=2):
        self.row = row
        self.col = col
        self.timer = timer
        self.start_time = time.time()
        self.waiting_for_bomb = False # Per controllare se il giocatore sta aspettando l'esplosione
        self.exploded = False # Per tracciare lo stato della bomba
        self.radius = 2  # Raggio dell'esplosione

    def has_exploded(self):
        """Verifica se la bomba è esplosa in base al timer."""
        return time.time() - self.start_time >= self.timer

    def explode(self, grid):
        """Gestisce l'esplosione della bomba."""
        if self.exploded:  # Evita esplosioni multiple
            return

        print(f"Bomba esplode in posizione ({self.row}, {self.col})!")

        grid.set_cell(self.row, self.col, "0")  # Rimuove la bomba dalla cella

        # Gestione delle celle coinvolte nell'esplosione
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Direzioni: sopra, sotto, sinistra, destra
            for i in range(1, self.radius + 1):
                r, c = self.row + dr * i, self.col + dc * i
                if 0 <= r < grid.rows and 0 <= c < grid.cols:
                    cell = grid.get_cell(r, c)
                    if cell == "W" or cell == "G":  # Blocchi indistruttibili
                        break
                    elif cell == "D":  # Blocchi distruttibili
                        print(f"Distrutto blocco distruttibile in ({r}, {c})")
                        grid.set_cell(r, c, "0")
                    elif cell == "P":  # Se il giocatore è nella zona di esplosione
                        grid.set_cell(r, c, "P")
                    else:  # Celle vuote o altre
                        grid.set_cell(r, c, "0")
        self.exploded = True

    def update(self, grid):
        """Aggiorna lo stato della bomba, facendo esplodere quando necessario."""
        if self.has_exploded() and not self.exploded:
            self.explode(grid)
            return True
        return False

    def simulate_bomb_explosion(self, grid):
        """
        Simula le celle coinvolte nell'esplosione, senza modificare a griglia.
        :param grid: Griglia di gioco.
        :return: Lista di celle coinvolte nell'esplosione.
        """
        affected_cell = []

     # Direzioni dell'esplosione: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, self.radius + 1):
                r, c = self.row + dr * i, self.col + dc * i

                if 0 <= r < grid.rows and 0 <= c < grid.cols:
                    cell_type = grid.get_cell(r, c)
                    affected_cell.append((r, c))

                    if cell_type in ["W", "G", "P"]:
                        break

        return affected_cell


