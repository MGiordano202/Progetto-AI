import random
from Operators.Selection.tournament_selection import tournament_selection
from Operators.Crossover.single_point_crossover import single_point_crossover
from Operators.Mutation.random_mutation import random_mutation
from individual import Individual
def generate_initial_population(size, grid_size):
    """
    Genera una popolazione iniziale di individui in maniera casuale.
    :param size: Dimensione della popolazione
    :param grid_size: Dimensione della griglia
    :return: Lista di individui
    """
    population = []
    for _ in range(size):
        path = [(random.randint(0, grid_size -1), random.randint(0, grid_size -1)) for _ in range(10)]
        bombs_placed = [(random.randint(0, grid_size -1), random.randint(0, grid_size -1)) for _ in range(3)]
        individual = Individual(path, bombs_placed)
        population.append(individual)
    return population

def next_generation(population, goal_position, tournament_size, mutation_rate):
    """
    Genera la prossima generazione di individui.
    :param population: Lista di individui.
    :param goal_position: Posizione dell'obiettivo.
    :param tournament_size: Dimensione del torneo.
    :param mutation_rate: Probabilità di mutazione
    :return: Nuova generazione
    """
    # Calcola il fitness di ogni individuo
    for individual in population:
        individual.calculate_fitness(goal_position)

    # Selezione la nuova generazione
    new_generation = []
    for _ in range(len(population)):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)
        child_data = single_point_crossover(parent1, parent2)
        child = Individual(child_data["path"], child_data["bombs_placed"])
        child = random_mutation(child, mutation_rate)
        new_generation.append(child)
    return new_generation