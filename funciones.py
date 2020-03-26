import cv2
import uuid
import time
import os

C = "C"
D = "D"

def conocido():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    video = cv2.VideoCapture(0)

    x = 0
    y = 0
    h = 0
    w = 0

    while True:
        ret,im = video.read()
        faces = face_cascade.detectMultiScale(im, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (125, 255, 0), 2)
            cv2.imwrite('/home/elkin/Documents/Facenet', im)
            img = cv2.imread('/home/elkin/Documents/Facenet/Captura.jpg')
            crop_img = img[y:y + h, x:x + w]
            cv2.imwrite('/home/elkin/Documents/Facenet/Deteccion.jpg', crop_img)

        cv2.imshow('Busqueda de Rostro',im)

        tecla = cv2.waitKey(10)
        if tecla == 27:
            break

def desconocido():
    Nombre = input("Nombre del nuevo usuario: ")

    video = cv2.VideoCapture(0)
    C = 0

    direccion = '/home/elkin/Documents/Facenet/' + Nombre
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

print("ingrese la categoria del usuario")
Usuario = input("Usuario conocido [C] Usuario desconocido [D]: ")

if (Usuario == C):
    conocido()
elif (Usuario == D):
    desconocido()
else:
    print("invalido")
