class Object:
    _id_counter = 0 
    def __init__(self, x, y):
        self.index = Object._id_counter
        Object._id_counter+=1
        self.x = x
        self.y = y

class Grass(Object):
    _id_counter = 0 
    def __init__(self, x, y):
        super().__init__(x, y)
        self.index = Grass._id_counter
        Grass._id_counter+=1
        print(f'Grass {self.index} spawned at coordinate: {x,y}')