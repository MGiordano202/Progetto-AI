import random
from AI.Genetic_Algorithm.individual import Individual
from AI.Genetic_Algorithm.Operators.Selection.tournament_selection import tournament_selection
from AI.Genetic_Algorithm.Operators.Crossover.single_point_crossover import single_point_crossover
from AI.Genetic_Algorithm.Operators.Mutation.random_mutation import random_mutation
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

def next_generation(population, mutation_rate, tournament_size):
    """
    Crea la prossima generazione di individui.
    :param population: lista di individui
    :param mutation_rate: Probabilità di mutazione per ogni gene.
    :param tournament_size: Numero di individui scelti per il torneo di selezione
    :return: nuova popolazione
    """
    new_population = []

    # Elitismo
    elite_count = max(1, len(population) // 10)
    sorted_popuation = sorted(population, key=lambda x: x.fitness, reverse=True)
    elites = sorted_popuation[:elite_count]

    new_population.extend(elites)

    # Genera il resto della popolazione
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)

        child_genome = single_point_crossover(parent1, parent2)

        mutated_genome = random_mutation(child_genome, mutation_rate)

        new_individual = Individual(mutated_genome, parent1.grid_size)
        new_population.append(new_individual)

    return new_population
