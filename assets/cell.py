class Types:
    empty = 0
    wall = 1
    sand = 2
    water = 3
    smoke = 4
    clone = 5



class Cell:
    def __init__(self,type,x,y):
        self.status = True #True when it wasn't moved by update_physics
        self.type = type
        self.x = x
        self.y = y
        self.data = {}

    def get_status(self):
        return self.status

    def set_status(self,status):
        self.status = status
        return self

    def get_type(self):
        return self.type

    def set_type(self,type):
        self.type = type
        return self

    def set_data(self,data):
        self.data = data
        return self
    def get_data(self):
        return self.data

    def get_position(self):
        return self.x,self.y
    def set_position(self,x,y):
        self.x = x
        self.y = y
        return self.x,self.y

    #icons are used for printing grid btw
    def get_icon(self):
        if self.get_type() == Types.empty:
            return " "
        elif self.get_type() == Types.wall:
            return "X"
        elif self.get_type() == Types.sand:
            return "#"
        elif self.get_type() == Types.water:
            return "."
        elif self.get_type() == Types.smoke:
            return "~"
        elif self.get_type() == Types.clone:
            return "C"
        else:
            return "?"
    
    def icon_to_type(icon):
        if icon == " ":
            return Types.empty
        elif icon == "X":
            return Types.wall
        elif icon == "#":
            return Types.sand
        elif icon == ".":
            return Types.water
        elif icon == "~":
            return Types.smoke
        elif icon == "C":
            return Types.clone
        else:
            return Types.empty
