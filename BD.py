#Informacion de los usuarios guardados en un diccionario.
import time
from pymongo import MongoClient
import easygui
#import pymongo
import cv2
import uuid
import os

mc = MongoClient('mongodb://admin:Suntrack_1m2@54.187.31.198:27017')
db = mc.usuarios
    
Usuario = {}


print("INGRESE LOS SIGUIENTES DATOS")

while True:
    
    Cedula = input("Cedula: ")
    Nombre = input("Nombre: ")
    Edad = input("Edad: ")
    
    while True:
        
        print(" si es ESTUDIANTE digite [1] \n si es PROFESOR digite   [2] \n si es EGRESADO digite   [3] \n si es EMPLEADO digite   [4]")
        Cargo = input("Cargo: ")
        
        if "1"<= Cargo <= "4":
            break
        else:
            print("Digite un valor valido")
            
    if Cargo == "1":
        Cargo = "Estudiante"
    if Cargo == "2":
        Cargo = "Profesor"
    if Cargo == "3":
        Cargo = "Egresado"
    if Cargo == "4":
        Cargo = "Empleado"
    
    Fecha = time.strftime("%x")
    Hora = time.strftime("%X")
    

    #Usuario = {Nombre:{"Edad": Edad, "Cargo": Cargo, "Hora": Hora}}
    Usuario["Cedula"] = Cedula
    Usuario["Nombre"] = Nombre
    Usuario["Edad"] = Edad 
    Usuario["Cargo"] = Cargo
    Usuario["Fecha"] = Fecha
    Usuario["Hora"] = Hora
    
    
    
    P = easygui.ynbox ('Cedula: '+ str(Cedula), '¿ES CORRECTA LA INFORMACION?', ('Sí', 'No'))

    O = easygui.ynbox ('Nombre: '+ Nombre, '¿ES CORRECTA LA INFORMACION?', ('Sí', 'No'))

    L = easygui.ynbox ('Edad: '+ str(Edad), '¿ES CORRECTA LA INFORMACION?', ('Sí', 'No'))

    A = easygui.ynbox ('Cargo: '+ Cargo, '¿ES CORRECTA LA INFORMACION?', ('Sí', 'No'))
    
    if P == False:
        print("REINGRESE LOS DATOS")
        
    elif O == False:
        print("REINGRESE LOS DATOS")
        
    elif L == False:
        print("REINGRESE LOS DATOS")
        
    elif A == False:
        print("REINGRESE LOS DATOS")
        
    else:
        video = cv2.VideoCapture(1)
        C = 0
        
        direccion = 'D:/DECIMO/PAE/GIT/face-recognition/train_img/' + Nombre
        dir = os.mkdir(direccion)
            
        while True:
        
            ret, im = video.read()
            #cv2.imshow('Busqueda de Rostro', im)
            nombre_foto = str(uuid.uuid4()) + ".jpg"
            cv2.imwrite(os.path.join(direccion, nombre_foto), im)
            cv2.imwrite("direccion/" + nombre_foto, im)
            print("foto tomada:{}".format(C))
            time.sleep(0.5)
            C = C + 1
        
            if C == 20:
                break
        video.release()
        cv2.destroyAllWindows()
        
        print("Datos almacenados correctamente")
        db['Datos'].insert(Usuario)
        break


'''
def Consulta():
    
    print("INGRESE LA CEDULA QUE DESEA CONSULTAR")
    Cedula = input("CEDULA: ")
    
    info = db['Datos'].find({"Cedula":Cedula})
    
    for Usuario in info:
        User = Usuario['Nombre']
        Ident = Usuario['Cedula']
        Age = Usuario['Edad']
        Charge = Usuario['Cargo']
        Date = Usuario['Fecha']
        Hour = Usuario['Hora']
        
        print("Nombre: " +User)
        print("Edad: " +Age)
        print("Cargo: " +Charge)
        
        
            
#Consulta()
'''