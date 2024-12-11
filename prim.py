import cv2
import numpy as np

# Nombre del mapa
nombreMapa = "3"

# Cargar la imagen del mapa (formato PNG) y los índices de los vértices (archivo .npy)
mapa = cv2.imread('mapa' + nombreMapa + '.png')
vertices = np.load("verticeMapa" + nombreMapa + ".npy")

# Convertir la imagen a escala de grises para facilitar su procesamiento
gray = cv2.cvtColor(mapa, cv2.COLOR_BGR2GRAY)

# Mostrar la imagen en escala de grises
cv2.imshow('mapa'+nombreMapa, gray)
cv2.imwrite('Mapa_Grises_'+nombreMapa+'.png', gray)  # Guardar la imagen en escala de grises

# Binarización de la imagen: los píxeles entre 254 y 255 se hacen blancos (255), el resto se vuelve negro (0)
ret, th1 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

# Crear un kernel de 11x11 para las operaciones de dilatación y erosión. Este es un bloque de unos que se usará para aplicar estos filtros.
kernel = np.ones((11, 11), np.uint8)

# Aplicar dilatación: expande las áreas blancas
th1 = cv2.dilate(th1, kernel, 1)

# Aplicar erosión: reduce las áreas blancas, devolviendo su tamaño después de la dilatación
th1 = cv2.erode(th1, kernel, 1)

# Aplicar filtro Gaussiano para suavizar los bordes de la imagen (reduce ruido)
th1 = cv2.GaussianBlur(th1, (5, 5), cv2.BORDER_DEFAULT)

# Segunda binarización: ajusta los niveles para asegurar que los píxeles importantes sean claramente blancos o negros
ret, th2 = cv2.threshold(th1, 235, 255, cv2.THRESH_BINARY)

# Aplicar dilatación de nuevo para asegurar que no queden pequeños agujeros (pequeñas áreas negras que aparecen dentro de regiones blancas)
th2 = cv2.dilate(th2, kernel, 1)

# Convertir la imagen binarizada de escala de grises a formato de 3 canales de color (BGR) para poder dibujar colores en ella
th2 = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)

# Dibujar los vértices en ambos mapas (en azul: color (255, 0, 0))
# cv2.circle dibuja un círculo en la imagen, donde:
# - El primer argumento es la imagen,
# - El segundo es la posición (x, y),
# - El tercero es el radio del círculo,
# - El cuarto es el color en formato BGR,
# - El último argumento indica el grosor del borde (-1 lo rellena).
for vertice in vertices:
    cv2.circle(th2, (vertice[1], vertice[0]), 3, (255, 0, 0), -1)
    cv2.circle(mapa, (vertice[1], vertice[0]), 3, (255, 0, 0), -1)

# Mostrar la imagen binarizada con los vértices
cv2.imshow('thres2', th2)
cv2.imwrite('Mapa_Binarizado_Vertices_'+nombreMapa+'.png', th2)  # Guardar la imagen binarizada con los vértices

# Crear una lista de aristas con sus pesos. Cada arista conecta dos vértices.
aristas = []

# Comparar cada vértice con los demás para calcular las distancias y crear aristas
for i, verticeA in enumerate(vertices):
    for j, verticeB in enumerate(vertices):
        if i != j:  # Evitar comparar un vértice consigo mismo
            x1, y1 = verticeA[1], verticeA[0]
            x2, y2 = verticeB[1], verticeB[0]
            peso = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Calcular la distancia entre dos vértices (peso de la arista)
            # (x1,y1) son las coordenadas del vértice A y (x2,y2) las coordenadas del vértice B

            # Verificar si no hay obstáculos (píxeles negros) entre los dos vértices
            ban = False
            for k in range(1, 12):  # Dividir el camino en 12 segmentos y revisar puntos intermedios
                half_x = int(x1 + k * (x2 - x1) / 12)
                half_y = int(y1 + k * (y2 - y1) / 12)

                # Si encontramos un píxel negro (obstáculo), marcar la arista como inválida
                if np.all(th2[half_y, half_x, 0] == 0):  # Comprobar si el píxel es negro
                    ban = True
                    break

            if not ban:  # Si no hay obstáculos, añadir la arista a la lista
                aristas.append(((x1, y1), (x2, y2), peso))

# Ordenar las aristas por peso (de menor a mayor)
aristas.sort(key=lambda arista: arista[2])

# Implementación del algoritmo de Prim para encontrar el Árbol de Expansión Mínima (MST)
num_vertices = len(vertices)
visited = [False] * num_vertices  # Lista para marcar los vértices visitados
grafoPrim = []  # Lista para almacenar las aristas del MST
visited[0] = True  # Comenzar desde el primer vértice (marcado como visitado)
conectados = 1  # Contador de vértices conectados al MST

# Ejecutar Prim hasta que todos los vértices estén conectados
while conectados < num_vertices:
    menor_peso = float('inf')
    mejor_arista = None
    vertice_no_visitado = None

    # Buscar la arista de menor peso que conecte un vértice visitado con uno no visitado
    for arista in aristas:
        v1, v2, peso = arista

        for i, verticeA in enumerate(vertices):
            # Si uno de los vértices está visitado y el otro no, considerar la arista
            if (v1 == (verticeA[1], verticeA[0]) and visited[i]) or (v2 == (verticeA[1], verticeA[0]) and visited[i]):
                for j, verticeB in enumerate(vertices):
                    if (v2 == (verticeB[1], verticeB[0]) and not visited[j]) or (v1 == (verticeB[1], verticeB[0]) and not visited[j]):
                        # Elegir la arista de menor peso
                        if peso < menor_peso:
                            menor_peso = peso
                            mejor_arista = arista
                            vertice_no_visitado = j

    # Añadir la mejor arista al MST y marcar el vértice como visitado
    if mejor_arista:
        grafoPrim.append(mejor_arista)
        visited[vertice_no_visitado] = True
        conectados += 1

# Dibujar las aristas del Árbol de Expansión Mínima (MST) en ambas imágenes
for arista in grafoPrim:
    v1, v2, _ = arista
    cv2.line(mapa, v1, v2, (255, 255, 0), 3)  # Dibujar la línea en el mapa original
    cv2.line(th2, v1, v2, (255, 255, 0), 3)  # Dibujar la línea en el mapa binarizado

# Mostrar las imágenes con las aristas del MST
cv2.imshow('Mapa con MST - Original', mapa)
cv2.imshow('Mapa con MST - Binarizado', th2)

# Guardar las imágenes resultantes
cv2.imwrite('Mapa_Original_MST_'+nombreMapa+'.png', mapa)
cv2.imwrite('Mapa_Binarizado_MST_'+nombreMapa+'.png', th2)

# Esperar indefinidamente hasta que el usuario presione una tecla
# El argumento '0' indica que esperará sin límite de tiempo
cv2.waitKey(0)

# Cerrar todas las ventanas de imágenes
cv2.destroyAllWindows()
