import random
from AI.Genetic_Algorithm.individual import Individual
def single_point_crossover(parent1, parent2):
    """
    Esegue il crossover a singono punto sui due genitori.
    :param parent1: primo genitore
    :param parent2: secondo genitore
    :return: nuovo individuo figlio
    """
    # Debug: Verifica i genitori
    if not isinstance(parent1, Individual) or not isinstance(parent2, Individual):
        raise TypeError("I genitori devono essere oggetti di tipo 'Individual'")

    crossover_point = random.randint(1, len(parent1.genome) - 1)
    new_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]

    child = Individual(genome=new_genome[:], grid_size=parent1.grid_size)

    return child
