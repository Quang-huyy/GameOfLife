import pygame, sys
import threading
import time
import numpy as np

from object import *

#define object name
#environment
W = 0 #water
S = 1 #sand
G = 2 #ground
#animal
R = 3 #rabbit
F = 4 #fox
#food
Gr = 5 #grass
#define objects color
BLUE = (0,0,255)
SANDYELLOW = (194, 178, 128)
GROUNDGREEN = (124, 252, 0)
RABBITBROWN = (139, 69, 19)
FOXRED = (255, 99, 71)
GRASSGREEN = (0, 100, 0)

#link tiles to colors
TileColor = {W : BLUE,
            S : SANDYELLOW,
            G : GROUNDGREEN}

#link animal to color
AnimalColor = {R : RABBITBROWN,
               F : FOXRED}

FoodColor = {Gr: GRASSGREEN}
class MapData:
    def __init__(self):
        self.map = [
    [W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G],
    [W, W, W, W, W, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G],
    [W, W, S, S, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G],
    [W, S, S, S, W, W, W, W, W, W, W, S, S, S, G, G, G, G, G, G],
    [S, S, S, S, S, W, W, W, W, W, S, S, S, G, G, G, G, G, G, G],
    [S, S, G, G, S, S, S, S, S, S, S, G, G, G, G, G, G, G, G, G],
    [S, G, G, G, S, S, S, S, S, S, S, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, S, S, S, S, S, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G]
]
        self.tileSize = 30
        self.mapHeight = len(self.map)
        self.mapWidth = len(self.map[0])
        self.event = threading.Event()
        self.grassList = []

    def get_matrix(self):
        return self.map
    
    def get_food(self):
        return self.grassList
    
    def createMap(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.tileSize * self.mapWidth, self.tileSize * self.mapHeight))
        self.background = pygame.Surface((self.tileSize * self.mapWidth, self.tileSize * self.mapHeight))
        self.animal_layer = pygame.Surface((self.tileSize * self.mapWidth, self.tileSize * self.mapHeight), pygame.SRCALPHA)
        self.animal_layer.fill((0, 0, 0, 0))  # Fill with transparent black
        self.food_layer = pygame.Surface((self.tileSize * self.mapWidth, self.tileSize * self.mapHeight), pygame.SRCALPHA)
        self.food_layer.fill((0, 0, 0, 0))  # Fill with transparent black
        # create background
        self.display.fill((0, 0, 0))  # Clear screen with black or any color
        self.drawBackground()
        pygame.display.update()
        self.event.set()
        
        #spawnInitialFood
        self.spawnFood(number = 10)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Clear the display
            self.display.fill((0, 0, 0))  # Clear screen with black or any color
            self.display.blit(self.background, (0, 0))  # Draw the background
            self.display.blit(self.animal_layer, (0, 0))  # Draw the animal layer
            self.display.blit(self.food_layer, (0, 0))  # Draw the animal layer
            pygame.display.update()

    def drawBackground(self):
        for row in range(self.mapHeight):
            for col in range(self.mapWidth):
                pygame.draw.rect(self.background, TileColor[self.map[row][col]], \
                                    (col*self.tileSize, row*self.tileSize, self.tileSize, self.tileSize))
    
    def spawnAnimal(self, list): 
        from animal import Rabbit, Fox   
        for animal in list:
            # Calculate the position
            pos = (animal.x * self.tileSize + self.tileSize // 2,
                   animal.y * self.tileSize + self.tileSize // 2)
            if isinstance(animal, Rabbit):
                pygame.draw.circle(self.animal_layer, RABBITBROWN, pos, 8)
            elif isinstance(animal, Fox):
                pygame.draw.circle(self.animal_layer, FOXRED, pos, 10)  # Foxes could be bigger, for example

    def spawnFood(self, number=None):
        if number is None:
            while True:
                time.sleep(2)  # Wait for 3 seconds before executing the function
                self.createFood()
                
        else:
            for _ in range(number):
                self.createFood()

    def createFood(self):
        x, y = np.random.randint(0, self.mapHeight), np.random.randint(0, self.mapWidth)
        if self.map[x][y] == S or self.map[x][y] == G:
            pos = (x * self.tileSize + self.tileSize // 2,
                    y * self.tileSize + self.tileSize // 2)
            pygame.draw.circle(self.food_layer, GRASSGREEN, pos, 5)

            self.grassList.append(Grass(x,y)) #add grass to grass list
            
            
        