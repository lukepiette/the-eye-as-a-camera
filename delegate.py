import threading
import numpy as np
from bluepy.btle import Scanner, Peripheral, DefaultDelegate
import sys
import time
import bitstring
from time import time, sleep
from datetime import datetime

class PeripheralDelegate(): #delegate for peripheral objects (Muse in this case)
    def __init__(self,callback):
        self.callback = callback
        #globals for callback stuff
        self.timestamps = np.zeros(5)
        self.mainData = np.zeros((5, 12))
        self.last_tm = 0
        # Initial params for the timestamp correction
        # The time it started + the inverse of sampling rate
        self.sample_index = 0
        self.reg_params = np.array([time(), 1./256])
        self.active = True
        #print("Connected muse ", self.addr)
    def unpackEEG(self, packet):
        """Decode data packet of one eeg channel.

        Each packet is encoded with a 16bit timestamp followed by 12 time samples with a 12 bit resolution.
        """
        aa = bitstring.Bits(bytes=packet)
        pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
        uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
        res = aa.unpack(pattern)
        packetIndex = res[0]
        data = res[1:]
        # 12 bits on a 2 mVpp range
        data = 0.48828125 * (np.array(data) - 2048)
        return packetIndex, data

    def handleNotification(self, cHandle, data): #called everytime we receive a new notify from the muse (a new eeg reading)
        """Calback for receiving a samples
        sample are received in this order : 44, 41, 38, 32, 35
        wait until we get 35 and call the data callback
        """
        self.timestamp = time()
        index = int((cHandle - 32) / 3)
        tm, d = self.unpackEEG(data) 

        self.mainData[index] = d
        self.timestamps[index] = self.timestamp
        if cHandle == 35:
            if tm != self.last_tm + 1 and self.last_tm != 0:
                print("---------------OOOOOOOOOOOOOOOOOOOmissing sample %d : %d" % (tm, self.last_tm))
                #print("muse: ", self.addr)
            self.last_tm = tm

            # Calculate index of time samples
            idxs = np.arange(0, 12) + self.sample_index
            self.sample_index += 12

            # Affect as timestamps
            self.timestamps = self.reg_params[1] * idxs + self.reg_params[0]

            # Push data
            self.callback(self.mainData, self.active)
            self.timestamps = np.zeros(5)
            self.data = np.zeros((5, 12))


