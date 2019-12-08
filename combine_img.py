import cv2
import numpy as np
import math


def run_basic():
    slate = cv2.imread('./nature_article/compost.png', cv2.IMREAD_COLOR)

    positions = np.linspace(0,9.6,49)
    for i in positions:
        ind = round(i,1)
        if(math.floor(ind) == ind):
            ind = math.floor(ind)
        p1 = cv2.imread('./nature_article/take_1/no' + str(ind) + 'lr.png')
        if(p1 is not None ):
    #        slate[i*100:(i+1)*100] = (p1 + np.flip(p2,axis=1)) / 2 # both
            print("reading",ind)
            if(ind > 9):
                print("skipping")
                break
            if(ind == 7.2):
                continue
            slate[int(ind*100):int((ind+1)*100)] = p1  # lr


    cv2.imwrite('./nature_article/raw_results/special_compost1.png', slate)

def fix(num):
    ind = round(num,1)
    if(math.floor(ind) == ind):
        ind = math.floor(ind)
    print(ind)
    return ind
         
def run_averaged():
    slate = cv2.imread('./nature_article/compost.png', cv2.IMREAD_COLOR)

    positions = np.linspace(0,9.6,49)

    for i in range(np.size(positions)):
        ind = round(positions[i],1)
        if(math.floor(ind) == ind):
            ind = math.floor(ind)
            print("newind", ind)
        positions[i] = ind
        print(positions[i])
    
    
    #for edges
    p0 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[0])) + 'lr.png')
    p1 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[1])) + 'lr.png')
    p2 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[2])) + 'lr.png')
    p3 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[3])) + 'lr.png')
    p45 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[45])) + 'lr.png')
    p46 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[46])) + 'lr.png')
    p47 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[47])) + 'lr.png')
    p48 = cv2.imread('./nature_article/take_1/no' + str(fix(positions[48])) + 'lr.png')
    
    row = np.zeros((20,1486,3))
    row += (p0[0:20] * 2) + p1[0:20] + (p2[0:20] / 2) / 3.5
    slate[0:20] = row  # lr

    row = np.zeros((20,1486,3))
    row += (p0[20:40] + p1[20:40]*2 + p2[20:40] + p3[20:40]/2)/4.5
    slate [20:40] = row

    row = np.zeros((20,1486,3))
    row += (p45[0:20]/2 + p46[0:20] + p47[0:20]*2 + p48[0:20])/4.5
    slate [940:960] = row

    row = np.zeros((20,1486,3))
    row += (p46[0:20]*2 + p47[0:20] + p48[0:20]/2)/3.5
    slate [960:980] = row

    for i in range(np.size(positions)):
        if(i <= 1 or i > 46):
            print("skipping", i)
            continue

        validcount = 0
        row = np.zeros((20,1486,3))
        for os in [-2,-1,0,1,2]:
            print(i+os)
            p = cv2.imread('./nature_article/take_1/no' + str(positions[i+os]) + 'lr.png')
            if p is not None:
                validcount+=1
                row += p[:20]

                #accentuate middle
                if(os == 0):
                    row += p[:20]

                #diminish edges
                if(os == -2 or os == 2):
                    row -= (p[:20] / 2)

        row = row / validcount        
        slate[int(round(positions[i]*100)):int(round(positions[i]*100 + 20))] = row  # lr


    cv2.imwrite('./nature_article/raw_results/special_compost1.png', slate)

run_averaged()
