# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:55:57 2024

@author: SamuelBrambila
"""

import pygame as pg
import numpy as np
from collections import deque

class MapaNode:
    def __init__(self, position, parent=None):
        self.parent = parent
        self.position = position
    
    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

class busqueda_amplitud(object):  # Cambio a búsqueda en amplitud
    def run(self, mapa, start, end):
        startNode = MapaNode(start[::-1])
        endNode = MapaNode(end[::-1])
        path = []
        queue = deque()  # Usamos una cola
        queue.append(startNode)
        mapaRows, mapaCols = np.shape(mapa)
        visited = np.zeros(mapa.shape)
        visited[startNode.position[0]][startNode.position[1]] = 1

        while queue:
            currentNode = queue.popleft()  # Usamos popleft para sacar de la cola
            if currentNode == endNode:
                break
            #-------------
            #|1.4| 1 |1.4|
            #| 1 | c | 1 |
            #|1.4| 1 |1.4|
            #-------------
            
            movements=[[-1,-1,1.4],
                       [0,-1,1],
                       [1,-1,1.4],
                       [-1,0,1],
                       [1,0,1],
                       [-1,1,1.4],
                       [0,1,1],
                       [1,1,1.4]
                       ]
            
            movements = [
                [0, -1, 1],  
                [-1, 0, 1],  
                [1, 0, 1],  
                [0, 1, 1]    
            ]
            
            for movement in movements:
                newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
                
                # Verificamos que la nueva posición esté dentro del mapa y que sea un espacio libre
                if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[1] >= mapaCols or newPosition[0] >= mapaRows:
                    continue
                elif visited[newPosition[0]][newPosition[1]] == 1:
                    continue
                elif mapa[newPosition[0]][newPosition[1]] == 0:
                    continue
                else:
                    adjacentNode = MapaNode(newPosition, currentNode)
                    queue.append(adjacentNode)
                    visited[newPosition[0]][newPosition[1]] = 1
        
        # Obtenemos el camino
        while currentNode is not None:
            path.append(currentNode.position)
            currentNode = currentNode.parent

        return path, visited

# El resto del código permanece igual para el manejo de Pygame y la interfaz.
pg.init()
mapaAlg = np.load('mapaProfundidad2.npy')
height, width = mapaAlg.shape
BLACK = pg.Color('black')
WHITE = pg.Color('white')
GREEN = pg.Color('green')
RED = pg.Color('red')
BLUE = pg.Color('blue')

color_light = (170,170,170)
color_dark = (100,100,100)
smallfont = pg.font.SysFont('tahoma', 30)
text = smallfont.render('Search', True, RED)
tile_size = 10
start = [59, 44] # Cambiamos la coordenada de inicio
goal = [5, 30]
topPadding = 50

search = busqueda_amplitud()  # Instanciamos la nueva búsqueda en amplitud
screen = pg.display.set_mode((width * tile_size, height * tile_size + topPadding))
clock = pg.time.Clock()
background = pg.Surface((width * tile_size, height * tile_size))
buttons = pg.Surface((width * tile_size, topPadding))

for y in range(0, height):
    for x in range(0, width):
        rect = (x * tile_size, y * tile_size, tile_size, tile_size)
        if mapaAlg[y, x] == 0:
            color = BLACK
        else:
            color = WHITE
        if x == start[0] and y == start[1]:
            color = GREEN
        if x == goal[0] and y == goal[1]:
            color = RED
        pg.draw.rect(background, color, rect)

game_exit = False
while not game_exit:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40:
                camino, mapavisited = search.run(mapaAlg, start, goal)
                for point in camino:
                    rect = (point[1] * tile_size, point[0] * tile_size, tile_size, tile_size)
                    pg.draw.rect(background, BLUE, rect)

    if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40:
        pg.draw.rect(buttons, color_light, [10, 10, 140, 30])
    else:
        pg.draw.rect(buttons, color_dark, [10, 10, 140, 30])

    screen.fill((0, 0, 0))
    screen.blit(buttons, (0, 0))
    screen.blit(background, (0, 50))
    screen.blit(text, (10, 10))
    pg.display.flip()
    clock.tick(30)

pg.display.quit()
