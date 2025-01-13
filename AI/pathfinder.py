# AI/pathfinder.py
class Pathfinder:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        raise NotImplementedError("This method should be overridden by subclasses")