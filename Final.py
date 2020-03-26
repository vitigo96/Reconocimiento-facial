# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:17:49 2019

@author: David Gonzalez
"""
'''
EJECUCION DE TODO EL RPOGRAMA
'''

import os

os.system("identify_video.py")

ruta = "D:/DECIMO/PAE/GIT/face-recognition/Probabilidades/probabilidad.txt"
archivo = open(ruta,'r')
acc = archivo.read()
valor = float(acc)
print(valor)
archivo.close()

while True:
    
    if valor > 0.8:
        registro = True
        break
    else:
        registro = False
        os.system("BD.py")
        os.system("data_preprocess.py")
        os.system("train_main.py")
        os.system("indentify_video.py")
        
        ruta = "D:/DECIMO/PAE/GIT/face-recognition/Probabilidades/probabilidad.txt"
        archivo = open(ruta,'r')
        acc = archivo.read()
        valor = float(acc)
        print(valor)
        archivo.close()
        
    print(registro)