class Types:
    empty = 0
    wall = 1
    sand = 2
    water = 3



class Cell:
    def __init__(self,type,x,y):
        self.status = True
        self.type = type
        self.x = x
        self.y = y

    def get_status(self):
        return self.status

    def set_status(self,status):
        self.status = status

    def get_type(self):
        return self.type

    def set_type(self,type):
        self.type = type

    def get_position(self):
        return self.x,self.y
    def set_position(self,x,y):
        self.x = x
        self.y = y

    def get_icon(self):
        if self.get_type() == Types.empty:
            return " "
        elif self.get_type() == Types.wall:
            return "X"
        elif self.get_type() == Types.sand:
            return "#"
        elif self.get_type() == Types.water:
            return "."