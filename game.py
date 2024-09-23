from animal import *
from map import *
import numpy as np
import threading

map = MapData()

def createAnimal(map, list, numberAnimal, typeAnimal, foodMap=None):
    map1 = map.get_matrix()
    for _ in range (numberAnimal):
        x, y = -1, -1
        while True:
            x, y = np.random.randint(0, map.mapHeight), np.random.randint(0, map.mapWidth)
            if map1[x][y] == S or map1[x][y] == G:
                break
        if typeAnimal == 'rabbit':
            list.append(Rabbit(x, y, foodMap))
        elif typeAnimal == 'fox':
            list.append(Fox(x, y))

map_thread = threading.Thread(target = map.createMap)
map_thread.start()
map.event.wait()

food_thread = threading.Thread(target = map.spawnFood)
food_thread.start()

createAnimal(map, Rabbit.listRabbit, 5, 'rabbit', map.get_food())
createAnimal(map, Fox.listFox, 2, 'fox')

map.spawnAnimal(Rabbit.listRabbit)
map.spawnAnimal(Fox.listFox)

 

