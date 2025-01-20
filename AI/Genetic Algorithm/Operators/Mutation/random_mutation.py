import random


def random_mutation(individual, mutation_rate, grid):
    """
    Esegue la mutazione casuale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :param grid: Griglia del gioco, usata per verificare la validità delle mutazioni.
    :return: Individuo mutato.
    """
    if random.random() < mutation_rate:
        mutation_index = random.randint(0, len(individual.path) - 1)

        # Genera una nuova mossa casuale
        new_row = random.randint(0, grid.rows - 1)
        new_col = random.randint(0, grid.cols - 1)
        place_bomb = random.choice([True, False])

        # Controlla che la posizione sia valida
        if grid.is_passable(new_row, new_col):
            individual.path[mutation_index] = (new_row, new_col, place_bomb)

    return individual
