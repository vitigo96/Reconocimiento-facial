#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:29:55 2019

@author: elkin
"""


#
#import glob
#import cv2
#
#images = [cv2.imread(file) for file in glob.glob("./Facenet/test_img/*.jpg")]
#
#print(images)

#import cv2
#import glob
#import pylab as plt
#
#folders = glob.glob('./Facenet/test_img/*.jpg')
#imagenames_list = []
#for folder in folders:
#    for f in glob.glob(folder+'/*.jpg'):
#        imagenames_list.append(f)
#
#read_images = []        
#
#for image in imagenames_list:
#    read_images.append(cv2.imread(image, cv2.IMREAD_GRAYSCALE))
#    
#plt.imshow(read_images[0])

# for image in os.listdir('./test_img'):
#            print(image)
#            frame = cv2.imread(os.path.join('./test_img', image))
#        # ret, frame = video_capture.read()
#            #frame = cv2.imread(images[n],0)
#            print(os.listdir('./test_img'))
#            frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

import pylab as plt
import os
#
files = [f for f in os.listdir('./GPIO') if f[-3:] == 'jpg']
img = None
for f in files:
    print(f)
    im=plt.imread('./GPIO/'+ f)
#    if img is None:
    img = plt.imshow(im)
    print("showing")
    #print(f)
#    else:
#        img.set_data(im)
#        print("showing not")
    plt.pause(.1)
    plt.draw()
#    
##y= [1, 2, 3, 4, 5, 6, 7]
#y_pred=[]
#for i in range(7):
#    y=[1]
#    y_pred.append(y[0])
#
#print(y_pred)
#
#import pylab as plt
#from sklearn.metrics import confusion_matrix
#
#y_true=['David', 'David', 'Elkin', 'Elkin', 'David', 'David', 'Elkin', 'David', 'Elkin', 'Elkin']
#y_pred=['David', 'David', 'Elkin', 'Elkin', 'David', 'David', 'Elkin', 'David', 'Elkin', 'Elkin']
##confusion_matrix(y_true, y_pred)
#
#labels = ['David', 'Elkin']
#cm = confusion_matrix(y_true,y_pred, labels)
#print(cm)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#cax = ax.matshow(cm)
#plt.title('Confusion matrix of the classifier')
#fig.colorbar(cax)
#ax.set_xticklabels([''] + labels)
#ax.set_yticklabels([''] + labels)
#plt.xlabel('Predicted')
#plt.ylabel('True')
#plt.show()
#
#

