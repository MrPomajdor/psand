from assets.cell import *
from assets.log import log
from assets.settings import Settings
import random

class Grid:
    def __init__(self, height, width, default_cell_type=Types.empty):
        self.width = width
        self.height = height
        self.grid = []
        self.default_cell_type = Types.empty
        self.create_grid()
    
    #explains itself
    def create_grid(self):
        log("\n\n---------------Creating grid---------------\n")
        log(f"width: {self.width}")
        log(f"height: {self.height}")
        log(f"Default cell type: {self.default_cell_type}")
        log("\n")
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(Cell(self.default_cell_type, x, y))
            self.grid.append(row)
    
    #Prints grid to console, or to file if Settings.drawToFile is true
    def print_grid(self,border=""):
        if Settings.drawToFile:
            with open(Settings.gridFileName, "w") as myfile:
                for x in range(self.height):
                    
                    for y in range(self.width):
                        myfile.write(self.grid[x][y].get_icon(), end=" ")
                    myfile.write(border+"\n")  # Add new line at the end of each row
        else:
            for x in range(self.height):
                print(border, end="")
                for y in range(self.width):
                    print(self.grid[y][x].get_icon(), end=" ")
                print(border)
            
        
    #Returns cell at given position       
    def get_cell(self, x, y):
        return self.grid[x][y]

    #Returns type of cell at given position (see class Types in cell.py)
    def get_cell_type(self, x, y):
        return self.grid[x][y].get_type()
    
    #Sets cell type at given position, and sets status to true
    def set_cell_type(self, x, y, type):
        log(f"h{self.height} w{self.width}")
        self.grid[x][y].set_type(type)
        self.grid[x][y].set_status(True)
        log(f"set cell at {(x,y)} to type {type}")
        return self.grid[x][y]
    
    #returns a cell neighbour in given direction
    def get_cell_neighbour(self, x, y,direction):
        if direction == "up":
            return self.grid[x][y-1]
        elif direction == "down":
            return self.grid[x][y+1]
        elif direction == "left":
            return self.grid[x-1][y]
        elif direction == "right":
            return self.grid[x+1][y]
        else:
            return None

    #moves cells in given direction  
    #Todo: NEED TO CHECK IF CELL IS MOVABLE
    def move_cell(self, x, y, direction):
        log(f"moving cell at {(x,y)} in direction {direction} ({self.grid[x][y].get_position()})")
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            log(f"cell at {(x,y)} is out of bounds, ignoring.")
            return
        if direction == "up":
            self.grid[x][y].set_position(x, y-1)
        elif direction == "down":
            self.grid[x][y].set_position(x, y + 1)
        elif direction == "left":
            self.grid[x][y].set_position(x - 1, y)
        elif direction == "right":
            self.grid[x][y].set_position(x + 1, y)
        log(f"new position: {self.grid[x][y].get_position()}")
        self.update_positions()
    
    #Update cell position when it is moved
    #Todo: it's not fully working i think
    def update_positions(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].get_position() == (x,y):
                    log(f"updating position of cell on {(x,y)} with position {self.grid[x][y].get_position()}")
                    #If cells position is not the same as the current cell in loop, set in array to new position
                    cell = self.grid[x][y]
                    self.grid[cell.get_position()[0]][cell.get_position()[1]] = cell  
                    self.grid[cell.get_position()[0]][cell.get_position()[1]].set_status(False)


                    self.grid[x][y] = Cell(Types.empty, x, y)

    #Update cell position based on its type
    #Main function for updating cell positions based on their type
    #Todo: make water work
    def update_physics(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].set_status(True)
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                #-------------SAND-------------
                if cell.get_type() == Types.sand:
                    if cell.get_status() == False: #check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue

                    #Check if cell is on edge of grid
                    if cell.get_position()[1] >= self.height - 1:
                        continue


                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"down").get_type() == Types.empty:
                        continue #do not move
                    
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")

                #-------------WATER-------------
                if cell.get_type()==Types.water:
                    if cell.get_status() == False:#check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue

                    #Check if cell is on edge of grid
                    if cell.get_position()[0] >= self.width - 1:
                        continue
                    rnd0 = random.randint(0,3)
                    rnd1 = random.randint(0,2)

                    #if it's on the floor, move it left or right from time to time
                    if cell.get_position()[1] >= self.height - 1:
                        if rnd0 == 0:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        elif rnd0 == 1: 
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue
                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"down").get_type() == Types.empty:
                        #move cell randomly left or right, the same as on floor
                        if rnd1 == 0:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        elif rnd1 == 1:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue
                    
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")
                #-------------SMOKE-------------
                if cell.get_type()==Types.smoke:
                    if cell.get_status() == False:#check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue

                    #Check if cell is on edge of grid
                    if cell.get_position()[0] >= self.width - 1:
                        continue
                    rnd0 = random.randint(0,3)
                    rnd1 = random.randint(0,2)

                    #if it's on the floor, move it left or right from time to time
                    if cell.get_position()[1] <=0:
                        if rnd0 == 0:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        elif rnd0 == 1: 
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue
                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"up").get_type() == Types.empty:
                        #move cell randomly left or right, the same as on floor
                        if rnd1 == 0:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        elif rnd1 == 1:
                            if self.get_cell_neighbour(cell.get_position()[0],cell.get_position()[1],"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        continue
                    
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "up")

