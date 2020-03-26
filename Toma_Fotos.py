import cv2
import uuid
import time
import os

Nombre = input("Nombre del nuevo usuario: ")

video = cv2.VideoCapture(0)
C = 0

direccion = 'D:/DECIMO/PAE/GIT/face-recognition/train_img/' + Nombre
dir = os.mkdir(direccion)

while True:

    ret, im = video.read()
    cv2.imshow('Busqueda de Rostro', im)
    nombre_foto = str(uuid.uuid4()) + ".jpg"
    cv2.imwrite(os.path.join(direccion, nombre_foto), im)
    cv2.imwrite("direccion/" + nombre_foto, im)
    print("foto tomada:{}".format(C))
    time.sleep(0.1)
    C = C + 1

    if C == 50:
        break