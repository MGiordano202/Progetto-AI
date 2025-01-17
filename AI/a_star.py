from heapq import heappush, heappop

class Astar:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        if not self.grid.is_passable(*start) or not self.grid.is_passable(*goal):
            print("Invalid start or goal start = {start}, goal = {goal}")
            return None, []

        block_destruction_cost = 2
        open_heap = []
        heappush(open_heap, (0, start))
        open_set = {start}

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        blocks_to_destroy= []

        while open_set:
            __, current = heappop(open_heap)
            open_set.remove(current)
            #print(f"Esaminando nodo: {current}, Goal: {goal}")  # Debug

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path, blocks_to_destroy

            for neighbor in self.grid.get_neighbors(*current):
                cell_type = self.grid.get_cell(*neighbor)

                if cell_type == "D":
                    tentative_g_score = g_score[current] + block_destruction_cost
                    if neighbor not in blocks_to_destroy:
                        blocks_to_destroy.append(neighbor) # Aggiungi il blocco alla lista
                else:
                    tentative_g_score = g_score[current] + 1

                if not self.grid.is_passable(*neighbor) and cell_type != "D":
                    continue

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        heappush(open_heap, (f_score[neighbor], neighbor))
                        open_set.add(neighbor)


            #print(f"Current: {current}, Open set: {open_set}, G score: {g_score}, F score: {f_score}")

        print("No path found")
        return None, []

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
