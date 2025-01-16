from bomb import Bomb


class Player:
    def __init__(self, row = 1, col = 1):
        self.row = row
        self.col = col
        self.waiting_for_bomb = False

    def move_towards_goal(self, grid, pathfinder, goal):
        if self.waiting_for_bomb:
            self.check_bomb_status(grid)
            print("Player is waiting for bomb to explode!")
            return

        # Trova il percorso dalla posizione attuale (row, col) al goal
        path, blocks_to_destroy = pathfinder.find_path((self.row, self.col), goal)

        if blocks_to_destroy:
            target_block = blocks_to_destroy[0]

            if(self.row, self.col) == target_block:
                print(f"Player in posizione blocco distruttibile: {target_block}. Piazzo una bomba!")
                grid.set_cell(self.row, self.col, "B")  # Ripristina la cella precedente
                return

            # Muovi verso il blocco distruttibile
            if path and len(path) > 1:
                next_step = path[1]
                self.move_to(next_step, grid)
            return

        # Se il percorso è valido (non vuoto) e contiene più di una cella
        if path and len(path) > 1:
            next_step = path[1]  # Prendi il secondo passo, il primo è la posizione attuale
            self.move_to(next_step, grid)

        else:
            print("No valid path to goal!")

    def place_bomb(self, grid):
        print(f"Bomba piazzata in posizione: ({self.row}, {self.col})")
        bomb = Bomb(self.row, self.col)
        grid.set_cell(self.row, self.col, "B")
        self.waiting_for_bomb = True
        return bomb

    def check_bomb_status(self, grid):
        """Controlla se la bomba è esplosa e, se sì consente al giocatore di riprendere il movimento"""
        if self.waiting_for_bomb:
            current_cell = grid.get_cell(self.row, self.col)
            if current_cell != "B":
                print("Bomba esplosa! Player può muoversi di nuovo.")
                self.waiting_for_bomb = False

    def move_to(self, next_step, grid):
        if grid.is_passable(*next_step):
            next_row, next_col = next_step
            grid.set_cell(self.row, self.col, "0")
            grid.set_cell(next_row, next_col, "P")
            self.row, self.col = next_row, next_col