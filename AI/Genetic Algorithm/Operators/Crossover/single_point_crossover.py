def single_point_crossover(p1, p2):
    """
    Esegue il crossover a singono punto sui due genitori.
    :param p1: primo genitore
    :param p2: secondo genitore
    :return: nuovo individuo figlio
    """
    midpoint = len(p1.path) // 2
    child_path = p1.path[:midpoint] + p2.path[midpoint:]
    return {"path": child_path}