# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:00:45 2019

@author: David Gonzalez
"""

#from pymongo import MongoClient
import os
import sys
import time
import random
import pandas as pd
from datetime import datetime
from time import sleep
#from pyA20.gpio import gpio
#from pyA20.gpio import port

from data import preprocessing
from edge_detector import find_steady_states
#import disag_FSM as FSM 


class disaggregator:
    def __init__(self):
        self.n_point_df=pd.DataFrame() 


def n_point_df(n_point_df, dictionary, columns = ['app1'], n=10):

    point_timestamp = dictionary['timestamp']/1000
    dt = datetime.fromtimestamp(point_timestamp)
    date = dt.date()
    hour = dt.time()
    dictionary.update({'date': date, 'time': hour})
    point = pd.DataFrame()

    for key in dictionary:
        point[key] = pd.Series(dictionary[key])
    point = point.set_index('timestamp')
    cols_hist = ['date', 'time']
    cols_hist.extend(columns)

    # return point
    n_point_df = n_point_df.append(point[columns])

    if (len(n_point_df) == n+1):
        assert n_point_df.shape[0] == n+1, "tamaño de arreglo mayor a n filas"
        n_point_df = n_point_df.drop(n_point_df.iloc[0:1].index)

    return n_point_df


def detect_event(n_point_df, columns = ['app1'], detect_position=4, median_window = 7, N = 4, n=10,
                            niter= 100, kappa = 35, gamma = 0.15, state_threshold = 70, noise_level = 80):

    var_med_an_npdf = preprocessing(n_point_df, columns = columns, m = median_window, S=1, N = N, niter = niter, kappa = kappa, gamma = gamma)

    [cl_steady, cl_transients] = find_steady_states(
        var_med_an_npdf, n_point = True, columns = columns, n=detect_position, state_threshold = state_threshold,
        noise_level = noise_level)

    n_point_df = var_med_an_npdf

    if cl_transients.empty:
        detected = False
    else:
        detected = True
    
    return cl_transients, detected

def init_bicycles(detected):

    #establecimiento de puertos de orange
    #Z = [port.PC0, port.PC1]
    pass


def update_station(disponibles, assigned_station, update = True):
    #Actualizar estaciones disponibles
    disponibles[assigned_station] = update
    idx_disp = [i for i in disponibles.keys() if disponibles[i] == True] 

    return disponibles, idx_disp


def init_bicycles(detected):

    #establecimiento de puertos de orange
    #Z = [port.PC0, port.PC1, port.PC2, port.PA19, gpio.PA7, gpio.PA8, gpio.PA9, gpio.PA10]
    Z = [0,0,0,0,0,0,0,0] #Todos los puertos desenergizados inicialmente

    n_estaciones = len(Z)

    # gpio.init()
    # gpio.setcfg(Z[0], gpio.OUTPUT)
    # gpio.setcfg(Z[1], gpio.OUTPUT)
    # gpio.setcfg(Z[2], gpio.OUTPUT)

    # usado = [0]*n_estaciones
    # estado = [0]*n_estaciones
    disponibles = {i:True for i in range(1,len(Z)+1)} #Keys de 1 hasta el número de estacionse de carga

    #Revisar estado inicial
    for i in range(n_estaciones):
        #gpio.output(Z[i],1) #Energiza el tomacorriente
        Z[i]= 1 #Energiza el tomacorriente de una de ellas

    for key,value in disponibles.items():
        #gpio.output(Z[key-1],0) #Desenergiza el tomacorriente de una de ellas
        Z[key-1]=0 #Desenergiza el tomacorriente de una de ellas

        time_permitted = 1 #número de segundos
        start = time.time() #Se inicia conteo de tiempo que tiene la persona antes de que se evalúe 
        #apagar la estación si no hubo un cambio positivo en la señal (osea, si no se conectó)
        time_since_activation = 0

        print('starts count init for station', key)
        while time_since_activation < time_permitted: 
            now = time.time()
            time_since_activation = now-start

            if detected == True:
                disponibles[key] = False
                #gpio.output(Z[key-1],1) #Si está ocupada, se reenergiza
                Z[key-1]= 1 #Energiza el tomacorriente de una de ellas
                break
        print('ends count init for station', key)

    idx_disp = [i for i in disponibles.keys() if disponibles[i] == True] #los índices de las estaciones disponibles
    print('Estaciones disponibles:', idx_disp)
    return Z, disponibles, idx_disp
    

def assign_bicycle(columns, Z, registro, idx_disp, disponibles, detected, cl_transients):

    '''
    Cuando alguien hace su registro, se evalúa cuáles estaciones está disponibles en ese momento, y al azar escoge una estación (al azar,
    o siguiendo quizá algún orden optimizador?)
    Se actualiza el vector con la estación donde se conecta (se hace la prueba de que efectivamente se conectó)
    Cuando se desconecta se desenergiza intermitentemente para saber cuál estación se saca de las ocupadas y se vuelve a poner disponible.
    '''

    if registro == True: #Se registra alguien
        assigned_station = random.choice(idx_disp) #Aleatorio entre las estaciones disponibles
        print ('Station assigned:', assigned_station)
        #gpio.output(Z[assigned_station],1) #Energiza el tomacorriente
        Z[assigned_station-1] = 1 #Energiza el tomacorriente
        #Actualizar estaciones disponibles
        disponibles, idx_disp = update_station(disponibles, assigned_station, update = False)

        print ('Estación de carga', assigned_station, ' activada')
        
        start = time.time() #Se inicia conteo de tiempo que tiene la persona antes de que se evalúe 
        #apagar la estación si no hubo un cambio positivo en la señal (osea, si no se conectó)
        time_since_activation = 0
        connected = False
        time_permitted = 1

        print('starts count connect')
        while time_since_activation < time_permitted: 
            now = time.time()
            time_since_activation = now-start

            #if (detected == True) and (cl_transients[columns[0]].iloc[0] > 0): # es decir, si se conectó la bicicleta
            if (detected == True): # es decir, si se conectó la bicicleta

                print ('Bicicleta conectada!')
                connected = True
                break

        print('ends count connect')
            
        if connected == False: #Event never detected in allotted time, bicycle never connected
            #gpio.output(Z[assigned_station],0) #Desenergiza el tomacorriente
            Z[assigned_station-1] = 0 #Desenergiza el tomacorriente
            print('Tiempo para conexión expirado. Estación de carga', assigned_station, ' se ha desactivado')
            #Actualizar estaciones disponibles
            disponibles, idx_disp = update_station(assigned_station, update = True)

        print('Estaciones disponibles:', idx_disp)
    
    else:
    #if (detected == True) and (cl_transients[columns[0]].iloc[0] < 0): #Un evento detectado fuera del registro sólo debería corresponder a una bicicleta desconectada
        #Revisar en cuál estación de carga ocurrió el cambio
        idx_not_disp = [i for i in disponibles.keys() if disponibles[i] == False] #los índices de las estaciones no disponibles

        assigned_station = random.choice(idx_not_disp) #Aleatorio entre las estaciones disponibles
        print ('Station assigned:', assigned_station)
        #gpio.output(Z[assigned_station],0) #Desenergiza el tomacorriente
        Z[assigned_station-1] = 0 #Desenergiza el tomacorriente

        #Actualizar estaciones disponibles
        disponibles, idx_disp = update_station(disponibles, assigned_station, update = True)

        print ('Estación de carga', assigned_station, ' de nuevo disponible')
 
        '''
        Dado que en las pruebas no es fácil simular la desconexión propiamente se decide desconectar a través de un aleatorio
        Sin embargo, el siguiente código debería ser probado para el caso real de desconexión, en el que se buscar a través de apagado intermitente
        de la energía en los cargadores activos para ver en cuál se desconectó y ese actualizarlo (volver a activarlo)

        for i in idx_not_disp:
            #gpio.output(Z[i],0) #Se desenergiza el tomacorriente para ver si no hay cambio en la señal de potencia, es decir si se desconectó allí
            Z[i-1] = 0 #Desenergiza el tomacorriente

            time_permitted = 1 #número de segundos
            start = time.time() #Se inicia conteo de tiempo que tiene la persona antes de que se evalúe 
            #apagar la estación si no hubo un cambio positivo en la señal (osea, si no se conectó)
            time_since_activation = 0
            
            print('starts count disconnect for station', i)
            while time_since_activation < time_permitted: 
                now = time.time()
                time_since_activation = now-start

                if (detected == True): #Es decir, si baja la señal de potencia al desenergizar una de las estaciones, significa que esa estación está ocupada
                    #gpio.output(Z[i],1) #Volver a energizar porque allí sigue una bicicleta
                    Z[i-1] = 1 #Energiza el tomacorriente
                    time_since_activation = time_permitted #para salir del ciclo sin seguir iterando
                    
                else: #si no se detecta evento es allí de donde se sacó la bicicleta, volver a poner entonces disponible 
                    disponibles[key] = True
                    #Actualizar estaciones disponibles
                    disponibles, idx_disp = update_station(key, update = True)
                    ('Estación de carga', key, 'de nuevo disponible')
            
            
            print('ends count disconnect for station', i)
        '''
        print('Estaciones disponibles:', idx_disp)

    return Z, disponibles, idx_disp









    '''
    #Conexion con pymongo
    mc = MongoClient('mongodb://admin:Suntrack_1m2@34.209.47.60:27017')
    db = mc.usuarios

    for i in range(len(Z)): 
        gpio.output(Z[i],1) #Energiza el tomacorriente
    print("Vector:",Vector)
    print("Usado:",Usado)

    # for i in range(8):
    #     num = int(input("INGRESE UNOS Y CEROS:"))
    #     Vector.append(num)
    # print("Vector:",Vector)
    # print("Usado:",Usado)
    
    # print("INGRESE LA CEDULA QUE DESEA ASIGNAR EL CONSUMO")
    # Cedula = input("CEDULA: ")
    
    # info = db['Datos'].find({"Cedula":Cedula})   

    # Consumo = {}

    if not(cl_transients.empty): #Si hay un cambio de estado de algún dispositivo
                self.df_transients = self.df_transients.append(cl_transients.iloc[0]) #se le anexa el nuevo transiente
                diff = []
                time = cl_steady[columns[0]].index[0]
                event = cl_steady[columns[0]].iloc[0]
                self.steady_state_init.append([time,event]) #se anexa el timestamp para escoger reiniciar las listas que empiezan en el timestamp que se cierre
                #también se anexa en bajadas (cl_transients < 0) para tener en cuenta bajadas de nivel en que no hay matching, para que tenga en cuenta como referencia para reiniciar listas

    #######Agregar un boolean de si el cambio de estado fue de conexión o de desconexión y según eso discriminar cuáles estaciones revisar##########

    for i in range(len(Z)):
        if usado[i] == 0: #Estaba apagado
            gpio.output(Z[i],0) #Energiza el tomacorriente 
        gpio.output(Z[i],1) #Energiza el tomacorriente 
        time.sleep(1) #tiempo para dejar que la persona conecte su bicicleta


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
    '''
