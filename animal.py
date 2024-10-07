from map import MapData
from object import Grass
import math, time, threading

class Animal:
    _id_counter = 0
    listAnimal = []

    def __init__(self, x, y):
        self.index = Animal._id_counter
        Animal._id_counter+=1
        self.coord = [x,y]
        self.__class__.listAnimal.append(self)
        self.stop = False

    @classmethod
    def getListAnimal(cls):
        return cls.listAnimal
    
    def probingFood(self, foodList, foodType):
        self.minDistance = 9999
        self.nearestFood = None
        foodIndex = None

        for food in foodList:
            # Check if the food is at the same coordinate
            if food.coord[0] == self.coord[0] and food.coord[1] == self.coord[1]:
                self.minDistance = 0
                self.nearestFood = food
                foodIndex = foodList.index(food)
                break
            else:
                distance = math.sqrt((self.coord[0] - food.coord[0]) ** 2 + (self.coord[1] - food.coord[1]) ** 2)
                if distance < self.minDistance:
                    self.minDistance = distance
                    self.nearestFood = food
                    foodIndex = foodList.index(food)
        return foodIndex

    def checkValidMove(self):
        for animal in self.listAnimal:
            if animal is not self:
                if isinstance(animal, self.__class__):
                    if self.coord == animal.coord:
                        return False
        return True

    def move(self, nearestFood):
        oldCoord = self.coord[:]    
        if self.coord[0] < nearestFood.coord[0]:
            self.coord[0] += 1
        elif self.coord[0] > nearestFood.coord[0]:
            self.coord[0] -= 1
        if self.coord[1] < nearestFood.coord[1]:
            self.coord[1] += 1
        elif self.coord[1] > nearestFood.coord[1]:
            self.coord[1] -= 1
        if not self.checkValidMove():
            self.coord = oldCoord

    def gotoFood(self, nearestFood):
        if nearestFood is not None:
            if self.coord[0] != nearestFood.coord[0] or self.coord[1] != nearestFood.coord[1]:
                self.move(nearestFood)
            print(f'{self.__class__.__name__} {self.index} now at coordinate: {self.coord[0],self.coord[1]}')

    def updateFoodMap(self, foodIndex, listFood):
        if foodIndex is not None:
            listFood.pop(foodIndex)
            listFood[foodIndex].stop = True
        else:
            print(f'{self.__class__.__name__} {self.index}: No valid food index to update.')

    def run(self, foodList, foodType):
        while not self.stop:
            foodIndex = self.probingFood(foodList, foodType)
            self.gotoFood(self.nearestFood)
            if self.coord[0] == self.nearestFood.coord[0] and self.coord[1] == self.nearestFood.coord[1]:
                self.updateFoodMap(foodIndex, foodList)
            time.sleep(1)
        self.stop_event.set()

class Rabbit(Animal):
    _id_counter = 0
    listRabbit = []
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__class__.listRabbit.append(self)
        self.index = Rabbit._id_counter
        Rabbit._id_counter+=1
        print(f'{self.__class__.__name__} {self.index} spawned at coordinate: {self.coord[0],self.coord[1]}')
        threading.Thread(target=self.run, args=(Grass.getgrassList(),Grass.__name__), daemon=True).start()
            
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
        threading.Thread(target=self.run, args=(Rabbit.getListRabbit(),Rabbit.__name__), daemon=True).start()

    @classmethod
    def getListFox(cls):
        return cls.listFox