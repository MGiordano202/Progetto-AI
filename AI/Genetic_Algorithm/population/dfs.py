def generate_all_paths(grid, start, goal):
    """
    Genera tutti i percorsi possibili tra due punti.
    :param grid: Griglia di gioco
    :param start: posizione di partenza (riga e colonna)
    :param goal: posizione di arrivo (riga e colonna)
    :return: Lista di percorsi, ogni percorsi è una lista di mosse
    """
    directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    all_paths = []
    max_depth = grid.size()
    def dfs(current_position, path, visited, depth):
        if depth > max_depth:
            return

        if current_position == goal:
            all_paths.append(path)
            return

        for move, (dr, dc) in directions.items():
            next_position = (current_position[0] + dr, current_position[1] + dc)

            if not grid.is_passable(*next_position):
                continue

            if grid.is_passable(*next_position):
                visited.add(next_position)
                path.appenf(move)

                dfs(next_position, path, visited, depth +1)

                path.pop()
                visited.remove(next_position)


    dfs(start, [], {start}, 0)
    return all_paths