class Player:
    def __init__(self, row = 1, col = 1):
        self.row = row
        self.col = col

    def move_towards_goal(self, grid, pathfinder, goal):
        # Trova il percorso dalla posizione attuale (row, col) al goal
        path = pathfinder.find_path((self.row, self.col), goal)

        # Se il percorso è valido (non vuoto) e contiene più di una cella (il primo passo è la posizione corrente)
        if path and len(path) > 1:
            next_step = path[1]  # Prendi il secondo passo, il primo è la posizione attuale
            next_row, next_col = next_step  # Estrai la nuova riga e colonna

            grid.set_cell(self.row, self.col, "0")  # Ripristina la cella precedente
            if (next_row, next_col) == goal:
                self.row, self.col = goal
                print(f"Player reached the goal at: {goal}")
            else:
                self.row, self.col = next_row, next_col
                print(f"Player moved to: ({self.row}, {self.col})")
            grid.set_cell(self.row, self.col, "P")  # Setta la cella del giocatore



        else:
            print("No valid path to goal!")

    def place_bomb(self, grid):
        grid.set_cell(self.row, self.col, "B")
