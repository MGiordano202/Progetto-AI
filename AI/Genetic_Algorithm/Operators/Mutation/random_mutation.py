import random
from AI.Genetic_Algorithm.individual import Individual
def random_mutation(individual, mutation_rate):
    """
    Esegue la mutazione casuale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :return: Individuo mutato.
    """
    for i in range(len(individual.genome)):
        if random.random() < mutation_rate:
            individual.genome[i] = random.choice(['u', 'd', 'l', 'r'])