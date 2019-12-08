import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def weighted_av():
    root = "./nature_article/take_1"
    #slate = cv2.imread('./nature_article/compost.png', cv2.IMREAD_COLOR)
    slate = np.zeros((960,1486,3))
    aa = np.linspace(0,9.6,49)
    
    for i in range(len(aa)):
        aa[i] = round(aa[i],1)

    for i in range(len(aa)):
        try:
            slate[i*20:(i+1)*20] = cv2.imread(root + "/no"+str(aa[i])+"lr.png")[:20]
        except:
            print("pass",aa[i])
            
    slate = slate.astype(int)
    
    for i in range(len(aa)):
        try:
            slate[i*20:(i+1)*20] = ((slate[i*20:(i+1)*20]*2) + ((slate[(i-1)*20:i*20]+slate[(i+1)*20:(i+2)*20])/2) + ((slate[(i-2)*20:(i-1)*20]*0.5+slate[(i+2)*20:(i+3)*20]*0.5)/2))/3
        except:
            print("skipping",aa[i])
    
    cv2.imwrite('./nature_article/transformed_results/special_compost_new.png', slate.astype(int))

weighted_av()

