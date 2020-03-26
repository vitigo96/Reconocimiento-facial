# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:00:45 2019

@author: David Gonzalez
"""

from pymongo import MongoClient
#import pymongo
import cv2

import os
import sys
import time

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

#Conexion con pymongo
mc = MongoClient('mongodb://admin:Suntrack_1m2@54.187.31.198:27017')
db = mc.usuarios

#establecimiento de puertos de orange
Z = [port.PC0, port.PC1, port.PC2, port.PA19, gpio.PA7, gpio.PA8, gpio.PA9, gpio.PA10]

gpio.init()
gpio.setcfg(Z[0], gpio.OUTPUT)
gpio.setcfg(Z[1], gpio.OUTPUT)
gpio.setcfg(Z[2], gpio.OUTPUT)

Usado = [0, 0, 0, 0, 0, 0, 0, 0]

while True:
    Vector=[]
    for i in range(8):
        num = int(input("INGRESE UNOS Y CEROS:"))
        Vector.append(num)
    print("Vector:",Vector)
    print("Usado:",Usado)
    
    consulta = os.system("identify_video")
    
    
    
    print("NOMBRE A QUIEN SE LE ASIGNARA EL CONSUMO")
    Nombre = consulta.result_names
    
    info = db['Datos'].find({"Nombre":Nombre})
    
    for Usuario in info:
        User = Usuario['Nombre']
        Ident = Usuario['Cedula']
        Age = Usuario['Edad']
        Charge = Usuario['Cargo']

        
    Consumo = {}
    
    Consumo["Cedula"] = Ident
    Consumo["Nombre"] = User
    Consumo["Edad"] = Age
    Consumo["Cargo"] = Charge

    for i in range(8):
        if Usado[i]==0:
            gpio.output(Z[i],1) #Energiza el tomacorriente
            time.sleep(1) #tiempo para dejar que la persona conecte su bicicleta
            if Vector[i]==1:  #caso dónde hay un cambio ascendente (0 a 1)
                print("Conector ",i,"Habilitado")
                Hora_Entrada = time.strftime("%X")
                #Registra nuevo usuario en la base de datos
                #Output -> se deja energizado
            else:
                gpio.output(Z[i], 0)
                #caso dónde no hay cambio (0 a 0)
                #output -> se desenergiza
                
        elif Vector[i]==0:   #caso dónde hay un cambio descendente (1 a 0)  
            #Se quita de la base de datos
            Consumo["Consumo"] = Vector[i] #asociar el pin de salida al usuario en la base de datos
            Hora_Salida = time.strftime("%X")
            #Output -> se desenergiza
            gpio.output(Z[i], 0)
        # el caso dónde no hay cambio (1 a 1) quedaría en el caso else:
        #que no se agrega al no importar la condición.
            Consumo["Consumo"] = Hora_Entrada
            Consumo["Consumo"] = Hora_Salida
        
        
    db['Consumo'].insert(Consumo)
    
    Usado = Vector
    