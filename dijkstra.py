# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 08:42:26 2024

@author: SamuelBrambila
"""

import pygame as pg
import numpy as np

class MapaNode:
    def __init__(self,position,cost,parent=None):
        self.position=position
        self.cost=cost
        self.parent=parent
        
    def __eq__(self,other):
        return self.position[0]==other.position[0] and self.position[1]==other.position[1]
    
class Dijkstra(object):
    def run(self,mapa,start,end):
        mapa=mapa.astype(np.float64)
        
        unique, counts = np.unique(mapa, return_counts=True)
        nodosEnUno=counts[1]
        path=[]
        vectorOfVisited=[]
        vectorOfLabeled=[]
        mapaRows,mapaCols=np.shape(mapa)
        visited=np.zeros(mapa.shape)
        costs=np.zeros(mapa.shape)
        vectorOfLabeled.append(MapaNode(start[::-1],0))
        endNode=MapaNode(end[::-1],0)
        
        while(len(vectorOfVisited)!=nodosEnUno):
            currentNode=vectorOfLabeled.pop(0)
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
            """
            movements=[
                        [0,-1,1],
                        [-1,0,1],
                        [1,0,1],
                        [0,1,1]
                      ]
            """
            
            for movement in movements:
                #Creamos la posición del adjacente
                newPosition=[currentNode.position[0]+movement[0],currentNode.position[1]+movement[1]]
                adjacentNode=MapaNode(newPosition,currentNode.cost+movement[2],currentNode)
                #Revisamos que este dentro del mapa, que no haya sido visitado y que no sea obstaculo
                if newPosition[0]<0 or newPosition[1]<0 or newPosition[1]>=mapaCols or newPosition[0]>=mapaRows:
                    continue
                elif mapa[newPosition[0]][newPosition[1]]==0:
                    continue
                elif visited[newPosition[0]][newPosition[1]]==1:
                    continue
                else:
                    #Se busca en la lista de etiquetados
                    encontrado=False
                    for labeled in vectorOfLabeled:
                        if(labeled==adjacentNode):
                            encontrado=True
                            if(labeled.cost>adjacentNode.cost):
                                labeled.cost=adjacentNode.cost
                                costs[newPosition[0]][newPosition[1]]=adjacentNode.cost
                                labeled.parent=currentNode
                    if not encontrado:
                        #Agregamos el nodo a los etiquetados
                        vectorOfLabeled.append(adjacentNode)
                        costs[newPosition[0]][newPosition[1]]=adjacentNode.cost
            
            vectorOfVisited.append(currentNode)
            if(currentNode==endNode):
                break
            #Marcamos el nodo como visitado
            visited[currentNode.position[0]][currentNode.position[1]]=1
            vectorOfLabeled=sorted(vectorOfLabeled, key=lambda x: x.cost)
            
        #En reversa para obtener el camino
        #Buscar mi destino dentro de los nodos visitados
        for visitedNode in vectorOfVisited:
            if visitedNode==endNode:
                endNode=visitedNode
                break
        #Una vez encontrado el que se marcó como final, recorrer el grafo hacia atras siguiendo los padres
        while endNode is not None:
            path.append(endNode.position)
            endNode=endNode.parent
        return path, visited, costs
    
    
    
pg.init()
#Cargamos el archivo de numpy que contiene el mapa
mapaAlg=np.load('mapaProfundidad2.npy')
#Checamos el tamaño del mapa
width,height = mapaAlg.shape
#Definimos los colores
BLACK = pg.Color('black')
WHITE = pg.Color('white')
GREEN = pg.Color('green')
RED   = pg.Color('red')
BLUE  = pg.Color('blue')
# Light shade of the button
color_light = (170,170,170)
# Dark shade of the button
color_dark = (100,100,100)
smallfont = pg.font.SysFont('comicsans', 30)
text = smallfont.render('Search', True, RED)

# Tamaño en pixeles de la celda o el cuadro
tile_size = 10
# Punto inicial en formato columna,fila (x,y)
start = [0,17]
# Punto final en formato columna,fila (x,y)
goal = [25,14]
# Tamaño para el espacio para el boton
topPadding = 50
# Creo el objeto para la busqueda con Dijkstra
search = Dijkstra()

# El tamaño del mapa debe tener la ventana por eso es el tamaño del mapa por el tamaño de los cuadros
screen = pg.display.set_mode((width*tile_size, height*tile_size+topPadding))

# Espacio para el mapa
background = pg.Surface((width*tile_size, height*tile_size))
# Esapcio para el boton
buttons = pg.Surface((width*tile_size, 50))

# Dibujamos los cuadros del mapa
for y in range(0, height):
    for x in range(0, width):
        rect = (x*tile_size, y*tile_size, tile_size, tile_size)
        if(mapaAlg[y,x]==0):
            color=BLACK
        else:
            color=WHITE
        if x==start[0] and y==start[1]:
            color=GREEN
        if x==goal[0] and y==goal[1]:
            color=RED
        pg.draw.rect(background, color, rect)
        
#Aquí es la ejecución del "Juego"
game_exit = False
while not game_exit:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            
            if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40:
                camino,mapavisited,costos=search.run(mapaAlg,start,goal)
                for point in camino:
                    rect = (point[1]*tile_size, point[0]*tile_size, tile_size, tile_size)
                    pg.draw.rect(background, BLUE, rect)
                    
                    
                    
    #Cuando el mouse esta sobre las coordenadas del boton le cambiamos el color a unos gris bajito
    if 0 <= mouse[0] <= 140 and 10 <= mouse[1] <= 40:
        pg.draw.rect(buttons,color_light,[10,10,140,30])
    
    else:
        pg.draw.rect(buttons,color_dark,[10,10,140,30])
    
    screen.fill((0,0,0))
    
    screen.blit(buttons, (0,0))
    screen.blit(background, (0,50))
    screen.blit(text, (10,10))
    pg.display.flip()
pg.display.quit()
    