import random

from AI.Genetic_Algorithm.Operators.Crossover.best_segment_crossover import best_segment_crossover
from AI.Genetic_Algorithm.Operators.Mutation.localized_mutation import localized_mutation
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


def next_generation(population, mutation_rate, tournament_size, grid, goal, start):
    """
    Crea la prossima generazione di individui.
    :param population: lista di individui (oggetti Individual)
    :param mutation_rate: Probabilità di mutazione per ogni gene.
    :param tournament_size: Numero di individui scelti per il torneo di selezione.
    :param grid: Griglia di gioco.
    :param goal: Posizione dell'obiettivo (tuple).
    :param start: Posizione iniziale (tuple).
    :return: nuova popolazione.
    """
    new_population = []

    # Elitismo: Manteniamo una percentuale dei migliori individui
    elite_count = int(0.1 * len(population))  # Manteniamo almeno il 10% dei migliori
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    elites = sorted_population[:elite_count]
    new_population.extend(elites)

    # Genera il resto della popolazione
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)

        # Assicurati che i genitori siano diversi
        while parent1 == parent2:
            parent2 = tournament_selection(population, tournament_size)

        # Crossover ibrido basato sui segmenti migliori
        child1, child2 = best_segment_crossover(parent1, parent2, goal, start, grid)
        print(f"[DEBUG] Crossover genitori: {parent1.genome} x {parent2.genome} -> Figli: {child1.genome}, {child2.genome}")

        # Mutazione localizzata
        mutated_child1 = localized_mutation(child1, mutation_rate, grid)
        mutated_child2 = localized_mutation(child2, mutation_rate, grid)

        # Aggiungi i figli mutati alla nuova popolazione
        new_population.append(mutated_child1)
        new_population.append(mutated_child2)

    # Limita la popolazione alla dimensione originale
    new_population = new_population[:len(population)]

    return new_population
