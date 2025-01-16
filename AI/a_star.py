from heapq import heappush, heappop

class Astar:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        if not self.grid.is_passable(*start) or not self.grid.is_passable(*goal):
            print(f"Invalid start or goal: start={start}, goal={goal}")
            return []

        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            __, current = heappop(open_set)
            print(f"Esaminando nodo: {current}, Goal: {goal}")  # Debug
            if current == goal:
                print("Goal raggiunto!")
                return self.reconstruct_path(came_from, current)

            for neighbor in self.grid.get_neighbors(*current):
                cell_type = self.grid.get_cell(*neighbor)
                if cell_type == "W":
                    continue
                elif cell_type == "D":
                    tentative_g_score = g_score[current] + self.grid.get_cost(*neighbor)
                else:
                    tentative_g_score = g_score[current] + self.grid.get_cost(*neighbor)

                if neighbor not in g_score or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))
            print(f"Current: {current}, Open set: {open_set}, G score: {g_score}, F score: {f_score}")
        print("No path found")
        return []

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
