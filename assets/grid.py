from assets.cell import *
from assets.log import log
from assets.settings import Settings
import random
import json
class Grid:
    def __init__(self, height, width, default_cell_type=Types.empty):
        self.width = width
        self.height = height
        self.grid = []
        self.default_cell_type = Types.empty
        self.filename = ""
        self.loaded_text=""
        self.grid_loaded = False
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
    def load(self,filename):
        if self.grid_loaded:
            with open(filename, "r") as f:
                ffg = f.read() 
                if ffg != self.loaded_text:
                    log(ffg)
                    self.loaded_text = ffg
                    lines = ffg.split("\n")
                    
                    for y in range(len(lines)-1):
                        for x in range(len(lines[y])-1):
                            self.set_cell_type(x, y, Cell.icon_to_type(lines[y][x])) 
                    f.close()
        else:
            with open(filename, "r") as f:
                self.loaded_text = f.read()
                lines = self.loaded_text.splitlines()
                self.loaded_grid=lines
                f.close()
            for y in range(len(lines)-1):
                for x in range(len(lines[y])-1):
                    self.set_cell_type(x, y, Cell.icon_to_type(lines[y][x])) 
            self.grid_loaded=True
            log("Grid loaded!")

    #Prints grid to console, or to file if Settings.drawToFile is true
    def print_grid(self,border=""):
        if Settings.drawToFile:
            with open(Settings.gridFileName, "w") as myfile:
                for x in range(self.height):
                    
                    for y in range(self.width):
                        myfile.write(self.grid[x][y].get_icon(), end=" ")
                    myfile.write(border+"\n")  # Add new line at the end of each row
        else:
            if not Settings.replaceCharactersInConsole:
                for x in range(self.height):
                    print(border, end="")
                    for y in range(self.width):
                        print(self.grid[y][x].get_icon(), end=" ")
                    print(border)
            else:
                lines="\r"
                for x in range(self.height):
                    lines += border
                    for y in range(self.width):
                        lines += self.grid[y][x].get_icon()+" "
                    lines+= border+"\n"
                lines+="\r"
                print("\r"+lines,end="\r")
            
            
        
    #Returns cell at given position       
    def get_cell(self, x, y):
        return self.grid[x][y]

    #Returns type of cell at given position (see class Types in cell.py)
    def get_cell_type(self, x, y):
        return self.grid[x][y].get_type()
    
    #Sets cell type at given position, and sets status to true
    def set_cell_type(self, x, y, type):
        self.grid[x][y].set_type(type)
        self.grid[x][y].set_status(True)
        log(f"set cell at {(x,y)} to type {type}",weight=60)
        return self.grid[x][y]
    


    #returns a cell neighbour in given direction
    def get_cell_neighbour(self, cell,direction):
        x,y = cell.get_position()  
        if direction == "up":
            #check if cell is in bounds
            if y-1 >= 0:  
                return self.grid[x][y-1]
            else:
                return Cell(Types.wall,x,y-1)
        elif direction == "down":
            if y+1 < self.height:
                return self.grid[x][y+1]
            else:
                return Cell(Types.wall,x,y+1)
        elif direction == "left":
            if x-1 >= 0:
                return self.grid[x-1][y]
            else:
                return Cell(Types.wall,x-1,y)
        elif direction == "right":
            if x+1 < self.width:
                return self.grid[x+1][y]
            else:
                return Cell(Types.wall,x+1,y)
        else:
            return None
    def get_all_neighbours(self, cell):
        directions = ["up", "down", "left", "right"]
        x,y = cell.get_position()
        neighbours = []
        for i in range(4):
            if self.get_cell_neighbour(cell, directions[i]).get_type() != Types.wall and self.get_cell_neighbour(cell, directions[i]).get_type() != Types.empty:
                neighbours.append(self.get_cell_neighbour(cell, directions[i]))
                log(f"found neighbour at {self.get_cell_neighbour(cell, directions[i]).get_position()}({self.get_cell_neighbour(cell, directions[i]).get_type()})",weight=70)
        if len(neighbours) == 0:
            log("no neighbours found",weight=70)
            return None
        return neighbours

    #moves cells in given direction  
    #Todo: NEED TO CHECK IF CELL IS MOVABLE
    def move_cell(self, x, y, direction):
        log(f"moving cell at {(x,y)} in direction {direction} ({self.grid[x][y].get_position()})",weight=8)
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
        log(f"new position: {self.grid[x][y].get_position()}",weight=8)
        self.update_positions()
    def swap_cells(self, cell1, cell2):
        log(f"swapping cells {cell1.get_position()} and {cell2.get_position()}",weight=60)
        cell1_type = cell1.get_type()
        cell2_type = cell2.get_type()
        cell1.set_type(cell2_type)
        cell2.set_type(cell1_type)
        cell1.set_status(True)
        cell2.set_status(True)
        self.update_positions()     
    #Update cell position when it is moved
    #Todo: it's not fully working i think
    def update_positions(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].get_position() == (x,y):
                    log(f"updating position of cell on {(x,y)} with position {self.grid[x][y].get_position()}",weight=10)
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


                def move_sides():
                    rnd1=random.randint(0,3)
                    if rnd1 == 0:
                        if self.get_cell_neighbour(cell,"left").get_type() == Types.empty:
                            self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                    elif rnd1 == 1:
                        if self.get_cell_neighbour(cell,"right").get_type() == Types.empty:
                            self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                       
                #-------------CLONE-------------
                if cell.get_type() == Types.clone:
                    if "cloning" in cell.get_data():
                        if self.get_cell_neighbour(cell,"down").get_type() == Types.empty:
                            self.set_cell_type(cell.get_position()[0], cell.get_position()[1]+1, cell.get_data()["cloning"])
                    else:
                        
                        neighbours = self.get_all_neighbours(cell)
                        if neighbours != None:
                            selected = neighbours[random.randint(0,len(neighbours)-1)]
                            log(f"cell at {cell.get_position()} cloning {selected.get_type()}",weight=70)
                            
                            cell.set_data({"cloning":selected.get_type()})
                            if self.get_cell_neighbour(cell,"down").get_type() == Types.empty:
                                self.set_cell_type(cell.get_position()[0], cell.get_position()[1]+1, cell.get_data()["cloning"])
                        
                #-------------SAND-------------
                elif cell.get_type() == Types.sand:
                    if cell.get_status() == False: #check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue

                    #Check if cell is on edge of grid
                    if cell.get_position()[1] >= self.height - 1:
                        continue


                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell,"down").get_type() == Types.empty:
                        if self.get_cell_neighbour(cell,"down").get_type() == Types.smoke:
                            self.swap_cells(cell,self.get_cell_neighbour(cell,"down"))
                            continue
                        rnd1=random.randint(0,6)
                        #move cell randomly
                        if rnd1 == 0:
                            if self.get_cell_neighbour(cell,"left").get_type() == Types.empty:
                                if self.get_cell(cell.get_position()[0]-1,cell.get_position()[1]+1).get_type() == Types.empty:
                                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                            elif self.get_cell_neighbour(cell,"right").get_type() == Types.empty:
                                if self.get_cell(cell.get_position()[0]+1,cell.get_position()[1]+1).get_type() == Types.empty:
                                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        elif rnd1 == 1:
                            if self.get_cell_neighbour(cell,"right").get_type() == Types.empty:
                                if self.get_cell(cell.get_position()[0]+1,cell.get_position()[1]+1).get_type() == Types.empty:
                                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                            elif self.get_cell_neighbour(cell,"left").get_type() == Types.empty:
                                if self.get_cell(cell.get_position()[0]-1,cell.get_position()[1]+1).get_type() == Types.empty:
                                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        continue
                    
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")

                #-------------WATER-------------
                elif cell.get_type()==Types.water:
                    if cell.get_status() == False:#check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue

                    rnd0 = random.randint(0,3)
                    rnd1 = random.randint(0,2)

                    

                    #if it's on the floor, move it left or right from time to time
                    if cell.get_position()[1] >= self.height - 1:
                        move_sides()
                        continue
                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell,"down").get_type() == Types.empty:
                        #if cell under current cell is smoke, swap cells
                        if self.get_cell_neighbour(cell,"down").get_type() == Types.smoke:
                            self.swap_cells(cell,self.get_cell_neighbour(cell,"down"))
                            continue
                        rnd1=random.randint(0,3)
                        #move cell randomly
                        if rnd1 == 0:
                            if self.get_cell_neighbour(cell,"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                            elif self.get_cell_neighbour(cell,"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                        elif rnd1 == 1:
                            if self.get_cell_neighbour(cell,"right").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "right")
                            elif self.get_cell_neighbour(cell,"left").get_type() == Types.empty:
                                self.move_cell(cell.get_position()[0], cell.get_position()[1], "left")
                        continue
                    
                             
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "down")
                #-------------SMOKE-------------
                elif cell.get_type()==Types.smoke:
                    if cell.get_status() == False:#check if cell was updated in previous loop
                        #log(f"status blocked {cell.get_position()}")
                        continue


                    #if it's on the floor, move it left or right from time to time
                    if cell.get_position()[1] <=0:
                        move_sides()
                        continue
                    #Check if cell under current cell NOT empty
                    if not self.get_cell_neighbour(cell,"up").get_type() == Types.empty:
                        #move cell randomly left or right, the same as on floor
                        move_sides()
                        continue
                    
                    #move cell down
                    self.move_cell(cell.get_position()[0], cell.get_position()[1], "up")

