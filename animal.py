class Animal:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

class Rabbit(Animal):
    def __init__(self, index, x, y):
        super().__init__(index, x, y)
        print(f'Rabbit {index} spawned at coordinate: {x,y}')
        