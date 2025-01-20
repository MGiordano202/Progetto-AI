import random

class Individual:
    def __init__(self, path, bombs_placed, fitness = 0):
        """
        Rappresenta un induviduo della popolazione.
        path è una lista di tuple (row, col, place_bomb) che rappresenta un percorso.
        """
        self.path = path
        self.bombs_placed = bombs_placed
        self.fitness = fitness

    def mutate(self, grid, mutation_rate):
        """Effettua la mutazione casuale sul percorso."""

        if random.random() < mutation_rate:
            index = random.randint(0, len(self.path) - 1)
            row, col, place_bomb = self.path[index]

            # Cambia casualmente la posizione o la decisione di piazzare una bomb
            if random.random() < 0.5:
                self.path[index] = (row, col, not place_bomb)
            else:
                new_row, new_col = row + random.choice([-1, 0, 1]), col + random.choice([-1, 0, 1])
                if grid.is_passable(new_row, new_col):
                    self.path[index] = (new_row, new_col, place_bomb)