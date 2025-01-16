from heapq import heappush, heappop

class Astar:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        destructible_blocks = set()

        while open_set:
            __, current = heappop(open_set)
            print(f"Esaminando nodo: {current}, Goal: {goal}")  # Debug

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1], list(destructible_blocks)

            for neighbor in self.grid.get_neighbors(*current):
                cell_type = self.grid.get_cell(*neighbor)

                if cell_type == "W":
                    continue

                if cell_type == "0" or cell_type == "G":
                    cost = 1
                elif cell_type == "D":
                    cost = 5
                else:
                    continue

                tentative_g_score = g_score[current] + cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if cell_type == "D":
                        destructible_blocks.add(neighbor)

                    heappush(open_set, (f_score[neighbor], neighbor))
            print(f"Current: {current}, Open set: {open_set}, G score: {g_score}, F score: {f_score}")

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
