from bomb import Bomb
def calculate_fitness(individual, grid, player_start, player_goal):
    """
    Calcola la fitness di un individuo.
    :param individual: Individuo da valutare
    :param grid: Griglia di gioco
    :param player_start: Posizione iniziale del giocare
    :param player_goal: Posizione dell'obiettivo
    :return: valore fitness
    """

    # Debug per verificare il tipo di genome
    if not hasattr(individual, 'genome'):
        raise AttributeError("L'individuo non ha un attributo 'genome'")
    if not isinstance(individual.genome, (list, str)):
        raise TypeError(f"'genome' deve essere una lista o una stringa, trovato: {type(individual.genome)}")

    # Debug per verificare il genoma iniziale
    print(f"[DEBUG] Genome dell'individuo: {individual.genome}")

    current_position = player_start
    fitness = 0
    destroyed_blocks = set()
    visited_positions = set()
    steps_taken = 0

    for gene in individual.genome:
        steps_taken += 1
        if gene == 'u':
            new_position = (current_position[0] - 1, current_position[1])
        elif gene == 'd':
            new_position = (current_position[0] + 1, current_position[1])
        elif gene == 'l':
            new_position = (current_position[0], current_position[1] - 1)
        elif gene == 'r':
            new_position = (current_position[0], current_position[1] + 1)
        else:
            continue

        # Penalizza i movimenti fuori dalla griglia
        if not (0 <= new_position[0] < grid.rows and 0 <= new_position[1] < grid.cols):
            fitness -= 50
            continue

        # Controlla la cella nella direzione del movimento
        if grid.get_cell(*new_position) == "D":
            # Piazza una bomba nella posizione attuale
            bomb = Bomb(*current_position)
            affected_blocks = bomb.simulate_bomb_explosion(grid)
            for block in affected_blocks:
                if grid.get_cell(*block) == "D" and block not in destroyed_blocks:
                    fitness += 50  # Premio per ogni blocco distrutto
                    destroyed_blocks.add(block)

        # Penalizza i movimenti in celle non passabili
        if not grid.is_passable(*new_position):
            fitness -= 50
            continue

        # Penalizza movimenti ripetuti nella stessa cella
        if new_position in visited_positions:
            fitness -= 10  # Penalità per cicli
        else:
            visited_positions.add(new_position)

        # Premia avvicinamento all'obiettivo
        goal_distance = abs(player_goal[0] - new_position[0]) + abs(player_goal[1] - new_position[1])
        fitness += 100 / (1 + goal_distance)

        current_position = new_position

    # Premio per il completamento rapido del percorso
    if current_position == player_goal:
        fitness += 1000  # Grande premio per aver raggiunto il goal
        fitness += 500 / steps_taken  # Premia un completamento rapido

    # Penalità per percorsi troppo lunghi senza raggiungere il goal
    if steps_taken > 200:
        fitness -= (steps_taken - 200) * 5

    # Debug per verificare la fitness calcolata
    print(f"[DEBUG] Fitness calcolata per l'individuo: {fitness}")

    individual.fitness = fitness
    return fitness