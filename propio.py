
import cv2
import matplotlib.pyplot as plt
import numpy as np
import uuid


cap = cv2.VideoCapture(0)
leido, frame = cap.read()

if leido == True:
    nombre_foto = str(uuid.uuid4()) + ".jpg"    # nombre aleatorio
    cv2.imwrite(nombre_foto, frame)             # captura de foto
    print("Foto tomada correctamente con el nombre {}".format(nombre_foto))

else:
    print("Error al tomar la fotografia")

cv2.waitKey(0)
cap.release()





img = cv2.imread(nombre_foto)      # leemos un frame y lo guardamos

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convertimos la imagen a blanco y negro
faces = face_cascade.detectMultiScale(gray, 1.3, 5) #buscamos las coordenadas de los rostros (si los hay) y guardamos su posicion

# Dibujamos un rectangulo en las coordenadas de cada rostro
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

# Mostramos la imagen
# cv2.imshow('img', img)
# Espera una tecla para salir del programa
# cv2.waitKey()

#Recorta el rostro detectado
crop_img = img[y:y+h, x:x+w] # Crop from x, y, w, h, NOTE: its img[y: y + h, x: x + w]
#cv2.imshow('rostro', crop_img)
#cv2.waitKey(0)





#Guarda la imagen del rostro
cv2.imwrite('C:/Users/daniel/PycharmProjects/untitled/Caras/Deteccion.jpg', crop_img)