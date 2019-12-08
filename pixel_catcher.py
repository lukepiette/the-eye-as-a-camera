import muse2
import psdthresh
import os
import sys
import numpy as np
import datetime 
import threading
import time
from time import sleep
import muse_MACs
import eyecam_pixel
import argparse
import cmd
import sliderconnection


class pixel_catcher():
    
    def __init__(self):
        self.conn_q = sliderconnection.slider()
        self.shutter_spd = 8
        self.target_f = 15
        self.iso = 100
        self.samplingFreq=256
        self.samplingTime=int(self.samplingFreq*self.shutter_spd)
        self.mode = 'capture'
        self.pixel_val = ()

        self.yind = 0
        self.cnt=0
        self.active = False
        self.ys1=[]
        self.ys2=[]
        self.ys3=[]
        self.ys4=[]
        self.ys5=[]
        self.raw_5 = []
        self.raw_cap = False
        self.raw_result = []
        
        self.myMuse = muse2.Muse(callback=self.eeg, address=muse_MACs.myaddress)
        self.p1=threading.Thread(target=self.myMuse.runListener).start()
        print("setup complete")

    def getPSD(self,y1,y2,y3,y4,y5):
        self.ys1=[]
        self.ys2=[]
        self.ys3=[]
        self.ys4=[]
        self.ys5=[]
        self.cnt = 0

        c1=np.array(y1);
        c2=np.array(y2);
        c3=np.array(y3);
        c4=np.array(y4);
        c5=np.array(y5);
        newarr=np.column_stack((c1,c2,c3,c4,c5)).transpose();
        
        if(self.mode == 'capture'):
            self.pixel_val = eyecam_pixel.bulb(newarr[4,:], self.shutter_spd, self.target_f, self.iso)
            print("pixel_value: ", self.pixel_val)
            f = open("pixeldata.txt", 'a')
            f.write(str(self.pixel_val) + ", " + str(datetime.datetime.now()) + "\n")
            self.active = False

        elif(self.mode == 'rms'):
            freq,psd,idx = psdthresh.calculatePSD(newarr[4,:], sample_f=256)
            psd = psd[freq>10]
            freq = freq[freq>10]
            psd = psd[freq<50]
            freq = freq[freq<50]
            psdabs = np.abs(psd)
            power = np.sum(psdabs)

            print(round(power / 1E9, 2))


    def eeg(self, data, trash = True):
        if(self.active):
            if(not self.raw_cap):
                self.cnt += 12
                
                for i in range(12):
                    self.ys1.append(data[0][i])
                    self.ys2.append(data[1][i])
                    self.ys3.append(data[2][i])
                    self.ys4.append(data[3][i])
                    self.ys5.append(data[4][i])
                dif = self.cnt % self.samplingTime
                if(self.cnt >= self.samplingTime and dif >=0 and dif < 12):
                    t1=self.ys1[:self.samplingTime]
                    t2=self.ys2[:self.samplingTime]
                    t3=self.ys3[:self.samplingTime]
                    t4=self.ys4[:self.samplingTime]
                    t5=self.ys5[:self.samplingTime]
                    self.getPSD(t1,t2,t3,t4,t5)

            elif(self.raw_cap):
                self.cnt += 12
                for i in range(12):
                    self.raw_5.append(data[4][i])
                dif = self.cnt % self.samplingTime
                if(self.cnt >= self.samplingTime and dif >=0 and dif < 12):
                    print("raw captured, saving to file")
                    np.save('./raw_out.npy', self.raw_5)
                    self.raw_result = self.raw_5
                    self.raw_5 = []
                    self.raw_cap = False
                    self.active = False
                    self.cnt = 0

    #                f = open("./rawdata.txt", 'a')
#                f.write(str(self.raw_5) + ", " + str(datetime.datetime.now()) + "\n")


