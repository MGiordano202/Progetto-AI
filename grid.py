import random
import time

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [["0" for _ in range(cols)] for _ in range(rows)]

    @property
    def size(self):
        return self.rows * self.cols

    def set_cell(self, row, col, value):
        self.grid[row][col] = value

    def get_cell(self, row, col):
        return self.grid[row][col]

    def get_goal(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "G":
                    return r, c
        return None

    def is_passable(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            print(f"Posizione non valida: ({row}, {col})")
            return False
        cell = self.grid[row][col]
        result = cell in ["0", "P", "G", "D"]
        return result

    def set_wall(self, row, col):
        self.grid[row][col] = "W"

    def is_wall(self, row, col):
        return self.grid[row][col] == "W"

    def is_free(self, row, col):
        return self.grid[row][col] == "0"

    def get_child(self, row, col):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                cell = self.get_cell(new_row, new_col)
                if cell in ["0", "G", "D", "P"]:
                    neighbors.append((new_row, new_col))
        return neighbors

    def get_cost(self, row, col):
        if self.grid[row][col] == "0":
            return 1
        elif self.grid[row][col] == "D":
            return 5
        elif self.grid[row][col] == "G":
            return 1
        return float("inf")

    def generate_bomberman_map(self):
        self.grid = [["W" for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if r % 2 == 0 and c % 2 == 0:
                    self.grid[r][c] = "W"
                else:
                    self.grid[r][c] = "0"

        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if self.grid[r][c] == "0" and random.random() < 0.5:
                    self.grid[r][c] = "D"

        self.clear_initial_areas()

    def clear_initial_areas(self):
        initial_positions = [(1, 1), (1, 2), (2, 1)]
        for r, c in initial_positions:
            self.grid[r][c] = "0"

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

    # --- Nuove funzioni per gestire le esplosioni e lo stato intermedio "E" ---

    def get_explosion_zone(self, bomb_row, bomb_col, radius=2):
        """
        Calcola e restituisce la lista di coordinate interessate dall'esplosione di una bomba.
        L'esplosione si propaga nelle 4 direzioni e si ferma se incontra un muro indistruttibile ("W")
        o il goal ("G"). Se incontra una cassa distruttibile ("D"), la include e si ferma.
        """
        explosion_zone = []
        # Verifica che la posizione della bomba sia valida
        if bomb_row < 0 or bomb_row >= self.rows or bomb_col < 0 or bomb_col >= self.cols:
            print(f"Posizione bomba non valida: ({bomb_row}, {bomb_col})")
            return explosion_zone

        explosion_zone.append((bomb_row, bomb_col))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, radius + 1):
                r = bomb_row + dr * i
                c = bomb_col + dc * i
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                    break
                cell = self.get_cell(r, c)
                if cell in ["W", "G"]:
                    break
                explosion_zone.append((r, c))

        return explosion_zone

    def apply_explosion_state(self, bomb_row, bomb_col, radius=2, explosion_duration=0.5):
        """
        Applica lo stato intermedio "E" alle celle interessate dall'esplosione della bomba.
        Le celle che non sono indistruttibili ("W" o "G") vengono segnate come in esplosione ("E")
        per un periodo definito (explosion_duration) e poi resettate a "0".
        NOTA: questa implementazione è bloccante (usa time.sleep) e in un ambiente di gioco reale
        andrebbe integrata in un game loop non bloccante.
        """
        zone = self.get_explosion_zone(bomb_row, bomb_col, radius)
        # Applica lo stato "E" alle celle interessate
        for r, c in zone:
            current = self.get_cell(r, c)
            if current not in ["W", "G"]:
                self.set_cell(r, c, "E")
        # Simula la durata dell'esplosione (modalità bloccante)
        time.sleep(explosion_duration)
        # Resetta le celle dallo stato "E" a "0" (in caso di casse distruttibili, vengono eliminate)
        for r, c in zone:
            if self.get_cell(r, c) == "E":
                self.set_cell(r, c, "0")

    def get_danger_map(self, bombs, radius=2):
        """
        Restituisce una mappa di pericolo (lista di liste con le stesse dimensioni della griglia)
        in cui ogni cella assume un valore:
          0 -> sicuro
          1 -> pericoloso (appartiene all'area di esplosione di una o più bombe)
        Parametro bombs: lista di oggetti Bomb o tuple (row, col).
        """
        danger_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for bomb in bombs:
            # Supporta sia oggetti Bomb che tuple (row, col)
            if hasattr(bomb, 'row') and hasattr(bomb, 'col'):
                bomb_row, bomb_col = bomb.row, bomb.col
            else:
                bomb_row, bomb_col = bomb
            zone = self.get_explosion_zone(bomb_row, bomb_col, radius)
            for r, c in zone:
                danger_map[r][c] = 1
        return danger_map
