import random

from AI.Genetic_Algorithm.Operators.Crossover.best_segment_crossover import is_valid_genome, repair_genome
from AI.Genetic_Algorithm.individual import Individual
from AI.a_star import Astar


def segment_mutation(individual, mutation_rate, grid):
    """
    Esegue una mutazione a segmento su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :param grid: Griglia di gioco per verificare posizioni valide.
    :return: Individuo mutato.
    """
    if not individual:
        raise ValueError("Individuo non valido")

    genome = individual.genome[:]
    genome_length = len(genome)
    goal = genome[-1]

    if random.random() >= mutation_rate:
        return Individual(genome= genome)

    # percorso troppo corto per la mutazione
    if genome_length < 4:
        return Individual(genome= genome)

    start_index = random.randint(1, genome_length -3)
    end_index = random.randint(start_index + 1, genome_length - 2)

    anchor_start = genome[start_index - 1]
    anchor_end = genome[end_index]

    astar = Astar(grid)
    new_segment, _ = astar.find_path(anchor_start, anchor_end)

    if new_segment is None or len(new_segment) < 2:
        return Individual(genome= genome)

    if new_segment[0] == anchor_start:
        new_segment = new_segment[1:]

    if new_segment[-1] != anchor_end:
        new_segment.append(anchor_end)

    new_genome = genome[:start_index] + new_segment + genome[end_index:]

    if not is_valid_genome(new_genome, genome[0]):
        new_genome = repair_genome(new_genome, genome[-1], grid)

    if new_genome[-1] != goal:
        segment_to_goal, _ = astar.find_path(new_genome[-1], goal)
        if segment_to_goal is not None and len(segment_to_goal) > 1:
            # Evito di duplicare l'ultimo gene
            if segment_to_goal[0] == new_genome[-1]:
                segment_to_goal = segment_to_goal[1:]
            new_genome.extend(segment_to_goal)

    return Individual(genome= new_genome)