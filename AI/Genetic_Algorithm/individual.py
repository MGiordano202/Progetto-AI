from AI.Genetic_Algorithm.fitness import calculate_fitness

class Individual:
    def __init__(self, genome):
        """
        Inizializza un nuovo individuo.
        :param genome:  Tuple di posizioni (riga, colonna) che rappresentano il genoma dell'individuo.

        """
        self.genome = genome
        self.fitness = 0

    def calculate_fitness(self, grid, player_start, player_goal):
        """
        Calcola la fitness di un individuo.
        :param grid: Griglia di gioco.
        :param player_start: Posizione di inizio del giocatore.
        :param player_goal: Posizione dell'obiettivo.
        :return: fitness dell'individuo.
        """
        self.fitness = calculate_fitness(self, grid, player_start, player_goal)


