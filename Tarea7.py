import cv2 as cv

# Cargar los archivos PNG (sombrero y bigote)
sombrero = cv.imread("sombrero.png", cv.IMREAD_UNCHANGED)
bigote = cv.imread("bigote.png", cv.IMREAD_UNCHANGED)

# Cargar clasificadores
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv.CascadeClassifier("haarcascade_smile.xml")  # Usamos el clasificador de sonrisas para colocar el bigote

# Obtener acceso a la webcam
video_capture = cv.VideoCapture(0)

# Configuración para grabar el video
fourcc = cv.VideoWriter_fourcc(*'XVID')  # Codec para el video
out = cv.VideoWriter('video_filtro.avi', fourcc, 20.0, (640, 480))

# Función para superponer la imagen PNG
def superponer_png(fondo, overlay, x, y, w, h):
    overlay_resized = cv.resize(overlay, (w, h))  # Redimensionar el PNG
    for i in range(h):
        for j in range(w):
            if y + i < fondo.shape[0] and x + j < fondo.shape[1]:
                if overlay_resized[i, j][3] != 0:  # Verificar el canal alfa
                    fondo[y + i, x + j] = overlay_resized[i, j][:3]  # Superponer si no es transparente

while True:
    ret, frame = video_capture.read()
    frame = cv.flip(frame, 1)
    imagenGrises = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros
    faces = face_cascade.detectMultiScale(imagenGrises, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Calcular el centro del rostro para centrar el sombrero
        face_center_x = x + w // 2

        # Ajustar el tamaño del sombrero dinámicamente en función del ancho del rostro
        sombrero_width = int(1.2 * w)
        sombrero_height = int(0.8 * h)

        # Calcular la nueva posición para centrar el sombrero sobre la cabeza
        sombrero_x = face_center_x - sombrero_width // 2
        sombrero_y = y - int(0.65 * h)

        # Superponer el sombrero
        superponer_png(frame, sombrero, sombrero_x, sombrero_y, sombrero_width, sombrero_height)

        # Detectar sonrisas (aproximación para la boca)
        roi_gris = imagenGrises[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        sonrisas = smile_cascade.detectMultiScale(roi_gris, scaleFactor=1.3, minNeighbors=22, minSize=(25, 25))
        if len(sonrisas) > 0:
            (sx, sy, sw, sh) = sonrisas[0]
            bigote_height = int(sw * 0.5)  # Determinar la altura del bigote basado en su ancho
            # Ajustar la posición vertical para que el bigote esté justo sobre la sonrisa
            superponer_png(roi_color, bigote, sx, sy - int(bigote_height / 2) + 10, sw, bigote_height)

    # Guardar el frame en el video de salida
    out.write(frame)

    # Mostrar la imagen
    cv.imshow('Video', frame)

    # Salir al presionar 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
video_capture.release()
out.release()
cv.destroyAllWindows()
