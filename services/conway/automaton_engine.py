# Conway Automaton Engine (B3/S23 Deterministic State Machine)
# Implementation: Conway's Game of Life with checkpoint hashing
import hashlib

class ConwayAutomatonEngine:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.grid = [0] * (width * height)

    def set_cell(self, x, y, state=1):
        self.grid[y * self.width + x] = state

    def step(self):
        next_grid = [0] * (self.width * self.height)
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self._count_neighbors(x, y)
                current = self.grid[y * self.width + x]
                if current == 1 and (neighbors == 2 or neighbors == 3):
                    next_grid[y * self.width + x] = 1
                elif current == 0 and neighbors == 3:
                    next_grid[y * self.width + x] = 1
        self.grid = next_grid
        return self.get_state_hash()

    def _count_neighbors(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                count += self.grid[ny * self.width + nx]
        return count

    def get_state_hash(self):
        state_bytes = bytes(self.grid)
        return hashlib.sha256(state_bytes).hexdigest()
