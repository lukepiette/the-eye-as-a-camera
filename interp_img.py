#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:35:54 2019

@author: jeremy
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import cv2


data = cv2.imread('./nature_article/special_compost.png',cv2.IMREAD_COLOR)
horiz = np.array(data[:,:,0])
datav = cv2.imread('./nature_article/special_compostv.png',cv2.IMREAD_COLOR)
vert = np.array(datav[:,:,0])

combined = (horiz[100:900,:] + vert[:,100:1550] )/ 2
#cv2.imshow('bobsuruncle', combined)
cv2.imwrite('interp.png', combined)
#cv2.imshow('billy', data)


"""for just horiz lr, taken from horiz"""
#x = np.arange(np.shape(horiz)[1])
#y = 50
#z = horiz[50]

x = np.arange(np.shape(horiz)[1])
y = np.arange(10)*100 + 50
points = np.empty((np.size(y)  * np.size(x), 2))
for i in range(np.size(y))
z = horiz[y]

inter = scipy.interpolate.interp2d(x,y,z, kind='linear')
#result = inter()


nx, ny = horiz.shape[1], horiz.shape[0]
X, Y = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))

#phil = scipy.interpolate.griddata(horiz, np.real(divs2), tuple(np.meshgrid(np.arange(W), np.arange(H))), method='linear')
#X= positions[0][int(window_length/2):int(-window_length/2)]
#Y=positions[1][int(window_length/2):int(-window_length/2)]
#phil = scipy.interpolate.griddata(np.array([x, y]).T, np.real(divs2), np.array([X,Y)], method='linear')

#plt.imshow(phil)