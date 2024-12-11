# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:47:46 2024

@author: SamuelBrambila
"""

import cv2 as cv
import numpy as np

# Función para detectar el color predominante en una región del video
def detectar_color_predominante(frame):

    # Seleccionar una región de la esquina superior derecha
    frame_width = frame.shape[1]
    region = frame[0:100, frame_width-100:frame_width]

    # Redimensionar la región para acelerar el procesamiento
    region = cv.resize(region, (50, 50))

    # Convertir la región a una lista de colores
    pixels = np.reshape(region, (-1, 3))

    # Encontrar el color promedio de la región (puede ser una aproximación)
    color_promedio = np.mean(pixels, axis=0)

    # Redondear los valores para tener valores enteros en RGB
    color_promedio = np.round(color_promedio).astype(int)
    
    return color_promedio

# Función para obtener la máscara de color a partir de los límites
def obtener_mascara_color(frame, color_predominante, tolerancia):
    # Generar los límites inferior y superior para el rango de color
    lower_thresh = np.clip(color_predominante - tolerancia, 0, 255)
    upper_thresh = np.clip(color_predominante + tolerancia, 0, 255)
    
    # Crear una máscara basada en ese rango
    mask_color = cv.inRange(frame, lower_thresh, upper_thresh)
    mask_inv = cv.bitwise_not(mask_color)
    return mask_color, mask_inv

# Abrir webcam (video 0)
video_webcam = cv.VideoCapture(0)

# Abrir video desde el archivo
video_archivo = cv.VideoCapture('video.mp4')

# Definir el codec y crear los objetos VideoWriter para guardar los videos
fourcc = cv.VideoWriter_fourcc(*'mp4v')

# Obtener la tasa de FPS original de los videos
fps_webcam = video_webcam.get(cv.CAP_PROP_FPS)
fps_video = video_archivo.get(cv.CAP_PROP_FPS)

# Establecer las medidas de los videos para evitar cualquier problema por dimensiones diferentes
frame_width, frame_height = 640, 480

# Crear objeto VideoWriter para guardar el video final en mp4
out_resultado_final = cv.VideoWriter('resultado_final.mp4', fourcc, fps_video, (frame_width, frame_height))


# Banderas para guardar solo una imagen por tipo de video (webcam original, sin fondo, etc.)
webcam_saved = False
foreground_saved = False
background_saved = False
resultado_final_saved = False

while video_webcam.isOpened() and video_archivo.isOpened():
    ret_webcam, frame_webcam = video_webcam.read()
    ret_video, frame_video = video_archivo.read()

    if not ret_webcam or not ret_video:
        print("Error capturando video o se ha terminado el video.")
        break

    # Redimensionar para que ambos videos tengan el mismo tamaño
    frame_webcam = cv.resize(frame_webcam, (frame_width, frame_height))
    frame_video = cv.resize(frame_video, (frame_width, frame_height))

    # Detectar el color predominante en la región de la esquina superior izquierda del fondo
    color_predominante = detectar_color_predominante(frame_webcam)

    # Obtener la máscara para eliminar el fondo con base en el color predominante
    mask_color, mask_inv = obtener_mascara_color(frame_webcam, color_predominante, tolerancia=52)

    # Aplicar la máscara para eliminar el fondo del video de la webcam
    foreground_webcam = cv.bitwise_and(frame_webcam, frame_webcam, mask=mask_inv)

    # Aplicar la máscara inversa para usar el fondo del video del archivo
    background_video = cv.bitwise_and(frame_video, frame_video, mask=mask_color)

    # Combinar los resultados
    total = cv.add(foreground_webcam, background_video)

    # Mostrar resultados
    cv.imshow('Webcam original', frame_webcam)          # Mostrar la webcam original
    cv.imshow('Webcam sin fondo', foreground_webcam)    # Mostrar la webcam sin el fondo detectado
    cv.imshow('Video de fondo', frame_video)            # Mostrar el video que sirve como fondo
    cv.imshow('Resultado final', total)                 # Mostrar el resultado final con la combinación

    # Guardar una sola imagen por tipo de video, esto es más que nada para evidencias del reporte
    if not webcam_saved:
        cv.imwrite('webcam_frame.png', frame_webcam)
        webcam_saved = True

    if not foreground_saved:
        cv.imwrite('foreground_webcam_frame.png', foreground_webcam)
        foreground_saved = True

    if not background_saved:
        cv.imwrite('background_video_frame.png', frame_video)
        background_saved = True

    if not resultado_final_saved:
        cv.imwrite('resultado_final_frame.png', total)
        resultado_final_saved = True

    # Guardar los frames en el archivo final
    out_resultado_final.write(total)   # Este es el video que se subirá a Youtube como evidencia

    # Presionar 'q' para salir o espera 30 segundos para dejar de capturar
    if cv.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar recursos
video_webcam.release()
video_archivo.release()
out_resultado_final.release()
cv.destroyAllWindows()