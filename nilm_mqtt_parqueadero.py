'''
    Solenium (c) 2019. MQTT Subscriber.
'''

import paho.mqtt.subscribe as subscribe
import os, datetime, yaml
import mqtt_utils
import pandas as pd
import random
#import disag_FSM as FSM 
#from disag_utils import n_point_df
import parking_utils
from parking_utils import init_bicycles, detect_event, update_station, assign_bicycle


#Disaggregator object
id_user=1
disag = FSM.disaggregator()
#disag.import_databases(path='Base_de_datos_disag.xlsx',id_user=id_user)
#disag.create_SCES()


frame = ['timestamp', 'app1', 'rpp1']
columns = ['app','rpp']

def mqtt_on_receive(client, userdata, message):

    try:
        d = mqtt_utils.decoder(message.payload)
        data = {f : d[f] for f in frame}
        try:
            disag.n_point_df
        except:
            disag.n_point_df = pd.DataFrame()
        
        disag.n_point_df = n_point_df(disag.n_point_df, data, columns = columns, n=12)

        cl_transients, detected = detect_event(disag.n_point_df, columns = columns, detect_position=4, median_window = 7, N = 4, n=10,
                            niter= 100, kappa = 35, gamma = 0.15, state_threshold = 70, noise_level = 80)

        #Estado inicial disponibles
        try:
            disponibles
        except:
            Z, disponibles, idx_disp = init_bicycles(detected)

        #Cambio de estado disponibles
        if detected == True:
            registro = random.choice([0,1]) #Para probar, 1 es que se hace registro, 0 que no, es decir que el cambio es por desconexión
            Z, disponibles, idx_disp = assign_bicycle(columns, Z, registro, idx_disp, disponibles, detected, cl_transients)
            #sea para conectar o desconectar una bicicleta
    
        #disag.n_point_df = disag.real_time_disag(data, columns = columns, standby_power = 25, detect_position = 4, n=12, median_window = 5,
        #                   niter=100, kappa = 30, gamma=0.15, tolerance=80, state_threshold = 70, noise_level=80,
        #                   metric='linear', large_threshold_distance=0.15, process=1)

        print(disag.n_point_df)
        print ('Las estaciones disponibles de carga son:', idx_disp)
        print(data)
    except Exception as e:
        print('Error: {}'.format(e))

if __name__ == "__main__":
    
    try:    
        subscribe.callback(
            mqtt_on_receive, 
            MQTT_TOPIC,
            hostname=MQTT_HOSTNAME,
            port=MQTT_PORT,
            auth=MQTT_AUTH, 
            qos=2
        )

    except Exception as e:
        print('Error: ' + str(e))
