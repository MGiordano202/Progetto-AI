from heapq import heappush, heappop

class UCS:
    def __init__(self, grid):
        self.grid = grid

        
    def find_path(self, start, goal):
        """
        Implementazione dell'algoritmo Uniform Cost Search per trovare il percorso più breve
        :param start: tupla che indica il punto di partenza 
        :param goal: tupla che indica la destinazione
        :return: lista di tuple che rappresentano il percorso o None se impossibile.
        """
        if not self.grid.is_passable(*start) or not self.grid.is_passable(*goal):
            print("Invalid start or goal start = {start}, goal = {goal}")
            return None, []
        
        block_destruction_cost = 5
        frontier = []
        heappush(frontier, (0, start)) # (costo, nodo)

        came_from = {}
        g_score = {start: 0}
        block_to_destroy = []

        while frontier:
            costo, current_node = heappop(frontier)

            if current_node == goal:
                path = self.reconstruct_path(came_from, current_node)
                return path, block_to_destroy


            for child in self.grid.get_child(*current_node):
                cell_type = self.grid.get_cell(*child)

               # Gestione dei costi
                if cell_type == "D":
                    tentative_g_score = g_score[current_node] + block_destruction_cost
                    if child not in block_to_destroy:
                        block_to_destroy.append(child)
                else:
                    tentative_g_score = g_score[current_node] + 1

                # Aggiorna il percorso se il costo è minore
                if child not in g_score or tentative_g_score < g_score[child]:
                        came_from[child] = current_node
                        g_score[child] = tentative_g_score
                        heappush(frontier, (g_score[child], child))

            
        print("No path found")
        return None, []

    @staticmethod
    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]