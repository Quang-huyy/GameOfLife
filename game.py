from animal import *
from map import *
import numpy as np
import threading

map = MapData()

map_thread = threading.Thread(target = map.createMap)
map_thread.start()

def createAnimal(map, listRabbit):
    map1 = map.get_matrix()
    for i in range (0,5):
        x, y = -1, -1
        while True:
            x, y = np.random.randint(0, map.mapHeight), np.random.randint(0, map.mapWidth)
            if map1[x][y] == S or map1[x][y] == G:
                break
        listRabbit.append(Rabbit(i, x, y))

listRabbit = []

createAnimal(map, listRabbit)
map.event.wait()
map.spawnAnimal(listRabbit)

food_thread = threading.Thread(target=map.spawnFood)
food_thread.start()