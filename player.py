from bomb import Bomb


class Player:
    def __init__(self, row = 1, col = 1):
        self.row = row
        self.col = col
        self.waiting_for_bomb = False

    def move_towards_goal(self, grid, pathfinder, goal):
        if self.waiting_for_bomb:
            print("Player is waiting for bomb to explode!")
            return

        # Trova il percorso dalla posizione attuale (row, col) al goal
        path = pathfinder.find_path((self.row, self.col), goal)

        # Se il percorso è valido (non vuoto) e contiene più di una cella
        if path and len(path) > 1:
            next_step = path[1]  # Prendi il secondo passo, il primo è la posizione attuale
            next_row, next_col = next_step
            cell_type = grid.get_cell(next_row, next_col)

            if cell_type == "D":
                print(f"Ostacolo trovato in pos {next_step}. Piazzo una bomba!")
                self.place_bomb(grid)
                self.waiting_for_bomb = True
                return

            grid.set_cell(self.row, self.col, "0") # Ripristina la cella precedente
            self.row, self.col = next_row, next_col
            """
            if (next_row, next_col) == goal:
                self.row, self.col = goal
                print(f"Player reached the goal at: {goal}")
            else:
                self.row, self.col = next_row, next_col
                print(f"Player moved to: ({self.row}, {self.col})")
            """
            grid.set_cell(self.row, self.col, "P")  # Setta la cella del giocatore
        else:
            print("No valid path to goal!")

    def place_bomb(self, grid):
        print(f"Bomba piazzata in posizione: ({self.row}, {self.col})")
        bomb = Bomb(self.row, self.col)
        grid.set_cell(self.row, self.col, "B")
        return bomb

    def check_bomb_status(self, grid):
        """Controlla se la bomba è esplosa e, se sì consente al giocatore di riprendere il movimento"""
        if self.waiting_for_bomb:
            current_cell = grid.get_cell(self.row, self.col)
            if current_cell != "B":
                print("Bomba esplosa! Player può muoversi di nuovo.")
                self.waiting_for_bomb = False
