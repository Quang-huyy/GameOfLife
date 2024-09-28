from map import MapData
from object import Grass
import math, time, threading

class Animal:
    _id_counter = 0
    def __init__(self, x, y):
        self.index = Animal._id_counter
        Animal._id_counter+=1
        self.x = x
        self.y = y

    def probingFood(self, foodList, foodType):
        self.minDistance = 9999
        self.nearestFood = None
        foodIndex = None

        for index, food in enumerate(foodList):
            # Check if the food is at the same coordinate
            if food.x == self.x and food.y == self.y:
                self.minDistance = 0
                self.nearestFood = food
                foodIndex = index
                break
            else:
                distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
                if distance < self.minDistance:
                    self.minDistance = distance
                    self.nearestFood = food
                    foodIndex = index

        print(f'{self.__class__.__name__} {self.index}: the closest {foodType} is at coord :{self.nearestFood.x, self.nearestFood.y}')
        return foodIndex

    def move(self, axe, nearestFood):
        if axe == True:
            if self.x < nearestFood.x:
                self.x += 1
            elif self.x > nearestFood.x:
                self.x -= 1
        elif axe == False:
            if self.y < nearestFood.y:
                self.y += 1
            elif self.y > nearestFood.y:
                self.y -= 1

    def gotoFood(self, nearestFood):
        if nearestFood is not None:
            if self.x != nearestFood.x:
                self.move(True, nearestFood)             #True to indicate axe X
            elif self.y != nearestFood.y:
                self.move(False, nearestFood)   
            print(f'{self.__class__.__name__} {self.index} now at coordinate: {self.x,self.y}')

    def updateFoodMap(self, foodIndex, listFood):
        if foodIndex is not None:
            listFood.pop(foodIndex)
        else:
            print(f'{self.__class__.__name__} {self.index}: No valid food index to update.')

    def run(self, foodList):
        while True:
            foodIndex = self.probingFood(foodList, Grass.__name__)
            self.gotoFood(self.nearestFood)
            if self.x == self.nearestFood.x and self.y == self.nearestFood.y:
                self.updateFoodMap(foodIndex, foodList)
            time.sleep(1)

class Rabbit(Animal):
    _id_counter = 0
    listRabbit = []
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__class__.listRabbit.append(self)
        self.index = Rabbit._id_counter
        Rabbit._id_counter+=1
        print(f'{self.__class__.__name__} {self.index} spawned at coordinate: {self.x,self.y}')
        threading.Thread(target=self.run, args=(Grass.getgrassList(),), daemon=True).start()
            
    @classmethod
    def getListRabbit(cls):
        return cls.listRabbit
        
class Fox(Animal):
    _id_counter = 0
    listFox = []
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__class__.listFox.append(self)
        self.index = Fox._id_counter
        Fox._id_counter+=1
        print(f'{self.__class__.__name__} {self.index} spawned at coordinate: {x,y}')
        threading.Thread(target=self.run, args=(Rabbit.getListRabbit(),), daemon=True).start()

    @classmethod
    def getFoxList(cls):
        return cls.listFox