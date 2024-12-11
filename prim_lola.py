import cv2
import numpy as np
import random as rd

nombreMapa="Chiquito"
#para cargar el mapa
mapa=cv2.imread('mapa'+nombreMapa+'.png')
# Para cargar la lista de indices
vertices=np.load("verticeMapa"+nombreMapa+".npy")
#pasamos la imagen a escala de grises
gray = cv2.cvtColor(mapa,cv2.COLOR_BGR2GRAY)
#muestro la imagen en escala de grises
#cv2.imshow('mapa3',gray)
#obtengo un binarizacion en blanco de todos lo pixeles cuyo valor sea entre 254 y 2555
ret,th1 = cv2.threshold(gray,254,255,cv2.THRESH_BINARY)
kernel = np.ones((11,11), np.uint8) 
#aplico un filtro de dilatacion. Este filtro hace que los puntos blancos se expandan 
#probocando que algunos puntitos negros desaparecan #le pueden hacer un cv.imshow para que vean el resultado
th1 = cv2.dilate(th1,kernel,1)
#cv2.imshow('th1', th1) #-------------------------
kernel = np.ones((11,11), np.uint8) 
#cv2.imshow('kernel', kernel) #-------------------------
#Despues aplico uno de erosion que hace lo opuesto al de dilatacion
th1 = cv2.erode(th1,kernel,1)
#cv2.imshow('th1_2', th1) #-------------------------------
#aplico un flitro gausiando de 5x5  para suavisar los bordes 
th1 = cv2.GaussianBlur(th1,(5,5),cv2.BORDER_DEFAULT)
#binariso la imagen
ret,th2 = cv2.threshold(th1,235,255,cv2.THRESH_BINARY)
th2 = cv2.dilate(th2,kernel,1)
th2 = cv2.cvtColor(th2,cv2.COLOR_GRAY2BGR)

aristas = []

for verticeA in vertices:
    cv2.circle(th2, (verticeA[1], verticeA[0]), 6, (255, 0, 0), -1)
    for verticeB in vertices:
        if not np.array_equal(verticeA, verticeB):  # Verifica que no sean vertices iguales
            x1, y1 = verticeA[1], verticeA[0]
            x2, y2 = verticeB[1], verticeB[0]
                        
            ban = False
            for i in range(1, 12):
                half_x = int(x1 + i * (x2 - x1) / 12)
                half_y = int(y1 + i * (y2 - y1) / 12)
                
                peso = np.sqrt((half_x - x1) ** 2 + (half_y - y1) ** 2)
                #peso = "{:.2f}".format(peso)
                
                # Verificamos si el punto medio y los vértices son negros
               # if np.all(th2[medio[i-1][1], medio[i-1][0]] == 0) or np.all(th2[verticeA[0], verticeA[1]] == 0) or np.all(th2[verticeB[0], verticeB[1]] == 0):
                if np.all(th2[half_y,half_x,0] == 0): 
                    ban = True
                    break

            # Si la bandera sigue siendo True después de verificar todos los puntos intermedios, agregamos la arista a la lista
            if not ban:
                aristas.append(((int(verticeA[1]), int(verticeA[0])), (int(verticeB[1]), int(verticeB[0])), peso))

aristas.sort(key=lambda aristas: aristas[2])
# for ar in aristas:
#     cv2.line(th2, ar[0], ar[1], (255, 255, 0), 3)
    #print (ar)
#cv2.imshow('aristas',th2) 
                
# Implementar el algoritmo de Prim para encontrar el árbol de expansión mínima
num_vertices = len(vertices)
visited = [] 
visited.append(aristas[0][0])
num_visited = 0  # Número de vértices visitados
grafoPrim = []
bandera = True

while num_visited < num_vertices and bandera:
    bandera = False
    for a in aristas:
        v1, v2, p = a
    
        if v1 in visited and not v2 in visited: #a[0][:] not in visited and not a[1][:]:
            visited.append(v2)
            grafoPrim.append(a)
            num_visited += 1
            bandera = True
            break
            
        if v2 in visited and not v1 in visited: #a[0][:] not in visited and not a[1][:]:
            visited.append(v1)
            grafoPrim.append(a)
            num_visited += 1
            bandera = True
            break

# # Dibuja el árbol de expansión mínima
for arista in grafoPrim:
    v1, v2, peso = arista
    cv2.circle(mapa, v1, 6, (255, 0, 0), -1)
    cv2.line(mapa, v1, v2, (255, 255, 0), 3)
    cv2.circle(mapa, v2, 6, (255, 0, 0), -1)
    cv2.line(th2, v1, v2, (255, 255, 0), 3)
    
cv2.imshow('thres2',th2)
cv2.imshow('Prim', mapa)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Acuerdense que las funciones de opencv esperan x y
# y las de arreeglos esperan fila columna

