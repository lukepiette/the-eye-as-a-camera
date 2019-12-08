import psdthresh
import requests
import subprocess
import numpy as np
import serial
import colorsys
import time

class slider:
    def __init__(self):
        self.timeeo = 0
        self.sliding_window_len_s = 3
        self.sf = 256
        self.frame_index = 0
        self.window_length = self.sf*self.sliding_window_len_s
        self.buf = np.empty((5,0))

    def classify(self, array):
        freq,psd,idx = psdthresh.calculatePSD(array[4,:], sample_f=256)
        psd = psd[freq>10]
        freq = freq[freq>10]
        psd = psd[freq<50]
        freq = freq[freq<50]
        psdabs = np.abs(psd)
        power = np.sum(psdabs)

        return round(power / 1E9, 2)

    def update(self, buf):
        output=self.classify(buf)
       
        print("Signal metric",output)

    def add_data(self, newbuf):
        self.buf = np.concatenate((self.buf, newbuf), axis = 1)
        self.frame_index += np.shape(newbuf)[1]
        if self.frame_index >= self.window_length:
            self.buf = self.buf[:,np.shape(self.buf)[1]-self.window_length:]
            self.update(self.buf)


