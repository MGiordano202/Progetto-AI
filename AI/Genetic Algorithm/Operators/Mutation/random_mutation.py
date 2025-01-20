import random

def random_mutation(individual, mutation_rate):
    """
    Esegue la mutazione casuale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :return: Individuo mutato.
    """
    if random.random() < mutation_rate:
        mutation_index = random.randint(0, len(individual.path) - 1)
        # Cambia la posizione a un valore casuale valido
        individual.path[mutation_index] = (random.randint(0, 9), random.randint(0, 9))
    return individual
