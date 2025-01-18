def manhattan_distance(param, goal):
    pass


def fitness_function(individual, grid, player, pathfinder, goal):
    """
    Calcola la fitness di un cromosoma.
    """
    fitness = 0
    simulated_player = player.clone()

    for action in individual["chromosome"]:
        if action == "B":
            simulated_player.place_bomb(grid)
        else:
            simulated_player.move_towards_goal(grid, pathfinder, goal)

        # Incrementa la fitness per avvicinarsi all'obiettivo
        distance = manhattan_distance((simulated_player.row, simulated_player.col), goal)
        fitness += max(1 / (distance + 1), 0.01)

    return fitness