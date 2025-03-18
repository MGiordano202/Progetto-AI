import random

from AI.Genetic_Algorithm.Operators.Crossover.best_segment_crossover import best_segment_crossover
from AI.Genetic_Algorithm.Operators.Mutation.segment_mutation import segment_mutation
from AI.Genetic_Algorithm.Operators.Selection.tournament_selection import tournament_selection
from AI.Genetic_Algorithm.individual import Individual
from AI.Genetic_Algorithm.population.dfs import generate_all_paths

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

    if not paths:  # Nessun percorso trovato
        raise ValueError("Nessun percorso valido trovato tra start e goal")

    population = []
    for _ in range(population_size):
        path = random.choice(paths)

        # Controlla che tutte le posizioni siano tuple valide
        if not all(isinstance(pos, tuple) and len(pos) == 2 for pos in path):
            raise ValueError(f"Percorso non valido: {path}")

        individual = Individual(genome=path)
        population.append(individual)

    return population


def next_generation(population, mutation_rate, tournament_size, crossover_rate, grid, goal, start):
    """
    Crea la prossima generazione di individui.
    :param population: Lista di individui (oggetti Individual)
    :param mutation_rate: Probabilità di mutazione per ogni gene.
    :param tournament_size: Numero di individui scelti per il torneo di selezione.
    :param grid: Griglia di gioco.
    :param goal: Posizione dell'obiettivo (tuple).
    :param start: Posizione iniziale (tuple).
    :return: Nuova popolazione.
    """
    new_population = []

    # Elitismo: Manteniamo una percentuale dei migliori individui
    elite_count = int(0.2 * len(population)) #20% di elitismo
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)

    elites = []
    seen_fitness = set()

    for ind in sorted_population:
        if ind.fitness not in seen_fitness:  # Controlla se la fitness è già stata selezionata
            elites.append(ind)
            seen_fitness.add(ind.fitness)
        if len(elites) >= elite_count:
            break

    new_population.extend(elites)

    # Genera il resto della popolazione
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)

        # Assicurati che i genitori siano diversi
        while parent1 == parent2:
            parent2 = tournament_selection(population, tournament_size)

        if random.random() < crossover_rate:
            child1, child2 = best_segment_crossover(parent1, parent2, goal, start, grid)
            print(f"[DEBUG] Crossover genitori: {parent1.genome} x {parent2.genome} -> Figli: {child1.genome}, {child2.genome}")
        else:
            child1, child2 = Individual(parent1.genome[:]), Individual(parent2.genome[:])
            print(f"[DEBUG] Nessun crossover: Figli identici ai genitori")

        # Mutazione dei figli
        mutated_child1 = segment_mutation(child1, mutation_rate, grid)
        mutated_child2 = segment_mutation(child2, mutation_rate, grid)

        # Aggiungi i figli mutati alla nuova popolazione
        new_population.append(mutated_child1)
        new_population.append(mutated_child2)

    # Limita la popolazione alla dimensione originale
    new_population = new_population[:len(population)]

    return new_population
