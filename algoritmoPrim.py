import cv2
import numpy as np
import random

nombreMapa = "1"
mapa = cv2.imread('mapa' + nombreMapa + '.png')
vertices = np.load("verticeMapa" + nombreMapa + ".npy")
gray = cv2.cvtColor(mapa, cv2.COLOR_BGR2GRAY)
cv2.imshow('mapa3', gray)

ret, th1 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
kernel = np.ones((11, 11), np.uint8)
th1 = cv2.dilate(th1, kernel, 1)
th1 = cv2.erode(th1, kernel, 1)
th1 = cv2.GaussianBlur(th1, (5, 5), cv2.BORDER_DEFAULT)
ret, th2 = cv2.threshold(th1, 235, 255, cv2.THRESH_BINARY)
th2 = cv2.dilate(th2, kernel, 1)
th2 = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)


# Carga la imagen binaria del grafo
#grafo_binario = cv2.imread('grafo_binario.png', cv2.IMREAD_GRAYSCALE)

# Encuentra las coordenadas de los píxeles blancos (aristas)
aristas = np.column_stack(np.where(th2 == 255))

# Crea un diccionario para representar el grafo con sus pesos
grafo = {}
for i in range(aristas.shape[0]):
    for j in range(i + 1, aristas.shape[0]):
        x1, y1 = aristas[i][:2]
        x2, y2 = aristas[j][:2]
        distancia = np.linalg.norm(np.array((x1, y1)) - np.array((x2, y2)))
        if (x2, y2) not in grafo:
            grafo[(x2, y2)] = [(x1, y1, distancia)]
        else:
            grafo[(x2, y2)].append((x1, y1, distancia))
        if (x1, y1) not in grafo:
            grafo[(x1, y1)] = [(x2, y2, distancia)]
        else:
            grafo[(x1, y1)].append((x2, y2, distancia))

# Algoritmo de Prim
def prim(grafo):
    arbol_minimo = {}
    visitados = set()

    # Elije un nodo inicial arbitrario
    inicio = list(grafo.keys())[0]
    visitados.add(inicio)

    while len(visitados) < len(grafo):
        arista_minima = None

        for nodo in visitados:
            vecinos = grafo[nodo]
            for vecino, distancia in vecinos:
                if vecino not in visitados and (
                    arista_minima is None or distancia < arista_minima[2]
                ):
                    arista_minima = (nodo, vecino, distancia)

        if arista_minima:
            origen, destino, distancia = arista_minima
            visitados.add(destino)
            if origen not in arbol_minimo:
                arbol_minimo[origen] = [(destino, distancia)]
            else:
                arbol_minimo[origen].append((destino, distancia))
            if destino not in arbol_minimo:
                arbol_minimo[destino] = [(origen, distancia)]
            else:
                arbol_minimo[destino].append((origen, distancia))

    return arbol_minimo

# Encuentra el árbol de expansión mínima
arbol_minimo = prim(grafo)

# Dibuja las aristas del árbol de expansión mínima
resultado = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
for origen, vecinos in arbol_minimo.items():
    for destino, distancia in vecinos:
        cv2.line(resultado, origen, destino, (0, 255, 0), 2)

cv2.imshow('asfe', th2)
cv2.waitKey(0)
cv2.destroyAllWindows()
