import random
from AI.Genetic_Algorithm.individual import Individual
def single_point_crossover(parent1, parent2):
    """
    Esegue il crossover a singono punto sui due genitori.
    :param parent1: primo genitore
    :param parent2: secondo genitore
    :return: nuovo individuo figlio
    """
    if not isinstance(parent1, Individual) or not isinstance(parent2, Individual):
        raise TypeError("Entrambi i genitori devono essere istanze di Individual")

    # Esegui il crossover
    crossover_point = random.randint(1, len(parent1.path) - 1)
    new_path = parent1.path[:crossover_point] + parent2.path[crossover_point:]
    new_bombs = parent1.bombs_placed[:crossover_point] + parent2.bombs_placed[crossover_point:]

    # Restituisci un nuovo individuo
    return Individual(new_path, new_bombs)