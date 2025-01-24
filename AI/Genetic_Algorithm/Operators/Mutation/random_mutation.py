import random
from AI.Genetic_Algorithm.individual import Individual
def random_mutation(individual, mutation_rate):
    """
    Esegue la mutazione casuale su un individuo.
    :param individual: Individuo da mutare.
    :param mutation_rate: Probabilità di mutazione.
    :return: Individuo mutato.
    """
    if not individual:  # Controllo su un valore None
        raise ValueError("L'individuo passato a mutation è None.")

    mutated_genome = []
    for gene in individual.genome:
        if random.random() < mutation_rate:
            mutated_genome.append(random.choice(['u', 'd', 'l', 'r']))  # Nuovo gene casuale
        else:
            mutated_genome.append(gene)  # Gene invariato

    # Assicurati che il nuovo individuo sia valido
    mutated_individual = Individual(genome=mutated_genome)
    return mutated_individual