import cv2
import numpy as np


slate = cv2.imread('./nature_article/tmp_results/compostv.png', cv2.IMREAD_COLOR)
print(np.shape(slate))
        
for i in range(16):
    p = cv2.imread('./nature_article/take_1/no' + str(i) + 'pass_2v.png')
    if(p is not None):
        for j in range(np.shape(p)[0]):
            print(np.shape(p[j]))
            slate[j,i*100:(i+1)*100] = p[j]

cv2.imwrite('./nature_article/tmp_results/special_compostv.png', slate)
