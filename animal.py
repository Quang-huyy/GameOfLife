from map import MapData
import math, time, threading

class Animal:
    _id_counter = 0
    def __init__(self, x, y):
        self.index = Animal._id_counter
        Animal._id_counter+=1
        self.x = x
        self.y = y

    def probingFood(self):
        pass

class Rabbit(Animal):
    _id_counter = 0
    listRabbit = []
    
    def __init__(self, x, y, grassList):
        super().__init__(x, y)
        self.index = Rabbit._id_counter
        Rabbit._id_counter+=1
        self.grassList = grassList
        print(f'Rabbit {self.index} spawned at coordinate: {x,y}')
        self.probingFood()
    
        # Start the thread to periodically check for food
        self.check_food_thread = threading.Thread(target=self.check_for_food)
        self.check_food_thread.start()

    def getRabbitList(self):
        return Rabbit.listRabbit
    
    def check_for_food(self):
        while True:
            time.sleep(2)  # Check every 2 seconds
            self.probingFood()

    def probingFood(self):
        self.minDistance = 9999
        for grass in self.grassList:
            if grass.x == self.x and grass.y == self.y:
                self.minDistance = 0
                break
            else:
                distance = math.sqrt((self.x - grass.x) ** 2 + (self.y - grass.y) ** 2)
                if distance < self.minDistance:
                    self.minDistance = distance
        print(f'Rabbit {self.index}: the closest food is at {self.minDistance}')
        
class Fox(Animal):
    _id_counter = 0
    listFox = []

    def __init__(self, x, y):
        super().__init__(x, y)
        self.index = Fox._id_counter
        Fox._id_counter+=1
        print(f'Fox {self.index} spawned at coordinate: {x,y}')