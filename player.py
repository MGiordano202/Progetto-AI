from bomb import Bomb

class Player:
    def __init__(self, row=1, col=1):
        self.row = row
        self.col = col
        self.waiting_for_bomb = False

    def move_towards_goal(self, grid, pathfinder, goal, bomb_list):
        """
        Muove il giocatore verso l'obiettivo (goal) utilizzando il pathfinder.
        Se nel percorso vengono identificati blocchi distruttibili essenziali,
        il giocatore cerca di posizionarsi in una cella adiacente per piazzare la bomba.
        Se il giocatore sta già aspettando l'esplosione della bomba, verifica lo stato.
        """
        if self.waiting_for_bomb:
            self.check_bomb_status(grid)
            print("Il giocatore sta aspettando che la bomba esploda.")
            return

        # Trova il percorso dalla posizione attuale al goal utilizzando un algotitmo di pathfinding
        path, blocks_to_destroy = pathfinder.find_path((self.row, self.col), goal)

        # Filtra i blocchi distruttibili essenziali (quelli che compaiono nel percorso)
        essential_blocks = self.filter_essential_blocks(blocks_to_destroy, path)

        if essential_blocks:
            target_block = essential_blocks[0]
            adjacent_positions = self.get_adjacent_positions(target_block[0], target_block[1], grid)

            # Se il giocatore è già in una posizione adiacente, piazza la bomba.
            if (self.row, self.col) in adjacent_positions:
                print(f"Player piazza la bomba in posizione: ({self.row}, {self.col})")
                self.place_bomb(grid, bomb_list)
                return

            # Cerca un percorso verso una posizione adiacente al blocco distruttibile
            for adj_pos in adjacent_positions:
                print(f"Checking path to adjacent position: {adj_pos}")
                path_to_adj, _ = pathfinder.find_path((self.row, self.col), adj_pos)
                print(f"Path to adjacent position {adj_pos}: {path_to_adj}")
                if path_to_adj and len(path_to_adj) > 1:
                    next_step = path_to_adj[1]
                    print(f"Prossimo passo verso la posizione adiacente: {next_step}")
                    self.move_to(next_step, grid)
                    return

            print(f"Cannot reach any adjacent position to target block: {target_block}")
            return

        # Se non ci sono blocchi essenziali e il percorso verso il goal è valido, muovi il giocatore.
        if path and len(path) > 1:
            next_step = path[1]  # Il primo passo è la posizione attuale, quindi si prende il successivo.
            self.move_to(next_step, grid)
        else:
            print("No valid path to goal!")

    @staticmethod
    def filter_essential_blocks(blocks_to_destroy, path):
        """
        Restituisce l'elenco dei blocchi distruttibili essenziali, ovvero quelli che compaiono nel percorso.
        """
        return [block for block in blocks_to_destroy if block in path]

    @staticmethod
    def get_adjacent_positions(row, col, grid):
        """
        Restituisce una lista di posizioni adiacenti (su, giù, sinistra, destra)
        che sono passabili sulla griglia.
        """
        adjacent_positions = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if grid.is_passable(adj_row, adj_col):
                adjacent_positions.append((adj_row, adj_col))
        return adjacent_positions

    def place_bomb(self, grid, bomb_list):
        """
        Tenta di piazzare una bomba nella cella attuale del giocatore.
        La bomba viene piazzata solo se la cella contiene il giocatore ('P') e non è occupata da altro.
        Se la bomba viene piazzata, il giocatore passa allo stato 'waiting_for_bomb'.
        """
        current_cell = grid.get_cell(self.row, self.col)
        if current_cell == "P":
            print(f"Bomba piazzata in posizione: ({self.row}, {self.col})")
            bomb = Bomb(self.row, self.col)
            grid.set_cell(self.row, self.col, "B")
            bomb_list.append(bomb)
            self.waiting_for_bomb = True
            return bomb
        else:
            print(f"Cannot place bomb at ({self.row}, {self.col}) - Cell is not empty (current value: {current_cell}).")
            return None

    def check_bomb_status(self, grid):
        """
        Controlla se la bomba è esplosa, verificando lo stato della cella corrente.
        Se la cella non contiene più una bomba ('B'), il giocatore può muoversi nuovamente.
        """
        if self.waiting_for_bomb:
            current_cell = grid.get_cell(self.row, self.col)
            if current_cell != "B":
                print("Bomba esplosa! Player può muoversi di nuovo.")
                self.waiting_for_bomb = False

    def move_to(self, next_step, grid):
        """
        Muove il giocatore verso la posizione specificata (next_step), se passabile.
        Aggiorna la griglia rimuovendo il giocatore dalla cella precedente e posizionandolo nella nuova cella.
        """
        if not isinstance(next_step, tuple) or len(next_step) != 2:
            print(f"Invalid next step: {next_step}")
            return

        next_row, next_col = next_step
        if grid.is_passable(next_row, next_col):
            # Libera la cella precedente
            grid.set_cell(self.row, self.col, "0")
            # Posiziona il giocatore nella nuova cella
            grid.set_cell(next_row, next_col, "P")
            self.row, self.col = next_row, next_col
            print(f"Player moved to ({next_row}, {next_col})")
        else:
            print(f"Cannot move to ({next_row}, {next_col}) - Cell is not passable.")
