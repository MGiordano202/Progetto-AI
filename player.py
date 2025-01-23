from bomb import Bomb


class Player:
    def __init__(self, row=1, col=1):
        self.row = row
        self.col = col
        self.waiting_for_bomb = False

    def move_towards_goal(self, grid, pathfinder, goal, bomb_list):
        if self.waiting_for_bomb:
            self.check_bomb_status(grid)
            print("Player is waiting for bomb to explode!")
            return

        # Trova il percorso dalla posizione attuale (row, col) al goal
        path, blocks_to_destroy = pathfinder.find_path((self.row, self.col), goal)

        # Filtra i blocchi distruttibili essenziali
        essential_blocks = self.filer_essential_blocks(blocks_to_destroy, path)

        if essential_blocks:
            target_block = essential_blocks[0]
            adjacent_positions = self.get_adjacent_positions(target_block[0], target_block[1], grid)

            # Controlla se il giocatore è già in una posizione adiacente
            if (self.row, self.col) in adjacent_positions:
                print(f"Player piazza la bomba in posizione: ({self.row}, {self.col})")
                self.place_bomb(grid, bomb_list)
                return

            # Cerca un percorso verso una posizione adiacente al blocco
            for adj_pos in adjacent_positions:
                print(f"Checking path to adjacent position: {adj_pos}")
                path_to_adj, _ = pathfinder.find_path((self.row, self.col), adj_pos)
                print(f"Path to adjacent position {adj_pos}: {path_to_adj}")

                if path_to_adj and len(path_to_adj) > 1:
                    next_step = path_to_adj[1]
                    print(f"Moving to next step towards adjacent position: {next_step}")
                    self.move_to(next_step, grid)
                    return

            print(f"Cannot reach any adjacent position to target block: {target_block}")
            return

        # Se il percorso è valido (non vuoto) e contiene più di una cella
        if path and len(path) > 1:
            next_step = path[1]  # Prendi il secondo passo, il primo è la posizione attuale
            self.move_to(next_step, grid)

        else:
            print("No valid path to goal!")

    @staticmethod
    def filer_essential_blocks(blocks_to_destroy, path):
        essential_blocks = []
        for block in blocks_to_destroy:
            if block in path:
                essential_blocks.append(block)
        return essential_blocks

    @staticmethod
    def get_adjacent_positions(rows, cols, grid):
        adjacent_positions = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            adj_row, adj_col = rows + dr, cols + dc
            if grid.is_passable(adj_row, adj_col):
                adjacent_positions.append((adj_row, adj_col))
        return adjacent_positions

    def place_bomb(self, grid, bomb_list):
        if grid.get_cell(self.row, self.col) == "P":  # Ensure the cell is empty before placing
            print(f"Bomba piazzata in posizione: ({self.row}, {self.col})")
            bomb = Bomb(self.row, self.col)
            grid.set_cell(self.row, self.col, "B")
            bomb_list.append(bomb)
            self.waiting_for_bomb = True
            return bomb
        else:
            print(f"Cannot place bomb at ({self.row}, {self.col}) - Cell is not empty.")
            return None

    def check_bomb_status(self, grid):
        """Check if the bomb has exploded and allow the player to move again."""
        if self.waiting_for_bomb:
            current_cell = grid.get_cell(self.row, self.col)
            if current_cell != "B":
                print("Bomba esplosa! Player può muoversi di nuovo.")
                self.waiting_for_bomb = False

    def move_to(self, next_step, grid):
        if not isinstance(next_step, tuple) or len(next_step) != 2:
            print(f"Invalid next step: {next_step}")
            return

        next_row, next_col = next_step
        if grid.is_passable(next_row, next_col):
            grid.set_cell(self.row, self.col, "0")  # Clear the previous cell
            grid.set_cell(next_row, next_col, "P")  # Set the player in the new position
            self.row, self.col = next_row, next_col  # Update player's position
            print(f"Player moved to ({next_row}, {next_col})")
        else:
            print(f"Cannot move to ({next_row}, {next_col}) - Cell is not passable.")
