import numpy as np
import cv2

# cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)

while (True):

    frame, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (125, 255, 0), 2)

    # Mostramos la imagen
    cv2.imshow('img', img)

    # con la tecla 'q' salimos del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('C:/Users/daniel/PycharmProjects/untitled/Fotos/prueba.jpg', frame)
        break
cap.release()
cv2.destroyAllWindows()