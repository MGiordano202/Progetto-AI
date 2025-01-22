import random
from AI.Genetic_Algorithm.individual import Individual

def generate_initial_population(size, genome_length, gird_size):
    """
    Genera una popolazione iniziale.
    :param size: Dimensione della popolazione
    :param genome_length: Lunghezza del genoma (numero di mosse)
    :param gird_size: Dimensione della griglia
    :return: Lista di individui
    """
    directions = ['u', 'd', 'l', 'r', 'b']
    population = [
        Individual(
            genome=''.join(random.choice(directions) for _ in range(genome_length)),
            grid_size=gird_size
        )
        for _ in range(size)
    ]
    return population