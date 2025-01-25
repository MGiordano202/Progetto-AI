import random

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [["0" for _ in range(cols)] for _ in range(rows)]

    @property
    def size(self):
        return self.rows * self.cols

    def set_cell(self, rows, cols, value):
        self.grid[rows][cols] = value

    def get_cell(self, rows, cols):
        return self.grid[rows][cols]

    def get_goal(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "G":
                    return r, c
        return None

    def is_passable(self, rows, cols):
        if rows < 0 or rows >= self.rows or cols < 0 or cols >= self.cols:
            print(f"Posizione non valida: ({rows}, {cols})")
            return False
        cell = self.grid[rows][cols]
        result = cell in ["0", "P", "G", "D"]

        return result

    def set_wall(self, rows, cols):
        self.grid[rows][cols] = "W"

    def is_wall(self, rows, cols):
        return self.grid[rows][cols] == "W"

    def is_free(self, rows, cols):
        return self.grid[rows][cols] == "0"

    def get_neighbors(self, rows, cols):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #movivimenti sulla griglia
            new_row, new_col = rows + dr, cols + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                cell = self.get_cell(new_row, new_col)
                if cell in ["0", "G", "D", "P"]:
                    neighbors.append((new_row, new_col))
        print(f"Vicini di ({rows}, {cols}): {neighbors}")
        return neighbors

    def get_cost(self, rows, cols):
        if self.grid[rows][cols] == "0": #cella libera
            return 1
        elif self.grid[rows][cols] == "D": #cella distruttibile
            return 5
        elif self.grid[rows][cols] == "G":  # Goal
            return 1
        return float("inf")

    def add_walls(self):
        wall_positions = [(2, 0)]  # Example positions
        for row, col in wall_positions:
            self.set_wall(row, col)

    def generate_bomberman_map(self):
        """Genera una mappa in stile Bomberman con blocchi distruttibili e indistruttibili."""
        self.grid = [["W" for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                # Blocchi indistruttibili ogni 2 celle (griglia fissa)
                if r % 2 == 0 and c % 2 == 0:
                    self.grid[r][c] = "W"
                else:
                    self.grid[r][c] = "0"

        # Aggiunge blocchi distruttibili casualmente
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if self.grid[r][c] == "0" and random.random() < 0.5:  # 5% di probabilità di blocco distruttibile
                    self.grid[r][c] = "D"

        self.clear_initial_areas()



    def clear_initial_areas(self):
        """Libera le aree iniziali per il giocatore e i nemici."""
        initial_positions = [(1, 1), (1, 2), (2, 1)]
        for r, c in initial_positions:
            self.grid[r][c] = "0"

    """def generate_maze(self):
        #Genera un labirinto utilizzando l'algoritmo di Prim.
        def is_valid_cell(row, col):
            return 0 < row < self.rows - 1 and 0 < col < self.cols - 1

        # Inizializza con celle libere
        self.grid = [["W" for _ in range(self.cols)] for _ in range(self.rows)]

        # Scegli un punto iniziale
        start_row, start_col = 1, 1
        self.grid[start_row][start_col] = 0  # Cella libera
        walls = [(start_row + dr, start_col + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

        while walls:
            # Seleziona una parete casuale
            wall = random.choice(walls)
            walls.remove(wall)

            r, c = wall
            if not is_valid_cell(r, c) or self.grid[r][c] != "W":
                continue

            # Conta le celle libere adiacenti
            adjacent_free = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if is_valid_cell(nr, nc) and self.grid[nr][nc] == 0:
                    adjacent_free += 1

            # Se c'è una sola cella libera adiacente, rendi questa cella libera
            if adjacent_free == 1:
                self.grid[r][c] = 0
                # Aggiungi le pareti adiacenti a questa alla lista
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if is_valid_cell(nr, nc):
                        walls.append((nr, nc))

        # Assicurati che il giocatore e il nemico abbiano spazio
        self.grid[1][1] = 0
        self.grid[self.rows - 2][self.cols - 2] = 0"""

    def print_grid(self, screen, images, cell_size):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                image = images.get(value, images["0"])
                screen.blit(image, (c * cell_size, r * cell_size))

    def print_debug(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
        print("\n")


