import random
from AI.Genetic_Algorithm.individual import Individual
def single_point_crossover(parent1, parent2):
    """
    Esegue il crossover a singono punto sui due genitori.
    :param parent1: primo genitore
    :param parent2: secondo genitore
    :return: due nuovi figli (oggetti Individual)
    """
    # Debug: Verifica i genitori
    if not isinstance(parent1, Individual) or not isinstance(parent2, Individual):
        raise TypeError("I genitori devono essere oggetti di tipo 'Individual'")

    genome1, genome2 = parent1.genome, parent2.genome
    crossover_point = random.randint(1, min(len(genome1), len(genome2)) - 1)

    child1_genome = genome1[:crossover_point] + genome2[crossover_point:]
    child2_genome = genome2[:crossover_point] + genome1[crossover_point:]

    child1 = Individual(child1_genome)
    child2 = Individual(child2_genome)

    return child1, child2
