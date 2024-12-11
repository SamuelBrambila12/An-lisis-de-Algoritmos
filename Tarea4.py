# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:13:39 2024

@author: SamuelBrambila
"""
import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
imagenOriginal = cv.imread('ruido2.webp', 0)

# Obtener las dimensiones de la imagen (filas y columnas)
filas, columnas = np.shape(imagenOriginal)

# Crear una copia de la imagen para el resultado del filtro
imagenFiltrada = imagenOriginal.copy()

# Definimos el filtro con apoyo de una matriz
filtro_3x3 = np.zeros((3, 3), dtype=float)
for i in range(3):
    for j in range(3):
        # Asignar los valores dinámicamente
        if i == 1 and j == 1:
            filtro_3x3[i, j] = 0.5  # Centro
        elif (i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 2) or (i == 2 and j == 1):
            filtro_3x3[i, j] = 0.1  # Bordes
        else:
            filtro_3x3[i, j] = 0.025  # Esquinas

# Aplicar el filtro
for fila in range(1, filas-1):
    for columna in range(1, columnas-1):
        suma = 0
        # Recorrer la ventana 3x3
        for i in range(-1, 2):  # Fila de la ventana
            for j in range(-1, 2):  # Columna de la ventana
                valor_filtro = filtro_3x3[i+1, j+1]  # Valor del filtro 3x3 generado
                suma += imagenOriginal[fila+i, columna+j] * valor_filtro

        # Asignar el valor calculado, asegurando que esté en el rango [0, 255]
        imagenFiltrada[fila, columna] = suma

# Guardar las imágenes
cv.imwrite('imagen_original.png', imagenOriginal)
cv.imwrite('imagen_filtrada.png', imagenFiltrada)

# Mostrar la imagen original y la imagen filtrada
cv.imshow('imagen original', imagenOriginal)
cv.imshow('imagen filtrada', imagenFiltrada)
cv.waitKey(0)
cv.destroyAllWindows()
