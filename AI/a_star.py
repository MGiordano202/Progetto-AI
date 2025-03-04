from heapq import heappush, heappop

class Astar:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        if not self.grid.is_passable(*start) or not self.grid.is_passable(*goal):
            print("Invalid start or goal start = {start}, goal = {goal}")
            return None, []

        block_destruction_cost = 5
        frontiera = []
        heappush(frontiera, (self.heuristic(start, goal), start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        blocks_to_destroy= []

        while frontiera:
            _, current_node = heappop(frontiera) # nodo con il costo minore
            #print(f"Esaminando nodo: {current_node}, Goal: {goal}")  # Debug

            if current_node == goal:
                path = self.reconstruct_path(came_from, current_node)
                return path, blocks_to_destroy


            for neighbor in self.grid.get_neighbors(*current_node):
                cell_type = self.grid.get_cell(*neighbor)

                # Calcolo del costo per raggiungere il vicino
                if cell_type == "D":
                    tentative_g_score = g_score[current_node] + block_destruction_cost # Costo per distruggere un blocco
                    if neighbor not in blocks_to_destroy:
                        blocks_to_destroy.append(neighbor)
                else:
                    tentative_g_score = g_score[current_node] + 1

                if neighbor not in g_score or tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(frontiera, (f_score[neighbor], neighbor))

            print(f"current_node: {current_node}, frontiera: {frontiera}, G score: {g_score}, F score: {f_score}")

        print("No path found")
        return None, []

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def reconstruct_path(came_from, current_node):
        path = [current_node]
        while current_node in came_from:
            current_node = came_from[current_node]
            path.append(current_node)
        return path[::-1]
