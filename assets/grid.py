from assets.cell import *
from assets.log import log
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.create_grid()
        
    def create_grid(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(Types.empty, j, i))
            self.grid.append(row)
            
    def print_grid(self):
        for row in self.grid:
            for cell in row:
                print(cell.get_icon(), end=" ")
            print()
            
    def get_cell(self, x, y):
        return self.grid[y][x]

    def get_cell_type(self, x, y):
        return self.grid[y][x].get_type()
    
    def set_cell_type(self, x, y, type):
        self.grid[y][x].set_type(type)
    
    def move_cell(self, x, y, direction):
        log(f"moving cell at {(x,y)} in direction {direction} ({self.grid[y][x].get_position()})")
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            log(f"cell at {(x,y)} is out of bounds, ignoring.")
            return
        if direction == "up":
            self.grid[y][x].set_position(x, y - 1)
        elif direction == "down":
            self.grid[y][x].set_position(x, y + 1)
        elif direction == "left":
            self.grid[y][x].set_position(x - 1, y)
        elif direction == "right":
            self.grid[y][x].set_position(x + 1, y)
        log(f"new position: {self.grid[y][x].get_position()}")
        self.update_positions()
    
    #Update cell position when it is moved
    def update_positions(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[y][x].get_position() == (x,y):
                    log(f"updating position of cell on {(x,y)} with position {self.grid[y][x].get_position()}")
                    #If cells position is not the same as the current cell in loop, set in array to new position
                    cell = self.grid[y][x]
                    self.grid[cell.get_position()[1]][cell.get_position()[0]] = cell  
                    self.grid[cell.get_position()[1]][cell.get_position()[0]].set_status(False)


                    self.grid[y][x] = Cell(Types.empty, y, x)

    #Update cell position based on its type
    def update_physics(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x].set_status(True)
        for row in self.grid:
            for cell in row:
                if cell.get_type() == Types.sand:
                    if cell.get_status() == False:
                        log(f"status blocked {cell.get_position()}")
                        continue

                    #Check if cell is on edge of grid
                    if cell.get_position()[0] >= self.width - 1 or cell.get_position()[1] >= self.height - 1:
                        continue

                    #Check if cell under current cell NOT empty
                    if not self.grid[cell.get_position()[1]][cell.get_position()[0] + 1].get_type() == Types.empty:
                        continue #do not move
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")
