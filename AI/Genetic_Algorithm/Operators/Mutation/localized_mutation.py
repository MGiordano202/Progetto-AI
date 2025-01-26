import random
from AI.Genetic_Algorithm.individual import Individual

def localized_mutation(individual, mutation_rate, grid):
    """
    Esegue una mutazione locale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :param grid: Griglia di gioco per verificare posizioni valide.
    :return: Individuo mutato.
    """
    if not individual:
        raise ValueError("L'individuo passato a mutation è None.")

    mutated_genome = individual.genome[:]

    for i in range(len(mutated_genome)):
        if random.random() < mutation_rate:
            current_coord = mutated_genome[i]

            # Genera una nuova posizione vicina (up, down, left, right)
            possible_moves = [
                (current_coord[0] - 1, current_coord[1]),  # Su
                (current_coord[0] + 1, current_coord[1]),  # Giù
                (current_coord[0], current_coord[1] - 1),  # Sinistra
                (current_coord[0], current_coord[1] + 1),  # Destra
            ]

            # Filtra le mosse valide (che sono all'interno della griglia e attraversabili)
            valid_moves = [
                move for move in possible_moves
                if 0 <= move[0] < grid.rows and 0 <= move[1] < grid.cols and grid.is_passable(move[0], move[1])
            ]

            # Se ci sono mosse valide, scegli una a caso
            if valid_moves and i != 0 and i != len(mutated_genome) - 1:
                mutated_genome[i] = random.choice(valid_moves)

    return Individual(genome=mutated_genome)
