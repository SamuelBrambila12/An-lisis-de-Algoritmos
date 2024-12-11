import cv2
import numpy as np

# Cargar la imagen en escala de grises
imagen = cv2.imread('arboles.jpg', cv2.IMREAD_GRAYSCALE)

# Obtener las dimensiones de la imagen
filas, columnas = imagen.shape

# Calcular el tamaño de las secciones de la cuadrícula 3x3
cuadrilla_filas = filas // 3
cuadrilla_columnas = columnas // 3

# Crear una copia de la imagen para almacenar el resultado filtrado
imagen_filtrada = np.zeros_like(imagen, dtype=np.float32)

# Definir propiedades del texto
color_texto = (255)  # Color blanco para el texto
fuente = cv2.FONT_HERSHEY_SIMPLEX
tamaño_fuente = 1
grosor_fuente = 2

# Recorrer las 9 secciones de la imagen y aplicar el filtro
for i in range(3):  # Para las 3 filas de secciones
    for j in range(3):  # Para las 3 columnas de secciones
        # Calcular el rango de la sección actual
        if i == 2:  # Última fila
            fin_fila = filas  # Hasta el final de la imagen
        else:
            fin_fila = (i + 1) * cuadrilla_filas

        if j == 2:  # Última columna
            fin_columna = columnas  # Hasta el final de la imagen
        else:
            fin_columna = (j + 1) * cuadrilla_columnas

        inicio_fila = i * cuadrilla_filas
        inicio_columna = j * cuadrilla_columnas

        # Obtener la sección de la imagen correspondiente
        seccion = imagen[inicio_fila:fin_fila, inicio_columna:fin_columna]

        # Determinar el valor del filtro basado en la posición (i, j)
        if j == 0:  # Columna izquierda
            if i == 1:  # Fila central
                valor = -0.5
            else:
                valor = -0.2
        elif j == 1:  # Columna central
            valor = 0
        else:  # Columna derecha
            if i == 1:  # Fila central
                valor = 0.5
            else:
                valor = 0.2

        # Aplicar el valor del filtro a la sección
        seccion_filtrada = seccion * abs(valor)

        # Almacenar la sección filtrada en la imagen de salida
        imagen_filtrada[inicio_fila:fin_fila, inicio_columna:fin_columna] = seccion_filtrada

# Convertir a un rango de valores válidos (0-255)
imagen_filtrada_limpia = np.clip(imagen_filtrada, 0, 255).astype(np.uint8)

# Guardar la imagen filtrada sin cuadrícula ni valores
cv2.imwrite('imagen_filtrada_sin_cuadricula_valores.jpg', imagen_filtrada_limpia)

# Ahora añadimos la cuadrícula y los valores en una copia de la imagen filtrada
imagen_filtrada_con_cuadricula = imagen_filtrada_limpia.copy()

# Dibujar las líneas de la cuadrícula en la imagen filtrada con cuadrícula y texto
color_linea = (255)  # Color blanco para las líneas de la cuadrícula

# Dibujar las líneas horizontales
for i in range(1, 3):
    cv2.line(imagen_filtrada_con_cuadricula, (0, i * cuadrilla_filas), (columnas, i * cuadrilla_filas), color_linea, 2)

# Dibujar las líneas verticales
for j in range(1, 3):
    cv2.line(imagen_filtrada_con_cuadricula, (j * cuadrilla_columnas, 0), (j * cuadrilla_columnas, filas), color_linea, 2)

# Dibujar los valores del filtro en el centro de cada sección
for i in range(3):
    for j in range(3):
        # Determinar el valor del filtro
        if j == 0:
            if i == 1:
                valor = -0.5
            else:
                valor = -0.2
        elif j == 1:
            valor = 0
        else:
            if i == 1:
                valor = 0.5
            else:
                valor = 0.2

        # Calcular el rango de la sección actual
        if i == 2:
            fin_fila = filas
        else:
            fin_fila = (i + 1) * cuadrilla_filas

        if j == 2:
            fin_columna = columnas
        else:
            fin_columna = (j + 1) * cuadrilla_columnas

        inicio_fila = i * cuadrilla_filas
        inicio_columna = j * cuadrilla_columnas

        # Calcular el centro de la sección para posicionar el texto
        centro_fila = inicio_fila + (fin_fila - inicio_fila) // 2
        centro_columna = inicio_columna + (fin_columna - inicio_columna) // 2

        # Dibujar el valor del filtro en el centro de la sección
        texto = f'{abs(valor):.1f}'  # Redondear el valor del filtro a un decimal
        cv2.putText(imagen_filtrada_con_cuadricula, texto, (centro_columna - 20, centro_fila + 10), 
                    fuente, tamaño_fuente, color_texto, grosor_fuente, cv2.LINE_AA)

# Mostrar el resultado
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen filtrada con valores y cuadrícula 3x3', imagen_filtrada_con_cuadricula)

# Guardar la imagen filtrada con cuadrícula y valores
cv2.imwrite('imagen_filtrada_con_cuadricula_y_valores.jpg', imagen_filtrada_con_cuadricula)

# Esperar a que se cierre la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()
