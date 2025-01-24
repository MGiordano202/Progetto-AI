def generate_all_paths(grid, start, goal):
    """
    Genera tutti i percorsi possibili tra due punti.
    :param grid: Griglia di gioco
    :param start: posizione di partenza (riga e colonna)
    :param goal: posizione di arrivo (riga e colonna)
    :return: Lista di percorsi, ogni percorsi è una lista di mosse
    """
    # Direzioni valide e relative lettere di movimento
    directions = {
        (-1, 0): 'u',  # Su
        (1, 0): 'd',   # Giù
        (0, -1): 'l',  # Sinistra
        (0, 1): 'r'    # Destra
    }
    all_paths = []
    #max_depth = grid.rows * grid.cols  # Limite di profondità

    def dfs(current, path, visited):

        if current == goal:  # Se raggiungiamo l'obiettivo, aggiungiamo il path
            all_paths.append(path[:])
            return

        for direction, move in directions.items():
            next_position = (current[0] + direction[0], current[1] + direction[1])

            # Controlla se la prossima posizione è valida e non ancora visitata
            if (
                    0 <= next_position[0] < grid.rows and
                    0 <= next_position[1] < grid.cols and
                    grid.is_passable(next_position[0], next_position[1])
                    and next_position not in visited
            ):
                visited.add(next_position)  # Aggiungi a visited
                path.append(move)  # Aggiungi al path

                # Chiamata ricorsiva
                dfs(next_position, path, visited)

                # Backtracking: rimuovi la posizione dal path e da visited
                path.pop()
                if next_position in visited:  # Controllo per sicurezza
                    visited.remove(next_position)

    dfs(start, [], {start})
    return all_paths