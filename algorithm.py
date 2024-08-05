import random

class Grid():
    def __init__(self, width=20, height=10, mines=15):
        self.width = width
        self.height = height
        self.mines = mines

        self.grid = None
        self.player_grid = None

    def generate_mines(self):
        self.mine_positions = []
        for _ in range(self.mines):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (x, y) not in self.mine_positions:
                    self.mine_positions.append((x, y))
                    self.grid[y][x] = -1
                    break
    
    def generate_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == -1:
                    continue
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        if 0 <= y + dy < self.height and 0 <= x + dx < self.width:
                            if self.grid[y + dy][x + dx] == -1:
                                count += 1
                self.grid[y][x] = count
    
    def new(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.generate_mines()
        self.generate_numbers()
        self.player_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def get_cell(self, x, y):
        return self.grid[y][x]
    
    def is_mine(self, x, y):
        return self.grid[y][x] == -1
    
    def print_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == -1:
                    print("*", end=" ")
                else:
                    print(self.grid[y][x], end=" ")
            print()

    def place_sign(self, n, position):
        x = int(position.x // 2)
        y = int(position.z // 2)
        self.player_grid[y][x] = n

    
if __name__ == "__main__":
    grid = Grid(mines=20)
    grid.new()
    grid.print_grid()