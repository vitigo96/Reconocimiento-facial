# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:30:40 2019

@author: David Gonzalez
"""

import os
import sys

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

rele = port.PA1
led0 = port.PA12
led1 = port.PA11
led2 = port.PA6

gpio.init()
gpio.setcfg(rele, gpio.INPUT)
gpio.setcfg(led0, gpio.OUTPUT)
gpio.setcfg(led1, gpio.OUTPUT)
gpio.setcfg(led2, gpio.OUTPUT)

try:
    print ("Pulsa CTRL+C para salir")
    while True:
        if gpio.input(port.PA1) == 0:
                gpio.output(led0, 1)
                sleep(0.1)
                gpio.output(led0, 0)
                #sleep(0.1)

                gpio.output(led1, 1)
                sleep(0.1)
                gpio.output(led1, 0)
                #sleep(0.1)

                gpio.output(led2, 1)
                sleep(0.1)
                gpio.output(led2, 0)
                #sleep(0.1)

                sleep(0.6)
except KeyboardInterrupt:
    print ("Saliendo")