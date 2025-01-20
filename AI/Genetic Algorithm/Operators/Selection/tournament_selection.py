import  random

def tournament_selection(population, tournament_size):
    """
    Esegue la selezione a torneo su una popolazione.
    :param population: Lista di individui.
    :param tournament_size: Numero di individui selezionati per il torneo
    :return: Il vincitore del torneo.
    """
    tournament_contestants = random.sample(population, tournament_size)

    best_individual = max(tournament_contestants, key=lambda x: x.fitness)
    return best_individual