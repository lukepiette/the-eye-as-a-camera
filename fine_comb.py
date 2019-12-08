import cv2
import numpy as np


def grey(value, bot=0,top=150):
    return((value,value,value))

slate = np.empty((80,1760,3))
ind = -1
for i in [9, 9.2, 9.4, 9.6, 9.8]:
    p1 = cv2.imread('./nature_article/take_1/no' + str(i) + 'lr.png')
    ind +=1
    print(np.shape(p1), i)
    if(p1 is not None):
        slate[ind*16:(ind+1)*16] = p1[:16]  # lr


cv2.imwrite('./nature_article/cameratry.png', slate)
 
