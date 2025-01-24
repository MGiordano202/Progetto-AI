import random
from AI.Genetic_Algorithm.individual import Individual
from AI.Genetic_Algorithm.population.dfs import generate_all_paths
from AI.Genetic_Algorithm.Operators.Selection.tournament_selection import tournament_selection
from AI.Genetic_Algorithm.Operators.Crossover.single_point_crossover import single_point_crossover
from AI.Genetic_Algorithm.Operators.Mutation.random_mutation import random_mutation
def generate_initial_population(grid, start, goal, population_size):
    """
    Genera la popolazione iniziale di individui utilizzando l'algoritmo
    Depth-First Search (DFS) per generare i genomi.
    :param grid: Griglia di gioco
    :param start: posizione iniziale (riga, colonna)
    :param goal: posizione obiettivo (riga, colonna)
    :param population_size: Numero di individui nella popolazione
    :return: Lista di oggetti Individual
    """
    paths = generate_all_paths(grid, start, goal)

    if not paths: # Nessun percorso trovato
        raise ValueError("Nessun percorso valido trovato tra start e goal")

    population = []
    for _ in range(population_size):
        path = random.choice(paths)
        individual = Individual(genome = path)
        population.append(individual)

    return population

def next_generation(population, mutation_rate, tournament_size):
    """
    Crea la prossima generazione di individui.
    :param population: lista di individui (oggetti Individual)
    :param mutation_rate: Probabilità di mutazione per ogni gene.
    :param tournament_size: Numero di individui scelti per il torneo di selezione
    :return: nuova popolazione
    """
    new_population = []

    # Elitismo
    elite_count = max(1, len(population) // 10) # 10% della popolazione
    sorted_popuation = sorted(population, key=lambda x: x.fitness, reverse=True)
    elites = sorted_popuation[:elite_count]

    new_population.extend(elites)

    # Genera il resto della popolazione
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)
        print(f"Selezione: Tipo={type(parent1)}, Genome={parent1.genome}")
        print(f"Selezione: Tipo={type(parent2)}, Genome={parent2.genome}")

        # Assicurati che i genitori siano diversi
        while parent1 == parent2:
            parent2 = tournament_selection(population, tournament_size)

        child1, child2 = single_point_crossover(parent1, parent2)
        print(f"Crossover: Nuovo individuo={child1}, Genome={child1.genome}")
        print(f"Crossover: Nuovo individuo={child2}, Genome={child2.genome}")
        mutated_child1 = random_mutation(child1, mutation_rate)
        mutated_child2 = random_mutation(child2, mutation_rate)
        print(f"Mutazione: Genome dopo mutazione={mutated_child1.genome}")
        print(f"Mutazione: Genome dopo mutazione={mutated_child2.genome}")
        new_population.append(mutated_child1)
        new_population.append(mutated_child2)

    # Rimuovi eventuali individui in eccesso
    new_population = new_population[:len(population)]

    return new_population
