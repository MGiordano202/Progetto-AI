def calculate_fitness(individual, grid, player_start, player_goal):
    """
    Calcola la fitness di un individuo.
    :param individual: Individuo da valutare
    :param grid: Griglia di gioco
    :param player_start: Posizione iniziale del giocare
    :param player_goal: Posizione dell'obiettivo
    :return: valore fitness
    """
    current_position = player_start
    fitness = 0
    destroyed_blocks = set()

    for gene in individual.genome:
        if gene == 'u':
            new_position = (current_position[0] - 1, current_position[1])
        elif gene == 'd':
            new_position = (current_position[0] + 1, current_position[1])
        elif gene == 'l':
            new_position = (current_position[0], current_position[1] - 1)
        elif gene == 'r':
            new_position = (current_position[0], current_position[1] + 1)
        elif gene == 'b':
            affected_blocks = simulate_bomb_explosion(grid, *current_position)
            for block in affected_blocks:
                if grid.get_cell(*block) == "D" and block not in destroyed_blocks:
                    fitness += 50
                    destroyed_blocks.add(block)
            continue
        else:
            continue

        # Penalizza i movimenti fuori dalla griglia
        if not (0 <= new_position[0] < grid.rows and 0 <= new_position[1] < grid.cols):
            fitness -= 100
            continue

        # Penalizza i movimenti in celle non passabili
        if not grid.is_passable(*new_position):
            fitness -= 100
            continue

        # Premia avvicinamento all'obiettivo
        goal_distance = abs(player_goal[0] - new_position[0]) + abs(player_goal[1] - new_position[1])
        fitness += 100 / (1 + goal_distance)

        current_position = new_position

    if current_position == player_goal:
        fitness += 1000

    individual.fitness = fitness
    return fitness