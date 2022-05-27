from assets.cell import *
from assets.log import log
from assets.settings import Settings
import random

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.default_cell_type = Types.empty
        self.create_grid()
        
    def create_grid(self):
        log("\n\n---------------Creating grid---------------\n")
        log(f"width: {self.width}")
        log(f"height: {self.height}")
        log(f"Default cell type: {self.default_cell_type}")
        log("\n")
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(self.default_cell_type, j, i))
            self.grid.append(row)
            
    def print_grid(self):
        if Settings.drawToFile:
            with open(Settings.gridFileName, "w") as myfile:
                for row in self.grid:
                    for cell in row:
                        myfile.write(cell.get_type().value + " ")
                    myfile.write("\n")  # Add new line at the end of each row
        else:
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
        self.grid[y][x].set_status(True)
        log(f"set cell at {(x,y)} to type {type}")
        return self.grid[y][x]
    def get_cell_neighbour(self, x, y,direction):
        if direction == "up":
            return self.grid[y - 1][x]
        elif direction == "down":
            return self.grid[y + 1][x]
        elif direction == "left":
            return self.grid[y][x - 1]
        elif direction == "right":
            return self.grid[y][x + 1]
        else:
            return None
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
                    if cell.get_position()[1] >= self.height - 1:
                        continue


                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"down").get_type() == Types.empty:
                        continue #do not move
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")

                if cell.get_type()==Types.water:
                    if cell.get_status() == False:
                        log(f"status blocked {cell.get_position()}")
                        continue
                    
                    
                    


                    #Check if cell is on edge of grid
                    if cell.get_position()[0] >= self.width - 1:
                        continue
                    if cell.get_position()[1] >= self.height - 1:
                        if random.randint(0,3) == 0:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        else:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue

                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"down").get_type() == Types.empty:

                        #move cell randomly left or right
                        if random.randint(0,2) == 0:
                            self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        else:
                            self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue

                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")

