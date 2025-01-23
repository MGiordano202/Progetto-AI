import random
from AI.Genetic_Algorithm.individual import Individual
def random_mutation(individual, mutation_rate):
    """
    Esegue la mutazione casuale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :return: Individuo mutato.
    """
    genome = list(individual.genome)
    directions = ['u', 'd', 'l', 'r']
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] = random.choice(directions)

    individual.genome = genome
    return individual
